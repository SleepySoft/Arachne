"""

PRINCIPLE:
    公司：不是配置节点集合，而是计算节点集合
    即：公司 = 数据驱动计算出的产业节点集合
    公司通过数据计算得到一个带权产业实体集合；这个集合在底层产业图上形成一个临时子图；多个公司的临时子图之间再通过产业流关系投影出公司关系。

公司不是简单选择一组产业节点，而是要根据：
    主营业务
    产品描述
    年报
    招股书
    公告
    官网
    新闻
    客户案例
    收入构成
    专利
    招聘
    供应链信息
去动态判断：
    这家公司实际参与了哪些 IndustrialEntity？
    以什么 Activity 参与？
    参与强度是多少？
    证据是什么？
    时间有效性如何？


公司的关系：
    inferred_industrial_relation - 由产业图推导出来的上下游关系。
        ```
        公司A produce 激光器
        公司B produce 激光雷达
        激光器 → 激光雷达
        因此：
        公司A inferred_upstream_of 公司B
        ```
    evidenced_business_relation - 有证据证明的真实业务关系。
        ```
        公司A 是 公司B 的供应商
        公司B 是 公司C 的客户
        ```
    similarity_or_peer_relation - 由于公司参与相似产业节点而产生的同业/相似关系。
        ```
        公司A produce 激光雷达
        公司B produce 激光雷达
        因此：
        公司A peer_of 公司B
        ```



Company
   |
   | CompanyNodeExposure
   v
IndustrialNode


公司临时图怎么生成

1. 查 CompanyNodeExposure 得到公司 node_ids
2. 到 Neo4j 查这些 node_ids 之间的 industrial_flow 边
3. 返回公司临时子图


公司之间关系怎么生成

1. 公司A有 node_a
2. 公司B有 node_b
3. Neo4j 中存在 node_a -> node_b
4. 则推导 公司A -> 公司B

"""

from __future__ import annotations

from enum import Enum
from uuid import UUID
from typing import List, Optional, Literal
from datetime import datetime, date

from pydantic import BaseModel, Field, field_validator, model_validator

from core_schema import Evidence, Confidence, RecordStatus
from industry_schema import Industry, IndustryNodeMapping


class CompanyActivityType(str, Enum):
    # 研发
    RND = "rnd"

    # 设计
    DESIGN = "design"

    # 制造
    MANUFACTURE = "manufacture"

    # 生产 / 销售产品
    PRODUCE = "produce"

    # 集成
    INTEGRATE = "integrate"

    # 运营
    OPERATE = "operate"

    # 提供服务
    PROVIDE_SERVICE = "provide_service"

    # 采购 / 使用上游输入
    PROCURE = "procure"

    # 使用某产业实体作为内部能力或生产资料
    USE = "use"

    # 暂时无法判断
    UNKNOWN = "unknown"


class Company(BaseModel):
    company_uuid: UUID

    company_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="稳定英文小写蛇形命名，例如 hesai_technology"
    )

    name_zh: str = Field(
        ...,
        description="公司中文名"
    )

    name_en: Optional[str] = None

    aliases: List[str] = Field(
        default_factory=list
    )

    stock_codes: List[str] = Field(
        default_factory=list,
        description="股票代码，可空"
    )

    description: Optional[str] = None

    status: RecordStatus = Field(
        default=RecordStatus.ACTIVE
    )

    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("name_zh")
    @classmethod
    def name_zh_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name_zh cannot be empty")
        return v


class CompanyNodeExposure(BaseModel):
    exposure_uuid: UUID

    exposure_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="例如 hesai_technology_produce_lidar_system"
    )

    company_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$"
    )

    node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="对应 IndustrialNode.node_id"
    )

    activity_type: CompanyActivityType = Field(
        default=CompanyActivityType.UNKNOWN
    )

    role: Optional[str] = Field(
        default=None,
        description="自然语言说明公司在该节点上的角色，例如 激光雷达整机厂商、核心零部件供应商"
    )

    weight: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="该公司对该产业节点的业务暴露强度，第一版可默认 1.0"
    )

    confidence: Confidence = Field(
        default=Confidence.LOW
    )

    evidence: List[Evidence] = Field(
        default_factory=list
    )

    status: RecordStatus = Field(
        default=RecordStatus.PENDING
    )

    as_of_date: Optional[date] = Field(
        default=None,
        description="该判断对应的观察日期"
    )

    notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_exposure_policy(self) -> "CompanyNodeExposure":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence exposure must have evidence")

        if self.status == RecordStatus.ACTIVE and not self.evidence:
            raise ValueError("ACTIVE exposure must have evidence")

        return self


class BusinessRegistrationBatch(BaseModel):
    batch_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$"
    )

    task_description: str

    industries_to_upsert: List[Industry] = Field(default_factory=list)

    industry_node_mappings_to_upsert: List[IndustryNodeMapping] = Field(default_factory=list)

    companies_to_upsert: List[Company] = Field(default_factory=list)

    company_node_exposures_to_upsert: List[CompanyNodeExposure] = Field(default_factory=list)

    @field_validator("task_description")
    @classmethod
    def task_description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("task_description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_no_duplicate_ids(self) -> "BusinessRegistrationBatch":
        industry_ids = [x.industry_id for x in self.industries_to_upsert]
        company_ids = [x.company_id for x in self.companies_to_upsert]
        mapping_ids = [x.mapping_id for x in self.industry_node_mappings_to_upsert]
        exposure_ids = [x.exposure_id for x in self.company_node_exposures_to_upsert]

        if len(industry_ids) != len(set(industry_ids)):
            raise ValueError("duplicate industry_id found")

        if len(company_ids) != len(set(company_ids)):
            raise ValueError("duplicate company_id found")

        if len(mapping_ids) != len(set(mapping_ids)):
            raise ValueError("duplicate mapping_id found")

        if len(exposure_ids) != len(set(exposure_ids)):
            raise ValueError("duplicate exposure_id found")

        return self
