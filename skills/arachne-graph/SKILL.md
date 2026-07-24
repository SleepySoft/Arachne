---
name: arachne-graph
description: 指导 Kimi Agent 按照 Arachne 统一产业本体图规范，正确提交产业实体与关系数据，区分工业流、本体治理与 PROV 声明。
---

# Arachne Graph Registration Skill

## 用途

指导 Kimi Agent 按照 Arachne 统一产业本体图规范，正确提交产业实体与关系数据。

本 Skill 确保 Agent 输出严格符合 `GraphRegistrationBatch` Schema，能够被 Arachne 系统直接消费和落库。

## 适用场景

- 从研究报告、新闻、百科、招标文件中提取产业实体
- 判断候选词是否应登记为节点、合并到已有节点、或拒绝
- 构建产业流关系（上游 → 下游）
- 构建本体治理关系（别名、子类、变体、相关术语）
- 人工复核前的 Agent 预处理输出

## 核心约束

### 1. 节点必须是稳定产业实体

**不可以登记为节点：**
- 公司名称、股票代码、品牌商标
- 市场概念、投资题材、政策口号
- 宽泛应用标签（如"军用""民用""国产"）
- 简单修饰词组合

> 注意：市场概念、投资题材、产业链视图等不应作为节点，而应通过 `arachne-api` 技能登记为 `Industry`（`theme_view` / `curated_view` / `formal_industry`），并在其中引用已存在的产业节点。

**可以登记为节点：**
- 材料、部件、器件、模块、子系统、系统、平台、基础设施
- 应用系统、服务、技术能力
- 已形成稳定产品类别的专用设备（如"气象雷达""火控雷达"）

### 2. 关系方向 = 上游 → 下游

所有 `industrial_flow` 关系必须表示：
```
A → B = A 为 B 提供某种输入
```

输入类型：物质、组成部件、能量、信息、能力、服务

### 3. node_id 命名规范

- 小写蛇形命名：`^[a-z][a-z0-9_]*$`
- 最小长度 3，最大长度 64
- 必须稳定，一旦确定不轻易变更
- 示例：`lidar_system`, `phased_array_radar`, `silicon_wafer`

### 4. Evidence 要求

- `confidence: HIGH` 必须有至少一条 evidence
- `status: ACTIVE` 必须有至少一条 evidence
- evidence 必须包含：`source_title`（资料标题）和 `quote`（原文摘录）
- `source_url` 可选

### 5. 先做实体归一，再建关系

登记流程：
1. 读取候选实体与关系
2. 实体归一（判断别名 / 子类 / 变体 / 新实体）
3. 决策：新增 / 合并 / 拒绝 / 待确认 / 登记为行业（Industry）
4. 登记 ontology 关系（alias_of / is_a / variant_of）
5. 登记 industrial_flow 关系
6. 对于需要行业视图的场景，使用 `arachne-api` 技能创建 `Industry` 并添加 `IndustryNodeMapping`
7. （可选）为关键节点补充 PROV 声明，使用 `/api/v1/prov/statements`
8. 输出结构化结果

## 输出格式

必须输出标准 `GraphRegistrationBatch` JSON 结构：

```json
{
  "batch_id": "your_batch_id_001",
  "task_description": "本次登记的任务描述",
  "nodes_to_upsert": [
    {
      "node_id": "stable_node_id",
      "canonical_name_zh": "中文标准名",
      "canonical_name_en": "English Name",
      "aliases": ["别名1", "别名2"],
      "definition": "必须说明该实体是什么，技术原理、功能、输入输出。",
      "entity_type": "system",
      "evidence": [
        {
          "source_title": "资料标题",
          "source_url": "https://example.com",
          "quote": "支持该实体定义的原文摘录"
        }
      ],
      "confidence": "MEDIUM",
      "status": "PENDING",
      "notes": ""
    }
  ],
  "edges_to_upsert": [
    {
      "edge_id": "from_node_is_a_to_node",
      "edge_namespace": "ontology",
      "edge_type": "is_a",
      "from_node": "from_node_id",
      "to_node": "to_node_id",
      "description": "必须说明 from_node 对 to_node 的作用",
      "evidence": [],
      "confidence": "MEDIUM"
    }
  ],
  "rejected_or_pending": [
    {
      "term": "被拒绝的候选词",
      "reason": "拒绝原因，具体说明",
      "suggested_action": "reject_as_market_concept",
      "evidence": [],
      "notes": ""
    }
  ]
}
```

## 实体判断决策树

遇到候选词时，按以下顺序判断：

1. **是否只是已有实体的别名？**
   - 是 → 建立 `alias_of` 关系，不创建新节点
