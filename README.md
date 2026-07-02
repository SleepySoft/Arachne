# Arachne

<figure style="text-align: center;">
  <img src="docs/logo.png" alt="Arachne">
  <figcaption>编织世界真相</figcaption>
</figure>

## PRINCIPLE

和所有的中二少年一样，我也想做一个系统来描述世界、理解世界，帮我看到纷繁事件间的联系，发掘事件背后的关联与真相。

我看过不少图谱项目，但其中的90%都是抓取数据，然后一股脑扔进图谱里。看起来很J8酷炫，但就像诗云一样，包含一切的同时也混杂一切。熵没有降低，毫无意义。

我自己也做过几个图谱原型，但始终不满意。直到某一天，我在思考公司、行业和产业链图谱时， 突然冒出了一个绝妙的想法：

公司、行业和产业链三者不是正交的，相反，它们的概念和要素之间的关系有相交和包含。即便从语义上考虑，也很难采用简单的关系将三者放在同一张图里。

另一个问题在于：公司的信息有时效性，今年所从事的产业和去年未必相同，上下游也是每年都会变化。在一张图里维护节点（增加，更新，删除）是非常messy的操作。

但如果我将产业和公司当作一个视图呢？即我只记录产业链物料与服务的关联，所谓的行业只不过是整个产业链物料和服务的一个子集。

而公司除了作为产业链的一个子集外，还能通过物料与服务之间的关系，计算出与其它公司的，产业链上的关联。

这个设计，特别对于公司来说，更有额外几个好处：

1. 公司视图可以根据任意时刻的公司数据计算，没有更新烦恼。
2. 通常我们能在财报中找到公司的产品服务，但不一定能找到它的上游依赖，但只要有产品和服务信息，我们就能从产业链中推论出有可能成为它上流的企业。
3. 公司财报中可能会有前十大客户的信息，我们将其做为有证据的关联，和第2点产业链关联能清楚区分开。

而从使用角度来说，这张图的核心目的应当是帮助人们探索产业链和背后公司的公司，而非作为一个大而全的数据库。
因此“怎样能通过图谱讲一个故事”，这一点是我在该项目设计中最重要的考量。


## UI

![arachne_ui.png](docs/arachne_ui.png)

## DESIGN

#### 基本特性

综合以上考虑，从根本性上来说，该系统应该提供以下特性：

1. 对人友好的探索和编辑界面，对AI友好的API服务。
    > 自然的浏览操作：拖动、缩放、单选、多选、右键菜单、ESC、Delete
 
    > 进阶浏览操作：拉近/显示/高亮上下游，上一个/下一个节点

    > 布局操作：水平/垂直对齐和均匀排列、视图回退

    > 过滤操作：按类型、行业、公司、状态

    > 探索操作：聚焦节点、隐藏节点、逐步显示上下游

    > 记录与分享：版本管理、保存、载入、导出、导出

    > AI支持：文档、CLI、SKILL

2. 通过限制与规则约束使图的结构符合设计。
    > 规则及原则定义 - 公司节点不得与产业节点有任何关联，等等。

    > 接口强限制与检查 - 参数必须符合schema定义

    > 随时可执行的扫描检查 - 提供检查页面，根据规则扫描，报告错误与警告

#### 技术栈

程序使用 Neo4j 存储图数据（节点与关系），使用 PostgreSQL 保存公司、行业、节点暴露关系等结构化数据；
后端基于 FastAPI（Python） 提供 REST API，前端采用 React + Vite 构建，图可视化部分使用 Cytoscape.js 实现。


## Usage

#### 部署

> 本项目默认在 Windows 本地以原生服务方式运行（Neo4j + PostgreSQL + Python 后端 + Vite 前端）。仓库也提供 `docker-compose.yml` 作为参考，但当前开发环境以本地安装为准。

##### 环境要求

- Windows 10/11（PowerShell 5.1+）
- Python 3.12
- Node.js 18+
- Neo4j 5.26.0 Community（需自行下载并放到 `neo4j-community-5.26.0/`）
- PostgreSQL 17（需自行下载并放到 `postgresql/pgsql/`）

##### 目录结构

```
Arachne/
├── backend/              # FastAPI 后端
│   ├── app/
│   ├── venv/             # Python 虚拟环境
│   └── requirements.txt
├── frontend/             # React + Vite 前端
│   └── node_modules/
├── neo4j-community-5.26.0/   # 本地 Neo4j（需自行准备，见下文）
├── postgresql/pgsql/         # 本地 PostgreSQL（需自行准备，见下文）
├── scripts/
│   ├── start-all.ps1
│   ├── stop-all.ps1
│   └── import_db.py
└── data/ArachneData/     # 图谱数据
```

> 注意1：`neo4j-community-5.26.0/` 和 `postgresql/pgsql/` 为本地运行目录，不包含在 Git 仓库中。 clone 代码后需按下面步骤自行下载并解压到对应位置。

> 注意2：本仓库为程序本体，数据图谱在另一个仓库：https://github.com/SleepySoft/ArachneData ，当前它作为本项目的一个子模块被引用进来。

##### 1. 安装后端依赖

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

