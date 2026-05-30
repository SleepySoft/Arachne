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
(via `/explore` endpoints) rather than batch-computed and persisted.

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

### 3.2 Backend Directory Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI entry, registers all routers
│   ├── config.py                  # Settings (Neo4j + PostgreSQL URLs)
│   ├── database.py                # Neo4j async driver
│   ├── database_postgres.py       # asyncpg pool + table init
│   ├── models/
│   │   ├── schemas.py             # Core graph models (Node, Edge, Evidence, RecordStatus)
│   │   ├── industry_schema.py     # Industry, IndustryNodeMapping, IndustryType
│   │   ├── company_schema.py      # Company, CompanyNodeExposure, CompanyActivityType, CompanyType, BusinessRegistrationBatch
│   │   └── factual_graph_schema.py # Person, FactualRelation, three relation types ★ NEW
│   ├── services/
│   │   ├── neo4j_storage.py       # Neo4j CRUD + subgraph queries
│   │   ├── graph_service.py       # Business logic: nodes, edges, batches, conflicts
│   │   ├── industry_storage.py    # PostgreSQL CRUD for industries + mappings
│   │   ├── company_storage.py     # PostgreSQL CRUD for companies + exposures
│   │   └── factual_graph_storage.py # PG + Neo4j for Factual Graph ★ NEW
│   └── routers/
│       ├── nodes.py               # /api/v1/nodes
│       ├── edges.py               # /api/v1/edges
│       ├── batches.py             # /api/v1/batches (GraphRegistrationBatch)
│       ├── business_batches.py    # /api/v1/business-batches (BusinessRegistrationBatch)
│       ├── industries.py          # /api/v1/industries + /subgraph + /mappings
│       ├── companies.py           # /api/v1/companies + /subgraph + /exposures + /by-node
│       ├── factual_graph.py       # /api/v1/factual-graph (Person + Relations) ★ NEW
│       ├── explore.py             # /api/v1/explore (cross-domain) ★ NEW
│       └── query.py               # /api/v1/query (subgraph, neighbors, paths, stats)
└── tests/
    ├── test_database_postgres.py
    ├── test_industry_storage.py
    ├── test_company_storage.py
    ├── test_industry_company_routers.py
    └── test_business_batches.py   # ★ NEW
```

### 3.3 Key API Endpoints

**Industries**
- `POST /api/v1/industries` — create
- `GET /api/v1/industries` — list (paginated, filterable)
- `GET /api/v1/industries/{id}` — detail
- `PUT /api/v1/industries/{id}` — update
- `DELETE /api/v1/industries/{id}` — delete
- `GET /api/v1/industries/{id}/mappings` — list node mappings
- `GET /api/v1/industries/{id}/subgraph` — Neo4j subgraph of mapped nodes

**Companies**
- `POST /api/v1/companies` — create
- `GET /api/v1/companies` — list (paginated, filter by country/type/status/node_id/activity_type)
- `GET /api/v1/companies/{id}` — detail
- `PUT /api/v1/companies/{id}` — update
- `DELETE /api/v1/companies/{id}` — delete
- `GET /api/v1/companies/{id}/exposures` — list node exposures
- `GET /api/v1/companies/{id}/subgraph` — Neo4j temporary subgraph of exposed nodes
- `GET /api/v1/companies/by-node/{node_id}` — reverse lookup: companies producing a node

**Batches**
- `POST /api/v1/batches` — GraphRegistrationBatch (nodes + edges)
- `POST /api/v1/business-batches` — BusinessRegistrationBatch (industries + mappings + companies + exposures)

---

## 4. Completed Work

### Commit 1 — PostgreSQL Infrastructure
- `database_postgres.py`: asyncpg pool + `init_postgres_tables()` creates 4 tables
- `config.py`: `POSTGRES_URL` setting (default port 5433)
- `requirements.txt`: added `asyncpg`
- `test_database_postgres.py`: connection test

### Commit 2 — Industry Storage Layer
- `industry_schema.py`: `Industry`, `IndustryNodeMapping`, `IndustryType` enum
- `industry_storage.py`: full CRUD + `get_industry_subgraph()` (Neo4j integration)
- `test_industry_storage.py`: full test coverage

### Commit 3 — Company Storage Layer
- `company_schema.py`: `Company`, `CompanyNodeExposure`, `CompanyActivityType` enum, `BusinessRegistrationBatch`
- `company_storage.py`: full CRUD + `get_company_subgraph()` + `list_companies_by_node()`
- `test_company_storage.py`: full test coverage

### Commit 4 — REST API Routes + Neo4j Subgraph
- `industries.py`: all industry endpoints
- `companies.py`: all company endpoints
- `main.py`: registered new routers
- `test_industry_company_routers.py`: end-to-end API tests

### Commit 5 — Business Batch Extension (latest)
- `business_batches.py`: new router for `BusinessRegistrationBatch`
- `graph_service.py`: `process_business_batch()` with upsert logic for all 4 entity types
- `industry_storage.py`: added `get_mapping_by_industry_and_node()` + `update_mapping()`
- `company_storage.py`: added `get_exposure_by_company_and_node()` + `update_exposure()`
- `company_schema.py`: added `CompanyType` enum + missing fields (`country`, `province`, `city`, `founded_year`, `employee_count`, `revenue_cny`, `market_cap_cny`, `net_profit_cny`, `company_type`)
- `industry_schema.py` / `company_schema.py`: UUID fields now have `default_factory=uuid4`
- `test_business_batches.py`: 4 tests (full batch, upsert existing, mapping dedup, empty batch)
- Cleaned up root-level stale files: `company_schema.py`, `core_schema.py`, `industry_schema.py`

### Historical Fixes (carried over)
- **HTTP 422 fix**: `page_size` query limit relaxed from `le=100` to `le=1000`
- **Frontend filter bug**: `GraphCanvas` `useEffect` deps fixed with `useRef` + `useCallback`
- **Neo4j compatibility**: evidence serialized as JSON string; `neo4j.time.DateTime` → Python `datetime`
- **Neo4j deployment**: local Windows install (Docker blocked by Zscaler)

---

## 5. Pending Work

### Phase 2 — Factual Graph Completion
The Factual Graph schema and storage are implemented. Remaining work:
- Frontend pages for Person CRUD and relation visualization
- Batch import for factual relations (annual reports, Tianyancha data)

### Phase 3 — Frontend Views
Build React pages for:
- **Industry List Page**: table view of industries with search/filter
- **Industry Detail Page**: show mapped nodes + subgraph visualization (reuse `GraphCanvas`)
- **Company List Page**: table view with country/type/node filters
- **Company Detail Page**: show exposures + temporary subgraph + factual relations
- **Person List/Detail Page**: new, for Factual Graph
- **Cross-domain Exploration Page**: unified explore interface with domain color coding

### Infrastructure
- [ ] **Install PostgreSQL locally** — system currently has no `psql`; backend code is ready but cannot run integration tests until PostgreSQL is installed
- [ ] **Run full test suite** — all PostgreSQL-dependent tests skip when DB is unavailable; verify they pass after installation

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

- `docs/view_design_v2.md` — Three-layer view pyramid architecture (Industry → Industrial → Company)
- `docs/think-01.md`, `docs/think-02.md` — Historical design thinking
- `docs/prompts.txt` — Prompt history

---

*Last updated: 2026-05-21*
