"""
Core graph models shared across all engines.

These models define the minimal common contract between the API layer and
engine subsystems. They intentionally keep a small, stable surface area.
Engine-specific schemas (e.g. IndustrialNodeCreate) live under
app/engines/<name>/schemas.py.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, field_validator


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class NodeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


RecordStatus = NodeStatus


class Evidence(BaseModel):
    source_title: str = Field(..., description="资料标题")
    source_url: Optional[HttpUrl] = Field(default=None, description="资料URL")
    quote: str = Field(..., description="原文摘录")

    @field_validator("source_title", "quote")
    @classmethod
    def non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v


class GraphNode(BaseModel):
    """Generic node returned by any graph engine."""

    node_id: str = Field(..., description="稳定英文小写蛇形命名")
    label: str = Field(..., description="显示名称（如中文名）")
    entity_type: str = Field(..., description="节点类型，引擎决定合法值")

    # Optional common metadata
    node_uuid: Optional[UUID] = Field(default=None)
    canonical_name_zh: Optional[str] = Field(default=None)
    canonical_name_en: Optional[str] = Field(default=None)
    aliases: List[str] = Field(default_factory=list)
    definition: Optional[str] = Field(default=None)
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    is_test: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Engine-specific extension properties
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """Generic edge returned by any graph engine."""

    edge_id: str = Field(..., description="稳定边ID")
    from_node: str = Field(..., description="起点节点ID")
    to_node: str = Field(..., description="终点节点ID")
    edge_namespace: str = Field(..., description="关系大类")
    edge_type: str = Field(..., description="具体关系类型")

    # Optional common metadata
    edge_uuid: Optional[UUID] = Field(default=None)
    description: Optional[str] = Field(default=None)
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    is_test: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Engine-specific extension properties
    properties: Dict[str, Any] = Field(default_factory=dict)


class PaginatedNodes(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[GraphNode]


class PaginatedEdges(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[GraphEdge]


class SubgraphResult(BaseModel):
    center_node_id: str
    depth: int
    nodes: List[GraphNode]
    edges: List[GraphEdge]


class GraphStats(BaseModel):
    total_nodes: int
    total_edges: int
    node_type_distribution: Dict[str, int] = Field(default_factory=dict)
    edge_namespace_distribution: Dict[str, int] = Field(default_factory=dict)
    edge_type_distribution: Dict[str, int] = Field(default_factory=dict)
    status_distribution: Dict[str, int] = Field(default_factory=dict)
    confidence_distribution: Dict[str, int] = Field(default_factory=dict)


class EngineMetadata(BaseModel):
    """Descriptive metadata for a registered graph engine."""

    name: str = Field(..., description="引擎标识符，用于 URL 和注册表")
    label: str = Field(..., description="前端展示名称")
    description: str = Field(default="", description="简短说明")
    is_read_only: bool = Field(default=False, description="是否只读引擎（禁止节点/边写操作）")
    supports_flows: bool = Field(default=False, description="是否支持流程图视图")
    default_view: str = Field(default="industrial_graph", description="切换到该引擎时的默认主视图")


class EngineList(BaseModel):
    engines: List[EngineMetadata]
    default: str = Field(..., description="默认引擎名称")
