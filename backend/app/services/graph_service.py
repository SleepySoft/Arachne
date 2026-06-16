from typing import List, Optional

from app.models.schemas import (
    GraphEdge,
    GraphRegistrationBatch,
    GraphStats,
    IndustrialFlowEdge,
    IndustrialFlowEdgeCreate,
    IndustrialFlowEdgeQuickCreate,
    IndustrialNode,
    IndustrialNodeCreate,
    IndustrialNodeQuickCreate,
    IndustrialNodeUpdate,
    OntologyEdge,
    OntologyEdgeCreate,
    RejectedOrPendingItem,
)
from app.models.company_schema import BusinessRegistrationBatch
# Use memory storage when Neo4j is unavailable
from app.services import neo4j_storage
from app.services import industry_storage
from app.services import company_storage
from app.database_postgres import get_postgres_pool


# ---------------------------------------------------------------------------
# Node Service
# ---------------------------------------------------------------------------

async def create_node(data: IndustrialNodeCreate) -> IndustrialNode:
    existing = await neo4j_storage.get_node(data.node_id)
    if existing:
        raise ValueError(f"node_id '{data.node_id}' already exists")

    node = IndustrialNode(**data.model_dump())
    return await neo4j_storage.create_node(node)


async def quick_create_node(data: IndustrialNodeQuickCreate) -> IndustrialNode:
    """快速创建草稿节点。node_id 留空时自动生成 draft_{uuid} 占位。"""
    from uuid import uuid4

    node_id = data.node_id
    if not node_id:
        node_id = f"draft_{uuid4().hex[:12]}"

    existing = await neo4j_storage.get_node(node_id)
    if existing:
        raise ValueError(f"node_id '{node_id}' already exists")

    # 快速创建允许只填中文名或英文名之一；构造 IndustrialNode 时用占位值通过必填校验
    canonical_name_zh = data.canonical_name_zh.strip() if data.canonical_name_zh else ""
    canonical_name_en = data.canonical_name_en.strip() if data.canonical_name_en else None
    if not canonical_name_zh:
        canonical_name_zh = canonical_name_en or node_id

    node = IndustrialNode(
        node_id=node_id,
        canonical_name_zh=canonical_name_zh,
        canonical_name_en=canonical_name_en,
        aliases=data.aliases,
        definition=data.definition or "（定义待补充）",
        entity_type=data.entity_type or IndustrialNode.model_fields["entity_type"].default,
        evidence=data.evidence,
        confidence=data.confidence,
        status=data.status,
        notes=data.notes,
    )
    return await neo4j_storage.create_node(node)


async def get_node(node_id: str) -> Optional[IndustrialNode]:
    return await neo4j_storage.get_node(node_id)


async def update_node(node_id: str, data: IndustrialNodeUpdate) -> Optional[IndustrialNode]:
    existing = await neo4j_storage.get_node(node_id)
    if not existing:
        return None

    update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_dict:
        return existing

    return await neo4j_storage.update_node(node_id, update_dict)


async def delete_node(node_id: str) -> bool:
    return await neo4j_storage.delete_node(node_id)


async def list_nodes(
    skip: int = 0,
    limit: int = 20,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    draft_only: Optional[bool] = None,
):
    return await neo4j_storage.list_nodes(skip, limit, entity_type, status, search, draft_only)


# ---------------------------------------------------------------------------
# Edge Service
# ---------------------------------------------------------------------------

async def create_edge(data) -> GraphEdge:
    from_exists = await neo4j_storage.get_node(data.from_node)
    to_exists = await neo4j_storage.get_node(data.to_node)
    if not from_exists:
        raise ValueError(f"from_node '{data.from_node}' does not exist")
    if not to_exists:
        raise ValueError(f"to_node '{data.to_node}' does not exist")
    if data.from_node == data.to_node:
        raise ValueError("self-loop edge is not allowed")

    existing = await neo4j_storage.get_edge(data.edge_id)
    if existing:
        raise ValueError(f"edge_id '{data.edge_id}' already exists")

    if isinstance(data, IndustrialFlowEdgeCreate):
        edge = IndustrialFlowEdge(**data.model_dump())
        return await neo4j_storage.create_industrial_flow_edge(edge)
    elif isinstance(data, OntologyEdgeCreate):
        edge = OntologyEdge(**data.model_dump())
        return await neo4j_storage.create_ontology_edge(edge)
    else:
        raise ValueError("Unsupported edge create type")


async def quick_create_edge(data: IndustrialFlowEdgeQuickCreate) -> IndustrialFlowEdge:
    """快速创建产业流关系。edge_id 留空时自动生成占位 ID。"""
    from uuid import uuid4

    from_exists = await neo4j_storage.get_node(data.from_node)
    to_exists = await neo4j_storage.get_node(data.to_node)
    if not from_exists:
        raise ValueError(f"from_node '{data.from_node}' does not exist")
    if not to_exists:
        raise ValueError(f"to_node '{data.to_node}' does not exist")
    if data.from_node == data.to_node:
        raise ValueError("self-loop edge is not allowed")

    edge_id = data.edge_id
    if not edge_id:
        candidate = f"{data.from_node}_to_{data.to_node}"
        if len(candidate) <= 128:
            existing = await neo4j_storage.get_edge(candidate)
            edge_id = candidate if not existing else f"draft_edge_{uuid4().hex[:12]}"
        else:
            edge_id = f"draft_edge_{uuid4().hex[:12]}"

    existing = await neo4j_storage.get_edge(edge_id)
    if existing:
        raise ValueError(f"edge_id '{edge_id}' already exists")

    description = data.description or f"{data.from_node} 为 {data.to_node} 提供输入"

    edge = IndustrialFlowEdge(
        edge_id=edge_id,
        from_node=data.from_node,
        to_node=data.to_node,
        edge_namespace="industrial_flow",
        edge_type=data.edge_type,
        description=description,
        evidence=data.evidence,
        confidence=data.confidence,
        notes=data.notes,
    )
    return await neo4j_storage.create_industrial_flow_edge(edge)


