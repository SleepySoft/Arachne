# Arachne 引擎子系统重构设计

> 目标：把当前“唯一”的图引擎拆分为可替换的子系统，明确核心共享层与引擎私有层的边界，使 `arachne-flow` 能与现有图引擎双擎共存。

---

## 1. 核心原则

1. **Metadata 是共享的**：`industrial_nodes`（PG）是所有引擎共享的节点元数据源。引擎不拥有 metadata，只拥有拓扑（Neo4j 中的关系）。
2. **实体 ID 是共享的**：`node_id` 在所有引擎中指向同一实体。`arachne-flow` 中的 `RESOURCE` 与现有图中的 `chip`、`hbm` 等共用同一 metadata 记录。
3. **核心 API 引擎无关**：`routers` 返回统一的 `GraphNode` / `GraphEdge` 等通用模型。具体 schema 校验下沉到各引擎子模块。
4. **引擎是可替换子系统**：每个引擎实现同一抽象接口。切换引擎 = 切换实现，不改动 API 契约。
5. **引擎管理自己的存储**：每个引擎可连接独立的 Neo4j 实例（或同一实例的不同标签/关系类型），核心不关心。

---

## 2. 共享核心层（Core）

### 2.1 通用数据模型 `app/models/core.py`

| 模型 | 字段 | 说明 |
|---|---|---|
| `GraphNode` | `node_id`, `label`, `entity_type`, 可选扩展字段 | 对前端是统一节点 |
| `GraphEdge` | `edge_id`, `from_node`, `to_node`, `edge_namespace`, `edge_type`, 可选扩展字段 | 对前端是统一边 |
| `Paginated[T]` | `total`, `page`, `page_size`, `items` | 通用分页 |
| `SubgraphResult` | `center_node_id`, `depth`, `nodes`, `edges` | 子图结果 |
| `GraphStats` | `total_nodes`, `total_edges`, 类型分布 | 统计结果 |
| `Evidence` | `source_title`, `source_url`, `quote` | metadata 与边共用 |
| `Confidence` / `NodeStatus` | 枚举 | metadata 状态 |

> `entity_type` / `edge_type` 在核心层是 `str`，引擎层可定义自己的枚举。

### 2.2 共享 Metadata 存储 `app/services/metadata_storage.py`

由现有 `app/services/node_storage.py` 改名并收紧职责：

- `create_node(node: IndustrialNode)` → 写入 PG `industrial_nodes`
- `get_node(node_id)` → 从 PG 读取
- `update_node(node_id, data)` → 更新 PG
- `delete_node(node_id)` → 删除 PG 记录
- `list_nodes(...)` → PG 查询
- `get_nodes_by_ids(node_ids)` → 批量读取

所有引擎都通过它解析 `node_id → metadata`。

### 2.3 引擎抽象接口 `app/engines/base.py`

```python
class GraphEngine(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    # 节点拓扑操作
    async def list_nodes(self, skip, limit, filters) -> tuple[list[GraphNode], int]: ...
    async def get_node(self, node_id) -> GraphNode | None: ...
    async def create_node(self, data) -> GraphNode: ...
    async def update_node(self, node_id, data) -> GraphNode | None: ...
    async def delete_node(self, node_id) -> bool: ...

    # 边拓扑操作
    async def list_edges(self, skip, limit, filters) -> tuple[list[GraphEdge], int]: ...
    async def get_edge(self, edge_id) -> GraphEdge | None: ...
    async def create_edge(self, data) -> GraphEdge: ...
    async def update_edge(self, edge_id, data) -> GraphEdge | None: ...
    async def delete_edge(self, edge_id) -> bool: ...

    # 查询操作
    async def get_subgraph(self, node_id, depth) -> tuple[list[GraphNode], list[GraphEdge]]: ...
    async def get_neighbors(self, node_id) -> tuple[list[GraphNode], list[GraphEdge]]: ...
    async def get_paths(self, from_node, to_node, max_depth) -> list[list[dict]]: ...
    async def get_stats(self) -> GraphStats: ...

    # 能力声明
    @property
    @abstractmethod
    def supports_write(self) -> bool: ...

    @abstractmethod
    async def get_capabilities(self) -> dict: ...
```

### 2.4 引擎注册表 `app/services/engine_registry.py`

根据 `settings` 或请求参数返回对应引擎实例：

```python
_engines: dict[str, GraphEngine] = {}

def register_engine(engine: GraphEngine):
    _engines[engine.name] = engine

def get_engine(name: str | None = None) -> GraphEngine:
    name = name or settings.DEFAULT_ENGINE
    return _engines[name]
```

### 2.5 配置 `app/config.py`

```python
class Settings:
    # 现有主图实例
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "arachne123"

    # arachne-flow 实例（双实例方案）
    NEO4J_FLOW_URI: str = "bolt://localhost:7688"
    NEO4J_FLOW_USER: str = "neo4j"
    NEO4J_FLOW_PASSWORD: str = "arachne123"

    # 默认引擎
    DEFAULT_ENGINE: str = "legacy"

    # arachne-flow 文件目录
    ARACHNE_FLOW_DIR: str = "./flows"
```

