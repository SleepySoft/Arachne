"""
PRINCIPLE:

"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional, Union, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, computed_field, field_validator, model_validator


# ============================================================
# Enums
# ============================================================

class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class NodeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


# Alias for backward compatibility with industry/company schemas
RecordStatus = NodeStatus


class EntityType(str, Enum):
    """
    AI 分类总则：

    1. 优先判断候选词是否为可定义、可命名、可复用、可被证据支持的产业实体。
    2. entity_type 只描述实体自身的主要交付形态或本体类别。
    3. component、module、subsystem、upstream、downstream、supplier、customer 等上下文角色通过关系表达。
    4. 结构层级通过 structural edge 表达。
    5. 产业流动通过 industrial_flow edge 表达。
    6. 同义词、上下位词、变体词通过 ontology edge 表达。
    7. 当候选词更像应用场景、市场分类、行业赛道、政策主题、营销概念、宽泛趋势时，应进入 rejected_or_pending。
    8. 当多个类型都可适用时，按主要交付形态选择：
       - 物质性输入优先 MATERIAL。
       - 简单物理件优先 PART。
       - 独立功能装置优先 DEVICE。
       - 生产、检测、制造、施工、运维装备优先 EQUIPMENT。
       - 多要素协同复合体优先 SYSTEM。
       - 代码、算法、模型、程序逻辑优先 SOFTWARE。
       - 基础承载资源优先 INFRASTRUCTURE。
       - 工艺、流程、处理活动优先 PROCESS。
       - 对外交付的持续性能力优先 SERVICE。
       - 方法、能力域、技术机制优先 TECHNOLOGY_CAPABILITY。
       - 承载、连接、复用、集成多类对象的实体优先 PLATFORM。
       - 规范、协议、标准优先 STANDARD。
       - 数据资源、数据集、知识库优先 DATA_ASSET。
    9. 证据不足时使用 UNKNOWN，并在 notes 中记录原因。
    """

    MATERIAL = "material"
    """
    材料、原料、化学品、能源介质、耗材等物质性实体。

    AI 分类指引：
    - 该类型适用于可作为制造、加工、化学反应、能量转换或产品构成输入的物质。
    - 该类型通常通过 material_input、energy_input、structural_composition 等关系连接到工艺、系统或产品。
    - 该类型可覆盖基础材料、中间材料、功能材料、化学品、燃料、气体、浆料、粉体、薄膜、晶圆、耗材等。
    - 候选词如果主要体现物质组成、物理化学属性、材料牌号、原料品类，可优先归入该类型。

    典型示例：
    - 碳酸锂
    - 六氟磷酸锂
    - 光刻胶
    - 硅片
    - 铜箔
    - 稀土永磁材料
    - 氢气
    - 石墨
    """

    PART = "part"
    """
    物理零件、部件、结构件、加工件等可交付物理实体。

    AI 分类指引：
    - 该类型适用于结构相对明确、通常作为产品或系统物理构成单元使用的实体。
    - 该类型强调实体自身为可识别、可采购、可制造、可装配的物理件。
    - 该类型可覆盖机械零件、电子部件、结构件、连接件、密封件、光学件、线束、壳体、极片、隔膜等。
    - 候选词如果主要体现结构件属性，且缺少独立复杂功能边界，可优先归入该类型。
    - 候选词作为某上级系统中的 component、module、subsystem 角色，应通过结构关系边表达。

    典型示例：
    - 轴承
    - 外壳
    - 连接器
    - 密封圈
    - 透镜
    - 线束
    - 电极片
    - 隔膜
    """

    DEVICE = "device"
    """
    具有独立功能边界的装置、器件、终端、功能单元等物理或软硬结合实体。

    AI 分类指引：
    - 该类型适用于具有明确输入、输出、功能、接口或控制边界的装置类实体。
    - 该类型通常可作为产品、终端、传感、执行、计算、通信、控制、转换、测量等功能单元存在。
    - 该类型可覆盖传感器、控制器、执行器、芯片、终端设备、功能器件、机电装置、电子装置等。
    - 候选词如果体现独立功能能力，并且可作为可交付装置或器件被采购、集成、使用，可优先归入该类型。

    典型示例：
    - 激光雷达
    - 摄像头
    - 传感器
    - MCU
    - PLC
    - 电机
    - 逆变器
    - 充电桩
    - 路侧单元
    """

    EQUIPMENT = "equipment"
    """
    用于生产、制造、检测、施工、实验、运维、物流等产业活动的装备类实体。

    AI 分类指引：
    - 该类型适用于服务于产业过程的装备、设备、机台、产线设备、测试设备、实验设备、施工装备等。
    - 该类型通常通过 equipment_enablement 关系连接到 process。
    - 该类型强调对生产过程、制造过程、检测过程、运维过程或工程过程的使能作用。
    - 候选词如果主要用于制造、加工、检测、装配、测量、施工、维护，可优先归入该类型。
    - 成套产线可根据语义粒度归入 EQUIPMENT 或 SYSTEM，并在 notes 中说明判断依据。

    典型示例：
    - 光刻机
    - 涂布机
    - 卷绕机
    - 刻蚀设备
    - 注塑机
    - 焊接机器人
    - 三坐标测量机
    - 电池化成分容设备
    """

    SYSTEM = "system"
    """
    由多个要素协同实现整体功能的复合实体。

    AI 分类指引：
    - 该类型适用于由硬件、软件、数据、接口、控制逻辑、流程、设施或多个功能单元共同构成的实体。
    - 该类型强调整体功能、内部协同、接口关系和系统边界。
    - 该类型可覆盖机电系统、控制系统、能源系统、信息物理系统、车辆系统、机器人系统、工业控制系统等。
    - 候选词如果体现多个要素集成并对外提供整体能力，可优先归入该类型。
    - 某实体在上级系统中的 subsystem 角色，应通过 structural edge 的 role_of_from_node 表达。

    典型示例：
    - 电池管理系统
    - 自动驾驶系统
    - 储能系统
    - 智能座舱系统
    - 机器人控制系统
    - 工业控制系统
    - 氢燃料电池系统
    """

    SOFTWARE = "software"
    """
    以代码、算法、模型、程序、协议栈、中间件或可运行逻辑为主要交付形态的数字制品。

    AI 分类指引：
    - 该类型适用于软件产品、算法、模型、操作系统、中间件、数据库、SDK、仿真软件、控制软件等。
    - 该类型强调数字制品本身，而非其部署环境或服务运营方式。
    - 候选词如果主要体现程序逻辑、算法能力、模型权重、软件栈、开发工具或数字化功能模块，可优先归入该类型。
    - 软件部署后对外持续提供能力时，可与 SERVICE 通过 service_provision 或 hosted_on 等关系连接。

    典型示例：
    - 实时操作系统
    - AUTOSAR 软件栈
    - 感知算法
    - 目标检测模型
    - 数据库软件
    - 仿真软件
    - SDK
    - 编译器
    """

    INFRASTRUCTURE = "infrastructure"
    """
    为产业活动、系统、服务、应用或数据流通提供基础承载能力的底座型实体。

    AI 分类指引：
    - 该类型适用于网络、能源、算力、交通、通信、物流、数据中心、充换电网络等基础性承载实体。
    - 该类型强调规模化、基础性、支撑性和可被多个上层对象复用的资源能力。
    - 候选词如果主要提供基础资源、运行环境、连接能力、承载能力或公共支撑能力，可优先归入该类型。
    - 基础设施对系统、服务或应用的作用可通过 capability_enablement、service_provision、information_input 等关系表达。

    典型示例：
    - 电网
    - 数据中心
    - 云计算基础设施
    - 5G 网络
    - 高速公路
    - 充换电网络
    - 卫星导航基础设施
    - 算力集群
    """

    PROCESS = "process"
    """
    将输入转化为输出，或完成生产、加工、处理、计算、测试、运营等活动的过程实体。

    AI 分类指引：
    - 该类型适用于工艺、流程、处理步骤、制造过程、检测过程、计算过程、运营过程等。
    - 该类型通常连接材料输入、设备使能、信息输入、能力使能和过程产出。
    - 候选词如果可以表达为一类活动、一道工序、一段流程、一种处理过程或一种生成过程，可优先归入该类型。
    - 工艺路线中的单个步骤和整体流程均可归入该类型，粒度差异应通过 notes 或层级关系说明。

    典型示例：
    - 光刻
    - 刻蚀
    - 涂布
    - 卷绕
    - 注塑
    - 热处理
    - 电池化成
    - 数据标注
    - 模型训练
    - 边缘推理
    """

    SERVICE = "service"
    """
    以持续性活动、能力调用、运营结果、业务结果或外部交付为主要形态的服务实体。

    AI 分类指引：
    - 该类型适用于可被客户调用、购买、订阅、委托或运营交付的服务。
    - 该类型强调外部交付、服务过程、服务结果、服务水平或持续运营能力。
    - 候选词如果体现对外提供服务、平台调用、运维托管、检测认证、数据处理、云端能力交付，可优先归入该类型。
    - 服务背后的软件、设备、基础设施、流程可作为独立节点，通过关系连接到该服务。

    典型示例：
    - 云计算服务
    - 检测认证服务
    - 设备运维服务
    - 数据标注服务
    - 仿真测试服务
    - 充电服务
    - 自动驾驶出租车服务
    - 碳核算服务
    """

    TECHNOLOGY_CAPABILITY = "technology_capability"
    """
    能够赋能产品、系统、工艺、服务或产业活动的技术能力、方法体系或能力域。

    AI 分类指引：
    - 该类型适用于具有明确技术机制、作用对象和能力提升效果的技术能力。
    - 该类型强调赋能作用，可通过 capability_enablement 关系连接到设备、系统、工艺、软件、服务或基础设施。
    - 候选词应能说明其技术原理、能力边界、作用对象或产业用途。
    - 宏观口号、政策标签、趋势词、营销概念、过宽泛主题应进入 rejected_or_pending。
    - 候选词如果可被实现为具体软件、设备、工艺或系统，应根据主要交付形态选择更具体的类型。

    典型示例：
    - 多传感器融合
    - 高精度定位
    - 电池热管理
    - 高压快充
    - 边缘计算
    - 机器视觉
    - 固态电池技术
    - 硅碳负极技术
    """

    PLATFORM = "platform"
    """
    能够承载、连接、集成、复用或赋能多个产品、服务、应用、设备、开发者、数据资源或参与方的平台型实体。

    AI 分类指引：
    - 该类型适用于具有承载能力、连接能力、集成能力、复用能力、生态扩展能力或多方协同能力的实体。
    - 该类型应具有明确的平台边界、平台对象、平台能力和上层承载对象。
    - 候选词名称中包含“平台”时，仍需根据定义判断实体类别。
    - 简单管理系统、单一应用软件、单一服务入口、营销命名项目应谨慎归入该类型。
    - 平台可通过 service_provision、capability_enablement、information_input、hosted_on、integrated_into 等关系连接其他节点。

    典型示例：
    - 工业互联网平台
    - 云原生平台
    - 自动驾驶计算平台
    - 机器人开发平台
    - 数据交易平台
    - 车型平台
    - 芯片平台
    - AI 训练平台
    """

    STANDARD = "standard"
    """
    标准、协议、规范、接口规范、技术规程、认证规则等制度化技术对象。

    AI 分类指引：
    - 该类型适用于具有规范性、约束性、互操作性、认证性或一致性要求的技术对象。
    - 该类型可覆盖国际标准、国家标准、行业标准、团体标准、通信协议、接口规范、安全规范、认证规范等。
    - 候选词如果主要规定系统、设备、软件、流程或服务的接口、行为、安全、质量、数据格式或通信方式，可优先归入该类型。
    - 标准对产品或系统的作用可通过 conforms_to、implements、capability_enablement 等关系表达，具体关系可后续扩展。

    典型示例：
    - USB
    - CAN
    - Ethernet
    - AUTOSAR
    - ISO 26262
    - OPC UA
    - MQTT
    - 充电接口标准
    """

    DATA_ASSET = "data_asset"
    """
    具有复用价值、训练价值、运营价值、知识价值或交易价值的数据资源实体。

    AI 分类指引：
    - 该类型适用于数据集、知识库、地图、语料库、样本库、场景库、运行数据、标注数据等。
    - 该类型强调数据资源本身的可管理性、可复用性、可交换性、可训练性或可分析性。
    - 候选词如果主要体现数据内容、数据集合、数据资源、数据产品或知识资源，可优先归入该类型。
    - 数据资源支撑软件、模型、服务、流程或应用时，应通过 information_input、capability_enablement、service_provision 等关系表达。

    典型示例：
    - 高精地图
    - 训练数据集
    - 语料库
    - 工业知识库
    - 缺陷样本库
    - 道路场景库
    - 传感器数据集
    - 设备运行数据集
    """

    USAGE = "usage"
    """
    PROV-style 使用动作节点（Usage）。

    用于物化“某个工艺执行使用了某个技术/方法”这一关系。
    典型连接：process_execution --uses--> usage --technology--> process_technology。
    """

    UNKNOWN = "unknown"
    """
    暂无法稳定分类的实体类型。

    AI 分类指引：
    - 该类型适用于证据不足、上下文不足、术语歧义较强、候选词粒度不清或实体边界不清的情况。
    - 使用该类型时，应在 notes 中说明不确定原因。
    - 如果候选词疑似市场概念、行业标签、应用场景、公司名称、产品系列、营销术语或泛化主题，应优先进入 rejected_or_pending。
    - 后续可通过补充证据、人工审核、实体合并或类型修正将 UNKNOWN 转换为稳定类型。
    """


class IndustrialFlowType(str, Enum):
    # ============================================================
    # Group A: Activity-Entity input/output (closest to PROV)
    # In PROV terms: Activity prov:used Entity; Entity prov:wasGeneratedBy Activity.
    # Arachne direction: input goes INTO the process; output goes OUT OF the process.
    # ============================================================
    MATERIAL_INPUT = "material_input"                     # 物料输入  → PROV prov:used (Activity used Entity)
    ENERGY_INPUT = "energy_input"                         # 能量输入  → PROV prov:used
    INFORMATION_INPUT = "information_input"               # 信息输入  → PROV prov:used
    EQUIPMENT_ENABLEMENT = "equipment_enablement"         # 设备使能  → PROV prov:used (non-consumable resource)
    PROCESS_OUTPUT = "process_output"                     # 工艺产出  → PROV prov:wasGeneratedBy (reverse: Activity generated Entity)

    # ============================================================
    # Group B: Activity-Entity association / soft enablement
    # PROV analogy: prov:wasAssociatedWith or prov:wasInformedBy (loose coupling).
    # ============================================================
    SERVICE_PROVISION = "service_provision"               # 服务提供  → PROV prov:wasAssociatedWith (service provider)
    CAPABILITY_ENABLEMENT = "capability_enablement"       # 能力使能  → PROV prov:wasAssociatedWith (capability/role)

    # ============================================================
    # Group C: Entity-Entity derivation
    # PROV analogy: prov:wasDerivedFrom.
    # ============================================================
    DERIVED_FROM = "derived_from"                         # 直接物料派生 → PROV prov:wasDerivedFrom

    # ============================================================
    # Group D: Reified Usage (Arachne v2 extension)
    # PROV does not have a native "Usage" node, but prov:used can be reified
    # via prov:Usage to attach extra attributes. Arachne materializes the
    # relationship as: execution --uses--> Usage --technology--> technology.
    # ============================================================
    USES = "uses"                                         # 工艺执行 → 使用动作（Usage 节点）
    TECHNOLOGY = "technology"                             # 使用动作 → 被使用的技术/方法

    # ============================================================
    # Group E: Domain-specific / summary relations (NOT direct PROV)
    # These are convenience edges for industrial-domain modeling.
    # ============================================================
    STRUCTURAL_COMPOSITION = "structural_composition"     # 结构组成（BOM 式，如 部件-整机）
    SUPPLY_RELATION = "supply_relation"                   # 供应关系（摘要级上下游、缺少明确中间工艺、产业链层级）

    # ============================================================
    # Group F: Fallback
    # ============================================================
    UNKNOWN = "unknown"                                   # 未知/待分类


# ============================================================
# Edge Type Labels (shared mapping)
# ============================================================

EDGE_TYPE_LABELS: dict[str, str] = {
    # IndustrialFlowType
    "material_input": "物料输入",
    "energy_input": "能量输入",
    "information_input": "信息输入",
    "equipment_enablement": "设备使能",
    "process_output": "工艺产出",
    "service_provision": "服务提供",
    "capability_enablement": "能力使能",
    "structural_composition": "结构组成",
    "supply_relation": "供应关系",
    "derived_from": "派生自",
    "uses": "使用",
    "technology": "使用技术",
    "unknown": "未知关系",
    # OntologyType
    "alias_of": "别名/同义",
    "is_a": "是一种",
    "part_of": "组成部分",
    "variant_of": "变体",
    "related_term": "相关术语",
}


class OntologyType(str, Enum):
    # ============================================================
    # Group H: Hierarchical / taxonomic relations
    # Not PROV; these are ontology/KOS relations.
    # is_a  ≈ rdfs:subClassOf / skos:broaderTransitive
    # part_of ≈ meronomy / mereology (component-whole)
    # ============================================================
    IS_A = "is_a"                                       # 是一种      → rdfs:subClassOf / skos:broader
    PART_OF = "part_of"                                 # 组成部分    → meronomy (component-whole)

    # ============================================================
    # Group L: Lexical / terminological relations
    # These map loosely to SKOS label/association relations, not PROV.
    # ============================================================
    ALIAS_OF = "alias_of"                               # 别名/同义   → skos:altLabel / owl:sameAs-ish
    VARIANT_OF = "variant_of"                           # 变体        → skos:closeMatch / variant label

    # ============================================================
    # Group D: Deprecated
    # related_term is deprecated. Existing edges are kept for backward
    # compatibility, but new edges should not be created. Use more specific
    # relations (is_a, part_of, variant_of, alias_of, or industrial_flow
    # edges) instead.
    # ============================================================
    RELATED_TERM = "related_term"                       # [DEPRECATED] 相关术语 → skos:related


class ReviewAction(str, Enum):
    CREATE_PENDING_NODE = "create_pending_node"
    MERGE_TO_EXISTING = "merge_to_existing"
    REJECT_AS_MARKET_CONCEPT = "reject_as_market_concept"
    REJECT_AS_COMPANY = "reject_as_company"
    REJECT_AS_APPLICATION_LABEL = "reject_as_application_label"
    NEED_MORE_EVIDENCE = "need_more_evidence"
    REVIEW_MANUALLY = "review_manually"


# ============================================================
# Evidence
# ============================================================

class Evidence(BaseModel):
    source_title: str = Field(
        ...,
        description="资料标题，例如网页标题、报告标题、公告标题"
    )
    source_url: Optional[HttpUrl] = Field(
        default=None,
        description="资料URL。若无URL，可为空"
    )
    quote: str = Field(
        ...,
        description="支持该节点或关系的原文摘录"
    )

    @field_validator("source_title", "quote")
    @classmethod
    def non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v


# ============================================================
# Node
# ============================================================

class IndustrialNode(BaseModel):
    node_uuid: UUID = Field(default_factory=uuid4)

    node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="稳定英文小写蛇形命名，例如 lidar_system"
    )
    canonical_name_zh: str = Field(
        ...,
        description="中文标准名"
    )
    canonical_name_en: Optional[str] = Field(
        default=None,
        description="英文标准名；未知可为空"
    )
    aliases: List[str] = Field(
        default_factory=list,
        description="别名、简称、英文缩写、旧称等"
    )
    definition: str = Field(
        ...,
        description="实体定义，必须说明该实体是什么"
    )
    entity_type: EntityType = Field(
        ...,
        description="实体粗分类"
    )
    evidence: List[Evidence] = Field(
        default_factory=list,
        description="节点登记证据"
    )
    confidence: Confidence = Field(
        default=Confidence.LOW
    )
    status: NodeStatus = Field(
        default=NodeStatus.PENDING
    )
    notes: Optional[str] = None
    is_test: bool = Field(default=False, description="标记是否为测试数据")

    # DB timestamps (not required for input, populated by storage)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("canonical_name_zh", "definition")
    @classmethod
    def non_empty_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_evidence_policy(self) -> "IndustrialNode":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence node must have evidence")

        if self.status == NodeStatus.ACTIVE and not self.evidence:
            raise ValueError("ACTIVE node must have evidence")

        return self


class IndustryNodeAssociation(BaseModel):
    """创建节点时同时关联行业的输入项。字段都有默认值，前端通常只需传 industry_id。"""
    industry_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
    )
    role: Optional[str] = Field(default=None, description="节点在该行业中的角色")
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="关联权重")
    confidence: Confidence = Field(default=Confidence.MEDIUM, description="关联置信度")
    status: NodeStatus = Field(default=NodeStatus.ACTIVE, description="映射状态")
    notes: Optional[str] = Field(default=None, description="备注")


class IndustrialNodeCreate(BaseModel):
    """用于创建节点的输入模型（不含自动生成的字段）"""
    node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
    )
    canonical_name_zh: str
    canonical_name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    definition: str
    entity_type: EntityType
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.PENDING
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")
    industry_ids: List[IndustryNodeAssociation] = Field(
        default_factory=list,
        description="创建节点时同时关联的行业",
    )

    @field_validator("canonical_name_zh", "definition")
    @classmethod
    def non_empty_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_evidence_policy(self) -> "IndustrialNodeCreate":
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence node must have evidence")
        if self.status == NodeStatus.ACTIVE and not self.evidence:
            raise ValueError("ACTIVE node must have evidence")
        return self


class IndustrialNodeUpdate(BaseModel):
    """用于更新节点的输入模型"""
    canonical_name_zh: Optional[str] = None
    canonical_name_en: Optional[str] = None
    aliases: Optional[List[str]] = None
    definition: Optional[str] = None
    entity_type: Optional[EntityType] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    status: Optional[NodeStatus] = None
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")


class IndustrialNodeQuickCreate(BaseModel):
    """用于快速创建草稿节点的输入模型。只需要中文名或英文名之一，其余字段由系统填充默认值。"""
    node_id: Optional[str] = Field(
        default=None,
        pattern=r"^[a-z][a-z0-9_]*$",
        min_length=3,
        max_length=64,
        description="可选；不提供时系统自动生成 draft_{uuid} 占位 ID，后续由 AI 或管理员替换为规范 snake_case ID",
    )
    canonical_name_zh: Optional[str] = Field(
        default=None,
        description="中文标准名；与 canonical_name_en 至少填一个",
    )
    canonical_name_en: Optional[str] = Field(
        default=None,
        description="英文标准名；与 canonical_name_zh 至少填一个",
    )
    aliases: List[str] = Field(default_factory=list)
    definition: Optional[str] = Field(
        default=None,
        description="实体定义；留空表示待补充",
    )
    entity_type: Optional[EntityType] = Field(
        default=EntityType.UNKNOWN,
        description="实体粗分类；留空默认为 unknown",
    )
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.PENDING
    notes: Optional[str] = Field(
        default=None,
        description="可记录'由人工快速添加，待 AI 补全'等备注",
    )
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")
    industry_ids: List[IndustryNodeAssociation] = Field(
        default_factory=list,
        description="创建节点时同时关联的行业",
    )

    @model_validator(mode="after")
    def validate_name_present(self) -> "IndustrialNodeQuickCreate":
        if not (self.canonical_name_zh and self.canonical_name_zh.strip()) and \
           not (self.canonical_name_en and self.canonical_name_en.strip()):
            raise ValueError("canonical_name_zh 和 canonical_name_en 至少填写一个")
        return self


# ============================================================
# Edge Base
# ============================================================

class BaseEdge(BaseModel):
    edge_uuid: UUID = Field(default_factory=uuid4)

    edge_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="稳定英文小写蛇形命名"
    )
    from_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="起点节点ID"
    )
    to_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="终点节点ID"
    )
    description: str = Field(
        ...,
        description="必须说明 from_node 对 to_node 的作用"
    )
    evidence: List[Evidence] = Field(
        default_factory=list
    )
    confidence: Confidence = Field(
        default=Confidence.LOW
    )
    notes: Optional[str] = None
    is_test: bool = Field(default=False, description="标记是否为测试数据")

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("description")
    @classmethod
    def description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_common_edge_policy(self) -> "BaseEdge":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")

        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")

        return self


# ============================================================
# Industrial Flow Edge
# ============================================================

class IndustrialFlowEdge(BaseEdge):
    edge_namespace: Literal["industrial_flow"] = "industrial_flow"
    edge_type: IndustrialFlowType

    @computed_field
    @property
    def edge_type_label(self) -> str:
        return EDGE_TYPE_LABELS.get(self.edge_type.value, self.edge_type.value)

    @model_validator(mode="after")
    def validate_industrial_flow_policy(self) -> "IndustrialFlowEdge":
        if not self.description.strip():
            raise ValueError("industrial_flow edge must have description")
        return self


class IndustrialFlowEdgeCreate(BaseModel):
    edge_namespace: Literal["industrial_flow"] = "industrial_flow"
    edge_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    from_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    to_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    edge_type: IndustrialFlowType
    description: str
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")

    @field_validator("description")
    @classmethod
    def description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_policy(self) -> "IndustrialFlowEdgeCreate":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")
        return self


class IndustrialFlowEdgeQuickCreate(BaseModel):
    """用于快速创建产业流关系的输入模型。只需提供起点和终点节点，其余字段由系统填充默认值。"""
    edge_id: Optional[str] = Field(
        default=None,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="可选；不提供时自动生成 {from_node}_to_{to_node} 或 draft_{uuid} 占位 ID",
    )
    from_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="上游节点 ID，为下游节点提供输入",
    )
    to_node: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="下游节点 ID，接收上游节点的输入",
    )
    edge_type: IndustrialFlowType = Field(
        default=IndustrialFlowType.MATERIAL_INPUT,
        description="关系类型；留空默认 material_input",
    )
    description: Optional[str] = Field(
        default=None,
        description="关系描述；留空自动生成",
    )
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = Field(
        default=None,
        description="备注",
    )
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")

    @model_validator(mode="after")
    def validate_policy(self) -> "IndustrialFlowEdgeQuickCreate":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")
        return self


class IndustrialFlowEdgeUpdate(BaseModel):
    edge_type: Optional[IndustrialFlowType] = None
    description: Optional[str] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")
    from_node: Optional[str] = Field(default=None, pattern=r"^[a-z][a-z0-9_]*$")
    to_node: Optional[str] = Field(default=None, pattern=r"^[a-z][a-z0-9_]*$")


# ============================================================
# Reified Edge (PROV-style Usage)
# ============================================================

class ReifiedUsageCreate(BaseModel):
    """物化边：创建 Usage 节点来表达 process_execution --uses--> technology。"""
    execution_node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="执行工艺节点 ID（如 pre_lithography_wafer_cleaning）",
    )
    technology_node_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="被使用的通用技术/方法节点 ID（如 wafer_cleaning_process）",
    )
    scenario: Optional[str] = Field(
        default=None,
        description="使用场景，用于区分同一对执行-技术的不同用法",
    )
    role: Optional[str] = Field(
        default=None,
        description="在该场景下扮演的角色",
    )
    description: Optional[str] = Field(
        default=None,
        description="Usage 节点描述；留空自动生成",
    )
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.PENDING
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")

    @model_validator(mode="after")
    def validate_policy(self) -> "ReifiedUsageCreate":
        if self.execution_node_id == self.technology_node_id:
            raise ValueError("execution_node_id and technology_node_id must be different")
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence reified usage must have evidence")
        return self


class ReifiedUsageResult(BaseModel):
    """物化边创建结果：Usage 节点 + 两条边。"""
    usage_node: IndustrialNode
    uses_edge: IndustrialFlowEdge
    technology_edge: IndustrialFlowEdge


# ============================================================
# Ontology Edge
# ============================================================

class OntologyEdge(BaseEdge):
    edge_namespace: Literal["ontology"] = "ontology"
    edge_type: OntologyType

    @computed_field
    @property
    def edge_type_label(self) -> str:
        return EDGE_TYPE_LABELS.get(self.edge_type.value, self.edge_type.value)

    @model_validator(mode="after")
    def validate_ontology_policy(self) -> "OntologyEdge":
        if self.edge_type == OntologyType.ALIAS_OF:
            text = self.description.lower()
            if (
                "alias" not in text
                and "别名" not in self.description
                and "同义" not in self.description
                and "译名" not in self.description
            ):
                raise ValueError(
                    "alias_of description should explain alias/synonym/translation relationship"
                )
        return self


class OntologyEdgeCreate(BaseModel):
    edge_namespace: Literal["ontology"] = "ontology"
    edge_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    from_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    to_node: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    edge_type: OntologyType
    description: str
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")

    @field_validator("description")
    @classmethod
    def description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_policy(self) -> "OntologyEdgeCreate":
        if self.from_node == self.to_node:
            raise ValueError("self-loop edge is not allowed")
        if self.confidence == Confidence.HIGH and not self.evidence:
            raise ValueError("HIGH confidence edge must have evidence")
        return self


class OntologyEdgeUpdate(BaseModel):
    edge_type: Optional[OntologyType] = None
    description: Optional[str] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    notes: Optional[str] = None
    is_test: Optional[bool] = Field(default=False, description="标记是否为测试数据")
    from_node: Optional[str] = Field(default=None, pattern=r"^[a-z][a-z0-9_]*$")
    to_node: Optional[str] = Field(default=None, pattern=r"^[a-z][a-z0-9_]*$")


# 使用 discriminator，确保根据 edge_namespace 自动解析为正确 Edge 类型
GraphEdge = Annotated[
    Union[IndustrialFlowEdge, OntologyEdge],
    Field(discriminator="edge_namespace")
]

GraphEdgeCreate = Annotated[
    Union[IndustrialFlowEdgeCreate, OntologyEdgeCreate],
    Field(discriminator="edge_namespace")
]


# ============================================================
# Rejected / Pending Items
# ============================================================

class RejectedOrPendingItem(BaseModel):
    term: str = Field(
        ...,
        description="被拒绝或待确认的候选词"
    )
    reason: str = Field(
        ...,
        description="拒绝或待确认原因"
    )
    suggested_action: ReviewAction
    evidence: List[Evidence] = Field(
        default_factory=list
    )
    notes: Optional[str] = None

    @field_validator("term", "reason")
    @classmethod
    def non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("field cannot be empty")
        return v


# ============================================================
# Registration Output Batch
# ============================================================

class GraphRegistrationBatch(BaseModel):
    batch_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$"
    )
    task_description: str

    nodes_to_upsert: List[IndustrialNode] = Field(
        default_factory=list
    )
    edges_to_upsert: List[GraphEdge] = Field(
        default_factory=list
    )
    rejected_or_pending: List[RejectedOrPendingItem] = Field(
        default_factory=list
    )

    @field_validator("task_description")
    @classmethod
    def task_description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("task_description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_no_duplicate_node_ids(self) -> "GraphRegistrationBatch":
        node_ids = [node.node_id for node in self.nodes_to_upsert]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("duplicate node_id found")
        return self

    @model_validator(mode="after")
    def validate_no_duplicate_edge_ids(self) -> "GraphRegistrationBatch":
        edge_ids = [edge.edge_id for edge in self.edges_to_upsert]
        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("duplicate edge_id found")
        return self


# ============================================================
# Candidate Input Schema
# ============================================================

class CandidateEntity(BaseModel):
    term: str = Field(
        ...,
        description="候选实体名称"
    )
    context: Optional[str] = Field(
        default=None,
        description="候选词出现的上下文"
    )
    source: Optional[Evidence] = Field(
        default=None
    )

    @field_validator("term")
    @classmethod
    def term_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("term cannot be empty")
        return v


class CandidateRelation(BaseModel):
    from_term: str = Field(
        ...,
        description="候选关系的起点词，未必是最终节点ID"
    )
    to_term: str = Field(
        ...,
        description="候选关系的终点词，未必是最终节点ID"
    )
    proposed_relation: Optional[str] = Field(
        default=None,
        description="资料中暗示的关系，未必是最终登记关系"
    )
    context: Optional[str] = None
    source: Optional[Evidence] = None

    @field_validator("from_term", "to_term")
    @classmethod
    def terms_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("term cannot be empty")
        return v


class GraphRegistrationInput(BaseModel):
    task_id: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$"
    )
    task_description: str

    candidate_entities: List[CandidateEntity] = Field(
        default_factory=list
    )
    candidate_relations: List[CandidateRelation] = Field(
        default_factory=list
    )

    instructions: Optional[str] = Field(
        default=None,
        description="本次登记的额外说明"
    )

    @field_validator("task_description")
    @classmethod
    def task_description_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("task_description cannot be empty")
        return v


# ============================================================
# Response wrappers
# ============================================================

class PaginatedNodes(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[IndustrialNode]


class PaginatedEdges(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[GraphEdge]


class GraphStats(BaseModel):
    total_nodes: int
    total_edges: int
    node_type_distribution: dict
    edge_namespace_distribution: dict
    edge_type_distribution: dict
    status_distribution: dict
    confidence_distribution: dict


class SubgraphResult(BaseModel):
    center_node_id: str
    depth: int
    nodes: List[IndustrialNode]
    edges: List[GraphEdge]


class PathResult(BaseModel):
    from_node: str
    to_node: str
    paths: List[List[dict]]
