"""Tests for the graph reasoning engine tasks.

These tests create `is_test=True` entities in Neo4j/PostgreSQL and clean them up
after each test via `cleanup_test_data()`.
"""

from __future__ import annotations

import uuid

import pytest
import pytest_asyncio

from app.models.schemas import (
    Confidence,
    EntityType,
    Evidence,
    IndustrialFlowEdge,
    IndustrialFlowType,
    IndustrialNode,
    OntologyEdge,
    OntologyType,
    RecordStatus,
)
from app.reasoning.schemas import OutputType, ReasoningConstraints, ReasoningTask, TaskType
from app.reasoning.tasks.association import run_association
from app.reasoning.tasks.bottleneck_detection import run_bottleneck_detection
from app.reasoning.tasks.candidate_discovery import run_candidate_discovery
from app.reasoning.tasks.cross_graph_context import run_cross_graph_context
from app.reasoning.tasks.impact_propagation import run_impact_propagation
from app.reasoning.tasks.substitution_search import run_substitution_search
from app.database import close_async_driver
from app.services import company_storage, neo4j_storage, test_data_cleanup
from app.models.company_schema import Company, CompanyNodeExposure, CompanyActivityType, CompanyType


pytestmark = pytest.mark.asyncio(loop_scope="session")


def _unique(prefix: str) -> str:
    return f"{prefix}_{str(uuid.uuid4())[:8]}"


async def _cleanup():
    await test_data_cleanup.cleanup_test_data(dry_run=False)


async def _create_test_node(node_id: str, name: str, entity_type: EntityType):
    node = IndustrialNode(
        node_id=node_id,
        canonical_name_zh=name,
        definition="test node",
        entity_type=entity_type,
        evidence=[Evidence(source_title="test", quote="test")],
        confidence=Confidence.HIGH,
        status=RecordStatus.ACTIVE,
        is_test=True,
    )
    return await neo4j_storage.create_node(node)


async def _create_test_edge(
    edge_id: str,
    from_node: str,
    to_node: str,
    edge_type: IndustrialFlowType,
):
    edge = IndustrialFlowEdge(
        edge_id=edge_id,
        from_node=from_node,
        to_node=to_node,
        edge_type=edge_type,
        description=f"test {edge_type.value}",
        evidence=[Evidence(source_title="test", quote="test")],
        confidence=Confidence.HIGH,
        is_test=True,
    )
    return await neo4j_storage.create_industrial_flow_edge(edge)


async def _create_test_ontology_edge(
    edge_id: str,
    from_node: str,
    to_node: str,
    edge_type: OntologyType,
):
    edge = OntologyEdge(
        edge_id=edge_id,
        from_node=from_node,
        to_node=to_node,
        edge_type=edge_type,
        description=f"test {edge_type.value}",
        evidence=[Evidence(source_title="test", quote="test")],
        confidence=Confidence.HIGH,
        is_test=True,
    )
    return await neo4j_storage.create_ontology_edge(edge)


def _make_task(task_type: TaskType, source_nodes: list[str], **overrides) -> ReasoningTask:
    return ReasoningTask(
        task_id=f"test_{task_type.value}",
        task_type=task_type,
        source_nodes=source_nodes,
        parameters=overrides.get("parameters", {}),
        constraints=overrides.get(
            "constraints",
            ReasoningConstraints(
                max_depth=3,
                max_paths=50,
                max_nodes=200,
                traversal_direction="forward",
            ),
        ),
        requested_outputs=overrides.get(
            "requested_outputs",
            [OutputType.SUBGRAPH, OutputType.PATHS, OutputType.EVIDENCE_CHAINS],
        ),
    )


@pytest_asyncio.fixture(autouse=True)
async def cleanup_after_test():
    """Cleanup test data after each test."""
    yield
    await _cleanup()
    await close_async_driver()
    from app.database_postgres import close_postgres_pool
    await close_postgres_pool()


