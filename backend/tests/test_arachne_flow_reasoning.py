"""Tests for arachne-flow reasoning adapter and tasks."""

from __future__ import annotations

from pathlib import Path

import pytest
import pytest_asyncio

from app.engines.arachne_flow import storage
from app.engines.arachne_flow.parser import parse_flow_file
from app.reasoning.arachne_flow_adapter import (
    expand_by_method_ref,
    fetch_arachne_flow_paths,
    validate_arachne_flow_sources,
)
from app.reasoning.engine import execute_reasoning_task
from app.reasoning.schemas import (
    OutputType,
    ReasoningConstraints,
    ReasoningTask,
    ResultStatus,
    TaskType,
    TraversalDirection,
)

FLOW_DIR = Path(__file__).resolve().parents[2] / "data" / "flows" / "semiconductor"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _wipe_flow_test_data():
    """Ensure arachne-flow tests start from an empty flow graph."""
    from app.database_flow import get_flow_async_driver

    driver = get_flow_async_driver()
    async with driver.session() as session:
        await session.run("MATCH ()-[r:ARACHNE_FLOW]->() DELETE r")
        await session.run("MATCH (n:ArachneFlowNode) DELETE n")
    yield


@pytest.mark.asyncio(loop_scope="session")
async def test_validate_arachne_flow_sources():
    for fid in ("smartphone", "semiconductor_chip_manufacturing"):
        parsed = parse_flow_file(FLOW_DIR / f"{fid}.yaml")
        await storage.compile_parsed_flow(parsed, clear_existing=True)

    try:
        existing, missing = await validate_arachne_flow_sources(
            ["chip", "pcb_board", "nonexistent_node"]
        )
        assert "chip" in existing
        assert "pcb_board" in existing
        assert "nonexistent_node" in missing
    finally:
        await storage.clear_flow("smartphone")
        await storage.clear_flow("semiconductor_chip_manufacturing")


@pytest.mark.asyncio(loop_scope="session")
async def test_fetch_arachne_flow_paths():
    parsed = parse_flow_file(FLOW_DIR / "semiconductor_chip_manufacturing.yaml")
    await storage.compile_parsed_flow(parsed, clear_existing=True)

    try:
        paths = await fetch_arachne_flow_paths(
            "chip", max_depth=2, direction="backward", limit=10
        )
        assert len(paths) > 0
        assert any(
            "act_chip_packaging_and_testing" in nid
            for p in paths
            for nid in p["node_ids"]
        )
    finally:
        await storage.clear_flow("semiconductor_chip_manufacturing")


@pytest.mark.asyncio(loop_scope="session")
async def test_expand_by_method_ref():
    parsed = parse_flow_file(FLOW_DIR / "semiconductor_chip_manufacturing.yaml")
    await storage.compile_parsed_flow(parsed, clear_existing=True)

    try:
        expanded = await expand_by_method_ref(
            ["semiconductor_chip_manufacturing:act_chip_packaging_and_testing"],
            direction="both",
        )
        assert "chip_packaging_and_testing" in expanded

        expanded = await expand_by_method_ref(["chip_packaging_and_testing"], direction="both")
        assert any("act_chip_packaging_and_testing" in nid for nid in expanded)
    finally:
        await storage.clear_flow("semiconductor_chip_manufacturing")


@pytest.mark.asyncio(loop_scope="session")
async def test_arachne_flow_association_task():
    parsed = parse_flow_file(FLOW_DIR / "semiconductor_chip_manufacturing.yaml")
    await storage.compile_parsed_flow(parsed, clear_existing=True)

    try:
        task = ReasoningTask(
            task_id="test_af_assoc_001",
            task_type=TaskType.ASSOCIATION,
            source_nodes=["chip"],
            parameters={},
            constraints=ReasoningConstraints(
                max_depth=2, max_paths=20, traversal_direction=TraversalDirection.BOTH
            ),
            requested_outputs=[OutputType.PATHS, OutputType.TEMPORARY_GRAPH],
            engine="arachne_flow",
        )
        result = await execute_reasoning_task(task)
        assert result.status == ResultStatus.SUCCESS
        paths = result.result_payload.get("paths", [])
        assert len(paths) > 0
        temp_graph = result.result_payload.get("temporary_graph", {})
        assert len(temp_graph.get("nodes", [])) > 0
        assert len(temp_graph.get("edges", [])) > 0
    finally:
        await storage.clear_flow("semiconductor_chip_manufacturing")


@pytest.mark.asyncio(loop_scope="session")
async def test_arachne_flow_association_missing_source():
    task = ReasoningTask(
        task_id="test_af_assoc_missing",
        task_type=TaskType.ASSOCIATION,
        source_nodes=["nonexistent_node"],
        parameters={},
        constraints=ReasoningConstraints(max_depth=2, max_paths=10),
        requested_outputs=[OutputType.PATHS],
        engine="arachne_flow",
    )
    result = await execute_reasoning_task(task)
    assert result.status == ResultStatus.NO_RESULT
    assert result.diagnostics.dangling_reference_count > 0
