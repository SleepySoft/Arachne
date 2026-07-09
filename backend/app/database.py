import asyncio

from neo4j import AsyncGraphDatabase

from app.config import get_settings

_settings = get_settings()

_async_driver = None
_driver_loop: asyncio.AbstractEventLoop | None = None


def get_async_driver():
    """Return the shared Neo4j async driver, recreating it if the event loop changes.

    Async drivers keep internal connections bound to the loop that runs them.
    In long-lived apps this is fine, but in test suites where each test may run
    on a fresh event loop we must avoid returning a driver tied to a closed loop.
    """
    global _async_driver, _driver_loop
    try:
        current_loop = asyncio.get_running_loop()
    except RuntimeError:
        current_loop = None

    if _async_driver is not None:
        stale = (
            current_loop is not _driver_loop
            or (current_loop is not None and current_loop.is_closed())
        )
        if stale:
            # Best-effort close of the stale driver without blocking the caller.
            if current_loop is not None:
                try:
                    current_loop.create_task(_async_driver.close())
                except Exception:
                    pass
            _async_driver = None
            _driver_loop = None

    if _async_driver is None:
        _async_driver = AsyncGraphDatabase.driver(
            _settings.NEO4J_URI,
            auth=(_settings.NEO4J_USER, _settings.NEO4J_PASSWORD),
            max_connection_lifetime=1800,
            connection_acquisition_timeout=30,
            max_connection_pool_size=50,
        )
        _driver_loop = current_loop
    return _async_driver


async def close_async_driver():
    global _async_driver, _driver_loop
    if _async_driver is not None:
        await _async_driver.close()
        _async_driver = None
        _driver_loop = None


async def init_db():
    try:
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
            # Node metadata (canonical_name_zh, etc.) now lives in PostgreSQL.
            # Neo4j only keeps the node_id + label for relationship storage.
    except Exception:
        # Neo4j not available, using memory storage fallback
        pass
