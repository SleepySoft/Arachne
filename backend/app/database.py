from neo4j import AsyncGraphDatabase

from app.config import get_settings

_settings = get_settings()

_async_driver = None


def get_async_driver():
    global _async_driver
    if _async_driver is None:
        _async_driver = AsyncGraphDatabase.driver(
            _settings.NEO4J_URI,
            auth=(_settings.NEO4J_USER, _settings.NEO4J_PASSWORD),
        )
    return _async_driver


async def close_async_driver():
    global _async_driver
    if _async_driver is not None:
        await _async_driver.close()
        _async_driver = None


async def init_db():
    driver = get_async_driver()
    async with driver.session() as session:
        # Constraints and indexes
        await session.run(
            """
            CREATE CONSTRAINT node_id_unique IF NOT EXISTS
            FOR (n:IndustrialNode) REQUIRE n.node_id IS UNIQUE
            """
        )
        await session.run(
            """
            CREATE CONSTRAINT edge_id_unique IF NOT EXISTS
            FOR ()-[r:INDUSTRIAL_FLOW]-() REQUIRE r.edge_id IS UNIQUE
            """
        )
        await session.run(
            """
            CREATE CONSTRAINT edge_id_unique_onto IF NOT EXISTS
            FOR ()-[r:ONTOLOGY]-() REQUIRE r.edge_id IS UNIQUE
            """
        )
        await session.run(
            """
            CREATE INDEX node_name_zh IF NOT EXISTS
            FOR (n:IndustrialNode) ON (n.canonical_name_zh)
            """
        )
