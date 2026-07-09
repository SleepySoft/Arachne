"""Candidate discovery reasoning task.

Suggests missing industrial nodes (primarily process nodes) and missing edges
by detecting common anti-patterns in the graph.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Set
from uuid import uuid4

from app.database import get_async_driver
from app.reasoning.derived_from_utils import expand_by_derived_from
from app.reasoning.schemas import (
    CandidateEdgeOutput,
    CandidateNodeOutput,
    EvidenceChain,
    FeatureTable,
    GraphType,
    OutputType,
    ReasoningDiagnostics,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    TemporaryReasoningGraph,
    TempGraphNode,
)
from app.reasoning.tasks.utils import (
    fetch_nodes_by_ids,
    node_to_dict,
    validate_source_nodes,
)
from app.reasoning.diagnostics import build_diagnostics
from app.reasoning.evidence import build_evidence_chains


_ENTITY_TYPES_NEEDING_PROCESS = {
    "device",
    "equipment",
    "system",
    "part",
}

_ENTITY_TYPES_CAN_BE_INPUT = {
    "material",
    "part",
    "device",
}


async def _find_missing_process_nodes(
    source_ids: List[str],
    constraints: Any,
) -> List[Dict[str, Any]]:
    """Find material_input edges that appear to skip an intermediate process node."""
    driver = get_async_driver()
    max_paths = constraints.max_paths

    where_source = ""
    params: Dict[str, Any] = {"max_paths": max_paths}
    if source_ids:
        where_source = "WHERE src.node_id IN $source_ids OR dst.node_id IN $source_ids"
        params["source_ids"] = source_ids

    cypher = f"""
    MATCH (src:IndustrialNode)-[r:INDUSTRIAL_FLOW {{edge_type: 'material_input'}}]->(dst:IndustrialNode)
    {where_source}
    WITH src, dst, r
    OPTIONAL MATCH (src)-[:INDUSTRIAL_FLOW {{edge_type: 'material_input'}}]->
                   (p:IndustrialNode {{entity_type: 'process'}})-
                   [:INDUSTRIAL_FLOW {{edge_type: 'process_output'}}]->(dst)
    WITH src, dst, r, p
    WHERE p IS NULL
    RETURN src.node_id AS from_id,
           src.canonical_name_zh AS from_name,
           dst.node_id AS to_id,
           dst.canonical_name_zh AS to_name
    LIMIT $max_paths
    """

    candidates: List[Dict[str, Any]] = []
    async with driver.session() as session:
        result = await session.run(cypher, **params)
        async for record in result:
            candidates.append({
                "from_id": record["from_id"],
                "from_name": record["from_name"] or record["from_id"],
                "to_id": record["to_id"],
                "to_name": record["to_name"] or record["to_id"],
            })
    return candidates


async def _find_under_specified_nodes(
    source_ids: List[str],
    min_degree: int = 3,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Find nodes with high degree but missing definition or unknown entity type."""
    driver = get_async_driver()
    where_source = ""
    params: Dict[str, Any] = {"min_degree": min_degree, "limit": limit}
    if source_ids:
        where_source = "WHERE n.node_id IN $source_ids"
        params["source_ids"] = source_ids

    cypher = f"""
    MATCH (n:IndustrialNode)
    {where_source}
    WITH n, size([(n)-[:INDUSTRIAL_FLOW|ONTOLOGY]-() | 1]) AS degree
    WHERE degree >= $min_degree
    RETURN n.node_id AS node_id, degree
    ORDER BY degree DESC
    LIMIT $limit
    """

    node_ids_with_degree: List[Dict[str, Any]] = []
    async with driver.session() as session:
        result = await session.run(cypher, **params)
        async for record in result:
            node_ids_with_degree.append({
                "node_id": record["node_id"],
                "degree": record["degree"],
            })

    node_ids = [item["node_id"] for item in node_ids_with_degree]
    node_map = await fetch_nodes_by_ids(node_ids)

    nodes: List[Dict[str, Any]] = []
    for item in node_ids_with_degree:
        node = node_map.get(item["node_id"])
        if node is None:
            continue
        entity_type = node.entity_type.value if hasattr(node.entity_type, "value") else node.entity_type
        definition = node.definition or ""
        if entity_type != "unknown" and definition:
            continue
        nodes.append({
            "node_id": node.node_id,
            "name": node.canonical_name_zh or node.node_id,
            "entity_type": entity_type,
            "degree": item["degree"],
        })
    return nodes


