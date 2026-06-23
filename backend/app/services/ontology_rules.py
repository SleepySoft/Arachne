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
    QUALITY = "quality"           # 数据质量（保留以兼容历史代码，建议优先使用 RuleGroup）


class RuleGroup(str, Enum):
    """规则的业务分组，用于前端展示和批量启用/禁用。"""
    CONTENT = "content"           # 内容质量：命名、定义、证据、别名
    TOPOLOGY = "topology"         # 拓扑结构：连接、方向、层级、过程完整性
    ONTOLOGY = "ontology"         # 本体层级：is_a / part_of / alias_of / variant_of
    CROSS_DOMAIN = "cross_domain" # 跨域隔离：产业图 vs 事实图 vs 业务表


@dataclass(frozen=True)
class OntologyRule:
    rule_id: str
    title: str
    description: str
    severity: Severity
    category: RuleCategory       # 旧分类，保留用于代码兼容性
    group: RuleGroup             # 新业务分组
    fixable: bool
    rationale: str
    examples: List[str]
    checker_id: Optional[str] = None


# ============================================================================
# 规则评估说明（2026-06-23）
# ----------------------------------------------------------------------------
# 已合并/删除的重复规则：
# - R03「ACTIVE 节点必须有证据」被 R02 覆盖（R02 已要求 ACTIVE 或 HIGH）。
# - R13「设备类节点不直接指向产品节点」被 R17 覆盖（R17 包含 device / material /
#   technology_capability，且覆盖 equipment_enablement / capability_enablement /
#   material_input / information_input）。若后续需要把 composition 等边也纳入，
#   可直接扩展 R17 的描述与 checker。
#
# 待补充方向（用户后续可继续添加）：
# - 内容：标准名语言一致性、定义抄袭/过短检测、别名冲突、证据 URL 可访问性。
# - 拓扑：特定 entity_type 的入度/出度约束、循环供应链、过程节点输入输出平衡。
# - 本体：is_a 跨类型跳跃、part_of 深度限制、alias_of 同类型要求。
# - 跨域：公司-产业节点重名、行业映射权重范围、公司暴露角色枚举校验。
# ============================================================================