---

## 3. 引擎私有层（Engine-specific）

### 3.1 现有图引擎 `app/engines/legacy/`

| 原文件 | 新位置 | 说明 |
|---|---|---|
| `models/schemas.py` 中的 `EntityType`, `IndustrialFlowType`, `OntologyType`, `IndustrialNodeCreate` 等 | `engines/legacy/schemas.py` | 现有引擎的输入校验 schema |
| `services/neo4j_storage.py` | `engines/legacy/storage.py` | Neo4j 主实例 CRUD |
| `services/graph_service.py` 的节点/边/查询逻辑 | `engines/legacy/engine.py` | `LegacyEngine` 实现 `GraphEngine` |
| `services/derived_from_policy.py` | `engines/legacy/policies/` | 现有引擎专有业务规则 |

`LegacyEngine` 的行为与当前系统完全一致：
- 节点 skeleton 写在主 Neo4j 实例的 `:IndustrialNode`
- 关系类型为 `:INDUSTRIAL_FLOW` / `:ONTOLOGY`
- 输入校验使用现有 schema

### 3.2 arachne-flow 引擎 `app/engines/arachne_flow/`

| 模块 | 职责 |
|---|---|
| `schemas.py` | `RESOURCE`/`ACTION`/`METHOD` 类型，`input_role`/`output_role`/`next`/`ref` 等枚举 |
| `parser.py` | YAML 读取、include 内联、三元组校验 |
| `compiler.py` | 把解析后的三元组编译为 Neo4j 节点/边 |
| `storage.py` | 连接 flow Neo4j 实例的读写 |
| `engine.py` | `ArachneFlowEngine` 实现 `GraphEngine`，只读 |
| `state.py` | PG 表 `arachne_flow_files`，记录文件 MD5 与编译状态 |

`ArachneFlowEngine` 特性：
- 节点 skeleton 写在 flow Neo4j 实例的 `:IndustrialNode`（或 `:IndustrialNode:ArachneFlowNode`）
- 关系类型为 `:ARACHNE_FLOW`（不污染主实例的 `:INDUSTRIAL_FLOW`）
- `supports_write = False`：`create_node` / `create_edge` 返回 405
- 通过 `metadata_storage.get_nodes_by_ids()` 复用共享 metadata

---

## 4. 边界划分

### 4.1 共享层负责

- 通用图模型（`GraphNode`, `GraphEdge`, `SubgraphResult`, `GraphStats`）
- 节点 metadata 的 CRUD（`metadata_storage.py`）
- 引擎抽象接口与注册表
- Router 的 endpoint 形状（URL、HTTP 方法、分页参数）
- 全局配置

### 4.2 引擎层负责

- 自己的 Neo4j driver / 连接
- 自己的节点/边 schema 校验
- 自己的关系类型与标签策略
- 自己的业务规则（如 `derived_from` 校验、环检测、多图检测）
- 自己的 edge type / entity type 枚举
- 自己的能力声明（是否可写、支持哪些查询深度等）
- 自己的编译/解析逻辑（arachne-flow）

### 4.3 跨层协作点

| 操作 | 共享层 | 引擎层 |
|---|---|---|
| 创建节点 | `metadata_storage.create_node()` 写 PG | engine 写 Neo4j skeleton |
| 删除节点 | `metadata_storage.delete_node()` 删 PG | engine 删 Neo4j 节点及关联边 |
| 列节点 | `metadata_storage.get_nodes_by_ids()` 读 PG | engine 从 Neo4j 取 ID 列表 |
| 子图查询 | `metadata_storage.get_nodes_by_ids()` 解析 metadata | engine 从 Neo4j 取拓扑 |
| 创建边 | — | engine 校验并写 Neo4j（不碰 metadata） |

---

## 5. 当前代码映射

```
app/models/schemas.py
├── 通用模型       → app/models/core.py
├── EntityType     → app/engines/legacy/schemas.py
├── IndustrialFlowType → app/engines/legacy/schemas.py
├── OntologyType   → app/engines/legacy/schemas.py
├── IndustrialNodeCreate → app/engines/legacy/schemas.py
└── ...

app/services/neo4j_storage.py
├── 节点 skeleton CRUD  → app/engines/legacy/storage.py
├── 边 CRUD             → app/engines/legacy/storage.py
└── 查询 (subgraph/neighbors/paths/stats) → app/engines/legacy/engine.py

app/services/node_storage.py
└── 全部 → app/services/metadata_storage.py

app/services/graph_service.py
└── 节点/边/查询业务逻辑 → app/engines/legacy/engine.py

app/routers/nodes.py
└── 调用 graph_service → 调用 engine_registry.get_engine()

app/routers/edges.py
└── 同上

app/routers/query.py
└── 同上
```

---

