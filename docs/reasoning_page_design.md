# 推理页面（ReasoningPage）设计与逻辑说明

> 本文档描述 `/reasoning` 页面的信息架构、任务体系、数据流和扩展点。
> 页面在 2026-07-25 重构为「任务优先」模型：**先选任务，起点类型由任务决定**。

---

## 1. 页面解决什么问题

给定一个起点（产业节点或公司），回答"它在图里和谁相关"的问题，
并把结果**翻译成可读的故事**（解读 tab），而不是扔给用户一张无序的图。

典型问题：

| 用户的问题 | 对应任务 |
|---|---|
| 芯片从哪来、到哪去、和谁相关？ | flow · 关联扩展 |
| 沪硅产业在产业中的位置？上下游/同业公司？ | flow · 公司产业上下文 |
| 某个节点断供会影响谁？ | legacy · 影响传播 |
| 哪个环节最卡脖子？ | legacy · 瓶颈检测 |
| 某物料能被什么替代？ | legacy · 替代搜索 |

---

## 2. 页面结构（左栏四步 + 右栏结果）

```
┌ 左栏（操作流，严格按顺序）─────────────┐
│ 1. 选择任务   引擎 + 任务类型 + 任务说明 │
│ 2. 添加起点   起点类型（由任务决定，固定）│
│               搜索 → 候选/相似建议 → 添加 │
│ 3. 已选起点   chips（可多选/混合）       │
│ 4. 参数与输出 深度/路径/节点/方向/输出    │
│               [运行推理]                │
├ 右栏（结果）───────────────────────────┤
│ tabs: 解读* / 概览 / 可视化图 / 路径 /   │
│       节点得分 / 公司暴露 / ...          │
└────────────────────────────────────────┘
* 解读 = 默认 tab
```

### 关键设计：任务决定起点类型

不再让用户手工选"查询范围"（这是旧设计最易犯错的地方——公司是事实节点，
在产业节点范围里搜公司必然查无结果）。映射规则（`seedSpec()`）：

| 任务 | 起点类型 | 后端查询范围 |
|---|---|---|
| flow · 关联扩展 | 产业节点 | `industrial_node`（PG industrial_nodes 模糊搜索） |
| flow · 公司产业上下文 | 公司 | `factual_node` + `object_type=company` |
| legacy · 全部任务 | 产业节点 | `industrial_node` |

搜索返回分两层：**候选**（匹配度 ≥0.99）和**相似建议**（其余相似节点，
可直接添加为起点）。点「添加」才进入起点列表——搜索是探索，添加是确认，
这样才能支持多起点（如同时比较两个节点的关联）。

---

## 3. 引擎与任务矩阵

### arachne_flow 引擎（流程图，默认）

图结构：`RESOURCE --input_role--> ACTION --output_role--> RESOURCE`，
`ACTION --ref--> METHOD`。RESOURCE/METHOD 的 node_id 即 legacy 产业节点 id，
ACTION 按 `flow_id:action_id` 命名空间化。

| 任务 | 起点 | 做什么 | 输出 |
|---|---|---|---|
| `association` 关联扩展 | 产业节点 | **主线/支线双层遍历**：主线按工艺阶段计深度（RESOURCE→ACTION→RESOURCE=1 阶段，ACTION 不计数），主线 ACTION 的其余投入挂为"协同投入"叶子；支线经 METHOD 找同工艺的兄弟 ACTION 及其物料 | 临时推理图、路径、节点得分（关联强度） |
| `cross_graph_context` 公司产业上下文 | 公司 | 公司→暴露节点→主线/支线展开→相关公司分类 | 同上 + `company_context` |

**广度收敛**（防枢纽节点爆图）：`max_actions_per_resource`（默认 4，
同 flow 延续优先于跨 flow 跳转）、`max_support_per_action`（默认 8）、
`branch_limit`（默认 20）。

**公司分类语义**（company_context）：

| 类别 | 定义 |
|---|---|
| 同业公司 peers | 暴露于**相同环节且活动类型相同**（如同为硅片生产商；买硅片的是客户不是同业） |
| 上游公司 | 暴露于种子上游链（backward）节点的公司 |
| 下游公司 | 暴露于种子下游链（forward）节点的公司 |
| 相关公司 | 暴露于同工艺 METHOD / 支线关联物料的公司（产业配套） |