2. **是否与已有实体定义、原理、功能、输入输出一致？**
   - 是 → 合并到已有实体
3. **是否是已有实体的稳定子类？**
   - 是 → 创建新节点 + `is_a` 关系
4. **是否是技术路线或产品形态变体？**
   - 是 → 创建新节点 + `variant_of` 关系
5. **是否只是应用领域或用途标签？**
   - 是 → `reject_as_application_label`
6. **是否是市场概念或投资题材？**
   - 是 → `reject_as_market_concept`
7. **是否是公司/股票？**
   - 是 → `reject_as_company`
8. **证据不足？**
   - 是 → `create_pending_node` 或 `need_more_evidence`

## 拆分原则

只有当候选实体与已有实体在以下方面存在显著差异时，才拆分：

- 技术原理不同
- 上游输入不同
- 下游应用不同
- 生产工艺不同
- 产品形态不同
- 主要参与者不同
- 价值链位置不同

**示例：**
- `雷达` vs `激光雷达` → **拆分**（技术原理、关键部件、产业链均不同）
- `Radar` vs `雷达` → **不拆分**（只是别名）
- `相控阵雷达` vs `雷达` → **不拆分为新节点**（如果已有雷达节点，建立 `is_a` 关系）

## 拒绝规则速查

| 候选词类型 | suggested_action | 示例 |
|-----------|-----------------|------|
| 公司/股票 | `reject_as_company` | 华为、大疆、600519 |
| 投资题材/市场热点 | `reject_as_market_concept` | 低空经济、AI概念、机器人赛道 |
| 应用领域标签 | `reject_as_application_label` | 军用雷达、民用雷达、国产芯片 |
| 宽泛修饰词 | `reject_as_application_label` | 高端、智能、新型 |
| 证据不足 | `create_pending_node` | 无法判断的新词 |
| 复杂歧义 | `review_manually` | 需要人工判断的情况 |

## 产业流关系类型

| edge_type | 含义 | 示例 |
|-----------|------|------|
| `material_flow` | A 是 B 的物理原料 | 硅 → 芯片 |
| `composition` | A 是 B 的结构组成部分 | 轴承 → 电机 |
| `energy_flow` | A 为 B 提供能量 | 电力 → 数据中心 |
| `information_flow` | A 向 B 提供数据/信号 | 传感器 → 控制系统 |
| `capability_supply` | A 为 B 提供基础能力 | 操作系统 → 应用软件 |
| `service_flow` | A 以服务形式支持 B | 云计算服务 → SaaS应用 |

## 本体治理关系类型

| edge_type | 含义 | 示例 |
|-----------|------|------|
| `alias_of` | A 是 B 的别名/缩写/译名 | Radar alias_of 雷达 |
| `is_a` | A 是 B 的稳定子类 | 相控阵雷达 is_a 无线电雷达 |
| `variant_of` | A 是 B 的技术变体 | 固态激光雷达 variant_of 激光雷达 |

## PROV 声明规范

PROV 声明是附着在产业图节点上的**类型级溯源断言**（已整体弃用）。物料血缘现在直接通过产业图工业流边 `derived_from` 表达，不再维护独立的 PROV 文件。旧代码保留在 `backend/app/services/prov_storage.py` 和 `backend/app/routers/prov.py` 中仅供参考。

> **加图是加图，加 PROV 是加 PROV，不要混在一起，也不要建立隐式关联。**

### 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `node_id` | 是 | 被描述的节点 ID（已在 Neo4j 中存在） |
| `node_role` | 是 | `entity` / `activity` / `agent` |
| `prov_relation` | 是 | `used` / `wasGeneratedBy` / `wasDerivedFrom` / `wasAttributedTo` / `wasAssociatedWith` / `actedOnBehalfOf` |
| `target_node_id` | 是 | 指向的节点 ID（已在 Neo4j 中存在） |
| `target_role` | 是 | `entity` / `activity` / `agent` |
| `evidence` | 推荐 | 至少包含 `source_title` 和 `quote` |
| `confidence` / `status` / `notes` | 否 | 遵循通用规范 |

### 允许的 PROV 关系

| prov_relation | 含义 | 方向 | 示例 |
|---|---|---|---|
| `used` | Activity 使用了 Entity | activity → entity | `wafer_manufacturing` used `silicon_wafer` |
| `wasGeneratedBy` | Entity 由 Activity 生成 | entity → activity | `wafer` wasGeneratedBy `wafer_manufacturing` |
| `wasDerivedFrom` | Entity 在物料身份上直接派生自 Entity（强关联、显式声明，不用于通用耗材） | entity → entity | `gan_power_device` wasDerivedFrom `gallium_nitride` |
| `wasAttributedTo` | Entity 归因于 Agent | entity → agent | 暂不推荐 |
| `wasAssociatedWith` | Activity 与 Agent 关联 | activity → agent | 暂不推荐 |
| `actedOnBehalfOf` | Agent 代表 Agent | agent → agent | 暂不推荐 |

