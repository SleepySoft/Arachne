"""Topology-aware source resolution for reasoning.

Ontology edges have different semantics from supply-chain edges. This module
resolves/replaces source nodes before flow traversal so that reasoning starts
from the semantically correct nodes.

Semantics:

* ``alias_of`` (别名/同义): upstream node is only an alias, all real
  relationships should attach to the downstream (canonical) node. We always
  resolve aliases to their canonical targets.

* ``is_a`` (是一种): logical subclass/superclass. Generic material/process
  edges attach to the downstream (parent/superclass), while specific
  upstream/downstream edges attach to the upstream (child/subclass). For
  reasoning we expand in both directions (parents and children).

* ``part_of`` (组成部分): a part can be viewed as its whole. We expand from
  part (upstream) to whole (downstream). We also expand from whole to direct
  parts because real process flows often connect to sub-nodes.

* ``variant_of`` / ``related_term``: semantically related but ambiguous. We
  treat them as bidirectional semantic neighbours with a small hop limit.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

from app.database import get_async_driver

ALIAS_EDGE_TYPE = "alias_of"
HIERARCHY_EDGE_TYPES = {"is_a", "part_of"}
RELATED_EDGE_TYPES = {"variant_of", "related_term"}
ALL_TOPOLOGY_EDGE_TYPES = {ALIAS_EDGE_TYPE, *HIERARCHY_EDGE_TYPES, *RELATED_EDGE_TYPES}


async def _query_direct_neighbors(
    node_ids: List[str],
    edge_type: str,
    direction: str,
) -> Set[str]:
    """Return one-step neighbors along a specific ontology edge type/direction.

    direction:
      - "out": follow edge direction (upstream -> downstream).
      - "in": reverse edge direction (downstream -> upstream).
    """
    if not node_ids:
        return set()

    driver = get_async_driver()
    if direction == "out":
        rel_clause = f"-[r:ONTOLOGY {{edge_type: '{edge_type}'}}]->"
    else:
        rel_clause = f"<-[r:ONTOLOGY {{edge_type: '{edge_type}'}}]-"

    cypher = f"""
    MATCH (src:IndustrialNode)
    WHERE src.node_id IN $node_ids
    MATCH (src){rel_clause}(dst:IndustrialNode)
    RETURN DISTINCT dst.node_id AS node_id
    """

    neighbors: Set[str] = set()
    async with driver.session() as session:
        result = await session.run(cypher, node_ids=list(node_ids))
        async for record in result:
            neighbors.add(record["node_id"])
    return neighbors


async def resolve_aliases(
    node_ids: List[str],
    max_hops: int = 3,
) -> Tuple[Set[str], Dict[str, str]]:
    """Resolve ``alias_of`` aliases to their canonical downstream nodes.

    Returns:
        - A set of canonical node IDs to use as effective sources.
        - A mapping ``{original_node_id: canonical_node_id}`` for diagnostics.
    """
    if not node_ids:
        return set(), {}

    driver = get_async_driver()
    resolved_map: Dict[str, str] = {nid: nid for nid in node_ids}
    frontier: Set[str] = set(node_ids)

    for _ in range(max_hops):
        if not frontier:
            break
        alias_to_canonical: Dict[str, str] = {}
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH (src:IndustrialNode)-[r:ONTOLOGY {edge_type: $alias_type}]->(dst:IndustrialNode)
                WHERE src.node_id IN $frontier
                RETURN src.node_id AS alias_id, dst.node_id AS canonical_id
                """,
                frontier=list(frontier),
                alias_type=ALIAS_EDGE_TYPE,
            )
            async for record in result:
                alias_to_canonical[record["alias_id"]] = record["canonical_id"]

        if not alias_to_canonical:
            break

        next_frontier: Set[str] = set()
        for original, current in list(resolved_map.items()):
            if current in alias_to_canonical:
                canonical = alias_to_canonical[current]
                resolved_map[original] = canonical
                next_frontier.add(canonical)
        frontier = next_frontier

    return set(resolved_map.values()), resolved_map


