# PROV 覆盖层设计记录

> 记录与 PROV-DM 结合的产业图设计结论，作为后续实现的依据。
> 本文不讨论具体实现，只固化架构约定。

---

## 1. 核心结论

1. **产业图保持为主模型**：现有的 `industrial_flow`、`ontology` 关系层不变。
2. **PROV 是覆盖层/视图层**：用于表达类型级实体的标准生成路径，并作为产业图的完整性校验器。
3. **永远不讨论批次**：本项目只使用类型级（class-level）PROV 描述，不追踪具体实例/批次。
4. **PROV entity / activity 映射到产业图节点**：以 `node_id` 为唯一对应键，不以中文名或别名对应。
5. **PROV 不表达“强相关/关键性”**：`gallium_nitride → power_device` 这类关键原料关系仍应使用独立的产业语义层（如 `key_input_for`）。
6. **`wasDerivedFrom` 需要独立语义**：现有 `industrial_flow` 只有 `material_input` / `process_output` 等过程级边，无法直接表达“Entity A 派生自 Entity B”。需要在图中新增 `derived_from` 语义。
7. **`derived_from` 是显式、临时的物料血缘视图**：它只表达“强关联的直接物料派生”，必须人工创建，不能由现有工艺图自动推论，且默认不显示在画布上。

---

## 2. PROV 概念到产业图对象的映射

| PROV 概念 | 对应产业图对象 | 备注 |
|---|---|---|
| `Entity` | `IndustrialNode`（大部分 `entity_type`） | 原材料、中间品、产品、部件、设备、系统、软件、数据资产等 |
| `Activity` | `IndustrialNode`（`entity_type = process`） | 工艺/加工/检测/运营活动 |
| `Agent` | 暂不直接映射 | 未来可对接 Factual Graph 的 `Company` / `Person`；当前 PROV 声明中 `agent` 仅作角色标记，不绑定产业图节点类型 |

### 2.1 `EntityType` → PROV 角色映射

| 产业图 `EntityType` | 默认 PROV 角色 | 说明 |
|---|---|---|
| `material` | `entity` | 物质性输入，可被 `used`；可作为 `derived_from` 的来源或目标 |
| `part` | `entity` | 结构件/部件，可被 `used` 或作为 `wasDerivedFrom` 的端点 |
| `device` | `entity` | 功能器件/终端 |
| `equipment` | `entity` | 生产/检测设备，通常作为 `used` 的仪器 |
| `system` | `entity` | 复合系统 |
| `software` | `entity` | 数字制品 |
| `infrastructure` | `entity` | 基础承载资源 |
| `process` | `activity` | 唯一默认映射为 PROV `activity` 的类型 |
| `service` | `entity`（可降级/提升） | 服务成果可视为 `entity`；若强调服务过程，可标记为 `activity` |
| `technology_capability` | `entity` | 能力域作为可被引用的产业实体 |
| `platform` | `entity` | 平台型实体 |
| `standard` | `entity` | 规范/协议/标准 |
| `data_asset` | `entity` | 数据资源/数据集 |
| `unknown` | `entity` | 待分类节点，默认按 `entity` 处理 |

> **原则**：除 `process` 明确为 `activity` 外，其余类型先统一视为 `entity`。具体 PROV 声明里仍可通过 `node_role` / `target_role` 覆盖。

---

## 3. PROV 关系到产业图关系的映射

| PROV 关系 | 产业图含义 | 对应 `IndustrialFlowType` | 创建方式 |
|---|---|---|---|
| `used(Activity, Entity)` | Activity 使用了某个 Entity | `material_input` / `energy_input` / `information_input` / `equipment_enablement` | 由工艺图直接创建 |
| `wasGeneratedBy(Entity, Activity)` | Entity 由某个 Activity 生成 | `process_output` | 由工艺图直接创建 |
| `wasDerivedFrom(Entity, Entity)` | 一个 Entity 在物料上直接派生自另一个 Entity | **`derived_from`** | **必须显式人工创建**，不能由工艺路径自动推论 |
| `wasAssociatedWith(Activity, Agent)` | Activity 与 Agent 关联 | 暂不实现 | 未来对接 Factual Graph |
| `wasAttributedTo(Entity, Agent)` | Entity 归因于 Agent | 暂不实现 | 未来对接 Factual Graph |
| `actedOnBehalfOf(Agent, Agent)` | Agent 代表 Agent | 暂不实现 | 未来对接 Factual Graph |

### 3.1 `IndustrialFlowType` → PROV 语义详细对照