## 6. Dry Run 场景

### 6.1 场景 A：现有引擎列节点

```
GET /api/v1/nodes?engine=legacy
  → routers/nodes.py 解析 engine=legacy
  → engine_registry.get_engine("legacy") → LegacyEngine
  → LegacyEngine.list_nodes():
       1. 查询主 Neo4j 实例得到 node_id 列表
       2. metadata_storage.get_nodes_by_ids(ids) 从 PG 取 metadata
       3. 组装为 list[GraphNode]
  → Router 返回通用 Paginated[GraphNode]
```

**效果**：与当前行为一致，只是经过了一层抽象。

### 6.2 场景 B：arachne-flow 子图查询

```
GET /api/v1/query/subgraph/chip?engine=arachne_flow&depth=2
  → routers/query.py 解析 engine=arachne_flow
  → engine_registry.get_engine("arachne_flow") → ArachneFlowEngine
  → ArachneFlowEngine.get_subgraph("chip", 2):
       1. 查询 flow Neo4j 实例得到 chip 的邻居拓扑
       2. metadata_storage.get_nodes_by_ids(ids) 从同一 PG 取 metadata
       3. 组装为 (list[GraphNode], list[GraphEdge])
  → Router 返回 SubgraphResult
```

**效果**：前端收到与现有引擎相同的数据结构，但拓扑来自另一实例。

### 6.3 场景 C：在现有引擎创建节点

```
POST /api/v1/nodes?engine=legacy
  body: IndustrialNodeCreate
  → LegacyEngine.create_node(data):
       1. 用 engines/legacy/schemas.py 校验
       2. metadata_storage.create_node() 写 PG
       3. 在主 Neo4j 实例创建 :IndustrialNode skeleton
  → 返回 GraphNode
```

**效果**：与当前行为一致，校验逻辑下沉到引擎。

### 6.4 场景 D：在 arachne-flow 引擎创建节点

```
POST /api/v1/nodes?engine=arachne_flow
  → ArachneFlowEngine.create_node(data)
  → 抛出 NotImplementedError 或返回 HTTP 405
```

**效果**：引擎声明自己只读，核心层不强制所有引擎支持写操作。

---

## 7. 前端影响

### 7.1 必须改的（有限）

1. **类型放宽**：`GraphEdge` 不再区分 `IndustrialFlowEdge | OntologyEdge`，统一为通用接口。
2. **引擎切换参数**：所有 API 调用增加 `?engine=` 参数，默认 `legacy`。
3. **样式动态化**：`ENTITY_TYPE_COLORS` / `EDGE_TYPE_LABELS` 保留 fallback，并支持从后端 `/engine/config` 加载引擎专属配置。

### 7.2 不需要改的

- `GraphCanvas` 渲染逻辑
- 节点/边的选中、拖拽、缩放、布局
- 子图加载、邻居拉取、路径查询
- 公司关联、行业映射等通用操作
- 画布状态管理

---

## 8. 兼容性与迁移

- 所有现有 endpoints 默认 `engine=legacy`，行为 100% 兼容。
- `industrial_nodes` 表结构不变。
- 现有 tests 应继续通过（LegacyEngine 行为不变）。
- 新增 engine 时不改动 routers / core models。
- 旧代码中的 `neo4j_storage` / `node_storage` 等引用逐步迁移，但保留兼容别名直到重构完成。

---

## 9. 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| 抽象层性能损耗 | 微秒级额外调用 | 接口保持轻量，不跨网络 |
| 引擎输入 schema 差异大 | 前端表单难统一 | 核心定义通用字段；引擎特有字段通过 `capabilities` 元数据动态渲染 |
| 节点删除跨层不一致 | metadata 删了但 Neo4j skeleton 残留 | Engine `delete_node` 必须保证“先删边，再删 skeleton，最后删 metadata”或反向，用事务/补偿 |
| 全局 node_id 冲突 | 两个引擎创建同名节点 | 共享 metadata 的 `node_id` 唯一约束天然防止 |
| arachne-flow 只读导致前端编辑按钮不可用 | 用户困惑 | 引擎 `capabilities` 返回 `read_only=true`，前端根据状态禁用编辑 |

---

## 10. 需要先做决定的开放问题

1. **节点创建放在哪一层？**
   - 方案 A：引擎 `create_node` 自己调 metadata_storage（简单，router 无感）
   - 方案 B：核心 `NodeService` 协调 metadata + engine skeleton hook（更干净，但需要新增 service 层）
   - **建议**：方案 A，保持 router 简单。

2. **引擎选择粒度？**
   - 方案 A：全局默认引擎（`DEFAULT_ENGINE`），整站一致
   - 方案 B：每个 API 请求通过 `?engine=` 参数切换
   - **建议**：方案 B，更灵活，前端可在同一 session 中对比两图。

