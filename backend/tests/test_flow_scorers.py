"""Unit tests for arachne-flow pluggable scorers (no DB required).

Each test builds a small ``FlowScoringContext`` by hand and asserts the
graph-theoretic property the scorer is meant to capture.

Test graph (production-flow orientation, from->to = downstream):

    r1 --feedstock--> a1 --primary_result--> r2 --feedstock--> a2 --primary_result--> r3
    r4 --component--> a1                         a2 --co_result--> r5
                       a1 --ref--> m1
"""
from __future__ import annotations

from typing import Any, Dict, Set

import pytest

from app.reasoning.flow_scorers import (
    BetweennessScorer,
    DegreeScorer,
    FlowScoringContext,
    PageRankScorer,
    ReachScorer,
    select_flow_scorer,
)


def _build_ctx(direction: str = "both") -> FlowScoringContext:
    nodes: Dict[str, Dict[str, Any]] = {
        "r1": {"line": "seed", "stage": 0, "kind": "resource"},
        "a1": {"line": "main", "stage": 1, "kind": "action"},
        "r2": {"line": "main", "stage": 1, "kind": "resource"},
        "a2": {"line": "main", "stage": 2, "kind": "action"},
        "r3": {"line": "main", "stage": 2, "kind": "resource"},
        "r4": {"line": "support", "stage": 1, "kind": "resource"},
        "r5": {"line": "main", "stage": 2, "kind": "resource"},
        "m1": {"line": "method", "stage": 1, "kind": "method"},
    }
    edges: Dict[str, Dict[str, Any]] = {
        "e1": {"from": "r1", "to": "a1", "role": "feedstock", "line": "main"},
        "e2": {"from": "a1", "to": "r2", "role": "primary_result", "line": "main"},
        "e3": {"from": "r2", "to": "a2", "role": "feedstock", "line": "main"},
        "e4": {"from": "a2", "to": "r3", "role": "primary_result", "line": "main"},
        "e5": {"from": "r4", "to": "a1", "role": "component", "line": "support"},
        "e6": {"from": "a2", "to": "r5", "role": "co_result", "line": "main"},
        "e7": {"from": "a1", "to": "m1", "role": "ref", "line": "method"},
    }
    resource_actions: Dict[str, Set[str]] = {
        "r1": {"a1"},
        "r2": {"a1", "a2"},
        "r3": {"a2"},
        "r4": {"a1"},
        "r5": {"a2"},
        "m1": {"a1"},
    }
    return FlowScoringContext(
        nodes=nodes,
        edges=edges,
        seed_resources={"r1"},
        seed_actions=set(),
        direction=direction,
        name_map={},
        entity_map={},
        resource_actions=resource_actions,
        branch_links={},
    )


# ---------------------------------------------------------------------------
# DegreeScorer
# ---------------------------------------------------------------------------


def test_degree_scorer_r2_is_hub():
    ctx = _build_ctx()
    res = DegreeScorer().score(ctx)
    # r2 is touched by two main-line actions -> highest degree
    assert res["r2"].score == pytest.approx(2.0)
    assert res["r1"].score == pytest.approx(1.0)
    assert res["r3"].score == pytest.approx(1.0)
    top = max(res, key=lambda k: res[k].score)
    assert top == "r2"
    assert res["r2"].score_components["main_actions"] == 2


def test_degree_scorer_custom_weights():
    ctx = _build_ctx()
    res = DegreeScorer(main_weight=2.0, branch_weight=1.0).score(ctx)
    assert res["r2"].score == pytest.approx(4.0)  # 2 actions * weight 2


# ---------------------------------------------------------------------------
# PageRankScorer
# ---------------------------------------------------------------------------


def test_pagerank_seed_is_high_and_all_positive():
    ctx = _build_ctx(direction="both")
    res = PageRankScorer().score(ctx)
    scores = {k: v.score for k, v in res.items()}
    # all probabilities positive
    assert all(v > 0 for v in scores.values())
    # seed r1 outranks distant leaves (depth decay from the seed)
    assert scores["r1"] > scores["r3"]
    assert scores["r1"] > scores["r5"]
    # the hub a1 (degree 4) collects the most walk mass
    assert scores["a1"] == max(scores.values())
    # sum approx 1 (probability distribution)
    assert sum(scores.values()) == pytest.approx(1.0, abs=0.05)
    # normalized field present
    assert 0.0 <= res["r1"].score_components["normalized"] <= 1.0


def test_pagerank_respects_damping():
    ctx = _build_ctx(direction="both")
    high = PageRankScorer(damping=0.5).score(ctx)
    low = PageRankScorer(damping=0.95).score(ctx)
    # lower damping => more teleport => seed less dominant
    assert high["r1"].score > low["r1"].score


