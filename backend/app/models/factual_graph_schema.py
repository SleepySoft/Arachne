"""
================================================================================
 DOMAIN: FACTUAL GRAPH (事实关系图)
================================================================================

独立于产业图的事实知识图谱，存储从年报、天眼查、工商登记、招股书等
渠道采集的实体和关系。

节点：
  :Person    — 独立的人（不依附于公司）
  :Company   — 公司（轻量引用，详细属性在 PostgreSQL companies 表）

关系（三类）：
  人 → 公司   (股东/高管/法定代表人/实际控制人/监事/董事...)
  人 → 人     (亲属/配偶/合伙人/同事/信托...)
  公司 → 公司 (供应商/客户/投资方/竞争对手/担保...)

原则：
  - 所有关系必须有 evidence 和 source
  - 关系有时效性（start_date / end_date / is_history）
  - 浏览事实关系图时，永远不出现 :IndustrialNode
================================================================================
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Annotated, List, Literal, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.schemas import Evidence, Confidence, RecordStatus


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PersonCompanyRelationType(str, Enum):
    SHAREHOLDER = "shareholder"
    EXECUTIVE = "executive"
    LEGAL_REPRESENTATIVE = "legal_representative"
    ACTUAL_CONTROLLER = "actual_controller"
    SUPERVISOR = "supervisor"
    DIRECTOR = "director"
    BOARD_CHAIR = "board_chair"
    GENERAL_MANAGER = "general_manager"
    HISTORY_ROLE = "history_role"


class PersonPersonRelationType(str, Enum):
    RELATIVE = "relative"
    SPOUSE = "spouse"
    PARENT_CHILD = "parent_child"
    SIBLING = "sibling"
    PARTNER = "partner"
    COLLEAGUE = "colleague"
    TRUST = "trust"
    ASSOCIATE = "associate"


class CompanyCompanyRelationType(str, Enum):
    SUPPLIER = "supplier"
    CUSTOMER = "customer"
    PARTNER = "partner"
    INVESTOR = "investor"
    INVESTEE = "investee"
    COMPETITOR = "competitor"
    CLIENT = "client"
    CONTRACTOR = "contractor"
    GUARANTOR = "guarantor"
    CREDITOR = "creditor"
    DEBTOR = "debtor"
    LESSEE = "lessee"
    LESSOR = "lessor"


# ---------------------------------------------------------------------------
# Person Node
# ---------------------------------------------------------------------------

class Person(BaseModel):
    """事实关系图中的独立人节点。"""

    person_uuid: UUID = Field(default_factory=uuid4)

    person_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="稳定英文小写蛇形命名，例如 person_zhang_san",
    )

    name_zh: str = Field(..., description="中文姓名")
    name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list, description="别名、曾用名")
    gender: Optional[str] = Field(default=None, description="male / female / other")
    birth_year: Optional[int] = None
    nationality: Optional[str] = None
    id_card_hash: Optional[str] = Field(
        default=None,
        description="脱敏身份标识哈希，用于跨源同一人去重",
    )
    profile: Optional[str] = Field(default=None, description="人物简介")
    status: RecordStatus = Field(default=RecordStatus.ACTIVE)
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


class PersonCreate(BaseModel):
    """创建 Person 的输入模型。"""

    person_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$", min_length=3, max_length=64)
    name_zh: str
    name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    gender: Optional[str] = None
    birth_year: Optional[int] = None
    nationality: Optional[str] = None
    id_card_hash: Optional[str] = None
    profile: Optional[str] = None
    status: RecordStatus = Field(default=RecordStatus.PENDING)
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")

    @field_validator("name_zh")
    @classmethod
    def name_zh_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name_zh cannot be empty")
        return v


class PersonUpdate(BaseModel):
    """更新 Person 的输入模型。"""

    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    aliases: Optional[List[str]] = None
    gender: Optional[str] = None
    birth_year: Optional[int] = None
    nationality: Optional[str] = None
    id_card_hash: Optional[str] = None
    profile: Optional[str] = None
    status: Optional[RecordStatus] = None
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")


# ---------------------------------------------------------------------------
# Factual Relations
# ---------------------------------------------------------------------------

class FactualRelationBase(BaseModel):
    """所有事实关系的公共字段。"""

    relation_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=128,
        description="稳定英文小写蛇形命名",
    )

    evidence: List[Evidence] = Field(default_factory=list)
    source: str = Field(
        ...,
        description="数据来源：天眼查、年报、招股说明书、工商登记、公告等",
    )
    confidence: Confidence = Field(default=Confidence.LOW)
    status: RecordStatus = Field(default=RecordStatus.PENDING)

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_history: bool = False

    notes: Optional[str] = None
    is_test: bool = Field(default=False, description="标记是否为测试数据")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("source")
    @classmethod
    def source_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("source cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_evidence_policy(self) -> "FactualRelationBase":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence relation must have evidence")
        if self.status == RecordStatus.ACTIVE and not self.evidence:
            raise ValueError("ACTIVE relation must have evidence")
        return self


class PersonCompanyRelation(FactualRelationBase):
    """人 → 公司 关系。"""

    relation_domain: Literal["person_company"] = "person_company"
    person_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    company_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    relation_type: PersonCompanyRelationType
    subtype: Optional[str] = Field(default=None, description="细分角色，如'董事长'、'技术总监'")
    equity_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="持股比例（仅股东）")
    amount_cny: Optional[float] = Field(default=None, description="出资金额")

    @model_validator(mode="after")
    def validate_person_company(self) -> "PersonCompanyRelation":
        if self.relation_type == PersonCompanyRelationType.SHAREHOLDER and self.equity_ratio is None:
            # 低置信度时允许无持股比例，但最好有
            pass
        return self


class PersonPersonRelation(FactualRelationBase):
    """人 → 人 关系。"""

    relation_domain: Literal["person_person"] = "person_person"
    from_person_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    to_person_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    relation_type: PersonPersonRelationType
    subtype: Optional[str] = Field(default=None, description="如'兄弟'、'堂兄弟'")


class CompanyCompanyRelation(FactualRelationBase):
    """公司 → 公司 关系（事实业务关系）。"""

    relation_domain: Literal["company_company"] = "company_company"
    from_company_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    to_company_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    relation_type: CompanyCompanyRelationType
    amount_cny: Optional[float] = Field(default=None, description="交易金额/投资金额/担保金额")
    contract_no: Optional[str] = Field(default=None, description="合同编号")
    proportion: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="占比（如采购占比）")


FactualRelation = Annotated[
    Union[PersonCompanyRelation, PersonPersonRelation, CompanyCompanyRelation],
    Field(discriminator="relation_domain"),
]


# ---------------------------------------------------------------------------
# Response wrappers
# ---------------------------------------------------------------------------

class PaginatedPersons(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[Person]


class PaginatedRelations(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[FactualRelation]