ONTOLOGY_RULES: List[OntologyRule] = [
    # -------------------------------------------------------------------------
    # Group: CONTENT（内容质量）
    # -------------------------------------------------------------------------
    OntologyRule(
        rule_id="R01",
        title="节点关键属性必须完整",
        description="产业节点必须提供 canonical_name_zh（中文标准名）、definition（定义）和 entity_type（实体类型）。",
        severity=Severity.WARNING,
        category=RuleCategory.NODE,
        group=RuleGroup.CONTENT,
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
        group=RuleGroup.CONTENT,
        fixable=False,
        rationale="高置信度或被激活的节点是图谱的权威节点，必须有可追溯来源。",
        examples=["HIGH confidence 但 evidence 为空的 'chip' 节点"],
        checker_id="high_confidence_missing_evidence",
    ),
    OntologyRule(
        rule_id="R04",
        title="禁止重复节点中文名",
        description="多个非草稿节点不得共享同一个 canonical_name_zh。",
        severity=Severity.WARNING,
        category=RuleCategory.NODE,
        group=RuleGroup.CONTENT,
        fixable=False,
        rationale="同名不同义会导致搜索结果歧义，应通过 alias_of 合并或改名。",
        examples=["两个 node_id 都叫 '芯片' 的节点"],
        checker_id="duplicate_node_names",
    ),
    OntologyRule(
        rule_id="R18",
        title="节点定义不能为空或占位符",
        description="definition 不能为空、仅含空格，或使用明显的占位符文本（如“待补充”、“TODO”、“暂无”）。",
        severity=Severity.WARNING,
        category=RuleCategory.NODE,
        group=RuleGroup.CONTENT,
        fixable=False,
        rationale="占位符定义无法帮助用户理解节点语义，也会降低审图和 AI 推理的可靠性。",
        examples=["definition = '待补充'", "definition = 'TODO'"],
        checker_id="placeholder_definition",
    ),
    OntologyRule(
        rule_id="R19",
        title="证据字段必须完整",
        description="每条 evidence 必须包含非空的 source_title（来源标题）和 quote（原文摘录）。",
        severity=Severity.WARNING,
        category=RuleCategory.QUALITY,
        group=RuleGroup.CONTENT,
        fixable=False,
        rationale="缺少来源标题或摘录的证据无法被复核，等于没有证据。",
        examples=["evidence.quote 为空", "evidence.source_title 为空"],
        checker_id="incomplete_evidence",
    ),
    OntologyRule(
        rule_id="R20",
        title="别名不能重复标准名",
        description="aliases 中不得包含与 canonical_name_zh 或 canonical_name_en 完全相同的字符串。",
        severity=Severity.WARNING,
        category=RuleCategory.NODE,
        group=RuleGroup.CONTENT,
        fixable=True,
        rationale="别名与标准名重复会造成数据冗余，也可能让去重和搜索逻辑产生混淆。",
        examples=["'芯片' 的 aliases 里又出现 '芯片'"],
        checker_id="alias_duplicates_canonical_name",
    ),

    # -------------------------------------------------------------------------
    # Group: TOPOLOGY（拓扑结构）
    # -------------------------------------------------------------------------
    OntologyRule(
        rule_id="R05",
        title="禁止自环关系",
        description="任何关系的起点和终点不能是同一个节点。",
        severity=Severity.ERROR,
        category=RuleCategory.EDGE,
        group=RuleGroup.TOPOLOGY,
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
        group=RuleGroup.TOPOLOGY,
        fixable=True,
        rationale="重复边会导致权重计算、路径搜索和可视化混乱。",
        examples=["wafer -> chip 存在两条 structural_composition 边"],
        checker_id="duplicate_edges",
    ),
    OntologyRule(
        rule_id="R07",
        title="产业流关系必须有描述",
        description="所有 INDUSTRIAL_FLOW 类型的边必须填写 description，说明 from_node 对 to_node 的作用。",
        severity=Severity.WARNING,
        category=RuleCategory.EDGE,
        group=RuleGroup.TOPOLOGY,
        fixable=False,
        rationale="描述是审图和后续维护的主要依据。",
        examples=["material_input 边 description 为空"],
        checker_id="missing_industrial_flow_description",
    ),
    OntologyRule(
        rule_id="R08",
        title="双向产业流冲突需确认",
        description="两个节点之间同时存在 A→B 和 B→A 的 INDUSTRIAL_FLOW 关系时，需要人工确认是否应保留双向。",
        severity=Severity.WARNING,
        category=RuleCategory.EDGE,
        group=RuleGroup.TOPOLOGY,
        fixable=False,
        rationale="产业流通常有明确上下游方向；双向关系可能意味着粒度或分类错误。",
        examples=["A material_input B 且 B material_input A"],
        checker_id="reverse_industrial_flow",
    ),
    OntologyRule(
        rule_id="R14",
        title="悬挂关系必须清理",
        description="INDUSTRIAL_FLOW 或 ONTOLOGY 关系的端点必须是存在的 IndustrialNode。",
        severity=Severity.ERROR,
        category=RuleCategory.EDGE,
        group=RuleGroup.TOPOLOGY,
        fixable=True,
        rationale="悬挂边通常是删除节点后残留的数据垃圾。",
        examples=["edge_id 指向已删除节点"],
        checker_id="dangling_edges",
    ),
    OntologyRule(
        rule_id="R16",
        title="孤立节点需审查",
        description="没有任何 INDUSTRIAL_FLOW 或 ONTOLOGY 关系连接的节点应被审查，确认是否需要补充关系或删除。",
        severity=Severity.WARNING,
        category=RuleCategory.QUALITY,
        group=RuleGroup.TOPOLOGY,
        fixable=False,
        rationale="孤立节点通常表示录入未完成或被遗忘。",
        examples=["新建节点未建立任何关系"],
        checker_id="orphan_nodes",
    ),
    OntologyRule(
        rule_id="R17",
        title="上游要素不直接指向产品",
        description="material、device、technology_capability 类型的节点不能通过 material_input / equipment_enablement / capability_enablement / information_input 直接指向 part / device / equipment / system / platform / software 等产品类节点。它们必须先指向 process / service / technology_capability 节点。",
        severity=Severity.WARNING,
        category=RuleCategory.EDGE,
        group=RuleGroup.TOPOLOGY,
        fixable=False,
        rationale="原材料、设备和能力都需要经过工艺/制造环节才能转化为产品；直接连边会掩盖产业链结构，也与 'Material -> Process -> Output' 的规范流程冲突。",
        examples=["铝 --material_input--> 活塞", "EDA软件 --capability_enablement--> 芯片设计", "光刻机 --equipment_enablement--> 晶圆制造"],
        checker_id="input_to_product_direct_edge",
    ),
    OntologyRule(
        rule_id="R21",
        title="part_of 只应在工艺节点之间",
        description="part_of 关系的起点和终点都应为 entity_type='process' 的节点。其他实体类型不应使用 part_of 表达层级。",
        severity=Severity.WARNING,
        category=RuleCategory.ONTOLOGY,
        group=RuleGroup.TOPOLOGY,
        fixable=True,
        rationale="part_of 用于表达“工艺/流程的组成部分”，非工艺节点应使用 structural_composition 或 is_a 等其他关系。",
        examples=["material --part_of--> process", "device --part_of--> system"],
        checker_id="part_of_process_only",
    ),
    OntologyRule(
        rule_id="R22",
        title="process 节点应同时具备输入和输出",
        description="entity_type='process' 的节点应至少有一条入向 INDUSTRIAL_FLOW（输入/使能）和一条出向 INDUSTRIAL_FLOW（输出/提供服务）。",
        severity=Severity.INFO,
        category=RuleCategory.EDGE,
        group=RuleGroup.TOPOLOGY,
        fixable=False,
        rationale="没有输入或输出的 process 节点可能是未完成的草稿，也可能是被错误分类为 process 的概念。",
        examples=["仅有 process_output 没有输入的 process 节点"],
        checker_id="process_incomplete_io",
    ),

    # -------------------------------------------------------------------------
    # Group: ONTOLOGY（本体层级）
    # -------------------------------------------------------------------------
    OntologyRule(
        rule_id="R09",
        title="本体关系禁止成环",
        description="ONTOLOGY 关系（is_a、alias_of、part_of 等）不能形成有向环。",
        severity=Severity.ERROR,
        category=RuleCategory.ONTOLOGY,
        group=RuleGroup.ONTOLOGY,
        fixable=False,
        rationale="is_a / alias_of / part_of 等关系是层级关系，成环会破坏分类体系。",
        examples=["A is_a B, B is_a C, C is_a A"],
        checker_id="ontology_cycle",
    ),
    OntologyRule(
        rule_id="R10",
        title="本体关系禁止双向冲突",
        description="两个节点之间不能同时存在同一类型的双向 ONTOLOGY 关系。",
        severity=Severity.ERROR,
        category=RuleCategory.ONTOLOGY,
        group=RuleGroup.ONTOLOGY,
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
        group=RuleGroup.ONTOLOGY,
        fixable=False,
        rationale="没有类型说明的 alias_of 无法判断是等价关系还是近似关系。",
        examples=["description 仅写 '别名' 而无具体类型"],
        checker_id="alias_of_description",
    ),
    OntologyRule(
        rule_id="R24",
        title="is_a 关系应保持类型一致性",
        description="is_a 关系表示“是一种”，起点与终点的 entity_type 应当相同，或终点是更抽象的类型（如 part -> device 不宜反向）。",
        severity=Severity.WARNING,
        category=RuleCategory.ONTOLOGY,
        group=RuleGroup.ONTOLOGY,
        fixable=False,
        rationale="跨类型的 is_a 会混淆分类体系，例如把“服务”说成“材料”的一种。",
        examples=["service --is_a--> material", "software --is_a--> device"],
        checker_id="is_a_type_consistency",
    ),

    # -------------------------------------------------------------------------
    # Group: CROSS_DOMAIN（跨域隔离）
    # -------------------------------------------------------------------------
    OntologyRule(
        rule_id="R12",
        title="公司和产业实体在产业图中必须隔离",
        description="Neo4j 产业图（IndustrialNode）中不能出现 :Company 标签的节点，也不能存在公司与产业实体之间的边。",
        severity=Severity.ERROR,
        category=RuleCategory.CROSS_DOMAIN,
        group=RuleGroup.CROSS_DOMAIN,
        fixable=True,
        rationale="公司属于事实图（Factual Graph），产业节点属于本体图；跨域关联应通过 PostgreSQL 的 company_node_exposures 等桥接表实现。",
        examples=["(:Company)-[:INDUSTRIAL_FLOW]->(:IndustrialNode)", "company_id 被误作为 IndustrialNode 节点"],
        checker_id="entity_domain_boundary",
    ),
    OntologyRule(
        rule_id="R15",
        title="行业映射和公司暴露不能悬空",
        description="PostgreSQL 中 industry_node_mappings 与 company_node_exposures 的 node_id 必须在 Neo4j 中存在。",
        severity=Severity.ERROR,
        category=RuleCategory.CROSS_DOMAIN,
        group=RuleGroup.CROSS_DOMAIN,
        fixable=True,
        rationale="桥接表是产业图与业务表的纽带，悬空映射会破坏查询一致性。",
        examples=["行业映射指向已删除的节点", "公司暴露指向不存在的节点"],
        checker_id="dangling_industry_mappings",
    ),
    OntologyRule(
        rule_id="R23",
        title="公司暴露应指向 ACTIVE 节点",
        description="company_node_exposures 中的 node_id 对应的 IndustrialNode 状态应为 ACTIVE。",
        severity=Severity.WARNING,
        category=RuleCategory.CROSS_DOMAIN,
        group=RuleGroup.CROSS_DOMAIN,
        fixable=False,
        rationale="PENDING / REJECTED / ARCHIVED 节点不适合作为公司业务暴露的依据。",
        examples=["某公司的核心产品暴露指向 status=PENDING 的节点"],
        checker_id="company_exposure_inactive_node",
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


def list_rules_by_group(group: RuleGroup) -> List[OntologyRule]:
    return [r for r in ONTOLOGY_RULES if r.group == group]