3. **arachne-flow 编译图是否带 `:IndustrialNode` 标签？**
   - 方案 A：只带 `:ArachneFlowNode`（彻底隔离，但现有 Cypher 工具不识别）
   - 方案 B：同时带 `:IndustrialNode:ArachneFlowNode`（兼容性好，便于调试）
   - **建议**：方案 B。

4. **arachne-flow 的关系类型用 `:ARACHNE_FLOW` 还是复用 `:INDUSTRIAL_FLOW`？**
   - 方案 A：`:ARACHNE_FLOW` + `edge_namespace=arachne_flow`（语义清晰，不污染现有统计）
   - 方案 B：复用 `:INDUSTRIAL_FLOW`，`edge_type` 用新字符串（现有查询会自然包含）
   - **建议**：方案 A，保持统计和 DB check 的清晰隔离。

---

## 11. 推荐实施顺序

1. **Phase 1：抽象层搭建**
   - 创建 `app/models/core.py`
   - 重命名 `node_storage.py` → `metadata_storage.py`
   - 创建 `app/engines/base.py`
   - 创建 `app/services/engine_registry.py`

2. **Phase 2：现有引擎迁移**
   - 把 `neo4j_storage.py` 移入 `engines/legacy/storage.py`
   - 把相关 schema 移入 `engines/legacy/schemas.py`
   - 实现 `LegacyEngine`
   - 修改 routers 使用 `engine_registry`
   - 跑通全部现有 tests

3. **Phase 3：双实例配置**
   - `config.py` 增加 flow Neo4j URI
   - `database_flow.py` 创建第二个 driver
   - 启动脚本支持第二个 Neo4j 实例

4. **Phase 4：arachne-flow 引擎**
   - 实现 parser / compiler / state
   - 实现 `ArachneFlowEngine`
   - 提供 `/arachne-flow/compile` 和 `/arachne-flow/status`

5. **Phase 5：前端适配**
   - 统一 `GraphEdge` / `GraphNode` 类型
   - 增加引擎切换 UI
   - 动态加载引擎样式配置

---

## 12. 效果评估

| 维度 | 重构前 | 重构后 |
|---|---|---|
| 新增引擎成本 | 改动 routers/models/services 多处 | 新增一个 `engines/<name>/` 子目录 |
| 现有 API 稳定性 | 与新功能耦合 | 默认 `legacy` 行为不变 |
| Metadata 一致性 | 唯一 PG 源 | 仍然是唯一 PG 源，所有引擎共享 |
| 拓扑隔离 | 无 | 通过 Neo4j 实例/标签/关系类型隔离 |
| 前端改动范围 | — | 仅类型放宽 + 引擎切换 + 样式动态化 |
| 测试覆盖 | 集中 | 各引擎独立测试 + core 共享测试 |

---

*下一步：确认以上设计后，进入 Phase 1 实施。*


## 13. 推理子系统设计

### 13.1 核心问题

如果核心只暴露“节点/边最小契约”，把所有边当作无差别字符串处理，会丢失子系统的语义能力。例如：

- 当前引擎的 `material_input` 无法区分“主体原料”和“催化剂”；
- arachne-flow 的 `feedstock` / `catalyst` / `energy` 能精确表达角色，但核心需要知道这些角色意味着什么。

因此，推理必须采用 **“核心主导 + 引擎赋能”** 的分层架构。

### 13.2 分层架构

```
┌─────────────────────────────────────────────────────┐
│ Layer 3: 引擎专属语义推理（Engine-specific Semantic）  │
│ - 原料追溯（只沿 feedstock）                          │
│ - 副产品识别（byproduct / co_result / scrap）         │
│ - ACTION-METHOD ref 链分析                           │
│ - 当前引擎的 derived_from 物料谱系                    │
├─────────────────────────────────────────────────────┤
│ Layer 2: 通用图算法推理（Generic Graph Reasoning）     │
│ - 连通性、路径搜索、子图展开                          │
│ - 中心性、瓶颈度、betweenness                        │
│ - 社区发现（可选）                                    │
├─────────────────────────────────────────────────────┤
│ Layer 1: 跨图上下文（Cross-graph Context）            │
│ - 公司暴露、行业映射、事实关系                        │
│ - 这部分基于 PG，与引擎无关                           │
└─────────────────────────────────────────────────────┘
```

### 13.3 主导权划分

| 层级 | 核心主导 | 引擎参与 |
|---|---|---|
| 任务契约 | `ReasoningTask` / `ReasoningResultEnvelope` | 无 |
| 任务调度 | dispatcher 决定调用哪个 handler | 可注册专属 handler |
| 通用算法 | path search / scoring / diagnostics | 提供边类型语义 |
| 语义解释 | 定义通用概念（上游/下游/本体） | `ReasoningAdapter` 返回具体边类型 |
| 专属任务 | 结果封装格式 | 实现算法逻辑 |

### 13.4 Engine ReasoningAdapter 接口