| `IndustrialFlowType` | PROV 语义 | 端点方向（from → to） | 示例 |
|---|---|---|---|
| `material_input` | `used` | `entity` → `activity` | `silicon_wafer → wafer_manufacturing` 表示 `wafer_manufacturing used silicon_wafer` |
| `energy_input` | `used` | `entity` → `activity` | `electricity → wafer_manufacturing` |
| `information_input` | `used` | `entity` → `activity` | `design_data → lithography_process` |
| `equipment_enablement` | `used` | `entity` → `activity` | `lithography_machine → lithography_process` |
| `process_output` | `wasGeneratedBy` | `activity` → `entity` | `wafer_manufacturing → wafer` 表示 `wafer wasGeneratedBy wafer_manufacturing` |
| `service_provision` | `wasAssociatedWith` / `used` | `activity/entity` → `entity` | 检测服务与检测活动的关联 |
| `capability_enablement` | `wasAssociatedWith` | `entity` → `activity` | 某技术能力使能某工艺 |
| `structural_composition` | **无直接 PROV 对应** | `entity` → `entity` | 结构组成（A 是 B 的组成部分）属于装配/本体关系；既不是 `derived_from`，也不是其反向 |
| `supply_relation` | **无直接 PROV 对应** | `entity` → `entity` | 摘要级供应关系，太抽象，不归入 PROV |
| `derived_from`（新增） | `wasDerivedFrom` | `entity` → `entity` | `tested_chip → silicon_wafer`、`gallium_nitride → gallium` |

---

## 4. 关键规则

1. **不讨论批次**：所有 PROV 声明均为类型级模板，描述“一个典型 X 是如何生成的”。
2. **PROV 与“强相关”语义分离**：PROV 描述生成/使用/派生，不描述重要性、关键性、替代性。
3. **缺失校验**：PROV 声明中 `target_node_id` 必须在产业图中存在；若不存在，提示补全或标记为缺失。
4. **`derived_from` 不替代工艺边**：`material_input` / `process_output` 仍是主模型；`derived_from` 是它们之上的**显式派生摘要**，只在临时视图中展示。
5. **`derived_from` 必须显式创建**：当前架构下不能从工艺图自动推论；创建时需要人工判断并附证据。

---

## 5. 交互设计

- **选中实体节点时**，按 PROV 链向上游高亮涉及的 Activity 和输入 Entity。
- **未涉及节点变淡**，以区分 PROV 视图与默认工艺视图。
- **缺失节点标红**，并给出补全建议。
- **PROV 视图开关**：用户可随时切换“工艺视图”与“来源视图”。
- **物料派生视图（新增）**：通过独立开关/按钮进入，只展示 `derived_from` 边。默认关闭，避免污染主图布局。

---

## 6. 实现状态

**已实现：**

- 文件存储：`data/prov_statements/{node_id}.prov.json`（已从 PostgreSQL `prov_statements` 迁移；早期实验性的 PROV-N 格式已弃用，parser 代码保留但不再被主代码引用）
- 后端模型：`backend/app/models/prov_schema.py`
- 存储层：`backend/app/services/prov_storage.py` + `backend/app/services/prov_n.py`
- REST API：`backend/app/routers/prov.py`，挂载在 `/api/v1/prov`
- 前端集成：`NodeProvPanel`、节点详情 PROV 区、右键菜单 "查看 PROV"

**待实现（按本设计推进）：**

- ✅ 在 `IndustrialFlowType` 中增加 `derived_from`（schema 标签已添加）。
- ✅ 后端 `derived_from` 策略校验：端点不能是 process、不能指向通用耗材、防重复、防环。
- ✅ 前端过滤面板增加“显示物料派生边（derived_from）”开关，默认关闭；关闭时边被隐藏且不参与布局和邻近展开。
- ✅ `derived_from` 边已被排除在公司探索/物料关联等传统上下游查询之外。
- 为 `derived_from` 增加更明显的创建入口（当前与普通边共用表单，后续可加专用快捷入口）。
- 将人工创建的 `derived_from` 边同步写回 JSON PROV 文件（`wasDerivedFrom`），标记 `is_inferred = false`。

---

## 7. 缺失的 `wasDerivedFrom` 语义设计

### 7.1 为什么缺失

当前产业图只有过程级边：

```
material_input:    silicon_wafer → wafer_manufacturing
process_output:    wafer_manufacturing → wafer
```

这两条边合在一起可以在逻辑上推出 `wafer wasDerivedFrom silicon_wafer`，但图中**没有显式的派生边**。更关键的是：

