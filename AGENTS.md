# Arachne Industrial Ontology Graph — Agent Context

> This file tracks project state, architecture decisions, and pending work.
> Read this first before making any changes.

---

## 1. Project Overview

Arachne is an **industrial ontology graph system** with a two-domain architecture:

```
Industrial Graph (产业图)           ← Neo4j: 技术链/本体
       ↓ (bridge: PG company_node_exposures)
Factual Graph (事实关系图)          ← Neo4j + PG: 人/公司/事实关系
```

**Previous three-layer view pyramid (Industry → Industrial → Company View) has been retired.**
Company-to-company upstream/downstream inference is now dynamic per-company
(via `/explore` endpoints and the older `/companies/{id}/exploration-graph`
endpoints) rather than batch-computed and persisted.

**Core principle:** Industrial nodes are the single source of truth. Companies connect to nodes via `CompanyNodeExposure` (edges in the relational model), never redefine nodes.

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Graph DB | Neo4j 5.26.0 (local install) |
| Relational DB | PostgreSQL (local install in `postgresql/pgsql/`, port 5433) |
| Async DB Driver | `neo4j` (async), `asyncpg` (PostgreSQL) |
| Frontend | React + Vite (dev server on :3000) |
| Test | pytest + pytest-asyncio |

### Environment
- **OS**: Windows (PowerShell)
- **Backend**: `http://localhost:8000`
- **Frontend**: `http://localhost:3000`
- **Neo4j**: `bolt://localhost:7687` (user: `neo4j`, pass: `arachne123`)
- **PostgreSQL**: `postgresql://postgres:postgres@localhost:5433/arachne` (running, tables initialized)

### System Management
- `scripts/start-all.ps1` / `scripts/stop-all.ps1` — PowerShell one-click scripts (Neo4j + PostgreSQL + Backend + Frontend)
- See `README.md` for troubleshooting.

---

## 3. Architecture

### 3.1 Database Division of Labor

| Data | Store | Notes |
|---|---|---|
| Industrial nodes & edges | Neo4j | `IndustrialNode`, `INDUSTRIAL_FLOW`, `ONTOLOGY` |
| Industries + node mappings | PostgreSQL | `industries`, `industry_node_mappings` |
| Companies + node exposures | PostgreSQL | `companies`, `company_node_exposures` |
| Persons + factual relations | PostgreSQL + Neo4j | `persons`, `factual_relations` tables; `:Person`, `:Company` nodes + typed relations in Neo4j |
| Computation jobs | PostgreSQL | `computation_jobs` (async/batch job tracking) |

### 3.2 Backend Directory Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI entry, registers all routers
│   ├── config.py                  # Settings (Neo4j + PostgreSQL URLs)
│   ├── database.py                # Neo4j async driver
│   ├── database_postgres.py       # asyncpg pool + table init (7 tables)
│   ├── models/
│   │   ├── schemas.py             # Core graph models (Node, Edge, Evidence, RecordStatus)
│   │   ├── industry_schema.py     # Industry, IndustryNodeMapping, IndustryType
│   │   ├── company_schema.py      # Company, CompanyNodeExposure, CompanyActivityType, CompanyType, BusinessRegistrationBatch
│   │   └── factual_graph_schema.py # Person, FactualRelation, three relation types
│   ├── services/
│   │   ├── neo4j_storage.py       # Neo4j CRUD + subgraph queries
│   │   ├── graph_service.py       # Business logic: nodes, edges, batches, conflicts, business batch processing
│   │   ├── industry_storage.py    # PostgreSQL CRUD for industries + mappings
│   │   ├── company_storage.py     # PostgreSQL CRUD for companies + exposures
│   │   ├── factual_graph_storage.py # PG + Neo4j for Factual Graph
│   │   ├── company_exploration.py # Heterogeneous company↔node exploration graph
│   │   └── company_material.py    # Material-flow based company connections
│   └── routers/
│       ├── nodes.py               # /api/v1/nodes
│       ├── edges.py               # /api/v1/edges
│       ├── batches.py             # /api/v1/batches (GraphRegistrationBatch)
│       ├── business_batches.py    # /api/v1/business-batches (BusinessRegistrationBatch)
│       ├── industries.py          # /api/v1/industries + /mappings + /nodes + /subgraph + /by-node
│       ├── companies.py           # /api/v1/companies + /nodes + /subgraph + /exposures + /by-node
│       ├── company_exploration.py # /api/v1/companies/{id}/exploration-graph + /nodes/{id}/connected-companies
│       ├── company_material.py    # /api/v1/companies/{id}/material-connections
│       ├── computation_jobs.py    # /api/v1/computation-jobs
│       ├── factual_graph.py       # /api/v1/factual-graph (Person + Relations)
│       ├── explore.py             # /api/v1/explore (cross-domain)
│       └── query.py               # /api/v1/query (subgraph, neighbors, paths, stats, conflicts)
└── tests/
    ├── test_database_postgres.py
    ├── test_industry_storage.py
    ├── test_company_storage.py
    ├── test_industry_company_routers.py
    └── test_business_batches.py
