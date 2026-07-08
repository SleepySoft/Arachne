"""Utilities for following and expanding `derived_from` material lineage edges."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from app.database import get_async_driver


_DERIVED_FROM_EDGE_TYPE = "derived_from"
_DERIVED_FROM_NAMESPACE = "INDUSTRIAL_FLOW"


async def _one_step_neighbors(
    node_ids: List[str],
    direction: str,
) -> Dict[str, List[str]]:
    """Return one-step neighbors along derived_from edges for each source node.

    direction:
      - "forward": follow edge direction (source -> target),
                   i.e. from derived product towards raw material.
      - "backward": reverse edge direction (target <- source),
                    i.e. from raw material towards derived products.
    """
    if not node_ids:
        return {}

    driver = get_async_driver()
    if direction == "forward":
        cypher = f"""
        MATCH (n:IndustrialNode)-[r:{_DERIVED_FROM_NAMESPACE} {{edge_type: $edge_type}}]->(m:IndustrialNode)
        WHERE n.node_id IN $node_ids
        RETURN n.node_id AS src, collect(DISTINCT m.node_id) AS dsts
        """
    else:
        cypher = f"""
        MATCH (n:IndustrialNode)<-[r:{_DERIVED_FROM_NAMESPACE} {{edge_type: $edge_type}}]-(m:IndustrialNode)
        WHERE n.node_id IN $node_ids
        RETURN n.node_id AS src, collect(DISTINCT m.node_id) AS dsts
        """

    async with driver.session() as session:
        result = await session.run(
            cypher,
            node_ids=node_ids,
            edge_type=_DERIVED_FROM_EDGE_TYPE,
        )
        mapping: Dict[str, List[str]] = {}
        async for record in result:
            mapping[record["src"]] = record["dsts"]
        return mapping


async def expand_by_derived_from(
    node_ids: List[str],
    direction: str = "both",
    max_hops: int = 5,
) -> Set[str]:
    """Expand a set of node IDs by following derived_from edges.

    The returned set always includes the original node IDs.
    direction may be "forward", "backward", or "both".
    """
    if not node_ids:
        return set()

    closed: Set[str] = set(node_ids)
    frontier: Set[str] = set(node_ids)

    for _ in range(max_hops):
        if not frontier:
            break
        directions_to_walk = []
        if direction in ("forward", "both"):
            directions_to_walk.append("forward")
        if direction in ("backward", "both"):
            directions_to_walk.append("backward")

        next_frontier: Set[str] = set()
        for walk_dir in directions_to_walk:
            neighbors = await _one_step_neighbors(list(frontier), walk_dir)
            for dsts in neighbors.values():
                for dst in dsts:
                    if dst not in closed:
                        closed.add(dst)
                        next_frontier.add(dst)
        frontier = next_frontier

    return closed


async def get_derived_from_lineage(
    node_id: str,
    max_hops: int = 5,
) -> Dict[str, List[str]]:
    """Return ancestors and descendants of a node via derived_from edges.

    - ancestors: nodes that this node is directly or indirectly derived from.
    - descendants: nodes that directly or indirectly derive from this node.
    """
    ancestors = await expand_by_derived_from([node_id], direction="forward", max_hops=max_hops)
    descendants = await expand_by_derived_from([node_id], direction="backward", max_hops=max_hops)
    # Remove the node itself from each list
    ancestors.discard(node_id)
    descendants.discard(node_id)
    return {
        "ancestors": sorted(ancestors),
        "descendants": sorted(descendants),
    }


async def get_equivalence_classes(
    node_ids: List[str],
    max_hops: int = 5,
) -> Dict[str, Set[str]]:
    """Map each input node to its undirected derived_from connected component."""
    if not node_ids:
        return {}

    classes: Dict[str, Set[str]] = {}
    for nid in node_ids:
        eq = await expand_by_derived_from([nid], direction="both", max_hops=max_hops)
        classes[nid] = eq
    return classes


def collapse_equivalence_classes(
    node_ids: List[str],
    classes: Dict[str, Set[str]],
) -> List[Set[str]]:
    """Merge overlapping equivalence classes into disjoint sets."""
    ids = set(node_ids)
    groups: List[Set[str]] = []
    for nid in ids:
        eq = classes.get(nid, {nid})
        merged = set(eq)
        merged.add(nid)
        # Merge with any existing group that overlaps
        new_groups: List[Set[str]] = []
        for g in groups:
            if g & merged:
                merged |= g
            else:
                new_groups.append(g)
        new_groups.append(merged)
        groups = new_groups
    return groups
