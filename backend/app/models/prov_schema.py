"""
PROV statement schema.

A PROV statement is a type-level provenance assertion attached to an entity node.
It is stored in PostgreSQL and projected onto the industrial graph on demand.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.schemas import Evidence, Confidence, RecordStatus


class ProvRole(str, Enum):
    ENTITY = "entity"
    ACTIVITY = "activity"
    AGENT = "agent"


class ProvRelation(str, Enum):
    USED = "used"
    WAS_GENERATED_BY = "wasGeneratedBy"
    WAS_DERIVED_FROM = "wasDerivedFrom"
    WAS_ATTRIBUTED_TO = "wasAttributedTo"
    WAS_ASSOCIATED_WITH = "wasAssociatedWith"
    ACTED_ON_BEHALF_OF = "actedOnBehalfOf"


class ProvStatement(BaseModel):
    statement_uuid: UUID = Field(default_factory=uuid4)

    statement_id: Optional[str] = Field(
        default=None,
        max_length=256,
        description="自动生成的语句 ID，格式为 node_id__relation__target_node_id",
    )

    node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="被描述的节点（entity/activity）的 node_id",
    )

    node_role: ProvRole = Field(
        default=ProvRole.ENTITY,
        description="node_id 在 PROV 中的角色",
    )

    prov_relation: ProvRelation = Field(
        ...,
        description="PROV 关系类型",
    )

    target_node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="指向节点的 node_id",
    )

    target_role: ProvRole = Field(
        default=ProvRole.ENTITY,
        description="target_node_id 在 PROV 中的角色",
    )

    is_inferred: bool = Field(
        default=False,
        description="是否由产业图自动推导而来",
    )

    evidence: List[Evidence] = Field(default_factory=list)

    confidence: Confidence = Field(default=Confidence.MEDIUM)

    status: RecordStatus = Field(default=RecordStatus.ACTIVE)

    notes: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("node_id", "target_node_id")
    @classmethod
    def id_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("node_id cannot be empty")
        return v

    @model_validator(mode="after")
    def generate_statement_id(self) -> "ProvStatement":
        if self.statement_id is None or not self.statement_id.strip():
            self.statement_id = f"{self.node_id}__{self.prov_relation.value}__{self.target_node_id}"
        return self

    @model_validator(mode="after")
    def validate_high_confidence_evidence(self) -> "ProvStatement":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence statement must have evidence")
        return self
