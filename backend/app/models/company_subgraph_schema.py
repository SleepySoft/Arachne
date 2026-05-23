"""
================================================================================
 DOMAIN: COMPANY SUBGRAPH (公司子图)
================================================================================
注意：以下所有模型定义的是"公司子图"域，与核心产业图域（IndustrialNode,
GraphEdge 等）严格隔离。

CompanySubgraphNode 是对 IndustrialNode 的**引用视图**，不是节点本身。
CompanySubgraphEdge 是对 GraphEdge 的**投影视图**，不是边本身。
CompanySubgraphRelation 是子图域内**推导/录入**的关系，只存在于子图上下文。

严禁将这些模型与核心产业图模型混用或互相继承。
================================================================================
"""

from __future__ import annotations

from enum import Enum
from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.schemas import Evidence, Confidence, RecordStatus


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SubgraphRelationType(str, Enum):
    INFERRED_INDUSTRIAL = "inferred_industrial"
    EVIDENCED_BUSINESS = "evidenced_business"
    SIMILARITY_PEER = "similarity_peer"
    PERSON_RELATION = "person_relation"      # ← 预留：人的关系


class SubgraphRelationSubtype(str, Enum):
    UPSTREAM_OF = "upstream_of"
    DOWNSTREAM_OF = "downstream_of"
    SUPPLIER = "supplier"
    CUSTOMER = "customer"
    PARTNER = "partner"
    PEER = "peer"
    SHAREHOLDER = "shareholder"              # ← 预留
    EXECUTIVE = "executive"                  # ← 预留


# ---------------------------------------------------------------------------
# Subgraph Node (投影视图)
# ---------------------------------------------------------------------------

class CompanySubgraphNode(BaseModel):
    """
    公司子图中的节点。
    这不是 IndustrialNode，而是"某公司在子图上下文中暴露的产业节点"的视图。
    """
    node_id: str = Field(..., description="引用 IndustrialNode.node_id")
    canonical_name_zh: str = Field(default="")
    entity_type: str = Field(default="unknown")
    activity_type: str = Field(default="unknown")
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    role: Optional[str] = None
    exposure_confidence: Optional[str] = None


# ---------------------------------------------------------------------------
# Subgraph Edge (产业流投影)
# ---------------------------------------------------------------------------

class CompanySubgraphEdge(BaseModel):
    """
    公司子图中的边。
    这不是 GraphEdge，而是"主图中两个被暴露节点之间的产业流边"的投影。
    """
    edge_id: str = Field(...)
    from_node: str = Field(...)
    to_node: str = Field(...)
    edge_namespace: str = Field(default="industrial_flow")
    edge_type: str = Field(default="material_flow")
    edge_type_label: Optional[str] = None
    description: Optional[str] = None
    confidence: Optional[str] = None


# ---------------------------------------------------------------------------
# Subgraph Relation (域内推导关系)
# ---------------------------------------------------------------------------

class CompanySubgraphRelation(BaseModel):
    """
    公司子图域内的推导关系。
    只存在于子图快照中，不属于核心产业图。
    """
    relation_id: Optional[int] = None
    from_company_id: str = Field(...)
    to_company_id: str = Field(...)
    relation_type: SubgraphRelationType = Field(default=SubgraphRelationType.SIMILARITY_PEER)
    relation_subtype: Optional[SubgraphRelationSubtype] = None
    strength: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence: Confidence = Field(default=Confidence.LOW)
    evidence: List[Evidence] = Field(default_factory=list)
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Subgraph Version (子图快照)
# ---------------------------------------------------------------------------

class CompanySubgraph(BaseModel):
    """
    公司子图快照版本。
    每次计算生成一个独立版本，旧版本保留。
    """
    subgraph_uuid: UUID = Field(default_factory=uuid4)
    subgraph_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    company_id: str = Field(...)
    version_name: Optional[str] = None
    description: Optional[str] = None
    status: RecordStatus = Field(default=RecordStatus.ACTIVE)
    nodes_summary: Optional[dict] = None
    edges_summary: Optional[dict] = None
    relations_summary: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # 展开时填充（不参与数据库存储）
    nodes: List[CompanySubgraphNode] = Field(default_factory=list)
    edges: List[CompanySubgraphEdge] = Field(default_factory=list)
    relations: List[CompanySubgraphRelation] = Field(default_factory=list)


class PaginatedCompanySubgraphs(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[CompanySubgraph]
