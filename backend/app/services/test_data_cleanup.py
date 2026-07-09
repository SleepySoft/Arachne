"""
Test-data cleanup service.

Scans Neo4j and PostgreSQL for entities marked with `is_test = true` and deletes
them in a safe order. Dry-run mode returns counts without making changes.
"""

from __future__ import annotations

from typing import Any, Dict

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool


async def cleanup_test_data(dry_run: bool = False) -> Dict[str, Any]:
    """Delete all test data across Neo4j and PostgreSQL.

    Returns a dict with counts per store/table. If ``dry_run`` is True, counts
    are computed but no deletions are performed.
    """
    result: Dict[str, Any] = {
        "dry_run": dry_run,
        "neo4j": {},
        "postgres": {},
    }

    # ------------------------------------------------------------------
    # Neo4j: delete test edges first, then test nodes (relationships cascade)
    # ------------------------------------------------------------------
    driver = get_async_driver()

    # IndustrialNode is_test metadata is now in PostgreSQL.
    pool = await get_postgres_pool()
    test_node_ids: list[str] = []
    if pool is not None:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT node_id FROM industrial_nodes WHERE is_test = true"
            )
            test_node_ids = [r["node_id"] for r in rows]

    async with driver.session() as session:
        edge_count_result = await session.run(
            """
            MATCH ()-[r:INDUSTRIAL_FLOW|ONTOLOGY]->()
            WHERE r.is_test = true
            RETURN count(r) AS total
            """
        )
        edge_count = (await edge_count_result.single())["total"]
        result["neo4j"]["industrial_edges"] = edge_count

        node_count = len(test_node_ids)
        result["neo4j"]["industrial_nodes"] = node_count

        # Factual graph nodes/edges
        factual_edge_count_result = await session.run(
            """
            MATCH ()-[r]->()
            WHERE r.is_test = true
            RETURN count(r) AS total
            """
        )
        factual_edge_count = (await factual_edge_count_result.single())["total"]
        result["neo4j"]["factual_edges"] = factual_edge_count

        factual_node_count_result = await session.run(
            """
            MATCH (n)
            WHERE (n:Person OR n:Company) AND n.is_test = true
            RETURN count(n) AS total
            """
        )
        factual_node_count = (await factual_node_count_result.single())["total"]
        result["neo4j"]["factual_nodes"] = factual_node_count

        if not dry_run:
            await session.run(
                """
                MATCH ()-[r:INDUSTRIAL_FLOW|ONTOLOGY]->()
                WHERE r.is_test = true
                DELETE r
                """
            )
            if test_node_ids:
                await session.run(
                    """
                    MATCH (n:IndustrialNode)
                    WHERE n.node_id IN $node_ids
                    DETACH DELETE n
                    """,
                    node_ids=test_node_ids,
                )
            await session.run(
                """
                MATCH ()-[r]->()
                WHERE r.is_test = true
                DELETE r
                """
            )
            await session.run(
                """
                MATCH (n)
                WHERE (n:Person OR n:Company) AND n.is_test = true
                DETACH DELETE n
                """
            )

    # ------------------------------------------------------------------
    # PostgreSQL: delete child rows before parent rows
    # ------------------------------------------------------------------
    pool = await get_postgres_pool()
    if pool is None:
        result["postgres"]["available"] = False
        return result

    result["postgres"]["available"] = True

    tables_in_order = [
        ("company_node_exposures", "exposure_id"),
        ("industry_node_mappings", "mapping_id"),
        ("factual_relations", "relation_id"),
        ("industrial_nodes", "node_id"),
        ("companies", "company_id"),
        ("industries", "industry_id"),
        ("persons", "person_id"),
    ]

    async with pool.acquire() as conn:
        for table, id_col in tables_in_order:
            count_row = await conn.fetchrow(
                f"SELECT COUNT(*) AS total FROM {table} WHERE is_test = true"
            )
            count = count_row["total"] if count_row else 0
            result["postgres"][table] = {"count": count, "id_column": id_col}

            if not dry_run and count > 0:
                await conn.execute(
                    f"DELETE FROM {table} WHERE is_test = true"
                )

    return result
