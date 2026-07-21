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
| Node metadata | PostgreSQL | `industrial_nodes` |
| Computation jobs | PostgreSQL | `computation_jobs` (async/batch job tracking) |

### 3.2 Backend Directory Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI entry, registers all routers
│   ├── config.py                  # Settings (Neo4j + PostgreSQL URLs)
│   ├── database.py                # Neo4j async driver
│   ├── database_postgres.py       # asyncpg pool + table init (8 tables)
│   ├── models/
│   │   ├── core.py                # Engine-agnostic graph models (GraphNode, GraphEdge, GraphStats)
│   │   ├── schemas.py             # Core graph models (Node, Edge, Evidence, RecordStatus)
│   │   ├── industry_schema.py     # Industry, IndustryNodeMapping, IndustryType
│   │   ├── company_schema.py      # Company, CompanyNodeExposure, CompanyActivityType, CompanyType, BusinessRegistrationBatch
│   │   └── factual_graph_schema.py # Person, FactualRelation, three relation types
│   ├── engines/
│   │   ├── base.py                # GraphEngine abstract base class
│   │   └── legacy/
│   │       ├── engine.py          # LegacyEngine implementation (Neo4j topology + PG metadata)
│   │       ├── storage.py         # Neo4j/PG storage helpers migrated from neo4j_storage.py
│   │       └── schemas.py         # Legacy engine schemas (currently re-export of app.models.schemas)
│   ├── services/
│   │   ├── engine_registry.py     # Engine registration and get_engine() resolver
│   │   ├── neo4j_storage.py       # Compatibility shim re-exporting engines.legacy.storage
│   │   ├── node_storage.py        # PostgreSQL CRUD for IndustrialNode metadata
│   │   ├── graph_service.py       # Thin orchestration layer: delegates node/edge/query ops to the active engine
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
- `database_postgres.py`: asyncpg pool + `init_postgres_tables()` creates **8 tables**
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
- **Pluggable graph-engine refactor (legacy-only)**: Introduced an engine subsystem so the Neo4j-backed implementation can be replaced without changing routers or core models. Added `app/models/core.py` (engine-agnostic models), `app/engines/base.py` (`GraphEngine` ABC), `app/services/engine_registry.py`, and `app/engines/legacy/` (`engine.py`, `storage.py`, `schemas.py`). Migrated the original `neo4j_storage.py` logic into `engines/legacy/storage.py` and turned `graph_service.py` into a thin pass-through layer. `app/services/neo4j_storage.py` remains as a compatibility shim. Routers (`nodes.py`, `edges.py`, `query.py`) now accept an optional `?engine=` query parameter and forward it to `graph_service`; omitting it keeps legacy behavior. `LegacyEngine` is registered in `app.main:lifespan`. Added `UnknownEngineError` and a 400 exception handler for invalid engine names. All 50 backend tests pass and the frontend production build succeeds.
- **Engine subsystem schema/policy cleanup (legacy-only)**: Completed the separation between core and legacy schemas that was deferred during the initial refactor. `app/models/schemas.py` is now a backward-compatibility shim that re-exports `app/models/core.py` primitives (`Confidence`, `Evidence`, `NodeStatus`, `RecordStatus`, `GraphNode`, etc.) and `app/engines/legacy/schemas.py` node/edge/input models (`EntityType`, `IndustrialFlowType`, `OntologyType`, `IndustrialNode`, `IndustrialFlowEdge`, `OntologyEdge`, `GraphEdge`, `GraphRegistrationBatch`, etc.). `app/engines/legacy/__init__.py` no longer eagerly imports `LegacyEngine`, breaking the circular import created by the shim. Moved legacy-specific policies out of core services: `app/services/derived_from_policy.py` and the checker implementations from `app/services/db_checkers.py` now live in `app/engines/legacy/policies/`, with the original paths kept as compatibility shims. `app/services/ontology_rules.py` remains in core as the design-rule registry. Updated all internal imports (routers, services, reasoning, tests) to reference `app/models/core.py` for primitives and `app/engines/legacy/schemas.py` for legacy types. Verified 50 backend tests pass, backend imports successfully, and frontend production build succeeds.
- **Arachne-flow engine (first implementation)**: Implemented the arachne-flow engine under `backend/app/engines/arachne_flow/`. Added schemas (`ResourceType`, `ActionType`, `InputRole`, `OutputRole`, `FlowDocument`, `ParsedFlow`), a YAML parser that validates triple patterns and checks single-connectivity + DAG constraints, and a compiler that writes flows into Neo4j using `:ArachneFlowNode`/`:ArachneFlowResource`/`:ArachneFlowAction`/`:ArachneFlowMethod` labels and `:ARACHNE_FLOW` relationships. `ArachneFlowEngine` implements the `GraphEngine` interface as a read-only engine; write operations raise `ReadOnlyEngineError` (returned as HTTP 405). Added `app/database_flow.py` for an optional second Neo4j instance (defaults to the main instance if `NEO4J_FLOW_URI` is not set), registered the engine in `app.main:lifespan`, added the `arachne_flow_files` state table to PostgreSQL, and added `ReadOnlyEngineError` exception handling. Added `backend/tests/test_arachne_flow.py` with parser, compiler, and engine tests.
- **Fixed arachne-flow YAML generator**: Rewrote `temp/generate_arachne_flow.py` so the generated `data/flows/semiconductor/*.yaml` files strictly follow `docs/design_v4.txt`. Legacy process/usage nodes are now emitted as METHOD nodes, each METHOD occurrence gets a unique ACTION node with a `[ACTION, ref, METHOD]` triple, and process nodes used as resource inputs are split into a METHOD plus a synthetic output RESOURCE so ACTION and RESOURCE remain disjoint. All 14 regenerated files pass the parser/validator (single connected graph, acyclic, no dual-role nodes). Updated `data/flows/semiconductor/README.md` with the new generation rules. Full backend test suite now passes with 61 tests; backend restarts successfully and the frontend production build still passes.
- **Arachne-flow data loading + API + UI viewer**: Added `backend/scripts/load_arachne_flows.py` to parse and compile all YAML files under `data/flows/semiconductor/` into Neo4j, tracking status in the `arachne_flow_files` PostgreSQL table. Added `backend/app/routers/flows.py` with `GET /api/v1/flows` and `POST /api/v1/flows/{flow_id}/compile`. Fixed arachne-flow storage serialization of `neo4j.time.DateTime` and `clear_flow()` so shared resource/method nodes across flows are preserved. Fixed `GET /api/v1/query/subgraph/{node_id}` to return the generic `SubgraphResult` from `app.models.core`, allowing it to serve the arachne-flow engine (`?engine=arachne_flow`). On the frontend, added a "流程图" tab (`MainView.flow_graph`), `FlowGraphPage` component, flow-list sidebar, and a read-only canvas that renders the selected product flow's subgraph with distinct colors for RESOURCE / ACTION / METHOD nodes. Frontend types and `ENTITY_TYPE_COLORS`/`EDGE_NAMESPACE_STYLES` were extended to include arachne-flow entity types and edge namespace. `npm run build` passes; `pytest backend/tests` passes 61 tests. The flow viewer is functional at `http://localhost:3000` when the backend is running on port 16060 and `backend/scripts/load_arachne_flows.py` has been executed.
- **HBM advanced packaging Usage refactor**: Corrected the HBM advanced packaging flow so the generic `advanced_packaging` technology node stays abstract and is not overloaded with a hard-coded HBM-specific process sequence. Deleted the HBM-specific intermediate state nodes (`hbm_tsv_memory_wafer`, `hbm_bumped_die`, `hbm_stacked_die`, `hbm_integrated_module`) and removed their connecting process-chain edges (`memory_wafer -> tsv_interconnection`, `memory_die -> die_stacking`, `underfill_process -> usage_hbm_advanced_packaging`). The flow is now `memory_wafer --material_input--> usage_hbm_advanced_packaging --process_output--> hbm`, with `usage_hbm_advanced_packaging --adopts--> advanced_packaging`. The `advanced_packaging` subprocesses (`tsv_interconnection`, `bumping_process`, `die_stacking`, `silicon_interposer_integration`, `underfill_process`) remain as `part_of` components describing what advanced packaging is composed of, but no longer encode a fixed execution order. The generic `memory_wafer --material_input--> memory_die` link is preserved; the `memory_die -> die_stacking` shortcut is removed because it was an HBM-specific conflation of wafer-dicing and die-stacking. Also fixed two data-quality issues introduced by the manual Neo4j-only migration: (1) confidence/status values were written in lowercase (`high`/`active`) instead of the enum-required uppercase (`HIGH`/`ACTIVE`), causing `GET /api/v1/query/neighbors/hbm` to return HTTP 500; (2) evidence JSON used `source`/`description` keys instead of the schema-required `source_title`/`quote`, causing neighbor queries on `usage_hbm_advanced_packaging` to fail validation. Cleaned up the corresponding orphan `industrial_nodes` rows in PostgreSQL. Verified `reverse_industrial_flow` remains at 0; 50 backend tests pass.
- **Remove standalone `memory_die` node**: Since `memory_die` had no downstream industrial-flow edges and its semantics are already covered by the generic `chip_die` path (`memory_wafer is_a wafer -> wafer_dicing -> chip_die -> die_bonding -> ...`), it was an isolated dead-end node in the graph. Deleted `memory_die` and its only edge `memory_wafer -> memory_die` from both Neo4j and PostgreSQL. Verified 50 backend tests pass and `reverse_industrial_flow` remains at 0.
- **v2 architecture: node metadata moved to PostgreSQL**: All IndustrialNode metadata now lives in the industrial_nodes PostgreSQL table. Neo4j :IndustrialNode skeletons only store 
ode_id + label; relationships remain in Neo4j. Added ackend/app/services/node_storage.py and ackend/scripts/migrate_nodes_to_postgres.py. Refactored 
eo4j_storage.py, graph_service.py, db_checkers.py, 	est_data_cleanup.py, routers, and reasoning tasks to read node metadata from PG. Removed obsolete 
eo4j_storage._node_from_record and the Neo4j 
ode_name_zh index. All 48 backend tests pass.
- **HBM supply-chain enrichment + cross-graph expansion**: Completed `backend/tmp_enrich_hbm.py`. Created/activated upstream nodes (`advanced_packaging`, `memory_die`, `tsv`, `silicon_interposer`, `microbump`, `underfill`) and downstream nodes (`gpu`, `ai_accelerator`, `server`, `data_center`), plus the corresponding `INDUSTRIAL_FLOW` edges. Fixed the downstream activation bug where `neo4j_storage._node_from_record` downgraded `ACTIVE`/`HIGH` nodes without evidence back to `PENDING`/`MEDIUM` by adding evidence during activation. Deduplicated company names: `雅克科技` maps to existing `jacques_technology`; created `联瑞新材` (`lianruixin_material`) and `华海诚科` (`huahai_chengke`). Created 13 `CompanyNodeExposure` records linking `hbm`, `advanced_packaging`, `silicon_interposer`, `packaging_substrate`, `underfill`, and `memory_module` to relevant companies.
  - Decomposed `advanced_packaging` into a process group with 5 `part_of` subprocesses: `tsv_interconnection`, `die_stacking`, `silicon_interposer_integration`, `bumping_process`, `underfill_process`. Moved material/capability inputs from the aggregate `advanced_packaging` node down to the appropriate subprocesses (`memory_die -> die_stacking`, `memory_wafer -> tsv_interconnection`, `tsv -> tsv_interconnection`, `silicon_interposer/packaging_substrate -> silicon_interposer_integration`, `microbump -> bumping_process`, `underfill -> underfill_process`), and linked each subprocess back to `advanced_packaging` via `process_output`. Added `advanced_packaging is_a chip_packaging_and_testing`.
  - Wired `expand_ontology` into `cross_graph_context` (`backend/app/reasoning/tasks/cross_graph_context.py`) so the task can grow its seed set via `is_a`/`part_of`/`variant_of` before querying companies/industries.
  - Added `industrial_neighbor_depth` parameter to `cross_graph_context` (and `--neighbor-depth` in `cli/arachne_cli.py`) to also query companies/industries exposed to upstream/downstream industrial-flow neighbors of the seed nodes.
  - Added regression tests in `backend/tests/test_reasoning_tasks.py`.
  - Effect on `hbm`:
    - `association`: full connected upstream/downstream chain, including subprocesses under `advanced_packaging`.
    - `cross_graph_context` default: 3 companies (HBM producers).
    - `cross_graph_context --expand-ontology`: 13 companies (broader `memory_chip` ecosystem).
    - `cross_graph_context --neighbor-depth 1`: 13 companies (OSATs + GPU/AI accelerator makers).
    - `cross_graph_context --neighbor-depth 2`: 39 companies (full upstream materials + downstream compute).
  - All 48 backend tests pass; backend restarted on port 16060.
