"""Cross-graph context reasoning task.

Bridges the industrial graph with companies, industries, and factual relations
(persons) by following company_node_exposures, industry_node_mappings, and
factual_relations in PostgreSQL.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Set, Tuple

from app.reasoning.derived_from_utils import expand_by_derived_from
from app.reasoning.schemas import (
    CompanyExposuresOutput,
    EvidenceChain,
    FeatureTable,
    GraphType,
    MetadataLink,
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
    fetch_nodes_by_ids,
    node_to_dict,
    validate_source_nodes,
)
from app.reasoning.diagnostics import build_diagnostics
from app.reasoning.evidence import build_evidence_chains


async def _get_company_exposures(node_ids: List[str], limit: int) -> Tuple[List[Any], List[Any]]:
    from app.services import company_storage

    exposures = await company_storage.list_exposures_by_nodes(node_ids, limit=limit)
    if not exposures:
        return [], []
    company_ids = list({e.company_id for e in exposures})
    companies = await company_storage.get_companies_by_ids(company_ids)
    return exposures, companies


async def _get_industries_for_nodes(node_ids: List[str]) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Any]]:
    from app.services import industry_storage

    mappings_by_node: Dict[str, List[Dict[str, Any]]] = {}
    industry_ids: Set[str] = set()
    for nid in node_ids:
        mappings, _ = await industry_storage.list_mappings_by_node(nid, limit=100)
        mappings_by_node[nid] = [
            {
                "mapping_id": m.mapping_id,
                "industry_id": m.industry_id,
                "node_id": m.node_id,
                "role": m.role,
                "weight": m.weight,
            }
            for m in mappings
        ]
        industry_ids.update(m.industry_id for m in mappings)

    industries = {}
    if industry_ids:
        for iid in industry_ids:
            industry = await industry_storage.get_industry(iid)
            if industry:
                industries[iid] = industry
    return mappings_by_node, industries


async def _get_relations_for_companies(company_ids: List[str], limit_per_company: int = 20) -> Tuple[List[Any], List[Any]]:
    from app.services import factual_graph_storage

    relation_ids: Set[str] = set()
    all_relations: List[Any] = []
    person_ids: Set[str] = set()
    for cid in company_ids:
        rels_from, _ = await factual_graph_storage.list_relations(
            from_entity_id=cid, page_size=limit_per_company
        )
        rels_to, _ = await factual_graph_storage.list_relations(
            to_entity_id=cid, page_size=limit_per_company
        )
        for r in rels_from + rels_to:
            if r.relation_id not in relation_ids:
                relation_ids.add(r.relation_id)
                all_relations.append(r)
                if r.from_entity_type == "person":
                    person_ids.add(r.from_entity_id)
                if r.to_entity_type == "person":
                    person_ids.add(r.to_entity_id)

    persons = []
    if person_ids:
        for pid in person_ids:
            p = await factual_graph_storage.get_person(pid)
            if p:
                persons.append(p)
    return all_relations, persons


async def run_cross_graph_context(
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

    max_exposures = int(task.parameters.get("max_company_exposures", 50))
    exposures, companies = await _get_company_exposures(seed_nodes, max_exposures)
    company_map = {c.company_id: c for c in companies}

    mappings_by_node, industries = await _get_industries_for_nodes(seed_nodes)

    relations, persons = [], []
    if companies:
        relations, persons = await _get_relations_for_companies(
            list(company_map.keys()), limit_per_company=20
        )
    person_map = {p.person_id: p for p in persons}

    industrial_nodes_map = await fetch_nodes_by_ids(seed_nodes)

    result_payload: Dict[str, Any] = {}

    metadata_links: List[MetadataLink] = []
    temp_nodes: List[TempGraphNode] = []
    temp_edges: List[TempGraphEdge] = []
    reasoning_paths: List[ReasoningPath] = []

    # Industrial nodes
    for nid in seed_nodes:
        n = industrial_nodes_map.get(nid)
        if n is None:
            continue
        temp_nodes.append(
            TempGraphNode(
                temp_node_id=n.node_id,
                origin_graph="industrial",
                origin_node_id=n.node_id,
                node_type=n.entity_type or "unknown",
                label=n.canonical_name_zh or n.node_id,
                properties=node_to_dict(n),
            )
        )

    # Companies + exposure links
    for e in exposures:
        c = company_map.get(e.company_id)
        if c is None:
            continue
        temp_nodes.append(
            TempGraphNode(
                temp_node_id=c.company_id,
                origin_graph="factual",
                origin_node_id=c.company_id,
                node_type="company",
                label=c.name_zh or c.name_en or c.company_id,
                properties={
                    "company_id": c.company_id,
                    "name_zh": c.name_zh,
                    "name_en": c.name_en,
                    "company_type": c.company_type.value if c.company_type else None,
                    "stock_codes": c.stock_codes,
                },
            )
        )
        metadata_links.append(
            MetadataLink(
                from_object_id=e.node_id,
                from_graph="industrial",
                to_object_id=c.company_id,
                to_graph="factual",
                link_type=f"company_exposure:{e.activity_type.value if e.activity_type else 'unknown'}",
                properties={"role": e.role, "weight": e.weight, "confidence": e.confidence.value if e.confidence else None},
            )
        )
        reasoning_paths.append(
            ReasoningPath(
                path_id=f"path_{reasoning_id}_{len(reasoning_paths)}",
                start_node_id=e.node_id,
                end_node_id=c.company_id,
                node_sequence=[e.node_id, c.company_id],
                edge_sequence=[],
                graph_sequence=["industrial", "factual"],
                path_length=1,
                node_name_map={
                    e.node_id: {
                        "canonical_name_zh": getattr(industrial_nodes_map.get(e.node_id), "canonical_name_zh", None),
                        "canonical_name_en": getattr(industrial_nodes_map.get(e.node_id), "canonical_name_en", None),
                        "entity_type": getattr(industrial_nodes_map.get(e.node_id), "entity_type", None),
                    },
                    c.company_id: {"canonical_name_zh": c.name_zh, "canonical_name_en": c.name_en, "entity_type": "company"},
                },
            )
        )

    # Industries + mapping links
    for nid, mappings in mappings_by_node.items():
        for m in mappings:
            ind = industries.get(m["industry_id"])
            if ind is None:
                continue
            temp_nodes.append(
                TempGraphNode(
                    temp_node_id=ind.industry_id,
                    origin_graph="concept",
                    origin_node_id=ind.industry_id,
                    node_type="industry",
                    label=ind.name_zh or ind.name_en or ind.industry_id,
                    properties={
                        "industry_id": ind.industry_id,
                        "name_zh": ind.name_zh,
                        "name_en": ind.name_en,
                        "industry_type": ind.industry_type.value if ind.industry_type else None,
                    },
                )
            )
            metadata_links.append(
                MetadataLink(
                    from_object_id=ind.industry_id,
                    from_graph="concept",
                    to_object_id=nid,
                    to_graph="industrial",
                    link_type="industry_node_mapping",
                    properties={"role": m["role"], "weight": m["weight"]},
                )
            )

    # Persons + relation links
    for r in relations:
        other_id = r.to_entity_id if r.from_entity_type == "company" else r.from_entity_id
        other_type = r.to_entity_type if r.from_entity_type == "company" else r.from_entity_type
        if other_type != "person":
            continue
        person = person_map.get(other_id)
        if person is None:
            continue
        temp_nodes.append(
            TempGraphNode(
                temp_node_id=person.person_id,
                origin_graph="factual",
                origin_node_id=person.person_id,
                node_type="person",
                label=person.name_zh or person.name_en or person.person_id,
                properties={
                    "person_id": person.person_id,
                    "name_zh": person.name_zh,
                    "name_en": person.name_en,
                },
            )
        )
        company_id = r.from_entity_id if r.from_entity_type == "company" else r.to_entity_id
        metadata_links.append(
            MetadataLink(
                from_object_id=company_id,
                from_graph="factual",
                to_object_id=person.person_id,
                to_graph="factual",
                link_type=f"factual_relation:{r.relation_type}",
                properties={"relation_domain": r.relation_domain, "relation_id": r.relation_id},
            )
        )
        # Extend path: node -> company -> person
        for e in exposures:
            if e.company_id == company_id and e.node_id in seed_nodes:
                seq = [e.node_id, company_id, person.person_id]
                reasoning_paths.append(
                    ReasoningPath(
                        path_id=f"path_{reasoning_id}_{len(reasoning_paths)}",
                        start_node_id=e.node_id,
                        end_node_id=person.person_id,
                        node_sequence=seq,
                        edge_sequence=[],
                        graph_sequence=["industrial", "factual", "factual"],
                        path_length=2,
                        node_name_map={
                            nid2: {
                                "canonical_name_zh": getattr(industrial_nodes_map.get(nid2), "canonical_name_zh", None) if nid2 in industrial_nodes_map else (person.name_zh if nid2 == person.person_id else company_map.get(company_id, {}).name_zh),
                                "canonical_name_en": getattr(industrial_nodes_map.get(nid2), "canonical_name_en", None) if nid2 in industrial_nodes_map else (person.name_en if nid2 == person.person_id else None),
                                "entity_type": getattr(industrial_nodes_map.get(nid2), "entity_type", None) if nid2 in industrial_nodes_map else ("person" if nid2 == person.person_id else "company"),
                            }
                            for nid2 in seq
                        },
                    )
                )

    # Deduplicate temp nodes by id
    seen_node_ids: Set[str] = set()
    dedup_nodes: List[TempGraphNode] = []
    for n in temp_nodes:
        if n.temp_node_id in seen_node_ids:
            continue
        seen_node_ids.add(n.temp_node_id)
        dedup_nodes.append(n)

    if OutputType.TEMPORARY_GRAPH in task.requested_outputs:
        result_payload["temporary_graph"] = TemporaryReasoningGraph(
            temp_graph_id=f"temp_{reasoning_id}",
            reasoning_id=reasoning_id,
            graph_scope="cross_graph",
            source_graphs=["industrial", "factual", "concept"],
            nodes=dedup_nodes,
            edges=temp_edges,
            metadata_links=metadata_links,
            created_at=datetime.utcnow(),
        ).model_dump()

    if OutputType.PATHS in task.requested_outputs:
        from app.reasoning.schemas import PathOutput
        result_payload["paths"] = PathOutput(
            paths=reasoning_paths,
            total_paths_found=len(reasoning_paths),
            returned_paths=len(reasoning_paths),
        ).model_dump()

    if OutputType.EVIDENCE_CHAINS in task.requested_outputs:
        result_payload["evidence_chains"] = [
            ec.model_dump()
            for ec in build_evidence_chains(nodes=list(industrial_nodes_map.values()), paths=reasoning_paths)
        ]

    if OutputType.FEATURE_TABLES in task.requested_outputs:
        rows = [
            {
                "node_id": n.temp_node_id,
                "origin_graph": n.origin_graph,
                "node_type": n.node_type,
                "label": n.label,
            }
            for n in dedup_nodes
        ]
        if rows:
            result_payload["feature_tables"] = [
                FeatureTable(
                    table_id=f"ft_cross_graph_{reasoning_id}",
                    entity_level="node",
                    columns=list(rows[0].keys()),
                    rows=rows,
                ).model_dump()
            ]

    if exposures and OutputType.CANDIDATE_NODES not in task.requested_outputs:
        # Always return company exposures when available, unless user explicitly excluded by not requesting
        result_payload["company_exposures"] = CompanyExposuresOutput(
            total_companies=len(companies),
            total_exposures=len(exposures),
            companies=[],  # populated below if requested
        ).model_dump()

    # Build full CompanyExposuresOutput
    if OutputType.CANDIDATE_NODES in task.requested_outputs or "company_exposures" in result_payload:
        from app.reasoning.tasks.utils import ExposedNodeInfo, CompanyExposureInfo
        grouped: Dict[str, CompanyExposureInfo] = {}
        for e in exposures:
            c = company_map.get(e.company_id)
            if c is None:
                continue
            if c.company_id not in grouped:
                grouped[c.company_id] = CompanyExposureInfo(
                    company_id=c.company_id,
                    name_zh=c.name_zh,
                    name_en=c.name_en,
                    stock_codes=c.stock_codes or [],
                    company_type=c.company_type.value if c.company_type else None,
                    exposed_nodes=[],
                )
            grouped[c.company_id].exposed_nodes.append(
                ExposedNodeInfo(
                    node_id=e.node_id,
                    activity_type=e.activity_type.value if e.activity_type else None,
                    role=e.role,
                    weight=e.weight,
                    confidence=e.confidence.value if e.confidence else None,
                    canonical_name_zh=getattr(industrial_nodes_map.get(e.node_id), "canonical_name_zh", None),
                    canonical_name_en=getattr(industrial_nodes_map.get(e.node_id), "canonical_name_en", None),
                    entity_type=getattr(industrial_nodes_map.get(e.node_id), "entity_type", None),
                )
            )
        result_payload["company_exposures"] = CompanyExposuresOutput(
            total_companies=len(grouped),
            total_exposures=len(exposures),
            companies=list(grouped.values()),
        ).model_dump()

    diagnostics.graph_boundary_crossed = any(n.origin_graph != "industrial" for n in dedup_nodes)
    diagnostics.metadata_links_used = len(metadata_links)
    diagnostics = build_diagnostics(
        nodes=list(industrial_nodes_map.values()),
        edges=[],
        diagnostics=diagnostics,
        warnings=warnings,
        started_at=started_at,
    )

    return ReasoningResultEnvelope(
        reasoning_id=reasoning_id,
        task_id=task.task_id,
        task_type=task.task_type.value,
        status=ResultStatus.SUCCESS if dedup_nodes else ResultStatus.NO_RESULT,
        generated_at=datetime.utcnow(),
        input_fingerprint="",
        output_types=[o.value for o in task.requested_outputs],
        result_payload=result_payload,
        diagnostics=diagnostics,
    )