async def test_association_with_derived_from_expansion():
    a = _unique("test_mat_a")
    b = _unique("test_mat_b")
    c = _unique("test_part_c")

    await _create_test_node(a, "测试原料A", EntityType.MATERIAL)
    await _create_test_node(b, "测试原料B", EntityType.MATERIAL)
    await _create_test_node(c, "测试部件C", EntityType.PART)
    await _create_test_edge(_unique("e_df"), a, b, IndustrialFlowType.DERIVED_FROM)
    await _create_test_edge(_unique("e_mi"), b, c, IndustrialFlowType.MATERIAL_INPUT)

    task = _make_task(TaskType.ASSOCIATION, [a])
    result = await run_association(task, reasoning_id="test_assoc")

    assert result.status in ("success", "partial")
    paths = result.result_payload.get("paths", {}).get("paths", [])
    sequences = [p["node_sequence"] for p in paths]
    assert any(a in seq and b in seq and c in seq for seq in sequences), f"Expected path through derived_from, got {sequences}"


async def test_association_topology_edges_not_mixed_by_default():
    a = _unique("test_onto_a")
    b = _unique("test_onto_b")
    c = _unique("test_onto_c")

    await _create_test_node(a, "测试原料A", EntityType.MATERIAL)
    await _create_test_node(b, "测试原料B", EntityType.MATERIAL)
    await _create_test_node(c, "测试概念C", EntityType.MATERIAL)
    await _create_test_edge(_unique("e_mi"), a, b, IndustrialFlowType.MATERIAL_INPUT)
    await _create_test_ontology_edge(_unique("e_ont"), a, c, OntologyType.IS_A)

    # Default association should follow the flow edge only, not the ontology edge.
    task = _make_task(TaskType.ASSOCIATION, [a])
    result = await run_association(task, reasoning_id="test_onto_default")
    assert result.status in ("success", "partial")
    subgraph = result.result_payload.get("subgraph", {})
    node_ids = {n["node_id"] for n in subgraph.get("nodes", [])}
    edge_types = {e.get("edge_type") for e in subgraph.get("edges", [])}
    assert a in node_ids
    assert b in node_ids
    assert c not in node_ids, f"Ontology neighbor should not appear without expand_ontology, got {node_ids}"
    assert "is_a" not in edge_types, f"Ontology edges should not be traversed by default, got {edge_types}"

    # With expand_ontology=True the topology neighbor is included as a source expansion.
    task_expand = _make_task(
        TaskType.ASSOCIATION,
        [a],
        parameters={"expand_ontology": True},
    )
    result_expand = await run_association(task_expand, reasoning_id="test_onto_expand")
    assert result_expand.status in ("success", "partial")
    subgraph_expand = result_expand.result_payload.get("subgraph", {})
    node_ids_expand = {n["node_id"] for n in subgraph_expand.get("nodes", [])}
    edge_types_expand = {e.get("edge_type") for e in subgraph_expand.get("edges", [])}
    assert a in node_ids_expand
    assert b in node_ids_expand
    assert c in node_ids_expand, f"Ontology neighbor should appear when expand_ontology=True, got {node_ids_expand}"
    assert "is_a" not in edge_types_expand, f"Ontology edges should still not be returned as flow paths, got {edge_types_expand}"


async def test_association_resolves_alias_of_source():
    alias = _unique("test_alias")
    canonical = _unique("test_canonical")
    downstream = _unique("test_downstream")

    await _create_test_node(alias, "别名节点", EntityType.MATERIAL)
    await _create_test_node(canonical, "规范节点", EntityType.MATERIAL)
    await _create_test_node(downstream, "下游节点", EntityType.PART)
    await _create_test_ontology_edge(
        _unique("e_alias"), alias, canonical, OntologyType.ALIAS_OF
    )
    await _create_test_edge(
        _unique("e_flow"), canonical, downstream, IndustrialFlowType.MATERIAL_INPUT
    )

    # Even without expand_ontology, alias_of sources should be resolved to canonical.
    task = _make_task(TaskType.ASSOCIATION, [alias])
    result = await run_association(task, reasoning_id="test_alias_resolution")
    assert result.status in ("success", "partial")
    subgraph = result.result_payload.get("subgraph", {})
    node_ids = {n["node_id"] for n in subgraph.get("nodes", [])}
    assert canonical in node_ids, "Should resolve alias to canonical node"
    assert downstream in node_ids, "Should traverse flow edges from canonical node"
    assert any(
        "alias" in w.lower() for w in result.diagnostics.warnings
    ), "Expected a warning about alias resolution"


