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

---

## 2. PROV 概念到产业图的映射

| PROV 概念 | 对应产业图对象 | 备注 |
|---|---|---|
| `Entity` | `IndustrialNode` | 原材料、中间品、产品、设备等 |
| `Activity` | `IndustrialNode`（`entity_type = process`） | 工艺/加工活动 |
| `Agent` | 暂不处理 | 未来可对接 Factual Graph 的 `Company` / `Person` |

---

## 3. PROV 关系到产业图关系的映射

| PROV 关系 | 产业图含义 | 遍历方式 |
|---|---|---|
| `used(Activity, Entity)` | Activity 使用了某个 Entity | 沿 `material_input` 边查找 |
| `wasGeneratedBy(Entity, Activity)` | Entity 由某个 Activity 生成 | 沿 `process_output` 边查找 |
| `wasDerivedFrom(Entity, Entity)` | 一个 Entity 派生自另一个 Entity | 通过 `process_output → Activity → material_input` 路径推导；**允许经过 `is_a` 节点** |

---

## 4. 关键规则

1. **不讨论批次**：所有 PROV 声明均为类型级模板，描述“一个典型 X 是如何生成的”。
2. **遍历允许经过 `is_a` 节点**：因为 PROV 过程可能引入通用节点，派生路径可以通过本体层级向上/向下扩展。
3. **原料输入总能在工艺侧找到**：不存在“多个原料无法对应到产品”的问题；中间工艺输入的原料可通过相关 Activity 节点定位。
4. **PROV 与“强相关”语义分离**：PROV 描述生成/使用/派生，不描述重要性、关键性、替代性。
5. **缺失校验**：PROV 声明中 target_node_id 必须在产业图中存在；若不存在，提示补全或标记为缺失。

---

## 5. 交互设计

- **选中实体节点时**，按 PROV 链向上游高亮涉及的 Activity 和输入 Entity。
- **未涉及节点变淡**，以区分 PROV 视图与默认工艺视图。
- **缺失节点标红**，并给出补全建议。
- **PROV 视图开关**：用户可随时切换“工艺视图”与“来源视图”。

---

## 6. 实现状态

**已实现：**

- 文件存储：`data/prov_statements/{node_id}.provn`（已从 PostgreSQL `prov_statements` 迁移，格式为 W3C PROV-N）
- 后端模型：`backend/app/models/prov_schema.py`
- 存储层：`backend/app/services/prov_storage.py`
- REST API：`backend/app/routers/prov.py`，挂载在 `/api/v1/prov`
- PROV-N 解析/序列化：`backend/app/services/prov_n.py`
- 前端集成：`NodeProvPanel`（关系列表 / PROV-N 源码双视图）、节点详情 PROV 区、右键菜单 "查看 PROV"

**待后续决定的问题：**

- 是否允许从 PROV 视图一键写回产业图关系（如补全缺失的 `material_input`）。
- `wasDerivedFrom` 的具体推导算法（路径长度、`is_a` 跳跃次数限制等）。
- PROV 在画布上的高亮/投影逻辑（目前只在右侧面板展示）。

---

## 7. 与“关键原料”语义层的关系

```
产业图主模型
├── industrial_flow      # 工艺流程
├── ontology             # is_a / part_of / related_term
└── material_trace       # key_input_for / enables（关键原料/使能关系）

PROV 覆盖层（只读/校验）
├── used                 # 对应 material_input
├── wasGeneratedBy       # 对应 process_output
└── wasDerivedFrom       # 由工艺流程推导
```

PROV 和 `material_trace` 是平行且互不替代的两层。