```python
class ReasoningAdapter(ABC):
    @abstractmethod
    def upstream_edge_types(self) -> list[str]:
        """所有可视为“上游输入”的 edge_type。"""

    @abstractmethod
    def downstream_edge_types(self) -> list[str]:
        """所有可视为“下游输出”的 edge_type。"""

    @abstractmethod
    def raw_material_edge_types(self) -> list[str]:
        """主体原料边类型（用于原料追溯）。"""

    @abstractmethod
    def ontology_edge_types(self) -> list[str]:
        """本体/拓扑边类型。"""

    @abstractmethod
    async def expand_sources(self, node_ids: list[str], params: dict) -> set[str]:
        """引擎自定义的 seed expansion（如 derived_from 谱系）。"""
```

### 13.5 各引擎适配器示例

**LegacyAdapter**（当前引擎）：

```python
class LegacyReasoningAdapter(ReasoningAdapter):
    def upstream_edge_types(self) -> list[str]:
        return ["material_input", "energy_input", "information_input",
                "equipment_enablement", "derived_from"]

    def downstream_edge_types(self) -> list[str]:
        return ["process_output", "supply_relation"]

    def raw_material_edge_types(self) -> list[str]:
        return ["material_input", "derived_from"]

    def ontology_edge_types(self) -> list[str]:
        return ["alias_of", "is_a", "part_of", "variant_of"]
```

**ArachneFlowAdapter**：

```python
class ArachneFlowReasoningAdapter(ReasoningAdapter):
    def upstream_edge_types(self) -> list[str]:
        return ["feedstock", "component", "additive", "process_material",
                "catalyst", "energy", "carrier", "tool", "packaging",
                "subject", "basis", "requirement"]

    def downstream_edge_types(self) -> list[str]:
        return ["primary_result", "co_result", "intermediate", "byproduct",
                "scrap", "waste", "emission", "recovered_resource"]

    def raw_material_edge_types(self) -> list[str]:
        # 原料追溯只关心“主体原料”
        return ["feedstock"]

    def ontology_edge_types(self) -> list[str]:
        return ["alias_of", "is_a", "part_of", "variant_of"]
```

### 13.6 通用任务执行流程

以 `association` 为例：

```python
async def run_association(task: ReasoningTask, engine: GraphEngine):
    adapter = engine.reasoning_adapter()

    # 1. 引擎语义扩展 seed nodes（如 derived_from / feedstock 预处理）
    seed_nodes = await adapter.expand_sources(task.source_nodes, task.parameters)

    # 2. 通用路径搜索，使用引擎定义的上游/下游边类型
    paths = await generic_path_search(
        engine=engine,
        sources=seed_nodes,
        upstream_types=adapter.upstream_edge_types(),
        downstream_types=adapter.downstream_edge_types(),
        constraints=task.constraints,
    )

    # 3. 通用结果组装（子图、路径、证据链、公司暴露）
    return build_result(paths, engine, task)
```

### 13.7 引擎专属任务

arachne-flow 可注册专属任务，例如：

- `action_role_analysis`：分析一个 ACTION 的输入角色构成
- `raw_material_trace`：只沿 `feedstock` 追溯主体原料
- `method_reference_graph`：分析 ACTION → METHOD 的引用网络

当前引擎可注册：

- `derived_from_lineage`：物料派生谱系
- `reified_usage_chain`：PROV-style Usage 链

注册方式：

```python
# engines/arachne_flow/__init__.py
from app.reasoning.engine import register_task_handler
from .reasoning_tasks import run_action_role_analysis

register_task_handler("action_role_analysis", run_action_role_analysis)
```

核心 dispatcher 收到任务时，先检查当前 engine 是否注册了该任务类型的 handler，有则调用，否则返回不支持。

### 13.8 多入多出问题的处理

当前引擎的“边直接连接 RESOURCE”模型存在多入多出歧义：

```
A --material_input--> B --process_output--> C
D --material_input--> ↑
                      ↓ --process_output--> E
```

无法判断 C 主要由 A 还是 D 生成。

arachne-flow 通过 **ACTION 中介节点** 解决：

```
A --feedstock--> ACTION_1 --primary_result--> C
D --catalyst--> ACTION_1
```

ACTION 节点使输入/输出关系精确对应。合并多个 flow 后，共享的 RESOURCE 会汇聚，但不同 ACTION 实例保持独立路径：

```
         ┌--> ACTION_flow1 --primary_result--> C1
硅片 --feedstock--┤
         └--> ACTION_flow2 --primary_result--> C2
```

因此 arachne-flow 的结构**简化了**多入多出，而不是加剧。

### 13.9 GraphNode / GraphEdge 的 properties

核心模型需要携带引擎扩展属性：

```python
class GraphNode(BaseModel):
    node_id: str
    label: str
    entity_type: str
    properties: dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    edge_id: str
    from_node: str
    to_node: str
    edge_namespace: str
    edge_type: str
    description: str
    confidence: str
    properties: dict[str, Any] = Field(default_factory=dict)
```