async def test_association_part_of_whole_expansion():
    part = _unique("test_part")
    whole = _unique("test_whole")
    downstream = _unique("test_whole_downstream")

    await _create_test_node(part, "子部件", EntityType.PART)
    await _create_test_node(whole, "整体", EntityType.SYSTEM)
    await _create_test_node(downstream, "整体下游", EntityType.PART)
    await _create_test_ontology_edge(
        _unique("e_part_of"), part, whole, OntologyType.PART_OF
    )
    await _create_test_edge(
        _unique("e_flow"), whole, downstream, IndustrialFlowType.MATERIAL_INPUT
    )

    task = _make_task(
        TaskType.ASSOCIATION,
        [part],
        parameters={"expand_ontology": True},
    )
    result = await run_association(task, reasoning_id="test_part_of_expand")
    assert result.status in ("success", "partial")
    subgraph = result.result_payload.get("subgraph", {})
    node_ids = {n["node_id"] for n in subgraph.get("nodes", [])}
    assert part in node_ids
    assert whole in node_ids, f"Should expand part -> whole via part_of, got {node_ids}"
    assert downstream in node_ids, f"Should traverse flow from whole to downstream, got {node_ids}"
    edge_types = {e.get("edge_type") for e in subgraph.get("edges", [])}
    assert "part_of" not in edge_types, f"part_of edges should not appear as flow paths, got {edge_types}"


async def test_impact_propagation_with_derived_from():
    a = _unique("test_mat_a")
    b = _unique("test_mat_b")
    c = _unique("test_part_c")

    await _create_test_node(a, "测试原料A", EntityType.MATERIAL)
    await _create_test_node(b, "测试原料B", EntityType.MATERIAL)
    await _create_test_node(c, "测试部件C", EntityType.PART)
    await _create_test_edge(_unique("e_df"), a, b, IndustrialFlowType.DERIVED_FROM)
    await _create_test_edge(_unique("e_mi"), b, c, IndustrialFlowType.MATERIAL_INPUT)

    task = _make_task(
        TaskType.IMPACT_PROPAGATION,
        [a],
        requested_outputs=[OutputType.NODE_SCORES, OutputType.PATHS],
    )
    result = await run_impact_propagation(task, reasoning_id="test_impact")

    assert result.status in ("success", "partial")
    scores = result.result_payload.get("node_scores", [])
    scored_ids = {s["node_id"] for s in scores}
    assert a in scored_ids
    assert b in scored_ids or c in scored_ids


async def test_bottleneck_detection_finds_shared_node():
    src1 = _unique("test_src1")
    src2 = _unique("test_src2")
    bottleneck = _unique("test_bottleneck")
    dst = _unique("test_dst")

    for nid, name, et in [
        (src1, "源1", EntityType.MATERIAL),
        (src2, "源2", EntityType.MATERIAL),
        (bottleneck, "瓶颈", EntityType.MATERIAL),
        (dst, "终点", EntityType.PART),
    ]:
        await _create_test_node(nid, name, et)
    await _create_test_edge(_unique("e1"), src1, bottleneck, IndustrialFlowType.MATERIAL_INPUT)
    await _create_test_edge(_unique("e2"), src2, bottleneck, IndustrialFlowType.MATERIAL_INPUT)
    await _create_test_edge(_unique("e3"), bottleneck, dst, IndustrialFlowType.MATERIAL_INPUT)

    task = _make_task(
        TaskType.BOTTLENECK_DETECTION,
        [src1, src2],
        requested_outputs=[OutputType.NODE_SCORES, OutputType.CANDIDATE_NODES],
    )
    result = await run_bottleneck_detection(task, reasoning_id="test_bottleneck")

    assert result.status in ("success", "partial")
    candidates = result.result_payload.get("candidate_nodes", [])
    candidate_ids = [c["proposed_node_id"] for c in candidates]
    assert bottleneck in candidate_ids, f"Expected bottleneck {bottleneck} in candidates {candidate_ids}"


