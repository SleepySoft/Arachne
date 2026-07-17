"""Legacy industrial graph engine implementation."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from app.database_postgres import get_postgres_pool
from app.engines.base import GraphEngine
from app.models.core import EngineMetadata
from app.engines.legacy import schemas as legacy_schemas
from app.engines.legacy.storage import (
    create_industrial_flow_edge,
    create_node as storage_create_node,
    create_ontology_edge,
    delete_edge as storage_delete_edge,
    delete_node as storage_delete_node,
    get_async_driver,
    get_edge as storage_get_edge,
    get_neighbors as storage_get_neighbors,
    get_node as storage_get_node,
    get_paths as storage_get_paths,
    get_stats as storage_get_stats,
    get_subgraph as storage_get_subgraph,
    list_edges as storage_list_edges,
    list_nodes as storage_list_nodes,
    update_edge as storage_update_edge,
    update_node as storage_update_node,
)
from app.models.core import GraphEdge, GraphNode, GraphStats, SubgraphResult
from app.models.industry_schema import IndustryNodeMapping
from app.services import company_storage, industry_storage
from app.services.derived_from_policy import validate_derived_from_edge


class LegacyEngine(GraphEngine):
    """Engine implementation backed by the original Neo4j graph structure."""

    @property
    def name(self) -> str:
        return "legacy"

    @property
    def metadata(self) -> EngineMetadata:
        return EngineMetadata(
            name="legacy",
            label="legacy 引擎",
            description="原始产业图引擎，支持完整的节点/关系读写",
            is_read_only=False,
            supports_flows=False,
            default_view="industrial_graph",
        )

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    async def _create_node_industry_mapping(
        self,
        node_id: str,
        assoc: legacy_schemas.IndustryNodeAssociation,
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

    # -----------------------------------------------------------------------
    # Nodes
    # -----------------------------------------------------------------------

    async def create_node(self, data: Any) -> GraphNode:
        existing = await storage_get_node(data.node_id)
        if existing:
            raise ValueError(f"node_id '{data.node_id}' already exists")

        node = legacy_schemas.IndustrialNode(**data.model_dump(exclude={"industry_ids"}))
        created = await storage_create_node(node)

        for assoc in data.industry_ids:
            await self._create_node_industry_mapping(created.node_id, assoc, node_is_test=node.is_test)

        return created

    async def quick_create_node(self, data: Any) -> GraphNode:
        from uuid import uuid4

        node_id = data.node_id
        if not node_id:
            node_id = f"draft_{uuid4().hex[:12]}"

        existing = await storage_get_node(node_id)
        if existing:
            raise ValueError(f"node_id '{node_id}' already exists")

        canonical_name_zh = data.canonical_name_zh.strip() if data.canonical_name_zh else ""
        canonical_name_en = data.canonical_name_en.strip() if data.canonical_name_en else None
        if not canonical_name_zh:
            canonical_name_zh = canonical_name_en or node_id

        node = legacy_schemas.IndustrialNode(
            node_id=node_id,
            canonical_name_zh=canonical_name_zh,
            canonical_name_en=canonical_name_en,
            aliases=data.aliases,
            definition=data.definition or "（定义待补充）",
            entity_type=data.entity_type or legacy_schemas.IndustrialNode.model_fields["entity_type"].default,
            evidence=data.evidence,
            confidence=data.confidence,
            status=data.status,
            notes=data.notes,
            is_test=data.is_test or False,
        )
        created = await storage_create_node(node)

        for assoc in data.industry_ids:
            await self._create_node_industry_mapping(created.node_id, assoc, node_is_test=data.is_test or False)

        return created

    async def get_node(self, node_id: str) -> Optional[GraphNode]:
        return await storage_get_node(node_id)

    async def update_node(self, node_id: str, data: Any) -> Optional[GraphNode]:
        existing = await storage_get_node(node_id)
        if not existing:
            return None

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_dict:
            return existing

        return await storage_update_node(node_id, update_dict)

    async def delete_node(self, node_id: str) -> bool:
        return await storage_delete_node(node_id)

    async def list_nodes(
        self,
        skip: int = 0,
        limit: int = 20,
        entity_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        draft_only: Optional[bool] = None,
    ) -> Tuple[List[GraphNode], int]:
        return await storage_list_nodes(skip, limit, entity_type, status, search, draft_only)

    # -----------------------------------------------------------------------
    # Edges
    # -----------------------------------------------------------------------

    async def create_edge(self, data: Any) -> GraphEdge:
        from_exists = await storage_get_node(data.from_node)
        to_exists = await storage_get_node(data.to_node)
        if not from_exists:
            raise ValueError(f"from_node '{data.from_node}' does not exist")
        if not to_exists:
            raise ValueError(f"to_node '{data.to_node}' does not exist")
        if data.from_node == data.to_node:
            raise ValueError("self-loop edge is not allowed")

        if isinstance(data, legacy_schemas.IndustrialFlowEdgeCreate) and data.edge_type == "derived_from":
            await validate_derived_from_edge(data.from_node, data.to_node)

        existing = await storage_get_edge(data.edge_id)
        if existing:
            raise ValueError(f"edge_id '{data.edge_id}' already exists")

        if isinstance(data, legacy_schemas.IndustrialFlowEdgeCreate):
            edge = legacy_schemas.IndustrialFlowEdge(**data.model_dump())
            return await create_industrial_flow_edge(edge)
        elif isinstance(data, legacy_schemas.OntologyEdgeCreate):
            edge = legacy_schemas.OntologyEdge(**data.model_dump())
            return await create_ontology_edge(edge)
        else:
            raise ValueError("Unsupported edge create type")

    async def quick_create_edge(self, data: Any) -> GraphEdge:
        from uuid import uuid4

        from_exists = await storage_get_node(data.from_node)
        to_exists = await storage_get_node(data.to_node)
        if not from_exists:
            raise ValueError(f"from_node '{data.from_node}' does not exist")
        if not to_exists:
            raise ValueError(f"to_node '{data.to_node}' does not exist")
        if data.from_node == data.to_node:
            raise ValueError("self-loop edge is not allowed")

        if data.edge_type == "derived_from":
            await validate_derived_from_edge(data.from_node, data.to_node)

        edge_id = data.edge_id
        if not edge_id:
            candidate = f"{data.from_node}_to_{data.to_node}"
            if len(candidate) <= 128:
                existing = await storage_get_edge(candidate)
                edge_id = candidate if not existing else f"draft_edge_{uuid4().hex[:12]}"
            else:
                edge_id = f"draft_edge_{uuid4().hex[:12]}"

        existing = await storage_get_edge(edge_id)
        if existing:
            raise ValueError(f"edge_id '{edge_id}' already exists")

        description = data.description or f"{data.from_node} 为 {data.to_node} 提供输入"

        edge = legacy_schemas.IndustrialFlowEdge(
            edge_id=edge_id,
            from_node=data.from_node,
            to_node=data.to_node,
            edge_namespace="industrial_flow",
            edge_type=data.edge_type,
            description=description,
            evidence=data.evidence,
            confidence=data.confidence,
            notes=data.notes,
            is_test=data.is_test or False,
        )
        return await create_industrial_flow_edge(edge)

    async def create_reified_usage(self, data: Any) -> Any:
        from uuid import uuid4
        import hashlib

        execution = await storage_get_node(data.execution_node_id)
        if execution is None:
            raise ValueError(f"execution_node_id '{data.execution_node_id}' does not exist")
        technology = await storage_get_node(data.technology_node_id)
        if technology is None:
            raise ValueError(f"technology_node_id '{data.technology_node_id}' does not exist")

        base = f"{data.execution_node_id}_{data.technology_node_id}_{data.scenario or ''}"
        if len(base) > 50:
            base = hashlib.md5(base.encode()).hexdigest()[:16]
        usage_id = f"usage_{base}"
        if len(usage_id) > 64:
            usage_id = f"usage_{hashlib.md5(base.encode()).hexdigest()[:16]}"

        existing_usage = await storage_get_node(usage_id)
        if existing_usage is not None:
            raise ValueError(f"reified usage '{usage_id}' already exists")

        execution_label = execution.canonical_name_zh or data.execution_node_id
        technology_label = technology.canonical_name_zh or data.technology_node_id
        scenario_text = f"（{data.scenario}）" if data.scenario else ""
        description = data.description or (
            f"{execution_label}{scenario_text} 使用 {technology_label} 技术/方法"
        )

        usage_node = legacy_schemas.IndustrialNode(
            node_id=usage_id,
            canonical_name_zh=f"{execution_label} 使用 {technology_label}{scenario_text}",
            canonical_name_en=None,
            aliases=[],
            definition=description,
            entity_type=legacy_schemas.EntityType.USAGE,
            evidence=data.evidence,
            confidence=data.confidence,
            status=data.status,
            notes=data.notes,
            is_test=data.is_test or False,
        )
        await storage_create_node(usage_node)

        uses_edge_id = f"{data.execution_node_id}_uses_{usage_id}"
        if len(uses_edge_id) > 64:
            uses_edge_id = f"uses_{hashlib.md5(uses_edge_id.encode()).hexdigest()[:16]}"
        adopts_edge_id = f"{usage_id}_adopts_{data.technology_node_id}"
        if len(adopts_edge_id) > 64:
            adopts_edge_id = f"adopts_{hashlib.md5(adopts_edge_id.encode()).hexdigest()[:16]}"

        if await storage_get_edge(uses_edge_id):
            uses_edge_id = f"uses_{uuid4().hex[:12]}"
        if await storage_get_edge(adopts_edge_id):
            adopts_edge_id = f"adopts_{uuid4().hex[:12]}"

        uses_edge = legacy_schemas.IndustrialFlowEdge(
            edge_id=uses_edge_id,
            from_node=data.execution_node_id,
            to_node=usage_id,
            edge_namespace="industrial_flow",
            edge_type=legacy_schemas.IndustrialFlowType.USES,
            description=f"{execution_label} 使用 {technology_label}{scenario_text}",
            evidence=data.evidence,
            confidence=data.confidence,
            notes=data.notes,
            is_test=data.is_test or False,
        )
        adopts_edge = legacy_schemas.IndustrialFlowEdge(
            edge_id=adopts_edge_id,
            from_node=usage_id,
            to_node=data.technology_node_id,
            edge_namespace="industrial_flow",
            edge_type=legacy_schemas.IndustrialFlowType.ADOPTS,
            description=f"{execution_label} 采用 {technology_label}{scenario_text}",
            evidence=data.evidence,
            confidence=data.confidence,
            notes=data.notes,
            is_test=data.is_test or False,
        )

        created_uses = await create_industrial_flow_edge(uses_edge)
        created_adopts = await create_industrial_flow_edge(adopts_edge)

        return legacy_schemas.ReifiedUsageResult(
            usage_node=usage_node,
            uses_edge=created_uses,
            adopts_edge=created_adopts,
        )

    async def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        return await storage_get_edge(edge_id)

    async def update_edge(self, edge_id: str, data: Any, namespace: str) -> Optional[GraphEdge]:
        existing = await storage_get_edge(edge_id)
        if not existing:
            return None

        update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_dict:
            return existing

        new_edge_type = update_dict.get("edge_type", existing.edge_type)
        if namespace == "industrial_flow" and new_edge_type == "derived_from":
            from_node = update_dict.get("from_node", existing.from_node)
            to_node = update_dict.get("to_node", existing.to_node)
            await validate_derived_from_edge(from_node, to_node)

        return await storage_update_edge(edge_id, update_dict, namespace)

    async def delete_edge(self, edge_id: str, namespace: str) -> bool:
        return await storage_delete_edge(edge_id, namespace)

    async def list_edges(
        self,
        skip: int = 0,
        limit: int = 20,
        edge_namespace: Optional[str] = None,
        edge_type: Optional[str] = None,
        from_node: Optional[str] = None,
        to_node: Optional[str] = None,
    ) -> Tuple[List[GraphEdge], int]:
        return await storage_list_edges(skip, limit, edge_namespace, edge_type, from_node, to_node)

    # -----------------------------------------------------------------------
    # Query
    # -----------------------------------------------------------------------

    async def get_subgraph(self, node_id: str, depth: int = 2) -> SubgraphResult:
        nodes, edges = await storage_get_subgraph(node_id, depth)
        return SubgraphResult(
            center_node_id=node_id,
            depth=depth,
            nodes=nodes,
            edges=edges,
        )

    async def get_neighbors(self, node_id: str) -> Tuple[List[GraphNode], List[GraphEdge]]:
        return await storage_get_neighbors(node_id)

    async def get_paths(self, from_node: str, to_node: str, max_depth: int = 5) -> List[List[Dict[str, Any]]]:
        return await storage_get_paths(from_node, to_node, max_depth)

    async def get_stats(self) -> GraphStats:
        return await storage_get_stats()

    # -----------------------------------------------------------------------
    # Conflict / incomplete
    # -----------------------------------------------------------------------

    async def get_incomplete_items(self, limit: int = 100) -> Dict[str, Any]:
        from app.services import node_storage

        driver = get_async_driver()
        summary = {
            "draft_nodes": 0,
            "pending_nodes": 0,
            "unknown_type_nodes": 0,
            "missing_definition_nodes": 0,
            "draft_edges": 0,
            "low_confidence_edges": 0,
            "placeholder_description_edges": 0,
            "isolated_nodes": 0,
        }
        node_issues = []
        edge_issues = []

        pool = await get_postgres_pool()
        if pool is not None:
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT node_id, canonical_name_zh AS name_zh, canonical_name_en AS name_en,
                           status, entity_type, definition, confidence,
                           node_id LIKE 'draft_%' AS is_draft,
                           status = 'PENDING' AS is_pending,
                           entity_type = 'unknown' AS is_unknown_type,
                           definition IS NULL OR definition = '' OR definition = '（定义待补充）' AS is_missing_definition
                    FROM industrial_nodes
                    ORDER BY updated_at DESC
                    LIMIT $1
                    """,
                    limit,
                )
            for rec in rows:
                issues = []
                if rec["is_draft"]:
                    issues.append("draft_id")
                    summary["draft_nodes"] += 1
                if rec["is_pending"]:
                    issues.append("pending_status")
                    summary["pending_nodes"] += 1
                if rec["is_unknown_type"]:
                    issues.append("unknown_type")
                    summary["unknown_type_nodes"] += 1
                if rec["is_missing_definition"]:
                    issues.append("missing_definition")
                    summary["missing_definition_nodes"] += 1
                if issues:
                    node_issues.append({
                        "node_id": rec["node_id"],
                        "name_zh": rec["name_zh"],
                        "name_en": rec["name_en"],
                        "status": rec["status"],
                        "entity_type": rec["entity_type"],
                        "confidence": rec["confidence"],
                        "issues": issues,
                    })

        async with driver.session() as session:
            result2 = await session.run(
                """
                MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(b:IndustrialNode)
                RETURN r.edge_id AS edge_id,
                       r.edge_namespace AS edge_namespace,
                       r.edge_type AS edge_type,
                       r.description AS description,
                       r.confidence AS confidence,
                       a.node_id AS from_node,
                       b.node_id AS to_node,
                       r.edge_id STARTS WITH 'draft_edge_' AS is_draft,
                       r.confidence = 'LOW' AS is_low_confidence,
                       r.description IS NULL OR r.description = '' OR r.description STARTS WITH '由系统自动生成' AS is_placeholder_desc
                ORDER BY r.updated_at DESC
                LIMIT $limit
                """,
                limit=limit,
            )
            async for rec in result2:
                issues = []
                if rec["is_draft"]:
                    issues.append("draft_id")
                    summary["draft_edges"] += 1
                if rec["is_low_confidence"]:
                    issues.append("low_confidence")
                    summary["low_confidence_edges"] += 1
                if rec["is_placeholder_desc"]:
                    issues.append("placeholder_description")
                    summary["placeholder_description_edges"] += 1
                if issues:
                    edge_issues.append({
                        "edge_id": rec["edge_id"],
                        "edge_namespace": rec["edge_namespace"],
                        "edge_type": rec["edge_type"],
                        "from_node": rec["from_node"],
                        "to_node": rec["to_node"],
                        "description": rec["description"],
                        "confidence": rec["confidence"],
                        "issues": issues,
                    })

            result3 = await session.run(
                """
                MATCH (n:IndustrialNode)
                WHERE NOT (n)-[:INDUSTRIAL_FLOW|ONTOLOGY]-()
                RETURN n.node_id AS node_id
                LIMIT $limit
                """,
                limit=limit,
            )
            isolated_ids = [rec["node_id"] async for rec in result3]
            isolated_name_map = await node_storage.get_nodes_by_ids(isolated_ids)
            for node_id in isolated_ids:
                summary["isolated_nodes"] += 1
                node = isolated_name_map.get(node_id)
                existing = next((x for x in node_issues if x["node_id"] == node_id), None)
                if existing:
                    if "isolated" not in existing["issues"]:
                        existing["issues"].append("isolated")
                else:
                    node_issues.append({
                        "node_id": node_id,
                        "name_zh": node.canonical_name_zh if node else node_id,
                        "name_en": node.canonical_name_en if node else None,
                        "status": node.status.value if node else None,
                        "entity_type": node.entity_type.value if node else None,
                        "confidence": node.confidence.value if node else None,
                        "issues": ["isolated"],
                    })

        return {
            "summary": summary,
            "nodes": node_issues,
            "edges": edge_issues,
            "total_issues": len(node_issues) + len(edge_issues),
        }

    async def detect_conflicts(self) -> List[Dict[str, Any]]:
        conflicts = []
        driver = get_async_driver()
        async with driver.session() as session:
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
