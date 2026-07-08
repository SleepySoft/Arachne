"""Bottleneck detection reasoning task.

Identifies nodes in the upstream/downstream supply graph that are highly shared,
have few alternatives, and lie on many source-to-leaf paths.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from app.database import get_async_driver
from app.reasoning.derived_from_utils import expand_by_derived_from
from app.reasoning.topology import resolve_sources_topologically
from app.reasoning.schemas import (
    CandidateNodeOutput,
    EvidenceChain,
    FeatureTable,
    GraphType,
    NodeScore,
    OutputType,
    PathOutput,
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
    allowed_confidence_values,
    build_allowed_rel_types,
    build_company_exposures,
    collect_unique_edges,
    collect_unique_node_ids,
    fetch_nodes_by_ids,
    node_to_dict,
    validate_source_nodes,
)
from app.reasoning.diagnostics import build_diagnostics
from app.reasoning.evidence import build_evidence_chains


async def _fetch_reachable_subgraph(
    source_ids: List[str],
    constraints: Any,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Fetch nodes and edges reachable from source_ids within constraints."""
    driver = get_async_driver()
    rel_pattern = build_allowed_rel_types(constraints)
    max_depth = constraints.max_depth
    limit = constraints.max_paths
    allowed_confidences = allowed_confidence_values(
        constraints.min_edge_confidence,
        constraints.include_low_confidence_edges,
    )
    edge_types = constraints.allowed_edge_types

    edge_filters = ["coalesce(rel.confidence, 'LOW') IN $allowed_confidences"]
    params: Dict[str, Any] = {
        "source_ids": source_ids,
        "max_depth": max_depth,
        "limit": limit,
        "allowed_confidences": allowed_confidences,
    }
    if edge_types:
        edge_filters.append("coalesce(rel.edge_type, 'unknown') IN $edge_types")
        params["edge_types"] = edge_types

    where_clause = " AND ".join(edge_filters)

    def make_cypher(direction: str) -> str:
        if direction == "forward":
            rel_clause = f"-[r:{rel_pattern}*1..{max_depth}]->"
        elif direction == "backward":
            rel_clause = f"<-[r:{rel_pattern}*1..{max_depth}]-"
        else:
            rel_clause = f"-[r:{rel_pattern}*1..{max_depth}]-"
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

    paths: List[Dict[str, Any]] = []
    if constraints.traversal_direction in ("forward", "both"):
        for sid in source_ids:
            cypher = make_cypher("forward")
            params["source_id"] = sid
            async with driver.session() as session:
                result = await session.run(cypher, **params)
                async for record in result:
                    paths.append({
                        "node_ids": record["node_ids"],
                        "rels": record["rels"],
                    })
    if constraints.traversal_direction in ("backward", "both"):
        for sid in source_ids:
            cypher = make_cypher("backward")
            params["source_id"] = sid
            async with driver.session() as session:
                result = await session.run(cypher, **params)
                async for record in result:
                    paths.append({
                        "node_ids": record["node_ids"],
                        "rels": record["rels"],
                    })

    node_ids = collect_unique_node_ids(paths)
    node_ids.update(source_ids)
    edge_records = collect_unique_edges(paths)
    nodes_map = await fetch_nodes_by_ids(list(node_ids))
    nodes = list(nodes_map.values())
    edges = list(edge_records.values())
    return nodes, edges


def _build_adjacency(
    edges: List[Dict[str, Any]],
    directed: bool,
) -> Tuple[Dict[str, Set[str]], Dict[str, Dict[str, Any]]]:
    """Build adjacency sets and edge lookup."""
    adj: Dict[str, Set[str]] = defaultdict(set)
    edge_lookup: Dict[str, Dict[str, Any]] = {}
    for e in edges:
        frm = e.get("from_node")
        to = e.get("to_node")
        eid = e.get("edge_id")
        if frm and to:
            adj[frm].add(to)
            if directed:
                adj[to]  # ensure key exists
            else:
                adj[to].add(frm)
        if eid:
            edge_lookup[eid] = e
    return adj, edge_lookup