### 示例

```json
{
  "node_id": "wafer",
  "node_role": "entity",
  "prov_relation": "wasGeneratedBy",
  "target_node_id": "wafer_manufacturing",
  "target_role": "activity",
  "evidence": [
    {
      "source_title": "半导体制造工艺",
      "quote": "晶圆由晶圆制造工艺生成。"
    }
  ],
  "confidence": "HIGH",
  "status": "ACTIVE"
}
```

## PROV 使用要点与提醒

1. **图和 PROV 完全独立**
   - 批量注册节点/边（`GraphRegistrationBatch`）不会自动创建 PROV。
   - PROV 声明不会替代缺失的工艺边；产业图缺边时应先补图。

2. **新增实体时建议同时编写 PROV**
   - 如果根据资料能明确一个典型实体的生成/使用/派生路径，应顺手通过 `/api/v1/prov/statements` 补一条 PROV 声明。
   - 如果来源路径不确定，不要硬写；宁可留空，也不要造路径。

3. **禁止用 PROV 表达关键性/强相关**
   - “氮化镓对功率器件很关键”不是 `wasDerivedFrom`，除非存在明确的物料派生链。
   - `wasDerivedFrom` 只用于“产物在物料身份上直接来源于某原料/中间品”的强关联，且必须显式声明；不能用于纯水、电、压缩空气、普通清洗剂等通用耗材。
   - 这类语义目前应记录到 notes，等待 material_trace 层实现。

4. **类型级，不讨论批次**
   - PROV 描述的是“一个典型 X 如何生成”，不是某个具体批次的真实溯源。

## Arachne-flow 流程建模要点

Arachne-flow 是独立于 legacy 产业图的流程图引擎，使用 YAML 三元组描述产品流程：

- **RESOURCE**：物料、部件、设备、服务、信息等（对应 PG `industrial_nodes` 中的实体，全局唯一）。
- **ACTION**：某个流程中的一次具体活动（`{flow_id}:{action_id}`，每流独立实例）。
- **METHOD**：工艺/方法词表（对应 PG 中的 process 类节点，全局唯一）。

三元组模式：
- `[RESOURCE, input_role, ACTION]` — 输入（feedstock / component / tool / subject / basis / requirement 等）
- `[RESOURCE, input_role, METHOD]` — 工艺的通用输入（METHOD 作为模板承载公用资源）
- `[ACTION, output_role, RESOURCE]` — 输出（primary_result / co_result / intermediate / byproduct 等）
- `[METHOD, output_role, RESOURCE]` — 工艺的通用输出（METHOD 作为模板承载公用产物）
- `[ACTION, ref, METHOD]` — 动作引用方法
- `[ACTION, next, ACTION]` — 动作顺序

建模原则：
- **共享 RESOURCE/METHOD 是流程之间的接口**：不同流程通过同一个 RESOURCE（如 `chip`）连接，而不是重复描述它的上游。
- **公共上游链抽成共享流程文件**：如 `semiconductor_chip_manufacturing.yaml`、`wafer_fabrication_processes.yaml`，产品流程只写自己的集成环节并 `include` 它们。
- **`include` 是依赖声明，不是复制粘贴**：被 include 的流程独立编译；当前文件只写自己的 triples，通过共享 RESOURCE 与它们拼接。
- **ACTION 不跨文件引用**：一个流程不能引用另一个流程的 ACTION（那是别人的实例），只能引用共享 RESOURCE/METHOD。
- **每个文件必须是一个连通 DAG**：解析器会校验连通性和无环。

编辑与验证：
- 使用前端「流程编辑器」或主工作区右侧面板编写 YAML，实时预览（当前文件 + include 的上游链）。
- 保存前用 `POST /api/v1/flows/preview` 校验；保存会自动重新编译。

## 关键提醒

- **分类不是关系**：`entity_type` 只是属性，不会自动建立边
- **名称不是实体**：不能因名称相似就合并，必须依据定义、原理、功能判断
- **ontology 不参与产业流推理**：本体关系只用于名称治理，不用于上下游分析
- **公司不进入底层图**：当前系统不登记公司关系，未来通过 Company → Activity → Entity 映射
- **允许弱一致性**：系统允许冲突、冗余、未确认节点存在，通过人工后续修正
