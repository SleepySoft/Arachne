# -*- coding: utf-8 -*-
"""
数据库检查与清理工具。

设计目标：可扩展。新增检查器只需继承 Checker、实现 run/fix，并在模块末尾调用 register_checker。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.database import get_async_driver
from app.database_postgres import get_postgres_pool
from app.services.ontology_rules import get_rule_by_checker


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class CheckIssue(BaseModel):
    issue_id: str
    check_id: str
    severity: Severity
    title: str
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)
    affected_ids: List[str] = Field(default_factory=list)
    fixable: bool = False


class CheckResult(BaseModel):
    check_id: str
    name: str
    description: str
    severity: Severity
    fixable: bool
    issues: List[CheckIssue]
    issue_count: int


class FixResult(BaseModel):
    check_id: str
    fixed_count: int
    skipped_count: int
    messages: List[str] = Field(default_factory=list)


class Checker(ABC):
    """所有数据库检查器的抽象基类。"""

    check_id: str
    name: str
    description: str
    severity: Severity = Severity.WARNING
    fixable: bool = False

    @abstractmethod
    async def run(self) -> List[CheckIssue]:
        """执行检查，返回发现的问题列表。"""
        ...

    async def fix(self, issues: List[CheckIssue]) -> FixResult:
        """默认不可修复。子类可覆盖。"""
        return FixResult(
            check_id=self.check_id,
            fixed_count=0,
            skipped_count=len(issues),
            messages=["该检查器不支持自动修复"],
        )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

CHECKERS: Dict[str, Checker] = {}


def register_checker(checker: Checker) -> Checker:
    instance = checker() if isinstance(checker, type) else checker
    CHECKERS[instance.check_id] = instance
    return instance


def get_checker(check_id: str) -> Optional[Checker]:
    return CHECKERS.get(check_id)


def list_checkers() -> List[Checker]:
    return list(CHECKERS.values())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_created_at(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return None
    return None


async def _neo4j_node_ids() -> set:
    driver = get_async_driver()
    async with driver.session() as s:
        result = await s.run("MATCH (n:IndustrialNode) RETURN n.node_id AS id")
        return {rec["id"] async for rec in result if rec["id"]}


async def _delete_neo4j_edges(edge_ids: List[str]) -> int:
    if not edge_ids:
        return 0
    driver = get_async_driver()
    async with driver.session() as s:
        result = await s.run(
            """
            MATCH ()-[r:INDUSTRIAL_FLOW|ONTOLOGY]->()
            WHERE r.edge_id IN $edge_ids
            DELETE r
            RETURN count(r) AS cnt
            """,
            {"edge_ids": edge_ids},
        )
        rec = await result.single()
        return rec["cnt"] if rec else 0


# ---------------------------------------------------------------------------
# Checkers
# ---------------------------------------------------------------------------

@register_checker
class DuplicateEdgesChecker(Checker):
    """两个节点之间存在多条相同 namespace + type 的关系。"""

    check_id = "duplicate_edges"
    name = "重复关系"
    description = "检测同一对节点之间是否存在多条相同 namespace 和 type 的边。"
    severity = Severity.ERROR
    fixable = True

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(b:IndustrialNode)
                WITH a.node_id AS from_id, b.node_id AS to_id,
                     r.edge_namespace AS ns, r.edge_type AS et,
                     collect({edge_id: r.edge_id, created_at: r.created_at}) AS edges
                WHERE size(edges) > 1
                RETURN from_id, to_id, ns, et, edges
                ORDER BY from_id, to_id, ns, et
                """
            )
            async for rec in result:
                edges = sorted(
                    rec["edges"],
                    key=lambda e: (_parse_created_at(e.get("created_at")) or datetime.min),
                )
                keep = edges[0]["edge_id"]
                duplicates = [e["edge_id"] for e in edges[1:]]
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['from_id']}->{rec['to_id']}:{rec['ns']}:{rec['et']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="重复关系",
                        summary=(
                            f"`{rec['from_id']}` → `{rec['to_id']}` 在 `{rec['ns']}:{rec['et']}` 上"
                            f"存在 {len(duplicates)} 条重复边"
                        ),
                        details={
                            "from_node": rec["from_id"],
                            "to_node": rec["to_id"],
                            "edge_namespace": rec["ns"],
                            "edge_type": rec["et"],
                            "keep_edge_id": keep,
                            "duplicate_edge_ids": duplicates,
                        },
                        affected_ids=[rec["from_id"], rec["to_id"], keep] + duplicates,
                        fixable=True,
                    )
                )
        return issues

    async def fix(self, issues: List[CheckIssue]) -> FixResult:
        to_delete: List[str] = []
        for issue in issues:
            to_delete.extend(issue.details.get("duplicate_edge_ids", []))
        deleted = await _delete_neo4j_edges(list(set(to_delete)))
        return FixResult(
            check_id=self.check_id,
            fixed_count=deleted,
            skipped_count=len(to_delete) - deleted,
            messages=[f"已删除 {deleted} 条重复关系"],
        )


