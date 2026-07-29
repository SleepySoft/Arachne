"""Pluggable node scorers for arachne-flow association reasoning.

Each scorer ranks nodes within the BFS-traversed subgraph by a different graph-
theoretic notion of importance. The scorer to use is resolved from the task
``parameters`` via either an explicit ``scoring_method`` or a semantic
``purpose`` (which binds to a default method + direction).

Implemented scorers (see ``docs/flow_scoring_design.md`` for rationale):
  - DegreeScorer      weighted degree centrality (baseline, backward-compat)
  - PageRankScorer    personalized PageRank / random walk with restart
  - BetweennessScorer betweenness centrality (Brandes) - bottleneck detection
  - ReachScorer       directional reachability - supply-risk / dependency pair

Note: legacy ``scorers.py`` scores *paths* (``BaseScorer.score(path, edges)``);
arachne-flow scores *nodes within a subgraph*, a different abstraction layer, so
a separate ``FlowNodeScorer`` base is used to avoid over-generalising.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Context & result containers
# ---------------------------------------------------------------------------


@dataclass
class FlowScoringContext:
    """Everything a scorer needs, all produced by the BFS traversal stage."""

    nodes: Dict[str, Dict[str, Any]]
    edges: Dict[str, Dict[str, Any]]
    seed_resources: Set[str]
    seed_actions: Set[str]
    direction: str  # "forward" | "backward" | "both" (traversal direction)
    name_map: Dict[str, str]
    entity_map: Dict[str, str]
    resource_actions: Dict[str, Set[str]]
    branch_links: Dict[str, Set[str]]


@dataclass
class NodeScoreResult:
    score: float
    score_components: Dict[str, Any]
    score_type: str
    flags: List[str] = field(default_factory=list)


class FlowNodeScorer(ABC):
    """Rank nodes within a traversed arachne-flow subgraph."""

    name: str = "base"
    default_score_type: str = "association_strength"

    @abstractmethod
    def score(self, ctx: FlowScoringContext) -> Dict[str, NodeScoreResult]:
        """Return ``node_id -> NodeScoreResult`` for every node in ``ctx``."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Adjacency helper
# ---------------------------------------------------------------------------

# ref edges (ACTION -> METHOD) are semantic links, not material flow.
_REF_ROLE = "ref"


def _build_adjacency(
    ctx: FlowScoringContext,
    mode: str = "both",
    exclude_ref: bool = False,
) -> Dict[str, Set[str]]:
    """Build a successor adjacency map from the traversed edges.

    BFS stores every edge in production-flow orientation
    (resource -> action -> resource), regardless of traversal direction, so
    ``from -> to`` is reliably "downstream".

    ``mode``: "forward" keeps from->to, "backward" reverses, "both" is symmetric.
    ``exclude_ref``: drop ref edges (used by material-flow scorers).
    """
    adj: Dict[str, Set[str]] = {nid: set() for nid in ctx.nodes}
    for e in ctx.edges.values():
        role = e.get("role", "")
        if exclude_ref and role == _REF_ROLE:
            continue
        src, dst = e["from"], e["to"]
        if src not in adj or dst not in adj:
            continue
        if mode in ("forward", "both"):
            adj[src].add(dst)
        if mode in ("backward", "both"):
            adj[dst].add(src)
    return adj


# ---------------------------------------------------------------------------
# 1. DegreeScorer (baseline = original behaviour)
# ---------------------------------------------------------------------------


