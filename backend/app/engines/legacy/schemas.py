"""
Legacy engine schemas.

For the initial refactor, these are re-exported from app.models.schemas to
maintain full backward compatibility. In the future, engine-specific input
schemas can be defined here directly.
"""

from __future__ import annotations

from app.models.schemas import (
    Confidence,
    EntityType,
    Evidence,
    GraphEdge,
    GraphEdgeCreate,
    GraphRegistrationBatch,
    GraphStats,
    IndustrialFlowEdge,
    IndustrialFlowEdgeCreate,
    IndustrialFlowEdgeQuickCreate,
    IndustrialFlowEdgeUpdate,
    IndustrialFlowType,
    IndustryNodeAssociation,
    IndustrialNode,
    IndustrialNodeCreate,
    IndustrialNodeQuickCreate,
    IndustrialNodeUpdate,
    NodeStatus,
    OntologyEdge,
    OntologyEdgeCreate,
    OntologyEdgeUpdate,
    PaginatedEdges,
    PaginatedNodes,
    ReifiedUsageCreate,
    ReifiedUsageResult,
    SubgraphResult,
)

__all__ = [
    "Confidence",
    "EntityType",
    "Evidence",
    "GraphEdge",
    "GraphEdgeCreate",
    "GraphRegistrationBatch",
    "GraphStats",
    "IndustrialFlowEdge",
    "IndustrialFlowEdgeCreate",
    "IndustrialFlowEdgeQuickCreate",
    "IndustrialFlowEdgeUpdate",
    "IndustrialFlowType",
    "IndustryNodeAssociation",
    "IndustrialNode",
    "IndustrialNodeCreate",
    "IndustrialNodeQuickCreate",
    "IndustrialNodeUpdate",
    "NodeStatus",
    "OntologyEdge",
    "OntologyEdgeCreate",
    "OntologyEdgeUpdate",
    "PaginatedEdges",
    "PaginatedNodes",
    "ReifiedUsageCreate",
    "ReifiedUsageResult",
    "SubgraphResult",
]
