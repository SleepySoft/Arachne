"""Tests for the arachne-flow engine: parser, compiler, and read-only engine."""

from __future__ import annotations

from pathlib import Path

import pytest
import pytest_asyncio

from app.engines.arachne_flow.engine import ArachneFlowEngine
from app.engines.arachne_flow.parser import FlowParseError, FlowValidationError, parse_flow_file
from app.engines.arachne_flow.schemas import ActionType, FlowDocument, FlowTriple, ResourceType
from app.engines.arachne_flow import storage
from app.services.engine_registry import get_engine, register_engine


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


# ---------------------------------------------------------------------------
# Parser tests (synchronous)
# ---------------------------------------------------------------------------


def test_parse_smartphone_flow():
    parsed = parse_flow_file(FLOW_DIR / "smartphone.yaml")
    assert parsed.schema_version == "arachne-flow/v0.1"
    assert parsed.flow_id == "smartphone"
    assert parsed.root_product == "smartphone"
    assert len(parsed.resources) > 0
    assert len(parsed.actions) > 0
    # Product flow now only declares its own integration step.
    assert "electronics_system_integration" in parsed.methods
    assert "act_electronics_system_integration" in parsed.actions
    assert parsed.includes == [
        "semiconductor_chip_manufacturing.yaml",
        "printed_circuit_board_fabrication.yaml",
    ]


def test_parse_chip_manufacturing_flow():
    parsed = parse_flow_file(FLOW_DIR / "semiconductor_chip_manufacturing.yaml")
    assert parsed.schema_version == "arachne-flow/v0.1"
    assert parsed.flow_id == "semiconductor_chip_manufacturing"
    assert parsed.root_product == "chip"
    assert len(parsed.resources) > 0
    assert len(parsed.actions) > 0
    # Chip manufacturing now starts from wafer (produced by wafer_fabrication_processes).
    assert "wafer_dicing" in parsed.methods
    assert "chip_testing" in parsed.methods
    assert "chip_packaging_and_testing" in parsed.methods
    assert parsed.includes == ["wafer_fabrication_processes.yaml"]


def test_parse_chip_design_flow():
    parsed = parse_flow_file(FLOW_DIR / "chip_design.yaml")
    assert parsed.schema_version == "arachne-flow/v0.1"
    assert parsed.flow_id == "chip_design"
    assert parsed.root_product == "chip_design_output"
    assert "chip_design" in parsed.methods
    assert "chip_design" not in parsed.resources
    assert "chip_design" not in parsed.actions
    assert "chip_design_output" in parsed.locals


def test_parse_photovoltaic_inverter_flow():
    parsed = parse_flow_file(FLOW_DIR / "photovoltaic_inverter.yaml")
    assert parsed.flow_id == "photovoltaic_inverter"
    assert len(parsed.resources) == 2
    assert len(parsed.actions) == 1
    assert len(parsed.methods) == 1
    assert len(parsed.triples) == 3


def test_parse_all_flows_are_valid():
    """All generated semiconductor flows must parse without structural errors."""
    for path in sorted(FLOW_DIR.glob("*.yaml")):
        if path.name == "manifest.yaml":
            continue
        parsed = parse_flow_file(path)
        assert parsed.triples


def test_parse_rejects_cycle():
    from app.engines.arachne_flow.parser import _normalize_and_validate
    from app.engines.arachne_flow.schemas import ParsedFlow

    parsed = ParsedFlow(
        schema_version="arachne-flow/v0.1",
        title="cycle",
        root_product="a",
        flow_id="cycle_test",
        triples=[],
    )
    parsed.triples = [
        FlowTriple(source="a", predicate="feedstock", target="act1"),
        FlowTriple(source="act1", predicate="primary_result", target="b"),
        FlowTriple(source="b", predicate="feedstock", target="act2"),
        FlowTriple(source="act2", predicate="primary_result", target="a"),
    ]
    with pytest.raises(FlowValidationError, match="cycle detected"):
        _normalize_and_validate(parsed)


def test_parse_rejects_disconnected_graph():
    from app.engines.arachne_flow.parser import _normalize_and_validate
    from app.engines.arachne_flow.schemas import ParsedFlow

    parsed = ParsedFlow(
        schema_version="arachne-flow/v0.1",
        title="disconnected",
        flow_id="disconnected_test",
        triples=[],
    )
    parsed.triples = [
        FlowTriple(source="a", predicate="feedstock", target="act1"),
        FlowTriple(source="act1", predicate="primary_result", target="b"),
        FlowTriple(source="c", predicate="feedstock", target="act2"),
        FlowTriple(source="act2", predicate="primary_result", target="d"),
    ]
    with pytest.raises(FlowValidationError, match="not a single connected graph"):
        _normalize_and_validate(parsed)


