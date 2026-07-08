"""Topology (ontology) expansion utilities for reasoning.

Ontology edges (``is_a``, ``part_of``, ``related_term``, ``variant_of``,
``alias_of``) express taxonomic or structural relationships, not supply-chain
flow. Reasoning tasks therefore handle them separately from
:class:`~app.models.schemas.IndustrialFlowEdge` edges:

* By default they are **not** traversed as part of flow paths.
* They can be used to expand the source node set before flow traversal when
  ``expand_ontology=True`` is requested.
"""

from __future__ import annotations

from typing import List, Set

from app.database import get_async_driver

TOPOLOGY_EDGE_TYPES = {"is_a", "part_of", "related_term", "variant_of", "alias_of"}


async def expand_by_topology(
    node_ids: List[str],
    direction: str = "both",
    max_hops: int = 2,
) -> Set[str]:
    """Expand a set of seed nodes via ontology edges.

    Args:
        node_ids: Seed node IDs.
        direction: ``"forward"`` (child → parent), ``"backward"`` (parent → child),
            or ``"both"``.
        max_hops: Maximum ontology hops to perform.

    Returns:
        Union of ``node_ids`` and any ontology-reachable node IDs.
    """
    if not node_ids or max_hops <= 0:
        return set(node_ids)

    driver = get_async_driver()
    params = {
        "seed_ids": list(node_ids),
        "edge_types": list(TOPOLOGY_EDGE_TYPES),
        "max_hops": max_hops,
    }

    if direction == "forward":
        rel_clause = f"-[r:ONTOLOGY*1..{max_hops}]->"
    elif direction == "backward":
        rel_clause = f"<-[r:ONTOLOGY*1..{max_hops}]-"
    else:
        rel_clause = f"-[r:ONTOLOGY*1..{max_hops}]-"

    cypher = f"""
    MATCH (src:IndustrialNode)
    WHERE src.node_id IN $seed_ids
    MATCH (src){rel_clause}(dst:IndustrialNode)
    WHERE all(rel IN r WHERE rel.edge_type IN $edge_types)
    RETURN DISTINCT dst.node_id AS node_id
    """

    expanded: Set[str] = set(node_ids)
    async with driver.session() as session:
        result = await session.run(cypher, **params)
        async for record in result:
            expanded.add(record["node_id"])
    return expanded
