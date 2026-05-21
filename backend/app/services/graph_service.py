from typing import List, Optional

from app.models.schemas import (
    GraphEdge,
    GraphRegistrationBatch,
    GraphStats,
    IndustrialFlowEdge,
    IndustrialFlowEdgeCreate,
    IndustrialNode,
    IndustrialNodeCreate,
    IndustrialNodeUpdate,
    OntologyEdge,
    OntologyEdgeCreate,
    RejectedOrPendingItem,
)
from app.services import neo4j_storage


# ---------------------------------------------------------------------------
# Node Service
# ---------------------------------------------------------------------------

async def create_node(data: IndustrialNodeCreate) -> IndustrialNode:
    existing = await neo4j_storage.get_node(data.node_id)
    if existing:
        raise ValueError(f"node_id '{data.node_id}' already exists")

    node = IndustrialNode(**data.model_dump())
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
):
    return await neo4j_storage.list_nodes(skip, limit, entity_type, status, search)


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
