"""
Policy enforcement for `derived_from` industrial-flow edges.

`derived_from` represents an explicit, human-curated material lineage assertion:
"a typical `from_node` is materially derived from `to_node`". It intentionally
skips process nodes and must not be used for generic consumables.

This is a legacy-engine policy: it depends on the original Neo4j industrial-flow
schema and storage layout.
"""

from __future__ import annotations

from typing import Optional, Set

from app.database import get_async_driver
from app.engines.legacy.storage import get_node, list_edges


# IDs of nodes that are generic process consumables. Derived_from must not point
# to these nodes because they participate in the process but do not define the
# material identity of the product. This list can be extended as the graph grows.
GENERIC_CONSUMABLE_IDS: Set[str] = {
    "water",
    "deionized_water",
    "ultrapure_water",
    "pure_water",
    "electricity",
    "power",
    "compressed_air",
    "air",
    "nitrogen",
    "oxygen",
    "argon",
    "hydrogen",
    "natural_gas",
    "cleaning_agent",
    "detergent",
    "solvent",
    "etching_gas",
    "process_gas",
    "cooling_water",
    "wastewater",
}

# Entity types that are acceptable as endpoints of a derived_from edge.
# Process nodes are explicitly excluded; non-material types such as service,
# software, capability, platform, standard, data_asset are also excluded because
# they do not carry material identity.
_ACCEPTABLE_ENTITY_TYPES: Set[str] = {
    "material",
    "part",
    "device",
    "equipment",
    "system",
    "infrastructure",
    "unknown",
}


def is_generic_consumable(node_id: str) -> bool:
    """Return True if the node is considered a generic process consumable."""
    return node_id in GENERIC_CONSUMABLE_IDS


async def _get_node_or_raise(node_id: str, label: str) -> dict:
    node = await get_node(node_id)
    if node is None:
        raise ValueError(f"{label} node '{node_id}' does not exist")
    return node


async def _existing_derived_from(from_node_id: str, to_node_id: str) -> bool:
    """Return True if a derived_from edge already exists between the two nodes."""
    edges, total = await list_edges(
        edge_namespace="industrial_flow",
        edge_type="derived_from",
        from_node=from_node_id,
        to_node=to_node_id,
    )
    return total > 0 or len(edges) > 0


async def _would_create_cycle(from_node_id: str, to_node_id: str) -> bool:
    """
    Return True if adding from_node -> to_node would create a cycle in the
    derived_from graph (i.e., to_node can already reach from_node via derived_from).
    """
    driver = get_async_driver()
    async with driver.session() as session:
        result = await session.run(
            """
            MATCH path = (start:IndustrialNode {node_id: $to_id})-[:INDUSTRIAL_FLOW*1..10]->(end:IndustrialNode {node_id: $from_id})
            WHERE ALL(r IN relationships(path) WHERE r.edge_type = 'derived_from')
            RETURN count(path) AS c
            """,
            to_id=to_node_id,
            from_id=from_node_id,
        )
        records = await result.data()
        return records[0]["c"] > 0 if records else False


async def validate_derived_from_edge(
    from_node_id: str,
    to_node_id: str,
    skip_cycle_check: bool = False,
) -> None:
    """
    Validate that a `derived_from` edge from `from_node_id` to `to_node_id`
    complies with the policy. Raises ValueError with a descriptive message if not.
    """
    if from_node_id == to_node_id:
        raise ValueError("derived_from edge cannot be a self-loop")

    from_node = await _get_node_or_raise(from_node_id, "from")
    to_node = await _get_node_or_raise(to_node_id, "to")

    from_entity = from_node.entity_type
    to_entity = to_node.entity_type

    if from_entity == "process" or to_entity == "process":
        raise ValueError(
            "derived_from endpoints cannot be process nodes; both endpoints must be entities"
        )

    if from_entity not in _ACCEPTABLE_ENTITY_TYPES:
        raise ValueError(
            f"derived_from source entity_type '{from_entity}' is not acceptable; "
            f"acceptable types are: {', '.join(sorted(_ACCEPTABLE_ENTITY_TYPES))}"
        )

    if to_entity not in _ACCEPTABLE_ENTITY_TYPES:
        raise ValueError(
            f"derived_from target entity_type '{to_entity}' is not acceptable; "
            f"acceptable types are: {', '.join(sorted(_ACCEPTABLE_ENTITY_TYPES))}"
        )

    if is_generic_consumable(to_node_id):
        raise ValueError(
            f"derived_from target '{to_node_id}' is a generic consumable and cannot be a material source"
        )

    if await _existing_derived_from(from_node_id, to_node_id):
        raise ValueError(
            f"derived_from edge from '{from_node_id}' to '{to_node_id}' already exists"
        )

    if not skip_cycle_check and await _would_create_cycle(from_node_id, to_node_id):
        raise ValueError(
            f"derived_from edge from '{from_node_id}' to '{to_node_id}' would create a cycle"
        )
