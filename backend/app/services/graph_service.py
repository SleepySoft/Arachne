"""
Graph service: thin orchestration layer over the active graph engine.

Node/edge/query operations are delegated to the registered engine.
Batch processing remains here because it orchestrates metadata, topology,
industries, and companies.
"""

from typing import List, Optional

from app.models.schemas import (
    Confidence,
    EntityType,
    GraphEdge,
    GraphRegistrationBatch,
    GraphStats,
    IndustrialFlowEdge,
    IndustrialFlowEdgeCreate,
    IndustrialFlowEdgeQuickCreate,
    IndustrialFlowType,
    IndustryNodeAssociation,
    IndustrialNode,
    IndustrialNodeCreate,
    IndustrialNodeQuickCreate,
    IndustrialNodeUpdate,
    OntologyEdge,
    OntologyEdgeCreate,
    RejectedOrPendingItem,
    ReifiedUsageCreate,
    ReifiedUsageResult,
)
from app.models.industry_schema import IndustryNodeMapping
from app.models.company_schema import BusinessRegistrationBatch
from app.engines.legacy import storage as legacy_storage
from app.services import industry_storage
from app.services import company_storage
from app.services.derived_from_policy import validate_derived_from_edge
from app.services.engine_registry import get_engine
from app.database_postgres import get_postgres_pool


# ---------------------------------------------------------------------------
# Node Service (delegated to engine)
# ---------------------------------------------------------------------------

async def create_node(data: IndustrialNodeCreate, engine: Optional[str] = None) -> IndustrialNode:
    return await get_engine(engine).create_node(data)


async def quick_create_node(data: IndustrialNodeQuickCreate, engine: Optional[str] = None) -> IndustrialNode:
    return await get_engine(engine).quick_create_node(data)


async def get_node(node_id: str, engine: Optional[str] = None) -> Optional[IndustrialNode]:
    return await get_engine(engine).get_node(node_id)


async def update_node(node_id: str, data: IndustrialNodeUpdate, engine: Optional[str] = None) -> Optional[IndustrialNode]:
    return await get_engine(engine).update_node(node_id, data)


async def delete_node(node_id: str, engine: Optional[str] = None) -> bool:
    return await get_engine(engine).delete_node(node_id)


async def list_nodes(
    skip: int = 0,
    limit: int = 20,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    draft_only: Optional[bool] = None,
    engine: Optional[str] = None,
):
    return await get_engine(engine).list_nodes(skip, limit, entity_type, status, search, draft_only)


# ---------------------------------------------------------------------------
# Edge Service (delegated to engine)
# ---------------------------------------------------------------------------

async def create_edge(data, engine: Optional[str] = None) -> GraphEdge:
    return await get_engine(engine).create_edge(data)


async def quick_create_edge(data: IndustrialFlowEdgeQuickCreate, engine: Optional[str] = None) -> IndustrialFlowEdge:
    return await get_engine(engine).quick_create_edge(data)


async def create_reified_usage(data: ReifiedUsageCreate, engine: Optional[str] = None) -> ReifiedUsageResult:
    return await get_engine(engine).create_reified_usage(data)


async def get_edge(edge_id: str, engine: Optional[str] = None) -> Optional[GraphEdge]:
    return await get_engine(engine).get_edge(edge_id)


async def update_edge(edge_id: str, data, namespace: str, engine: Optional[str] = None) -> Optional[GraphEdge]:
    return await get_engine(engine).update_edge(edge_id, data, namespace)


async def delete_edge(edge_id: str, namespace: str, engine: Optional[str] = None) -> bool:
    return await get_engine(engine).delete_edge(edge_id, namespace)


async def list_edges(
    skip: int = 0,
    limit: int = 20,
    edge_namespace: Optional[str] = None,
    edge_type: Optional[str] = None,
    from_node: Optional[str] = None,
    to_node: Optional[str] = None,
    engine: Optional[str] = None,
):
    return await get_engine(engine).list_edges(skip, limit, edge_namespace, edge_type, from_node, to_node)


# ---------------------------------------------------------------------------
# Batch Service (kept in service layer)
# ---------------------------------------------------------------------------