def _collect_simple_paths(
    sources: Set[str],
    adj: Dict[str, Set[str]],
    max_depth: int,
    max_paths: int,
) -> Tuple[List[List[str]], Dict[str, int], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """DFS simple paths from each source up to max_depth.

    Returns:
      - paths: list of node sequences
      - node_path_count: how many paths include each node
      - source_reach: source nodes that can reach each node
      - leaf_reach: leaf nodes reachable from each node
    """
    paths: List[List[str]] = []
    node_path_count: Dict[str, int] = defaultdict(int)
    source_reach: Dict[str, Set[str]] = defaultdict(set)
    leaf_reach: Dict[str, Set[str]] = defaultdict(set)

    total = 0
    for src in sources:
        stack: List[Tuple[str, List[str]]] = [(src, [src])]
        while stack and total < max_paths:
            node, seq = stack.pop()
            depth = len(seq) - 1
            if depth > 0:
                node_path_count[node] += 1
                source_reach[node].add(src)
            is_leaf = True
            if depth < max_depth:
                for nxt in adj.get(node, set()):
                    if nxt in seq:
                        continue
                    is_leaf = False
                    stack.append((nxt, seq + [nxt]))
            if is_leaf and depth > 0:
                leaf_reach[src].add(node)
                paths.append(seq)
                total += 1
                if total >= max_paths:
                    break
    return paths, node_path_count, source_reach, leaf_reach


def _score_bottlenecks(
    nodes_map: Dict[str, Any],
    sources: Set[str],
    adj: Dict[str, Set[str]],
    node_path_count: Dict[str, int],
    source_reach: Dict[str, Set[str]],
    leaf_reach: Dict[str, Set[str]],
) -> List[Tuple[str, float, Dict[str, Any]]]:
    """Return nodes sorted by bottleneck score (higher = more critical)."""
    total_paths = max(1, sum(node_path_count.values()))
    total_sources = max(1, len(sources))
    scored: List[Tuple[str, float, Dict[str, Any]]] = []
    for nid, node in nodes_map.items():
        if nid in sources:
            continue
        shared_sources = len(source_reach.get(nid, set()))
        downstream_leaves = set()
        for s in source_reach.get(nid, set()):
            downstream_leaves |= leaf_reach.get(s, set())
        supplier_count = len([p for p in adj.get(nid, set()) if p != nid])
        betweenness = node_path_count.get(nid, 0)
        # Heuristic bottleneck score
        score = (
            (shared_sources / total_sources)
            * (1 + betweenness / total_paths)
            * (1.0 / (1 + supplier_count))
            * (1 + len(downstream_leaves) / max(1, len(sources)))
        )
        components = {
            "shared_sources": shared_sources,
            "supplier_count": supplier_count,
            "betweenness_proxy": betweenness,
            "downstream_leaf_count": len(downstream_leaves),
        }
        scored.append((nid, score, components))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


async def run_bottleneck_detection(
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

    # 1. Always resolve alias_of to canonical targets.
    try:
        canonical_ids, details = await resolve_sources_topologically(
            existing, expand_ontology=False
        )
        alias_map = details.get("aliases_resolved", {})
        aliased = {k: v for k, v in alias_map.items() if k != v}
        if aliased:
            warnings.append(
                f"Resolved {len(aliased)} alias source(s) to canonical node(s): {aliased}"
            )
        seed_nodes = sorted(canonical_ids)
    except Exception as exc:
        warnings.append(f"alias resolution failed: {exc}")
        seed_nodes = existing

    # 2. Expand derived_from material lineage.
    expand_derived = task.parameters.get("expand_derived_from", True)
    if expand_derived:
        try:
            expanded = await expand_by_derived_from(seed_nodes, direction="both", max_hops=5)
            before = len(seed_nodes)
            seed_nodes = sorted(expanded)
            if len(seed_nodes) > before:
                warnings.append(
                    f"Expanded {before} source(s) to {len(seed_nodes)} equivalent nodes via derived_from"
                )
        except Exception as exc:
            warnings.append(f"derived_from expansion failed: {exc}")

    # 3. Optionally expand ontology semantics (is_a, part_of, related).
    expand_ontology = task.parameters.get("expand_ontology", False)
    if expand_ontology:
        try:
            before = len(seed_nodes)
            effective, details = await resolve_sources_topologically(
                seed_nodes, expand_ontology=True, max_ontology_hops=2
            )
            seed_nodes = sorted(effective)
            if len(seed_nodes) > before:
                warnings.append(
                    f"Expanded {before} seed(s) to {len(seed_nodes)} nodes via ontology topology"
                )
            diagnostics.metadata["topology_expansion"] = {
                k: sorted(v) if isinstance(v, set) else v
                for k, v in details.items()
            }
        except Exception as exc:
            warnings.append(f"ontology expansion failed: {exc}")

    nodes, edges = await _fetch_reachable_subgraph(seed_nodes, task.constraints)
    nodes_map = {n.node_id: n for n in nodes}
    nodes_map.update(await fetch_nodes_by_ids(seed_nodes))
    nodes = list(nodes_map.values())

    if len(nodes) > task.constraints.max_nodes:
        warnings.append(f"Subgraph truncated from {len(nodes)} to {task.constraints.max_nodes} nodes")
        diagnostics.truncated = True
        diagnostics.truncation_reason = "max_nodes reached"
        kept = set(seed_nodes) | set([n.node_id for n in nodes if n.node_id not in seed_nodes][: task.constraints.max_nodes])
        nodes = [n for n in nodes if n.node_id in kept]
        nodes_map = {n.node_id: n for n in nodes}

    directed = task.constraints.traversal_direction != "both"
    adj, edge_lookup = _build_adjacency(edges, directed=directed)

    paths, node_path_count, source_reach, leaf_reach = _collect_simple_paths(
        set(seed_nodes),
        adj,
        task.constraints.max_depth,
        task.constraints.max_paths,
    )

    scored = _score_bottlenecks(
        nodes_map,
        set(seed_nodes),
        adj,
        node_path_count,
        source_reach,
        leaf_reach,
    )

    result_payload: Dict[str, Any] = {}

    reasoning_paths = [
        ReasoningPath(
            path_id=f"path_{reasoning_id}_{idx}",
            start_node_id=p[0],
            end_node_id=p[-1],
            node_sequence=p,
            edge_sequence=[],
            graph_sequence=["industrial"] * len(p),
            path_length=len(p) - 1,
            node_name_map={
                nid: {
                    "canonical_name_zh": getattr(nodes_map.get(nid), "canonical_name_zh", None),
                    "canonical_name_en": getattr(nodes_map.get(nid), "canonical_name_en", None),
                    "entity_type": getattr(nodes_map.get(nid), "entity_type", None),
                }
                for nid in p
            },
        )
        for idx, p in enumerate(paths)
    ]

    if OutputType.NODE_SCORES in task.requested_outputs:
        result_payload["node_scores"] = [
            NodeScore(
                node_id=nid,
                graph="industrial",
                score=round(score, 6),
                rank=idx + 1,
                score_type="bottleneck_score",
                score_components=components,
                canonical_name_zh=getattr(nodes_map.get(nid), "canonical_name_zh", None),
                canonical_name_en=getattr(nodes_map.get(nid), "canonical_name_en", None),
                entity_type=getattr(nodes_map.get(nid), "entity_type", None),
            ).model_dump()
            for idx, (nid, score, components) in enumerate(scored)
        ]

    if OutputType.CANDIDATE_NODES in task.requested_outputs:
        top_n = task.parameters.get("top_n", 20)
        result_payload["candidate_nodes"] = [
            CandidateNodeOutput(
                candidate_id=f"bottleneck_{reasoning_id}_{idx}",
                proposed_graph=GraphType.INDUSTRIAL,
                proposed_node_id=nid,
                canonical_name=getattr(nodes_map.get(nid), "canonical_name_zh", None) or nid,
                aliases=getattr(nodes_map.get(nid), "aliases", []) or [],
                proposed_entity_type=getattr(nodes_map.get(nid), "entity_type", None),
                source_claims=task.source_claims,
                nearest_existing_objects=list(source_reach.get(nid, set()))[:5],
                validation_status="valid",
                flags=["bottleneck_candidate"],
            ).model_dump()
            for idx, (nid, _, _) in enumerate(scored[:top_n])
        ]

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
                score=next((s for nid2, s, _ in scored if nid2 == n.node_id), None),
            )
            for n in nodes
        ]
        temp_edges = [
            TempGraphEdge(
                temp_edge_id=e.get("edge_id", f"edge_{reasoning_id}_{idx}"),
                origin_graph="industrial",
                origin_edge_id=e.get("edge_id"),
                from_temp_node_id=e["from_node"],
                to_temp_node_id=e["to_node"],
                edge_namespace=e.get("edge_namespace", "industrial_flow"),
                edge_type=e.get("edge_type", "unknown"),
                properties=e,
            )
            for idx, e in enumerate(edges)
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

    if OutputType.EVIDENCE_CHAINS in task.requested_outputs:
        result_payload["evidence_chains"] = [
            ec.model_dump()
            for ec in build_evidence_chains(nodes=nodes, edges=edges, paths=reasoning_paths)
        ]

    if OutputType.FEATURE_TABLES in task.requested_outputs:
        rows = [
            {
                **node_to_dict(n),
                "bottleneck_score": next((s for nid2, s, _ in scored if nid2 == n.node_id), 0.0),
            }
            for n in nodes
        ]
        result_payload["feature_tables"] = [
            FeatureTable(
                table_id=f"ft_bottleneck_nodes_{reasoning_id}",
                entity_level="node",
                columns=list(rows[0].keys()) if rows else [],
                rows=rows,
            ).model_dump()
        ]

    if task.parameters.get("include_company_exposures"):
        node_ids = [n.node_id for n in nodes]
        max_exp = int(task.parameters.get("max_company_exposures", 50))
        company_exposures = await build_company_exposures(node_ids, max_exposures=max_exp)
        if company_exposures:
            result_payload["company_exposures"] = company_exposures.model_dump()

    diagnostics = build_diagnostics(
        nodes=nodes,
        edges=edges,
        diagnostics=diagnostics,
        warnings=warnings,
        started_at=started_at,
    )

    return ReasoningResultEnvelope(
        reasoning_id=reasoning_id,
        task_id=task.task_id,
        task_type=task.task_type.value,
        status=ResultStatus.SUCCESS if nodes else ResultStatus.NO_RESULT,
        generated_at=datetime.utcnow(),
        input_fingerprint="",
        output_types=[o.value for o in task.requested_outputs],
        result_payload=result_payload,
        diagnostics=diagnostics,
    )
