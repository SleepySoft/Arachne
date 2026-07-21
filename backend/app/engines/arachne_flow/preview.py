"""Preview arachne-flow YAML content without persisting to Neo4j.

This module parses a flow document (plus its included dependencies), builds an
in-memory graph, and converts it to the generic ``GraphNode``/``GraphEdge``
shapes used by the frontend canvas. It is used by the ``POST /flows/preview``
endpoint.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from app.engines.arachne_flow.builder import FlowGraph, FlowGraphBuilder
from app.engines.arachne_flow.parser import FlowParseError, parse_flow_content, parse_flow_file
from app.engines.arachne_flow.schemas import (
    FlowResource,
    FlowTriple,
    InputRole,
    OutputRole,
    ResourceType,
)
from app.models.core import GraphEdge, GraphNode
from app.services import node_storage

FLOW_DIR = Path(__file__).resolve().parents[4] / "data" / "flows" / "semiconductor"


async def flow_graph_to_graph_elements(graph: FlowGraph) -> Tuple[List[GraphNode], List[GraphEdge]]:
    """Convert an in-memory FlowGraph to generic graph nodes/edges.

    Labels are resolved from PostgreSQL ``industrial_nodes`` where available;
    ACTION nodes borrow their label from the referenced METHOD.

    Each node carries a ``flow_ids`` property listing which flows reference it,
    so the frontend can decide how to collapse/expand flow groups.
    """
    resource_ids = set(graph.resources.keys())
    method_ids = set(graph.methods.keys())
    action_method_refs = {a.method_ref for a in graph.actions.values() if a.method_ref}
    meta_map = await node_storage.get_nodes_by_ids(
        list(resource_ids | method_ids | action_method_refs)
    )

    # Map each node id to the set of flow ids that reference it.
    node_flow_ids: Dict[str, Set[str]] = {}
    for triple, flow_id in graph.triples:
        node_flow_ids.setdefault(triple.source, set()).add(flow_id)
        node_flow_ids.setdefault(triple.target, set()).add(flow_id)

    nodes: List[GraphNode] = []
    dual_ids = graph.dual_node_ids()

    # RESOURCE and dual-role nodes
    for rid, res in graph.resources.items():
        meta = meta_map.get(rid)
        label = (meta.canonical_name_zh if meta else None) or res.local_name or rid
        if rid.startswith("flow_folder:"):
            folder_name = res.local_name or rid.replace("flow_folder:", "")
            nodes.append(
                GraphNode(
                    node_id=rid,
                    label=f"📁 {folder_name}",
                    entity_type="arachne_flow:folder",
                    properties={
                        "node_kind": "folder",
                        "is_flow_folder": True,
                        "flow_id": folder_name,
                        "flow_ids": [folder_name],
                    },
                )
            )
            continue
        if rid in dual_ids:
            action = graph.actions[rid]
            nodes.append(
                GraphNode(
                    node_id=rid,
                    label=label,
                    entity_type="arachne_flow:dual",
                    properties={
                        "node_kind": "dual",
                        "resource_type": res.resource_type.value,
                        "action_type": action.action_type.value,
                        "local_name": res.local_name,
                        "original_action_id": action.action_id,
                        "method_ref": action.method_ref,
                        "flow_id": action.flow_id,
                        "flow_ids": sorted(node_flow_ids.get(rid, [])),
                        "canonical_name_zh": meta.canonical_name_zh if meta else None,
                        "canonical_name_en": meta.canonical_name_en if meta else None,
                    },
                )
            )
        else:
            nodes.append(
                GraphNode(
                    node_id=rid,
                    label=label,
                    entity_type="arachne_flow:resource",
                    properties={
                        "node_kind": "resource",
                        "resource_type": res.resource_type.value,
                        "local_name": res.local_name,
                        "flow_ids": sorted(node_flow_ids.get(rid, [])),
                        "canonical_name_zh": meta.canonical_name_zh if meta else None,
                        "canonical_name_en": meta.canonical_name_en if meta else None,
                    },
                )
            )

    # METHOD nodes
    for mid, method in graph.methods.items():
        meta = meta_map.get(mid)
        label = (meta.canonical_name_zh if meta else None) or method.method_name or mid
        nodes.append(
            GraphNode(
                node_id=mid,
                label=label,
                entity_type="arachne_flow:method",
                properties={
                    "node_kind": "method",
                    "method_name": method.method_name or mid,
                    "flow_ids": sorted(node_flow_ids.get(mid, [])),
                    "canonical_name_zh": meta.canonical_name_zh if meta else None,
                    "canonical_name_en": meta.canonical_name_en if meta else None,
                },
            )
        )

    # ACTION nodes (non-dual)
    for aid, action in graph.actions.items():
        if aid in dual_ids:
            continue
        method_ref = action.method_ref
        meta = meta_map.get(method_ref) if method_ref else None
        label = (meta.canonical_name_zh if meta else None) or action.action_id
        nodes.append(
            GraphNode(
                node_id=aid,
                label=label,
                entity_type="arachne_flow:action",
                properties={
                    "node_kind": "action",
                    "action_type": action.action_type.value,
                    "original_action_id": action.action_id,
                    "method_ref": method_ref,
                    "flow_id": action.flow_id,
                    "flow_ids": sorted(node_flow_ids.get(aid, [])),
                    "canonical_name_zh": meta.canonical_name_zh if meta else None,
                    "canonical_name_en": meta.canonical_name_en if meta else None,
                },
            )
        )

    edges: List[GraphEdge] = []
    for idx, (triple, flow_id) in enumerate(graph.triples):
        edge_id = f"{flow_id}:{triple.source}->{triple.target}:{triple.predicate}"
        edges.append(
            GraphEdge(
                edge_id=edge_id,
                from_node=triple.source,
                to_node=triple.target,
                edge_namespace="arachne_flow",
                edge_type=triple.predicate,
                properties={"flow_id": flow_id},
            )
        )

    return nodes, edges


def _add_with_includes(
    builder: FlowGraphBuilder,
    parsed,
    seen: Set[str],
    errors: List[str],
) -> None:
    """Add a parsed flow and recursively parse/add its includes."""
    if parsed.flow_id in seen:
        return
    seen.add(parsed.flow_id)
    builder.add_parsed_flow(parsed)
    for include_name in parsed.includes:
        include_path = FLOW_DIR / include_name
        if not include_path.exists():
            errors.append(f"include file not found: {include_name}")
            continue
        try:
            included = parse_flow_file(include_path)
        except FlowParseError as exc:
            errors.append(f"include '{include_name}' parse error: {exc}")
            continue
        _add_with_includes(builder, included, seen, errors)


def resolve_include_flow_ids(content: str, flow_id: str = "preview") -> List[str]:
    """Parse YAML content and return the transitively included flow ids."""
    try:
        parsed = parse_flow_content(content, flow_id)
    except FlowParseError:
        return []
    seen: Set[str] = set()
    order: List[str] = []

    def visit(p) -> None:
        if p.flow_id in seen:
            return
        seen.add(p.flow_id)
        order.append(p.flow_id)
        for name in p.includes:
            include_path = FLOW_DIR / name
            if not include_path.exists():
                continue
            try:
                visit(parse_flow_file(include_path))
            except FlowParseError:
                continue

    visit(parsed)
    return [fid for fid in order if fid != flow_id]


async def preview_flow_graph(
    content: str,
    flow_id: str = "preview",
) -> Tuple[List[GraphNode], List[GraphEdge], List[str], List[str]]:
    """Parse YAML content and return the rendered graph without persisting.

    Returns:
        (nodes, edges, errors, warnings)
    """
    errors: List[str] = []
    warnings: List[str] = []

    try:
        parsed = parse_flow_content(content, flow_id)
    except FlowParseError as exc:
        errors.append(str(exc))
        return [], [], errors, warnings

    builder = FlowGraphBuilder()
    seen: Set[str] = set()
    _add_with_includes(builder, parsed, seen, errors)

    if errors:
        return [], [], errors, warnings

    builder.validate_global()
    warnings.extend(builder.graph.warnings)
    if builder.graph.errors:
        errors.extend(builder.graph.errors)
        return [], [], errors, warnings

    nodes, edges = await flow_graph_to_graph_elements(builder.graph)
    return nodes, edges, errors, warnings