但 `properties` 只是扩展槽，不解决结构性歧义。真正的语义来自节点结构（如 ACTION 中介）和 `ReasoningAdapter` 的解释。

---

## 14. Ontology / Topology 是否应该移到核心？

### 14.1 结论

**应该移到核心，但采用“核心定义语义 + 引擎暴露边”的模式**，而不是把 ontology 数据强制绑定到某个引擎实例。

原因：

1. `alias_of` / `is_a` / `part_of` / `variant_of` 是通用知识组织（KOS）关系，不是某个引擎的私有概念。
2. 推理的 source expansion、别名解析、上下位扩展是跨引擎通用需求。
3. 如果把 ontology 留在 legacy 引擎，arachne-flow 引擎的推理就无法复用这些能力，必须重复实现。
4. 实体 ID 是共享的，ontology 边连接的是共享实体，天然应该跨引擎共享。

### 14.2 当前问题

当前 `app/reasoning/topology.py` 直接硬编码：

```python
ALIAS_EDGE_TYPE = "alias_of"
TAXONOMIC_EDGE_TYPES = {"is_a", "variant_of"}
PART_OF_EDGE_TYPE = "part_of"
```

并且 Cypher 直接查 `:ONTOLOGY` 关系。这导致：

- ontology 处理与 legacy 引擎的存储实现耦合；
- arachne-flow 引擎如果也使用 ontology，要么复用 `:ONTOLOGY`（跨实例不可行），要么自己实现一套。

### 14.3 建议方案

#### 14.3.1 核心层定义 TopologyService

新建 `app/services/topology_service.py`（或 `app/core/topology.py`）：

```python
class TopologyService:
    """共享的 ontology/topology 解析服务。"""

    ALIAS_EDGE_TYPE = "alias_of"
    TAXONOMIC_EDGE_TYPES = {"is_a", "variant_of"}
    PART_OF_EDGE_TYPE = "part_of"

    async def resolve_aliases(self, node_ids: list[str], max_hops: int = 3) -> tuple[set[str], dict[str, str]]: ...
    async def expand_taxonomic(self, node_ids: list[str], max_hops: int = 2) -> tuple[set[str], set[str]]: ...
    async def expand_part_of(self, node_ids: list[str], max_hops: int = 2) -> tuple[set[str], set[str]]: ...
    async def resolve_sources(self, node_ids: list[str], expand: bool = False) -> tuple[set[str], dict]: ...
```

#### 14.3.2 Topology 数据存储在共享图空间

把 ontology 边存放在**主 Neo4j 实例**（`bolt://localhost:7687`），作为所有引擎共享的“概念层”：

- 关系类型：`:ONTOLOGY`
- 属性：`edge_type` 为 `alias_of` / `is_a` / `part_of` / `variant_of`
- 节点：共享的 `:IndustrialNode`（与 legacy 引擎共用同一实例的 skeleton）

这样：

- legacy 引擎继续把自己的 `:ONTOLOGY` 边存在主实例，行为不变；
- arachne-flow 引擎的 flow 实例只存 `:ARACHNE_FLOW` 过程边；
- 核心 `TopologyService` 统一读取主实例的 `:ONTOLOGY` 边。

#### 14.3.3 引擎的 ReasoningAdapter 声明 topology 来源

```python
class ReasoningAdapter(ABC):
    @abstractmethod
    def topology_edge_types(self) -> list[str]:
        return ["alias_of", "is_a", "part_of", "variant_of"]

    @abstractmethod
    def topology_relationship_type(self) -> str:
        """Neo4j 关系类型，如 ONTOLOGY。"""
        return "ONTOLOGY"
```

#### 14.3.4 推理执行流程（含共享 topology）

```python
async def run_association(task, engine):
    adapter = engine.reasoning_adapter()

    # 1. 核心 TopologyService 解析别名和本体扩展（在主实例）
    canonical_ids, topo_details = await topology_service.resolve_sources(
        task.source_nodes,
        expand_ontology=task.parameters.get("expand_ontology", False),
    )

    # 2. 引擎语义扩展（如 derived_from / feedstock）
    seed_nodes = await adapter.expand_sources(canonical_ids, task.parameters)

    # 3. 通用路径搜索（在引擎自己的实例）
    paths = await generic_path_search(
        engine=engine,
        sources=seed_nodes,
        upstream_types=adapter.upstream_edge_types(),
        downstream_types=adapter.downstream_edge_types(),
        constraints=task.constraints,
    )

    # 4. 结果组装
    return build_result(paths, engine, task, topo_details)
```

### 14.4 边界划分

| 组件 | 核心层 | 引擎层 |
|---|---|---|
| ontology 语义定义 | `TopologyService` | 无 |
| ontology 算法（alias 解析、taxonomic/part_of 扩展） | `TopologyService` | 无 |
| ontology 数据存储 | 主 Neo4j 实例（共享） | 不存储 |
| 引擎自己的结构关系 | 无 | 各引擎自己定义（如 `:ARACHNE_FLOW` / `:INDUSTRIAL_FLOW`） |
| 引擎对 topology 的使用 | 通过 `ReasoningAdapter` 声明 | 声明哪些边是 topology 边 |