# ---------------------------------------------------------------------------
# Compiler / storage tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_compile_and_read_photovoltaic_flow():
    flow_id = "photovoltaic_inverter"
    parsed = parse_flow_file(FLOW_DIR / f"{flow_id}.yaml")

    await storage.clear_flow(flow_id)
    counts = await storage.compile_parsed_flow(parsed, clear_existing=True)

    assert counts["resources"] == 2
    assert counts["actions"] == 1
    assert counts["methods"] == 1
    assert counts["edges"] == 3
    assert counts["dual"] == 0

    resource = await storage.get_flow_node("photovoltaic_inverter")
    assert resource is not None
    assert resource.entity_type == "arachne_flow:resource"

    action = await storage.get_flow_node(storage.namespaced_action_id(flow_id, "act_integrate_photovoltaic_inverter"))
    assert action is not None
    assert action.entity_type == "arachne_flow:action"

    method = await storage.get_flow_node("integration_of_photovoltaic_inverter")
    assert method is not None
    assert method.entity_type == "arachne_flow:method"

    edges, total = await storage.list_flow_edges(from_node="power_semiconductor")
    assert total == 1
    assert edges[0].edge_type == "feedstock"

    await storage.clear_flow(flow_id)


@pytest.mark.asyncio(loop_scope="session")
async def test_compile_smartphone_flow():
    flow_id = "smartphone"
    parsed = parse_flow_file(FLOW_DIR / f"{flow_id}.yaml")

    await storage.clear_flow(flow_id)
    counts = await storage.compile_parsed_flow(parsed, clear_existing=True)
    assert counts["resources"] > 0
    assert counts["actions"] > 0
    assert counts["dual"] == 0

    stats = await storage.get_flow_stats()
    expected_nodes = counts["resources"] + counts["actions"] + counts["methods"] - counts["dual"]
    assert stats.total_nodes == expected_nodes
    assert stats.total_edges == counts["edges"]
    assert "arachne_flow" in stats.edge_namespace_distribution

    await storage.clear_flow(flow_id)


# ---------------------------------------------------------------------------
# Engine tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_engine_registered():
    register_engine(ArachneFlowEngine())
    engine = get_engine("arachne_flow")
    assert isinstance(engine, ArachneFlowEngine)
    assert engine.name == "arachne_flow"
    assert not engine.supports_write


@pytest.mark.asyncio(loop_scope="session")
async def test_engine_subgraph():
    flow_id = "photovoltaic_inverter"
    parsed = parse_flow_file(FLOW_DIR / f"{flow_id}.yaml")
    await storage.clear_flow(flow_id)
    await storage.compile_parsed_flow(parsed, clear_existing=True)

    engine = ArachneFlowEngine()
    subgraph = await engine.get_subgraph("photovoltaic_inverter", depth=2)
    assert subgraph.center_node_id == "photovoltaic_inverter"
    assert any(n.node_id == "photovoltaic_inverter" for n in subgraph.nodes)

    await storage.clear_flow(flow_id)


@pytest.mark.asyncio(loop_scope="session")
async def test_flow_subgraph_filtered_by_flow_id():
    """Per-flow subgraph must not pull in other flows' occurrences via shared nodes.

    smartphone and personal_computer both use shared resources like ``chip``
    and ``pcb_board`` but have their own integration actions. Filtering by
    flow_id=smartphone must exclude personal_computer's actions.
    """
    for fid in ("smartphone", "personal_computer"):
        parsed = parse_flow_file(FLOW_DIR / f"{fid}.yaml")
        await storage.compile_parsed_flow(parsed, clear_existing=True)

    try:
        nodes, edges = await storage.get_flow_subgraph("smartphone", 3, flow_id="smartphone")
        node_ids = {n.node_id for n in nodes}
        edge_flows = {(e.properties or {}).get("flow_id") for e in edges}

        # 只包含 smartphone 自己的边
        assert edge_flows == {"smartphone"}
        # 不包含其它流程的动作节点
        assert not any(nid.startswith("personal_computer:") for nid in node_ids)
        # smartphone 自己的系统集成动作仍在
        assert "smartphone:act_electronics_system_integration" in node_ids
        # 共享资源节点仍然出现
        assert "chip" in node_ids
        assert "pcb_board" in node_ids

        # 不过滤时（生态视角）应包含其它流程的动作
        nodes_all, _ = await storage.get_flow_subgraph("smartphone", 3)
        node_ids_all = {n.node_id for n in nodes_all}
        assert any(nid.startswith("personal_computer:") for nid in node_ids_all)
    finally:
        await storage.clear_flow("smartphone")
        await storage.clear_flow("personal_computer")