async def _find_missing_derived_from_hints(
    source_ids: List[str],
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Heuristic: pairs of materials/parts that share many downstream outputs."""
    driver = get_async_driver()
    where_source = ""
    params: Dict[str, Any] = {"limit": limit}
    if source_ids:
        where_source = "WHERE a.node_id IN $source_ids OR b.node_id IN $source_ids"
        params["source_ids"] = source_ids

    cypher = f"""
    MATCH (a:IndustrialNode)-[:INDUSTRIAL_FLOW]->(x:IndustrialNode)<-[:INDUSTRIAL_FLOW]-(b:IndustrialNode)
    {where_source}
    WITH a, b, x
    WHERE a.node_id < b.node_id
      AND a.entity_type IN ['material', 'part']
      AND b.entity_type IN ['material', 'part']
      AND NOT EXISTS {{
        MATCH (a)-[:INDUSTRIAL_FLOW {{edge_type: 'derived_from'}}]-(b)
      }}
    WITH a, b, count(DISTINCT x) AS shared_outputs
    WHERE shared_outputs >= 2
    RETURN a.node_id AS from_id, a.canonical_name_zh AS from_name,
           b.node_id AS to_id, b.canonical_name_zh AS to_name,
           shared_outputs
    ORDER BY shared_outputs DESC
    LIMIT $limit
    """

    hints: List[Dict[str, Any]] = []
    async with driver.session() as session:
        result = await session.run(cypher, **params)
        async for record in result:
            hints.append({
                "from_id": record["from_id"],
                "from_name": record["from_name"] or record["from_id"],
                "to_id": record["to_id"],
                "to_name": record["to_name"] or record["to_id"],
                "shared_outputs": record["shared_outputs"],
            })
    return hints


def _make_process_candidate_id(from_id: str, to_id: str) -> str:
    return f"process_{from_id}_to_{to_id}"


async def run_candidate_discovery(
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

    expand_derived = task.parameters.get("expand_derived_from", True)
    seed_nodes = existing
    if existing and expand_derived:
        try:
            expanded = await expand_by_derived_from(existing, direction="both", max_hops=5)
            seed_nodes = sorted(expanded)
            if len(seed_nodes) > len(existing):
                warnings.append(
                    f"Expanded {len(existing)} source(s) to {len(seed_nodes)} equivalent nodes via derived_from"
                )
        except Exception as exc:
            warnings.append(f"derived_from expansion failed: {exc}")

    min_degree = task.parameters.get("min_degree", 3)
    missing_process = await _find_missing_process_nodes(seed_nodes, task.constraints)
    under_specified = await _find_under_specified_nodes(seed_nodes, min_degree=min_degree, limit=task.constraints.max_nodes)
    derived_hints = await _find_missing_derived_from_hints(seed_nodes, limit=task.constraints.max_paths)

    result_payload: Dict[str, Any] = {}

    candidate_nodes: List[CandidateNodeOutput] = []
    candidate_edges: List[CandidateEdgeOutput] = []
    all_node_ids: Set[str] = set()

    for idx, mp in enumerate(missing_process):
        candidate_id = _make_process_candidate_id(mp["from_id"], mp["to_id"])
        candidate_nodes.append(
            CandidateNodeOutput(
                candidate_id=candidate_id,
                proposed_graph=GraphType.INDUSTRIAL,
                proposed_node_id=candidate_id,
                canonical_name=f"{mp['from_name']} → {mp['to_name']} 工艺",
                aliases=[],
                proposed_entity_type="process",
                source_claims=task.source_claims,
                nearest_existing_objects=[mp["from_id"], mp["to_id"]],
                validation_status="needs_review",
                rule_violations=[],
                flags=["missing_process_node", "material_input_gap"],
            )
        )
        all_node_ids.update([mp["from_id"], mp["to_id"]])

    for idx, us in enumerate(under_specified):
        candidate_nodes.append(
            CandidateNodeOutput(
                candidate_id=f"underspecified_{reasoning_id}_{idx}",
                proposed_graph=GraphType.INDUSTRIAL,
                proposed_node_id=us["node_id"],
                canonical_name=us["name"],
                aliases=[],
                proposed_entity_type=us["entity_type"],
                source_claims=task.source_claims,
                nearest_existing_objects=[],
                validation_status="needs_review",
                rule_violations=[{"rule": "high_degree_missing_metadata", "degree": us["degree"]}],
                flags=["underspecified_node"],
            )
        )
        all_node_ids.add(us["node_id"])

    for idx, dh in enumerate(derived_hints):
        candidate_edges.append(
            CandidateEdgeOutput(
                candidate_id=f"missing_derived_{reasoning_id}_{idx}",
                proposed_graph=GraphType.INDUSTRIAL,
                from_object_id=dh["from_id"],
                to_object_id=dh["to_id"],
                proposed_edge_namespace="industrial_flow",
                proposed_edge_type="derived_from",
                source_claims=task.source_claims,
                validation_status="needs_review",
                rule_violations=[{"rule": "heuristic_shared_outputs", "shared_outputs": dh["shared_outputs"]}],
                flags=["missing_derived_from_hint"],
            )
        )
        all_node_ids.update([dh["from_id"], dh["to_id"]])

    nodes_map = await fetch_nodes_by_ids(list(all_node_ids))
    nodes = list(nodes_map.values())

    if OutputType.CANDIDATE_NODES in task.requested_outputs:
        result_payload["candidate_nodes"] = [c.model_dump() for c in candidate_nodes]

    if OutputType.CANDIDATE_EDGES in task.requested_outputs:
        result_payload["candidate_edges"] = [c.model_dump() for c in candidate_edges]

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
            for n in nodes
        ]
        # Add candidate process nodes as REASONING origin
        for c in candidate_nodes:
            if c.proposed_entity_type == "process":
                temp_nodes.append(
                    TempGraphNode(
                        temp_node_id=c.candidate_id,
                        origin_graph="reasoning",
                        origin_node_id=None,
                        node_type="process",
                        label=c.canonical_name,
                        properties={
                            "candidate_id": c.candidate_id,
                            "nearest_existing_objects": c.nearest_existing_objects,
                            "validation_status": c.validation_status,
                        },
                    )
                )
        result_payload["temporary_graph"] = TemporaryReasoningGraph(
            temp_graph_id=f"temp_{reasoning_id}",
            reasoning_id=reasoning_id,
            graph_scope="single_graph",
            source_graphs=["industrial", "reasoning"],
            nodes=temp_nodes,
            edges=[],
            created_at=datetime.utcnow(),
        ).model_dump()

    if OutputType.EVIDENCE_CHAINS in task.requested_outputs:
        result_payload["evidence_chains"] = [
            ec.model_dump()
            for ec in build_evidence_chains(nodes=nodes)
        ]

    if OutputType.FEATURE_TABLES in task.requested_outputs:
        rows = [c.model_dump() for c in candidate_nodes] + [c.model_dump() for c in candidate_edges]
        if rows:
            result_payload["feature_tables"] = [
                FeatureTable(
                    table_id=f"ft_candidates_{reasoning_id}",
                    entity_level="candidate",
                    columns=list(rows[0].keys()),
                    rows=rows,
                ).model_dump()
            ]

    if task.parameters.get("include_company_exposures") and nodes:
        max_exp = int(task.parameters.get("max_company_exposures", 50))
        company_exposures = await build_company_exposures(
            [n.node_id for n in nodes], max_exposures=max_exp
        )
        if company_exposures:
            result_payload["company_exposures"] = company_exposures.model_dump()

    diagnostics = build_diagnostics(
        nodes=nodes,
        edges=[],
        diagnostics=diagnostics,
        warnings=warnings,
        started_at=started_at,
    )

    status = ResultStatus.SUCCESS if (candidate_nodes or candidate_edges) else ResultStatus.NO_RESULT
    return ReasoningResultEnvelope(
        reasoning_id=reasoning_id,
        task_id=task.task_id,
        task_type=task.task_type.value,
        status=status,
        generated_at=datetime.utcnow(),
        input_fingerprint="",
        output_types=[o.value for o in task.requested_outputs],
        result_payload=result_payload,
        diagnostics=diagnostics,
    )
