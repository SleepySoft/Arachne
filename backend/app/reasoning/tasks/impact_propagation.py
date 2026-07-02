"""Impact propagation reasoning task: deterministic what-if propagation."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from app.reasoning.rules import get_propagation_profile
from app.reasoning.scorers import CompositeScorer, DepthDecayScorer, EdgeWeightScorer
from app.reasoning.schemas import (
    EdgeScore,
    EvidenceChain,
    FeatureTable,
    NodeScore,
    OutputType,
    PathOutput,
    ReasoningConstraints,
    ReasoningDiagnostics,
    ReasoningPath,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    TemporaryReasoningGraph,
    TempGraphEdge,
    TempGraphNode,
)
from app.reasoning.tasks.association import _fetch_paths, _paths_to_reasoning_paths
from app.reasoning.tasks.utils import (
    collect_unique_edges,
    collect_unique_node_ids,
    edge_to_dict,
    fetch_nodes_by_ids,
    node_to_dict,
    passes_node_filters,
    validate_source_nodes,
)
from app.reasoning.diagnostics import build_diagnostics
from app.reasoning.evidence import build_evidence_chains


def _resolve_propagation_constraints(
    task: ReasoningTask,
) -> tuple[ReasoningConstraints, dict]:
    """Merge task constraints with propagation profile defaults."""
    profile_name = task.parameters.get("propagation_profile", "supply_forward")
    profile = get_propagation_profile(profile_name)

    constraints = task.constraints.model_copy(deep=True)
    # Profile may override allowed edge types/namespaces if not explicitly set
    if not task.constraints.allowed_edge_namespaces:
        constraints.allowed_edge_namespaces = profile.allowed_edge_namespaces
    if not task.constraints.allowed_edge_types:
        constraints.allowed_edge_types = profile.allowed_edge_types

    # Direction from profile takes precedence for propagation
    if profile.direction == "forward":
        constraints.traversal_direction = "forward"
    elif profile.direction == "backward":
        constraints.traversal_direction = "backward"
    else:
        constraints.traversal_direction = "both"

    scorer = CompositeScorer(
        [
            EdgeWeightScorer(profile.edge_weights),
            DepthDecayScorer(decay=profile.decay_factor),
        ],
        scorer_weights=[1.0, 1.0],
    )

    return constraints, {
        "profile": profile,
        "scorer": scorer,
        "initial_score": profile.initial_node_score,
    }


async def run_impact_propagation(
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

    constraints, propagation_ctx = _resolve_propagation_constraints(task)
    scorer = propagation_ctx["scorer"]
    initial_score = propagation_ctx["initial_score"]

    # Fetch raw paths
    all_paths: List[Dict[str, Any]] = []
    for source_id in existing:
        source_paths = await _fetch_paths(source_id, constraints)
        all_paths.extend(source_paths)
        if len(all_paths) >= constraints.max_paths:
            all_paths = all_paths[: constraints.max_paths]
            diagnostics.truncated = True
            diagnostics.truncation_reason = "max_paths reached"
            warnings.append("Path collection truncated due to max_paths")
            break

    node_ids = collect_unique_node_ids(all_paths)
    node_ids.update(existing)

    if len(node_ids) > constraints.max_nodes:
        diagnostics.truncated = True
        diagnostics.truncation_reason = "max_nodes reached"
        warnings.append("Node collection truncated due to max_nodes")
        reachable = list(node_ids - set(existing))[: constraints.max_nodes]
        node_ids = set(existing) | set(reachable)
        all_paths = [p for p in all_paths if all(nid in node_ids for nid in p["node_ids"])]

    nodes_map = await fetch_nodes_by_ids(list(node_ids))
    source_set = set(existing)
    filtered_nodes = {
        nid: n for nid, n in nodes_map.items()
        if nid in source_set or passes_node_filters(n, constraints)
    }
    filtered_node_ids = set(filtered_nodes.keys())
    all_paths = [p for p in all_paths if all(nid in filtered_node_ids for nid in p["node_ids"])]

    unique_edges = collect_unique_edges(all_paths)
    # Keep edges matching profile/types; confidence already filtered by Cypher
    filtered_edge_records = {
        eid: e for eid, e in unique_edges.items()
        if not constraints.allowed_edge_types or e.get("edge_type") in constraints.allowed_edge_types
    }

    # Score nodes and paths
    node_scores: Dict[str, float] = {nid: initial_score for nid in existing}
    edge_scores: Dict[str, float] = {}
    reasoning_paths: List[ReasoningPath] = []

    for idx, p in enumerate(all_paths):
        node_ids_seq = p["node_ids"]
        rels = p["rels"]
        if len(node_ids_seq) < 2:
            continue

        # Build lightweight edge objects for scorer
        scored_edges: List[Any] = []
        for r in rels:
            edge = type("_ScoredEdge", (), {})()
            edge.edge_id = r["edge_id"]
            edge.from_node = r["from_node"]
            edge.to_node = r["to_node"]
            edge.edge_namespace = r.get("edge_namespace", "industrial_flow")
            edge.edge_type = r.get("edge_type", "unknown")
            edge.confidence = r.get("confidence", "LOW")
            scored_edges.append(edge)

        score = scorer.score(node_ids_seq, scored_edges) * initial_score
        score_components = scorer.score_components(node_ids_seq, scored_edges)

        path_id = f"path_{reasoning_id}_{idx}"
        reasoning_paths.append(
            ReasoningPath(
                path_id=path_id,
                start_node_id=node_ids_seq[0],
                end_node_id=node_ids_seq[-1],
                node_sequence=node_ids_seq,
                edge_sequence=[r["edge_id"] for r in rels],
                graph_sequence=["industrial"] * len(node_ids_seq),
                path_length=len(rels),
                path_score=score,
                score_components=score_components,
            )
        )

        # Update node scores (max over paths)
        for nid in node_ids_seq:
            node_scores[nid] = max(node_scores.get(nid, 0.0), score)

        # Update edge scores (max over paths containing edge)
        for i, r in enumerate(rels):
            eid = r["edge_id"]
            edge_scores[eid] = max(edge_scores.get(eid, 0.0), score)

    result_payload: Dict[str, Any] = {}

    if OutputType.TEMPORARY_GRAPH in task.requested_outputs:
        temp_nodes = [
            TempGraphNode(
                temp_node_id=n.node_id,
                origin_graph="industrial",
                origin_node_id=n.node_id,
                node_type=n.entity_type or "unknown",
                label=n.canonical_name_zh or n.node_id,
                properties=node_to_dict(n),
                score=node_scores.get(n.node_id),
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
                weight=edge_scores.get(e["edge_id"]),
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

    if OutputType.PATHS in task.requested_outputs:
        result_payload["paths"] = PathOutput(
            paths=reasoning_paths,
            total_paths_found=len(reasoning_paths),
            returned_paths=len(reasoning_paths),
            truncated=diagnostics.truncated,
            truncation_reason=diagnostics.truncation_reason,
        ).model_dump()

    if OutputType.NODE_SCORES in task.requested_outputs:
        sorted_nodes = sorted(
            [(nid, s) for nid, s in node_scores.items() if nid in filtered_node_ids],
            key=lambda x: x[1],
            reverse=True,
        )
        result_payload["node_scores"] = [
            NodeScore(
                node_id=nid,
                graph="industrial",
                score=round(score, 6),
                rank=idx + 1,
                score_type="impact_propagation",
                score_components={"initial_score": initial_score},
            ).model_dump()
            for idx, (nid, score) in enumerate(sorted_nodes)
        ]

    if OutputType.EDGE_SCORES in task.requested_outputs:
        sorted_edges = sorted(
            [(eid, s) for eid, s in edge_scores.items() if eid in filtered_edge_records],
            key=lambda x: x[1],
            reverse=True,
        )
        result_payload["edge_scores"] = [
            EdgeScore(
                edge_id=eid,
                graph="industrial",
                score=round(score, 6),
                rank=idx + 1,
                score_type="impact_propagation",
                score_components={},
            ).model_dump()
            for idx, (eid, score) in enumerate(sorted_edges)
        ]

    evidence_chains: List[EvidenceChain] = []
    if OutputType.EVIDENCE_CHAINS in task.requested_outputs:
        evidence_chains = build_evidence_chains(
            nodes=list(filtered_nodes.values()),
            edges=filtered_edge_records.values(),
            paths=reasoning_paths,
        )
        result_payload["evidence_chains"] = [ec.model_dump() for ec in evidence_chains]

    if OutputType.FEATURE_TABLES in task.requested_outputs:
        node_rows = [
            {**node_to_dict(n), "impact_score": node_scores.get(n.node_id)}
            for n in filtered_nodes.values()
        ]
        edge_rows = [
            {**e, "impact_score": edge_scores.get(e["edge_id"])}
            for e in filtered_edge_records.values()
        ]
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