### 14.5 与 arachne-flow 的关系

`design_v4` 说 topology 在 arachne-flow 体系之外定义，这正好与我们的设计一致：

- arachne-flow 文件只描述 `RESOURCE → ACTION → METHOD` 的过程拓扑；
- ontology（alias/is_a/part_of/variant_of）由系统核心统一维护；
- 编译 arachne-flow 时，不生成 `:ONTOLOGY` 边；这些边由其他机制（AI 抽取、人工维护、legacy 迁移）维护在主实例中。

### 14.6 风险与缓解

| 风险 | 说明 | 缓解 |
|---|---|---|
| 主实例同时存 legacy 供应链 + 共享 ontology | 概念上混合 | 用关系类型区分（`:INDUSTRIAL_FLOW` vs `:ONTOLOGY`），逻辑上清晰 |
| arachne-flow 实例缺少 ontology | 某些 reasoning 无法做 | 核心 `TopologyService` 从主实例读取，只要实体 ID 共享就能解析 |
| 不同引擎对同一 ontology 语义理解不同 | 如 `part_of` 是否可逆 | 核心定义标准语义，引擎遵循 |
| legacy 的 `:ONTOLOGY` 数据质量 | 已有数据可能不一致 | 保留现有数据，新增校验规则 |

### 14.7 实施建议

1. 将 `app/reasoning/topology.py` 迁移为 `app/services/topology_service.py`。
2. `TopologyService` 只读主 Neo4j 实例的 `:ONTOLOGY` 边。
3. 各引擎的 `ReasoningAdapter` 不再自己实现 ontology 扩展，而是调用 `TopologyService`。
4. 保留 legacy 引擎写 `:ONTOLOGY` 边的能力（通过 `create_ontology_edge`），但概念上属于“共享 topology 层”。
5. arachne-flow 引擎不管理 ontology；如果需要为 flow 中的 RESOURCE 建立别名/上下位，通过现有 ontology API 写入主实例。

---

*设计文档更新完毕。下一步可进入 Phase 1 实施。*


## 15. 子系统直达 API（Pass-through API）

### 15.1 为什么需要直达机制

通用 API（如 `GET /api/v1/nodes?engine=arachne_flow`）只能返回统一的 `GraphNode` / `GraphEdge` 模型。但子系统经常需要暴露一些**不适合也不应该被硬塞进通用接口**的定制化信息。

例如 arachne-flow：

- 编译状态：`/engines/arachne_flow/status`
- 触发编译：`POST /engines/arachne_flow/compile`
- 文件列表：`/engines/arachne_flow/files`
- 校验结果：`/engines/arachne_flow/validate/{flow_name}`
- 编译 diff：`/engines/arachne_flow/diff`

例如 legacy 引擎未来可能的专属诊断：

- `/engines/legacy/reverse-flow-report`
- `/engines/legacy/process-group-analysis`

这些信息用 `GraphNode` / `GraphEdge` 表达会很别扭，应该由子系统自己定义 endpoints。

### 15.2 URL 约定

```
/api/v1/nodes?engine=legacy              ← 通用 API
/api/v1/edges?engine=arachne_flow        ← 通用 API
/api/v1/query/subgraph/{id}?engine=x     ← 通用 API

/api/v1/engines/legacy/xxx               ← legacy 专属 API
/api/v1/engines/arachne_flow/xxx         ← arachne-flow 专属 API
/api/v1/engines/{engine_name}/{path}     ← 任意子系统专属 API
```

### 15.3 后端设计

#### 目录结构

```
backend/app/engines/
├── legacy/
│   ├── __init__.py
│   ├── engine.py
│   ├── storage.py
│   ├── schemas.py
│   ├── reasoning_adapter.py
│   └── router.py              # 子系统专属 endpoints
└── arachne_flow/
    ├── __init__.py
    ├── engine.py
    ├── storage.py
    ├── parser.py
    ├── compiler.py
    ├── schemas.py
    ├── reasoning_adapter.py
    └── router.py              # 子系统专属 endpoints
```

#### 动态注册（利用 Python 动态特性）

不硬编码每个引擎的 router，而是在 `app/engines/__init__.py` 中动态扫描并注册：

```python
# app/engines/__init__.py
import importlib
import pkgutil
from fastapi import APIRouter

ENGINE_ROUTERS: dict[str, APIRouter] = {}

for module_info in pkgutil.iter_modules(__path__):
    module_name = module_info.name
    try:
        module = importlib.import_module(f"app.engines.{module_name}.router")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            ENGINE_ROUTERS[module_name] = router
    except ImportError:
        continue


def register_engine_routers(app, api_v1_prefix: str):
    for engine_name, router in ENGINE_ROUTERS.items():
        app.include_router(
            router,
            prefix=f"{api_v1_prefix}/engines/{engine_name}",
            tags=[f"Engine: {engine_name}"],
        )
```

