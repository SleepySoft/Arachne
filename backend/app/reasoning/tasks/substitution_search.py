"""Substitution search reasoning task.

Finds alternative industrial nodes that could replace a source node, based on
material lineage (derived_from), ontology similarity, and shared upstream/downstream
neighbors.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from app.database import get_async_driver
from app.reasoning.derived_from_utils import expand_by_derived_from, get_derived_from_lineage
from app.reasoning.schemas import (
    CandidateNodeOutput,
    EvidenceChain,
    FeatureTable,
    GraphType,
    OutputType,
    ReasoningDiagnostics,
    ReasoningPath,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
    TemporaryReasoningGraph,
    TempGraphEdge,
    TempGraphNode,
)
from app.reasoning.tasks.utils import (
    build_company_exposures,
    fetch_nodes_by_ids,
    node_to_dict,
    validate_source_nodes,
)
from app.reasoning.diagnostics import build_diagnostics
from app.reasoning.evidence import build_evidence_chains


async def _get_direct_neighbors(
    node_ids: List[str],
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Return (upstream, downstream, ontology) neighbor sets for each node."""
    driver = get_async_driver()
    upstream: Dict[str, Set[str]] = defaultdict(set)
    downstream: Dict[str, Set[str]] = defaultdict(set)
    ontology: Dict[str, Set[str]] = defaultdict(set)

    async with driver.session() as session:
        result = await session.run(
            """
            MATCH (n:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]-(m:IndustrialNode)
            WHERE n.node_id IN $node_ids
            RETURN n.node_id AS nid, m.node_id AS mid,
                   CASE WHEN startNode(r).node_id = n.node_id THEN 'out' ELSE 'in' END AS dir,
                   r.edge_namespace AS ns, r.edge_type AS et
            """,
            node_ids=node_ids,
        )
        async for record in result:
            nid = record["nid"]
            mid = record["mid"]
            if mid == nid:
                continue
            ns = record["ns"]
            et = record["et"]
            if ns == "ontology" or et in ("is_a", "part_of", "variant_of", "alias_of"):
                ontology[nid].add(mid)
            else:
                if record["dir"] == "out":
                    downstream[nid].add(mid)
                else:
                    upstream[nid].add(mid)
    return upstream, downstream, ontology


async def _collect_substitution_candidates(
    target_id: str,
    max_depth: int = 5,
) -> Set[str]:
    """Gather candidate node IDs that might substitute for target_id."""
    candidates: Set[str] = set()

    # 1. Derived-from lineage and siblings
    lineage = await get_derived_from_lineage(target_id, max_hops=max_depth)
    candidates.update(lineage["ancestors"])
    candidates.update(lineage["descendants"])

    # Siblings: descendants of ancestors, excluding target's own lineage
    for anc in lineage["ancestors"]:
        anc_lineage = await get_derived_from_lineage(anc, max_hops=max_depth)
        candidates.update(anc_lineage["descendants"])

    # 2. Ontology neighbors and their ontology neighbors
    _, _, ontology = await _get_direct_neighbors([target_id])
    direct_onto = ontology.get(target_id, set())
    candidates.update(direct_onto)
    if direct_onto:
        _, _, onto2 = await _get_direct_neighbors(list(direct_onto))
        for s in onto2.values():
            candidates.update(s)

    # 3. Structural substitutes: nodes sharing upstream or downstream with target
    up, down, _ = await _get_direct_neighbors([target_id])
    shared_sources: Set[str] = set()
    for nid in up.get(target_id, set()):
        # upstream suppliers of target -> their other customers are substitutes
        _, down2, _ = await _get_direct_neighbors([nid])
        shared_sources |= down2.get(nid, set())
    for nid in down.get(target_id, set()):
        # downstream customers of target -> their other suppliers are substitutes
        up2, _, _ = await _get_direct_neighbors([nid])
        shared_sources |= up2.get(nid, set())
    candidates.update(shared_sources)

    candidates.discard(target_id)
    # Remove direct lineage members already added above
    candidates.discard(target_id)
    return candidates


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def _score_candidates(
    target_id: str,
    candidate_ids: Set[str],
    nodes_map: Dict[str, Any],
    target_up: Set[str],
    target_down: Set[str],
    target_onto: Set[str],
    all_up: Dict[str, Set[str]],
    all_down: Dict[str, Set[str]],
    all_onto: Dict[str, Set[str]],
    lineage: Dict[str, List[str]],
) -> List[Tuple[str, float, Dict[str, Any]]]:
    """Score substitution candidates and return sorted list."""
    scored: List[Tuple[str, float, Dict[str, Any]]] = []
    target_lineage = set(lineage["ancestors"]) | set(lineage["descendants"])

    for cid in candidate_ids:
        node = nodes_map.get(cid)
        if node is None:
            continue

        up = all_up.get(cid, set())
        down = all_down.get(cid, set())
        onto = all_onto.get(cid, set())

        structural_sim = (_jaccard(target_up, up) + _jaccard(target_down, down)) / 2
        ontology_sim = _jaccard(target_onto, onto)

        # Derived-from distance
        if cid in target_lineage:
            lineage_proximity = 1.0
        elif target_onto & onto:
            lineage_proximity = 0.7
        else:
            lineage_proximity = 0.0

        # Same entity type bonus
        target_node = nodes_map.get(target_id)
        same_type = 1.0 if target_node and getattr(target_node, "entity_type", None) == getattr(node, "entity_type", None) else 0.0

        score = 0.5 * structural_sim + 0.25 * ontology_sim + 0.15 * lineage_proximity + 0.1 * same_type

        components = {
            "structural_similarity": round(structural_sim, 4),
            "ontology_similarity": round(ontology_sim, 4),
            "lineage_proximity": round(lineage_proximity, 4),
            "same_entity_type": bool(same_type),
            "shared_upstream": sorted(target_up & up),
            "shared_downstream": sorted(target_down & down),
        }
        scored.append((cid, score, components))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