class DegreeScorer(FlowNodeScorer):
    """Weighted degree centrality: main-line ACTION count + branch links."""

    name = "degree"
    default_score_type = "association_strength"

    def __init__(self, main_weight: float = 1.0, branch_weight: float = 0.5):
        self.main_weight = main_weight
        self.branch_weight = branch_weight

    def score(self, ctx: FlowScoringContext) -> Dict[str, NodeScoreResult]:
        results: Dict[str, NodeScoreResult] = {}
        for nid in ctx.nodes:
            main_deg = len(ctx.resource_actions.get(nid, set()))
            branch_deg = len(ctx.branch_links.get(nid, set()))
            results[nid] = NodeScoreResult(
                score=self.main_weight * main_deg + self.branch_weight * branch_deg,
                score_components={
                    "main_actions": main_deg,
                    "branch_links": branch_deg,
                    "main_weight": self.main_weight,
                    "branch_weight": self.branch_weight,
                },
                score_type=self.default_score_type,
            )
        return results


# ---------------------------------------------------------------------------
# 2. PageRankScorer (personalized PageRank / random walk with restart)
# ---------------------------------------------------------------------------


class PageRankScorer(FlowNodeScorer):
    """Personalized PageRank over the traversed subgraph, seeded from the query.

    ``r = damping * P^T r + (1 - damping) * s`` where ``s`` is uniform over the
    seed nodes. Naturally combines depth decay + directed propagation +
    seed-relative importance (the synthesis of the legacy decay scorer and the
    arachne degree scorer).
    """

    name = "pagerank"
    default_score_type = "personalized_pagerank"

    def __init__(self, damping: float = 0.85, max_iter: int = 50, tol: float = 1e-6):
        if not 0.0 < damping < 1.0:
            raise ValueError("damping must be in (0, 1)")
        self.damping = damping
        self.max_iter = max_iter
        self.tol = tol

    def score(self, ctx: FlowScoringContext) -> Dict[str, NodeScoreResult]:
        node_ids = list(ctx.nodes.keys())
        n = len(node_ids)
        if n == 0:
            return {}
        idx = {nid: i for i, nid in enumerate(node_ids)}

        mode = "both" if ctx.direction == "both" else ctx.direction
        adj = _build_adjacency(ctx, mode=mode, exclude_ref=False)

        out_deg = [len(adj[nid]) for nid in node_ids]
        # successor index lists
        succ = [[idx[d] for d in adj[nid]] for nid in node_ids]

        # seed vector: uniform over seeds present in the subgraph
        seeds = (ctx.seed_resources | ctx.seed_actions) & set(ctx.nodes)
        if seeds:
            s = [0.0] * n
            for nid in seeds:
                s[idx[nid]] = 1.0 / len(seeds)
        else:
            s = [1.0 / n] * n  # degenerate: uniform fallback

        r = s[:]
        for _ in range(self.max_iter):
            r_new = [0.0] * n
            dangling_mass = 0.0
            for i in range(n):
                if out_deg[i] == 0:
                    dangling_mass += r[i]
                else:
                    share = r[i] / out_deg[i]
                    for j in succ[i]:
                        r_new[j] += share
            # redistribute dangling mass uniformly
            if dangling_mass > 0 and n > 0:
                add = dangling_mass / n
                r_new = [v + add for v in r_new]
            # teleport
            r_new = [self.damping * v + (1.0 - self.damping) * s[i] for i, v in enumerate(r_new)]
            delta = sum(abs(r_new[i] - r[i]) for i in range(n))
            r = r_new
            if delta < self.tol:
                break

        max_r = max(r) if r else 0.0
        results: Dict[str, NodeScoreResult] = {}
        for i, nid in enumerate(node_ids):
            val = r[i]
            results[nid] = NodeScoreResult(
                score=val,
                score_components={
                    "pagerank": val,
                    "normalized": (val / max_r) if max_r > 0 else 0.0,
                    "damping": self.damping,
                    "iterations": self.max_iter,
                    "is_seed": nid in seeds,
                },
                score_type=self.default_score_type,
                flags=["seed"] if nid in seeds else [],
            )
        return results


# ---------------------------------------------------------------------------
# 3. BetweennessScorer (Brandes' algorithm)
# ---------------------------------------------------------------------------


