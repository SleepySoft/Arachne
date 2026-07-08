"""Association reasoning task: neighborhood expansion and path discovery."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from app.database import get_async_driver
from app.reasoning.schemas import (
    EvidenceChain,
    FeatureTable,
    OutputType,
    PathOutput,
    ReasoningConstraints,
    ReasoningDiagnostics,
    ReasoningPath,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    SubgraphOutput,
    TemporaryReasoningGraph,
    TempGraphEdge,
    TempGraphNode,
)
from app.reasoning.derived_from_utils import expand_by_derived_from
from app.reasoning.topology import expand_by_topology
from app.reasoning.tasks.utils import (
    allowed_confidence_values,
    build_allowed_rel_types,
    build_company_exposures,
    collect_unique_edges,
    collect_unique_node_ids,
    edge_to_dict,
    fetch_nodes_by_ids,
    node_to_dict,
    passes_edge_filters,
    passes_node_filters,
    validate_source_nodes,
)
from app.reasoning.diagnostics import build_diagnostics
from app.reasoning.evidence import build_evidence_chains


async def _fetch_paths(
    source_id: str,
    constraints: ReasoningConstraints,
) -> List[Dict[str, Any]]:
    """Fetch paths from Neo4j according to traversal direction."""
    driver = get_async_driver()
    rel_pattern = build_allowed_rel_types(constraints)
    max_depth = constraints.max_depth
    limit = constraints.max_paths
    allowed_confidences = allowed_confidence_values(
        constraints.min_edge_confidence,
        constraints.include_low_confidence_edges,
    )
    edge_types = constraints.allowed_edge_types

    # Build WHERE clause for edge attributes
    edge_filters = ["coalesce(rel.confidence, 'LOW') IN $allowed_confidences"]
    params: Dict[str, Any] = {
        "source_id": source_id,
        "max_depth": max_depth,
        "limit": limit,
        "allowed_confidences": allowed_confidences,
    }
    if edge_types:
        edge_filters.append("coalesce(rel.edge_type, 'unknown') IN $edge_types")
        params["edge_types"] = edge_types

    where_clause = " AND ".join(edge_filters)

    paths: List[Dict[str, Any]] = []

    def make_cypher(direction: str) -> str:
        if direction == "forward":
            rel_clause = f"-[r:{rel_pattern}*1..{max_depth}]->"
        else:
            rel_clause = f"<-[r:{rel_pattern}*1..{max_depth}]-"
        return f"""
        MATCH path = (src:IndustrialNode {{node_id: $source_id}}){rel_clause}(dst:IndustrialNode)
        WHERE all(rel IN r WHERE {where_clause})
        RETURN [n IN nodes(path) | n.node_id] AS node_ids,
               [rel IN relationships(path) | {{
                    edge_id: rel.edge_id,
                    edge_namespace: rel.edge_namespace,
                    edge_type: rel.edge_type,
                    from_node: startNode(rel).node_id,
                    to_node: endNode(rel).node_id,
                    confidence: rel.confidence,
                    description: rel.description,
                    evidence: rel.evidence
               }}] AS rels
        LIMIT $limit
        """

    directions = []
    if constraints.traversal_direction in ("forward", "both"):
        directions.append("forward")
    if constraints.traversal_direction in ("backward", "both"):
        directions.append("backward")

    for direction in directions:
        cypher = make_cypher(direction)
        async with driver.session() as session:
            result = await session.run(cypher, **params)
            async for record in result:
                paths.append({
                    "node_ids": record["node_ids"],
                    "rels": record["rels"],
                })
    return paths


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
        # Deduplicate by full node sequence
        key = ">".join(node_ids)
        if key in seen:
            continue
        seen.add(key)
        node_name_map = {
            nid: {
                "canonical_name_zh": getattr(nodes_map.get(nid), "canonical_name_zh", None),
                "canonical_name_en": getattr(nodes_map.get(nid), "canonical_name_en", None),
                "entity_type": getattr(nodes_map.get(nid), "entity_type", None),
            }
            for nid in node_ids
        }
        flags = []
        if any(r.get("edge_type") == "derived_from" for r in rels):
            flags.append("via_derived_from")
        out.append(
            ReasoningPath(
                path_id=f"path_{source_id}_{idx}",
                start_node_id=node_ids[0],
                end_node_id=node_ids[-1],
                node_sequence=node_ids,
                edge_sequence=[r["edge_id"] for r in rels],
                graph_sequence=["industrial"] * len(node_ids),
                path_length=len(rels),
                node_name_map=node_name_map,
                flags=flags,
            )
        )
    return out


async def run_association(
    task: ReasoningTask,
    reasoning_id: str,
) -> ReasoningResultEnvelope:
    started_at = datetime.utcnow()
    diagnostics = ReasoningDiagnostics()
    warnings: List[str] = []

    existing, missing = await validate_source_nodes(task.source_nodes)
    if missing:
        warnings.append(f"Missing source nodes: {missing}")
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

    expand_derived = task.parameters.get("expand_derived_from", True)
    seed_nodes = existing
    if expand_derived:
        try:
            expanded = await expand_by_derived_from(existing, direction="both", max_hops=5)
            seed_nodes = sorted(expanded)
            if len(seed_nodes) > len(existing):
                warnings.append(
                    f"Expanded {len(existing)} source(s) to {len(seed_nodes)} equivalent nodes via derived_from"
                )
        except Exception as exc:
            warnings.append(f"derived_from expansion failed: {exc}")

    expand_ontology = task.parameters.get("expand_ontology", False)
    if expand_ontology:
        try:
            expanded = await expand_by_topology(seed_nodes, direction="both", max_hops=2)
            before = len(seed_nodes)
            seed_nodes = sorted(expanded)
            if len(seed_nodes) > before:
                warnings.append(
                    f"Expanded {before} seed(s) to {len(seed_nodes)} nodes via ontology topology"
                )
        except Exception as exc:
            warnings.append(f"ontology expansion failed: {exc}")

    # Fetch raw paths for all sources
    all_paths: List[Dict[str, Any]] = []
    for source_id in seed_nodes:
        source_paths = await _fetch_paths(source_id, task.constraints)
        all_paths.extend(source_paths)
        if len(all_paths) >= task.constraints.max_paths:
            all_paths = all_paths[: task.constraints.max_paths]
            diagnostics.truncated = True
            diagnostics.truncation_reason = "max_paths reached"
            warnings.append("Path collection truncated due to max_paths")
            break

    node_ids = collect_unique_node_ids(all_paths)
    # Ensure all seed nodes (including derived_from/ontology expansions) are included
    node_ids.update(seed_nodes)

    if len(node_ids) > task.constraints.max_nodes:
        diagnostics.truncated = True
        diagnostics.truncation_reason = "max_nodes reached"
        warnings.append("Node collection truncated due to max_nodes")
        # Keep source nodes + first N reachable nodes
        reachable = list(node_ids - set(existing))[: task.constraints.max_nodes]
        node_ids = set(existing) | set(reachable)
        # Re-filter paths
        all_paths = [p for p in all_paths if all(nid in node_ids for nid in p["node_ids"])]

    nodes_map = await fetch_nodes_by_ids(list(node_ids))

    # Filter nodes, but always retain source nodes even if pending
    source_set = set(seed_nodes)
    filtered_nodes = {
        nid: n for nid, n in nodes_map.items()
        if nid in source_set or passes_node_filters(n, task.constraints)
    }
    filtered_node_ids = set(filtered_nodes.keys())
    all_paths = [p for p in all_paths if all(nid in filtered_node_ids for nid in p["node_ids"])]

    # Filter edges
    unique_edges = collect_unique_edges(all_paths)
    filtered_edge_records = {
        eid: e for eid, e in unique_edges.items()
        if not task.constraints.allowed_edge_types or e.get("edge_type") in task.constraints.allowed_edge_types
    }
    # Note: confidence already filtered in Cypher; namespace filtered by rel pattern.

    # Build result payload
    result_payload: Dict[str, Any] = {}

    if OutputType.SUBGRAPH in task.requested_outputs:
        result_payload["subgraph"] = SubgraphOutput(
            center_nodes=existing,
            depth=task.constraints.max_depth,
            nodes=[node_to_dict(n) for n in filtered_nodes.values()],
            edges=list(filtered_edge_records.values()),
            truncated=diagnostics.truncated,
            truncation_reason=diagnostics.truncation_reason,
        ).model_dump()

    reasoning_paths = _paths_to_reasoning_paths(all_paths, existing[0] if existing else "", nodes_map)
    if OutputType.PATHS in task.requested_outputs:
        result_payload["paths"] = PathOutput(
            paths=reasoning_paths,
            total_paths_found=len(reasoning_paths),
            returned_paths=len(reasoning_paths),
            truncated=diagnostics.truncated,
            truncation_reason=diagnostics.truncation_reason,
        ).model_dump()

    if OutputType.TEMPORARY_GRAPH in task.requested_outputs:
        temp_nodes = [
            TempGraphNode(
                temp_node_id=n.node_id,
                origin_graph="industrial",
                origin_node_id=n.node_id,
                node_type=n.entity_type or "unknown",
                label=n.canonical_name_zh or n.node_id,
                properties=node_to_dict(n),
            )
            for n in filtered_nodes.values()
        ]
        temp_edges = [
            TempGraphEdge(
                temp_edge_id=e["edge_id"],
                origin_graph="industrial",
                origin_edge_id=e["edge_id"],
                from_temp_node_id=e["from_node"],
                to_temp_node_id=e["to_node"],
                edge_namespace=e.get("edge_namespace", "industrial_flow"),
                edge_type=e.get("edge_type", "unknown"),
                properties=e,
            )
            for e in filtered_edge_records.values()
        ]
        result_payload["temporary_graph"] = TemporaryReasoningGraph(
            temp_graph_id=f"temp_{reasoning_id}",
            reasoning_id=reasoning_id,
            graph_scope="single_graph",
            source_graphs=["industrial"],
            nodes=temp_nodes,
            edges=temp_edges,
            created_at=datetime.utcnow(),
        ).model_dump()

    evidence_chains: List[EvidenceChain] = []
    if OutputType.EVIDENCE_CHAINS in task.requested_outputs:
        evidence_chains = build_evidence_chains(
            nodes=list(filtered_nodes.values()),
            edges=filtered_edge_records.values(),
            paths=reasoning_paths,
        )
        result_payload["evidence_chains"] = [ec.model_dump() for ec in evidence_chains]

    if OutputType.FEATURE_TABLES in task.requested_outputs:
        node_rows = [node_to_dict(n) for n in filtered_nodes.values()]
        edge_rows = list(filtered_edge_records.values())
        result_payload["feature_tables"] = [
            FeatureTable(
                table_id=f"ft_nodes_{reasoning_id}",
                entity_level="node",
                columns=list(node_rows[0].keys()) if node_rows else [],
                rows=node_rows,
            ).model_dump(),
            FeatureTable(
                table_id=f"ft_edges_{reasoning_id}",
                entity_level="edge",
                columns=list(edge_rows[0].keys()) if edge_rows else [],
                rows=edge_rows,
            ).model_dump(),
        ]

    if task.parameters.get("include_company_exposures"):
        max_exposures = task.parameters.get("max_company_exposures", 50)
        try:
            max_exposures = int(max_exposures)
        except Exception:
            max_exposures = 50
        company_exposures = await build_company_exposures(
            list(filtered_node_ids),
            max_exposures=max_exposures,
        )
        if company_exposures:
            result_payload["company_exposures"] = company_exposures.model_dump()

    diagnostics = build_diagnostics(
        nodes=list(filtered_nodes.values()),
        edges=list(filtered_edge_records.values()),
        diagnostics=diagnostics,
        warnings=warnings,
        started_at=started_at,
    )

    return ReasoningResultEnvelope(
        reasoning_id=reasoning_id,
        task_id=task.task_id,
        task_type=task.task_type.value,
        status=ResultStatus.SUCCESS if filtered_nodes else ResultStatus.NO_RESULT,
        generated_at=datetime.utcnow(),
        input_fingerprint="",
        output_types=[o.value for o in task.requested_outputs],
        result_payload=result_payload,
        diagnostics=diagnostics,
    )
