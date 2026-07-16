"""
PROV statement schema.

A PROV statement is a parsed relation from a PROV-N document. It is intentionally
loosely coupled to the industrial graph: `node_id` and `target_node_id` hold the
PROV identifiers exactly as they appear in the PROV-N file. If an identifier
happens to match an existing `IndustrialNode.node_id`, the frontend or other
consumers may create a link; otherwise the statement is still valid provenance
metadata.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.core import Confidence, Evidence, RecordStatus


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
        max_length=512,
        description="语句唯一标识，默认使用 statement_uuid 的字符串",
    )

    node_id: str = Field(
        ...,
        max_length=256,
        description="PROV 关系主体标识符（尽量复用图谱 node_id，但不强制）",
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
        max_length=256,
        description="PROV 关系客体标识符（尽量复用图谱 node_id，但不强制）",
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
            raise ValueError("identifier cannot be empty")
        return v.strip()

    @model_validator(mode="after")
    def generate_statement_id(self) -> "ProvStatement":
        if self.statement_id is None or not self.statement_id.strip():
            self.statement_id = str(self.statement_uuid)
        return self

    @model_validator(mode="after")
    def validate_high_confidence_evidence(self) -> "ProvStatement":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence statement must have evidence")
        return self