### legacy 引擎（产业图）

图结构：`:IndustrialNode + INDUSTRIAL_FLOW/ONTOLOGY`。
任务：association、impact_propagation、bottleneck_detection、
substitution_search、candidate_discovery、cross_graph_context（均为既有实现，
本文不展开）。flow 引擎尚不支持的任务会在 UI 中自动隐藏。

---

## 4. 结果的组织（右栏 tabs）

- **解读（默认）**：规则化叙事层，把 payload 翻译成四段——
  ① 一句话概览（规模统计）② 主线讲了什么（最长 3 条路径的可读链）
  ③ 关键发现（主线枢纽/共享工艺/支线关联物料，带「以此为起点深入」按钮）
  ④ 产业玩家 / 公司上下文（公司任务的分类公司 chips，点击可直接以该公司重跑）。
- **可视化图**：主线实线、工艺引用紫色虚线（METHOD 六边形）、协同投入灰细线、
  支线蓝虚线；起点黄色粗框；横向 dagre 布局，附静态图例和规模摘要条。
- **路径 / 节点得分 / 公司暴露**：明细表格。
- **NO_RESULT**：不再是静默空白。显示警告原因 + flow 图内相似可用起点
  （`missing_flow_suggestions`，点击直接重跑）+ 「切换到 legacy 重跑」按钮。

### 「以此为起点深入」（deepDive）

故事中的每个发现（枢纽节点、同业公司等）都可以一键成为新种子重跑推理，
这是"沿着故事继续探索"的核心交互。实现上复用 `buildPayload()`，
仅替换 source_nodes 并立即执行。

---

## 5. 数据流

```
用户输入
  │  1. 选择任务 (engine, task_type)
  │  2. 搜索起点  POST /api/v1/reasoning/query {query_text, query_scope}
  │               → candidates + suggestions（scope 由任务决定）
  │  3. 添加起点  sources[]（object_id 列表）
  │  4. 运行      POST /api/v1/reasoning/execute
  ▼               {task_type, source_nodes, parameters, constraints,
                   requested_outputs, engine}
后端 execute_reasoning_task
  │  engine.py: 预校验种子（PG）→ 按 engine 分发
  │    legacy      → tasks/association.py 等
  │    arachne_flow → association → tasks/arachne_flow_association.py
  │                 → cross_graph_context → tasks/arachne_flow_company_context.py
  ▼
ReasoningResultEnvelope {status, result_payload, diagnostics}
  │  payload: paths / temporary_graph / node_scores /
  │           company_exposures / company_context / node_counts /
  │           missing_flow_suggestions
  ▼
前端：tabs 渲染（解读为默认）+ deepDive 循环探索
```

---

## 6. 扩展点

**新增 flow 任务**：
1. 在 `backend/app/reasoning/tasks/` 新建任务函数（可复用
   `arachne_flow_association.py` 的主线/支线机器——company_context 即是
   复用示例）；
2. `reasoning/engine.py` 的 flow 分发注册；
3. 前端 `FLOW_TASK_OPTIONS` 加选项、`FLOW_TASK_DESC` 加说明、
   `seedSpec()` 声明起点类型；
4. 如有新 payload 区块，在 StoryView 加对应叙事段。

**自然候选**：瓶颈检测（关联强度评分已是雏形：被多流程依赖且替代少的
资源/工艺）、替代搜索（同 METHOD 同 role 的兄弟物料即候选）。

**新增引擎**：实现 `engine` 字段分发 + 前端 `ENGINE_OPTIONS` / 任务矩阵即可，
UI 结构无需改动。

---

## 7. 已知边界

- flow 图覆盖 = 已编译流程文件（`data/flows/`）。产业图中大量节点不在
  flow 图中（如商业模式、下游抽象应用），此时用 NO_RESULT 面板引导：
  推荐图内相似节点或切 legacy 引擎。
- 对象查询是引擎无关的（始终查 PG），因此起点能否用于 flow 取决于它是否
  出现在流程文件里——`_suggest_flow_nodes()` 负责兜底推荐。
- 新增 METHOD/RESOURCE 的 PG metadata（中文名）可能缺失，UI 回退显示 id。
