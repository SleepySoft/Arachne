# Arachne - 统一产业本体图系统

基于 `core_schema.py` 实现的完整产业本体图系统，覆盖半导体、新能源汽车、光伏、风电、钢铁五大核心供应链。

## 系统概览

| 指标 | 数值 |
|------|------|
| 节点 | 36（17 材料 / 6 设备 / 3 组件 / 2 模块 / 6 系统 / 1 基础设施 / 1 平台） |
| 关系 | 37（15 物料流 / 17 组合 / 2 能力供给 / 2 能量流 / 1 信息流） |
| 供应链 | 半导体、新能源汽车、光伏、风电、钢铁 |

## 技术栈

| 层级 | 技术 |
|------|------|
| 数据库 | Neo4j 5.x Community（本地安装） |
| 后端 | FastAPI + Pydantic v2 + neo4j-python-driver（异步） |
| 前端 | React 18 + TypeScript + Vite + Cytoscape.js + Tailwind CSS |
| 管理 | Python 跨平台进程管理器（`arachne_manager.py`） |
| Agent 支持 | Kimi Skill + Prompt |

## 项目结构

```
Arachne/
├── arachne_manager.py              # Python 跨平台系统管理器（启动/停止/状态/统计）
├── requirements.txt                # 管理器依赖（psutil + httpx）
├── start-all.ps1                   # PowerShell 一键启动（备用）
├── stop-all.ps1                    # PowerShell 一键停止（备用）
├── backend/                        # FastAPI 后端
│   ├── app/
│   │   ├── main.py                 # FastAPI 入口
│   │   ├── config.py               # 环境配置（Neo4j 连接等）
│   │   ├── database.py             # Neo4j 异步驱动
│   │   ├── models/schemas.py       # Pydantic 核心 Schema
│   │   ├── routers/                # API 路由
│   │   │   ├── nodes.py            # 节点 CRUD
│   │   │   ├── edges.py            # 边 CRUD
│   │   │   ├── batches.py          # 批量注册
│   │   │   └── query.py            # 查询接口（子图/路径/统计/冲突）
│   │   └── services/               # 业务逻辑层
│   │       ├── graph_service.py    # 核心图服务
│   │       ├── neo4j_storage.py    # Neo4j 存储层
│   │       └── memory_storage.py   # 内存存储（Neo4j 不可用时 fallback）
│   └── venv/                       # Python 虚拟环境
├── frontend/                       # React 前端
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── GraphCanvas.tsx     # Cytoscape.js 图可视化
│   │   │   ├── FilterPanel.tsx     # 多维过滤面板
│   │   │   ├── SearchPanel.tsx     # 节点搜索
│   │   │   ├── NodeDetail.tsx      # 节点详情
│   │   │   ├── EdgeDetail.tsx      # 边详情
│   │   │   ├── NodeForm.tsx        # 节点创建/编辑
│   │   │   ├── EdgeForm.tsx        # 边创建/编辑
│   │   │   ├── BatchUploader.tsx   # 批量上传 JSON
│   │   │   └── StatsBar.tsx        # 顶部统计栏
│   │   ├── services/api.ts         # Axios API 客户端
│   │   └── types/index.ts          # TypeScript 类型定义
│   └── package.json
├── cli/
│   └── arachne_cli.py              # 命令行工具（submit / query）
├── data/
│   └── seed_industry_graph.json    # 种子数据（36 节点 / 37 边）
├── neo4j-community-5.26.0/         # 本地 Neo4j 安装目录
├── core_schema.py                  # 原始核心 Schema
├── docs/                           # 设计文档与 Prompt
│   ├── prompts.txt
│   ├── think-01.md
│   └── think-02.md
└── .kimi/skills/arachne-graph/     # Kimi Agent Skill
    ├── SKILL.md
    └── prompt.md
```

## 快速开始

### 前置条件

- Python 3.12+
- Node.js 20+
- Java 17+（Neo4j 需要）

### 安装管理器依赖

```bash
cd Arachne
pip install -r requirements.txt
```

### 一键启动全系统

```bash
python arachne_manager.py start
```

输出示例：

```
Starting neo4j...
  Neo4j started on port 7687
Starting backend...
  Backend started on port 8000
Starting frontend...
  Frontend started on port 3000

────────────────────────────────────────────────────────────
Arachne System Status
────────────────────────────────────────────────────────────
  RUNNING   neo4j        PID=52152  port=7687  browser=http://localhost:7474
  RUNNING   backend      PID=51520  port=8000  docs=http://localhost:8000/docs  nodes=36  edges=37
  RUNNING   frontend     PID=50096  port=3000  url=http://localhost:3000
────────────────────────────────────────────────────────────
```

