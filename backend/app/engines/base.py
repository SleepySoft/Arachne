"""
Abstract base class for all graph engines.

A graph engine is responsible for storing and querying the topology
(relationships) of industrial nodes. Node metadata lives in PostgreSQL and
is shared across engines via app.services.metadata_storage.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from app.models.core import EngineMetadata, GraphEdge, GraphNode, GraphStats, SubgraphResult


class GraphEngine(ABC):
    """Abstract base class for pluggable graph engines."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique engine identifier used in URLs and registry."""
        ...

    @property
    def metadata(self) -> EngineMetadata:
        """Return descriptive metadata for the engine.

        Subclasses should override this to expose engine-specific capabilities
        and default views to the frontend.
        """
        return EngineMetadata(
            name=self.name,
            label=self.name,
            description="",
            is_read_only=False,
            supports_flows=False,
            default_view="industrial_graph",
        )

    # -----------------------------------------------------------------------
    # Node topology operations
    # -----------------------------------------------------------------------

    @abstractmethod
    async def create_node(self, data: Any) -> GraphNode:
        """Create a node skeleton in the engine's graph store and return it."""
        ...

    @abstractmethod
    async def quick_create_node(self, data: Any) -> GraphNode:
        """Quick-create a draft node."""
        ...

    @abstractmethod
    async def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Return a node by ID, or None if not found."""
        ...

    @abstractmethod
    async def update_node(self, node_id: str, data: Any) -> Optional[GraphNode]:
        """Update a node and return the updated node, or None if not found."""
        ...

    @abstractmethod
    async def delete_node(self, node_id: str) -> bool:
        """Delete a node and its relationships. Return True if deleted."""
        ...

    @abstractmethod
    async def list_nodes(
        self,
        skip: int = 0,
        limit: int = 20,
        entity_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        draft_only: Optional[bool] = None,
    ) -> Tuple[List[GraphNode], int]:
        """Return a paginated list of nodes and the total count."""
        ...

    # -----------------------------------------------------------------------
    # Edge topology operations
    # -----------------------------------------------------------------------

    @abstractmethod
    async def create_edge(self, data: Any) -> GraphEdge:
        """Create an edge in the engine's graph store and return it."""
        ...

    @abstractmethod
    async def quick_create_edge(self, data: Any) -> GraphEdge:
        """Quick-create an edge with minimal input."""
        ...

    @abstractmethod
    async def create_reified_usage(self, data: Any) -> Any:
        """Create a PROV-style reified usage edge."""
        ...

    @abstractmethod
    async def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        """Return an edge by ID, or None if not found."""
        ...

    @abstractmethod
    async def update_edge(self, edge_id: str, data: Any, namespace: str) -> Optional[GraphEdge]:
        """Update an edge and return it, or None if not found."""
        ...

    @abstractmethod
    async def delete_edge(self, edge_id: str, namespace: str) -> bool:
        """Delete an edge. Return True if deleted."""
        ...

    @abstractmethod
    async def list_edges(
        self,
        skip: int = 0,
        limit: int = 20,
        edge_namespace: Optional[str] = None,
        edge_type: Optional[str] = None,
        from_node: Optional[str] = None,
        to_node: Optional[str] = None,
    ) -> Tuple[List[GraphEdge], int]:
        """Return a paginated list of edges and the total count."""
        ...

    # -----------------------------------------------------------------------
    # Query operations
    # -----------------------------------------------------------------------

    @abstractmethod
    async def get_subgraph(self, node_id: str, depth: int = 2) -> SubgraphResult:
        """Return the subgraph around a node up to a given depth."""
        ...

    @abstractmethod
    async def get_neighbors(self, node_id: str) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """Return direct neighbors and connecting edges of a node."""
        ...

    @abstractmethod
    async def get_paths(
        self,
        from_node: str,
        to_node: str,
        max_depth: int = 5,
    ) -> List[List[Dict[str, Any]]]:
        """Return paths from one node to another."""
        ...

    @abstractmethod
    async def get_stats(self) -> GraphStats:
        """Return graph statistics."""
        ...

    @abstractmethod
    async def get_incomplete_items(self, limit: int = 100) -> Dict[str, Any]:
        """Return a summary of incomplete/draft items."""
        ...

    @abstractmethod
    async def detect_conflicts(self) -> List[Dict[str, Any]]:
        """Detect potential conflicts in the graph."""
        ...