async def test_substitution_search_finds_sibling():
    raw = _unique("test_raw")
    derived_a = _unique("test_da")
    derived_b = _unique("test_db")

    await _create_test_node(raw, "基础原料", EntityType.MATERIAL)
    await _create_test_node(derived_a, "派生A", EntityType.MATERIAL)
    await _create_test_node(derived_b, "派生B", EntityType.MATERIAL)
    await _create_test_edge(_unique("e_da"), derived_a, raw, IndustrialFlowType.DERIVED_FROM)
    await _create_test_edge(_unique("e_db"), derived_b, raw, IndustrialFlowType.DERIVED_FROM)

    task = _make_task(
        TaskType.SUBSTITUTION_SEARCH,
        [derived_a],
        requested_outputs=[OutputType.CANDIDATE_NODES],
    )
    result = await run_substitution_search(task, reasoning_id="test_substitution")

    assert result.status in ("success", "partial")
    candidates = result.result_payload.get("candidate_nodes", [])
    candidate_ids = [c["proposed_node_id"] for c in candidates]
    assert derived_b in candidate_ids, f"Expected sibling {derived_b} in candidates {candidate_ids}"


async def test_candidate_discovery_missing_process():
    m = _unique("test_mat_m")
    p = _unique("test_part_p")

    await _create_test_node(m, "测试原料", EntityType.MATERIAL)
    await _create_test_node(p, "测试部件", EntityType.PART)
    await _create_test_edge(_unique("e_mi"), m, p, IndustrialFlowType.MATERIAL_INPUT)

    task = _make_task(
        TaskType.CANDIDATE_DISCOVERY,
        [m],
        requested_outputs=[OutputType.CANDIDATE_NODES, OutputType.CANDIDATE_EDGES],
    )
    result = await run_candidate_discovery(task, reasoning_id="test_candidate")

    assert result.status in ("success", "partial")
    candidates = result.result_payload.get("candidate_nodes", [])
    process_candidates = [c for c in candidates if c.get("proposed_entity_type") == "process"]
    assert process_candidates, f"Expected process candidate, got {candidates}"


async def test_cross_graph_context_returns_company_exposure():
    try:
        from app.database_postgres import get_postgres_pool
        pool = await get_postgres_pool()
        if pool is None:
            pytest.skip("PostgreSQL not available")
    except Exception:
        pytest.skip("PostgreSQL not available")

    node_id = _unique("test_cross_node")
    company_id = _unique("test_cross_company")
    unique_suffix = str(uuid.uuid4())[:6]

    await _create_test_node(node_id, f"测试交叉节点{unique_suffix}", EntityType.MATERIAL)

    company = await company_storage.create_company(
        Company(
            company_id=company_id,
            name_zh=f"测试交叉公司{unique_suffix}",
            company_type=CompanyType.PRIVATE,
            country="CN",
            is_test=True,
        )
    )
    assert company is not None

    exposure = await company_storage.create_exposure(
        CompanyNodeExposure(
            exposure_id=_unique("exp"),
            company_id=company_id,
            node_id=node_id,
            activity_type=CompanyActivityType.PRODUCE,
            role="producer",
            is_test=True,
        ),
    )
    assert exposure is not None

    task = _make_task(
        TaskType.CROSS_GRAPH_CONTEXT,
        [node_id],
        requested_outputs=[OutputType.TEMPORARY_GRAPH],
    )
    result = await run_cross_graph_context(task, reasoning_id="test_cross")

    assert result.status in ("success", "partial")
    temp_graph = result.result_payload.get("temporary_graph", {})
    node_ids = {n["temp_node_id"] for n in temp_graph.get("nodes", [])}
    assert node_id in node_ids
    assert company_id in node_ids