async def _expand_hierarchy(
    node_ids: List[str],
    edge_type: str,
    direction: str,
    max_hops: int,
) -> Set[str]:
    """Expand node set along a directed ontology edge type up to max_hops."""
    if not node_ids or max_hops <= 0:
        return set()

    driver = get_async_driver()
    if direction == "out":
        rel_clause = f"-[r:ONTOLOGY*1..{max_hops}]->"
    else:
        rel_clause = f"<-[r:ONTOLOGY*1..{max_hops}]-"

    cypher = f"""
    MATCH (src:IndustrialNode)
    WHERE src.node_id IN $node_ids
    MATCH (src){rel_clause}(dst:IndustrialNode)
    WHERE all(rel IN r WHERE rel.edge_type = $edge_type)
    RETURN DISTINCT dst.node_id AS node_id
    """

    expanded: Set[str] = set()
    async with driver.session() as session:
        result = await session.run(
            cypher,
            node_ids=list(node_ids),
            edge_type=edge_type,
        )
        async for record in result:
            expanded.add(record["node_id"])
    return expanded


async def expand_is_a(
    node_ids: List[str],
    max_hops: int = 2,
) -> Tuple[Set[str], Set[str]]:
    """Expand by ``is_a``: return (parents, children).

    - parents  = downstream targets of ``is_a`` (superclasses).
    - children = upstream sources of ``is_a`` (subclasses).
    """
    parents = await _expand_hierarchy(node_ids, "is_a", "out", max_hops)
    children = await _expand_hierarchy(node_ids, "is_a", "in", max_hops)
    return parents, children


async def expand_part_of(
    node_ids: List[str],
    max_hops_whole: int = 2,
    max_hops_part: int = 1,
) -> Tuple[Set[str], Set[str]]:
    """Expand by ``part_of``: return (wholes, parts).

    - wholes = downstream targets of ``part_of`` (groups/parents).
    - parts  = upstream sources of ``part_of`` (sub-parts).
    """
    wholes = await _expand_hierarchy(node_ids, "part_of", "out", max_hops_whole)
    parts = await _expand_hierarchy(node_ids, "part_of", "in", max_hops_part)
    return wholes, parts


async def expand_related(
    node_ids: List[str],
    max_hops: int = 1,
) -> Set[str]:
    """Expand by ``variant_of`` / ``related_term`` in both directions."""
    if not node_ids or max_hops <= 0:
        return set()

    driver = get_async_driver()
    cypher = f"""
    MATCH (src:IndustrialNode)
    WHERE src.node_id IN $node_ids
    MATCH (src)-[r:ONTOLOGY*1..{max_hops}]-(dst:IndustrialNode)
    WHERE all(rel IN r WHERE rel.edge_type IN $edge_types)
    RETURN DISTINCT dst.node_id AS node_id
    """

    expanded: Set[str] = set()
    async with driver.session() as session:
        result = await session.run(
            cypher,
            node_ids=list(node_ids),
            edge_types=list(RELATED_EDGE_TYPES),
        )
        async for record in result:
            expanded.add(record["node_id"])
    return expanded


async def resolve_sources_topologically(
    node_ids: List[str],
    expand_ontology: bool = False,
    max_ontology_hops: int = 2,
) -> Tuple[Set[str], Dict[str, Any]]:
    """Resolve source nodes according to topology semantics.

    Always performs alias normalization. When ``expand_ontology`` is true,
    also expands ``is_a``, ``part_of``, ``variant_of`` and ``related_term``.

    Returns:
        - Effective source node IDs for flow traversal.
        - Resolution details for diagnostics.
    """
    if not node_ids:
        return set(), {"aliases_resolved": {}}

    canonical_ids, alias_map = await resolve_aliases(node_ids)

    details: Dict[str, Any] = {
        "aliases_resolved": alias_map,
    }

    if not expand_ontology:
        return canonical_ids, details

    is_a_parents, is_a_children = await expand_is_a(
        list(canonical_ids), max_hops=max_ontology_hops
    )
    part_of_wholes, part_of_parts = await expand_part_of(
        list(canonical_ids),
        max_hops_whole=max_ontology_hops,
        max_hops_part=1,
    )
    related = await expand_related(list(canonical_ids), max_hops=1)

    effective = (
        canonical_ids
        | is_a_parents
        | is_a_children
        | part_of_wholes
        | part_of_parts
        | related
    )

    details.update(
        {
            "is_a_parents": is_a_parents,
            "is_a_children": is_a_children,
            "part_of_wholes": part_of_wholes,
            "part_of_parts": part_of_parts,
            "related": related,
        }
    )
    return effective, details

