# -*- coding: utf-8 -*-
import pytest

from app.services import db_checkers


def test_registered_checkers():
    """所有检查器都应正确注册。"""
    checkers = db_checkers.list_checkers()
    assert len(checkers) >= 10
    ids = {c.check_id for c in checkers}
    expected = {
        "duplicate_edges",
        "self_loops",
        "orphan_nodes",
        "reverse_industrial_flow",
        "missing_node_properties",
        "duplicate_node_names",
        "dangling_industry_mappings",
        "dangling_company_exposures",
        "dangling_edges",
        "high_confidence_missing_evidence",
        "active_status_missing_evidence",
        "ontology_symmetric_conflict",
        "ontology_cycle",
        "alias_of_description",
        "unknown_entity_type",
        "missing_industrial_flow_description",
    }
    assert expected.issubset(ids)


@pytest.mark.asyncio
async def test_duplicate_edges_checker_runs():
    """DuplicateEdgesChecker 应能运行且不抛异常（结果取决于数据库内容）。"""
    checker = db_checkers.get_checker("duplicate_edges")
    assert checker is not None
    issues = await checker.run()
    assert isinstance(issues, list)
