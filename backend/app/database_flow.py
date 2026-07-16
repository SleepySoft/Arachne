"""Async Neo4j driver for the optional arachne-flow engine instance."""

import asyncio

from neo4j import AsyncGraphDatabase

from app.config import get_settings

_settings = get_settings()

_flow_async_driver = None
_flow_driver_loop: asyncio.AbstractEventLoop | None = None


def get_flow_async_driver():
    """Return the shared arachne-flow Neo4j async driver.

    Defaults to the same URI as the main Neo4j instance if NEO4J_FLOW_URI is not
    set, but keeps a separate driver object so it can be pointed at a second
    instance in the future. The driver is recreated if the running event loop
    changes (important for pytest-asyncio).
    """
    global _flow_async_driver, _flow_driver_loop
    try:
        current_loop = asyncio.get_running_loop()
    except RuntimeError:
        current_loop = None

    if _flow_async_driver is not None:
        stale = (
            current_loop is not _flow_driver_loop
            or (current_loop is not None and current_loop.is_closed())
        )
        if stale:
            if current_loop is not None:
                try:
                    current_loop.create_task(_flow_async_driver.close())
                except Exception:
                    pass
            _flow_async_driver = None
            _flow_driver_loop = None

    if _flow_async_driver is None:
        _flow_async_driver = AsyncGraphDatabase.driver(
            _settings.NEO4J_FLOW_URI,
            auth=(_settings.NEO4J_FLOW_USER, _settings.NEO4J_FLOW_PASSWORD),
            max_connection_lifetime=1800,
            connection_acquisition_timeout=30,
            max_connection_pool_size=50,
        )
        _flow_driver_loop = current_loop
    return _flow_async_driver


async def close_flow_async_driver():
    global _flow_async_driver, _flow_driver_loop
    if _flow_async_driver is not None:
        await _flow_async_driver.close()
        _flow_async_driver = None
        _flow_driver_loop = None


async def init_flow_db():
    """Create constraints/indexes for the arachne-flow graph."""
    try:
        driver = get_flow_async_driver()
        async with driver.session() as session:
            await session.run(
                """
                CREATE CONSTRAINT arachne_flow_node_id_unique IF NOT EXISTS
                FOR (n:ArachneFlowNode) REQUIRE n.node_id IS UNIQUE
                """
            )
            await session.run(
                """
                CREATE CONSTRAINT arachne_flow_edge_id_unique IF NOT EXISTS
                FOR ()-[r:ARACHNE_FLOW]-() REQUIRE r.edge_id IS UNIQUE
                """
            )
    except Exception:
        # Flow Neo4j not available; engine operations will surface errors later.
        pass