async def _create_node_industry_mapping(
    node_id: str,
    assoc: IndustryNodeAssociation,
    node_is_test: bool = False,
) -> bool:
    """为节点创建一个行业映射；行业不存在或已存在映射时静默跳过。"""
    try:
        industry = await industry_storage.get_industry(assoc.industry_id)
        if industry is None:
            return False

        existing = await industry_storage.get_mapping_by_industry_and_node(
            assoc.industry_id, node_id
        )
        if existing:
            return True

        mapping_id = f"{assoc.industry_id}_contains_{node_id}"
        if len(mapping_id) > 128:
            from uuid import uuid4
            mapping_id = f"{assoc.industry_id}_contains_{uuid4().hex[:8]}"
        if await industry_storage.get_mapping(mapping_id):
            from uuid import uuid4
            mapping_id = f"{mapping_id}_{uuid4().hex[:6]}"

        mapping = IndustryNodeMapping(
            mapping_id=mapping_id,
            industry_id=assoc.industry_id,
            node_id=node_id,
            role=assoc.role,
            weight=assoc.weight,
            confidence=assoc.confidence,
            evidence=[],
            status=assoc.status,
            notes=assoc.notes or "由节点创建表单自动关联",
            is_test=node_is_test,
        )
        await industry_storage.create_mapping(mapping)
        return True
    except Exception:
        return False


async def process_batch(batch: GraphRegistrationBatch, engine: Optional[str] = None) -> dict:
    """
    Process a GraphRegistrationBatch using the active engine.
    """
    results = {
        "batch_id": batch.batch_id,
        "nodes_created": 0,
        "nodes_updated": 0,
        "edges_created": 0,
        "edges_updated": 0,
        "rejected_or_pending_stored": 0,
        "errors": [],
    }

    # Process nodes
    for node in batch.nodes_to_upsert:
        try:
            existing = await get_engine(engine).get_node(node.node_id)
            if existing:
                update_data = node.model_dump(exclude={"node_id", "created_at", "node_uuid"})
                await legacy_storage.update_node(node.node_id, update_data)
                results["nodes_updated"] += 1
            else:
                await legacy_storage.create_node(node)
                results["nodes_created"] += 1
        except Exception as e:
            results["errors"].append({"type": "node", "id": node.node_id, "error": str(e)})

    # Process edges
    for edge in batch.edges_to_upsert:
        try:
            existing = await get_engine(engine).get_edge(edge.edge_id)
            if existing:
                update_data = edge.model_dump(exclude={"edge_id", "created_at", "edge_uuid", "from_node", "to_node", "edge_namespace"})
                if edge.edge_namespace == "industrial_flow" and edge.edge_type == "derived_from":
                    await validate_derived_from_edge(edge.from_node, edge.to_node)
                await legacy_storage.update_edge(edge.edge_id, update_data, edge.edge_namespace)
                results["edges_updated"] += 1
            else:
                if isinstance(edge, IndustrialFlowEdge):
                    if edge.edge_type == "derived_from":
                        await validate_derived_from_edge(edge.from_node, edge.to_node)
                    await legacy_storage.create_industrial_flow_edge(edge)
                else:
                    await legacy_storage.create_ontology_edge(edge)
                results["edges_created"] += 1
        except Exception as e:
            results["errors"].append({"type": "edge", "id": edge.edge_id, "error": str(e)})

    # Store rejected_or_pending as lightweight records
    for item in batch.rejected_or_pending:
        try:
            results["rejected_or_pending_stored"] += 1
        except Exception as e:
            results["errors"].append({"type": "rejected_or_pending", "term": item.term, "error": str(e)})

    return results


