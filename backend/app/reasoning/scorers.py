"""Pluggable scoring functions for reasoning tasks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.models.schemas import GraphEdge


class BaseScorer(ABC):
    """Abstract base for all scorers."""

    name: str = "base"

    @abstractmethod
    def score(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> float:
        """Return a score for the given path/edge sequence."""
        raise NotImplementedError

    def score_components(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """Return human-readable score components."""
        return {"score": self.score(path, edges, node_scores)}


class DepthDecayScorer(BaseScorer):
    """Score decays exponentially with path length."""

    name = "depth_decay"

    def __init__(self, decay: float = 0.75, max_depth: int = 10):
        if not 0 < decay <= 1:
            raise ValueError("decay must be in (0, 1]")
        self.decay = decay
        self.max_depth = max_depth

    def score(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> float:
        depth = max(1, len(edges))
        return self.decay ** (depth - 1)

    def score_components(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        depth = max(1, len(edges))
        return {"depth": depth, "decay": self.decay, "factor": self.decay ** (depth - 1)}


class EdgeWeightScorer(BaseScorer):
    """Score is the product of edge weights along the path."""

    name = "edge_weight"

    def __init__(self, edge_weights: Optional[Dict[str, float]] = None):
        self.edge_weights = edge_weights or {}

    def _edge_weight(self, edge: GraphEdge) -> float:
        key = getattr(edge, "edge_type", None) or "unknown"
        return self.edge_weights.get(key, 0.5)

    def score(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> float:
        if not edges:
            return 1.0
        product = 1.0
        for edge in edges:
            product *= self._edge_weight(edge)
        return product

    def score_components(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        components = {}
        for i, edge in enumerate(edges):
            components[f"edge_{i}"] = {
                "edge_id": edge.edge_id,
                "edge_type": getattr(edge, "edge_type", None),
                "weight": self._edge_weight(edge),
            }
        return {"edge_weights": components, "product": self.score(path, edges, node_scores)}


class CompositeScorer(BaseScorer):
    """Combine multiple scorers with optional weights."""

    name = "composite"

    def __init__(
        self,
        scorers: List[BaseScorer],
        scorer_weights: Optional[List[float]] = None,
    ):
        self.scorers = scorers
        if scorer_weights is None:
            scorer_weights = [1.0] * len(scorers)
        if len(scorer_weights) != len(scorers):
            raise ValueError("scorer_weights length must match scorers length")
        total = sum(scorer_weights)
        self.scorer_weights = [w / total for w in scorer_weights]

    def score(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> float:
        total = 0.0
        for scorer, weight in zip(self.scorers, self.scorer_weights):
            total += scorer.score(path, edges, node_scores) * weight
        return total

    def score_components(
        self,
        path: List[str],
        edges: List[GraphEdge],
        node_scores: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        components = {}
        for scorer, weight in zip(self.scorers, self.scorer_weights):
            components[scorer.name] = {
                "weight": weight,
                "score": scorer.score(path, edges, node_scores),
                "details": scorer.score_components(path, edges, node_scores),
            }
        return {"components": components, "score": self.score(path, edges, node_scores)}