class BetweennessScorer(FlowNodeScorer):
    """Betweenness centrality via Brandes' algorithm.

    Nodes sitting on many shortest paths are bottlenecks. Note: high degree does
    not imply high betweenness (a hub may have parallel bypass paths).
    """

    name = "betweenness"
    default_score_type = "betweenness_centrality"

    def __init__(self, normalize: bool = True):
        self.normalize = normalize

    def score(self, ctx: FlowScoringContext) -> Dict[str, NodeScoreResult]:
        node_ids = list(ctx.nodes.keys())
        n = len(node_ids)
        if n == 0:
            return {}
        idx = {nid: i for i, nid in enumerate(node_ids)}

        undirected = ctx.direction == "both"
        mode = "both" if undirected else ctx.direction
        adj = _build_adjacency(ctx, mode=mode, exclude_ref=False)

        betweenness = [0.0] * n

        for s in range(n):
            # single-source shortest paths (BFS, unweighted)
            stack: List[int] = []
            pred: List[List[int]] = [[] for _ in range(n)]
            sigma = [0.0] * n
            sigma[s] = 1.0
            dist = [-1] * n
            dist[s] = 0
            q = deque([s])
            while q:
                v = q.popleft()
                stack.append(v)
                for w in adj[node_ids[v]]:
                    wj = idx[w]
                    if dist[wj] < 0:
                        q.append(wj)
                        dist[wj] = dist[v] + 1
                    if dist[wj] == dist[v] + 1:
                        sigma[wj] += sigma[v]
                        pred[wj].append(v)
            delta = [0.0] * n
            while stack:
                w = stack.pop()
                for v in pred[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
                if w != s:
                    betweenness[w] += delta[w]

        if undirected:
            betweenness = [b / 2.0 for b in betweenness]

        # normalise to [0,1] by theoretical max for comparability
        max_val = max(betweenness) if betweenness else 0.0
        results: Dict[str, NodeScoreResult] = {}
        for i, nid in enumerate(node_ids):
            val = betweenness[i]
            norm = (val / max_val) if max_val > 0 else 0.0
            results[nid] = NodeScoreResult(
                score=val,
                score_components={
                    "betweenness": val,
                    "normalized": norm if self.normalize else None,
                },
                score_type=self.default_score_type,
            )
        return results


# ---------------------------------------------------------------------------
# 4. ReachScorer (directional reachability)
# ---------------------------------------------------------------------------


class ReachScorer(FlowNodeScorer):
    """Directional reachability: how many nodes are downstream / upstream of N.

    - ``forward``  (supply_risk): downstream blast radius - if N is cut, how many
      nodes are affected.
    - ``backward`` (sourcing_dependency): upstream dependency breadth - how many
      nodes feed into N.

    Only material-flow edges are counted (ref edges excluded); methods are not
    part of the flow and will score 0.
    """

    name = "reach"
    default_score_type = "downstream_blast_radius"

    def __init__(self, reach_direction: str = "forward"):
        if reach_direction not in ("forward", "backward"):
            raise ValueError("reach_direction must be 'forward' or 'backward'")
        self.reach_direction = reach_direction
        self.default_score_type = (
            "downstream_blast_radius"
            if reach_direction == "forward"
            else "upstream_dependency"
        )

    def _reachable_count(self, start: str, adj: Dict[str, Set[str]]) -> int:
        seen: Set[str] = set()
        q = deque(adj.get(start, ()))
        while q:
            v = q.popleft()
            if v in seen:
                continue
            seen.add(v)
            for w in adj.get(v, ()):
                if w not in seen:
                    q.append(w)
        return len(seen)  # excludes start itself

    def score(self, ctx: FlowScoringContext) -> Dict[str, NodeScoreResult]:
        mode = self.reach_direction
        adj = _build_adjacency(ctx, mode=mode, exclude_ref=True)
        counts = {nid: self._reachable_count(nid, adj) for nid in ctx.nodes}
        max_c = max(counts.values()) if counts else 0
        results: Dict[str, NodeScoreResult] = {}
        for nid in ctx.nodes:
            val = float(counts[nid])
            results[nid] = NodeScoreResult(
                score=val,
                score_components={
                    "reachable_nodes": counts[nid],
                    "normalized": (val / max_c) if max_c > 0 else 0.0,
                    "reach_direction": self.reach_direction,
                },
                score_type=self.default_score_type,
            )
        return results


# ---------------------------------------------------------------------------
# Registry: purpose -> (method, defaults)
# ---------------------------------------------------------------------------

# purpose -> (scoring_method, score_type, extra scorer kwargs)
PURPOSE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "exposure": {
        "scoring_method": "degree",
        "score_type": "association_strength",
    },
    "supply_risk": {
        "scoring_method": "reach",
        "score_type": "downstream_blast_radius",
        "reach_direction": "forward",
    },
    "sourcing_dependency": {
        "scoring_method": "reach",
        "score_type": "upstream_dependency",
        "reach_direction": "backward",
    },
    "bottleneck": {
        "scoring_method": "betweenness",
        "score_type": "betweenness_centrality",
    },
    "importance": {
        "scoring_method": "pagerank",
        "score_type": "personalized_pagerank",
    },
}

