# core_schema.py

from __future__ import annotations

import json
from enum import Enum
from uuid import UUID
from typing import Annotated, List, Optional, Union, Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


# ============================================================
# Enums
# ============================================================

class Confidence(str, Enum):
    # 高置信度：有权威来源，或多个可靠来源相互印证
    HIGH = "HIGH"

    # 中等置信度：有可靠来源支持，但来源数量、定义精度或一致性仍需后续完善
    MEDIUM = "MEDIUM"

    # 低置信度：证据不足、来源较弱、存在歧义，或仅作为临时登记
    LOW = "LOW"


class RecordStatus(str, Enum):
    # 已确认节点：可进入正式产业图
    ACTIVE = "ACTIVE"

    # 待确认节点：暂时登记，但仍需补充证据或人工复核
    PENDING = "PENDING"

    # 已拒绝节点：不应作为基础产业实体进入图中
    REJECTED = "REJECTED"

    # 已归档（删除）节点
    ARCHIVED = "ARCHIVED"


class EntityType(str, Enum):
    # 原材料：被加工、消耗或转化后进入下游实体的基础物质
    MATERIAL = "material"

    # 部件：构成更大设备、模块或系统的基础结构单元
    COMPONENT = "component"

    # 器件：具备明确功能的物理器件，通常比部件更功能化
    DEVICE = "device"

    # 模块：由多个部件或器件组成，承担相对独立功能的单元
    MODULE = "module"

    # 子系统：系统内部相对完整的功能系统，可由多个模块组成
    SUBSYSTEM = "subsystem"

    # 系统：具备完整功能的设备、产品或工程系统
    SYSTEM = "system"

    # 平台：为其他系统、应用或服务提供承载能力的基础平台
    PLATFORM = "platform"

    # 基础设施：支撑大规模运行、生产、流通或服务交付的基础设施
    INFRASTRUCTURE = "infrastructure"

    # 应用系统：面向具体场景或用户需求的应用级系统
    APPLICATION_SYSTEM = "application_system"

    # 服务：以持续服务形式提供价值的实体
    SERVICE = "service"

    # 技术能力：非具体产品，但可为其他实体提供能力基础的技术能力
    TECHNOLOGY_CAPABILITY = "technology_capability"

    # 未知类型：当前证据不足，暂时无法确定实体类型
    UNKNOWN = "unknown"


class IndustrialFlowType(str, Enum):
    # 物质流：A 是 B 的物理原料，或经加工、转化后成为 B 的一部分
    MATERIAL_FLOW = "material_flow"

    # 组成关系：A 是 B 的结构组成部分、器件、模块或子系统
    COMPOSITION = "composition"

    # 能量流：A 为 B 提供运行所需能量
    ENERGY_FLOW = "energy_flow"

    # 信息流：A 向 B 提供数据、信号、测量结果、控制信息或反馈信息
    INFORMATION_FLOW = "information_flow"

    # 能力供给：A 为 B 提供基础能力，使 B 能运行、部署、交付或发挥功能
    CAPABILITY_SUPPLY = "capability_supply"

    # 服务流：A 以服务形式持续支持 B 的运行、交付、流通或使用
    SERVICE_FLOW = "service_flow"


class OntologyType(str, Enum):
    # 别名关系：A 只是 B 的别名、缩写、英文名、中文译名或同义表达
    ALIAS_OF = "alias_of"

    # 上下位关系：A 是 B 的稳定子类
    IS_A = "is_a"

    # 变体关系：A 是 B 的技术路线、产品形态或实现方式变体
    VARIANT_OF = "variant_of"

    # 相关术语：A 与 B 语义相关，但暂时无法确定为别名、子类或变体
    RELATED_TERM = "related_term"


