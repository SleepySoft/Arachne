"""
Arachne-flow YAML parser and validator.

Parses flow documents, inlines `include` references, validates triple patterns,
and checks that the resulting graph is a single connected DAG.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml

from app.engines.arachne_flow.schemas import (
    ActionType,
    FlowAction,
    FlowDocument,
    FlowMethod,
    FlowResource,
    FlowTriple,
    InputRole,
    OutputRole,
    ParsedFlow,
    ResourceType,
    SpecialRole,
)


class FlowParseError(Exception):
    """Raised when a flow document is structurally invalid."""


class FlowValidationError(Exception):
    """Raised when a parsed flow fails DAG or connectivity checks."""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_flow_content(content: str, flow_id: str) -> ParsedFlow:
    """Parse a flow YAML document from a string.

    ``include`` is a **dependency declaration**, not textual inclusion: the
    current document only parses its own ``edges``, and the builder resolves
    cross-file references through globally shared RESOURCE/METHOD nodes.

    Args:
        content: YAML text of the flow document.
        flow_id: Flow identifier used for namespacing ACTION occurrences.

    Returns:
        A normalized ParsedFlow object.
    """
    try:
        raw = yaml.safe_load(content)
    except Exception as exc:
        raise FlowParseError(f"invalid YAML: {exc}") from exc

    if raw is None:
        raw = {}

    try:
        doc = FlowDocument.model_validate(raw)
    except Exception as exc:
        raise FlowParseError(f"invalid flow document: {exc}") from exc

    parsed = ParsedFlow(
        schema_version=doc.schema_version,
        title=doc.title,
        root_product=doc.root_product,
        flow_id=flow_id,
        includes=list(doc.include or []),
        locals=dict(doc.local),
        resources={},
        actions={},
        methods={},
        triples=[],
    )

    # Parse only this document's own triples. Included flows are dependencies,
    # not text to inline.
    for raw_triple in doc.edges:
        parsed.triples.append(
            FlowTriple(source=raw_triple[0], predicate=raw_triple[1], target=raw_triple[2])
        )

    _normalize_and_validate(parsed)
    return parsed


def parse_flow_file(path: Path, base_dir: Optional[Path] = None, _seen: Optional[Set[Path]] = None) -> ParsedFlow:
    """Parse a flow YAML file.

    Args:
        path: Path to the YAML file.
        base_dir: Unused, kept for backward compatibility.
        _seen: Unused, kept for backward compatibility.

    Returns:
        A normalized ParsedFlow object.
    """
    path = Path(path).resolve()

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:
        raise FlowParseError(f"failed to load {path}: {exc}") from exc

    return parse_flow_content(content, flow_id=path.stem)


# ---------------------------------------------------------------------------
# Normalization & validation
# ---------------------------------------------------------------------------


def _normalize_and_validate(parsed: ParsedFlow) -> None:
    """Infer node kinds, validate triple patterns, and check DAG/connectivity."""
    _infer_node_kinds(parsed)
    _validate_triple_patterns(parsed)
    _build_graph(parsed)
    _validate_single_connected_component(parsed)
    _validate_acyclic(parsed)


def _infer_node_kinds(parsed: ParsedFlow) -> None:
    """Infer whether each node is a resource, action, or method.

    Nodes that appear both as a resource and as an action are treated as
    dual-role nodes. This can happen when a generated flow reuses a legacy
    process ID (e.g. ``chip_design``) both as an ACTION and as an information
    input to another ACTION. The compiler creates a single Neo4j node carrying
    both labels for such cases.
    """
    # kind -> set of node ids
    kind_hints: Dict[str, Set[str]] = {
        "resource": set(),
        "action": set(),
        "method": set(),
    }

    for triple in parsed.triples:
        pred = triple.predicate
        src, tgt = triple.source, triple.target

        if pred in {r.value for r in InputRole}:
            # [RESOURCE, input_role, ACTION] or [RESOURCE, input_role, METHOD]
            kind_hints["resource"].add(src)
            kind_hints["action"].add(tgt)
            kind_hints["method"].add(tgt)
        elif pred in {r.value for r in OutputRole}:
            # [ACTION, output_role, RESOURCE] or [METHOD, output_role, RESOURCE]
            kind_hints["action"].add(src)
            kind_hints["method"].add(src)
            kind_hints["resource"].add(tgt)
        elif pred == SpecialRole.NEXT.value:
            # [ACTION, next, ACTION]
            kind_hints["action"].add(src)
            kind_hints["action"].add(tgt)
        elif pred == SpecialRole.REF.value:
            # [ACTION, ref, METHOD]
            kind_hints["action"].add(src)
            kind_hints["method"].add(tgt)

    # Build normalized node objects (dual nodes appear in both dicts)
    resource_ids = kind_hints["resource"]
    action_ids = kind_hints["action"]
    method_ids = kind_hints["method"]

    for rid in resource_ids:
        parsed.resources[rid] = FlowResource(
            resource_id=rid,
            resource_type=ResourceType.OTHER,
            local_name=parsed.locals.get(rid),
        )

    for aid in action_ids:
        # Default action type is OTHER; callers can override via compiler/engine.
        parsed.actions[aid] = FlowAction(
            action_id=aid,
            action_type=ActionType.OTHER,
            flow_id=parsed.flow_id,
        )

    for mid in method_ids:
        parsed.methods[mid] = FlowMethod(method_id=mid)

    # Record ref relationships on actions
    for triple in parsed.triples:
        if triple.predicate == SpecialRole.REF.value:
            action = parsed.actions.get(triple.source)
            if action:
                action.method_ref = triple.target


def _validate_triple_patterns(parsed: ParsedFlow) -> None:
    """Ensure every triple matches one of the four allowed patterns."""
    input_roles = {r.value for r in InputRole}
    output_roles = {r.value for r in OutputRole}

    # A node is a valid resource if it was ever used as a resource; a valid
    # action if it was ever used as an action. Dual-role nodes satisfy both.
    valid_resources = set(parsed.resources.keys())
    valid_actions = set(parsed.actions.keys())
    valid_methods = set(parsed.methods.keys())

    for triple in parsed.triples:
        pred = triple.predicate
        src, tgt = triple.source, triple.target

        if pred in input_roles:
            if src not in valid_resources or tgt not in valid_actions:
                raise FlowParseError(
                    f"invalid input-role triple [{src}, {pred}, {tgt}]: "
                    "expected [RESOURCE, input_role, ACTION]"
                )
        elif pred in output_roles:
        pred = triple.predicate
        src, tgt = triple.source, triple.target

        # next and input/output role edges participate in the flow DAG.
        if pred in input_roles:
            directed[src].append(tgt)
        elif pred in output_roles:
            directed[src].append(tgt)
        elif pred == SpecialRole.NEXT.value:
            directed[src].append(tgt)
        # ref edges do not participate in the DAG but do connect the graph.

        undirected[src].append(tgt)
        undirected[tgt].append(src)

    parsed._directed_adj = directed  # type: ignore[attr-defined]
    parsed._undirected_adj = undirected  # type: ignore[attr-defined]
    return directed, undirected


def _all_flow_nodes(parsed: ParsedFlow) -> Set[str]:
    return (
        set(parsed.resources.keys())
        | set(parsed.actions.keys())
        | set(parsed.methods.keys())
    )


def _validate_single_connected_component(parsed: ParsedFlow) -> None:
    nodes = _all_flow_nodes(parsed)
    if not nodes:
        raise FlowValidationError("flow contains no nodes")

    adj = getattr(parsed, "_undirected_adj", None)
    if adj is None:
        raise RuntimeError("_build_graph must be called before connectivity check")

    start = next(iter(nodes))
    visited: Set[str] = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in adj.get(current, []):
            if neighbor not in visited:
                stack.append(neighbor)

    if visited != nodes:
        isolated = nodes - visited
        raise FlowValidationError(
            f"flow is not a single connected graph; isolated nodes: {sorted(isolated)}"
        )


def _validate_acyclic(parsed: ParsedFlow) -> None:
    adj = getattr(parsed, "_directed_adj", None)
    if adj is None:
        raise RuntimeError("_build_graph must be called before cycle check")

    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[str, int] = {node: WHITE for node in adj}
    path: List[str] = []

    def visit(node: str) -> None:
        color[node] = GRAY
        path.append(node)
        for neighbor in adj.get(node, []):
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                raise FlowValidationError(
                    f"cycle detected in flow: {' -> '.join(cycle)}"
                )
            if color[neighbor] == WHITE:
                visit(neighbor)
        path.pop()
        color[node] = BLACK

    for node in adj:
        if color[node] == WHITE:
            visit(node)
        if pred in input_roles:
            # Allow [RESOURCE, input_role, ACTION] or [RESOURCE, input_role, METHOD]
            valid_targets = valid_actions | valid_methods
            if src not in valid_resources or tgt not in valid_targets:
                raise FlowParseError(
                    f"invalid input-role triple [{src}, {pred}, {tgt}]: "
                    "expected [RESOURCE, input_role, ACTION] or [RESOURCE, input_role, METHOD]"
                )
        elif pred in output_roles:
            # Allow [ACTION, output_role, RESOURCE] or [METHOD, output_role, RESOURCE]
            valid_sources = valid_actions | valid_methods
            if src not in valid_sources or tgt not in valid_resources:
                raise FlowParseError(
                    f"invalid output-role triple [{src}, {pred}, {tgt}]: "
                    "expected [ACTION, output_role, RESOURCE] or [METHOD, output_role, RESOURCE]"
                )
        elif pred == SpecialRole.NEXT.value:
            if src not in valid_actions or tgt not in valid_actions:
                raise FlowParseError(
                    f"invalid next triple [{src}, {pred}, {tgt}]: "
                    "expected [ACTION, next, ACTION]"
                )
        elif pred == SpecialRole.REF.value:
            if src not in valid_actions or tgt not in valid_methods:
                raise FlowParseError(
                    f"invalid ref triple [{src}, {pred}, {tgt}]: "
                    "expected [ACTION, ref, METHOD]"
                )