### 访问服务

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端应用 | http://localhost:3000 | 图可视化与交互 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| Neo4j Browser | http://localhost:7474 | 图数据库管理界面（neo4j / arachne123） |

### 一键停止

```bash
python arachne_manager.py stop
```

### 查看图谱统计

```bash
python arachne_manager.py stats
```

### 查看各组件状态

```bash
python arachne_manager.py status
```

### 查看 Neo4j 日志

```bash
python arachne_manager.py logs neo4j
```

## 管理器命令详解

`arachne_manager.py` 是跨平台（Windows / Linux / macOS）的系统管理程序，替代了 Shell 脚本：

```bash
python arachne_manager.py <command> [target]

# 命令
status                    # 显示所有组件状态
start [all|neo4j|backend|frontend]
stop  [all|neo4j|backend|frontend]
stats                     # 从后端获取图谱统计
logs neo4j                # 显示 Neo4j 最近日志
```

**特性：**
- 通过端口检测进程状态，不依赖 PID 文件
- `start` 自动检测已运行组件，跳过重复启动
- 后端启动后自动检测空库并导入 seed 数据
- 停止时先发送 SIGTERM，5 秒内未退出则强制 Kill

## 手动启动（开发调试用）

如果只需要启动单个组件进行调试：

### Neo4j

```bash
# Windows
cd neo4j-community-5.26.0
.\bin\neo4j.bat console

# 默认密码已设为 arachne123
# 修改密码：.\bin\neo4j-admin.bat dbms set-initial-password <新密码>
```

### 后端

```bash
cd backend
.\venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端

```bash
cd frontend
npx vite --host
```

## CLI 工具

`cli/arachne_cli.py` 提供了命令行方式提交数据和查询图谱：

```bash
# 提交种子数据
python cli/arachne_cli.py submit data/seed_industry_graph.json

# 查询统计
python cli/arachne_cli.py query --stats

# 查询子图
python cli/arachne_cli.py query --subgraph silicon_metal

# 列出所有节点
python cli/arachne_cli.py query --list-nodes

