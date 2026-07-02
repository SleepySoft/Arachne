"""
Arachne Graph Reasoning Kernel API

Provides:
  - Object Query API  (name/alias -> candidate IDs)
  - Reasoning Execution API (deterministic graph reasoning)
"""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.reasoning.engine import execute_reasoning_task
from app.reasoning.schemas import (
    GraphType,
    MatchType,
    ObjectCandidate,
    ObjectKind,
    ObjectQueryRequest,
    ObjectQueryResult,
    ReasoningResultEnvelope,
    ReasoningTask,
    ResultStatus,
)
from app.services import (
    company_storage,
    factual_graph_storage,
    fuzzy_search,
    industry_storage,
    neo4j_storage,
)

router = APIRouter()


# ============================================================================
# Object Query
# ============================================================================

def _node_candidate(node: Any, match_type: MatchType, score: float | None = None) -> ObjectCandidate:
    return ObjectCandidate(
        object_id=node.node_id,
        object_kind=ObjectKind.NODE,
        graph=GraphType.INDUSTRIAL,
        canonical_name=node.canonical_name_zh or node.canonical_name_en,
        aliases=node.aliases or [],
        entity_type=node.entity_type,
        status=node.status,
        confidence=node.confidence,
        match_type=match_type,
        match_score=score,
    )


def _company_candidate(company: Any, match_type: MatchType) -> ObjectCandidate:
    return ObjectCandidate(
        object_id=company.company_id,
        object_kind=ObjectKind.NODE,
        graph=GraphType.FACTUAL,
        canonical_name=company.name_zh or company.name_en,
        aliases=company.aliases or [],
        status=company.status,
        confidence=None,
        match_type=match_type,
    )


def _industry_candidate(industry: Any, match_type: MatchType) -> ObjectCandidate:
    return ObjectCandidate(
        object_id=industry.industry_id,
        object_kind=ObjectKind.METADATA,
        graph=None,
        canonical_name=industry.name_zh or industry.name_en,
        aliases=industry.aliases or [],
        status=industry.status,
        confidence=None,
        match_type=match_type,
    )


def _person_candidate(person: Any, match_type: MatchType) -> ObjectCandidate:
    return ObjectCandidate(
        object_id=person.person_id,
        object_kind=ObjectKind.NODE,
        graph=GraphType.FACTUAL,
        canonical_name=person.name_zh or person.name_en,
        aliases=person.aliases or [],
        status=person.status,
        confidence=None,
        match_type=match_type,
    )


def _edge_candidate(edge: Any, match_type: MatchType) -> ObjectCandidate:
    return ObjectCandidate(
        object_id=edge.edge_id,
        object_kind=ObjectKind.EDGE,
        graph=GraphType.INDUSTRIAL,
        canonical_name=f"{edge.from_node} -> {edge.to_node}",
        entity_type=None,
        edge_type=getattr(edge, "edge_type", None),
        status=None,
        confidence=edge.confidence,
        match_type=match_type,
    )


async def _query_industrial_nodes(req: ObjectQueryRequest) -> List[ObjectCandidate]:
    candidates: List[ObjectCandidate] = []

    # Exact ID match first
    if req.search_mode in (MatchType.EXACT, MatchType.NORMALIZED, MatchType.ALIAS):
        node = await neo4j_storage.get_node(req.query_text)
        if node is not None:
            candidates.append(_node_candidate(node, MatchType.EXACT, 1.0))

    # Fuzzy / keyword search
    if req.search_mode in (MatchType.NORMALIZED, MatchType.KEYWORD, MatchType.PREFIX, MatchType.ALIAS):
        scored = await fuzzy_search.fuzzy_search_nodes(
            query=req.query_text,
            limit=req.limit,
        )
        for item in scored:
            node = item["node"]
            # Avoid duplicate exact match
            if any(c.object_id == node.node_id for c in candidates):
                continue
            candidates.append(_node_candidate(node, MatchType.NORMALIZED, item["score"]))

    return candidates[: req.limit]


async def _query_companies(req: ObjectQueryRequest) -> List[ObjectCandidate]:
    items, _ = await company_storage.list_companies(
        search=req.query_text,
        limit=req.limit,
    )
    return [_company_candidate(c, MatchType.KEYWORD) for c in items]


async def _query_industries(req: ObjectQueryRequest) -> List[ObjectCandidate]:
    items, _ = await industry_storage.list_industries(
        search=req.query_text,
        limit=req.limit,
    )
    return [_industry_candidate(i, MatchType.KEYWORD) for i in items]


async def _query_factual_nodes(req: ObjectQueryRequest) -> List[ObjectCandidate]:
    # Person search; companies are handled via _query_companies
    items, _ = await factual_graph_storage.list_persons(
        search=req.query_text,
        page_size=req.limit,
    )
    return [_person_candidate(p, MatchType.KEYWORD) for p in items]


async def _query_industrial_edges(req: ObjectQueryRequest) -> List[ObjectCandidate]:
    items, _ = await neo4j_storage.list_edges(limit=1000)
    query = req.query_text.lower()
    matched = [
        e for e in items
        if query in e.edge_id.lower()
        or query in e.from_node.lower()
        or query in e.to_node.lower()
        or query in (getattr(e, "edge_type", "") or "").lower()
    ]
    return [_edge_candidate(e, MatchType.KEYWORD) for e in matched[: req.limit]]


async def _query_factual_edges(req: ObjectQueryRequest) -> List[ObjectCandidate]:
    relation = await factual_graph_storage.get_relation(req.query_text)
    if relation is None:
        return []
    return [
        ObjectCandidate(
            object_id=relation.relation_id,
            object_kind=ObjectKind.EDGE,
            graph=GraphType.FACTUAL,
            canonical_name=f"{relation.relation_domain}: {relation.relation_type}",
            status=relation.status,
            confidence=relation.confidence,
            match_type=MatchType.EXACT,
        )
    ]


@router.post("/query", response_model=ObjectQueryResult)
async def query_objects(req: ObjectQueryRequest):
    """Resolve query text to candidate object IDs."""
    try:
        if req.query_scope.value == "industrial_node":
            candidates = await _query_industrial_nodes(req)
        elif req.query_scope.value == "company":
            candidates = await _query_companies(req)
        elif req.query_scope.value == "industry":
            candidates = await _query_industries(req)
        elif req.query_scope.value == "factual_node":
            candidates = await _query_factual_nodes(req)
        elif req.query_scope.value == "industrial_edge":
            candidates = await _query_industrial_edges(req)
        elif req.query_scope.value == "factual_edge":
            candidates = await _query_factual_edges(req)
        else:
            candidates = []
    except Exception as exc:
        return ObjectQueryResult(
            query_id=req.query_id,
            status=ResultStatus.FAILED,
            diagnostics={"error": str(exc)},
        )

    status = ResultStatus.SUCCESS if candidates else ResultStatus.NO_RESULT
    return ObjectQueryResult(
        query_id=req.query_id,
        status=status,
        candidates=candidates,
        diagnostics={"returned": len(candidates)},
    )


# ============================================================================
# Reasoning Execution
# ============================================================================

@router.post("/execute", response_model=ReasoningResultEnvelope)
async def execute_reasoning(req: ReasoningTask):
    """Execute a deterministic reasoning task on exact object IDs."""
    return await execute_reasoning_task(req)
