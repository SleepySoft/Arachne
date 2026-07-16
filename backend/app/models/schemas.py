"""
Backward-compatibility schema re-exports.

This module used to contain all graph schema definitions. After the engine
subsystem refactor, the canonical locations are:

- app/models/core.py          — engine-agnostic primitives and generic models
- app/engines/legacy/schemas.py — legacy Neo4j engine node/edge/input models

Existing code can continue importing from app.models.schemas; new code should
import directly from core or from the engine-specific schema module.
"""

from __future__ import annotations

# Shared primitives / generic models
from app.models.core import (
    Confidence,
    Evidence,
    GraphEdge as CoreGraphEdge,
    GraphNode,
    GraphStats,
    NodeStatus,
    PaginatedEdges,
    PaginatedNodes,
    RecordStatus,
    SubgraphResult,
)

# Legacy engine schemas
from app.engines.legacy.schemas import (
    EDGE_TYPE_LABELS,
    BaseEdge,
    CandidateEntity,
    CandidateRelation,
    EntityType,
    GraphEdge,
    GraphEdgeCreate,
    GraphRegistrationBatch,
    GraphRegistrationInput,
    IndustrialFlowEdge,
    IndustrialFlowEdgeCreate,
    IndustrialFlowEdgeQuickCreate,
    IndustrialFlowEdgeUpdate,
    IndustrialFlowType,
    IndustrialNode,
    IndustrialNodeCreate,
    IndustrialNodeQuickCreate,
    IndustrialNodeUpdate,
    IndustryNodeAssociation,
    OntologyEdge,
    OntologyEdgeCreate,
    OntologyEdgeUpdate,
    OntologyType,
    PathResult,
    RejectedOrPendingItem,
    ReifiedUsageCreate,
    ReifiedUsageResult,
    ReviewAction,
)

__all__ = [
    # core primitives
    "Confidence",
    "Evidence",
    "NodeStatus",
    "RecordStatus",
    "CoreGraphEdge",
    "GraphNode",
    "GraphStats",
    "PaginatedEdges",
    "PaginatedNodes",
    "SubgraphResult",
    # legacy engine
    "EDGE_TYPE_LABELS",
    "BaseEdge",
    "CandidateEntity",
    "CandidateRelation",
    "EntityType",
    "GraphEdge",
    "GraphEdgeCreate",
    "GraphRegistrationBatch",
    "GraphRegistrationInput",
    "IndustrialFlowEdge",
    "IndustrialFlowEdgeCreate",
    "IndustrialFlowEdgeQuickCreate",
    "IndustrialFlowEdgeUpdate",
    "IndustrialFlowType",
    "IndustrialNode",
    "IndustrialNodeCreate",
    "IndustrialNodeQuickCreate",
    "IndustrialNodeUpdate",
    "IndustryNodeAssociation",
    "OntologyEdge",
    "OntologyEdgeCreate",
    "OntologyEdgeUpdate",
    "OntologyType",
    "PathResult",
    "RejectedOrPendingItem",
    "ReifiedUsageCreate",
    "ReifiedUsageResult",
    "ReviewAction",
]
