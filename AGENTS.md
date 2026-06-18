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
| Relational DB | PostgreSQL (planned, code ready, not installed locally) |
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
- `scripts/arachne_manager.py` — Python cross-platform manager (`start/stop/status/stats/logs`)
- `scripts/start-all.ps1` / `scripts/stop-all.ps1` — PowerShell one-click scripts
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
- `schemas.py`: added `IndustrialFlowEdgeQuickCreate` input model with auto-generated `edge_id`, default `edge_type=material_flow`, and auto-generated description
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

### Historical Fixes (carried over)
- **HTTP 422 fix**: `page_size` query limit relaxed from `le=100` to `le=1000`
- **Frontend filter bug**: `GraphCanvas` `useEffect` deps fixed with `useRef` + `useCallback`
- **Neo4j compatibility**: evidence serialized as JSON string; `neo4j.time.DateTime` → Python `datetime`
- **Neo4j deployment**: local Windows install (Docker blocked by Zscaler)

### Recent Changes
- **Process node type + `produces` edge type**: `EntityType.PROCESS` and `IndustrialFlowType.PRODUCES` added to backend/frontend schemas; used for material/equipment → process → product flow modeling.
- **Ontology rules registry**: `backend/app/services/ontology_rules.py` is the code-side single source of truth for design rules; `docs/ontology_design_rules.md` documents material/process granularity and the canonical `Input → Process → Output` flow.
- **New DB checkers**: `entity_domain_boundary`, `device_to_product_direct_edge`, `input_to_product_direct_edge` enforce cross-domain isolation and the process-intermediation rule.
- **Frontend modularization**: `frontend/src/App.tsx` refactored from 1120 lines to ~280 lines by extracting `useIndustrialGraph`, `useCompanyGraph`, and panel components under `frontend/src/components/panels/`.
- **High-frequency process refactor**: Inserted process nodes for automotive steel/aluminum forming, copper processing, glass/optical fiber manufacturing, semiconductor wafer/design flows, and remaining domains (aluminum/cement/wood/real estate/paper/PCB/PET/plastic/rubber/steel sheet); `input_to_product_direct_edge` violations reduced from 46 to 0.
- **Neo4j connection resilience**: Added connection pool settings (`max_connection_lifetime`, `connection_acquisition_timeout`, `max_connection_pool_size`) and global exception handlers for `ServiceUnavailable` / `SessionExpired` / `ConnectionResetError` to return 503 instead of crashing uvicorn.
- **Node search ranking fix**: `list_nodes` now boosts exact matches, then prefix matches, then substring matches; also searches `canonical_name_en`. Searching "芯片" now returns the `chip` node first instead of being buried after other chip-related nodes.

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
- `IndustrialFlowType` now includes `produces` for process → output relationships.
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

*Last updated: 2026-06-18*
