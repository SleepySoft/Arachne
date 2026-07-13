"""
Deterministic propagation profiles for impact propagation.

V0.2 uses runtime edge-weight tables rather than persisting reasoning
attributes on IndustrialFlowEdge, avoiding a schema migration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


@dataclass
class PropagationProfile:
    name: str
    description: str
    direction: Literal["forward", "backward", "both"]
    allowed_edge_namespaces: List[str]
    allowed_edge_types: List[str]
    edge_weights: Dict[str, float]
    decay_method: Literal["depth_decay", "none"]
    decay_factor: float
    initial_node_score: float


# V0.2 default weights by industrial-flow edge type.
# These values are structural heuristics, not predictions.
DEFAULT_EDGE_WEIGHTS: Dict[str, float] = {
    "material_input": 1.0,
    "supply_relation": 0.95,
    "process_output": 0.8,
    "energy_input": 0.75,
    "structural_composition": 0.6,
    "equipment_enablement": 0.5,
    "capability_enablement": 0.4,
    "service_provision": 0.35,
    "information_input": 0.3,
    "unknown": 0.2,
}


PROPAGATION_PROFILES: Dict[str, PropagationProfile] = {
    "supply_forward": PropagationProfile(
        name="supply_forward",
        description="沿供应链/物料输入正向传播（原材料 → 工艺 → 产品）",
        direction="forward",
        allowed_edge_namespaces=["industrial_flow"],
        allowed_edge_types=[
            "material_input",
            "supply_relation",
            "process_output",
            "energy_input",
            "structural_composition",
        ],
        edge_weights=DEFAULT_EDGE_WEIGHTS,
        decay_method="depth_decay",
        decay_factor=0.75,
        initial_node_score=1.0,
    ),
    "supply_backward": PropagationProfile(
        name="supply_backward",
        description="沿供应链反向传播（产品/下游需求 → 上游输入）",
        direction="backward",
        allowed_edge_namespaces=["industrial_flow"],
        allowed_edge_types=[
            "material_input",
            "supply_relation",
            "process_output",
            "energy_input",
            "structural_composition",
        ],
        edge_weights=DEFAULT_EDGE_WEIGHTS,
        decay_method="depth_decay",
        decay_factor=0.75,
        initial_node_score=1.0,
    ),
    "demand_forward": PropagationProfile(
        name="demand_forward",
        description="沿需求/服务关系正向传播（下游需求 → 上游能力）",
        direction="forward",
        allowed_edge_namespaces=["industrial_flow"],
        allowed_edge_types=[
            "service_provision",
            "capability_enablement",
            "information_input",
            "supply_relation",
        ],
        edge_weights={
            "service_provision": 0.9,
            "capability_enablement": 0.85,
            "information_input": 0.6,
            "supply_relation": 0.7,
        },
        decay_method="depth_decay",
        decay_factor=0.8,
        initial_node_score=1.0,
    ),
    "technology_diffusion": PropagationProfile(
        name="technology_diffusion",
        description="沿能力/信息/设备使能关系传播技术影响",
        direction="both",
        allowed_edge_namespaces=["industrial_flow", "ontology"],
        allowed_edge_types=[
            "capability_enablement",
            "equipment_enablement",
            "information_input",
            "service_provision",
            "is_a",
            "part_of",
        ],
        edge_weights={
            "capability_enablement": 0.85,
            "equipment_enablement": 0.7,
            "information_input": 0.65,
            "service_provision": 0.5,
            "is_a": 0.4,
            "part_of": 0.35,
        },
        decay_method="depth_decay",
        decay_factor=0.85,
        initial_node_score=1.0,
    ),
}


def get_propagation_profile(name: Optional[str]) -> PropagationProfile:
    if not name:
        return PROPAGATION_PROFILES["supply_forward"]
    if name not in PROPAGATION_PROFILES:
        raise ValueError(f"Unknown propagation profile: {name}")
    return PROPAGATION_PROFILES[name]
