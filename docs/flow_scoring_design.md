# Arachne-Flow 推理评分体系设计

> 记录图论分析、评分算法选型、插拔式架构决策与实现注意事项。

---

## 1. 背景：当前评分与图论对应

arachne-flow 关联推理（`backend/app/reasoning/tasks/arachne_flow_association.py`）
原先用硬编码公式给节点打分：

```python
main_deg = len(resource_actions.get(nid, set()))   # 主线 ACTION 数
branch_deg = len(branch_links.get(nid, set()))      # 支线连接数
score = main_deg + 0.5 * branch_deg
```

这对应图论中的概念：

| 代码实现 | 图论术语 | 含义 |
|---|---|---|
| arachne_flow `main_deg + 0.5*branch_deg` | **加权度中心性** (weighted degree centrality) | 节点连接了多少 ACTION |
| legacy `DepthDecayScorer` `decay^(depth-1)` | **Katz 中心性**（单路径版） | 带衰减的路径计数 |

传统引擎的评分是插拔式的（`backend/app/reasoning/scorers.py` 的
`BaseScorer`/`DepthDecayScorer`/`EdgeWeightScorer`/`CompositeScorer`），但
**只有 `impact_propagation.py` 在用**；arachne-flow 的关联分是硬编码，没走框架。

---

## 2. 关键洞察：评分必须绑定目的和方向

同一张图，不同问法会给出**相反排名**。以"硅片"为例：

- 问"上游断供谁最危险" → 评分 = **下游可达产出数**（forward reach）。
  硅片喂太阳能电池+芯片两条线 → 高分（关键卡点）。
- 问"下游需求萎缩谁最受伤" → 评分 = **上游原料依赖广度**（backward reach）。
  同一硅片若上游多晶硅来源单一 → 高分（脆弱）。

同一个节点，前者要它"喂得多"，后者要它"吃面窄"，方向相反、语义相反。
原 arachne_flow 的度分是**无向**的，两种问法给同一个分——这是它最大的盲点。

**结论：评分应作为推理任务的参数（按目的动态生成），而非图的固有属性。**

---

## 3. 学科入口（供系统学习）

领域名：**Network Science（网络科学）/ 复杂网络分析**（非纯图论，偏度量与应用）。

推荐教材：
- Barabási, *Network Science* — `networksciencebook.com` 全文免费，标杆入门。
- Newman, *Networks: An Introduction* — 更严谨全面，第二本。

核心术语地图：

| 术语 | 中文 | 回答的问题 |
|---|---|---|
| Degree centrality | 度中心性 | 连了多少人 |
| Betweenness centrality | 介数中心性 | 是不是咽喉要道（瓶颈） |
| Closeness centrality | 接近中心性 | 离所有人都多近 |
| Eigenvector centrality | 特征向量中心性 | 连到重要节点才算重要（递归） |
| PageRank | — | 重要性沿链接传播（有向） |
| Katz centrality | — | 带衰减的所有路径计数 |
| Personalized PageRank / RWR | 个性化 PageRank | **从种子出发的相对重要性** |
| Harmonic centrality | 调和中心性 | 对距离求和的鲁棒版 |
| Structural equivalence | 结构等价性 | 谁和谁邻居结构一样（替代品） |
| Max-flow min-cut | 最大流最小割 | 供应能承受多大冲击 |
| Modularity / community | 模块度/社团 | 哪些节点抱团成一个产业 |

---

## 4. 目的 → 方法 → 方向 映射

| 分析目的 | 图论方法 | 方向 | 备注 |
|---|---|---|---|
| 市场暴露广度 | 度中心性 | 无向 | **原实现**，作为默认基线 |
| 种子相对重要性 | Personalized PageRank | 有向+衰减 | 统一深度衰减+多路径+种子相对性 |
| 关键卡点/瓶颈 | 介数中心性 (Brandes) | 无向 | 真正的瓶颈识别 |
| 上游断供风险 | 下游可达性 (forward reach) | forward | blast radius |
| 上游依赖广度 | 上游可达性 (backward reach) | backward | 与 supply_risk 方向相反 |
| 替代品发现 | 结构等价性 (Jaccard) | 无向 | 未实现，留作后续 |
| 供应链韧性 | 最大流最小割 | 有向流 | 未实现，留作后续 |
| 产业聚类 | 模块度/社团检测 | 无向 | 未实现，留作后续 |

---

## 5. 架构决策：可配置 + 目的绑定默认值

**绑定还是可配置？→ 两者都要：可配置，但按目的绑定默认值。**

- `purpose`（语义意图）→ 映射到默认 scorer + 方向（绑定，开箱即用）
- `scoring_method`（显式覆盖）→ 直接指定 scorer（可配置，给进阶用户）
- 两者都不传 → 默认 `degree`（向后兼容）

这呼应 legacy 引擎已有的 `propagation_profiles.py`（profile = purpose → 默认值）模式。

### 目的注册表