# ---------------------------------------------------------------------------
# BetweennessScorer
# ---------------------------------------------------------------------------


def test_betweenness_central_nodes_above_leaves():
    ctx = _build_ctx(direction="both")
    res = BetweennessScorer().score(ctx)
    # r2 and a1 sit on shortest paths between the two ends -> high betweenness
    assert res["r2"].score > 0
    assert res["a1"].score > 0
    # leaves r1/r3/r5 are endpoints, never interior -> zero betweenness
    assert res["r1"].score == 0
    assert res["r3"].score == 0
    assert res["r5"].score == 0
    assert res["r2"].score >= res["r1"].score


# ---------------------------------------------------------------------------
# ReachScorer
# ---------------------------------------------------------------------------


def test_reach_forward_blast_radius():
    ctx = _build_ctx()
    res = ReachScorer(reach_direction="forward").score(ctx)
    # r1 reaches all downstream: a1,r2,a2,r3,r5 = 5 (ref excluded)
    assert res["r1"].score_components["reachable_nodes"] == 5
    # r2 reaches a2,r3,r5 = 3
    assert res["r2"].score_components["reachable_nodes"] == 3
    # leaves at the bottom reach nothing
    assert res["r3"].score == 0
    assert res["r5"].score == 0
    assert res["r1"].score_type == "downstream_blast_radius"


def test_reach_backward_dependency():
    ctx = _build_ctx()
    res = ReachScorer(reach_direction="backward").score(ctx)
    # r3 (bottom) reaches all upstream: a2,r2,a1,r1,r4 = 5
    assert res["r3"].score_components["reachable_nodes"] == 5
    # r1 (top) has nothing upstream
    assert res["r1"].score == 0
    assert res["r3"].score_type == "upstream_dependency"


def test_reach_forward_and_backward_rank_oppositely():
    """The core insight: same graph, opposite directions -> flipped ranking."""
    ctx = _build_ctx()
    fwd = ReachScorer(reach_direction="forward").score(ctx)
    bwd = ReachScorer(reach_direction="backward").score(ctx)
    # r1 is top in forward (blast radius) but bottom in backward (no upstream)
    assert fwd["r1"].score > fwd["r3"].score
    assert bwd["r1"].score < bwd["r3"].score


# ---------------------------------------------------------------------------
# Registry / select_flow_scorer
# ---------------------------------------------------------------------------


def test_registry_defaults_to_degree():
    scorer, meta = select_flow_scorer({})
    assert isinstance(scorer, DegreeScorer)
    assert meta["scoring_method"] == "degree"


def test_registry_purpose_supply_risk():
    scorer, meta = select_flow_scorer({"purpose": "supply_risk"})
    assert isinstance(scorer, ReachScorer)
    assert scorer.reach_direction == "forward"
    assert meta["score_type"] == "downstream_blast_radius"


def test_registry_purpose_sourcing_dependency():
    scorer, meta = select_flow_scorer({"purpose": "sourcing_dependency"})
    assert isinstance(scorer, ReachScorer)
    assert scorer.reach_direction == "backward"


def test_registry_purpose_bottleneck():
    scorer, meta = select_flow_scorer({"purpose": "bottleneck"})
    assert isinstance(scorer, BetweennessScorer)


def test_registry_purpose_importance():
    scorer, meta = select_flow_scorer({"purpose": "importance"})
    assert isinstance(scorer, PageRankScorer)


def test_registry_explicit_method_overrides_purpose():
    scorer, meta = select_flow_scorer(
        {"purpose": "supply_risk", "scoring_method": "pagerank"}
    )
    assert isinstance(scorer, PageRankScorer)
    assert meta["scoring_method"] == "pagerank"


def test_registry_scoring_cfg_passes_through():
    scorer, meta = select_flow_scorer(
        {"scoring_method": "pagerank", "scoring": {"damping": 0.7}}
    )
    assert isinstance(scorer, PageRankScorer)
    assert scorer.damping == 0.7


def test_registry_reach_cfg_overrides_purpose_default():
    # purpose says forward, but explicit scoring cfg forces backward
    scorer, meta = select_flow_scorer(
        {"purpose": "supply_risk", "scoring": {"reach_direction": "backward"}}
    )
    assert isinstance(scorer, ReachScorer)
    assert scorer.reach_direction == "backward"


def test_registry_rejects_unknown_method():
    with pytest.raises(ValueError):
        select_flow_scorer({"scoring_method": "nonsense"})


def test_registry_rejects_unknown_purpose():
    with pytest.raises(ValueError):
        select_flow_scorer({"purpose": "nope"})
