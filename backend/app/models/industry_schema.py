"""
PRINCIPLE:
    行业：配置出来的节点过滤器
    即：行业 = 人定义的产业节点集合

Industry
   |
   | IndustryNodeMapping
   v
IndustrialNode

行业图怎么生成

1. 查 IndustryNodeMapping 得到 node_ids
2. 到 Neo4j 查这些 node_ids 之间的 industrial_flow 边
3. 返回行业子图

"""



from __future__ import annotations

from enum import Enum
from uuid import UUID, uuid4
from typing import List, Optional, Literal
from datetime import datetime, date

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.schemas import Evidence, Confidence, RecordStatus


class IndustryType(str, Enum):
    # 正式行业，例如申万行业、中信行业、证监会行业
    FORMAL_INDUSTRY = "formal_industry"

    # 研究员维护的产业链视图，例如机器人、智能驾驶、数据中心
    CURATED_VIEW = "curated_view"

    # 市场主题或投资题材，例如低空经济、AI算力
    THEME_VIEW = "theme_view"


class Industry(BaseModel):
    industry_uuid: UUID = Field(default_factory=uuid4)

    industry_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="稳定英文小写蛇形命名，例如 intelligent_driving"
    )

    name_zh: str = Field(
        ...,
        description="行业、产业链或主题视图中文名"
    )

    name_en: Optional[str] = None

    aliases: List[str] = Field(
        default_factory=list,
        description="行业别名"
    )

    industry_type: IndustryType = Field(
        default=IndustryType.CURATED_VIEW
    )

    description: Optional[str] = None

    status: RecordStatus = Field(
        default=RecordStatus.ACTIVE
    )

    notes: Optional[str] = None
    is_test: bool = Field(default=False, description="标记是否为测试数据")

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("name_zh")
    @classmethod
    def name_zh_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name_zh cannot be empty")
        return v


class IndustryNodeMapping(BaseModel):
    mapping_uuid: UUID = Field(default_factory=uuid4)

    mapping_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="例如 intelligent_driving_contains_lidar_system"
    )

    industry_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$"
    )

    node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="对应 IndustrialNode.node_id"
    )

    role: Optional[str] = Field(
        default=None,
        description="该节点在行业视图中的角色，例如 核心产品、上游部件、基础能力、下游应用"
    )

    weight: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="该节点在行业视图中的重要性，第一版可默认 1.0"
    )

    confidence: Confidence = Field(
        default=Confidence.MEDIUM
    )

    evidence: List[Evidence] = Field(
        default_factory=list
    )

    status: RecordStatus = Field(
        default=RecordStatus.ACTIVE
    )

    notes: Optional[str] = None
    is_test: bool = Field(default=False, description="标记是否为测试数据")

    @model_validator(mode="after")
    def validate_mapping_policy(self) -> "IndustryNodeMapping":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence mapping must have evidence")
        return self