- 工艺图里大量通用消耗品（纯水、电、压缩空气、普通清洗剂）也会作为 `material_input` 出现；
- 如果把这些输入都当成“派生来源”，`wasDerivedFrom` 会失去聚焦，导致图极度混乱；
- 因此 `wasDerivedFrom` 不能由现有工艺图自动推论，必须作为**人工判断的强关联声明**单独存在。

### 7.2 设计目标

1. **显式表达强物料派生**：只记录“某产物在物料身份上直接来源于某原料/中间品”。
2. **跳过工艺流程**：`derived_from` 不描述具体工艺步骤，只描述起点和终点之间的物料血缘。
3. **人工创建、人工负责**：当前架构下不能自动推论；创建时必须提供证据和置信度。
4. **默认隐藏、临时查看**：避免污染主图和常规上下游关系。
5. **类型级**：仍然不讨论批次，只描述“典型 X 在物料上直接派生自典型 Y”。

### 7.3 新增 `derived_from` 工业流边

- **类型名**：`IndustrialFlowType.DERIVED_FROM = "derived_from"`
- **标签**：`派生自`
- **方向**：`from_node` 为派生体（下游产物），`to_node` 为来源体（上游原料/中间品）。
  - 即 `from_node --derived_from--> to_node` 对应 PROV `wasDerivedFrom(from_node, to_node)`。
- **端点约束**：
  - 两端都必须是 `entity` 类型节点（`entity_type != process`）。
  - 两端都应是具有明确物料身份的产业实体。
- **与现有边的区别**：
  - `material_input`：从 entity 指向 process，表示“被某个工艺使用”。
  - `process_output`：从 process 指向 entity，表示“被某个工艺生成”。
  - `derived_from`：从 entity 指向 entity，表示“在物料身份上直接派生自”。

### 7.4 `derived_from` 与 `structural_composition` 的区别

`structural_composition`（A 是 B 的结构组成部分）**不是** `derived_from`，也不是它的反向。

| 维度 | `structural_composition` | `derived_from` |
|---|---|---|
| 语义 | 装配关系：A 作为部件存在于 B 中 | 物料血缘：B 在物料身份上来源于 A |
| 方向 | `component → whole`（部件指向整体） | `product → source`（产物指向来源） |
| 示例 | `bearing → motor`（轴承是电机的部件） | `motor derived_from copper`（电机在物料上来源于铜） |
| 是否跳过工艺 | 与工艺无关 | 跳过具体工艺步骤 |
| PROV 对应 | 无 | `wasDerivedFrom` |

因此，**不要因为一个部件属于某个整体，就写 `whole derived_from component`**。如果确实想表达“电机由铜线派生而来”，应该写 `motor derived_from copper_wire`，并且需要证据支持。

### 7.5 什么情况下应该创建 `derived_from`

**适合创建 `derived_from` 的场景：**

1. **产物与其决定性原料/中间品之间的直接血缘**：原料是产物物料身份的核心组成部分。
   - `wafer derived_from silicon_wafer`
   - `gallium_nitride derived_from gallium`
   - `tested_chip derived_from silicon_wafer`（类型级跨工艺摘要）
   - `gan_power_device derived_from gan_wafer`

2. **跨层派生**：产物与原料之间相隔多个工艺步骤，但物料血缘清晰且需要被单独探索。
   - `chip_die derived_from wafer`

**不应该创建 `derived_from` 的场景：**

1. **通用工艺消耗品**：纯水、电、压缩空气、普通清洗剂、通用溶剂、通用保护气体等。这些物质参与工艺，但不构成产物的物料身份。
   - ❌ `wafer derived_from deionized_water`
   - ❌ `wafer derived_from electricity`
2. **设备/工具**：设备是使能条件，不是物料来源。
   - ❌ `chip derived_from lithography_machine`
3. **能力/服务/软件**：这些不是物料实体。
   - ❌ `battery derived_from battery_thermal_management`
4. **仅“强相关/关键”但不构成物料身份**：应使用 `key_input_for` / `enables` 等独立语义层，而不是 `derived_from`。
   - ❌ `power_device derived_from gallium_nitride`（若仅表示“氮化镓对功率器件很关键”）

### 7.6 为什么不自动推导

理论上可以从工艺路径 `process_output → activity → material_input` 推导出“产物由哪些原料生成”，但实际会导致：

- **噪声爆炸**：每个产物都会关联到大量通用耗材和辅助材料。
- **语义降级**：把“使用”等同于“派生”，模糊了 PROV 的精确语义。
- **人工判断不可替代**：是否构成“物料身份上的直接派生”需要领域知识和证据，不能由图结构自动决定。

因此，当前架构下 **禁止自动推论 `derived_from`**。未来即使引入推导辅助，也应是“推荐候选，人工确认后写入”，而不是直接写边。