# 搜索
python cli/arachne_cli.py query --search "硅"
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/v1/batches` | 批量注册 GraphRegistrationBatch |
| `GET`  | `/api/v1/nodes` | 节点列表（分页、搜索、过滤） |
| `POST` | `/api/v1/nodes` | 创建节点 |
| `GET`  | `/api/v1/nodes/{node_id}` | 获取节点详情 |
| `PUT`  | `/api/v1/nodes/{node_id}` | 更新节点 |
| `DELETE` | `/api/v1/nodes/{node_id}` | 删除节点 |
| `GET`  | `/api/v1/edges` | 边列表（分页、过滤） |
| `POST` | `/api/v1/edges` | 创建边 |
| `GET`  | `/api/v1/edges/{edge_id}` | 获取边详情 |
| `PUT`  | `/api/v1/edges/{edge_id}` | 更新边 |
| `DELETE` | `/api/v1/edges/{edge_id}` | 删除边 |
| `GET`  | `/api/v1/query/subgraph/{node_id}` | 子图查询 |
| `GET`  | `/api/v1/query/neighbors/{node_id}` | 邻接展开 |
| `GET`  | `/api/v1/query/path` | 路径查询 |
| `GET`  | `/api/v1/query/stats` | 图统计信息 |
| `GET`  | `/api/v1/query/conflicts` | 冲突检测 |

## 数据模型

### 节点（IndustrialNode）

```json
{
  "node_id": "silicon_wafer",
  "canonical_name_zh": "硅片",
  "canonical_name_en": "Silicon Wafer",
  "aliases": ["晶圆", "半导体硅片"],
  "definition": "...",
  "entity_type": "material",
  "evidence": [
    {"source_title": "战略新兴产业分类", "source_url": "...", "quote": "..."}
  ],
  "confidence": "HIGH",
  "status": "ACTIVE"
}
```

### 边（GraphEdge）

边使用 `edge_namespace` 作为 discriminator：

**产业流边（industrial_flow）：**
```json
{
  "edge_namespace": "industrial_flow",
  "edge_type": "material_flow",
  "edge_id": "polysilicon_to_ingot",
  "from_node": "polysilicon",
  "to_node": "monocrystalline_silicon_ingot",
  "description": "...",
  "evidence": [...],
  "confidence": "HIGH"
}
```

**本体边（ontology）：**
```json
{
  "edge_namespace": "ontology",
  "edge_type": "is_a",
  "edge_id": "...",
  "from_node": "...",
  "to_node": "...",
  "description": "...",
  "evidence": [...],
  "confidence": "HIGH"
}
```

### 边类型定义

| 命名空间 | 类型 | 语义 |
|----------|------|------|
| `industrial_flow` | `material_flow` | 上游材料 → 下游加工/制造 |
| `industrial_flow` | `composition` | 组件构成整机/系统 |
| `industrial_flow` | `energy_flow` | 能量输入/转换/消耗 |
| `industrial_flow` | `information_flow` | 信息/控制指令传递 |
| `industrial_flow` | `capability_supply` | 能力/服务供给 |
| `ontology` | `is_a` | 是一种/属于 |
| `ontology` | `alias_of` | 别名关系 |
| `ontology` | `variant_of` | 变体关系 |
| `ontology` | `related_term` | 相关术语 |

## 前端功能

- **图可视化**：Cytoscape.js + dagre 自动布局，支持缩放/平移
- **多维过滤**：按边命名空间、边类型、实体类型、节点状态、置信度筛选
- **节点搜索**：按中文名/别名实时搜索，支持拼音首字母
- **详情面板**：点击节点/边查看完整属性、证据、备注
- **局部展开**：双击节点加载邻接子图并自动布局
- **增删改查**：节点和关系的创建、编辑、删除表单
- **批量上传**：上传 `GraphRegistrationBatch` JSON 文件
- **统计概览**：顶部栏实时显示节点/边数量

## Agent Skill

位于 `.kimi/skills/arachne-graph/`，为 Kimi Agent 提供产业本体图操作能力：

- **SKILL.md**：Agent 行为约束、决策树、关系类型说明、证据规范
- **prompt.md**：可直接注入的系统提示词模板

安装方式：将 `.kimi/skills/arachne-graph/` 复制到你的 Kimi skills 目录下。

## 设计原则

| 原则 | 实现 |
|------|------|
| 事实只有一份 | 底层只存 `IndustrialNode` + `IndustrialFlowEdge` + `OntologyEdge` |
| 分类不是关系 | `entity_type` 是节点属性，不自动建立本体边 |
| 方向统一 | 所有产业流边统一为 **上游 → 下游** |
| 弱一致性 | 允许冲突存在，提供 `/query/conflicts` 检测接口 |
| 不自动推理 | Graph Service 只做登记/校验，不做产业链推导 |
| 扩展性预留 | API 版本化（`/api/v1/`），Schema 向后兼容 |

## 故障排查

### Zscaler / 企业代理导致 Docker Hub 无法访问

如果 `docker pull neo4j:5-community` 报 TLS handshake timeout，说明企业代理（如 Zscaler）拦截了 HTTPS 流量。

**解决方案：** 使用公司私有镜像仓库作为缓存：

```bash
# 以 Bose Artifactory 为例
docker pull artifactory.bose.com/asd-docker/library/neo4j:5-community
docker tag artifactory.bose.com/asd-docker/library/neo4j:5-community neo4j:5-community
```

或者跳过 Docker 直接本地安装 Neo4j（本项目已采用此方案）。

### Neo4j 连接失败

后端默认连接 `bolt://localhost:7687`。如果 Neo4j 未启动或密码错误：

1. 检查 Neo4j 是否运行：`python arachne_manager.py status`
2. 检查密码：`backend/app/config.py` 中 `NEO4J_PASSWORD` 默认为 `arachne123`
3. 重置密码：停止 Neo4j，删除 `neo4j-community-5.26.0/data/` 目录，重新启动并设置初始密码

### 前端过滤不生效

早期的 bug 是 `GraphCanvas` 在 filter 变化时被 effect 依赖的不稳定 callback 触发重建，导致过滤结果被覆盖。已在 `GraphCanvas.tsx` 中修复：
- 初始化 effect 依赖改为 `[]`（只初始化一次）
- 使用 `useRef` 维护 `onNodeClick` / `onEdgeClick` / `filters`
- 过滤使用 `toggleClass("hidden")` 而非 `style("display")`，性能更好

## 验证状态

- [x] 后端 FastAPI 启动成功，Swagger UI 正常
- [x] Neo4j 本地安装成功，数据持久化
- [x] 前端 TypeScript 编译通过，Vite 热重载正常
- [x] 36 节点 / 37 边 seed 数据导入成功
- [x] 过滤、搜索、增删改查交互正常
- [x] Agent Skill 封装完成
- [x] Python 跨平台管理器 `arachne_manager.py` 可用