| purpose | scoring_method | score_type | reach_direction |
|---|---|---|---|
| `exposure`（默认） | degree | association_strength | — |
| `supply_risk` | reach | downstream_blast_radius | forward |
| `sourcing_dependency` | reach | upstream_dependency | backward |
| `bottleneck` | betweenness | betweenness_centrality | — |
| `importance` | pagerank | personalized_pagerank | — |

### 解析优先级
1. `parameters.scoring_method` 显式指定 → 直接用
2. `parameters.purpose` → 查注册表
3. 都没有 → `degree`（向后兼容）

### 任务参数接口（`task.parameters`）
- `purpose`: str — 语义意图
- `scoring_method`: str — 显式覆盖（degree/pagerank/betweenness/reach）
- `scoring`: dict — scorer 专属参数（如 `{"damping": 0.9}`, `{"reach_direction": "forward"}`, `{"main_weight": 1.0, "branch_weight": 0.5}`）
- `top_k`: int — 返回 node_scores 条数（默认 50）

---

## 6. 实现的 Scorer

文件：`backend/app/reasoning/flow_scorers.py`

> 注意：legacy `scorers.py` 的 `BaseScorer` 接口是按**路径**打分
> (`score(path, edges, node_scores)`)，而 arachne-flow 需要按**子图节点**打分。
> 两者抽象层级不同，强行复用会过度设计。因此新建 `FlowNodeScorer` 抽象，
> 专为 arachne-flow 子图节点评分，不污染 legacy 接口。

### 6.1 DegreeScorer（基线 = 原行为）
`score = main_actions + 0.5 * branch_links`，可经 `scoring.main_weight`/`branch_weight` 调权重。
向后兼容默认。

### 6.2 PageRankScorer（Personalized PageRank / RWR）
- 在 BFS 已圈定的子图上构建有向邻接（`from->to` 视为下游/生产方向）
- 种子向量：`seed_resources ∪ seed_actions` 均匀分布
- 幂迭代：`r = damping * P^T @ r + (1-damping) * s`，damping 默认 0.85
- 悬挂节点（无出边）概率均匀重分配
- 收敛：L1 < 1e-6 或 50 轮
- 自然带深度衰减 + 有向传播 + 种子相对性，是度分与 legacy 衰减分的合成升级

### 6.3 BetweennessScorer（Brandes 算法）
- 子图上计算介数中心性（节点位于多少最短路径上）
- O(VE)，子图受 max_nodes 约束，可行
- 真正的瓶颈识别（度高≠瓶颈，枢纽可能有多条平行通路绕过）

### 6.4 ReachScorer（方向化可达性）
- `forward`：从节点出发沿生产方向能到达多少节点 = 下游 blast radius
- `backward`：能到达该节点的上游节点数 = 依赖广度
- 实现"相反评分"的那一对：supply_risk vs sourcing_dependency
- 仅统计物料流边（排除 ref），方法节点不参与（方法不是"流"）

---

## 7. 关键实现注意事项

1. **边方向恒为生产方向**：BFS 无论 traversal_direction 如何，都把边存成
   resource->action->resource（生产方向）。scorer 可靠地把 `from->to` 当下游。
   （已验证 `_stage_expand` forward/backward 的 `add_edge` 调用。）

2. **ref 边处理**：ref（action->method）是语义链接非物料流。
   - ReachScomer 排除 ref（blast radius 只走物料）
   - PageRank/Betweenness 包含 ref（共享方法可作为重要性/瓶颈枢纽）

3. **子图先建后评**：BFS 定义子图范围（受 max_nodes 约束），scorer 在该范围内排名。
   不重新查全图——与原设计一致，且高效有界。

4. **分数尺度不统一**：degree 是小整数，pagerank ~0-1，betweenness 依赖图规模，
   reach 是 0~V。`NodeScore.score` 保留原始值，`score_components.normalized`
   提供 [0,1] 归一化便于横向比较。`score_type` 字段区分尺度。

5. **temp_graph 节点分同步**：临时图节点的 `score`/`score_components` 字段
   原先也硬编码度分；改造后统一用所选 scorer 的结果，保证 node_scores 与
   临时图节点分一致。

6. **METHOD 节点覆盖差异**：DegreeScorer 给方法打分（经 resource_actions）；
   ReachScorer 不给方法打分（仅物料流）。这是预期行为，非 bug。

7. **向后兼容**：不传 purpose/scoring_method 时行为与改造前完全一致（degree）。

8. **未实现的留作后续**：结构等价性（替代品）、最大流最小割（韧性）、
   社团检测（聚类）——各有价值但属于不同任务类型，避免本次过度设计。

---

## 8. 验证

- `backend/tests/test_flow_scorers.py`：4 个 scorer 的纯算法单元测试
  （不依赖 Neo4j/PG，直接构造 ScoringContext）
- `test_arachne_flow_reasoning.py`：端到端，验证 purpose/scoring_method 参数生效
  且默认行为不变
