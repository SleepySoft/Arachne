"""
Arachne-flow data model and YAML document schemas.

This module mirrors the model described in docs/design_v4.txt:
- RESOURCE nodes (material, craft, service, right, information, qualification, other)
- ACTION nodes (transform, combine, separate, modify, deliver, assess, other)
- METHOD nodes (open domain vocabulary referenced by ACTIONs)
- input_role / output_role edges plus special 'next' and 'ref' relations
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.core import Evidence


class ResourceType(str, Enum):
    MATERIAL = "material"
    CRAFT = "craft"
    SERVICE = "service"
    RIGHT = "right"
    INFORMATION = "information"
    QUALIFICATION = "qualification"
    OTHER = "other"


class ActionType(str, Enum):
    TRANSFORM = "transform"
    COMBINE = "combine"
    SEPARATE = "separate"
    MODIFY = "modify"
    DELIVER = "deliver"
    ASSESS = "assess"
    OTHER = "other"


class InputRole(str, Enum):
    # main inputs
    FEEDSTOCK = "feedstock"
    COMPONENT = "component"
    ADDITIVE = "additive"
    # process participants
    PROCESS_MATERIAL = "process_material"
    CATALYST = "catalyst"
    ENERGY = "energy"
    CARRIER = "carrier"
    TOOL = "tool"
    PACKAGING = "packaging"
    # immaterial participants
    SUBJECT = "subject"
    BASIS = "basis"
    REQUIREMENT = "requirement"
    OTHER = "other"


class OutputRole(str, Enum):
    PRIMARY_RESULT = "primary_result"
    CO_RESULT = "co_result"
    INTERMEDIATE = "intermediate"
    BYPRODUCT = "byproduct"
    SCRAP = "scrap"
    WASTE = "waste"
    EMISSION = "emission"
    RECOVERED_RESOURCE = "recovered_resource"
    OTHER = "other"


class SpecialRole(str, Enum):
    NEXT = "next"
    REF = "ref"


# A triple predicate is either an input role, output role, or one of the two special roles.
Predicate = Union[InputRole, OutputRole, SpecialRole]


class FlowNodeRef(BaseModel):
    """Reference to a node inside a flow document."""

    node_id: str
    # kind is inferred from the surrounding triple pattern
    kind: Literal["resource", "action", "method"] = "resource"


class FlowTriple(BaseModel):
    """One edge triple parsed from a flow file."""

    source: str
    predicate: str
    target: str

    @field_validator("source", "target")
    @classmethod
    def non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("triple source/target cannot be empty")
        return v.strip()

    @field_validator("predicate")
    @classmethod
    def known_predicate(cls, v: str) -> str:
        v = v.strip()
        all_roles = (
            {r.value for r in InputRole}
            | {r.value for r in OutputRole}
            | {r.value for r in SpecialRole}
        )
        if v not in all_roles:
            raise ValueError(f"unknown predicate '{v}'")
        return v


class FlowAction(BaseModel):
    """An ACTION occurrence discovered while parsing a flow."""

    action_id: str
    action_type: ActionType = ActionType.OTHER
    flow_id: str
    method_ref: Optional[str] = None


class FlowResource(BaseModel):
    """A RESOURCE occurrence in a flow."""

    resource_id: str
    resource_type: ResourceType = ResourceType.OTHER
    local_name: Optional[str] = None


class FlowMethod(BaseModel):
    """A METHOD referenced by at least one ACTION."""

    method_id: str
    method_name: Optional[str] = None


class ParsedFlow(BaseModel):
    """Normalized result of parsing one flow document."""

    model_config = ConfigDict(populate_by_name=True)

    schema_version: str = Field(alias="schema")
    title: Optional[str] = None
    root_product: Optional[str] = None
    flow_id: str
    includes: List[str] = Field(default_factory=list)
    locals: Dict[str, str] = Field(default_factory=dict)
    resources: Dict[str, FlowResource] = Field(default_factory=dict)
    actions: Dict[str, FlowAction] = Field(default_factory=dict)
    methods: Dict[str, FlowMethod] = Field(default_factory=dict)
    triples: List[FlowTriple] = Field(default_factory=list)


class FlowDocument(BaseModel):
    """Raw YAML document schema used for validation before normalization."""

    model_config = ConfigDict(populate_by_name=True)

    schema_version: str = Field(
        default="arachne-flow/v0.1",
        alias="schema",
        pattern=r"^arachne-flow/v0\.1$",
    )
    title: Optional[str] = None
    root_product: Optional[str] = None
    include: List[str] = Field(default_factory=list)
    local: Dict[str, str] = Field(default_factory=dict)
    edges: List[List[str]] = Field(default_factory=list)

    @field_validator("edges")
    @classmethod
    def validate_triples(cls, v: List[List[str]]) -> List[List[str]]:
        if not v:
            return v
        for idx, triple in enumerate(v):
            if not isinstance(triple, (list, tuple)) or len(triple) != 3:
                raise ValueError(f"edge {idx}: must be a 3-element list")
            source, predicate, target = triple
            if not source or not target:
                raise ValueError(f"edge {idx}: source/target cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_document(self) -> "FlowDocument":
        if self.schema_version != "arachne-flow/v0.1":
            raise ValueError(f"unsupported schema '{self.schema_version}'")
        return self


# ---------------------------------------------------------------------------
# Engine output schemas (returned via the GraphEngine interface)
# ---------------------------------------------------------------------------

class ArachneFlowNodeProperties(BaseModel):
    """Common properties stored on arachne-flow nodes in Neo4j."""

    node_id: str
    flow_id: str
    node_kind: Literal["resource", "action", "method"]
    resource_type: Optional[str] = None
    action_type: Optional[str] = None
    local_name: Optional[str] = None
    method_name: Optional[str] = None


class ArachneFlowEdgeProperties(BaseModel):
    """Common properties stored on :ARACHNE_FLOW edges."""

    edge_id: str
    flow_id: str
    edge_namespace: Literal["arachne_flow"] = "arachne_flow"
    edge_type: str
