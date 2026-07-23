"""Arachne-flow association reasoning task: neighborhood expansion and path discovery."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Set

from app.reasoning.arachne_flow_adapter import (
    expand_by_method_ref,
    fetch_arachne_flow_nodes,
    fetch_arachne_flow_paths,
    map_arachne_flow_node_to_reasoning,
    validate_arachne_flow_sources,
)
from app.reasoning.diagnostics import build_diagnostics
from app.reasoning.schemas import (
    OriginGraph,
    OutputType,
    ReasoningDiagnostics,
    ReasoningPath,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    SubgraphOutput,
    TempGraphEdge,
    TempGraphNode,
    TemporaryReasoningGraph,
)


def _paths_to_reasoning_paths(
    paths: List[Dict[str, Any]],
    source_id: str,
    nodes_map: Dict[str, Any],
) -> List[ReasoningPath]:
    """Convert raw path records to ReasoningPath objects."""
    out: List[ReasoningPath] = []
    seen: Set[str] = set()
    for idx, p in enumerate(paths):
        node_ids = p["node_ids"]
        rels = p["rels"]
        if len(node_ids) < 2:
            continue
        key = ">".join(node_ids)
        if key in seen:
            continue
        seen.add(key)
        node_name_map = {
            nid: {
                "canonical_name_zh": nodes_map.get(nid, {}).get("canonical_name_zh"),
                "canonical_name_en": nodes_map.get(nid, {}).get("canonical_name_en"),
                "entity_type": nodes_map.get(nid, {}).get("entity_type"),
            }
            for nid in node_ids
        }
        flags = []
        if any(r.get("edge_type") == "ref" for r in rels):
            flags.append("via_method_ref")
        out.append(
            ReasoningPath(
                path_id=f"path_{source_id}_{idx}",
                start_node_id=node_ids[0],
                end_node_id=node_ids[-1],
                node_sequence=node_ids,
                edge_sequence=[r["edge_id"] for r in rels],
                graph_sequence=["arachne_flow"] * len(node_ids),
                path_length=len(rels),
                node_name_map=node_name_map,
                flags=flags,
            )
        )
    return out


async def run_arachne_flow_association(
    task: ReasoningTask,
    reasoning_id: str,
) -> ReasoningResultEnvelope:
    """Run association reasoning on the arachne-flow graph."""
    started_at = datetime.utcnow()
    diagnostics = ReasoningDiagnostics()
    warnings: List[str] = []

    # 1. Validate source nodes in the arachne-flow graph.
    existing, missing = await validate_arachne_flow_sources(task.source_nodes)
    if missing:
        warnings.append(f"Missing source nodes in arachne_flow graph: {missing}")
        diagnostics.dangling_reference_count += len(missing)
    if not existing:
        diagnostics.warnings = warnings
        diagnostics.execution_time_ms = int((datetime.utcnow() - started_at).total_seconds() * 1000)
        return ReasoningResultEnvelope(
            reasoning_id=reasoning_id,
            task_id=task.task_id,
            task_type=task.task_type.value,
            status=ResultStatus.NO_RESULT,
            generated_at=datetime.utcnow(),
            input_fingerprint="",
            output_types=[o.value for o in task.requested_outputs],
            result_payload={},
            diagnostics=diagnostics,
        )

    # 2. Optionally expand via method_ref (actions <-> methods).
    expand_method_ref = task.parameters.get("expand_method_ref", True)
    seed_nodes = list(existing)
    if expand_method_ref:
        try:
            expanded = await expand_by_method_ref(seed_nodes, direction="both")
            before = len(seed_nodes)
            seed_nodes = sorted(expanded)
            if len(seed_nodes) > before:
                warnings.append(
                    f"Expanded {before} source(s) to {len(seed_nodes)} nodes via method_ref"
                )
        except Exception as exc:
            warnings.append(f"method_ref expansion failed: {exc}")

    # 3. Fetch raw paths for all sources.
    max_depth = task.constraints.max_depth
    max_paths = task.constraints.max_paths
    direction = task.constraints.traversal_direction.value

    all_paths: List[Dict[str, Any]] = []
    for source_id in seed_nodes:
        source_paths = await fetch_arachne_flow_paths(
            source_id, max_depth=max_depth, direction=direction, limit=max_paths
        )
        all_paths.extend(source_paths)
        if len(all_paths) >= max_paths:
            all_paths = all_paths[:max_paths]
            diagnostics.truncated = True
            diagnostics.truncation_reason = "max_paths reached"
            warnings.append("Path collection truncated due to max_paths")
            break

    # 4. Collect node ids from paths and fetch node metadata.
    node_ids: Set[str] = set(seed_nodes)
    for p in all_paths:
        node_ids.update(p["node_ids"])

    if len(node_ids) > task.constraints.max_nodes:
        diagnostics.truncated = True
        diagnostics.truncation_reason = "max_nodes reached"
        warnings.append("Node collection truncated due to max_nodes")
        reachable = list(node_ids - set(existing))[: task.constraints.max_nodes]
        node_ids = set(existing) | set(reachable)
        all_paths = [p for p in all_paths if all(nid in node_ids for nid in p["node_ids"])]

    nodes_map_raw = await fetch_arachne_flow_nodes(list(node_ids))
    nodes_map = {nid: map_arachne_flow_node_to_reasoning(n) for nid, n in nodes_map_raw.items()}

    # 5. Convert paths to ReasoningPath objects.
    reasoning_paths: List[ReasoningPath] = []
    for source_id in seed_nodes:
        source_paths = [p for p in all_paths if p["node_ids"] and p["node_ids"][0] == source_id]
        reasoning_paths.extend(_paths_to_reasoning_paths(source_paths, source_id, nodes_map))

    # 6. Build temporary reasoning graph.
    temp_nodes: List[TempGraphNode] = []
    temp_edges: List[TempGraphEdge] = []
    node_id_set = set()
    edge_id_set = set()

    for nid in sorted(node_ids):
        if nid in node_id_set:
            continue
        node_id_set.add(nid)
        node_info = nodes_map.get(nid, {})
        temp_nodes.append(
            TempGraphNode(
                temp_node_id=nid,
                origin_graph=OriginGraph.INDUSTRIAL,
                origin_node_id=nid,
                node_type=node_info.get("entity_type", "unknown"),
                label=node_info.get("label", nid),
                properties=node_info,
            )
        )

    for p in all_paths:
        for rel in p["rels"]:
            eid = rel["edge_id"]
            if eid in edge_id_set:
                continue
            edge_id_set.add(eid)
            temp_edges.append(
                TempGraphEdge(
                    temp_edge_id=eid,
                    origin_graph=OriginGraph.INDUSTRIAL,
                    origin_edge_id=eid,
                    from_temp_node_id=rel["from_node"],
                    to_temp_node_id=rel["to_node"],
                    edge_namespace=rel["edge_namespace"],
                    edge_type=rel["edge_type"],
                    properties=rel,
                )
            )

    from app.reasoning.schemas import GraphType, TempGraphScope

    temp_graph = TemporaryReasoningGraph(
        temp_graph_id=f"temp_graph_{reasoning_id}",
        reasoning_id=reasoning_id,
        graph_scope=TempGraphScope.SINGLE_GRAPH,
        source_graphs=[GraphType.INDUSTRIAL],
        nodes=temp_nodes,
        edges=temp_edges,
        created_at=datetime.utcnow(),
    )

    # 7. Build result payload.
    result_payload: Dict[str, Any] = {
        "seed_nodes": seed_nodes,
        "paths": [p.model_dump() for p in reasoning_paths],
    }
    if OutputType.TEMPORARY_GRAPH in task.requested_outputs or not task.requested_outputs:
        result_payload["temporary_graph"] = temp_graph.model_dump()

    diagnostics.warnings = warnings
    diagnostics.execution_time_ms = int((datetime.utcnow() - started_at).total_seconds() * 1000)

    return ReasoningResultEnvelope(
        reasoning_id=reasoning_id,
        task_id=task.task_id,
        task_type=task.task_type.value,
        status=ResultStatus.SUCCESS,
        generated_at=datetime.utcnow(),
        input_fingerprint="",
        output_types=[o.value for o in task.requested_outputs],
        result_payload=result_payload,
        diagnostics=diagnostics,
    )
