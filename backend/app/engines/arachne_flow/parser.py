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


def parse_flow_file(path: Path, base_dir: Optional[Path] = None, _seen: Optional[Set[Path]] = None) -> ParsedFlow:
    """Parse a flow YAML file, recursively inlining included flows.

    Args:
        path: Path to the YAML file.
        base_dir: Directory used to resolve relative include paths. Defaults to
            the parent directory of ``path``.
        _seen: Internal set used to detect circular includes.

    Returns:
        A normalized ParsedFlow object.
    """
    path = Path(path).resolve()
    if base_dir is None:
        base_dir = path.parent
    if _seen is None:
        _seen = set()

    if path in _seen:
        raise FlowParseError(f"circular include detected: {path}")
    _seen.add(path)

    try:
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    except Exception as exc:
        raise FlowParseError(f"failed to load {path}: {exc}") from exc

    if raw is None:
        raw = {}

    try:
        doc = FlowDocument.model_validate(raw)
    except Exception as exc:
        raise FlowParseError(f"invalid flow document {path}: {exc}") from exc

    flow_id = path.stem
    parsed = ParsedFlow(
        schema_version=doc.schema_version,
        title=doc.title,
        root_product=doc.root_product,
        flow_id=flow_id,
        includes=[],
        locals=dict(doc.local),
        resources={},
        actions={},
        methods={},
        triples=[],
    )

    # Inline includes first so later triples can reference them.
    for include_name in doc.include or []:
        include_path = (base_dir / include_name).resolve()
        if not include_path.exists():
            raise FlowParseError(f"include file not found: {include_name} (looked in {base_dir})")
        included = parse_flow_file(include_path, base_dir=base_dir, _seen=_seen)
        parsed.includes.append(include_name)
        # Merge locals and triples. ACTIONs from included flows keep their own
        # flow_id namespace so they remain distinct occurrences.
        parsed.locals.update(included.locals)
        parsed.triples.extend(included.triples)
        # Resources/methods are shared by ID; actions are namespaced below.
        for res in included.resources.values():
            parsed.resources.setdefault(res.resource_id, res)
        for method in included.methods.values():
            parsed.methods.setdefault(method.method_id, method)
        for action in included.actions.values():
            parsed.actions.setdefault(action.action_id, action)

    # Add this file's own locals and triples.
    parsed.locals.update(doc.local)
    for group in doc.edges:
        for raw_triple in group:
            parsed.triples.append(
                FlowTriple(source=raw_triple[0], predicate=raw_triple[1], target=raw_triple[2])
            )

    _normalize_and_validate(parsed)
    return parsed


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
            # [RESOURCE, input_role, ACTION]
            kind_hints["resource"].add(src)
            kind_hints["action"].add(tgt)
        elif pred in {r.value for r in OutputRole}:
            # [ACTION, output_role, RESOURCE]
            kind_hints["action"].add(src)
            kind_hints["resource"].add(tgt)
        elif pred == SpecialRole.NEXT.value:
            # [ACTION, next, ACTION]
            kind_hints["action"].add(src)
            kind_hints["action"].add(tgt)
        elif pred == SpecialRole.REF.value:
            # [ACTION, ref, METHOD]
            kind_hints["action"].add(src)
            kind_hints["method"].add(tgt)

    # METHOD/resource conflicts are still disallowed because the design doc
    # keeps those classes disjoint.
    for node_id in kind_hints["resource"] & kind_hints["method"]:
        raise FlowParseError(
            f"node '{node_id}' is used both as a RESOURCE and as a METHOD"
        )
    for node_id in kind_hints["action"] & kind_hints["method"]:
        raise FlowParseError(
            f"node '{node_id}' is used both as an ACTION and as a METHOD"
        )

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
            if src not in valid_actions or tgt not in valid_resources:
                raise FlowParseError(
                    f"invalid output-role triple [{src}, {pred}, {tgt}]: "
                    "expected [ACTION, output_role, RESOURCE]"
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


def _build_graph(parsed: ParsedFlow) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Build adjacency lists for directed and undirected graphs."""
    directed: Dict[str, List[str]] = {node: [] for node in _all_flow_nodes(parsed)}
    undirected: Dict[str, List[str]] = {node: [] for node in _all_flow_nodes(parsed)}

    input_roles = {r.value for r in InputRole}
    output_roles = {r.value for r in OutputRole}

    for triple in parsed.triples:
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