@register_checker
class SelfLoopChecker(Checker):
    """节点指向自身的边。"""

    check_id = "self_loops"
    name = "自环关系"
    description = "检测起点和终点为同一节点的关系。"
    severity = Severity.ERROR
    fixable = True

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (n:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(n)
                RETURN n.node_id AS node_id, r.edge_id AS edge_id, r.edge_namespace AS ns, r.edge_type AS et
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['edge_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="自环关系",
                        summary=f"节点 `{rec['node_id']}` 存在指向自身的 `{rec['ns']}:{rec['et']}` 关系。",
                        details={
                            "node_id": rec["node_id"],
                            "edge_id": rec["edge_id"],
                            "edge_namespace": rec["ns"],
                            "edge_type": rec["et"],
                        },
                        affected_ids=[rec["node_id"], rec["edge_id"]],
                        fixable=True,
                    )
                )
        return issues

    async def fix(self, issues: List[CheckIssue]) -> FixResult:
        to_delete = [i.details["edge_id"] for i in issues if i.details.get("edge_id")]
        deleted = await _delete_neo4j_edges(list(set(to_delete)))
        return FixResult(
            check_id=self.check_id,
            fixed_count=deleted,
            skipped_count=len(to_delete) - deleted,
            messages=[f"已删除 {deleted} 条自环关系"],
        )