这样新增一个引擎时，只要创建 `engines/<name>/router.py` 并导出 `router`，无需修改 `main.py`。

#### main.py 挂载

```python
# app/main.py
from app.engines import register_engine_routers

# ... 其他 include_router ...

register_engine_routers(app, settings.API_V1_STR)
```

#### arachne-flow router 示例

```python
# app/engines/arachne_flow/router.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def get_status():
    """返回当前编译状态、文件 MD5、是否 stale。"""
    ...


@router.post("/compile")
async def compile_flows():
    """重新编译所有 flow 文件到 flow Neo4j 实例。"""
    ...


@router.get("/files")
async def list_files():
    """列出扫描到的 flow 文件。"""
    ...


@router.post("/validate/{flow_name}")
async def validate_flow(flow_name: str):
    """校验单个 flow 文件。"""
    ...
```

#### legacy router 示例

```python
# app/engines/legacy/router.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/reverse-flow-report")
async def reverse_flow_report():
    """返回当前图中反向工业流的统计。"""
    ...


@router.get("/process-group-analysis")
async def process_group_analysis():
    """分析 process 节点群的结构。"""
    ...
```

### 15.4 前端设计

#### 目录结构

```
frontend/src/
├── services/
│   ├── api.ts                 # 通用 API
│   └── engines/
│       ├── legacy.ts          # legacy 专属 API
│       └── arachneFlow.ts     # arachne-flow 专属 API
├── components/
│   ├── common/                # 通用组件
│   └── engines/
│       ├── legacy/            # legacy 专属 UI
│       └── arachneFlow/       # arachne-flow 专属 UI
```

#### 动态发现引擎专属服务（利用 JS 动态特性）

```typescript
// frontend/src/services/engines/index.ts
const engineServices: Record<string, () => Promise<Record<string, any>>> = {
  legacy: () => import("./legacy"),
  arachne_flow: () => import("./arachneFlow"),
};

export async function getEngineService(engine: string) {
  const loader = engineServices[engine];
  if (!loader) return null;
  return loader();
}
```

#### 前端服务示例

```typescript
// frontend/src/services/engines/arachneFlow.ts
import axios from "axios";

const BASE = "/api/v1/engines/arachne_flow";

export const getStatus = async () => {
  const res = await axios.get(`${BASE}/status`);
  return res.data;
};

export const compileFlows = async () => {
  const res = await axios.post(`${BASE}/compile`);
  return res.data;
};

export const listFiles = async () => {
  const res = await axios.get(`${BASE}/files`);
  return res.data;
};
```

#### UI 组件示例

```tsx
// frontend/src/components/engines/arachneFlow/FlowCompilerPanel.tsx
import { useEngine } from "@/contexts/EngineContext";
import * as arachneFlowApi from "@/services/engines/arachneFlow";

export function FlowCompilerPanel() {
  const { engine } = useEngine();
  if (engine !== "arachne_flow") return null;

  return (
    <div>
      <h3>Arachne Flow 编译状态</h3>
      <StatusDisplay />
      <button onClick={arachneFlowApi.compileFlows}>重新编译</button>
    </div>
  );
}
```

### 15.5 边界划分

| 进通用 API | 进专属 API |
|---|---|
| 节点/边的 CRUD 和查询 | 引擎的配置、状态、编译、校验 |
| 子图/邻居/路径/统计 | 引擎的诊断报告、分析报告 |
| 跨图上下文（公司/行业） | 引擎的导入/导出/迁移工具 |
| 推理任务执行（核心契约） | 引擎的自定义可视化数据 |
| fuzzy search / incomplete items | 引擎的批量管理操作 |

判断标准：

> **如果信息可以用 `GraphNode` / `GraphEdge` / `SubgraphResult` 等通用模型表达，进通用 API；否则进专属 API。**

### 15.6 安全与权限

1. **统一中间件**：所有 `/api/v1/engines/*` 都走同一套认证/权限中间件。
2. **能力声明**：引擎在 `/api/v1/engine/config` 中声明自己支持哪些专属操作，前端据此显示按钮。
3. **只读引擎限制**：arachne-flow 提供 `/compile` 但不提供直接修改编译后图数据的接口。

### 15.7 与通用 API 的关系

```
                    ┌─────────────────────────────┐
                    │         前端 UI              │
                    │  通用组件 + 引擎专属组件      │
                    └───────────┬─────────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
   /api/v1/nodes?engine=x   /api/v1/query/...   /api/v1/engines/{name}/...
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │    EngineRegistry     │
                    │  （通用 API 路由用）    │
                    └───────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            engines/legacy/          engines/arachne_flow/
            engine.py + router.py     engine.py + router.py
```

通用 API 通过 `engine_registry.get_engine(name)` 选择引擎；专属 API 直接由子系统自己的 router 处理。

---

*设计文档已补充子系统直达 API 章节。*