后端默认连接：
- Neo4j: `bolt://localhost:7687`（用户名 `neo4j`，密码 `arachne123`）
- PostgreSQL: `postgresql://postgres:postgres@localhost:5433/arachne`

可在 `backend/app/config.py` 或环境变量中修改。

##### 2. 安装前端依赖

```powershell
cd frontend
npm install
```

##### 3. 准备数据库

**Neo4j**

1. 下载 Neo4j 5.26.0 Community 版：
   - 官方下载页：https://neo4j.com/download-center/#community
   - 或 Neo4j Deployment Center：https://deployment.neo4j.com/5.26.0/neo4j-community-5.26.0-windows.zip
2. 解压到项目根目录，确保目录名为 `neo4j-community-5.26.0/`。
3. 设置初始密码（仅需一次）：

```powershell
cd neo4j-community-5.26.0
.\bin\neo4j-admin dbms set-initial-password arachne123
```

4. 确认 `conf/neo4j.conf` 中 bolt 端口为 `7687`（默认即是）。

**PostgreSQL**

1. 下载 PostgreSQL 17 Windows 二进制包（zip 版）：
   - 官方下载页：https://www.postgresql.org/download/windows/
   - 或 PostgreSQL 二进制镜像（EnterpriseDB / BigSQL）
2. 解压到 `postgresql/pgsql/`。
3. 初始化数据目录（仅需执行一次）：

```powershell
cd postgresql\pgsql
.\bin\initdb.exe -D .\data -U postgres --encoding=UTF8 --locale=C
# 启动服务
.\bin\pg_ctl.exe -D .\data -l logfile start
```

后端首次启动时会自动创建 `arachne` 数据库及所需表（`industries`、`companies`、`company_node_exposures`、`persons`、`factual_relations` 等）。

##### 4. 一键启动

```powershell
# 在项目根目录
.\scripts\start-all.ps1
```

该脚本会按顺序启动：
1. Neo4j（端口 7687）
2. PostgreSQL（端口 5433）
3. FastAPI 后端（端口 16060）
4. Vite 前端（端口 3000）

如果 Neo4j 图谱为空，脚本会自动导入 `data/seed_industry_graph.json` 作为种子数据。

##### 5. 数据导入

将导出的图谱数据导入 Neo4j：

```powershell
cd scripts
python import_db.py --input-dir ../data/ArachneData/newest --clear --yes
```

`--clear` 会先清空现有图数据，请谨慎使用。

##### 6. 访问服务

| 服务 | 地址 |
|------|------|
| 前端应用 | http://localhost:3000 |
| 后端 API 文档 | http://localhost:16060/docs |
| Neo4j Browser | http://localhost:7474 |
| PostgreSQL | localhost:5433 |

##### 7. 停止服务

```powershell
.\scripts\stop-all.ps1
```

##### 常见问题

**Q: 端口被占用**

检查 7687、5433、16060、3000 是否已被占用。`start-all.ps1` 会自动跳过已运行的服务。

**Q: PostgreSQL 提示数据库不存在**

先确保 PostgreSQL 已启动，然后创建数据库：

```powershell
cd postgresql\pgsql
.\bin\createdb.exe -U postgres arachne
```

**Q: 前端构建失败**

确认 Node.js 版本 ≥ 18，并删除 `frontend/node_modules` 后重新 `npm install`。

**Q: Docker 方式**

仓库提供 `docker-compose.yml`，可直接：

```powershell
docker-compose up -d
```

注意：当前开发环境因网络策略未使用 Docker，compose 文件未包含 PostgreSQL，如需完整容器化部署需自行补充。

#### 快速上手

访问：http://localhost:3000/

菜单：导入 -> 选择 [views/semiconductor.json](views/semiconductor.json)

菜单：载入 -> 选择最新的版本

#### 操作

滚轮：缩放

ESC：取消选择/高亮（遇事不决ESC）

左键按下：选择并高亮

左键按下拖动：圈选节点

中键按下拖动：拖动画布

CTRL+左键按下拖动：拖动画布

> 注1：菜单提供导航功能，可以快速在上一个/下一个节点之间跳跃

> 注2：菜单提供恢复上一个布局功能，防止误操作打乱布局

> 注3：当显示的节点非全部节点时，右上角会显示“返回全图按钮”

右键-空白处：菜单1

右键-节点上：菜单2

右键-边上：菜单3

右键-多选情况：菜单4

Delete：选中边可删除

#### 编辑视图

可手动调整布局使图按你的心意显示。

右键提供拉近节点和对齐功能，非常实用。

误操作布局不要慌，可以点“恢复上一个布局”。

注意及时保存。

#### 探索

节点非常多，并不利于观看。可以从某些关注的节点出发，选中并右键 -> 聚焦选中节点，然后从可见节点逐步探索。

#### 编辑数据

虽然本程序尽可能提供友好的界面供用户录入数据，但我还是建议数据的录入通过Agent进行。

程序中的skills目录专供Agent使用。

建议：增加数据不要贪多，虽然数据通过Agent编辑，但要想数据有价值，还需要人一步步调整评估和指导。

> 注：当前的规则还不算成熟，等我彻底考虑清楚了再把规则这一块补全。

## TODO

时间紧张，慢慢更新。
