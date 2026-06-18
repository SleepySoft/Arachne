# 产业本体设计规则

> 本文档与 `backend/app/services/ontology_rules.py` 共同维护。新增或修改规则时，请先更新 `ontology_rules.py`，再同步本文档，并确保对应 checker 已注册到 `backend/app/services/db_checkers.py`。

---

## 1. 节点粒度实践

### 1.1 物料节点（material）

物料节点是最容易出现粒度漂移的类型。一个名称在不同语境下可能指“化学元素”“工程材料”“中间产品”或“成品零部件”。推荐按以下分层建模：

| 层级 | 说明 | 示例 | entity_type |
|---|---|---|---|
| 元素/基础化学品 | 自然界或化工厂的基础形态，未针对电子/半导体场景加工 | `silicon`（硅元素）、`tungsten_hexafluoride` | `material` |
| 工程材料/基材 | 已经过提纯、掺杂、成型，面向特定工艺环节 | `silicon_wafer`（硅片）、`photoresist`（光刻胶）、`sputtering_target`（溅射靶材） | `material` |
| 工艺耗材 | 在使用过程中被消耗，不进入最终产品结构 | `cmp_slurry`（CMP 研磨液）、`wet_chemicals`（湿电子化学品） | `material` |
| 中间产品 | 已完成部分制造流程，可作为下游工序输入 | `wafer`（晶圆）、`polyester_chip`（聚酯切片） | `component` / `material` 视场景而定 |

**命名与建模约定：**

1. **避免大而泛的“XX材料”节点。** 如果确实要登记“半导体材料”这类集合概念，应作为抽象分类节点，通过 `is_a` 连接具体材料；不应用它直接参与 material_flow。
2. **形态要在 node_id 和中文名中体现。** 例如 `silicon_wafer` 比 `silicon` 更准确；`polyester_pellet` 比 `polyester_chip` 更不容易与芯片混淆。
3. **元素 ≠ 材料 ≠ 产品。**
   - 元素是材料的一种：`silicon_wafer is_a semiconductor_material`、`silicon is_a raw_material`（或 `chemical_element`）。
   - 材料流入工艺：`silicon_wafer --material_flow--> wafer_manufacturing`。
   - 材料不要直接 `composition` 进入产品；composition 只用于“零部件/模块/子系统构成系统”。
4. **material_flow 只用于“作为输入被消耗/转化”。** 如果上游只是“检测/测量”下游，应使用 `information_flow` 或 `capability_supply`。

### 1.2 工艺/制造环节节点（process）

`process` 填补了“设备/材料 → 产品”之间的空白，但也很容易成为粒度大杂烩。建议分层：

| 粒度 | 说明 | 示例 |
|---|---|---|
| 单步工艺（unit_process） | 制造流程中的单一物理/化学步骤 | `lithography_process`、`etching_process`、`ion_implantation_process` |
| 完整制造流程（flow） | 由多个单步工艺组成的端到端流程 | `wafer_manufacturing`、`chip_packaging` |
| 设计/服务流程（service_process） | 不直接改变物理形态，但为制造提供输出 | `chip_design`、`failure_analysis` |

**约定：**

1. 设备（device）必须指向 `process` / `service` / `technology_capability`，不能直接指向产品（component 及以上）。
2. 材料（material）也应指向 `process`，由 `process` 输出产品或半成品。
3. 同一流程内的单步工艺之间可以用 `composition` 或 `information_flow` 连接，但不要把单步工艺直接 material_flow 到最终产品；应通过完整 flow 节点中转。
4. 未来可在节点属性中增加 `process_stage`（front_end / back_end / packaging / testing）来统一分类。

---

## 2. 规范流程模式

推荐用以下“漏斗型”结构描述从输入到产品的转化：

```text
材料/输入物  --material_flow-->  工艺过程
设备/能力    --capability_supply-->  工艺过程
设计数据     --information_flow-->  工艺过程

工艺过程     --produces-->  产物 / 中间产物
中间产物     --material_flow-->  下游工艺过程 或 下游产物
```

**说明：**

- `produces` 专门用于“工艺过程 → 产出”，语义上比 `material_flow` 更精确。
- 当产物继续作为下游输入时，仍使用 `material_flow`（也可理解为 `processes_into` 的语义）。
- 禁止材料、设备、能力直接 `material_flow` / `capability_supply` / `information_flow` 到产品节点。

**示例：**

```text
硅片 --material_flow--> 晶圆制造 --produces--> 晶圆
光刻机 --capability_supply--> 光刻工艺
光刻工艺 --composition--> 晶圆制造
晶圆 --material_flow--> 芯片封装 --produces--> 芯片
```

---

## 2. 规则注册表