VALID_SCORING_METHODS = {"degree", "pagerank", "betweenness", "reach"}
VALID_PURPOSES = set(PURPOSE_REGISTRY.keys())


def select_flow_scorer(
    params: Dict[str, Any],
) -> Tuple[FlowNodeScorer, Dict[str, Any]]:
    """Resolve which scorer to use from task ``parameters``.

    Priority:
      1. ``scoring_method`` (explicit override)
      2. ``purpose`` (semantic intent -> registered default)
      3. neither -> ``degree`` (backward compatible)

    Scorer-specific tuning lives under the ``scoring`` sub-dict, e.g.
    ``{"scoring": {"damping": 0.9}}`` or
    ``{"scoring": {"reach_direction": "forward"}}``.
    """
    scoring_cfg = dict(params.get("scoring", {}))
    method = params.get("scoring_method")
    purpose = params.get("purpose")
    meta: Dict[str, Any] = {"purpose": purpose, "scoring_method": None}

    if method:
        if method not in VALID_SCORING_METHODS:
            raise ValueError(
                f"Unknown scoring_method '{method}'. Valid: {sorted(VALID_SCORING_METHODS)}"
            )
        meta["scoring_method"] = method
    elif purpose:
        if purpose not in PURPOSE_REGISTRY:
            raise ValueError(
                f"Unknown purpose '{purpose}'. Valid: {sorted(VALID_PURPOSES)}"
            )
        entry = PURPOSE_REGISTRY[purpose]
        method = entry["scoring_method"]
        meta["scoring_method"] = method
        meta["score_type"] = entry["score_type"]
        # purpose-supplied defaults are overridden by explicit scoring cfg
        for k, v in entry.items():
            if k not in ("scoring_method", "score_type") and k not in scoring_cfg:
                scoring_cfg[k] = v
    else:
        method = "degree"
        meta["scoring_method"] = "degree"

    if method == "degree":
        scorer: FlowNodeScorer = DegreeScorer(
            main_weight=scoring_cfg.get("main_weight", 1.0),
            branch_weight=scoring_cfg.get("branch_weight", 0.5),
        )
    elif method == "pagerank":
        scorer = PageRankScorer(
            damping=scoring_cfg.get("damping", 0.85),
            max_iter=scoring_cfg.get("max_iter", 50),
            tol=scoring_cfg.get("tol", 1e-6),
        )
    elif method == "betweenness":
        scorer = BetweennessScorer(normalize=scoring_cfg.get("normalize", True))
    else:  # reach
        scorer = ReachScorer(
            reach_direction=scoring_cfg.get("reach_direction", "forward")
        )

    meta["scorer_name"] = scorer.name
    meta.setdefault("score_type", scorer.default_score_type)
    return scorer, meta