@register_checker
class OrphanNodeChecker(Checker):
    """没有任何关系连接的孤立节点。"""

    check_id = "orphan_nodes"
    name = "孤立节点"
    description = "检测没有任何 INDUSTRIAL_FLOW 或 ONTOLOGY 关系连接的节点。"
    severity = Severity.WARNING
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (n:IndustrialNode)
                WHERE NOT (n)-[:INDUSTRIAL_FLOW|ONTOLOGY]-(:IndustrialNode)
                RETURN n.node_id AS node_id, n.canonical_name_zh AS name
                ORDER BY node_id
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['node_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="孤立节点",
                        summary=f"节点 `{rec['name'] or rec['node_id']}` 未连接到任何其他节点。",
                        details={"node_id": rec["node_id"], "name": rec["name"]},
                        affected_ids=[rec["node_id"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class ReverseIndustrialFlowChecker(Checker):
    """双向产业流关系可能冲突。"""

    check_id = "reverse_industrial_flow"
    name = "双向产业流冲突"
    description = "检测两个节点之间同时存在 A→B 和 B→A 的 INDUSTRIAL_FLOW 关系。"
    severity = Severity.WARNING
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (a:IndustrialNode)-[r1:INDUSTRIAL_FLOW]->(b:IndustrialNode),
                      (b)-[r2:INDUSTRIAL_FLOW]->(a)
                WHERE a.node_id < b.node_id
                RETURN a.node_id AS a, b.node_id AS b,
                       collect(DISTINCT r1.edge_type) AS types_ab,
                       collect(DISTINCT r2.edge_type) AS types_ba
                ORDER BY a, b
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['a']}<->{rec['b']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="双向产业流冲突",
                        summary=(
                            f"`{rec['a']}` 与 `{rec['b']}` 之间同时存在上下游产业流关系，"
                            "请确认是否应保留双向关系。"
                        ),
                        details={
                            "node_a": rec["a"],
                            "node_b": rec["b"],
                            "a_to_b_types": rec["types_ab"],
                            "b_to_a_types": rec["types_ba"],
                        },
                        affected_ids=[rec["a"], rec["b"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class MissingNodePropertyChecker(Checker):
    """节点缺少关键属性。"""

    check_id = "missing_node_properties"
    name = "节点关键属性缺失"
    description = "检测缺少 canonical_name_zh、definition 或 entity_type 的节点。"
    severity = Severity.WARNING
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (n:IndustrialNode)
                WHERE n.canonical_name_zh IS NULL OR trim(n.canonical_name_zh) = ''
                   OR n.definition IS NULL OR trim(n.definition) = ''
                   OR n.entity_type IS NULL OR trim(n.entity_type) = ''
                RETURN n.node_id AS node_id,
                       n.canonical_name_zh AS name,
                       n.definition AS definition,
                       n.entity_type AS entity_type
                ORDER BY node_id
                """
            )
            async for rec in result:
                missing = []
                if not rec.get("name"):
                    missing.append("canonical_name_zh")
                if not rec.get("definition"):
                    missing.append("definition")
                if not rec.get("entity_type"):
                    missing.append("entity_type")
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['node_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="节点关键属性缺失",
                        summary=f"节点 `{rec['node_id']}` 缺少关键属性：{', '.join(missing)}。",
                        details={"node_id": rec["node_id"], "missing": missing},
                        affected_ids=[rec["node_id"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class DuplicateNodeNameChecker(Checker):
    """多个节点使用相同中文名。"""

    check_id = "duplicate_node_names"
    name = "重复节点中文名"
    description = "检测多个节点共享相同 canonical_name_zh（草稿节点除外）。"
    severity = Severity.WARNING
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (n:IndustrialNode)
                WHERE n.canonical_name_zh IS NOT NULL AND trim(n.canonical_name_zh) <> ''
                  AND NOT n.node_id STARTS WITH 'draft_'
                WITH n.canonical_name_zh AS name, collect(n.node_id) AS ids
                WHERE size(ids) > 1
                RETURN name, ids
                ORDER BY name
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['name']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="重复节点中文名",
                        summary=f"中文名 `{rec['name']}` 被 {len(rec['ids'])} 个节点共用。",
                        details={"name": rec["name"], "node_ids": rec["ids"]},
                        affected_ids=rec["ids"],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class DanglingIndustryMappingChecker(Checker):
    """行业映射指向不存在的产业节点。"""

    check_id = "dangling_industry_mappings"
    name = "行业映射悬空"
    description = "检测 industry_node_mappings 中 node_id 在 Neo4j 中不存在的映射。"
    severity = Severity.ERROR
    fixable = True

    async def run(self) -> List[CheckIssue]:
        pool = await get_postgres_pool()
        if pool is None:
            return []
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT mapping_id, industry_id, node_id FROM industry_node_mappings"
            )
        if not rows:
            return []

        valid_nodes = await _neo4j_node_ids()
        issues: List[CheckIssue] = []
        for r in rows:
            if r["node_id"] not in valid_nodes:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{r['mapping_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="行业映射悬空",
                        summary=(
                            f"行业 `{r['industry_id']}` 的映射 `{r['mapping_id']}` "
                            f"指向不存在的节点 `{r['node_id']}`。"
                        ),
                        details={
                            "mapping_id": r["mapping_id"],
                            "industry_id": r["industry_id"],
                            "node_id": r["node_id"],
                        },
                        affected_ids=[r["mapping_id"], r["node_id"]],
                        fixable=True,
                    )
                )
        return issues

    async def fix(self, issues: List[CheckIssue]) -> FixResult:
        pool = await get_postgres_pool()
        if pool is None:
            return FixResult(check_id=self.check_id, fixed_count=0, skipped_count=len(issues), messages=["PostgreSQL 不可用"])
        mapping_ids = [i.details["mapping_id"] for i in issues if i.details.get("mapping_id")]
        if not mapping_ids:
            return FixResult(check_id=self.check_id, fixed_count=0, skipped_count=0, messages=["没有问题需要修复"])
        async with pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM industry_node_mappings WHERE mapping_id = ANY($1::text[])",
                mapping_ids,
            )
        # asyncpg execute returns command tag like "DELETE 3"
        count_str = result.split(" ")[-1] if isinstance(result, str) else "0"
        try:
            fixed = int(count_str)
        except ValueError:
            fixed = len(mapping_ids)
        return FixResult(
            check_id=self.check_id,
            fixed_count=fixed,
            skipped_count=len(mapping_ids) - fixed,
            messages=[f"已删除 {fixed} 条悬空行业映射"],
        )


@register_checker
class DanglingCompanyExposureChecker(Checker):
    """公司暴露指向不存在的产业节点。"""

    check_id = "dangling_company_exposures"
    name = "公司暴露悬空"
    description = "检测 company_node_exposures 中 node_id 在 Neo4j 中不存在的暴露关系。"
    severity = Severity.ERROR
    fixable = True

    async def run(self) -> List[CheckIssue]:
        pool = await get_postgres_pool()
        if pool is None:
            return []
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT exposure_id, company_id, node_id FROM company_node_exposures"
            )
        if not rows:
            return []

        valid_nodes = await _neo4j_node_ids()
        issues: List[CheckIssue] = []
        for r in rows:
            if r["node_id"] not in valid_nodes:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{r['exposure_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="公司暴露悬空",
                        summary=(
                            f"公司 `{r['company_id']}` 的暴露 `{r['exposure_id']}` "
                            f"指向不存在的节点 `{r['node_id']}`。"
                        ),
                        details={
                            "exposure_id": r["exposure_id"],
                            "company_id": r["company_id"],
                            "node_id": r["node_id"],
                        },
                        affected_ids=[r["exposure_id"], r["node_id"]],
                        fixable=True,
                    )
                )
        return issues

    async def fix(self, issues: List[CheckIssue]) -> FixResult:
        pool = await get_postgres_pool()
        if pool is None:
            return FixResult(check_id=self.check_id, fixed_count=0, skipped_count=len(issues), messages=["PostgreSQL 不可用"])
        exposure_ids = [i.details["exposure_id"] for i in issues if i.details.get("exposure_id")]
        if not exposure_ids:
            return FixResult(check_id=self.check_id, fixed_count=0, skipped_count=0, messages=["没有问题需要修复"])
        async with pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM company_node_exposures WHERE exposure_id = ANY($1::text[])",
                exposure_ids,
            )
        count_str = result.split(" ")[-1] if isinstance(result, str) else "0"
        try:
            fixed = int(count_str)
        except ValueError:
            fixed = len(exposure_ids)
        return FixResult(
            check_id=self.check_id,
            fixed_count=fixed,
            skipped_count=len(exposure_ids) - fixed,
            messages=[f"已删除 {fixed} 条悬空公司暴露"],
        )


@register_checker
class DanglingEdgesChecker(Checker):
    """边端点不是 IndustrialNode（悬挂边）。"""

    check_id = "dangling_edges"
    name = "悬挂关系"
    description = "检测端点节点不存在或不属于 IndustrialNode 的关系。"
    severity = Severity.ERROR
    fixable = True

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH ()-[r:INDUSTRIAL_FLOW|ONTOLOGY]->()
                WHERE NOT (startNode(r):IndustrialNode AND endNode(r):IndustrialNode)
                RETURN elementId(r) AS rel_id, r.edge_id AS edge_id,
                       type(r) AS rel_type, r.edge_namespace AS ns, r.edge_type AS et
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['rel_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="悬挂关系",
                        summary=f"关系 `{rec['edge_id'] or rec['rel_id']}` 的端点节点缺失或类型错误。",
                        details={
                            "rel_id": rec["rel_id"],
                            "edge_id": rec["edge_id"],
                            "rel_type": rec["rel_type"],
                            "edge_namespace": rec["ns"],
                            "edge_type": rec["et"],
                        },
                        affected_ids=[rec["edge_id"] or rec["rel_id"]],
                        fixable=True,
                    )
                )
        return issues

    async def fix(self, issues: List[CheckIssue]) -> FixResult:
        rel_ids = [i.details.get("rel_id") for i in issues if i.details.get("rel_id")]
        if not rel_ids:
            return FixResult(check_id=self.check_id, fixed_count=0, skipped_count=0, messages=["没有问题需要修复"])
        driver = get_async_driver()
        async with driver.session() as s:
            result = await s.run(
                "MATCH ()-[r]->() WHERE elementId(r) IN $rel_ids DELETE r RETURN count(r) AS cnt",
                {"rel_ids": rel_ids},
            )
            rec = await result.single()
            deleted = rec["cnt"] if rec else 0
        return FixResult(
            check_id=self.check_id,
            fixed_count=deleted,
            skipped_count=len(rel_ids) - deleted,
            messages=[f"已删除 {deleted} 条悬挂关系"],
        )


@register_checker
class HighConfidenceMissingEvidenceChecker(Checker):
    """HIGH confidence 的节点或关系缺少 evidence。"""

    check_id = "high_confidence_missing_evidence"
    name = "高置信度缺少证据"
    description = "检测 confidence 为 HIGH 但缺少 evidence 的节点和关系。"
    severity = Severity.ERROR
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            # nodes
            node_result = await s.run(
                """
                MATCH (n:IndustrialNode)
                WHERE n.confidence = 'HIGH'
                  AND (n.evidence IS NULL OR n.evidence = '' OR n.evidence = '[]')
                RETURN n.node_id AS node_id, n.canonical_name_zh AS name
                ORDER BY node_id
                """
            )
            async for rec in node_result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:node:{rec['node_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="高置信度节点缺少证据",
                        summary=f"节点 `{rec['name'] or rec['node_id']}` 为 HIGH 置信度但缺少证据。",
                        details={"node_id": rec["node_id"], "name": rec["name"]},
                        affected_ids=[rec["node_id"]],
                        fixable=False,
                    )
                )

            # edges
            edge_result = await s.run(
                """
                MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(b:IndustrialNode)
                WHERE r.confidence = 'HIGH'
                  AND (r.evidence IS NULL OR r.evidence = '' OR r.evidence = '[]')
                RETURN r.edge_id AS edge_id, a.node_id AS from_node, b.node_id AS to_node,
                       r.edge_namespace AS ns, r.edge_type AS et
                ORDER BY edge_id
                """
            )
            async for rec in edge_result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:edge:{rec['edge_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="高置信度关系缺少证据",
                        summary=(
                            f"关系 `{rec['edge_id']}` ({rec['from_node']} → {rec['to_node']}) "
                            f"为 HIGH 置信度但缺少证据。"
                        ),
                        details={
                            "edge_id": rec["edge_id"],
                            "from_node": rec["from_node"],
                            "to_node": rec["to_node"],
                            "edge_namespace": rec["ns"],
                            "edge_type": rec["et"],
                        },
                        affected_ids=[rec["edge_id"], rec["from_node"], rec["to_node"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class ActiveStatusMissingEvidenceChecker(Checker):
    """ACTIVE 状态的节点缺少 evidence（当前边模型不含 status）。"""

    check_id = "active_status_missing_evidence"
    name = "ACTIVE 节点缺少证据"
    description = "检测状态为 ACTIVE 但缺少 evidence 的节点。"
    severity = Severity.WARNING
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            node_result = await s.run(
                """
                MATCH (n:IndustrialNode)
                WHERE n.status = 'ACTIVE'
                  AND (n.evidence IS NULL OR n.evidence = '' OR n.evidence = '[]')
                RETURN n.node_id AS node_id, n.canonical_name_zh AS name
                ORDER BY node_id
                """
            )
            async for rec in node_result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:node:{rec['node_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="ACTIVE 节点缺少证据",
                        summary=f"节点 `{rec['name'] or rec['node_id']}` 为 ACTIVE 但缺少证据。",
                        details={"node_id": rec["node_id"], "name": rec["name"]},
                        affected_ids=[rec["node_id"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class OntologySymmetricConflictChecker(Checker):
    """本体关系双向冲突，例如 A is_a B 且 B is_a A。"""

    check_id = "ontology_symmetric_conflict"
    name = "本体关系双向冲突"
    description = "检测两个节点之间同时存在同一 ontology 类型的双向关系。"
    severity = Severity.ERROR
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (a:IndustrialNode)-[r1:ONTOLOGY]->(b:IndustrialNode),
                      (b)-[r2:ONTOLOGY]->(a)
                WHERE a.node_id < b.node_id AND r1.edge_type = r2.edge_type
                RETURN a.node_id AS a, b.node_id AS b, r1.edge_type AS et,
                       collect(DISTINCT r1.edge_id) AS ab_edges,
                       collect(DISTINCT r2.edge_id) AS ba_edges
                ORDER BY a, b, et
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['a']}<->{rec['b']}:{rec['et']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="本体关系双向冲突",
                        summary=(
                            f"`{rec['a']}` 与 `{rec['b']}` 之间同时存在双向 `{rec['et']}` 关系。"
                        ),
                        details={
                            "node_a": rec["a"],
                            "node_b": rec["b"],
                            "edge_type": rec["et"],
                            "a_to_b_edges": rec["ab_edges"],
                            "b_to_a_edges": rec["ba_edges"],
                        },
                        affected_ids=[rec["a"], rec["b"]] + rec["ab_edges"] + rec["ba_edges"],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class OntologyCycleChecker(Checker):
    """ONTOLOGY 关系形成有向环。"""

    check_id = "ontology_cycle"
    name = "本体关系环"
    description = "检测 ONTOLOGY 关系中出现的有向环（如 A is_a B is_a A）。"
    severity = Severity.ERROR
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        seen: set = set()
        async with driver.session() as s:
            # Find any cycle up to length 10; limit to avoid runaway queries.
            result = await s.run(
                """
                MATCH path = (a:IndustrialNode)-[:ONTOLOGY*1..10]->(a)
                RETURN [n IN nodes(path) | n.node_id] AS cycle_nodes,
                       [r IN relationships(path) | r.edge_id] AS cycle_edges
                LIMIT 1000
                """
            )
            async for rec in result:
                cycle = rec["cycle_nodes"]
                key = tuple(sorted(cycle))
                if key in seen:
                    continue
                seen.add(key)
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{cycle[0]}:{len(cycle)}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="本体关系环",
                        summary=f"节点 `{' → '.join(cycle)} → {cycle[0]}` 形成 ONTOLOGY 环。",
                        details={
                            "cycle_nodes": cycle,
                            "cycle_edges": rec["cycle_edges"],
                        },
                        affected_ids=list(set(cycle)),
                        fixable=False,
                    )
                )
        return issues


@register_checker
class AliasOfDescriptionChecker(Checker):
    """alias_of 关系缺少说明为何是别名/同义/译名。"""

    check_id = "alias_of_description"
    name = "alias_of 关系描述不完整"
    description = "检测 alias_of 关系缺少 description 或未说明别名类型。"
    severity = Severity.WARNING
    fixable = False

    _ALIAS_KEYWORDS = ("别名", "同义", "译名", "简称", "旧称", "也称", "又称")

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (a:IndustrialNode)-[r:ONTOLOGY]->(b:IndustrialNode)
                WHERE r.edge_type = 'alias_of'
                RETURN r.edge_id AS edge_id, a.node_id AS from_node, b.node_id AS to_node,
                       r.description AS description
                ORDER BY edge_id
                """
            )
            async for rec in result:
                desc = rec.get("description") or ""
                if not desc.strip() or not any(kw in desc for kw in self._ALIAS_KEYWORDS):
                    issues.append(
                        CheckIssue(
                            issue_id=f"{self.check_id}:{rec['edge_id']}",
                            check_id=self.check_id,
                            severity=self.severity,
                            title="alias_of 关系描述不完整",
                            summary=(
                                f"关系 `{rec['edge_id']}` ({rec['from_node']} → {rec['to_node']}) "
                                f"为 alias_of，但缺少别名类型说明。"
                            ),
                            details={
                                "edge_id": rec["edge_id"],
                                "from_node": rec["from_node"],
                                "to_node": rec["to_node"],
                                "description": desc,
                            },
                            affected_ids=[rec["edge_id"], rec["from_node"], rec["to_node"]],
                            fixable=False,
                        )
                    )
        return issues


@register_checker
class UnknownEntityTypeChecker(Checker):
    """节点 entity_type 为 unknown。"""

    check_id = "unknown_entity_type"
    name = "未知实体类型"
    description = "检测 entity_type 为 unknown 或缺失的节点。"
    severity = Severity.WARNING
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (n:IndustrialNode)
                WHERE n.entity_type IS NULL OR trim(n.entity_type) = '' OR n.entity_type = 'unknown'
                RETURN n.node_id AS node_id, n.canonical_name_zh AS name, n.entity_type AS entity_type
                ORDER BY node_id
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['node_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="未知实体类型",
                        summary=f"节点 `{rec['name'] or rec['node_id']}` 的 entity_type 为 `{rec['entity_type'] or '空'}`。",
                        details={"node_id": rec["node_id"], "name": rec["name"], "entity_type": rec["entity_type"]},
                        affected_ids=[rec["node_id"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class InputToProductDirectEdgeChecker(Checker):
    """material / device / technology_capability 不直接指向产品节点。"""

    check_id = "input_to_product_direct_edge"
    name = "输入物/设备/能力不直连产品"
    description = "检测 material、device、technology_capability 节点是否直接通过产业流指向产品类节点。"
    severity = Severity.WARNING
    fixable = False

    INPUT_TYPES = {"material", "device", "technology_capability"}
    # 产品/交付物类节点：上游输入需先经过 process / service / technology_capability 中转
    PRODUCT_TYPES = {"part", "device", "equipment", "system", "platform", "software"}
    EDGE_TYPES = {
        "material_input",
        "equipment_enablement",
        "capability_enablement",
        "information_input",
    }

    def __init__(self):
        rule = get_rule_by_checker(self.check_id)
        if rule:
            self.name = rule.title
            self.description = rule.description
            self.severity = Severity(rule.severity.value)
            self.fixable = rule.fixable

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
                WHERE a.entity_type IN $input_types
                  AND b.entity_type IN $product_types
                  AND r.edge_type IN $edge_types
                RETURN elementId(r) AS rel_id, r.edge_id AS edge_id,
                       a.node_id AS from_node, a.canonical_name_zh AS from_name, a.entity_type AS from_type,
                       b.node_id AS to_node, b.canonical_name_zh AS to_name, b.entity_type AS to_type,
                       r.edge_type AS et
                ORDER BY edge_id
                """,
                {
                    "input_types": list(self.INPUT_TYPES),
                    "product_types": list(self.PRODUCT_TYPES),
                    "edge_types": list(self.EDGE_TYPES),
                },
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['rel_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="输入物/设备/能力直接指向产品",
                        summary=(
                            f"`{rec['from_name'] or rec['from_node']}` ({rec['from_type']}) "
                            f"通过 `{rec['et']}` 直接指向产品 "
                            f"`{rec['to_name'] or rec['to_node']}` ({rec['to_type']})。"
                        ),
                        details={
                            "rel_id": rec["rel_id"],
                            "edge_id": rec["edge_id"],
                            "from_node": rec["from_node"],
                            "from_name": rec["from_name"],
                            "from_type": rec["from_type"],
                            "to_node": rec["to_node"],
                            "to_name": rec["to_name"],
                            "to_type": rec["to_type"],
                            "edge_type": rec["et"],
                        },
                        affected_ids=[rec["edge_id"] or rec["rel_id"], rec["from_node"], rec["to_node"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class MissingIndustrialFlowDescriptionChecker(Checker):
    """产业流关系缺少 description。"""

    check_id = "missing_industrial_flow_description"
    name = "产业流关系缺少描述"
    description = "检测 INDUSTRIAL_FLOW 类型的边是否缺少 description。"
    severity = Severity.WARNING
    fixable = False

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW]->(b:IndustrialNode)
                WHERE r.description IS NULL OR trim(r.description) = ''
                RETURN r.edge_id AS edge_id, a.node_id AS from_node, b.node_id AS to_node,
                       r.edge_type AS et
                ORDER BY edge_id
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['edge_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="产业流关系缺少描述",
                        summary=(
                            f"关系 `{rec['edge_id']}` ({rec['from_node']} → {rec['to_node']}) "
                            f"缺少 description。"
                        ),
                        details={
                            "edge_id": rec["edge_id"],
                            "from_node": rec["from_node"],
                            "to_node": rec["to_node"],
                            "edge_type": rec["et"],
                        },
                        affected_ids=[rec["edge_id"], rec["from_node"], rec["to_node"]],
                        fixable=False,
                    )
                )
        return issues


@register_checker
class EntityDomainBoundaryChecker(Checker):
    """公司与产业实体在产业图中隔离。"""

    check_id = "entity_domain_boundary"
    name = "公司与产业实体隔离"
    description = "检测 Neo4j 产业图中是否存在 :Company 与 :IndustrialNode 之间的边。"
    severity = Severity.ERROR
    fixable = True

    def __init__(self):
        rule = get_rule_by_checker(self.check_id)
        if rule:
            self.name = rule.title
            self.description = rule.description
            self.severity = Severity(rule.severity.value)
            self.fixable = rule.fixable

    async def run(self) -> List[CheckIssue]:
        driver = get_async_driver()
        issues: List[CheckIssue] = []
        async with driver.session() as s:
            result = await s.run(
                """
                MATCH (a)-[r:INDUSTRIAL_FLOW|ONTOLOGY]->(b)
                WHERE (a:Company AND b:IndustrialNode) OR (a:IndustrialNode AND b:Company)
                RETURN elementId(r) AS rel_id, r.edge_id AS edge_id,
                       labels(a) AS from_labels, a.node_id AS from_id,
                       labels(b) AS to_labels, b.node_id AS to_id,
                       type(r) AS rel_type, r.edge_namespace AS ns, r.edge_type AS et
                ORDER BY edge_id
                """
            )
            async for rec in result:
                issues.append(
                    CheckIssue(
                        issue_id=f"{self.check_id}:{rec['rel_id']}",
                        check_id=self.check_id,
                        severity=self.severity,
                        title="公司与产业实体隔离违规",
                        summary=(
                            f"关系 `{rec['edge_id'] or rec['rel_id']}` 连接了 "
                            f"{rec['from_labels']} `{rec['from_id']}` 与 "
                            f"{rec['to_labels']} `{rec['to_id']}`。"
                        ),
                        details={
                            "rel_id": rec["rel_id"],
                            "edge_id": rec["edge_id"],
                            "from_node": rec["from_id"],
                            "from_labels": rec["from_labels"],
                            "to_node": rec["to_id"],
                            "to_labels": rec["to_labels"],
                            "rel_type": rec["rel_type"],
                            "edge_namespace": rec["ns"],
                            "edge_type": rec["et"],
                        },
                        affected_ids=[rec["edge_id"] or rec["rel_id"], rec["from_id"], rec["to_id"]],
                        fixable=True,
                    )
                )
        return issues

    async def fix(self, issues: List[CheckIssue]) -> FixResult:
        rel_ids = [i.details.get("rel_id") for i in issues if i.details.get("rel_id")]
        if not rel_ids:
            return FixResult(check_id=self.check_id, fixed_count=0, skipped_count=0, messages=["没有问题需要修复"])
        driver = get_async_driver()
        async with driver.session() as s:
            result = await s.run(
                "MATCH ()-[r]->() WHERE elementId(r) IN $rel_ids DELETE r RETURN count(r) AS cnt",
                {"rel_ids": rel_ids},
            )
            rec = await result.single()
            deleted = rec["cnt"] if rec else 0
        return FixResult(
            check_id=self.check_id,
            fixed_count=deleted,
            skipped_count=len(rel_ids) - deleted,
            messages=[f"已删除 {deleted} 条跨域违规关系"],
        )


# Note: device-to-product direct edge checking is now covered by input_to_product_direct_edge
# (R17) which includes material/device/technology_capability -> product flows.