### 7.7 人工显式声明流程

1. 用户在“物料派生视图”或节点详情中点击“声明派生关系”。
2. 选择来源实体（必须是 material/part/device 等物料身份明确的实体）。
3. 填写证据（如原文摘录）、置信度、备注。
4. 系统校验：
   - 两端都不是 `process`；
   - 两端都不是通用消耗品（可通过标签/黑名单/人工审核实现）；
   - 不形成循环；
   - 不与已有 `derived_from` 重复。
5. 写入产业图 `derived_from` 边，并同步生成一条 `wasDerivedFrom` PROV 声明，`is_inferred = false`。

### 7.8 同步到 PROV 文件

由于 `derived_from` 是人工显式声明，它应该在 PROV 覆盖层有对应记录：

| 图中边 | PROV 声明 | `is_inferred` |
|---|---|---|
| `derived_from`（人工创建） | `wasDerivedFrom(...)` | `false` |
| 工艺路径推荐（未写入图的候选） | 不写入 PROV 文件 | - |

推荐做法：
- 仅在用户确认创建 `derived_from` 边后，才写入 `data/prov_statements/{node_id}.prov.json`；
- 前端“PROV 来源视图”和“物料派生视图”都读取同一份 JSON PROV 数据；
- 删除 `derived_from` 边时同步删除对应 PROV 声明。
- PROV-N 可以作为未来从产业图导出的*输出*格式，但不再是存储格式。

### 7.9 校验规则

1. **端点类型校验**：`derived_from` 两端不能是 `process`。
2. **端点语义校验**：两端应属于 `material` / `part` / `device` / `system` 等具有物料身份的实体；不建议使用 `service` / `technology_capability` / `infrastructure` / `platform` / `standard` / `software` / `data_asset`。
3. **通用消耗品黑名单**：`derived_from` 不应指向通用耗材（水、电、气、普通清洗剂等）。黑名单可维护在配置或本体标签中。
4. **不循环**：`derived_from` 图必须无环。
5. **不重复**：同一对 `(from_node, to_node)` 只能有一条 `derived_from` 边。
6. **证据要求**：`confidence = HIGH` 时必须有证据。

### 7.10 显示规则

- **默认不显示**：`derived_from` 边不出现在常规工艺画布、上游/下游查询、公司关联查询中。
- **独立开关**：通过“物料派生视图”按钮临时开启；开启时以叠加层形式渲染，不参与主布局（dagre）。
- **视觉样式**：建议使用虚线、低饱和度颜色（如灰蓝或暗橙），并在边标签上显示“派生自”。
- **临时性**：切换回工艺视图或刷新页面后，若未保存视图状态，则默认恢复隐藏。

### 7.11 迁移路径

1. 在 `backend/app/models/schemas.py` 的 `IndustrialFlowType` 中新增 `DERIVED_FROM = "derived_from"`。
2. 在 `EDGE_TYPE_LABELS` 中增加 `"derived_from": "派生自"`。
3. 在 `backend/app/routers/edges.py` 的创建/更新逻辑中增加 `derived_from` 的端点和语义校验。
4. 在 `backend/app/services/prov_sync.py`（新增）中实现 `derived_from` 边 ↔ PROV-N `wasDerivedFrom` 声明的双向同步。
5. 前端 `GraphCanvas` 增加 `derived_from` 边的独立渲染层和开关；默认不加载到主图中。
6. 为已有工艺链（芯片、功率半导体）人工补全一批 `derived_from` 边，并生成对应 PROV 声明。

---

## 8. 与“关键原料”语义层的关系

```
产业图主模型
├── industrial_flow
│   ├── material_input          # PROV: used
│   ├── process_output          # PROV: wasGeneratedBy
│   ├── derived_from            # PROV: wasDerivedFrom（显式、人工、默认隐藏）
│   ├── equipment_enablement    # PROV: used
│   └── ...
├── ontology                    # is_a / part_of / related_term
└── material_trace              # key_input_for / enables（关键原料/使能关系）

PROV 覆盖层（只读/校验）
├── used                        # 对应 material_input / energy_input / information_input / equipment_enablement
├── wasGeneratedBy              # 对应 process_output
└── wasDerivedFrom              # 对应 derived_from（显式、人工）
```

三层关系互不替代：
- **工艺流**（`material_input` / `process_output`）：回答“它在哪一步被怎么用/生成”。
- **物料派生**（`derived_from`）：回答“它在物料身份上直接来自什么原料”。
- **关键原料/使能**（`material_trace`）：回答“什么原料对它最关键/不可替代”。
