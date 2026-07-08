"""
Arachne Graph Reasoning Kernel — V0.2 Schemas

All Pydantic models for object query, reasoning tasks, and structured output.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from app.models.schemas import Confidence, Evidence


# ============================================================================
# Enums
# ============================================================================

class QueryScope(str, Enum):
    INDUSTRIAL_NODE = "industrial_node"
    INDUSTRIAL_EDGE = "industrial_edge"
    FACTUAL_NODE = "factual_node"
    FACTUAL_EDGE = "factual_edge"
    COMPANY = "company"
    INDUSTRY = "industry"
    CLAIM = "claim"


class SearchMode(str, Enum):
    EXACT = "exact"
    ALIAS = "alias"
    NORMALIZED = "normalized"
    KEYWORD = "keyword"
    PREFIX = "prefix"


class ObjectKind(str, Enum):
    NODE = "node"
    EDGE = "edge"
    CLAIM = "claim"
    METADATA = "metadata"


class GraphType(str, Enum):
    INDUSTRIAL = "industrial"
    FACTUAL = "factual"
    CONCEPT = "concept"


class MatchType(str, Enum):
    EXACT = "exact"
    ALIAS = "alias"
    NORMALIZED = "normalized"
    KEYWORD = "keyword"
    PREFIX = "prefix"
    METADATA = "metadata"


class TaskType(str, Enum):
    ASSOCIATION = "association"
    IMPACT_PROPAGATION = "impact_propagation"
    BOTTLENECK_DETECTION = "bottleneck_detection"
    SUBSTITUTION_SEARCH = "substitution_search"
    CANDIDATE_DISCOVERY = "candidate_discovery"
    CROSS_GRAPH_CONTEXT = "cross_graph_context"


class TraversalDirection(str, Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    BOTH = "both"


class OutputType(str, Enum):
    TEMPORARY_GRAPH = "temporary_graph"
    SUBGRAPH = "subgraph"
    PATHS = "paths"
    EVIDENCE_CHAINS = "evidence_chains"
    NODE_SCORES = "node_scores"
    EDGE_SCORES = "edge_scores"
    CANDIDATE_NODES = "candidate_nodes"
    CANDIDATE_EDGES = "candidate_edges"
    FEATURE_TABLES = "feature_tables"
    ADJACENCY_MATRIX = "adjacency_matrix"


class ResultStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    NO_RESULT = "no_result"


class EvidenceSupports(str, Enum):
    NODE = "node"
    EDGE = "edge"
    PATH = "path"
    CANDIDATE_NODE = "candidate_node"
    CANDIDATE_EDGE = "candidate_edge"
    SCORE = "score"


class EvidenceCompleteness(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    MISSING = "missing"


class TempGraphScope(str, Enum):
    SINGLE_GRAPH = "single_graph"
    CROSS_GRAPH = "cross_graph"


class OriginGraph(str, Enum):
    INDUSTRIAL = "industrial"
    FACTUAL = "factual"
    CONCEPT = "concept"
    IIS = "iis"
    REASONING = "reasoning"
    METADATA = "metadata"


class EntityLevel(str, Enum):
    NODE = "node"
    EDGE = "edge"
    PATH = "path"
    CANDIDATE = "candidate"


# ============================================================================
# Object Query
# ============================================================================

class ObjectQueryRequest(BaseModel):
    query_id: str = Field(..., description="上游查询追踪 ID")
    query_text: str = Field(..., description="查询文本（名称/别名/ID 片段）")
    query_scope: QueryScope = Field(..., description="查询对象类型")
    search_mode: SearchMode = Field(default=SearchMode.NORMALIZED)
    filters: Dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(default=20, ge=1, le=1000)
    include_evidence: bool = Field(default=False)
    include_metadata: bool = Field(default=True)


class ObjectCandidate(BaseModel):
    object_id: str
    object_kind: ObjectKind
    graph: Optional[GraphType] = None
    canonical_name: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    entity_type: Optional[str] = None
    edge_type: Optional[str] = None
    status: Optional[str] = None
    confidence: Optional[Confidence] = None
    match_type: MatchType
    match_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    evidence_refs: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ObjectQueryResult(BaseModel):
    query_id: str
    status: ResultStatus
    candidates: List[ObjectCandidate] = Field(default_factory=list)
    suggestions: List[ObjectCandidate] = Field(default_factory=list)
    diagnostics: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# Task Input
# ============================================================================

class TaskContext(BaseModel):
    region_ids: List[str] = Field(default_factory=list)
    time_window_start: Optional[datetime] = None
    time_window_end: Optional[datetime] = None
    metadata_filters: Dict[str, Any] = Field(default_factory=dict)
    upstream_system: Optional[str] = None
    upstream_trace_id: Optional[str] = None
    notes: Optional[str] = None


class ReasoningConstraints(BaseModel):
    max_depth: int = Field(default=3, ge=1, le=10)
    max_paths: int = Field(default=100, ge=1, le=10000)
    max_nodes: int = Field(default=500, ge=1, le=10000)
    max_edges: int = Field(default=1000, ge=1, le=20000)

    allowed_graphs: List[GraphType] = Field(default_factory=lambda: [GraphType.INDUSTRIAL])
    allowed_node_types: Optional[List[str]] = None
    allowed_edge_namespaces: Optional[List[str]] = None
    allowed_edge_types: Optional[List[str]] = None

    min_node_confidence: Confidence = Confidence.LOW
    min_edge_confidence: Confidence = Confidence.LOW

    include_pending_nodes: bool = False
    include_low_confidence_edges: bool = True

    traversal_direction: TraversalDirection = TraversalDirection.FORWARD
    stop_node_types: Optional[List[str]] = None

    allow_cross_graph_metadata_links: bool = False
    require_evidence: bool = False


class ReasoningTask(BaseModel):
    task_id: str
    task_type: TaskType

    source_nodes: List[str] = Field(default_factory=list)
    source_edges: List[str] = Field(default_factory=list)
    source_claims: List[str] = Field(default_factory=list)
    source_metadata: List[str] = Field(default_factory=list)

    parameters: Dict[str, Any] = Field(default_factory=dict)
    constraints: ReasoningConstraints = Field(default_factory=ReasoningConstraints)
    requested_outputs: List[OutputType] = Field(default_factory=list)
    context: Optional[TaskContext] = None


# ============================================================================
# Output Components
# ============================================================================

class TempGraphNode(BaseModel):
    temp_node_id: str
    origin_graph: Optional[OriginGraph] = None
    origin_node_id: Optional[str] = None
    node_type: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    score: Optional[float] = None
    score_components: Dict[str, Any] = Field(default_factory=dict)
    evidence_refs: List[str] = Field(default_factory=list)


class TempGraphEdge(BaseModel):
    temp_edge_id: str
    origin_graph: Optional[OriginGraph] = None
    origin_edge_id: Optional[str] = None
    from_temp_node_id: str
    to_temp_node_id: str
    edge_namespace: str
    edge_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    weight: Optional[float] = None
    score_components: Dict[str, Any] = Field(default_factory=dict)
    evidence_refs: List[str] = Field(default_factory=list)


class MetadataLink(BaseModel):
    from_object_id: str
    from_graph: OriginGraph
    to_object_id: str
    to_graph: OriginGraph
    link_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class TemporaryReasoningGraph(BaseModel):
    temp_graph_id: str
    reasoning_id: str
    graph_scope: TempGraphScope
    source_graphs: List[GraphType]
    nodes: List[TempGraphNode]
    edges: List[TempGraphEdge]
    metadata_links: List[MetadataLink] = Field(default_factory=list)
    created_at: datetime
    expires_at: Optional[datetime] = None


class SubgraphOutput(BaseModel):
    center_nodes: List[str]
    depth: int
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    truncated: bool = False
    truncation_reason: Optional[str] = None


class ReasoningPath(BaseModel):
    path_id: str
    start_node_id: str
    end_node_id: str
    node_sequence: List[str]
    edge_sequence: List[str]
    graph_sequence: List[str]
    path_length: int
    path_score: Optional[float] = None
    score_components: Dict[str, Any] = Field(default_factory=dict)
    node_name_map: Dict[str, Dict[str, Optional[str]]] = Field(default_factory=dict)
    evidence_chain_id: Optional[str] = None
    flags: List[str] = Field(default_factory=list)


class PathOutput(BaseModel):
    paths: List[ReasoningPath]
    total_paths_found: int
    returned_paths: int
    truncated: bool = False
    truncation_reason: Optional[str] = None


class EvidenceRef(BaseModel):
    evidence_id: str
    source_system: Literal[
        "industrial_graph", "factual_graph", "concept_graph", "iis", "manual"
    ]
    source_title: str
    source_url: Optional[str] = None
    quote: str
    collected_at: Optional[datetime] = None
    reliability: Confidence


class EvidenceChain(BaseModel):
    evidence_chain_id: str
    supports: EvidenceSupports
    target_id: str
    evidence_items: List[EvidenceRef]
    completeness: EvidenceCompleteness


class NodeScore(BaseModel):
    node_id: str
    graph: str
    score: float
    rank: int
    score_type: str
    score_components: Dict[str, Any]
    canonical_name_zh: Optional[str] = None
    canonical_name_en: Optional[str] = None
    entity_type: Optional[str] = None
    source_paths: List[str] = Field(default_factory=list)
    evidence_chain_ids: List[str] = Field(default_factory=list)
    flags: List[str] = Field(default_factory=list)


class EdgeScore(BaseModel):
    edge_id: str
    graph: str
    score: float
    rank: int
    score_type: str
    score_components: Dict[str, Any]
    from_node: Optional[str] = None
    to_node: Optional[str] = None
    from_node_name_zh: Optional[str] = None
    from_node_name_en: Optional[str] = None
    to_node_name_zh: Optional[str] = None
    to_node_name_en: Optional[str] = None
    edge_type: Optional[str] = None
    source_paths: List[str] = Field(default_factory=list)
    evidence_chain_ids: List[str] = Field(default_factory=list)
    flags: List[str] = Field(default_factory=list)


class ExposedNodeInfo(BaseModel):
    node_id: str
    canonical_name_zh: Optional[str] = None
    canonical_name_en: Optional[str] = None
    entity_type: Optional[str] = None
    activity_type: Optional[str] = None
    role: Optional[str] = None
    weight: Optional[float] = None
    confidence: Optional[str] = None


class CompanyExposureInfo(BaseModel):
    company_id: str
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    stock_codes: List[str] = Field(default_factory=list)
    company_type: Optional[str] = None
    exposed_nodes: List[ExposedNodeInfo] = Field(default_factory=list)


class CompanyExposuresOutput(BaseModel):
    total_companies: int
    total_exposures: int
    companies: List[CompanyExposureInfo]


class FeatureTable(BaseModel):
    table_id: str
    entity_level: EntityLevel
    columns: List[str]
    rows: List[Dict[str, Any]]


class ReasoningDiagnostics(BaseModel):
    truncated: bool = False
    truncation_reason: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    rule_violations: List[Dict[str, Any]] = Field(default_factory=list)
    missing_evidence_count: int = 0
    low_confidence_node_count: int = 0
    low_confidence_edge_count: int = 0
    pending_node_count: int = 0
    dangling_reference_count: int = 0
    graph_boundary_crossed: bool = False
    metadata_links_used: int = 0
    execution_time_ms: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CandidateNodeOutput(BaseModel):
    candidate_id: str
    proposed_graph: GraphType
    proposed_node_id: Optional[str] = None
    canonical_name: str
    aliases: List[str] = Field(default_factory=list)
    proposed_entity_type: Optional[str] = None
    source_claims: List[str] = Field(default_factory=list)
    nearest_existing_objects: List[str] = Field(default_factory=list)
    evidence_chain_ids: List[str] = Field(default_factory=list)
    validation_status: Literal["valid", "warning", "invalid", "needs_review"] = "needs_review"
    rule_violations: List[Dict[str, Any]] = Field(default_factory=list)
    flags: List[str] = Field(default_factory=list)


class CandidateEdgeOutput(BaseModel):
    candidate_id: str
    proposed_graph: GraphType
    from_object_id: Optional[str] = None
    to_object_id: Optional[str] = None
    from_text: Optional[str] = None
    to_text: Optional[str] = None
    proposed_edge_namespace: Optional[str] = None
    proposed_edge_type: Optional[str] = None
    source_claims: List[str] = Field(default_factory=list)
    evidence_chain_ids: List[str] = Field(default_factory=list)
    validation_status: Literal["valid", "warning", "invalid", "needs_review"] = "needs_review"
    rule_violations: List[Dict[str, Any]] = Field(default_factory=list)
    flags: List[str] = Field(default_factory=list)


# ============================================================================
# Result Envelope
# ============================================================================

class ReasoningResultEnvelope(BaseModel):
    reasoning_id: str
    task_id: str
    task_type: str
    status: ResultStatus
    generated_at: datetime
    input_fingerprint: str
    graph_snapshot_ids: List[str] = Field(default_factory=list)
    output_types: List[str] = Field(default_factory=list)
    result_payload: Dict[str, Any] = Field(default_factory=dict)
    diagnostics: ReasoningDiagnostics = Field(default_factory=ReasoningDiagnostics)
