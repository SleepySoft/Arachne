"""
PRINCIPLE:

"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Union, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, computed_field, field_validator, model_validator


# ============================================================
# Enums
# ============================================================

class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class NodeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


# Alias for backward compatibility with industry/company schemas
RecordStatus = NodeStatus


class EntityType(str, Enum):
    MATERIAL = "material"
    COMPONENT = "component"
    DEVICE = "device"
    MODULE = "module"
    SUBSYSTEM = "subsystem"
    SYSTEM = "system"
    PLATFORM = "platform"
    INFRASTRUCTURE = "infrastructure"
    APPLICATION_SYSTEM = "application_system"
    SERVICE = "service"
    TECHNOLOGY_CAPABILITY = "technology_capability"
    UNKNOWN = "unknown"


class IndustrialFlowType(str, Enum):
    MATERIAL_FLOW = "material_flow"
    COMPOSITION = "composition"
    ENERGY_FLOW = "energy_flow"
    INFORMATION_FLOW = "information_flow"
    CAPABILITY_SUPPLY = "capability_supply"
    SERVICE_FLOW = "service_flow"


# ============================================================
# Edge Type Labels (shared mapping)
# ============================================================

EDGE_TYPE_LABELS: dict[str, str] = {
    # IndustrialFlowType
    "material_flow": "物料流",
    "composition": "组成/构成",
    "energy_flow": "能量流",
    "information_flow": "信息流",
    "capability_supply": "能力供给",
    "service_flow": "服务流",
    # OntologyType
    "alias_of": "别名/同义",
    "is_a": "是一种",
    "variant_of": "变体",
    "related_term": "相关术语",
}


class OntologyType(str, Enum):
    ALIAS_OF = "alias_of"
    IS_A = "is_a"
    VARIANT_OF = "variant_of"
    RELATED_TERM = "related_term"


class ReviewAction(str, Enum):
    CREATE_PENDING_NODE = "create_pending_node"
    MERGE_TO_EXISTING = "merge_to_existing"
    REJECT_AS_MARKET_CONCEPT = "reject_as_market_concept"
    REJECT_AS_COMPANY = "reject_as_company"
    REJECT_AS_APPLICATION_LABEL = "reject_as_application_label"
    NEED_MORE_EVIDENCE = "need_more_evidence"
    REVIEW_MANUALLY = "review_manually"


# ============================================================
# Evidence
# ============================================================

class Evidence(BaseModel):
    source_title: str = Field(
        ...,
        description="资料标题，例如网页标题、报告标题、公告标题"
    )
    source_url: Optional[HttpUrl] = Field(
        default=None,
        description="资料URL。若无URL，可为空"
    )
    quote: str = Field(
        ...,
        description="支持该节点或关系的原文摘录"
    )

    @field_validator("source_title", "quote")
    @classmethod
    def non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v


# ============================================================
# Node
# ============================================================

class IndustrialNode(BaseModel):
    node_uuid: UUID = Field(default_factory=uuid4)

    node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="稳定英文小写蛇形命名，例如 lidar_system"
    )
    canonical_name_zh: str = Field(
        ...,
        description="中文标准名"
    )
    canonical_name_en: Optional[str] = Field(
        default=None,
        description="英文标准名；未知可为空"
    )
    aliases: List[str] = Field(
        default_factory=list,
        description="别名、简称、英文缩写、旧称等"
    )
    definition: str = Field(
        ...,
        description="实体定义，必须说明该实体是什么"
    )
    entity_type: EntityType = Field(
        ...,
        description="实体粗分类"
    )
    evidence: List[Evidence] = Field(
        default_factory=list,
        description="节点登记证据"
    )
    confidence: Confidence = Field(
        default=Confidence.LOW
    )
    status: NodeStatus = Field(
        default=NodeStatus.PENDING
    )
    notes: Optional[str] = None

    # DB timestamps (not required for input, populated by storage)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("canonical_name_zh", "definition")
    @classmethod
    def non_empty_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_evidence_policy(self) -> "IndustrialNode":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence node must have evidence")

        if self.status == NodeStatus.ACTIVE and not self.evidence:
            raise ValueError("ACTIVE node must have evidence")

        return self


class IndustrialNodeCreate(BaseModel):
    """用于创建节点的输入模型（不含自动生成的字段）"""
    node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
    )
    canonical_name_zh: str
    canonical_name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    definition: str
    entity_type: EntityType
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.PENDING
    notes: Optional[str] = None

    @field_validator("canonical_name_zh", "definition")
    @classmethod
    def non_empty_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_evidence_policy(self) -> "IndustrialNodeCreate":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence node must have evidence")
        if self.status == NodeStatus.ACTIVE and not self.evidence:
            raise ValueError("ACTIVE node must have evidence")
        return self


class IndustrialNodeUpdate(BaseModel):
    """用于更新节点的输入模型"""
    canonical_name_zh: Optional[str] = None
    canonical_name_en: Optional[str] = None
    aliases: Optional[List[str]] = None
    definition: Optional[str] = None
    entity_type: Optional[EntityType] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    status: Optional[NodeStatus] = None
    notes: Optional[str] = None


class IndustrialNodeQuickCreate(BaseModel):
    """用于快速创建草稿节点的输入模型。只需要中文名或英文名之一，其余字段由系统填充默认值。"""
    node_id: Optional[str] = Field(
        default=None,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="可选；不提供时系统自动生成 draft_{uuid} 占位 ID，后续由 AI 或管理员替换为规范 snake_case ID",
    )
    canonical_name_zh: Optional[str] = Field(
        default=None,
        description="中文标准名；与 canonical_name_en 至少填一个",
    )
    canonical_name_en: Optional[str] = Field(
        default=None,
        description="英文标准名；与 canonical_name_zh 至少填一个",
    )
    aliases: List[str] = Field(default_factory=list)
    definition: Optional[str] = Field(
        default=None,
        description="实体定义；留空表示待补充",
    )
    entity_type: Optional[EntityType] = Field(
        default=EntityType.UNKNOWN,
        description="实体粗分类；留空默认为 unknown",
    )
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.PENDING
    notes: Optional[str] = Field(
        default=None,
        description="可记录'由人工快速添加，待 AI 补全'等备注",
    )

    @model_validator(mode="after")
    def validate_name_present(self) -> "IndustrialNodeQuickCreate":
        if not (self.canonical_name_zh and self.canonical_name_zh.strip()) and \
           not (self.canonical_name_en and self.canonical_name_en.strip()):
            raise ValueError("canonical_name_zh 和 canonical_name_en 至少填写一个")
        return self


# ============================================================
# Edge Base
# ============================================================

class BaseEdge(BaseModel):
    edge_uuid: UUID = Field(default_factory=uuid4)

    edge_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="稳定英文小写蛇形命名"
    )
    from_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="起点节点ID"
    )
    to_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="终点节点ID"
    )
    description: str = Field(
        ...,
        description="必须说明 from_node 对 to_node 的作用"
    )
    evidence: List[Evidence] = Field(
        default_factory=list
    )
    confidence: Confidence = Field(
        default=Confidence.LOW
    )
    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("description")
    @classmethod
    def description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_common_edge_policy(self) -> "BaseEdge":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")

        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")

        return self


# ============================================================
# Industrial Flow Edge
# ============================================================

class IndustrialFlowEdge(BaseEdge):
    edge_namespace: Literal["industrial_flow"] = "industrial_flow"
    edge_type: IndustrialFlowType

    @computed_field
    @property
    def edge_type_label(self) -> str:
        return EDGE_TYPE_LABELS.get(self.edge_type.value, self.edge_type.value)

    @model_validator(mode="after")
    def validate_industrial_flow_policy(self) -> "IndustrialFlowEdge":
        if not self.description.strip():
            raise ValueError("industrial_flow edge must have description")
        return self


class IndustrialFlowEdgeCreate(BaseModel):
    edge_namespace: Literal["industrial_flow"] = "industrial_flow"
    edge_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    from_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    to_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    edge_type: IndustrialFlowType
    description: str
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None

    @field_validator("description")
    @classmethod
    def description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_policy(self) -> "IndustrialFlowEdgeCreate":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")
        return self


class IndustrialFlowEdgeQuickCreate(BaseModel):
    """用于快速创建产业流关系的输入模型。只需提供起点和终点节点，其余字段由系统填充默认值。"""
    edge_id: Optional[str] = Field(
        default=None,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="可选；不提供时自动生成 {from_node}_to_{to_node} 或 draft_{uuid} 占位 ID",
    )
    from_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="上游节点 ID，为下游节点提供输入",
    )
    to_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="下游节点 ID，接收上游节点的输入",
    )
    edge_type: IndustrialFlowType = Field(
        default=IndustrialFlowType.MATERIAL_FLOW,
        description="关系类型；留空默认 material_flow",
    )
    description: Optional[str] = Field(
        default=None,
        description="关系描述；留空自动生成",
    )
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = Field(
        default=None,
        description="备注",
    )

    @model_validator(mode="after")
    def validate_policy(self) -> "IndustrialFlowEdgeQuickCreate":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")
        return self


class IndustrialFlowEdgeUpdate(BaseModel):
    description: Optional[str] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    notes: Optional[str] = None


# ============================================================
# Ontology Edge
# ============================================================

class OntologyEdge(BaseEdge):
    edge_namespace: Literal["ontology"] = "ontology"
    edge_type: OntologyType

    @computed_field
    @property
    def edge_type_label(self) -> str:
        return EDGE_TYPE_LABELS.get(self.edge_type.value, self.edge_type.value)

    @model_validator(mode="after")
    def validate_ontology_policy(self) -> "OntologyEdge":
        if self.edge_type == OntologyType.ALIAS_OF:
            text = self.description.lower()
            if (
                "alias" not in text
                and "别名" not in self.description
                and "同义" not in self.description
                and "译名" not in self.description
            ):
                raise ValueError(
                    "alias_of description should explain alias/synonym/translation relationship"
                )
        return self


class OntologyEdgeCreate(BaseModel):
    edge_namespace: Literal["ontology"] = "ontology"
    edge_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    from_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    to_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    edge_type: OntologyType
    description: str
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None

    @field_validator("description")
    @classmethod
    def description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_policy(self) -> "OntologyEdgeCreate":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")
        return self


class OntologyEdgeUpdate(BaseModel):
    description: Optional[str] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    notes: Optional[str] = None


# 使用 discriminator，确保根据 edge_namespace 自动解析为正确 Edge 类型
GraphEdge = Annotated[
    Union[IndustrialFlowEdge, OntologyEdge],
    Field(discriminator="edge_namespace")
]

GraphEdgeCreate = Annotated[
    Union[IndustrialFlowEdgeCreate, OntologyEdgeCreate],
    Field(discriminator="edge_namespace")
]


# ============================================================
# Rejected / Pending Items
# ============================================================

class RejectedOrPendingItem(BaseModel):
    term: str = Field(
        ...,
        description="被拒绝或待确认的候选词"
    )
    reason: str = Field(
        ...,
        description="拒绝或待确认原因"
    )
    suggested_action: ReviewAction
    evidence: List[Evidence] = Field(
        default_factory=list
    )
    notes: Optional[str] = None

    @field_validator("term", "reason")
    @classmethod
    def non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v


# ============================================================
# Registration Output Batch
# ============================================================

class GraphRegistrationBatch(BaseModel):
    batch_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$"
    )
    task_description: str

    nodes_to_upsert: List[IndustrialNode] = Field(
        default_factory=list
    )
    edges_to_upsert: List[GraphEdge] = Field(
        default_factory=list
    )
    rejected_or_pending: List[RejectedOrPendingItem] = Field(
        default_factory=list
    )

    @field_validator("task_description")
    @classmethod
    def task_description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("task_description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_no_duplicate_node_ids(self) -> "GraphRegistrationBatch":
        node_ids = [node.node_id for node in self.nodes_to_upsert]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("duplicate node_id found")
        return self

    @model_validator(mode="after")
    def validate_no_duplicate_edge_ids(self) -> "GraphRegistrationBatch":
        edge_ids = [edge.edge_id for edge in self.edges_to_upsert]
        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("duplicate edge_id found")
        return self


# ============================================================
# Candidate Input Schema
# ============================================================

class CandidateEntity(BaseModel):
    term: str = Field(
        ...,
        description="候选实体名称"
    )
    context: Optional[str] = Field(
        default=None,
        description="候选词出现的上下文"
    )
    source: Optional[Evidence] = Field(
        default=None
    )

    @field_validator("term")
    @classmethod
    def term_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("term cannot be empty")
        return v


class CandidateRelation(BaseModel):
    from_term: str = Field(
        ...,
        description="候选关系的起点词，未必是最终节点ID"
    )
    to_term: str = Field(
        ...,
        description="候选关系的终点词，未必是最终节点ID"
    )
    proposed_relation: Optional[str] = Field(
        default=None,
        description="资料中暗示的关系，未必是最终登记关系"
    )
    context: Optional[str] = None
    source: Optional[Evidence] = None

    @field_validator("from_term", "to_term")
    @classmethod
    def terms_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("term cannot be empty")
        return v


class GraphRegistrationInput(BaseModel):
    task_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$"
    )
    task_description: str

    candidate_entities: List[CandidateEntity] = Field(
        default_factory=list
    )
    candidate_relations: List[CandidateRelation] = Field(
        default_factory=list
    )

    instructions: Optional[str] = Field(
        default=None,
        description="本次登记的额外说明"
    )

    @field_validator("task_description")
    @classmethod
    def task_description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("task_description cannot be empty")
        return v


# ============================================================
# Response wrappers
# ============================================================

class PaginatedNodes(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[IndustrialNode]


class PaginatedEdges(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[GraphEdge]


class GraphStats(BaseModel):
    total_nodes: int
    total_edges: int
    node_type_distribution: dict
    edge_namespace_distribution: dict
    edge_type_distribution: dict
    status_distribution: dict
    confidence_distribution: dict


class SubgraphResult(BaseModel):
    center_node_id: str
    depth: int
    nodes: List[IndustrialNode]
    edges: List[GraphEdge]


class PathResult(BaseModel):
    from_node: str
    to_node: str
    paths: List[List[dict]]