| 规则 ID | 名称 | 严重级别 | 自动修复 | 类别 | Checker ID | 说明 |
|---|---|---|---|---|---|---|
| R01 | 节点关键属性必须完整 | WARNING | × | node | `missing_node_properties` | 节点必须提供 canonical_name_zh、definition、entity_type |
| R02 | ACTIVE / HIGH 置信度节点必须有证据 | ERROR | × | quality | `high_confidence_missing_evidence` | HIGH confidence 节点必须带 evidence |
| R03 | ACTIVE 节点必须有证据 | WARNING | × | quality | `active_status_missing_evidence` | ACTIVE 节点必须带 evidence |
| R04 | 禁止重复节点中文名 | WARNING | × | node | `duplicate_node_names` | 多个非草稿节点不能同名 |
| R05 | 禁止自环关系 | ERROR | √ | edge | `self_loops` | 起点终点不能相同 |
| R06 | 禁止重复关系 | ERROR | √ | edge | `duplicate_edges` | 同一对节点同 namespace+type 只能一条 |
| R07 | 产业流关系必须有描述 | WARNING | × | edge | `missing_industrial_flow_description` | INDUSTRIAL_FLOW 边必须有 description |
| R08 | 双向产业流冲突需确认 | WARNING | × | edge | `reverse_industrial_flow` | A→B 和 B→A 同时存在需人工确认 |
| R09 | 本体关系禁止成环 | ERROR | × | ontology | `ontology_cycle` | ONTOLOGY 关系不能成环 |
| R10 | 本体关系禁止双向冲突 | ERROR | × | ontology | `ontology_symmetric_conflict` | 同类型 ONTOLOGY 双向关系禁止 |
| R11 | alias_of 关系必须说明别名类型 | WARNING | × | ontology | `alias_of_description` | alias_of 描述需说明别名类型 |
| R12 | 公司和产业实体在产业图中必须隔离 | ERROR | √ | cross_domain | `entity_domain_boundary` | :Company 与 :IndustrialNode 之间不能连边 |
| R13 | 设备类节点不直接指向产品节点 | ERROR | √ | edge | `device_to_product_direct_edge` | device 必须通过 process/service/capability 中转 |
| R14 | 悬挂关系必须清理 | ERROR | √ | edge | `dangling_edges` | 边端点必须是存在的 IndustrialNode |
| R15 | 行业映射和公司暴露不能悬空 | ERROR | √ | cross_domain | `dangling_industry_mappings` / `dangling_company_exposures` | 桥接表 node_id 必须在 Neo4j 中存在 |
| R16 | 孤立节点需审查 | WARNING | × | quality | `orphan_nodes` | 无连接的节点需审查 |
| R17 | 输入物/设备/能力不直接指向产品 | WARNING | × | edge | `input_to_product_direct_edge` | material/device/capability 必须先指向 process |

---

## 3. 关键规则详解

### R12 公司与产业实体隔离

**规则：** Neo4j 产业图（`:IndustrialNode`）中不能出现 `:Company` 标签的节点，也不能存在公司与产业实体之间的边。

**理由：** 公司属于“事实图”（Factual Graph），产业节点属于“本体图”。公司与产业节点的关联应通过 PostgreSQL 桥接表实现，例如 `company_node_exposures`。

**示例：** 以下关系必须删除：

```cypher
(:Company)-[:INDUSTRIAL_FLOW]->(:IndustrialNode)
(:IndustrialNode)-[:ONTOLOGY]->(:Company)
```

### R13 设备类节点不直接指向产品节点

**规则：** `entity_type='device'` 的节点不能通过 `INDUSTRIAL_FLOW` 直接指向以下“产品”类节点：
`component`、`module`、`subsystem`、`system`、`platform`、`application_system`。

**理由：** 设备本身不是下游产品的直接输入，而是通过工艺/制造环节作用于产品。直接连边会掩盖产业链的真实结构。

**反例：**

```text
lithography_machine --material_flow--> wafer
etching_machine --material_flow--> chip
```

**正例：**

```text
lithography_machine --capability_supply--> lithography_process
photoresist --material_flow--> lithography_process
lithography_process --material_flow--> wafer_manufacturing
wafer_manufacturing --produces--> wafer
```

### R17 输入物/设备/能力不直接指向产品

**规则：** `material`、`device`、`technology_capability` 类型的节点不能通过 `material_flow` / `capability_supply` / `information_flow` 直接指向 `component` / `module` / `subsystem` / `system` / `platform` / `application_system` 等产品类节点。

**理由：** 这违反了“输入 → 工艺过程 → 产出”的规范流程。原材料、设备、软件/数据能力都需要经过工艺/制造环节才能转化为产品。

**反例：**

```text
铝 --material_flow--> 活塞
EDA软件 --capability_supply--> 芯片
```

**正例：**

```text
铝 --material_flow--> 压铸工艺 --produces--> 活塞
EDA软件 --information_flow--> 芯片设计 --produces--> 芯片
```

---

## 4. 如何新增规则

1. 在 `backend/app/services/ontology_rules.py` 的 `ONTOLOGY_RULES` 列表中添加 `OntologyRule`。
2. 若需要自动检查，在 `backend/app/services/db_checkers.py` 中实现对应的 `Checker` 子类，并用 `@register_checker` 注册；checker 的 `check_id` 与规则 `checker_id` 一致。
3. 更新本文档的规则表和详解。
4. 运行 `POST /api/v1/admin/db-checks/run-all` 验证新规则。

---

## 5. 相关文档

- `docs/ontology_design_practice_avoid_broad_nodes.md` —— 避免大而泛节点与 composition/material_flow 边界
- `backend/app/services/db_checkers.py` —— 检查器实现
- `backend/app/services/ontology_rules.py` —— 规则注册表（代码侧单一事实来源）