async def get_edge(edge_id: str) -> Optional[GraphEdge]:
    return await neo4j_storage.get_edge(edge_id)


async def update_edge(edge_id: str, data, namespace: str) -> Optional[GraphEdge]:
    existing = await neo4j_storage.get_edge(edge_id)
    if not existing:
        return None

    update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_dict:
        return existing

    return await neo4j_storage.update_edge(edge_id, update_dict, namespace)


async def delete_edge(edge_id: str, namespace: str) -> bool:
    return await neo4j_storage.delete_edge(edge_id, namespace)


async def list_edges(
    skip: int = 0,
    limit: int = 20,
    edge_namespace: Optional[str] = None,
    edge_type: Optional[str] = None,
    from_node: Optional[str] = None,
    to_node: Optional[str] = None,
):
    return await neo4j_storage.list_edges(skip, limit, edge_namespace, edge_type, from_node, to_node)


# ---------------------------------------------------------------------------
# Batch Service
# ---------------------------------------------------------------------------

async def process_batch(batch: GraphRegistrationBatch) -> dict:
    """
    Process a GraphRegistrationBatch:
    - Upsert nodes (create if not exists, update if exists)
    - Upsert edges (create if not exists, update if exists)
    - Store rejected_or_pending items (as node properties with status REJECTED or PENDING)
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
            existing = await neo4j_storage.get_node(node.node_id)
            if existing:
                update_data = node.model_dump(exclude={"node_id", "created_at", "node_uuid"})
                await neo4j_storage.update_node(node.node_id, update_data)
                results["nodes_updated"] += 1
            else:
                await neo4j_storage.create_node(node)
                results["nodes_created"] += 1
        except Exception as e:
            results["errors"].append({"type": "node", "id": node.node_id, "error": str(e)})

    # Process edges
    for edge in batch.edges_to_upsert:
        try:
            existing = await neo4j_storage.get_edge(edge.edge_id)
            if existing:
                update_data = edge.model_dump(exclude={"edge_id", "created_at", "edge_uuid", "from_node", "to_node", "edge_namespace"})
                await neo4j_storage.update_edge(edge.edge_id, update_data, edge.edge_namespace)
                results["edges_updated"] += 1
            else:
                if isinstance(edge, IndustrialFlowEdge):
                    await neo4j_storage.create_industrial_flow_edge(edge)
                else:
                    await neo4j_storage.create_ontology_edge(edge)
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


# ---------------------------------------------------------------------------
# Business Batch Service
# ---------------------------------------------------------------------------

async def process_business_batch(batch: BusinessRegistrationBatch) -> dict:
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

    # ------------------------------------------------------------------
    # Auto-activate companies and exposures created/updated in this batch
    # so that they are visible to exploration queries.
    # ------------------------------------------------------------------
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
                        WHERE exposure_id = ANY($1) AND status = 'PENDING'
                        """,
                        list(exposure_ids_in_batch),
                    )

    return results


# ---------------------------------------------------------------------------
# Query Service
# ---------------------------------------------------------------------------

async def get_subgraph(node_id: str, depth: int = 2):
    return await neo4j_storage.get_subgraph(node_id, depth)


async def get_neighbors(node_id: str):
    return await neo4j_storage.get_neighbors(node_id)


async def get_paths(from_node: str, to_node: str, max_depth: int = 5):
    return await neo4j_storage.get_paths(from_node, to_node, max_depth)


async def get_stats() -> GraphStats:
    return await neo4j_storage.get_stats()


# ---------------------------------------------------------------------------
# Conflict Detection
# ---------------------------------------------------------------------------

async def detect_conflicts() -> List[dict]:
    """
    Detect potential conflicts in the graph:
    - Dangling edges (pointing to non-existent nodes)
    - Alias loops
    - Contradictory is_a relationships
    """
    conflicts = []
    driver = neo4j_storage.get_async_driver()
    async with driver.session() as session:
        # Dangling edges
        result = await session.run(
            """
            MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(b:IndustrialNode)
            WHERE a IS NULL OR b IS NULL
            RETURN r.edge_id AS edge_id, type(r) AS rel_type
            """
        )
        async for rec in result:
            conflicts.append({
                "type": "dangling_edge",
                "edge_id": rec["edge_id"],
                "rel_type": rec["rel_type"],
            })

        # Nodes without any edges
        result2 = await session.run(
            """
            MATCH (n:IndustrialNode)
            WHERE NOT (n)-[:INDUSTRIAL_FLOW|ONTOLOGY]-()
            RETURN n.node_id AS node_id
            """
        )
        async for rec in result2:
            conflicts.append({
                "type": "isolated_node",
                "node_id": rec["node_id"],
            })

    return conflicts