async def run_substitution_search(
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

    target_id = existing[0]
    expand_derived = task.parameters.get("expand_derived_from", True)
    if expand_derived:
        try:
            expanded = await expand_by_derived_from([target_id], direction="both", max_hops=5)
            if len(expanded) > 1:
                target_id = sorted(expanded)[0]
                warnings.append(f"Expanded target via derived_from; using representative {target_id}")
        except Exception as exc:
            warnings.append(f"derived_from expansion failed: {exc}")

    candidate_ids = await _collect_substitution_candidates(target_id)
    if not candidate_ids:
        diagnostics.warnings = warnings + ["No substitution candidates found"]
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

    all_node_ids = [target_id] + list(candidate_ids)
    nodes_map = await fetch_nodes_by_ids(all_node_ids)

    target_up, target_down, target_onto = await _get_direct_neighbors([target_id])
    all_up, all_down, all_onto = await _get_direct_neighbors(list(candidate_ids))
    lineage = await get_derived_from_lineage(target_id)

    scored = _score_candidates(
        target_id,
        candidate_ids,
        nodes_map,
        target_up.get(target_id, set()),
        target_down.get(target_id, set()),
        target_onto.get(target_id, set()),
        all_up,
        all_down,
        all_onto,
        lineage,
    )

    result_payload: Dict[str, Any] = {}

    if OutputType.CANDIDATE_NODES in task.requested_outputs:
        result_payload["candidate_nodes"] = [
            CandidateNodeOutput(
                candidate_id=f"substitution_{reasoning_id}_{idx}",
                proposed_graph=GraphType.INDUSTRIAL,
                proposed_node_id=cid,
                canonical_name=getattr(nodes_map.get(cid), "canonical_name_zh", None) or cid,
                aliases=getattr(nodes_map.get(cid), "aliases", []) or [],
                proposed_entity_type=getattr(nodes_map.get(cid), "entity_type", None),
                source_claims=task.source_claims,
                nearest_existing_objects=[target_id] + sorted((target_up.get(target_id, set()) | target_down.get(target_id, set())) & (all_up.get(cid, set()) | all_down.get(cid, set())))[:5],
                validation_status="valid" if score >= 0.3 else "needs_review",
                flags=["substitution_candidate"],
            ).model_dump()
            for idx, (cid, score, _) in enumerate(scored)
        ]

    # Build paths: target -> common neighbor -> candidate
    reasoning_paths: List[ReasoningPath] = []
    for idx, (cid, _, components) in enumerate(scored):
        shared_up = set(components.get("shared_upstream", []))
        shared_down = set(components.get("shared_downstream", []))
        bridge = next(iter(shared_up | shared_down), None)
        if bridge:
            seq = [target_id, bridge, cid]
        else:
            seq = [target_id, cid]
        reasoning_paths.append(
            ReasoningPath(
                path_id=f"path_{reasoning_id}_{idx}",
                start_node_id=target_id,
                end_node_id=cid,
                node_sequence=seq,
                edge_sequence=[],
                graph_sequence=["industrial"] * len(seq),
                path_length=len(seq) - 1,
                node_name_map={
                    nid: {
                        "canonical_name_zh": getattr(nodes_map.get(nid), "canonical_name_zh", None),
                        "canonical_name_en": getattr(nodes_map.get(nid), "canonical_name_en", None),
                        "entity_type": getattr(nodes_map.get(nid), "entity_type", None),
                    }
                    for nid in seq
                },
            )
        )

    if OutputType.PATHS in task.requested_outputs:
        from app.reasoning.schemas import PathOutput
        result_payload["paths"] = PathOutput(
            paths=reasoning_paths,
            total_paths_found=len(reasoning_paths),
            returned_paths=len(reasoning_paths),
        ).model_dump()

    if OutputType.TEMPORARY_GRAPH in task.requested_outputs:
        nodes_in_graph = list(nodes_map.values())
        # Add target-candidate edges through shared neighbors as metadata links?
        temp_nodes = [
            TempGraphNode(
                temp_node_id=n.node_id,
                origin_graph="industrial",
                origin_node_id=n.node_id,
                node_type=n.entity_type or "unknown",
                label=n.canonical_name_zh or n.node_id,
                properties=node_to_dict(n),
                score=next((s for cid2, s, _ in scored if cid2 == n.node_id), None),
            )
            for n in nodes_in_graph
        ]
        result_payload["temporary_graph"] = TemporaryReasoningGraph(
            temp_graph_id=f"temp_{reasoning_id}",
            reasoning_id=reasoning_id,
            graph_scope="single_graph",
            source_graphs=["industrial"],
            nodes=temp_nodes,
            edges=[],
            created_at=datetime.utcnow(),
        ).model_dump()

    if OutputType.EVIDENCE_CHAINS in task.requested_outputs:
        result_payload["evidence_chains"] = [
            ec.model_dump()
            for ec in build_evidence_chains(nodes=list(nodes_map.values()), paths=reasoning_paths)
        ]

    if OutputType.FEATURE_TABLES in task.requested_outputs:
        rows = [
            {
                **node_to_dict(nodes_map[cid]),
                "substitution_score": score,
                **components,
            }
            for cid, score, components in scored
        ]
        result_payload["feature_tables"] = [
            FeatureTable(
                table_id=f"ft_substitution_{reasoning_id}",
                entity_level="candidate",
                columns=list(rows[0].keys()) if rows else [],
                rows=rows,
            ).model_dump()
        ]

    if task.parameters.get("include_company_exposures"):
        node_ids = [target_id] + [cid for cid, _, _ in scored]
        max_exp = int(task.parameters.get("max_company_exposures", 50))
        company_exposures = await build_company_exposures(node_ids, max_exposures=max_exp)
        if company_exposures:
            result_payload["company_exposures"] = company_exposures.model_dump()

    diagnostics = build_diagnostics(
        nodes=list(nodes_map.values()),
        edges=[],
        diagnostics=diagnostics,
        warnings=warnings,
        started_at=started_at,
    )

    return ReasoningResultEnvelope(
        reasoning_id=reasoning_id,
        task_id=task.task_id,
        task_type=task.task_type.value,
        status=ResultStatus.SUCCESS if scored else ResultStatus.NO_RESULT,
        generated_at=datetime.utcnow(),
        input_fingerprint="",
        output_types=[o.value for o in task.requested_outputs],
        result_payload=result_payload,
        diagnostics=diagnostics,
    )
