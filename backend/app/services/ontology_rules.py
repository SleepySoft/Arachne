# -*- coding: utf-8 -*-
"""
产业本体设计规则注册表。

本文件是“规则即代码”的单一事实来源：
- DB checker 的 description / severity / fixable 应从本表读取；
- 设计文档 docs/ontology_design_rules.md 应与本表保持同步；
- 新增规则时，先在这里注册，再实现对应 checker，再更新文档。
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class RuleCategory(str, Enum):
    NODE = "node"                 # 节点本身属性/分类
    EDGE = "edge"                 # 产业流/关系
    ONTOLOGY = "ontology"         # 本体关系
    CROSS_DOMAIN = "cross_domain" # 跨域隔离
    QUALITY = "quality"           # 数据质量


@dataclass(frozen=True)
class OntologyRule:
    rule_id: str
    title: str
    description: str
    severity: Severity
    category: RuleCategory
    fixable: bool
    rationale: str
    examples: List[str]
    checker_id: Optional[str] = None


ONTOLOGY_RULES: List[OntologyRule] = [
    OntologyRule(
        rule_id="R01",
        title="节点关键属性必须完整",
        description="产业节点必须提供 canonical_name_zh（中文标准名）、definition（定义）和 entity_type（实体类型）。",
        severity=Severity.WARNING,
        category=RuleCategory.NODE,
        fixable=False,
        rationale="缺少关键属性的节点无法被搜索、理解和验证，也会污染图谱。",
        examples=["缺少 definition 的 'draft_xxx' 节点", "entity_type 为 unknown 的节点"],
        checker_id="missing_node_properties",
    ),
    OntologyRule(
        rule_id="R02",
        title="ACTIVE / HIGH 置信度节点必须有证据",
        description="状态为 ACTIVE 或置信度为 HIGH 的节点必须附带至少一条 evidence。",
        severity=Severity.ERROR,
        category=RuleCategory.QUALITY,
        fixable=False,
        rationale="高置信度或被激活的节点是图谱的权威节点，必须有可追溯来源。",
        examples=["HIGH confidence 但 evidence 为空的 'chip' 节点"],
        checker_id="high_confidence_missing_evidence",
    ),
    OntologyRule(
        rule_id="R03",
        title="ACTIVE 节点必须有证据",
        description="状态为 ACTIVE 的节点必须附带至少一条 evidence。",
        severity=Severity.WARNING,
        category=RuleCategory.QUALITY,
        fixable=False,
        rationale="ACTIVE 节点对外提供查询服务，证据缺失会降低可信度。",
        examples=["status=ACTIVE 但 evidence 为空的节点"],
        checker_id="active_status_missing_evidence",
    ),
    OntologyRule(
        rule_id="R04",
        title="禁止重复节点中文名",
        description="多个非草稿节点不得共享同一个 canonical_name_zh。",
        severity=Severity.WARNING,
        category=RuleCategory.NODE,
        fixable=False,
        rationale="同名不同义会导致搜索结果歧义，应通过 alias_of 合并或改名。",
        examples=["两个 node_id 都叫 '芯片' 的节点"],
        checker_id="duplicate_node_names",
    ),
    OntologyRule(
        rule_id="R05",
        title="禁止自环关系",
        description="任何关系的起点和终点不能是同一个节点。",
        severity=Severity.ERROR,
        category=RuleCategory.EDGE,
        fixable=True,
        rationale="自环边没有语义价值，通常是录入错误。",
        examples=["wafer -> wafer"],
        checker_id="self_loops",
    ),
    OntologyRule(
        rule_id="R06",
        title="禁止重复关系",
        description="同一对节点之间不能存在多条相同 namespace 和 type 的关系。",
        severity=Severity.ERROR,
        category=RuleCategory.EDGE,
        fixable=True,
        rationale="重复边会导致权重计算、路径搜索和可视化混乱。",
        examples=["wafer -> chip 存在两条 composition 边"],
        checker_id="duplicate_edges",
    ),
    OntologyRule(
        rule_id="R07",
        title="产业流关系必须有描述",
        description="所有 INDUSTRIAL_FLOW 类型的边必须填写 description，说明 from_node 对 to_node 的作用。",
        severity=Severity.WARNING,
        category=RuleCategory.EDGE,
        fixable=False,
        rationale="描述是审图和后续维护的主要依据。",
        examples=["material_flow 边 description 为空"],
        checker_id="missing_industrial_flow_description",
    ),
    OntologyRule(
        rule_id="R08",
        title="双向产业流冲突需确认",
        description="两个节点之间同时存在 A→B 和 B→A 的 INDUSTRIAL_FLOW 关系时，需要人工确认是否应保留双向。",
        severity=Severity.WARNING,
        category=RuleCategory.EDGE,
        fixable=False,
        rationale="产业流通常有明确上下游方向；双向关系可能意味着粒度或分类错误。",
        examples=["A material_flow B 且 B material_flow A"],
        checker_id="reverse_industrial_flow",
    ),
    OntologyRule(
        rule_id="R09",
        title="本体关系禁止成环",
        description="ONTOLOGY 关系（is_a、alias_of 等）不能形成有向环。",
        severity=Severity.ERROR,
        category=RuleCategory.ONTOLOGY,
        fixable=False,
        rationale="is_a / alias_of 等关系是层级关系，成环会破坏分类体系。",
        examples=["A is_a B, B is_a C, C is_a A"],
        checker_id="ontology_cycle",
    ),
    OntologyRule(
        rule_id="R10",
        title="本体关系禁止双向冲突",
        description="两个节点之间不能同时存在同一类型的双向 ONTOLOGY 关系。",
        severity=Severity.ERROR,
        category=RuleCategory.ONTOLOGY,
        fixable=False,
        rationale="例如 A is_a B 且 B is_a A 会同时断言两个分类方向，逻辑矛盾。",
        examples=["A is_a B 且 B is_a A"],
        checker_id="ontology_symmetric_conflict",
    ),
    OntologyRule(
        rule_id="R11",
        title="alias_of 关系必须说明别名类型",
        description="alias_of 关系的 description 必须说明是别名、同义、译名、简称、旧称等类型。",
        severity=Severity.WARNING,
        category=RuleCategory.ONTOLOGY,
        fixable=False,
        rationale="没有类型说明的 alias_of 无法判断是等价关系还是近似关系。",
        examples=["description 仅写 '别名' 而无具体类型"],
        checker_id="alias_of_description",
    ),
    OntologyRule(
        rule_id="R12",
        title="公司和产业实体在产业图中必须隔离",
        description="Neo4j 产业图（IndustrialNode）中不能出现 :Company 标签的节点，也不能存在公司与产业实体之间的边。",
        severity=Severity.ERROR,
        category=RuleCategory.CROSS_DOMAIN,
        fixable=True,
        rationale="公司属于事实图（Factual Graph），产业节点属于本体图；跨域关联应通过 PostgreSQL 的 company_node_exposures 等桥接表实现。",
        examples=["(:Company)-[:INDUSTRIAL_FLOW]->(:IndustrialNode)", "company_id 被误作为 IndustrialNode 节点"],
        checker_id="entity_domain_boundary",
    ),
    OntologyRule(
        rule_id="R13",
        title="设备类节点不直接指向产品节点",
        description="entity_type='device' 的节点不能通过 INDUSTRIAL_FLOW 直接指向 component / module / subsystem / system / platform / application_system 等‘产品’类节点。设备必须通过 process / service / technology_capability 节点中转。",
        severity=Severity.ERROR,
        category=RuleCategory.EDGE,
        fixable=True,
        rationale="设备本身不是下游产品的直接输入，而是通过工艺/制造环节作用于产品；直接连边会掩盖产业链的真实结构。",
        examples=["lithography_machine -> wafer", "etching_machine -> chip"],
        checker_id="device_to_product_direct_edge",
    ),
    OntologyRule(
        rule_id="R14",
        title="悬挂关系必须清理",
        description="INDUSTRIAL_FLOW 或 ONTOLOGY 关系的端点必须是存在的 IndustrialNode。",
        severity=Severity.ERROR,
        category=RuleCategory.EDGE,
        fixable=True,
        rationale="悬挂边通常是删除节点后残留的数据垃圾。",
        examples=["edge_id 指向已删除节点"],
        checker_id="dangling_edges",
    ),
    OntologyRule(
        rule_id="R15",
        title="行业映射和公司暴露不能悬空",
        description="PostgreSQL 中 industry_node_mappings 与 company_node_exposures 的 node_id 必须在 Neo4j 中存在。",
        severity=Severity.ERROR,
        category=RuleCategory.CROSS_DOMAIN,
        fixable=True,
        rationale="桥接表是产业图与业务表的纽带，悬空映射会破坏查询一致性。",
        examples=["行业映射指向已删除的节点", "公司暴露指向不存在的节点"],
        checker_id="dangling_industry_mappings",
    ),
    OntologyRule(
        rule_id="R16",
        title="孤立节点需审查",
        description="没有任何 INDUSTRIAL_FLOW 或 ONTOLOGY 关系连接的节点应被审查，确认是否需要补充关系或删除。",
        severity=Severity.WARNING,
        category=RuleCategory.QUALITY,
        fixable=False,
        rationale="孤立节点通常表示录入未完成或被遗忘。",
        examples=["新建节点未建立任何关系"],
        checker_id="orphan_nodes",
    ),
]


# 方便通过 rule_id 或 checker_id 查找
_RULE_BY_ID = {r.rule_id: r for r in ONTOLOGY_RULES}
_RULE_BY_CHECKER = {r.checker_id: r for r in ONTOLOGY_RULES if r.checker_id}


def get_rule(rule_id: str) -> Optional[OntologyRule]:
    return _RULE_BY_ID.get(rule_id)


def get_rule_by_checker(checker_id: str) -> Optional[OntologyRule]:
    return _RULE_BY_CHECKER.get(checker_id)


def list_rules() -> List[OntologyRule]:
    return list(ONTOLOGY_RULES)
