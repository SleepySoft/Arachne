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
- **PostgreSQL**: `postgresql://postgres:postgres@localhost:5433/arachne` (not installed yet)

### System Management
- `arachne_manager.py` — Python cross-platform manager (`start/stop/status/stats/logs`)
- `start-all.ps1` / `stop-all.ps1` — PowerShell one-click scripts
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

### Commit 8 — Industry Mapping Workflow (Frontend + Backend)
- `IndustryMappingForm.tsx`: new create/edit form for industry-to-node mappings, with searchable node picker, role/weight/confidence/status/evidence/notes fields
- `IndustryDetail.tsx`: replaced the `alert("添加映射功能待实现")` stub with inline add/edit mapping UI; added per-mapping edit/delete actions
- `NodeIndustriesPanel.tsx`: added "关联到新行业" form to associate the current node with an existing industry
- `IndustryForm.tsx`: added aliases input (comma-separated) so created industries can have aliases
- `api.ts`: added `updateIndustryMapping()` wrapper
- `industries.py`: added `PUT /api/v1/industries/{id}/mappings/{mapping_id}` endpoint
- `test_industry_storage.py`: removed stale `IndustryCreate` import
- `StatsBar.tsx` / `App.tsx`: fixed pre-existing TypeScript errors that blocked the production build (dead `MainView` type, unused setters)

### Historical Fixes (carried over)
- **HTTP 422 fix**: `page_size` query limit relaxed from `le=100` to `le=1000`
- **Frontend filter bug**: `GraphCanvas` `useEffect` deps fixed with `useRef` + `useCallback`
- **Neo4j compatibility**: evidence serialized as JSON string; `neo4j.time.DateTime` → Python `datetime`
- **Neo4j deployment**: local Windows install (Docker blocked by Zscaler)

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
- [ ] **Install PostgreSQL locally** — system currently has no `psql`; backend code is ready but cannot run integration tests until PostgreSQL is installed
- [ ] **Run full test suite** — all PostgreSQL-dependent tests skip when DB is unavailable; verify they pass after installation

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

*Last updated: 2026-06-16*
