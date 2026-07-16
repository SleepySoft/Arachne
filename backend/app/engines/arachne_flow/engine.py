"""Arachne-flow engine implementation."""

from __future__ import annotations

from typing import Any, List, Optional, Tuple

from app.engines.arachne_flow import storage
from app.engines.base import GraphEngine
from app.models.core import GraphEdge, GraphNode, GraphStats, SubgraphResult


class ReadOnlyEngineError(Exception):
    """Raised when a write operation is requested on the read-only arachne-flow engine."""


class ArachneFlowEngine(GraphEngine):
    """Read-only engine backed by compiled arachne-flow YAML graphs.

    The flow graph lives in a separate Neo4j space (:ARACHNE_FLOW edges and
    :ArachneFlowNode labels) and can be compiled from YAML files via
    ``storage.compile_parsed_flow``.
    """

    @property
    def name(self) -> str:
        return "arachne_flow"

    @property
    def supports_write(self) -> bool:
        return False

    # -----------------------------------------------------------------------
    # Nodes (read-only)
    # -----------------------------------------------------------------------

    async def create_node(self, data) -> GraphNode:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def quick_create_node(self, data) -> GraphNode:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def get_node(self, node_id: str) -> Optional[GraphNode]:
        return await storage.get_flow_node(node_id)

    async def update_node(self, node_id: str, data) -> Optional[GraphNode]:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def delete_node(self, node_id: str) -> bool:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def list_nodes(
        self,
        skip: int = 0,
        limit: int = 20,
        entity_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        draft_only: Optional[bool] = None,
    ) -> Tuple[List[GraphNode], int]:
        # status / draft_only are legacy metadata concepts; ignored for flow nodes.
        return await storage.list_flow_nodes(
            skip=skip, limit=limit, entity_type=entity_type, search=search
        )

    # -----------------------------------------------------------------------
    # Edges (read-only)
    # -----------------------------------------------------------------------

    async def create_edge(self, data) -> GraphEdge:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def quick_create_edge(self, data) -> GraphEdge:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def create_reified_usage(self, data):
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        return await storage.get_flow_edge(edge_id)

    async def update_edge(self, edge_id: str, data) -> Optional[GraphEdge]:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def delete_edge(self, edge_id: str) -> bool:
        raise ReadOnlyEngineError("arachne_flow engine is read-only; modify YAML and recompile")

    async def list_edges(
        self,
        skip: int = 0,
        limit: int = 20,
        edge_namespace: Optional[str] = None,
        edge_type: Optional[str] = None,
        from_node: Optional[str] = None,
        to_node: Optional[str] = None,
    ) -> Tuple[List[GraphEdge], int]:
        return await storage.list_flow_edges(
            skip=skip,
            limit=limit,
            edge_type=edge_type,
            from_node=from_node,
            to_node=to_node,
        )

    # -----------------------------------------------------------------------
    # Queries
    # -----------------------------------------------------------------------

    async def get_subgraph(self, node_id: str, depth: int) -> SubgraphResult:
        nodes, edges = await storage.get_flow_subgraph(node_id, depth)
        return SubgraphResult(
            center_node_id=node_id,
            depth=depth,
            nodes=nodes,
            edges=edges,
        )

    async def get_neighbors(self, node_id: str) -> Tuple[List[GraphNode], List[GraphEdge]]:
        return await storage.get_flow_neighbors(node_id)

    async def get_paths(
        self,
        from_node: str,
        to_node: str,
        max_depth: int,
    ) -> List[List[dict]]:
        return await storage.get_flow_paths(from_node, to_node, max_depth)

    async def get_stats(self) -> GraphStats:
        return await storage.get_flow_stats()

    async def get_incomplete_items(self, limit: int = 100) -> dict:
        return {
            "draft_nodes": [],
            "missing_definitions": [],
            "placeholder_edges": [],
            "isolated_nodes": [],
        }

    async def detect_conflicts(self) -> dict:
        return {"conflicts": []}