@pytest.mark.asyncio(loop_scope="session")
async def test_flow_file_graph_returns_exact_file_content():
    """Per-file view must return exactly the triples declared by the files."""
    parsed = parse_flow_file(FLOW_DIR / "smartphone.yaml")
    await storage.compile_parsed_flow(parsed, clear_existing=True)

    try:
        nodes, edges = await storage.get_flow_file_graph(["smartphone"])
        edge_flows = {(e.properties or {}).get("flow_id") for e in edges}
        assert edge_flows == {"smartphone"}
        # 文件声明的全部三元组都在
        assert len(edges) == len(parsed.triples)
        node_ids = {n.node_id for n in nodes}
        # 只包含 smartphone 自己声明的节点
        assert "chip" in node_ids
        assert "pcb_board" in node_ids
        assert "lpddr5" in node_ids
        assert "smartphone:act_electronics_system_integration" in node_ids
        assert "electronics_system_integration" in node_ids
        # 不包含其它流程的边或节点
        assert not any(nid.startswith("personal_computer:") for nid in node_ids)
        assert "wafer" not in node_ids
    finally:
        await storage.clear_flow("smartphone")


@pytest.mark.asyncio(loop_scope="session")
async def test_merged_flow_graph_merges_actions_and_edges():
    """Merged full view: cross-flow same-method actions collapse; parallels aggregate."""
    for fid in ("smartphone", "personal_computer"):
        parsed = parse_flow_file(FLOW_DIR / f"{fid}.yaml")
        await storage.compile_parsed_flow(parsed, clear_existing=True)

    try:
        nodes, edges = await storage.get_merged_flow_graph()
        action_nodes = [n for n in nodes if n.entity_type == "arachne_flow:action"]
        action_ids = {n.node_id for n in action_nodes}

        # 两个流程的系统集成动作合并为一个 merged_action 节点
        assert storage.merged_action_id("electronics_system_integration") in action_ids
        assert not any(nid.endswith(":act_electronics_system_integration") for nid in action_ids)

        merged_integration = next(
            n for n in action_nodes if n.node_id == storage.merged_action_id("electronics_system_integration")
        )
        flow_ids = set(merged_integration.properties.get("flow_ids") or [])
        assert {"smartphone", "personal_computer"} <= flow_ids
        assert merged_integration.label

        # 平行边聚合：pcb_board -> merged_integration 的 feedstock 聚成一条且 count >= 2
        agg = [
            e
            for e in edges
            if e.from_node == "pcb_board"
            and e.to_node == storage.merged_action_id("electronics_system_integration")
            and e.edge_type == "feedstock"
        ]
        assert len(agg) == 1
        assert int(agg[0].properties.get("count") or 0) >= 2
        assert {"smartphone", "personal_computer"} <= set(
            agg[0].properties.get("flow_ids") or []
        )
    finally:
        await storage.clear_flow("smartphone")
        await storage.clear_flow("personal_computer")


@pytest.mark.asyncio(loop_scope="session")
async def test_engine_neighbors():
    flow_id = "photovoltaic_inverter"
    parsed = parse_flow_file(FLOW_DIR / f"{flow_id}.yaml")
    await storage.clear_flow(flow_id)
    await storage.compile_parsed_flow(parsed, clear_existing=True)

    engine = ArachneFlowEngine()
    nodes, edges = await engine.get_neighbors("photovoltaic_inverter")
    assert len(edges) == 1
    assert edges[0].to_node == "photovoltaic_inverter"

    await storage.clear_flow(flow_id)


@pytest.mark.asyncio(loop_scope="session")
async def test_engine_read_only_raises():
    engine = ArachneFlowEngine()
    with pytest.raises(Exception):  # ReadOnlyEngineError
        await engine.create_node(None)