```

### 3.3 Key API Endpoints

**Industries**
- `POST /api/v1/industries` — create
- `GET /api/v1/industries` — list (paginated, filter by `industry_type`, `status`, `search`)
- `GET /api/v1/industries/{id}` — detail
- `PUT /api/v1/industries/{id}` — update
- `DELETE /api/v1/industries/{id}` — delete
- `GET /api/v1/industries/{id}/mappings` — list node mappings
- `POST /api/v1/industries/{id}/mappings` — create a mapping
- `DELETE /api/v1/industries/{id}/mappings/{mapping_id}` — delete a mapping
- `GET /api/v1/industries/{id}/nodes` — mapped IndustrialNodes
- `GET /api/v1/industries/{id}/subgraph` — Neo4j subgraph of mapped nodes + edges
- `GET /api/v1/industries/by-node/{node_id}` — reverse lookup: industries mapping a node

**Companies**
- `POST /api/v1/companies` — create
- `GET /api/v1/companies` — list (paginated, filter by `country`, `company_type`, `status`, `search`)
- `GET /api/v1/companies/{id}` — detail
- `PUT /api/v1/companies/{id}` — update
- `DELETE /api/v1/companies/{id}` — delete
- `GET /api/v1/companies/{id}/exposures` — list node exposures (filter by `activity_type`)
- `POST /api/v1/companies/{id}/exposures` — create an exposure
- `DELETE /api/v1/companies/{id}/exposures/{exposure_id}` — delete an exposure
- `GET /api/v1/companies/{id}/nodes` — exposed IndustrialNodes
- `GET /api/v1/companies/{id}/subgraph` — Neo4j temporary subgraph of exposed nodes + edges
- `GET /api/v1/companies/by-node/{node_id}` — reverse lookup: companies exposing a node

**Company Exploration (heterogeneous graph)**
- `GET /api/v1/companies/{id}/exploration-graph` — company-centered heterogeneous graph
- `GET /api/v1/companies/nodes/{node_id}/connected-companies` — peer/upstream/downstream companies

**Company Material Connections**
- `GET /api/v1/companies/{id}/material-connections` — material-flow based company connections

**Factual Graph**
- `POST /api/v1/factual-graph/persons` — create Person
- `GET /api/v1/factual-graph/persons` — list persons
- `GET /api/v1/factual-graph/persons/{id}` — person detail
- `PUT /api/v1/factual-graph/persons/{id}` — update person
- `POST /api/v1/factual-graph/relations` — create a factual relation
- `GET /api/v1/factual-graph/relations` — list relations
- `GET /api/v1/factual-graph/relations/{id}` — relation detail
- `PUT /api/v1/factual-graph/relations/{id}` — update relation
- `GET /api/v1/factual-graph/persons/{id}/neighborhood` — person-centered relations
- `GET /api/v1/factual-graph/companies/{id}/neighborhood` — company-centered factual relations

**Cross-domain Explore**
- `GET /api/v1/explore/companies/{id}/industrial-context`
- `GET /api/v1/explore/nodes/{id}/ecosystem`
- `GET /api/v1/explore/persons/{id}/industrial-footprint`
- `GET /api/v1/explore/companies/{id}/full-context`

**Quick Create (Draft Mode)**
- `POST /api/v1/nodes/quick-create` — create a draft node with only a name
- `POST /api/v1/edges/quick-create` — create a draft industrial-flow edge with only from/to nodes
- `GET /api/v1/nodes/fuzzy-search` — fuzzy node name search to detect near-duplicates without vector DB

**Batches**
- `POST /api/v1/batches` — GraphRegistrationBatch (nodes + edges)
- `POST /api/v1/business-batches` — BusinessRegistrationBatch (industries + mappings + companies + exposures)

---

## 4. Completed Work

### Commit 1 — PostgreSQL Infrastructure
- `database_postgres.py`: asyncpg pool + `init_postgres_tables()` creates **7 tables**
  (`industries`, `industry_node_mappings`, `companies`, `company_node_exposures`, `computation_jobs`, `persons`, `factual_relations`)
- `config.py`: `POSTGRES_URL` setting (default port 5433)
- `requirements.txt`: added `asyncpg`
- `test_database_postgres.py`: connection test (currently only asserts the original 4 tables)

### Commit 2 — Industry Storage Layer
- `industry_schema.py`: `Industry`, `IndustryNodeMapping`, `IndustryType` enum
- `industry_storage.py`: full CRUD + `get_mapping_by_industry_and_node()` + `update_mapping()`
- `test_industry_storage.py`: full test coverage
- **Note:** `GET /api/v1/industries/{id}/subgraph` is implemented inline in `routers/industries.py`, not in `industry_storage.py`.

### Commit 3 — Company Storage Layer
- `company_schema.py`: `Company`, `CompanyNodeExposure`, `CompanyActivityType` enum, `BusinessRegistrationBatch`, `CompanyType` + financial/location fields
- `company_storage.py`: full CRUD + `get_exposure_by_company_and_node()` + `update_exposure()` + `list_exposures_by_node()`
- `test_company_storage.py`: full test coverage
- **Note:** `GET /api/v1/companies/{id}/subgraph` and `GET /api/v1/companies/by-node/{node_id}` are implemented inline in `routers/companies.py` (subgraph query) and via `list_exposures_by_node()` + `get_company()` (reverse lookup), not as standalone storage helpers.

### Commit 4 — REST API Routes + Neo4j Subgraph
- `industries.py`: all industry endpoints, including `/nodes`, `/subgraph`, `/by-node`
- `companies.py`: all company endpoints, including `/nodes`, `/subgraph`, `/by-node`
- `main.py`: registered new routers
- `test_industry_company_routers.py`: end-to-end API tests

### Commit 5 — Business Batch Extension
- `business_batches.py`: new router for `BusinessRegistrationBatch`
- `graph_service.py`: `process_business_batch()` with upsert logic for all 4 entity types
- `industry_storage.py`: added `get_mapping_by_industry_and_node()` + `update_mapping()`
- `company_storage.py`: added `get_exposure_by_company_and_node()` + `update_exposure()`
- `company_schema.py`: added `CompanyType` enum + missing fields (`country`, `province`, `city`, `founded_year`, `employee_count`, `revenue_cny`, `market_cap_cny`, `net_profit_cny`, `company_type`)
- `industry_schema.py` / `company_schema.py`: UUID fields now have `default_factory=uuid4`
- `test_business_batches.py`: 4 tests (full batch, upsert existing, mapping dedup, empty batch)
- Cleaned up root-level stale files: `company_schema.py`, `core_schema.py`, `industry_schema.py`

### Commit 6 — Factual Graph Backend (Phase 2 backend)
- `factual_graph_schema.py`: `Person`, three relation types, `FactualRelation` discriminated union
- `factual_graph_storage.py`: PG CRUD + Neo4j sync for persons and relations
- `factual_graph.py`: full REST router for persons, relations, and neighborhood queries
- `database_postgres.py`: added `persons` and `factual_relations` tables

### Commit 7 — Cross-domain Exploration Backend
- `explore.py`: cross-domain endpoints bridging Industrial Graph and Factual Graph
- `company_exploration.py`: heterogeneous company exploration graph endpoints
- `company_material.py`: material-flow based company connection endpoints
- `computation_jobs.py`: async computation job tracking endpoints

### Commit 12 — Top Bar DB Health Indicators (Neo4j + PostgreSQL)
- `backend/app/routers/query.py`: added `GET /api/v1/query/health` endpoint that checks Neo4j and PostgreSQL connectivity
- `frontend/src/services/api.ts`: added `getHealth()` wrapper
- `frontend/src/components/StatsBar.tsx`: added Neo4j and PostgreSQL status dots with 10s polling; green = ok, amber = not configured, red = error

### Commit 11 — Semiconductor Industry View: Start PostgreSQL + Create Industry + Mappings + Auto-filter
- Started local PostgreSQL from `postgresql/pgsql/bin` on port 5433 (configured in `postgresql.conf`)
- Initialized PostgreSQL tables via `init_postgres_tables()`
- Created `semiconductor_industry` formal industry in PostgreSQL with description and evidence
- Created 32 industry-to-node mappings linking the semiconductor industry to core nodes (materials, equipment, chips, business models, downstream applications)
- Restarted backend so it picks up the PostgreSQL pool; industry endpoints now return data
- `frontend/src/App.tsx`: selecting an industry in the sidebar now auto-loads the industry subgraph into the main canvas, so the main graph is filtered to show only nodes/edges belonging to that industry
- Updated `AGENTS.md` to reflect PostgreSQL is running

### Commit 10 — Fuzzy Node Search + Duplicate Prevention + Incomplete Items (Frontend + Backend + CLI + Skills)
- `backend/app/services/fuzzy_search.py`: pure-Python fuzzy matcher combining substring containment, character bigram Jaccard, token overlap, and `difflib.SequenceMatcher` similarity; no vector DB or external dependencies
- `backend/app/routers/nodes.py`: added `GET /api/v1/nodes/fuzzy-search?query=&limit=&score_threshold=` endpoint
- `backend/app/services/graph_service.py` / `routers/query.py`: added `GET /api/v1/query/incomplete-items?limit=` to scan draft nodes, missing definitions, placeholder edges, and isolated nodes
- `frontend/src/services/api.ts`: added `fuzzySearchNodes()` wrapper
- `frontend/src/components/SimilarNodesPanel.tsx`: new component listing similar nodes with confidence badges and one-click selection
- `frontend/src/components/QuickNodeForm.tsx` / `NodeForm.tsx`: debounced fuzzy search while typing; warns users about potential duplicates and lets them select an existing node instead of creating a new one
- `cli/arachne_cli.py`: added `query --fuzzy-search <query>` and `query --incomplete-items` commands
- `skills/arachne-api/SKILL.md`: documented fuzzy search and added an AI workflow for scanning and curating incomplete items
- `backend/app/services/neo4j_storage.py`: fixed pre-existing `get_subgraph` Cypher bug where `$depth` parameter was used inside path length pattern and returned columns did not match `_node_from_record`/`_edge_from_record`
- No new Python dependencies required

### Commit 9 — Quick Edge Creation (Frontend + Backend + CLI + Skills)
- `schemas.py`: added `IndustrialFlowEdgeQuickCreate` input model with auto-generated `edge_id`, default `edge_type=material_input`, and auto-generated description
- `graph_service.py`: added `quick_create_edge()` service that validates endpoints, resolves a unique `edge_id`, fills placeholders, and creates an `IndustrialFlowEdge`
- `edges.py`: added `POST /api/v1/edges/quick-create` endpoint
- `QuickEdgeForm.tsx`: new minimal form to add an upstream/downstream edge, with searchable node picker, edge-type selector, optional description/notes, and an "expand to full form" button that pre-fills `EdgeForm`
- `NodeDetail.tsx`: removed the duplicate top-level "添加上游/下游" buttons; all relationship creation now flows through `NodeEdgeList`
- `NodeEdgeList.tsx`: relationship management now defaults to `QuickEdgeForm` when adding, while still supporting full `EdgeForm` via the expand action or edit action
- `api.ts` / `types/index.ts`: added `quickCreateEdge()` wrapper and `IndustrialFlowEdgeQuickCreate` type
- `cli/arachne_cli.py`: added `quick-edge` command (`--from`, `--to`, `--edge-type`, `--description`, `--notes`)
- `skills/arachne-api/SKILL.md`: documented `quick-edge` usage and the frontend quick-add workflow
- Restarted backend uvicorn on port 16060 and verified `POST /api/v1/edges/quick-create` returns 201

### Commit 8 — Industry Mapping Workflow + Draft Node Quick Add (Frontend + Backend + CLI + Skills)
- `IndustryMappingForm.tsx`: new create/edit form for industry-to-node mappings, with searchable node picker, role/weight/confidence/status/evidence/notes fields
- `IndustryDetail.tsx`: replaced the `alert("添加映射功能待实现")` stub with inline add/edit mapping UI; added per-mapping edit/delete actions
- `NodeIndustriesPanel.tsx`: added "关联到新行业" form to associate the current node with an existing industry
- `IndustryForm.tsx`: added aliases input (comma-separated) so created industries can have aliases
- `api.ts`: added `updateIndustryMapping()` wrapper
- `industries.py`: added `PUT /api/v1/industries/{id}/mappings/{mapping_id}` endpoint
- `schemas.py` / `graph_service.py` / `nodes.py`: added `IndustrialNodeQuickCreate` schema and `POST /nodes/quick-create` endpoint for minimal-effort draft node creation
- `neo4j_storage.py` / `nodes.py`: added `draft_only` filter to `list_nodes` for discovering incomplete nodes
- `QuickNodeForm.tsx` / `SearchPanel.tsx`: frontend quick-add entry point with draft-node badge and draft-node list
- `NodeDetail.tsx`: added "草稿节点 / 待完善" banner for draft/incomplete nodes
- `SearchPanel.tsx`: fixed search/draft dropdown item text layout (vertical text → single-line with truncation)
- `GraphCanvas.tsx`: enhanced single-node highlight style (larger border, larger node, yellow label); changed highlight animation from `fit` (zoom) to `center` (pan only); added fallback to fetch and add node if selected from search but not loaded in current graph
- `cli/arachne_cli.py`: added `industry update-mapping` and `quick-node` commands; `query --draft-only` flag
- `skills/arachne-api/SKILL.md`: updated with `update-mapping`, `quick-node`, `query --draft-only` examples and frontend UI operation guide
- `.kimi/skills/arachne-graph/SKILL.md`: added guidance that market concepts / themes should be registered as `Industry` rather than nodes
- `test_industry_storage.py`: removed stale `IndustryCreate` import
- `StatsBar.tsx` / `App.tsx`: fixed pre-existing TypeScript errors that blocked the production build (dead `MainView` type, unused setters)

### Commit 15 — 独占式画布拖拽（Ctrl/Cmd / 鼠标中键）
- `frontend/src/components/GraphCanvas.tsx`: 新增两种不依赖空白区域的画布拖拽方式
  - 按住 `Ctrl` / `Cmd` 时，节点变为不可抓取，拖动任意位置均可平移画布
  - 按住鼠标中键拖动，直接平移画布（阻止 Cytoscape 默认的节点抓取/选择）
- `frontend/src/styles/index.css`: 增加 `.canvas-pan-modifier` / `.canvas-middle-panning` 光标样式（grab / grabbing）

### Commit 14 — 节点/关系增删改保持视图不变
- `frontend/src/components/GraphCanvas.tsx`: 新增 `updateNode(node)` / `updateEdge(edge)` ref 方法，就地更新 Cytoscape 元素数据而不触发重新布局
- `frontend/src/App.tsx`: 新增 `onNodeUpdated`、`onNodeDeleted`、`onEdgeCreated`、`onEdgeUpdated`、`onEdgeDeleted` 回调，直接操作 `GraphCanvasRef` 增删改元素，不再调用 `refreshGraph()`
- `frontend/src/components/panels/RightPanel.tsx` / `NodeDetail.tsx` / `NodeAssociations.tsx` / `NodeEdgeList.tsx` / `EdgeDetail.tsx`: 把节点/关系变更事件透传到 canvas，删除关系后仅移除对应边，删除节点后仅移除对应节点，编辑/创建后仅更新/新增元素
- 修复了删除一条边导致整个画布重新布局、当前视角和节点位置全部丢失的问题

### Commit 13 — 节点拉近 (Edge Pull)
- `frontend/src/components/EdgeContextMenu.tsx`: added "拉近节点" menu item (only shown when an `onPull` handler is provided)
- `frontend/src/components/GraphCanvas.tsx`: exposed `pullEdgeEndpointsIntoView(edgeId)` via ref; moves off-screen endpoint(s) of the selected edge into the current viewport while keeping the camera and other node positions unchanged
- `frontend/src/App.tsx`: wired the edge context menu's "拉近节点" action to `GraphCanvasRef.pullEdgeEndpointsIntoView`
- Movement is animated (200 ms ease-out); if both endpoints are off-screen, both are pulled toward the viewport center

### Historical Fixes (carried over)
- **HTTP 422 fix**: `page_size` query limit relaxed from `le=100` to `le=1000`
- **Frontend filter bug**: `GraphCanvas` `useEffect` deps fixed with `useRef` + `useCallback`
- **Neo4j compatibility**: evidence serialized as JSON string; `neo4j.time.DateTime` → Python `datetime`
- **Neo4j deployment**: local Windows install (Docker blocked by Zscaler)

### Recent Changes
- **Smart undo fix**: The "恢复上个视图" button was restoring the post-drag state instead of the pre-drag state because the view-history push was triggered in the `dragfree` (end-of-drag) handler after the node had already moved. Moved the push into the `grab` (start-of-drag) handler so the snapshot captures positions *before* the gesture. Added `dragHistoryPushedRef` to ensure a multi-node drag gesture pushes history only once; the previous `cy.nodes(":grabbed").length <= 1` guard failed because `:grabbed` is not populated when the `grab` event fires. Then narrowed the undo scope to **layout only** (node positions): removed `onBeforeCameraChange` push from all canvases, so panning/zooming no longer adds to the undo stack and does not affect the button. Renamed the toolbar button to "恢复上一个布局" and updated its tooltip. Also added `pushIndustrialHistory(true)` before right-click "拉近" operations (`pullEdgeEndpointsIntoView` and `pullNeighborsIntoView`) so these layout changes are also recoverable. Removed the process-group toggle from the undo stack (it is a content change, not a layout change) and made layout-only undo restore only node positions, leaving the current camera unchanged. Reset the undo stack when loading a view from the view manager, so old layout entries do not leak across different views. Reordered the node context menu so that "拉近上游节点" / "拉近下游节点" appear at the top of the neighbor-action group, and changed their icon from `Eye` to `Move` to avoid confusion with the focus/hide actions. Fixed the "返回全图" button not appearing after hiding nodes: the button now shows whenever the view is not the full graph (active industry/company selection, focus mode, hidden nodes, subgraph, or highlighted nodes), and clicking it also clears focus and hide states in addition to clearing selections. Added multi-node "查看关联公司": select multiple industrial nodes, right-click, and choose "查看关联公司" to see the union of companies exposed to any of the selected nodes. The list is loaded asynchronously via the new backend endpoint `POST /api/v1/companies/by-nodes`; clicking a company row highlights the related nodes in the graph, and the `Info` icon opens the company detail panel.
- **EntityType redesign**: Replaced old taxonomy (`component`, `module`, `subsystem`, `application_system`) with new industrial ontology types (`part`, `equipment`, `software`, `standard`, `data_asset`). Deprecated values kept in `EntityType_Deprecated`. Migrated 797 Neo4j nodes with default mapping; `component` → `part`, `subsystem` → `system`, `application_system` → `software`. Frontend type union, colors, and node forms updated. Prompts/skills updated to new types.
- **Process node type + `process_output` edge type**: `EntityType.PROCESS` and `IndustrialFlowType.PROCESS_OUTPUT` added to backend/frontend schemas; used for material/equipment → process → product flow modeling.
- **Ontology rules registry**: `backend/app/services/ontology_rules.py` is the code-side single source of truth for design rules; `docs/ontology_design_rules.md` documents material/process granularity and the canonical `Input → Process → Output` flow.
- **New DB checkers**: `entity_domain_boundary`, `device_to_product_direct_edge`, `input_to_product_direct_edge` enforce cross-domain isolation and the process-intermediation rule.
- **Frontend modularization**: `frontend/src/App.tsx` refactored from 1120 lines to ~280 lines by extracting `useIndustrialGraph`, `useCompanyGraph`, and panel components under `frontend/src/components/panels/`.
- **High-frequency process refactor**: Inserted process nodes for automotive steel/aluminum forming, copper processing, glass/optical fiber manufacturing, semiconductor wafer/design flows, and remaining domains (aluminum/cement/wood/real estate/paper/PCB/PET/plastic/rubber/steel sheet); `input_to_product_direct_edge` violations reduced from 46 to 0.
- **Semiconductor industry process layer**: Added `chip_packaging_and_testing` and `electronics_system_integration` process nodes, mapped all front-end and back-end process nodes to `semiconductor_industry`, and redirected chip's direct application-system edges through the new process layer. `chip` out-degree reduced from 9 to 2; reverse_industrial_flow conflicts reduced from 3 to 2.
- **Neo4j connection resilience**: Added connection pool settings (`max_connection_lifetime`, `connection_acquisition_timeout`, `max_connection_pool_size`) and global exception handlers for `ServiceUnavailable` / `SessionExpired` / `ConnectionResetError` to return 503 instead of crashing uvicorn.
- **Node search ranking fix**: `list_nodes` now boosts exact matches, then prefix matches, then substring matches; also searches `canonical_name_en`. Searching "芯片" now returns the `chip` node first instead of being buried after other chip-related nodes.
- **Front-end process link to wafer manufacturing**: Added `is_a` ontology edges from `lithography_process`, `etching_process`, `thin_film_deposition_process`, `ion_implantation_process`, `cmp_process`, `cleaning_process`, and `metrology_inspection` to `wafer_manufacturing`. This resolves the reported isolation of `photoresist` / `lithography_process` by connecting them into the wafer manufacturing flow.
- **Graph visual editing mode**: Implemented in `GraphCanvas` with right-click canvas → create node (quick/full), right-click edge → delete, Delete key to remove selected edge, and a connect-mode toolbar to draw edges between nodes. The canvas exposes imperative methods (`addNode`/`addEdge`/`removeEdge`) so edits appear immediately without a full graph reload.
- **Bug fix**: `EntityType.COMPONENT` in `backend/app/models/schemas.py` was mistakenly `"compon"`; fixed to `"component"`, resolving the 500 error on `GET /api/v1/nodes`.
- **Process hierarchy (`part_of`)**: Added `part_of` ontology relation for subprocess-to-aggregate-process composition. Migrated front-end semiconductor process edges from `is_a` to `part_of`, moved `tungsten_film`/`molybdenum_film` inputs to `thin_film_deposition_process`, and added a frontend expand/collapse control so `wafer_manufacturing` can be viewed as a collapsible process group instead of a super-hub.
- **Compound node experiment**: Implemented Cytoscape compound nodes for `wafer_manufacturing` and its `part_of` subprocesses. Materials are now connected to specific subprocesses (e.g., `silicon_wafer -> lithography_process`, `tungsten_film -> thin_film_deposition_process`); expanding the parent forms a visual container, while collapsing falls back to the flat dagre layout.
- **Semiconductor wafer manufacturing flow refactor**: Replaced direct material flows into specific cleaning subprocesses with a single `cleaning_process` node in the main flow. Derived specific cleaning steps (`initial_wafer_cleaning`, `pre_lithography_wafer_cleaning`, `post_etch_residue_cleaning`, `post_cmp_cleaning`, `pre_diffusion_cleaning`, `pre_deposition_cleaning`) are linked to `cleaning_process` via `is_a` ontology edges. Removed intermediate `diffusion_ready_wafer`/`deposition_ready_wafer` states; cleaned up the main silicon_wafer → wafer flow.
- **Frontend nested compound expansion fix**: Updated `GraphCanvas.tsx` double-click handler to resolve the innermost expandable `process-group` under the cursor using rendered bounding-box hit testing, instead of always toggling the outermost compound parent.
- **Compound-group context-menu toggle**: Added "展开组 / 收起组" menu item to `NodeContextMenu.tsx` for selected compound group nodes; exposed `GraphCanvasRef.isCompoundGroupNode()` to determine group membership from current `part_of` edges, and wired the toggle to `useIndustrialGraph.toggleProcessParent()` in `App.tsx`. The menu item is placed at the top of the node context menu, separated by a divider from the "显示..." neighbor actions, avoiding reliance on double-click and reducing accidental toggles.
- **Box selection + multi-node context menu**: Changed `GraphCanvas` so left-drag on the canvas performs box selection of nodes only (`userPanningEnabled: false`, `boxSelectionEnabled: true`, `selectionType: "additive"`, edges marked `selectable: false`); Ctrl+left-drag and middle-drag still pan. Because Cytoscape's built-in wheel zoom requires `userPanningEnabled: true`, added a custom `wheel` event handler on the canvas container that zooms toward the cursor while respecting `minZoom`/`maxZoom`. Added `MultiNodeContextMenu.tsx` for when two or more nodes are selected, with an "自动排列" action that runs a localized force simulation (repulsion + weak anchor spring) on the selected nodes and animates them to new positions without moving the camera or unselected nodes. Exposed `getSelectedNodeIds` and `clearNodeSelection` on `GraphCanvasRef`.
- **Draggable/collapsible top toolbar + zoom sensitivity slider**: Created `frontend/src/components/toolbar/CanvasToolbar.tsx`, `ZoomSensitivitySlider.tsx`, and kept `GraphToolbar.tsx`/`ViewToolbar.tsx` as composable pieces. The new toolbar floats over the canvas, can be dragged by its grip handle, and collapsed to a small button; view buttons, zoom slider, and (commented-out) graph tools are arranged in a single row by default. Added `wheelSensitivity` state to `useIndustrialGraph` (default `0.1`, displayed as `1.0`) and wired it to `GraphCanvas` so the slider adjusts滚轮 zoom speed in real time; the slider maps display values (`0.1`–`3.0`, left step `0.1`, right step `0.2`) to internal factors multiplied by `0.1`, so `1.0` equals the standard speed. Commented out "重排" and "连线" buttons with explanatory notes about preserving user layout and avoiding accidental interactions.
- **Focus/Reveal mode for industrial graph**: Added a generic focus mode that lets users select one or more seed nodes, hides everything else, and progressively reveals upstream/downstream neighbors layer by layer. Implemented `FocusState`/`FocusStep` types, `useIndustrialGraph` focus actions, `GraphCanvas` imperative focus API and filter integration, context-menu entries for single and multi-node selection, a floating `FocusControlPanel`, and view serialization support so focused views can be saved and restored. Compound parents remain visible when any child is visible and render collapsed by default. Later refined `bfsReveal` to use explicit `connectedEdges` direction filtering and to traverse hidden edges during reveal; auto-expand any process group whose children become visible; add a complementary `HideState` with right-click "隐藏此节点 / 隐藏选中节点" and a floating `HideControlPanel`; and add `revealInternal` to display `part_of` children of a focused group parent.
- **Wafer cleaning process data refactor**: Removed the generic `cleaned_wafer` node. Changed relationships between specific cleaning steps (`initial_wafer_cleaning`, `pre_lithography_wafer_cleaning`, `post_etch_residue_cleaning`, `post_cmp_cleaning`, `pre_diffusion_cleaning`, `pre_deposition_cleaning`) and `wafer_cleaning_process` from `part_of` to `is_a`. Introduced differentiated intermediate wafer states (`initial_cleaned_wafer`, `lithography_ready_wafer`, `etch_cleaned_wafer`, `cmp_cleaned_wafer`, `diffusion_ready_wafer`, `deposition_ready_wafer`) and rewired downstream process inputs accordingly. Updated `semiconductor_industry` mappings to remove `cleaned_wafer` and include the new state nodes. Backup stored at `data\backup\20260629_155506`.
- **Front-end diffusion path repair**: Corrected `pre_diffusion_cleaning` upstream: removed the incorrect `oxidized_wafer -> pre_diffusion_cleaning` link and added `etched_wafer -> pre_diffusion_cleaning`, so diffusion follows the lithography/etch sequence rather than branching directly from oxidation. The full silicon-to-thin-film-deposition path remains continuous via both diffusion and ion-implantation branches. Backup stored at `data\backup\20260629_161856`.
- **Flat lithography subprocess hierarchy for focus reveal**: Removed `part_of` ontology edges from `photoresist_coating_process`, `exposure_process`, and `development_process` into `lithography_process`. These subprocesses are now independent process nodes connected only by industrial-flow edges (`lithography_ready_wafer -> photoresist_coating_process -> photoresist_coated_wafer -> ... -> lithography_process`). This eliminates the nested compound-group expansion that previously pulled the entire `wafer_manufacturing` group into view when revealing the downstream of `lithography_ready_wafer`. Backup stored at `data\backup\20260629_162931`.
- **Etch-cleaning diffusion path fix**: Moved the diffusion-branch input from `etched_wafer` to `etch_cleaned_wafer`: deleted `etched_wafer -> pre_diffusion_cleaning` and added `etch_cleaned_wafer -> pre_diffusion_cleaning`. This makes the sequence `etched_wafer -> photoresist_stripping_process -> photoresist_stripped_wafer -> post_etch_residue_cleaning -> etch_cleaned_wafer -> pre_diffusion_cleaning -> diffusion_ready_wafer -> diffusion_process`, which correctly requires post-etch cleaning before diffusion instead of jumping straight from the just-etched wafer. Backup stored at `data\backup\20260629_164906`.
- **Strict etch post-treatment sequence**: Removed the shortcut `etched_wafer -> post_etch_residue_cleaning`. `etched_wafer` now has a single downstream path through `photoresist_stripping_process`; cleaning and the subsequent ion-implantation / diffusion branches all start from `etch_cleaned_wafer`. Backup stored at `data\backup\20260629_165828`.
- **Metrology inspection output node**: Fixed the broken downstream of `metrology_inspection` by creating a `metrology_data` data-asset node and adding `metrology_inspection -> metrology_data` (`process_output`). `annealed_wafer` still feeds both `pre_deposition_cleaning` (thin-film continuation) and `metrology_inspection` (parallel inspection), but the inspection branch now terminates in a data node instead of a dead end. Added `metrology_data` to the `semiconductor_industry` mappings. Backup stored at `data\backup\20260629_170949`. Note: initial evidence fields used `source`/`note` keys; corrected to `source_title`/`quote` to match the `Evidence` schema and avoid 500 errors on node/mapping reads.
- **CMP-to-lithography loop normalization**: Replaced the shortcut `cmp_cleaned_wafer -> photoresist_coating_process` with `cmp_cleaned_wafer -> lithography_ready_wafer`. This makes the BEOL metal-layer loop (`lithography_ready_wafer -> photoresist_coating_process -> ... -> CMP -> post_cmp_cleaning -> cmp_cleaned_wafer -> lithography_ready_wafer`) explicit and keeps `photoresist_coating_process` with a single upstream state. Backup stored at `data\backup\20260629_173424`.
- **Saved view version chains**: Redesigned saved views to support versioning per view. Each `SavedView` now stores `base` (version-chain root UUID), `viewVersion` (incrementing revision number), and `id` (unique UUID of that revision). Saving from a loaded view inherits the same `base` and bumps `viewVersion`; saving from scratch creates a new `base` at v1. Import deduplicates by `id`, groups by `base`, and sorts by `viewVersion` then `created_at`. Old v1 views are migrated on load: missing `base` falls back to the view's `id`, missing `viewVersion` becomes 1. The view manager now groups entries by `base` with expandable version lists showing `vN`, short UUID, and timestamp. File format version remains `version` on `SavedView`/`SavedViewFile` and was bumped to 2.
- **Chip design / chip relationship cleanup**: Merged `ic_design` (Integrated Circuit Design) into `chip_design` via an `ontology/alias_of` edge and updated `chip_design` aliases to include `集成电路设计` and `IC设计`. Removed the incorrect `fabless` alias `芯片设计` to avoid naming conflicts. Deleted three semantically wrong industrial-flow edges: `chip_design --[process_output]--> chip` (design does not produce physical chips), `ip_core --[structural_composition]--> chip` (IP cores are design inputs, not physical components), and `wafer --[structural_composition]--> chip` (wafers are manufacturing intermediates, not chip components). Preserved the correct flow `chip_design --[information_input]--> wafer_manufacturing --[process_output]--> chip --[material_input]--> chip_packaging_and_testing`. Backup stored at `data\backups\neo4j_backup_20260630_061005.json`.
- **Chip packaging and testing process group**: Restructured `chip_packaging_and_testing` from a single process into an expandable process group with five `part_of` subprocesses: `wafer_dicing`, `die_bonding`, `wire_bonding`, `chip_molding`, and `chip_testing`. Added four intermediate state nodes (`die_attached_substrate`, `wire_bonded_package`, `molded_chip`, `tested_chip`) to model the detailed backend flow. The complete route is now `cmp_cleaned_wafer --[material_input]--> wafer_dicing --[process_output]--> chip --[material_input]--> die_bonding --[process_output]--> die_attached_substrate --[material_input]--> wire_bonding --[process_output]--> wire_bonded_package --[material_input]--> chip_molding --[process_output]--> molded_chip --[material_input]--> chip_testing --[process_output]--> tested_chip --[material_input]--> electronics_system_integration`. Removed obsolete edges: `chip --[material_input]--> chip_packaging_and_testing`, `chip_packaging_and_testing --[material_input]--> electronics_system_integration`, `packaging_substrate --[structural_composition]--> chip`, `osat --[capability_enablement]--> chip`, and `wafer_manufacturing --[process_output]--> chip` (now routed through dicing). `cmp_cleaned_wafer` still loops back to `pre_lithography_wafer_cleaning` for multi-layer iteration, while also exiting into the packaging group. Backup stored at `data\backups\neo4j_backup_20260630_063213.json`.
- **Fix: show upstream/downstream for process groups**: `GraphCanvas.showNeighbors` previously treated all edge types (including `ontology/part_of`) as upstream/downstream, so right-clicking a process group parent like `chip_packaging_and_testing` tried to pull its subprocesses in as "neighbors." Because those subprocesses are `part_of` children, adding them without updating `expandedProcessParents` caused `applyFilters` to immediately hide them, making the action appear to do nothing. Fixed by filtering `showNeighbors` to `industrial_flow` edges only. Also added a short camera fit animation to the newly revealed nodes so the result is always visible.
- **Return-to-full-graph preserves layout**: The "返回全图" button now saves the current node positions and camera before clearing the subgraph selection, then re-initializes the canvas with the full graph while restoring those positions. Nodes that exist in the full graph but were not in the previous view are placed in a circle around the center of the preserved layout instead of stacking at the default position, so users can return to the full graph without losing their current arrangement.
- **Cross-device view scaling**: Added `containerSize` to `IndustrialViewState`/`CompanyViewState` and `getContainerSize()` to the three canvas refs (`GraphCanvas`, `CompanyNetworkCanvas`, `ExplorationCanvas`). When a saved view is applied, `nodePositions` and `camera.pan` are scaled by `min(currentWidth / savedWidth, currentHeight / savedHeight)` to preserve aspect ratio across different screen resolutions/DPIs. This reduces layout distortion when importing views created on another machine, especially for expanded compound groups.
- **Multi-node alignment and distribution layout tools**: Added layout actions for multiple selected nodes in the industrial graph. The `MultiNodeContextMenu` now offers four new actions: horizontal align, vertical align, horizontal distribute, and vertical distribute. `GraphCanvas` exposes `alignSelectedNodes(axis)` and `distributeSelectedNodes(axis)`, which animate selected nodes to new positions while keeping the camera unchanged. Alignment requires at least 2 nodes; distribution requires at least 3.
- **Preserve saved view layout on restore**: Fixed a layout corruption issue when loading a saved view that contained expanded process groups. `GraphCanvas` now skips the initial `runHybridLayout` when `restoredPositions` is present and applies the saved node positions directly, preventing the temporary radial layout of compound groups from overwriting user-positioned nodes. `npx tsc --noEmit` and `npm run build` pass.
- **Lithography process hierarchy restoration**: Restored `part_of` ontology edges from `photoresist_coating_process`, `exposure_process`, and `development_process` to `lithography_process`, reversing the previous flat hierarchy. Moved material/equipment inputs to the subprocesses that actually consume them: `photoresist`/`duv_photoresist`/`euv_photoresist` → `photoresist_coating_process`; `lithography_machine` → `exposure_process`; `track_coater_developer` → both `photoresist_coating_process` and `development_process`. Removed the semantically backwards `developed_wafer -> lithography_process` edge and set `lithography_process` to take `lithography_ready_wafer` as input and output `patterned_wafer`. Deleted the redundant `developed_wafer` node and its `semiconductor_industry` mapping; `development_process` now outputs `patterned_wafer` directly. No backup was stored per user request.
- **Edge namespace fix**: The newly created `part_of` edges were missing the `edge_namespace='ontology'` property, causing `_edge_from_record` to default them to `industrial_flow` and fail Pydantic validation when `get_neighbors` was called on `lithography_process` (HTTP 500). Fixed by setting `edge_namespace='ontology'` on all ontology edges and `edge_namespace='industrial_flow'` on all industrial-flow edges that lacked the property. Verified `/api/v1/query/neighbors/lithography_process` now returns 200.
- **Edge namespace robustness**: Hardened `backend/app/services/neo4j_storage.py` `_edge_from_record` to derive the Pydantic edge subclass from the canonical Neo4j relationship type (`:INDUSTRIAL_FLOW` vs `:ONTOLOGY`) instead of the redundant `edge_namespace` property. Added new ontology rule `R25` and a registered db checker `EdgeNamespaceConsistencyChecker` in `backend/app/services/db_checkers.py` to detect missing or mismatched `edge_namespace` properties with auto-fix support. Updated `backend/tests/test_db_checkers.py` to include the new checker.
- **Compound-group expansion layout stability**: Fixed `frontend/src/components/GraphCanvas.tsx` so expanding a process group only lays out the *newly* expanded group, not all currently expanded groups. Added diff tracking via `prevExpandedProcessParentsRef` and propagated `parentsToLayout` through `syncCompoundParents` / `runHybridLayout`. Updated `layoutExpandedCompound` to preserve existing child positions when children are already spread out (spread > 20px), centering the parent on the children's bounding box instead of forcing a radial layout. This prevents expanding `lithography_process` inside `wafer_manufacturing` from re-arranging the outer group or disturbing the global graph. Frontend production build passes.
- **QuickNodeForm overflow fixes**: Fixed input overflow in `frontend/src/components/QuickNodeForm.tsx` by adding `min-w-0` to all flex inputs/select so they shrink correctly inside the narrow `w-80` popup, shortened button labels and allowed them to wrap, and added `max-w-[calc(100vw-2rem)]` plus viewport-edge clamping in `frontend/src/App.tsx` so the quick-create popup stays on screen when triggered near the right/bottom edge. Frontend production build passes.
- **Canvas view-state undo**: Added an undo stack for industrial/company canvas view state. `frontend/src/hooks/useViewStateHistory.ts` tracks snapshots of node positions, camera, expanded process groups, focus/hide state, and node/edge filters. View-changing actions (node drag, auto-arrange, zoom/pan, reset view, process-group expand/collapse, focus/hide, filter resets) push the previous snapshot before applying the change; the toolbar's "撤销" button or `Ctrl+Z` pops the snapshot and restores it via the existing `loadView` path. To avoid polluting the stack, node drags are only recorded when the node actually moves, and camera changes are debounced. The stack is capped at 20 entries and cleared on explicit view load/save or workspace switch.
- **Storage chip packaging flow cleanup**: Removed incorrect `process_output` edges from `chip_packaging_and_testing` to specific storage chips (`three_d_nand_flash`, `lpddr5`, `ddr5_dram_chip`) per the rule that packaging/testing only outputs `tested_chip` (a kind of `chip`), and specific storage chips should be related via `is_a` hierarchy. Replaced the backwards `memory_chip --[structural_composition]--> hbm` edge with `hbm is_a memory_chip`. Verified `reverse_industrial_flow` and `ontology_cycle` checkers report zero issues after the change. Backup stored at `data\backups\neo4j_backup_20260701_001433.json`.
- **Electronics system integration flow fix**: Corrected `electronics_system_integration` relationships. It had no upstream inputs and its seven downstream edges were wrongly typed as `material_input` (pointing from the process to the products). Changed them to `process_output`: `automotive_electronics`, `consumer_electronics`, `industrial_electronics`, `new_energy_vehicle`, `personal_computer`, `server`, `smartphone`. Changed the entity_type of all seven downstream targets from `software` to `system`. Restructured the upstream so that `chip`, `chip_resistor`, and `ceramic_capacitor` feed into `printed_circuit_board_fabrication` as `material_input`; `printed_circuit_board_fabrication` outputs `pcb_board`; and `pcb_board` feeds into `electronics_system_integration`. Removed the direct `chip -> electronics_system_integration` edge. This gives a clean `Input → Process → Output` chain: components → PCB manufacturing → populated PCB → system integration → electronic systems. Verified `reverse_industrial_flow` and `ontology_cycle` remain at zero issues. Backup stored at `data\backups\neo4j_backup_20260701_004107.json`.
- **Chip design neighborhood cleanup**: Restructured relationships around `chip_design` to separate concrete industrial flow from abstract business models. Removed incorrect `industrial_flow` edges: `eda_software -> fabless`, `eda_software -> idm`, `fabless -> chip_design`, `idm -> chip_design`, `idm -> wafer_manufacturing`. Preserved the concrete flow: `eda_software --capability_enablement--> chip_design --information_input--> wafer_manufacturing`, plus `ip_core --information_input--> chip_design` and `foundry --service_provision--> wafer_manufacturing`. Reconnected `fabless` and `idm` as business-model concepts via `ontology/related_term` edges: `fabless` relates to `chip_design` and `foundry`; `idm` relates to `chip_design` and `wafer_manufacturing`. Added descriptions to `chip_design`, `eda_software`, `fabless`, and `idm`. Verified `reverse_industrial_flow`, `ontology_cycle`, and `edge_namespace_consistency` are all zero issues. Backup stored at `data\backups\neo4j_backup_20260701_005149.json`.
- **Save menu recent-save hint**: Updated `frontend/src/components/ViewToolbar.tsx` so the save dropdown shows the context of the current save. If a view is already loaded, it displays the loaded view name and version (e.g., "当前已载入：MyView v3 → 保存为 v4"). If no view is loaded but saved views exist, it shows the most recent save name/version and notes that a new version chain will be created. If no views exist, it shows "将创建第一个视图". Frontend `npm run build` passes.
- **Toolbar undo placement/label**: Moved the undo button out of `ViewToolbar` and placed it directly in `CanvasToolbar` between `GraphToolbar` and `ZoomSensitivitySlider`, separated by dividers. Added a `showUndo` prop to `ViewToolbar` so it can be hidden when rendered inside `CanvasToolbar`. Renamed the button text from "撤销" to "恢复上个视图" and updated its tooltip to clarify it restores the previous view state (Ctrl+Z). Frontend `npm run build` passes.
- **Smart view-state undo**: Refactored `App.tsx` `handleUndo` to avoid a full canvas re-initialization when the only differences between the current state and the previous history entry are camera and/or node positions. For these common cases, it directly calls `setCamera` / `setNodePositions` on the active canvas ref, providing a smooth undo without flash. When filters, focus, hide, selection, process-group expansion, or other non-layout state changed, it still falls back to the full snapshot restore. Added helper functions `scaleCameraAndPositions`, `industrialContentEqual`, and `companyContentEqual`. Later hardened the comparison functions to normalize optional `focus`/`hide` fields and compare IDs/filter arrays in an order-independent way, reducing false negatives that could force a full snapshot restore. Frontend `npm run build` passes.
- **Company exposure auto-activation fix**: `process_business_batch` now only auto-activates `PENDING` exposures that carry evidence (`evidence IS NOT NULL AND evidence::text != '[]'`). This prevents the `ACTIVE exposure must have evidence` Pydantic validation error that caused `POST /api/v1/companies/by-nodes` to return 500. Existing bad rows were cleaned, and `tests/test_business_batches.py` was updated to supply evidence on the test exposure and run all business-batch scenarios inside a single `httpx.AsyncClient` lifespan to avoid pytest-asyncio loop-boundary flakiness.
- **Duplicate company cleanup + name-zh uniqueness**: Found and merged 12 groups of duplicate companies by `name_zh` (including 江丰电子 and 精测电子). For each group, kept the richer record (stock codes, description, founded year, etc.), merged aliases/stock codes, moved unique exposures to the kept company, and deleted the duplicates. Backup at `data\backup\duplicate_companies_merge_backup_20260701_220839.json`. Added `company_storage.get_company_by_name_zh()` and a uniqueness check in `create_company`; `POST /api/v1/companies` now returns `409 公司名称已存在` if the Chinese name already exists. Updated tests to use unique `name_zh` per run and added a storage-level test for duplicate-name rejection.
- **Floating company filter panel**: Replaced the right-panel "node-companies" / "multi-node-companies" flow with a persistent floating `CompanyFilterPanel`. Right-clicking a node or multi-selection and choosing "查看关联公司" now adds/updates the selected node(s) in the filter list; the list stays open until explicitly closed or cleared. Users can check/uncheck nodes to control which nodes contribute to the union of exposed companies, remove individual nodes, or clear all. The panel does not close on outside clicks and does not interfere with node selection or other canvas interactions. `useIndustrialGraph` exposes `companyFilter`, `showCompanyFilter`, `toggleCompanyFilterNode`, `removeCompanyFilterNode`, `closeCompanyFilter`, and `clearCompanyFilter`.
- **Biopharma representative company batch (Task A)**: Created and submitted `batch_biopharma_companies_001` via `arachne_cli.py business-batch`. Registered 8 representative CXO/innovative pharma companies (药明康德, 药明生物, 凯莱英, 泰格医药, 恒瑞医药, 百济神州, 昭衍新药, 康龙化成) with 2024 annual-report fundamentals and 44 `CompanyNodeExposure` records linking them to existing biopharma skeleton nodes (CRO/CDMO service nodes, process nodes, product/material nodes). Batch file: `data/stock_batches/batch_biopharma_companies_001.json`.
- **Graph Reasoning Kernel V0.2 backend**: Implemented `backend/app/reasoning/` module with object query (`POST /api/v1/reasoning/query`), association (`POST /api/v1/reasoning/execute` `task_type=association`), and impact propagation (`task_type=impact_propagation`) tasks. Returns temporary reasoning graphs, paths, node/edge scores, evidence chains, feature tables, and diagnostics. Fixed the `GraphEdge` Annotated-Union `isinstance` issue in `backend/app/reasoning/evidence.py` that caused impact propagation to fail with `TypeError: Subscripted generics cannot be used with class and instance checks`.
- **Industry selection during node creation**: Added the ability to choose one or more industries while creating a node, instead of creating the node first and then adding industry mappings separately. Backend: added `IndustryNodeAssociation` schema, extended `IndustrialNodeCreate` and `IndustrialNodeQuickCreate` with an `industry_ids` field, and updated `graph_service.create_node` / `quick_create_node` to create `industry_node_mappings` after the Neo4j node is created (idempotent, silent skip on missing industry/PostgreSQL). Frontend: added reusable `IndustryMultiSelect` component and integrated it into `QuickNodeForm` and `NodeForm` (create mode only). API response shape remains `IndustrialNode` for backward compatibility. Added integration tests in `backend/tests/test_industry_company_routers.py`. Verified end-to-end via API on port 16060; backend was restarted to pick up the changes. Frontend `npm run build` passes.
- **Context-menu connect mode**: Added a "连线" item to the node context menu. Selecting it enters connect mode with the chosen node as the source and immediately draws a dashed cyan dynamic edge from the source node to the mouse cursor. The line is updated on mouse move and on every Cytoscape render (pan/zoom/layout), hidden when the pointer leaves the page, and restored when it returns. Pressing ESC exits connect mode entirely. Clicking another node sets it as the target and opens the existing `ConnectEdgePanel` (quick edge form) at the click position, just like the toolbar connect flow. Implemented in `frontend/src/components/NodeContextMenu.tsx`, `frontend/src/components/GraphCanvas.tsx`, and `frontend/src/App.tsx`. Removed the completed TODO from `docs/prompts.txt`. Frontend `npm run build` passes.
- **PROV statement storage backend**: Implemented type-level PROV assertion storage in PostgreSQL. Added `prov_statements` table (created by `init_postgres_tables`), `backend/app/models/prov_schema.py`, `backend/app/services/prov_storage.py`, `backend/app/routers/prov.py` mounted at `/api/v1/prov`, and `backend/tests/test_prov_storage.py`. Supports `used`, `wasGeneratedBy`, `wasDerivedFrom`, and other PROV relations attached to industrial nodes, independent of the Neo4j graph. Design recorded in `docs/prov_overlay_design.md`.
- **PROV frontend integration**: Added `NodeProvPanel` and `node-prov` right-panel; node detail now shows a compact PROV section when statements exist; node context menu shows "查看 PROV ({count})" only for nodes with PROV statements. Wired to `/api/v1/prov/nodes/{node_id}/statements`. Frontend production build passes.
- **Chip material PROV sample**: Created 12 type-level PROV statements for the chip manufacturing chain (`silicon_wafer` → `wafer` → `wafer_dicing` → `chip_die` → `chip_molding` → `molded_chip` → `chip_testing` → `tested_chip`, plus `lithography_process` inputs). Verified via API and frontend build.

---

## 5. Pending Work

### Phase 2 — Factual Graph Frontend
The Factual Graph **backend** (schema, storage, router, Neo4j sync) is implemented. Remaining work:
- Frontend Person CRUD pages/components (`PersonList`, `PersonForm`, `PersonDetail`)
- Frontend relation visualization for factual relations
- Batch import UI/API for factual relations (annual reports, Tianyancha data)

### Phase 3 — Frontend Views
Current frontend is a single-page dashboard with sidebars and detail panels, not dedicated routes/pages.

Implemented:
- `IndustrySidebar`: list with search/type/status filters
- `IndustryDetail`: shows mapped nodes + can load subgraph
- `CompanySidebar`: list with type/status/search filters
- `CompanyDetail`: shows exposures
- `ExplorationCanvas`: manual cross-domain exploration UI

Missing or stubbed:
- **Dedicated Industry/Company pages** (currently only sidebars/panels)
- **Country filter** and **node filter** in company list
- **Temporary subgraph inside CompanyDetail panel**
- **Factual relations inside CompanyDetail panel**
- **Person List/Detail Page** — no Person components exist
- **Add exposure workflow** in `CompanyDetail` (`onAddExposure` is an `alert` stub)
- **Cross-domain exploration page** currently uses `company_exploration.py` endpoints (`/companies/{id}/exploration-graph`, `/companies/nodes/{id}/connected-companies`); the newer `/api/v1/explore/*` endpoints are not yet wired to the UI

### Infrastructure
- [x] **Install/start PostgreSQL locally** — binary in `postgresql/pgsql/`, started on port 5433, tables initialized via `init_postgres_tables()`
- [ ] **Run full test suite** — PostgreSQL is now available; run PG-dependent tests to verify

### Data / Batch Debt
Historical batch construction logs list these as future work; none are implemented:
- Inferred inter-company industrial relations for batches 002–004
- Industry filter/views for batches 002–004
- Additional exposure relationships (e.g., Shenzhen Energy sludge/waste-water treatment)
- Periodic financial-data refresh mechanism for company revenue / market cap
- Remaining company batches beyond Batch 001

---

## 6. Important Constraints & Notes

### Neo4j Compatibility
- Neo4j **does NOT support nested Map properties**. Evidence lists must be serialized as JSON strings before storage.
- `_evidence_to_db()` in `neo4j_storage.py` handles this automatically.
- `_to_datetime()` converts `neo4j.time.DateTime` → Python `datetime`.

### PostgreSQL
- Code is fully written but **not locally installed**.
- When PostgreSQL is unavailable, `get_postgres_pool()` returns `None`; storage functions return empty lists / `None` gracefully.
- Table schemas use `TEXT[]` for arrays, `JSONB` for evidence, `TIMESTAMPTZ` for timestamps.
- `init_postgres_tables()` now creates 7 tables: `industries`, `industry_node_mappings`, `companies`, `company_node_exposures`, `computation_jobs`, `persons`, `factual_relations`.

### Schema Patterns
- All IDs use snake_case regex: `^[a-z][a-z0-9_]*$`, min 3 chars, max 64.
- `RecordStatus`: `ACTIVE`, `PENDING`, `REJECTED`, `ARCHIVED`
- `Confidence`: `HIGH`, `MEDIUM`, `LOW`
- `EntityType` now includes `process` for manufacturing/process nodes.
- `IndustrialFlowType` now includes `process_output` for process → output relationships.
- UUID fields now auto-generate; callers do not need to supply them.

### Git Hygiene
- Do NOT run `git commit`, `git push`, `git reset`, `git rebase` without explicit user confirmation.
- LF/CRLF warnings are normal on Windows; Git will handle conversion.

---

## 7. Design Documents

- `docs/view_design_v2.md` — Three-layer view pyramid architecture (Industry → Industrial → Company) (retired)
- `docs/think-01.md`, `docs/think-02.md` — Historical design thinking
- `docs/prompts.txt` — Prompt history
- `docs/ui_architecture_refactor_2026-05-24.md` — Current UI architecture and future extension directions

---

## 8. Agent Skills

项目级 agent skills 位于根目录 `skills/` 下，提供针对本系统的程序化操作指引：

- `skills/arachne-graph/` — 本体设计技能：判断候选词是否应登记为产业节点、合并为别名或被拒绝。
- `skills/arachne-api/` — CLI/API 操作技能：优先通过 `cli/arachne_cli.py` 批量注册节点/关系/公司/行业/映射/暴露，管理行业和公司，以及查询图谱；CLI 未覆盖的场景可直接调用底层 API。

通过对话构造或维护图谱时，通常两个技能协同使用：`arachne-graph` 负责本体决策，`arachne-api` 负责通过 CLI 执行具体操作。

---

*Last updated: 2026-07-01 08:15 CST*
