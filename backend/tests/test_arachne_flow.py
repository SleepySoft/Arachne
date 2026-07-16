"""Tests for the arachne-flow engine: parser, compiler, and read-only engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.engines.arachne_flow.engine import ArachneFlowEngine
from app.engines.arachne_flow.parser import FlowParseError, FlowValidationError, parse_flow_file
from app.engines.arachne_flow.schemas import ActionType, FlowDocument, FlowTriple, ResourceType
from app.engines.arachne_flow import storage
from app.services.engine_registry import get_engine, register_engine


FLOW_DIR = Path(__file__).resolve().parents[2] / "data" / "flows" / "semiconductor"


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


def test_parse_smartphone_flow():
    parsed = parse_flow_file(FLOW_DIR / "smartphone.yaml")
    assert parsed.schema_version == "arachne-flow/v0.1"
    assert parsed.flow_id == "smartphone"
    assert parsed.root_product == "smartphone"
    assert len(parsed.resources) > 0
    assert len(parsed.actions) > 0
    assert len(parsed.triples) == 39  # from manifest

    # Check well-known nodes were classified correctly.
    assert "smartphone" in parsed.resources
    assert "wafer_manufacturing" in parsed.actions
    assert "electronics_system_integration" in parsed.actions
    # chip_design is used both as an action and as an information input,
    # so it appears in both dictionaries (dual-role node).
    assert "chip_design" in parsed.resources
    assert "chip_design" in parsed.actions


def test_parse_photovoltaic_inverter_flow():
    parsed = parse_flow_file(FLOW_DIR / "photovoltaic_inverter.yaml")
    assert parsed.flow_id == "photovoltaic_inverter"
    assert len(parsed.resources) == 2
    assert len(parsed.actions) == 1
    assert len(parsed.triples) == 2


def test_parse_rejects_cycle():
    doc = FlowDocument(
        title="cycle",
        root_product="a",
        edges=[
            [["a", "feedstock", "act1"], ["act1", "primary_result", "b"]],
            [["b", "feedstock", "act2"], ["act2", "primary_result", "a"]],
        ],
    )
    # pydantic model is not a file; exercise parser internals indirectly by
    # building from raw YAML would require temp file. Use internal validation.
    from app.engines.arachne_flow.parser import _normalize_and_validate
    from app.engines.arachne_flow.schemas import ParsedFlow

    parsed = ParsedFlow(
        schema="arachne-flow/v0.1",
        title="cycle",
        root_product="a",
        flow_id="cycle_test",
        triples=[],
    )
    # Manually add triples
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
        schema="arachne-flow/v0.1",
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
    assert counts["edges"] == 2

    # Verify nodes exist
    resource = await storage.get_flow_node("photovoltaic_inverter")
    assert resource is not None
    assert resource.entity_type == "arachne_flow:resource"

    action = await storage.get_flow_node(storage.namespaced_action_id(flow_id, "integrate_photovoltaic_inverter"))
    assert action is not None
    assert action.entity_type == "arachne_flow:action"

    # Verify an edge exists
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
    assert counts["edges"] == 39

    # Stats (dual-role nodes are counted once in Neo4j but in both dicts)
    stats = await storage.get_flow_stats()
    expected_nodes = counts["resources"] + counts["actions"] - counts["dual"]
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