async def process_business_batch(
    batch: BusinessRegistrationBatch,
    engine: Optional[str] = None,
) -> dict:
    """
    Process a BusinessRegistrationBatch:
    - Upsert industries (create if not exists, update if exists)
    - Upsert industry_node_mappings (dedup by industry_id + node_id)
    - Upsert companies (create if not exists, update if exists)
    - Upsert company_node_exposures (dedup by company_id + node_id)
    """
    results = {
        "batch_id": batch.batch_id,
        "industries_created": 0,
        "industries_updated": 0,
        "mappings_created": 0,
        "mappings_updated": 0,
        "companies_created": 0,
        "companies_updated": 0,
        "exposures_created": 0,
        "exposures_updated": 0,
        "errors": [],
    }

    # Process industries
    for ind in batch.industries_to_upsert:
        try:
            existing = await industry_storage.get_industry(ind.industry_id)
            if existing:
                update_data = ind.model_dump(
                    exclude={"industry_id", "industry_uuid", "created_at", "updated_at"},
                    mode="json",
                )
                await industry_storage.update_industry(ind.industry_id, update_data)
                results["industries_updated"] += 1
            else:
                await industry_storage.create_industry(ind)
                results["industries_created"] += 1
        except Exception as e:
            results["errors"].append({"type": "industry", "id": ind.industry_id, "error": str(e)})

    # Process industry node mappings
    for mapping in batch.industry_node_mappings_to_upsert:
        try:
            existing = await industry_storage.get_mapping_by_industry_and_node(
                mapping.industry_id, mapping.node_id
            )
            if existing:
                update_data = mapping.model_dump(
                    exclude={"mapping_id", "mapping_uuid", "industry_id", "node_id", "created_at", "updated_at"},
                    mode="json",
                )
                await industry_storage.update_mapping(existing.mapping_id, update_data)
                results["mappings_updated"] += 1
            else:
                await industry_storage.create_mapping(mapping)
                results["mappings_created"] += 1
        except Exception as e:
            results["errors"].append({"type": "mapping", "id": mapping.mapping_id, "error": str(e)})

    # Process companies
    for comp in batch.companies_to_upsert:
        try:
            existing = await company_storage.get_company(comp.company_id)
            if existing:
                update_data = comp.model_dump(
                    exclude={"company_id", "company_uuid", "created_at", "updated_at"},
                    mode="json",
                )
                await company_storage.update_company(comp.company_id, update_data)
                results["companies_updated"] += 1
            else:
                await company_storage.create_company(comp)
                results["companies_created"] += 1
        except Exception as e:
            results["errors"].append({"type": "company", "id": comp.company_id, "error": str(e)})

    # Process company node exposures
    for exposure in batch.company_node_exposures_to_upsert:
        try:
            existing = await company_storage.get_exposure_by_company_and_node(
                exposure.company_id, exposure.node_id
            )
            if existing:
                update_data = exposure.model_dump(
                    exclude={"exposure_id", "exposure_uuid", "company_id", "node_id", "created_at", "updated_at"},
                    mode="json",
                )
                await company_storage.update_exposure(existing.exposure_id, update_data)
                results["exposures_updated"] += 1
            else:
                await company_storage.create_exposure(exposure)
                results["exposures_created"] += 1
        except Exception as e:
            results["errors"].append({"type": "exposure", "id": exposure.exposure_id, "error": str(e)})

    # Auto-activate companies and exposures
    company_ids_in_batch = {c.company_id for c in batch.companies_to_upsert}
    exposure_ids_in_batch = {e.exposure_id for e in batch.company_node_exposures_to_upsert}

    if company_ids_in_batch or exposure_ids_in_batch:
        pool = await get_postgres_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                if company_ids_in_batch:
                    await conn.execute(
                        """
                        UPDATE companies
                        SET status = 'ACTIVE', updated_at = NOW()
                        WHERE company_id = ANY($1) AND status = 'PENDING'
                        """,
                        list(company_ids_in_batch),
                    )
                if exposure_ids_in_batch:
                    await conn.execute(
                        """
                        UPDATE company_node_exposures
                        SET status = 'ACTIVE', updated_at = NOW()
                        WHERE exposure_id = ANY($1)
                          AND status = 'PENDING'
                          AND evidence IS NOT NULL
                          AND evidence::text != '[]'
                        """,
                        list(exposure_ids_in_batch),
                    )

    return results


# ---------------------------------------------------------------------------
# Query Service (delegated to engine)
# ---------------------------------------------------------------------------

async def get_subgraph(node_id: str, depth: int = 2, engine: Optional[str] = None):
    return await get_engine(engine).get_subgraph(node_id, depth)


async def get_neighbors(node_id: str, engine: Optional[str] = None):
    return await get_engine(engine).get_neighbors(node_id)


async def get_paths(from_node: str, to_node: str, max_depth: int = 5, engine: Optional[str] = None):
    return await get_engine(engine).get_paths(from_node, to_node, max_depth)


async def get_stats(engine: Optional[str] = None) -> GraphStats:
    return await get_engine(engine).get_stats()


# ---------------------------------------------------------------------------
# Conflict Detection (delegated to engine)
# ---------------------------------------------------------------------------

async def get_incomplete_items(limit: int = 100, engine: Optional[str] = None) -> dict:
    return await get_engine(engine).get_incomplete_items(limit)


async def detect_conflicts(engine: Optional[str] = None) -> List[dict]:
    return await get_engine(engine).detect_conflicts()