- **Topology-aware reasoning**: Ontology edges are handled according to their semantics rather than being mixed into supply-chain traversal. `alias_of` is **always** resolved to its downstream canonical node before reasoning. When `expand_ontology=True`, `is_a` and `variant_of` are expanded bidirectionally (parents and children), `part_of` is expanded from part to whole and conservatively from whole to direct parts. Ontology edges are never returned as flow paths. Applied to `association` and `bottleneck_detection`; `impact_propagation` still uses propagation profiles. Added `expand_ontology` parameter (CLI `--expand-ontology`, frontend toggle) and `metadata` to `ReasoningDiagnostics`. Also fixed a missing `is_test` parameter in `neo4j_storage.create_ontology_edge`.
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
- **pytest/async test-suite hardening**: `backend/app/database.py` and `backend/app/database_postgres.py` now track the event loop that created the shared Neo4j driver / asyncpg pool and automatically recreate them when the running loop changes or is closed. This fixes the pre-existing `Event loop is closed`, `pool is closed`, and `another operation is in progress` failures when running the full suite under `pytest-asyncio`. Converted all async test fixtures to `pytest_asyncio.fixture`, made non-IO fixtures synchronous, removed the stale `pg_pool` reference, replaced the strict float equality in `test_create_and_list_by_company` with an approximate check, and migrated `test_reasoning_tasks.py` from a deprecated custom `event_loop` fixture to `pytest.mark.asyncio(loop_scope="session")`. `pytest backend/tests` now passes (44 passed).
- **Focus/Reveal mode for industrial graph**: Added a generic focus mode that lets users select one or more seed nodes, hides everything else, and progressively reveals upstream/downstream neighbors layer by layer. Implemented `FocusState`/`FocusStep` types, `useIndustrialGraph` focus actions, `GraphCanvas` imperative focus API and filter integration, context-menu entries for single and multi-node selection, a floating `FocusControlPanel`, and view serialization support so focused views can be saved and restored. Compound parents remain visible when any child is visible and render collapsed by default. Later refined `bfsReveal` to use explicit `connectedEdges` direction filtering and to traverse hidden edges during reveal; auto-expand any process group whose children become visible; add a complementary `HideState` with right-click "隐藏此节点 / 隐藏选中节点" and a floating `HideControlPanel`; and add `revealInternal` to display `part_of` children of a focused group parent.
- **Reasoning visual graph layout fix**: The `ResultGraph` component in `frontend/src/pages/ReasoningPage.tsx` previously passed the `dagre` layout via the Cytoscape init `layout` option, which does not auto-execute; nodes appeared scattered/randomly. Now it explicitly calls `cy.layout({ name: "dagre", rankDir: "TB", ... }).run()` after setting node colors and fits the viewport on `layoutstop`. The visual graph now renders as a proper hierarchical layout.
- **Reasoning query scope cleanup**: The query scope dropdown in `ReasoningPage` exposed edge and claim scopes, but reasoning tasks only accept node-like sources and the backend does not implement the `claim` scope. Limited the dropdown to `industrial_node`, `factual_node`, and `industry`. The query input label/placeholder and the example-fill button adapt to the selected scope. `factual_node` now searches both persons and companies on the backend; the UI exposes an optional "事实节点类型" filter to narrow to person/company only. The separate `company` scope was removed from the dropdown since it is covered by `factual_node`.
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
- **Chip design neighborhood cleanup**: Restructured relationships around `chip_design` to separate concrete industrial flow from abstract business models. Removed incorrect `industrial_flow` edges: `eda_software -> fabless`, `eda_software -> idm`, `fabless -> chip_design`, `idm -> chip_design`, `idm -> wafer_manufacturing`. Preserved the concrete flow: `eda_software --capability_enablement--> chip_design --information_input--> wafer_manufacturing`, plus `ip_core --information_input--> chip_design` and `foundry --service_provision--> wafer_manufacturing`. Reconnected `fabless` and `idm` as business-model concepts via ontology edges to `chip_design`, `foundry`, and `wafer_manufacturing` (these placeholder edges are now deprecated; new modeling should use more specific relations). Added descriptions to `chip_design`, `eda_software`, `fabless`, and `idm`. Verified `reverse_industrial_flow`, `ontology_cycle`, and `edge_namespace_consistency` are all zero issues. Backup stored at `data\backups\neo4j_backup_20260701_005149.json`.
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
- **PROV statement storage backend (deprecated)**: Implemented type-level PROV assertion storage as JSON files under `data/prov_statements/{node_id}.prov.json`. Added `backend/app/models/prov_schema.py`, `backend/app/services/prov_storage.py`, `backend/app/routers/prov.py` mounted at `/api/v1/prov`, and `backend/tests/test_prov_storage.py`. The entire PROV overlay layer is now deprecated: `derived_from` is expressed directly as a graph edge, so there is no longer any PROV-to-graph or graph-to-PROV synchronization. The code remains in the repository for reference but is no longer part of the active workflow.
- **PROV frontend integration**: Added `NodeProvPanel` and `node-prov` right-panel; node detail now shows a compact PROV section when statements exist; node context menu shows "查看 PROV ({count})" only for nodes with PROV statements. Wired to `/api/v1/prov/nodes/{node_id}/statements`. Frontend production build passes.
- **Chip material PROV sample**: Created 12 type-level PROV statements for the chip manufacturing chain (`silicon_wafer` → `wafer` → `wafer_dicing` → `chip_die` → `chip_molding` → `molded_chip` → `chip_testing` → `tested_chip`, plus `lithography_process` inputs). Verified via API and frontend build.
- **Power semiconductor PROV + entity sample**: Created power-semiconductor domain nodes (`gallium`, `gallium_nitride`, `silicon_carbide`, `gan_wafer`, `sic_wafer`, `power_device`, `gan_power_device`, `sic_power_device`, `silicon_power_device`, `power_mosfet`, `igbt`, `wide_bandgap_semiconductor`) and connected them to the existing generic semiconductor process flow instead of a separate simplified chain. GaN/SiC wafers now feed into `initial_wafer_cleaning` and share the same lithography/etch/implant/dicing/packaging path as silicon wafers. Added cross-layer PROV statements such as `gan_power_device --wasDerivedFrom--> gan_wafer --wasDerivedFrom--> gallium_nitride --wasDerivedFrom--> gallium` to express raw-material-to-end-device provenance. Removed the earlier oversimplified parallel process nodes (`gan_crystal_growth`, `gan_device_fabrication`, `sic_device_fabrication`, `silicon_power_device_fabrication`). Mapped new nodes to `semiconductor_industry`.
- **Import script DATE fix**: Fixed `scripts/import_db.py` to parse ISO date strings (`YYYY-MM-DD`) back into `datetime.date` objects when importing PostgreSQL tables. Previously only full ISO datetime strings with a `T` separator were converted, so `DATE` columns like `company_node_exposures.as_of_date` caused `asyncpg.exceptions.DataError: 'str' object has no attribute 'toordinal'`. Verified by successfully importing `data/ArachneData/newest` with `--clear --yes`.
- **PROV semantics mapping & derivation design**: Mapped all `EntityType` and `IndustrialFlowType` values to PROV roles/relations in `docs/prov_overlay_design.md`. Identified that `wasDerivedFrom` has no direct graph equivalent. Designed `derived_from` as an explicit, human-curated industrial-flow edge for direct material lineage between entity nodes; it intentionally skips process nodes, must not be auto-inferred from the current process graph, and must remain hidden by default to avoid polluting the main canvas. Documented allowed/disallowed scenarios, validation rules, display rules, and PROV-N synchronization.
- **PROV-N storage format (deprecated)**: Experimented with W3C PROV-N text documents stored as `data/prov_statements/{node_id}.provn`. Added `backend/app/services/prov_n.py` with a parser/serializer and `/prov/nodes/{id}/provn` endpoints. Later reversed: PROV-N support was commented out of the main backend/frontend code path, storage reverted to JSON (`{node_id}.prov.json`), existing `.provn` files were converted back to JSON and moved to `data/prov_statements/legacy_provn/`. The `prov_n.py` module and raw endpoints remain in the repository for reference and potential future export use, but are no longer imported or mounted. Updated `docs/prov_overlay_design.md` and `frontend/src/components/NodeProvPanel.tsx`. Frontend `npm run build` passes.
- **Semiconductor `derived_from` backfill**: Created 25 `derived_from` edges for semiconductor product chains, including `tested_chip`/`molded_chip`/`chip`/logic/memory/analog/sensor/rf/automotive/dram/nand/ddr5 chips → `chip_die`, `chip_die` → `wafer`, `wafer` → `silicon_wafer`, `silicon_wafer` → `silicon`, silicon-based power devices → `silicon`, and GaN/SiC chains (`gallium_nitride` → `gallium`, `gan_wafer` → `gallium_nitride`, `gan_power_device` → `gan_wafer`, `sic_wafer` → `silicon_carbide`, `sic_power_device` → `sic_wafer`). Fixed a bug in `backend/app/services/derived_from_policy.py` `_existing_derived_from()` where it treated the `(items, total)` tuple returned by `neo4j_storage.list_edges()` as a list, causing all new `derived_from` edges to be rejected as duplicates. Backend restarted to pick up the fix; verification script at `temp/verify_semiconductor_derived_from.py`.
- **`is_test` flag + automated cleanup**: Added `is_test: bool` to IndustrialNode/edge create/update models, Industry/Company/Person/FactualRelation schemas, and PostgreSQL tables (`industries`, `industry_node_mappings`, `companies`, `company_node_exposures`, `persons`, `factual_relations`). Implemented `backend/app/services/test_data_cleanup.py`, `backend/app/routers/admin.py` (`POST /api/v1/admin/cleanup-test-data`), CLI `cleanup-test-data`, and `scripts/cleanup_test_data.py`. Updated test fixtures to stamp `is_test=True`. PostgreSQL `init_postgres_tables()` now adds the column via `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` for existing databases.
- **Arachne-flow engine switcher + flow viewer UI**: Added a top-bar engine selector in `StatsBar.tsx` that switches between `legacy` and `arachne_flow`; selecting `arachne_flow` enters the `flow_graph` workspace with a flow-file list, multi-select checkboxes, and a merged/deduplicated subgraph rendered in the shared `GraphCanvas` via `POST /api/v1/flows/subgraph`. Added a per-selection "重新编译" action that calls the batch endpoint `POST /api/v1/flows/compile`. Verified the engine-specific pass-through APIs (`/api/v1/flows`, `/api/v1/flows/subgraph`, `/api/v1/flows/compile`) and generic engine routing (`/api/v1/query/subgraph/{id}?engine=arachne_flow`).
- **Engine discovery API + dynamic frontend engine selector**: Backend exposes `GET /api/v1/engines` returning registered engine metadata (`name`, `label`, `description`, `is_read_only`, `supports_flows`, `default_view`) and the default engine. Each engine class (`LegacyEngine`, `ArachneFlowEngine`) now provides a `metadata` property. Frontend `StatsBar` fetches this list and renders engine options dynamically instead of hard-coding `legacy`/`arachne_flow`; `App.tsx` uses `default_view` from metadata when switching engines. Added `backend/tests/test_engines.py`. Frontend production build passes; backend tests pass (62).
- **Flow graph canvas refresh fix**: Fixed `FlowGraphPage` so switching selected flows or recompiling actually reloads the shared `GraphCanvas`. The canvas is remounted via a `subgraphQueryKey + canvasVersion` key, and compile success invalidates both the flow list and `flows-subgraph` queries while bumping the version; previously the canvas kept showing the first loaded subgraph because its init effect never reran.
- **Per-file exact-content view + merged full view**: Two flow-view semantics are now explicit. **Per-file view** (`POST /flows/subgraph` via `storage.get_flow_file_graph`) renders exactly the triples declared by the selected file(s) — "what you see is what the file declares" — replacing the previous root-product depth traversal that truncated upstream chains (smartphone now shows all 50 triples including wafer/dicing/bonding segments). **Full view** (`GET /api/v1/flows/graph?merge=method`, used by `GraphCanvas` when no file is selected) merges cross-flow occurrences for readability: ACTION nodes with the same `method_ref` collapse into one `merged_action:{method}` node (provenance in `flow_ids`/`merged_from` properties), parallel edges with the same (from, to, predicate) aggregate into one edge with `count`/`flow_ids` (canvas label shows `×N`), while RESOURCE/METHOD nodes stay shared. Effect: 289 → 189 nodes (-35%), 669 → 198 edges (-70%); the full graph now reads as a layered shared backbone with merged system-integration fanning out to all end products. `merge=none` returns the raw graph. Merged-node ids are view-layer constructs (detail panels render from panel state; relationship list for them is empty by design). Added regression tests `test_flow_file_graph_returns_exact_file_content` and `test_merged_flow_graph_merges_actions_and_edges`. Backend tests pass (66); both views verified via browser screenshots.
- **Per-flow subgraph isolation**: Selecting flow files in the flow view now shows only those flows' own triples. Previously `get_flow_subgraph` traversed `:ARACHNE_FLOW` edges without a `flow_id` filter, so shared resource nodes (e.g. `chip`, produced by packaging/testing actions in all 14 product flows) pulled every other flow's occurrences into the current view — selecting only `smartphone` rendered 47 nodes / 62 edges from 11 flows. Now `get_flow_subgraph(node_id, depth, flow_id=...)` filters traversal with `WHERE ALL(rel IN relationships(path) WHERE rel.flow_id = $flow_id)`, and `POST /flows/subgraph` passes the per-file `flow_id`, so `smartphone` shows just its own 9-node chain (its own packaging/testing actions, chip, PCB, integration, smartphone). The generic engine `get_subgraph` (`?engine=arachne_flow&node_id=X`) keeps the unfiltered cross-flow ecosystem traversal. Node/edge highlight on click always uses canvas data, which is 100% arachne-flow — never legacy. Added regression test `test_flow_subgraph_filtered_by_flow_id`. Backend tests pass (64); verified via browser screenshot.
- **Flow detail panels parity with legacy**: Closed the richness gap between engines' detail panels. Backend: metadata enrichment now covers METHOD nodes (Chinese name/definition from PG) and ACTION nodes (borrow method name/definition via `method_ref`), dispatched via `_enrich_node`; a compile post-pass `_stamp_canonical_names` writes `canonical_name_zh/en` onto resource/dual/method nodes so Chinese search works (`芯片设计` → `chip_design`), and the search clause + label resolution prefer those stamped names. Frontend: `NodeDetail` in readOnly mode now renders the relationship list (`NodeEdgeList` with `engine`/`readOnly`/`onSelectEdge` props, flow nodes adapted for Chinese names) instead of hiding associations entirely; `SearchPanel` adapts flow `GraphNode` results before opening detail (previously blank 中文名) and displays `label`; `EdgeDetail` shows an engine-properties block (`flow_id` 所属流程); `NodeDetail`'s engine-properties block dedupes fields already shown in the main section. Verified via browser screenshot: flow node detail now shows 中文名/英文名/类型/状态/置信度/定义/别名/引擎属性/上下游关系， structurally identical to legacy. Backend tests pass (63).
- **Flow full-graph loading + engine-scoped stats**: Fixed the flow view showing a stale subgraph after unchecking all flow files — the flow effect in `useIndustrialGraph` now bumps `graphKey` when the selection transitions to empty, so `GraphCanvas` remounts and loads the full arachne-flow graph (union of all compiled flow files: 289 nodes / 669 edges from the 14 semiconductor flows). Also `getStats(engine)` now passes the engine to `GET /api/v1/query/stats`, so the top-bar node/edge counts follow the selected engine (flow: 289/669 vs legacy: 933/802). Verified via browser screenshot and API that the flow graph contains **only** `:ArachneFlowNode` nodes and `:ARACHNE_FLOW` edges — no legacy topology (`is_a`/`part_of`) or industrial-flow edges are mixed in; the only legacy touchpoints are shared resource node IDs and Chinese names enriched from the PostgreSQL `industrial_nodes` metadata layer by design.
- **Arachne-flow edge role coloring + direction legend**: Verified (via API + browser screenshots) that flow edge directions are correct and consistent with `design_v4` triples (`[material, feedstock, action]` / `[action, primary_result, product]`) and the legacy graph — materials upstream, arrows point downstream to the final product. To make the direction unmistakable in dense hub fans, arachne_flow edges are now colored by role: input roles (feedstock/component/tool/subject 等, 资源 → 动作) sky blue `#38bdf8`, output roles (primary_result/intermediate 等, 动作 → 资源) emerald `#34d399`, ref/next violet `#a78bfa`; edge labels match the line color. `FlowSidebarPanel` shows a “边颜色与流向” legend explaining the convention. Implemented via `arachneFlowEdgeColor()` in `frontend/src/types/index.ts` and `edgeVisualColor()` in `GraphCanvas.tsx`.
- **Unified engine-agnostic graph workspace**: Both engines now share the exact same main workspace (Layout + CanvasToolbar + search panel + context menus + right panel + saved views). The separate `FlowGraphPage` and the “流程图” tab are removed; the top-bar engine selector switches the data source of the industrial workspace in place. `useIndustrialGraph(engine)` loads nodes/edges via the generic `?engine=` routes (adapting flow `GraphNode`/`GraphEdge` to canvas shapes via `lib/flowAdapters.ts`), resets selections/filters on engine switch (`switchEngine`), and exposes flow-file selection + recompile (`selectedFlowIds`, `toggleFlowId`, `recompileSelectedFlows`). The left sidebar swaps industry/company sections for a `FlowSidebarPanel` (flow multi-select with auto-loaded merged subgraph + recompile button) while keeping the same outer layout and FilterPanel (now engine-aware). Read-only engines only disable editing: node/edge create/edit/delete buttons, connect mode, canvas create menu, edge context-menu delete, and the legacy-only detail sections are hidden, while layout/view save-load/undo/search/focus/hide all keep working. Saved views now record `engine` + `selectedFlowIds` (they only store node IDs/layout, so they are engine-agnostic); loading a view whose engine differs from the current one switches engine first, then applies the view. Backend generic GET routes (`/nodes`, `/edges`) serve both engines. Deleted `frontend/src/components/FlowGraphPage.tsx`. Verified: frontend build passes; all 14 flows recompiled (289 flow nodes).
- **Shared node/edge detail sidebars across engines**: `NodeDetail` and `EdgeDetail` now support a `readOnly` mode (hides edit/delete buttons, draft banner, and legacy-only associations/PROV/expansion sections) and an `engine` prop. `EdgeDetail` resolves endpoint nodes via `GET /nodes/{id}?engine=` and normalizes flow `GraphNode.label` onto `canonical_name_zh`; `NodeDetail` renders engine-specific `properties` (flow_id / resource_type / action_type / method_ref) with Chinese labels. `FlowGraphPage` now reuses these shared panels for both node and edge details (replacing the custom `FlowNodeDetail`), supports edge selection, and adapts flow nodes/edges through the same adapters used by the canvas. Backend fix: generic GET routes (`GET /nodes`, `GET /nodes/{id}`, `GET /edges`, `GET /edges/{id}`) no longer bind legacy response models, so `?engine=arachne_flow` returns flow shapes instead of HTTP 500; legacy responses are unchanged. Added regression test `test_generic_node_and_edge_routes_support_flow_engine`. Backend tests pass (63); frontend build passes.
- **Arachne-flow schema Chinese labels**: Completed Chinese text for the arachne-flow schema on the frontend. `EDGE_TYPE_LABELS` now covers all input roles (`feedstock` 原料, `component` 部件, `additive` 添加剂, `process_material` 过程物料, `catalyst` 催化剂, `energy` 能量, `carrier` 载体, `tool` 工具, `packaging` 包装, `subject` 作用对象, `basis` 依据, `requirement` 要求), all output roles (`primary_result` 主产物, `co_result` 并列产物, `intermediate` 中间产物, `byproduct` 副产物, `scrap` 废料, `waste` 废弃物, `emission` 排放物, `recovered_resource` 回收资源), special roles (`next` 下一步, `ref` 引用方法) and the `other` fallback. Added `ARACHNE_FLOW_PREDICATES`, `ARACHNE_FLOW_NODE_TYPE_LABELS` (资源/动作/方法), `ARACHNE_FLOW_ENTITY_TYPE_LABELS`, `ARACHNE_FLOW_RESOURCE_TYPE_LABELS` (物料/工艺/服务/权利/信息/资质/其他) and `ARACHNE_FLOW_ACTION_TYPE_LABELS` (转化/组合/分离/改性/交付/评估/其他). `FlowGraphPage` now stamps `edge_type_label` on adapted edges so canvas edge labels render Chinese, the node detail panel shows Chinese kind/resource/action-type labels, and the canvas filter list covers the full predicate set instead of the previous subset.
- **Arachne-flow in-memory builder + batch compile + statistics**: Introduced `backend/app/engines/arachne_flow/builder.py` with `FlowGraphBuilder` that loads all YAML files into a unified in-memory graph: RESOURCE/METHOD nodes are global singletons, ACTION nodes are namespaced by `flow_id`, conflicts are detected as warnings, and global validation runs before persistence. Added `storage.compile_flow_graph()` to write the whole in-memory graph to Neo4j in one pass. Rewrote `backend/scripts/load_arachne_flows.py` to use the builder and print statistics: 14 flows, 97 resources, 46 methods, 146 actions, 669 triples; 34 shared resources, 15 shared methods, 15 methods referenced by multiple actions; PostgreSQL coverage gaps; and top common action-method paths across flows (e.g. `chip_design -> wafer_manufacturing -> wafer_dicing` appears in 11 flows). `compile_parsed_flow()` still works for single-flow recompiles and now uses `ON CREATE SET` to avoid overwriting shared node metadata. Updated `clear_flow()` to remove orphan nodes regardless of `flow_id`. All 66 backend tests pass.
- **Arachne-flow merge-by-method only for shared methods**: Changed `get_merged_flow_graph()` so that `merge=method` only creates `merged_action:*` nodes when the same METHOD is referenced by actions in more than one flow. Product-specific integration methods (e.g. `integration_of_photovoltaic_inverter`) now keep their original per-flow action node instead of generating a confusing singleton merged node. Only genuinely cross-flow methods like `chip_design` or `integration_of_gpu` are collapsed. All 66 backend tests pass.
- **Arachne-flow include semantics changed to dependency declaration**: `include` in flow YAML no longer copies/merges included triples into the current file. Instead, it declares an upstream dependency so that the builder can order compilation, detect circular includes, and expand per-flow **effective** views through referenced flows. The parser now only parses the current file's own edges. `POST /api/v1/flows/subgraph` accepts `mode="effective"` (default `"declared"`) to return the selected flows plus all transitively included flows. `FlowGraphBuilder.validate_global()` now warns when a RESOURCE is produced by multiple flows or when a flow consumes a resource produced by an unincluded flow. All 66 backend tests pass.
- **Extracted shared arachne-flow sub-flows**: Moved the duplicated upstream chains out of the 11 product YAMLs into dedicated shared flows: `semiconductor_chip_manufacturing.yaml` (39 triples, chip_design → wafer_manufacturing → wafer_dicing → die_bonding → wire_bonding → chip_molding → chip_testing/chip_packaging_and_testing → chip) and `printed_circuit_board_fabrication.yaml` (6 triples, PCB fabrication → pcb_board). Product flows now `include` these shared flows and keep only their own integration triples. Effects: actions 146 → 59, triples 669 → 237, shared-resource warnings dropped from 15 to 6 (remaining duplicates are downstream component flows like `integration_of_gpu`/`integration_of_ddr5`). Per-file declared view stays clean; per-file effective view (`mode="effective"`) automatically expands through includes so product-to-raw-material tracing is preserved. `POST /api/v1/flows/subgraph` verified: smartphone declared = 6 nodes/5 edges, effective = 47 nodes/50 edges including wafer/chip. All 67 backend tests pass.
- **Completed semiconductor arachne-flow coverage against legacy graph**: Compared the legacy `semiconductor_industry` subgraph (152 nodes, 207 edges) with arachne-flow and added missing value chains as shared flows: `chip_design.yaml` (EDA/IP/IDM → chip_design_output), `silicon_wafer_manufacturing.yaml` (silicon → purification → ingot → slicing → silicon_wafer), `wafer_fabrication_processes.yaml` (silicon_wafer + chip_design_output → cleaning/oxidation/lithography/etching/implantation/diffusion/annealing/deposition/CMP/metrology → wafer, with equipment and material inputs), and `power_semiconductor_manufacturing.yaml` (gallium/GaN/SiC/silicon_wafer → power_device → power_semiconductor). `semiconductor_chip_manufacturing.yaml` now starts from `wafer` and includes `wafer_fabrication_processes.yaml`; `photovoltaic_inverter.yaml` now includes `power_semiconductor_manufacturing.yaml` instead of treating `power_semiconductor` as a leaf. Retired the redundant `metrology_data.yaml` (moved to `data/flows/semiconductor/legacy/`). Enriched wafer fabrication with extra material inputs (dopant_gas, tungsten precursors, molybdenum_precursor). Created the missing PG method node `power_device_fabrication`. Added a persistence verification step to `load_arachne_flows.py` that counts Neo4j nodes/edges after compile. Effects: 19 flows, 99 resources, 40 methods, 57 actions, 245 triples; multi-producer warnings now only cover downstream component integration flows. All 68 backend tests pass.
- **Arachne-flow YAML editor with live preview**: Added a new "流程编辑器" main view (`FlowEditorPage`) with a left YAML editor and right live preview canvas. Backend: refactored `parser.py` to expose `parse_flow_content()`, added `app/engines/arachne_flow/preview.py` to build an in-memory graph (with transitive includes) and convert it to `GraphNode`/`GraphEdge` without writing to Neo4j, added `POST /api/v1/flows/preview` + `GET /api/v1/flows/{flow_id}/content`, `POST /api/v1/flows/format` to re-serialize YAML with edges in compact `[a, b, c]` triple form, and `PUT /api/v1/flows/{flow_id}` / `POST /api/v1/flows` to save/create flow files (with validation and auto-recompile). The preview endpoint tags every node with `properties.flow_ids` (which flows reference it) and returns the transitive `includes` list; the frontend implements the "折叠 include" toggle locally using `lib/flowCollapse.ts`, hiding nodes/edges that belong exclusively to included flows and redirecting cross-boundary edges to `flow_folder:*` nodes (shared nodes stay visible). Frontend: debounced preview on content change (500ms), red error banner keeps the last good graph on syntax/validation errors, flow file selector with content loading, assisted editing toolbar with a searchable node picker, predicate dropdown, quick-insert triple buttons, a triple composer, the collapse toggle, a "整理格式" button that calls the format endpoint, and a "保存" button that saves existing files or creates new ones (prompting for a new flow_id). All 72 backend tests pass; frontend `npm run build` passes.
- **Embedded arachne-flow editor panel in main workspace**: The main workspace's right-side panel now reuses the full `FlowEditorPage` editor (without its right-hand preview canvas) via `FlowEditorPanel`. The FlowSidebarPanel has an "编辑流程" button that opens the panel without navigating away, so the total graph remains visible next to the editor. The panel includes the complete assisted editing UI (flow selector, node picker, triple composer, save/format/collapse controls). The divider between the editor and the main graph is draggable (resizable right panel via `Layout`'s `rightPanelWidth`/`onRightPanelResize`). While editing, the nodes from the current YAML content are automatically highlighted in the main graph (computed from the preview result's current-flow edges, with ACTION nodes also mapped to their `merged_action:{method_ref}` counterparts to avoid isolated highlights). After saving, the main graph recompiles the selected flows. A disabled "从图添加（预留）" placeholder for future graph-level editing is kept. All 72 backend tests pass; frontend `npm run build` passes.
- **Integration method PG nodes + NAND flash flow**: Created missing PG `industrial_nodes` for all `integration_of_*` methods (e.g. `integration_of_ssd` = 固态硬盘集成, `integration_of_gpu` = GPU集成) so arachne-flow action nodes now have Chinese labels. Added `nand_flash_chip_manufacturing.yaml` shared flow (`chip_die` → `chip_packaging_and_testing` → `nand_flash_chip`) and updated `ssd.yaml` to include it, fixing the isolated `act_integrate_ssd` node. Also fixed the save-success banner to auto-hide after 3 seconds instead of pushing the toolbar buttons. All 72 backend tests pass.
- **Retired legacy metrology_data.yaml**: Extracted its remaining useful content into `wafer_fabrication_processes.yaml` (pre-diffusion cleaning step producing `diffusion_ready_wafer`, and `annealed_wafer` as an additional input to `metrology_inspection`) and deleted the legacy file. All 72 backend tests pass.
- **Hierarchical flow file organization**: Backend now scans `data/flows/` recursively for YAML files and computes a `category` from the directory path (e.g. `semiconductor`). `GET /api/v1/flows` returns `category` for each flow; the FlowSidebarPanel and the flow editor's file selector group flows by category instead of a flat list. `include` resolution now searches recursively across all categories. The legacy `manifest.yaml` was removed since listing is now driven by recursive scanning. All 72 backend tests pass.
- **Merge-by-method only for cross-flow shared methods**: Fixed `get_merged_flow_graph()` so `merge=method` only creates `merged_action:*` nodes when the same METHOD is referenced by actions from **more than one distinct flow**. Intra-flow repeated methods like `wafer_cleaning_process` (multiple cleaning steps inside `wafer_fabrication_processes.yaml`) no longer collapse into a single merged node. Added a "原始视图 / 合并视图" toggle in the FlowSidebarPanel to switch between `merge=none` (raw graph) and `merge=method` (merged graph) for the full flow view. All 72 backend tests pass.

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
- [x] **Run full test suite** — `pytest backend/tests` passes (44 passed). Fixed pytest-asyncio loop-boundary flakiness and async fixture declaration bugs.

### PROV / Derivation
> PROV 覆盖层已整体弃用：`derived_from` 直接作为产业图的一条工业流边存在，不再维护独立的 PROV 声明文件，也不存在 PROV 同步任务。

- [x] **Add `derived_from` to schemas and labels**: `IndustrialFlowType.DERIVED_FROM` and `EDGE_TYPE_LABELS` updated in backend, frontend types/labels, edge forms, and CLI choices.
- [x] **Implement `derived_from` policy validation**: endpoints cannot be `process`, target cannot be a generic consumable, no duplicate, acyclic; enforced in `create_edge`, `quick_create_edge`, `update_edge`, and `process_batch`.
- [x] **Implement material-derivation overlay view**: frontend filter panel toggle "显示物料派生边（derived_from）" default off; hidden edges are excluded from layout and neighbor expansion. `derived_from` also excluded from company exploration and material-connection queries.
- [ ] **Dedicated `derived_from` creation UI**: currently shares the normal edge creation form; a dedicated shortcut/wizard can be added later.
- [x] **Backfill existing chains**: manually curated and created 25 `derived_from` edges for chip and power-semiconductor flows (e.g., `tested_chip → silicon_wafer`, `gallium_nitride → gallium`).

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
- `init_postgres_tables()` now creates 8 tables: `industries`, `industry_node_mappings`, `companies`, `company_node_exposures`, `computation_jobs`, `persons`, `factual_relations`, `industrial_nodes`.

### Schema Patterns
- All IDs use snake_case regex: `^[a-z][a-z0-9_]*$`, min 3 chars, max 64.
- `RecordStatus`: `ACTIVE`, `PENDING`, `REJECTED`, `ARCHIVED`
- `Confidence`: `HIGH`, `MEDIUM`, `LOW`
- `EntityType` now includes `process` for manufacturing/process nodes.
- `IndustrialFlowType` now includes `process_output` for process → output relationships.
- UUID fields now auto-generate; callers do not need to supply them.

### Test Data Conventions
- All test-created entities (nodes, edges, industries, companies, mappings, exposures, persons, factual relations) **SHOULD set `is_test: true`**.
- The backend exposes `POST /api/v1/admin/cleanup-test-data?dry_run=true|false` to delete all entities flagged as test data.
- The CLI provides `python cli/arachne_cli.py cleanup-test-data [--dry-run]`.
- A standalone script is available at `scripts/cleanup_test_data.py` for post-test hooks.
- After running tests, call one of the cleanup tools to remove residual test data instead of deleting manually.

### Git Hygiene
- Do NOT run `git commit`, `git push`, `git reset`, `git rebase` without explicit user confirmation.
- LF/CRLF warnings are normal on Windows; Git will handle conversion.

---

## 7. Design Documents

- `docs/view_design_v2.md` — Three-layer view pyramid architecture (Industry → Industrial → Company) (retired)
- `docs/think-01.md`, `docs/think-02.md` — Historical design thinking
- `docs/prompts.txt` — Prompt history
- `docs/ui_architecture_refactor_2026-05-24.md` — Current UI architecture and future extension directions
- `docs/arachne_engine_refactor_design.md` — Engine subsystem refactor: dual Neo4j instances, shared metadata, pluggable engines (legacy + arachne-flow)

---

## 8. Pending Architecture Work

### Engine Subsystem Refactor

**Legacy-only phase is complete.** The original Neo4j-backed implementation has been moved into `app/engines/legacy/` (`engine.py`, `storage.py`, `schemas.py`, `policies/`), core models live in `app/models/core.py`, and `app/services/graph_service.py` delegates to the registered engine. All existing endpoints remain backward-compatible.

Remaining work (arachne-flow integration):
- [ ] **Dual Neo4j instances (optional)**: Community Edition does not support multiple databases; for full isolation run a second Neo4j process on a different port (main: `7687`, flow: `7688`) and set `NEO4J_FLOW_URI`. Currently both engines share the same instance but use separate labels/relationship types.
- [ ] **Arachne-flow reasoning adapter**: the engine can be queried for nodes/edges/subgraphs, but the reasoning module still assumes legacy edge types. Implement `ArachneFlowReasoningAdapter` so tasks like `association`, `bottleneck_detection`, and `impact_propagation` can traverse `:ARACHNE_FLOW` edges.
- [ ] **Flow metadata richness**: synthetic resource `local` names are currently generic; improve the generator to read `industrial_nodes.canonical_name_zh` for friendlier labels. Surface METHOD descriptions and ACTION method refs more prominently in the UI.
- [x] **Engine switcher + recompile workflow UI**: Added a top-bar engine selector and a flow sidebar with multi-select plus a "重新编译" action calling `POST /api/v1/flows/compile`.
- [ ] **Cross-engine overlay**: optionally overlay arachne-flow process paths onto the legacy industrial graph for comparison.

See `docs/arachne_engine_refactor_design.md` for full boundary analysis, dry-run scenarios, reasoning architecture, pass-through API design, and implementation phases.

---

## 9. Agent Skills

项目级 agent skills 位于根目录 `skills/` 下，提供针对本系统的程序化操作指引：

- `skills/arachne-graph/` — 本体设计技能：判断候选词是否应登记为产业节点、合并为别名或被拒绝。
- `skills/arachne-api/` — CLI/API 操作技能：优先通过 `cli/arachne_cli.py` 批量注册节点/关系/公司/行业/映射/暴露，管理行业和公司，以及查询图谱；CLI 未覆盖的场景可直接调用底层 API。

通过对话构造或维护图谱时，通常两个技能协同使用：`arachne-graph` 负责本体决策，`arachne-api` 负责通过 CLI 执行具体操作。

---

*Last updated: 2026-07-16 21:05 CST*