@pytest.mark.asyncio(loop_scope="session")
async def test_generic_node_and_edge_routes_support_flow_engine():
    """Regression: /nodes/{id} and /edges/{id} must work with ?engine=arachne_flow.

    The generic GET routes must not force legacy response models onto flow
    nodes/edges, otherwise the shared detail sidebars cannot resolve flow
    endpoints.
    """
    import httpx
    from httpx import ASGITransport

    from app.engines.legacy.engine import LegacyEngine
    from app.main import app

    flow_id = "photovoltaic_inverter"
    parsed = parse_flow_file(FLOW_DIR / f"{flow_id}.yaml")
    await storage.clear_flow(flow_id)
    await storage.compile_parsed_flow(parsed, clear_existing=True)

    register_engine(LegacyEngine())
    register_engine(ArachneFlowEngine())

    try:
        async with httpx.AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Flow action node (namespaced id)
            action_id = storage.namespaced_action_id(flow_id, "act_integrate_photovoltaic_inverter")
            r = await client.get(f"/api/v1/nodes/{action_id}", params={"engine": "arachne_flow"})
            assert r.status_code == 200, r.text
            data = r.json()
            assert data["node_id"] == action_id
            assert data["entity_type"] == "arachne_flow:action"

            # Flow edge
            edges, total = await storage.list_flow_edges()
            assert total > 0
            edge_id = edges[0].edge_id
            r = await client.get(f"/api/v1/edges/{edge_id}", params={"engine": "arachne_flow"})
            assert r.status_code == 200, r.text
            assert r.json()["edge_id"] == edge_id

            # Flow node list
            r = await client.get("/api/v1/nodes", params={"engine": "arachne_flow", "page_size": 5})
            assert r.status_code == 200, r.text
            assert r.json()["total"] > 0

            # Legacy endpoints still return the legacy shape
            r = await client.get("/api/v1/nodes", params={"page_size": 1})
            assert r.status_code == 200, r.text
    finally:
        await storage.clear_flow(flow_id)


# ---------------------------------------------------------------------------
# Preview endpoint tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_flow_preview_valid_yaml():
    import httpx
    from httpx import ASGITransport

    from app.engines.legacy.engine import LegacyEngine
    from app.main import app

    register_engine(LegacyEngine())
    register_engine(ArachneFlowEngine())

    content = """
schema: arachne-flow/v0.1
title: 'Preview test'
root_product: widget
include: []
local: {}
edges:
- [steel, feedstock, act_make_widget]
- [act_make_widget, ref, widget_making]
- [act_make_widget, primary_result, widget]
"""
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post("/api/v1/flows/preview", json={"content": content})
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["valid"] is True
        assert len(data["nodes"]) == 4
        assert len(data["edges"]) == 3
        node_ids = {n["node_id"] for n in data["nodes"]}
        assert "steel" in node_ids
        assert "widget" in node_ids
        assert "preview:act_make_widget" in node_ids
        assert "widget_making" in node_ids


@pytest.mark.asyncio(loop_scope="session")
async def test_flow_preview_syntax_error_keeps_valid_false():
    import httpx
    from httpx import ASGITransport

    from app.engines.legacy.engine import LegacyEngine
    from app.main import app

    register_engine(LegacyEngine())
    register_engine(ArachneFlowEngine())

    content = "schema: [unclosed"
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post("/api/v1/flows/preview", json={"content": content})
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["valid"] is False
        assert data["errors"]


@pytest.mark.asyncio(loop_scope="session")
async def test_flow_preview_resolves_includes():
    import httpx
    from httpx import ASGITransport

    from app.engines.legacy.engine import LegacyEngine
    from app.main import app

    register_engine(LegacyEngine())
    register_engine(ArachneFlowEngine())

    content = """
schema: arachne-flow/v0.1
title: 'Preview include test'
root_product: smartphone
include:
- semiconductor_chip_manufacturing.yaml
- printed_circuit_board_fabrication.yaml
local: {}
edges:
- [chip, feedstock, act_electronics_system_integration]
- [act_electronics_system_integration, ref, electronics_system_integration]
- [act_electronics_system_integration, primary_result, smartphone]
"""
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post("/api/v1/flows/preview", json={"content": content})
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["valid"] is True
        node_ids = {n["node_id"] for n in data["nodes"]}
        # Included shared nodes should be present
        assert "wafer" in node_ids
        assert "chip" in node_ids
        assert "pcb_board" in node_ids


@pytest.mark.asyncio(loop_scope="session")
async def test_flow_preview_does_not_write_to_db():
    from app.database_flow import get_flow_async_driver
    from app.engines.arachne_flow.preview import preview_flow_graph

    content = """
schema: arachne-flow/v0.1
title: 'Preview no-write test'
root_product: widget
include: []
local: {}
edges:
- [steel, feedstock, act_make_widget]
- [act_make_widget, ref, widget_making]
- [act_make_widget, primary_result, widget]
"""
    driver = get_flow_async_driver()
    async with driver.session() as session:
        before = await session.run("MATCH (n:ArachneFlowNode) RETURN count(n) AS c")
        before_count = (await before.single())["c"]

    nodes, edges, errors, warnings = await preview_flow_graph(content, flow_id="preview_nowrite")
    assert not errors
    assert len(nodes) == 4
    assert len(edges) == 3

    async with driver.session() as session:
        after = await session.run("MATCH (n:ArachneFlowNode) RETURN count(n) AS c")
        after_count = (await after.single())["c"]
    assert after_count == before_count
