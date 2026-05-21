# Arachne - 统一产业本体图系统

基于 `spec_v1.md`、`design_v1.md` 和 `core_schema.py` 实现的完整产业本体图系统。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI + Neo4j (异步驱动) |
| 前端 | React 18 + TypeScript + Cytoscape.js + Tailwind CSS |
| 部署 | Docker Compose |
| Agent 支持 | Kimi Skill + Prompt |

## 项目结构

```
Arachne/
├── docker-compose.yml              # Docker 一键部署
├── backend/                        # FastAPI 后端
│   ├── app/
│   │   ├── main.py                 # FastAPI 入口
│   │   ├── config.py               # 环境配置
│   │   ├── database.py             # Neo4j 连接与初始化
│   │   ├── models/schemas.py       # Pydantic 核心 Schema
│   │   ├── routers/                # API 路由
│   │   │   ├── nodes.py            # 节点 CRUD
│   │   │   ├── edges.py            # 边 CRUD
│   │   │   ├── batches.py          # 批量注册
│   │   │   └── query.py            # 查询接口
│   │   └── services/               # 业务逻辑层
│   │       ├── graph_service.py    # 核心图服务
│   │       └── neo4j_storage.py    # Neo4j 存储层
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                       # React 前端
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── GraphCanvas.tsx     # Cytoscape.js 图可视化
│   │   │   ├── FilterPanel.tsx     # 关系/类型过滤
│   │   │   ├── SearchPanel.tsx     # 节点搜索
│   │   │   ├── NodeDetail.tsx      # 节点详情
│   │   │   ├── EdgeDetail.tsx      # 边详情
│   │   │   ├── NodeForm.tsx        # 节点表单
│   │   │   ├── EdgeForm.tsx        # 边表单
│   │   │   ├── BatchUploader.tsx   # 批量上传
│   │   │   └── StatsBar.tsx        # 统计栏
│   │   ├── services/api.ts         # API 客户端
│   │   └── types/index.ts          # TypeScript 类型
│   ├── package.json
│   └── Dockerfile
├── core_schema.py                  # 原始核心 Schema
├── spec_v1.md                      # 工程设计说明
├── design_v1.md                    # 本体图设计文档
└── .kimi/skills/arachne-graph/     # Agent Skill
    ├── SKILL.md
    └── prompt.md
```

## 快速开始

### 方式一：Docker Compose 部署（推荐）

**前置条件：** 安装并启动 [Docker Desktop](https://www.docker.com/products/docker-desktop/)

```bash
# 一键启动 Neo4j + Backend + Frontend
docker-compose up --build -d

# 访问服务
# Neo4j Browser: http://localhost:7474 (neo4j / arachne123)
# API 文档:     http://localhost:8000/api/v1/docs
# Web 应用:     http://localhost:3000
```

### 方式二：本地开发运行

#### 1. 启动 Neo4j

```bash
# 使用 Docker 启动 Neo4j
docker run -d \
  --name arachne-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/arachne123 \
  neo4j:5-community
```

#### 2. 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/v1/batches` | 批量注册 GraphRegistrationBatch |
| `GET`  | `/api/v1/nodes` | 节点列表（分页、搜索、过滤） |
| `POST` | `/api/v1/nodes` | 创建节点 |
| `PUT`  | `/api/v1/nodes/{node_id}` | 更新节点 |
| `DELETE` | `/api/v1/nodes/{node_id}` | 删除节点 |
| `GET`  | `/api/v1/edges` | 边列表（分页、过滤） |
| `POST` | `/api/v1/edges` | 创建边 |
| `PUT`  | `/api/v1/edges/{edge_id}` | 更新边 |
| `DELETE` | `/api/v1/edges/{edge_id}` | 删除边 |
| `GET`  | `/api/v1/query/subgraph/{node_id}` | 子图查询 |
| `GET`  | `/api/v1/query/neighbors/{node_id}` | 邻接展开 |
| `GET`  | `/api/v1/query/path` | 路径查询 |
| `GET`  | `/api/v1/query/stats` | 图统计 |
| `GET`  | `/api/v1/query/conflicts` | 冲突检测 |

## 前端功能

- **图可视化**：Cytoscape.js 渲染，支持 dagre 自动布局
- **关系过滤**：按命名空间（产业流/本体）、实体类型、状态、置信度筛选
- **节点搜索**：按名称/别名实时搜索
- **节点详情**：点击节点查看完整属性、证据、备注
- **边详情**：点击边查看关系详情
- **局部展开**：双击节点加载邻接子图
- **增删改查**：支持节点和关系的创建、编辑、删除
- **批量上传**：上传 `GraphRegistrationBatch` JSON
- **统计概览**：顶部栏实时显示节点/边数量

## Agent Skill 使用

位于 `.kimi/skills/arachne-graph/`，包含：

- **SKILL.md**：完整的 Agent 行为约束、决策树、关系类型说明
- **prompt.md**：可直接注入的系统提示词模板

安装方式：将 `.kimi/skills/arachne-graph/` 目录复制到你的 Kimi skills 目录下。

## 设计原则实现

| 原则 | 实现 |
|------|------|
| 事实只有一份 | 底层只存 IndustrialNode + IndustrialFlowEdge + OntologyEdge |
| 分类不是关系 | `entity_type` 是属性，不自动建立边 |
| 方向统一 | 所有产业流边统一 上游→下游 |
| 弱一致性 | 允许冲突存在，提供冲突检测接口 |
| 不自动推理 | Graph Service 只登记/校验，不做产业链推导 |
| 扩展性预留 | API 版本化 (`/api/v1/`) |

## 验证状态

- [x] 后端 FastAPI 语法检查通过
- [x] 后端路由加载成功（/health, /docs 正常）
- [x] 前端 TypeScript 编译通过
- [x] 前端 Vite 构建成功
- [x] Agent Skill 封装完成
- [ ] Docker Compose 部署（需启动 Docker Desktop）