class ReviewAction(str, Enum):
    # 创建待确认节点：候选词可能是实体，但证据不足，先进入 PENDING 状态
    CREATE_PENDING_NODE = "create_pending_node"

    # 合并到已有实体：候选词应作为已有节点的别名、同义表达或重复项处理
    MERGE_TO_EXISTING = "merge_to_existing"

    # 拒绝为市场概念：候选词是投资题材、市场热点、政策主题或交易概念
    REJECT_AS_MARKET_CONCEPT = "reject_as_market_concept"

    # 拒绝为公司实体：候选词是公司、股票或企业主体，不属于当前产业实体图
    REJECT_AS_COMPANY = "reject_as_company"

    # 拒绝为应用标签：候选词更像用途、场景、军用/民用等应用领域标签
    REJECT_AS_APPLICATION_LABEL = "reject_as_application_label"

    # 需要更多证据：当前信息不足以决定是否创建、合并或拒绝
    NEED_MORE_EVIDENCE = "need_more_evidence"

    # 人工复核：存在复杂歧义，需要人工判断
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
    node_uuid: UUID

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
    status: RecordStatus = Field(
        default=RecordStatus.PENDING
    )
    notes: Optional[str] = None

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

        if self.status == RecordStatus.ACTIVE and not self.evidence:
            raise ValueError("ACTIVE node must have evidence")

        return self


# ============================================================
# Edge Base
# ============================================================

class BaseEdge(BaseModel):
    edge_uuid: UUID

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

    @model_validator(mode="after")
    def validate_industrial_flow_policy(self) -> "IndustrialFlowEdge":
        # 产业流关系必须保持“上游 -> 下游”
        # 这里无法自动判断方向是否语义正确，但要求 description 必须说明供给内容。
        if not self.description.strip():
            raise ValueError("industrial_flow edge must have description")

        return self


# ============================================================
# Ontology Edge
# ============================================================

class OntologyEdge(BaseEdge):
    edge_namespace: Literal["ontology"] = "ontology"
    edge_type: OntologyType

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


# 使用 discriminator，确保根据 edge_namespace 自动解析为正确 Edge 类型
GraphEdge = Annotated[
    Union[IndustrialFlowEdge, OntologyEdge],
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


# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    example_output = {
        "batch_id": "radar_registration_batch_001",
        "task_description": "登记雷达相关实体与关系",
        "nodes_to_upsert": [
            {
                "node_id": "radio_radar_system",
                "canonical_name_zh": "无线电雷达",
                "canonical_name_en": "Radio Radar System",
                "aliases": ["雷达", "Radar"],
                "definition": "利用无线电波探测目标距离、速度、方位等信息的系统。",
                "entity_type": "system",
                "evidence": [
                    {
                        "source_title": "示例资料",
                        "quote": "雷达通常利用无线电波探测目标。"
                    }
                ],
                "confidence": "MEDIUM",
                "status": "ACTIVE",
                "notes": "示例节点"
            },
            {
                "node_id": "phased_array_radar",
                "canonical_name_zh": "相控阵雷达",
                "canonical_name_en": "Phased Array Radar",
                "aliases": [],
                "definition": "通过控制阵列天线中各单元信号相位实现波束扫描的雷达系统。",
                "entity_type": "system",
                "evidence": [
                    {
                        "source_title": "示例资料",
                        "quote": "相控阵雷达通过控制阵列天线实现波束扫描。"
                    }
                ],
                "confidence": "MEDIUM",
                "status": "ACTIVE"
            }
        ],
        "edges_to_upsert": [
            {
                "edge_id": "phased_array_radar_is_a_radio_radar_system",
                "edge_namespace": "ontology",
                "edge_type": "is_a",
                "from_node": "phased_array_radar",
                "to_node": "radio_radar_system",
                "description": "相控阵雷达是无线电雷达的一种稳定子类。",
                "evidence": [
                    {
                        "source_title": "示例资料",
                        "quote": "相控阵雷达是一类雷达系统。"
                    }
                ],
                "confidence": "MEDIUM"
            }
        ],
        "rejected_or_pending": [
            {
                "term": "军用雷达",
                "reason": "该词更像应用领域或用途标签，不宜直接作为基础产业实体登记。",
                "suggested_action": "review_manually",
                "evidence": [],
                "notes": "后续可细化为火控雷达、机载预警雷达等稳定产品类别"
            }
        ]
    }

    obj = GraphRegistrationBatch.model_validate(example_output)

    print("validation ok")
    print(json.dumps(obj.model_dump(mode="json"), ensure_ascii=False, indent=2))


