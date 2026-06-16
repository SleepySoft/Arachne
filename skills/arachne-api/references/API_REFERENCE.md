# Arachne REST API 参考

> 本文件作为底层 API 参考。日常操作请优先使用 `arachne_cli.py`（见 CLI_REFERENCE.md）；当 CLI 未覆盖某些操作（如人员、事实关系）时，可直接调用以下 API。

## 基础 URL

CLI 默认连接：

```
http://localhost:8005/api/v1
```

后端原生地址（若直接调用）：

```
http://localhost:8000/api/v1
```

当前后端未配置认证，CORS 为开放状态。

---

## 接口索引

### 产业图

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/nodes` | 创建节点 |
| GET | `/nodes` | 列出节点 |
| GET | `/nodes/{node_id}` | 获取节点详情 |
| PUT | `/nodes/{node_id}` | 更新节点 |
| DELETE | `/nodes/{node_id}` | 删除节点 |
| POST | `/edges` | 创建边 |
| GET | `/edges` | 列出边 |
| GET | `/edges/{edge_id}` | 获取边详情 |
| PUT | `/edges/{edge_id}` | 更新边 |
| DELETE | `/edges/{edge_id}` | 删除边 |
| POST | `/batches` | 提交 `GraphRegistrationBatch` |

### 行业

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/industries` | 创建行业 |
| GET | `/industries` | 列出行业 |
| GET | `/industries/{id}` | 获取行业详情 |
| PUT | `/industries/{id}` | 更新行业 |
| DELETE | `/industries/{id}` | 删除行业 |
| GET | `/industries/{id}/mappings` | 列出节点映射 |
| POST | `/industries/{id}/mappings` | 创建节点映射 |
| DELETE | `/industries/{id}/mappings/{mapping_id}` | 删除节点映射 |
| GET | `/industries/{id}/nodes` | 获取映射的产业节点 |
| GET | `/industries/{id}/subgraph` | 获取 Neo4j 子图 |
| GET | `/industries/by-node/{node_id}` | 反向查询：哪些行业映射了该节点 |

### 公司

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/companies` | 创建公司 |
| GET | `/companies` | 列出公司 |
| GET | `/companies/{id}` | 获取公司详情 |
| PUT | `/companies/{id}` | 更新公司 |
| DELETE | `/companies/{id}` | 删除公司 |
| GET | `/companies/{id}/exposures` | 列出节点暴露 |
| POST | `/companies/{id}/exposures` | 创建节点暴露 |
| DELETE | `/companies/{id}/exposures/{exposure_id}` | 删除节点暴露 |
| GET | `/companies/{id}/nodes` | 获取暴露的产业节点 |
| GET | `/companies/{id}/subgraph` | 获取 Neo4j 临时子图 |
| GET | `/companies/by-node/{node_id}` | 反向查询：哪些公司暴露了该节点 |
| GET | `/companies/{id}/exploration-graph` | 异构探索图 |
| GET | `/companies/nodes/{node_id}/connected-companies` | 同业/上游/下游公司 |
| GET | `/companies/{id}/material-connections` | 基于物料流的公司关系 |

### 业务批量

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/business-batches` | 提交 `BusinessRegistrationBatch` |

### 事实关系图

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/factual-graph/persons` | 创建人员 |
| GET | `/factual-graph/persons` | 列出人员 |
| GET | `/factual-graph/persons/{id}` | 获取人员详情 |
| PUT | `/factual-graph/persons/{id}` | 更新人员 |
| DELETE | `/factual-graph/persons/{id}` | 删除人员 |
| POST | `/factual-graph/relations/person-company` | 创建人员→公司关系 |
| POST | `/factual-graph/relations/person-person` | 创建人员→人员关系 |
| POST | `/factual-graph/relations/company-company` | 创建公司→公司关系 |
| GET | `/factual-graph/relations` | 列出关系 |
| GET | `/factual-graph/relations/{id}` | 获取关系详情 |
| PUT | `/factual-graph/relations/{id}` | 更新关系 |
| DELETE | `/factual-graph/relations/{id}` | 删除关系 |
| GET | `/factual-graph/persons/{id}/neighborhood` | 以人员为中心的子图 |
| GET | `/factual-graph/companies/{id}/neighborhood` | 以公司为中心的子图 |
| POST | `/factual-graph/sync-companies` | 将所有 ACTIVE 公司同步到 Neo4j |

### 跨域探索

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/explore/companies/{id}/industrial-context` | 公司 → 上游/下游节点 |
| GET | `/explore/nodes/{id}/ecosystem` | 节点 → 暴露公司 + 事实关系 |
| GET | `/explore/persons/{id}/industrial-footprint` | 人员 → 公司 → 暴露 |
| GET | `/explore/companies/{id}/full-context` | 综合事实与产业上下文 |

### 查询

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/query/subgraph/{node_id}` | 节点周边子图 |
| GET | `/query/neighbors/{node_id}` | 直接邻居 |
| GET | `/query/path` | 两节点间路径 |
| GET | `/query/stats` | 图谱统计 |
| GET | `/query/conflicts` | 冲突检测 |

---

## 通用 Schema

### Evidence（证据）

```json
{
  "source_title": "资料标题",
  "source_url": "https://example.com/report.pdf",
  "quote": "支持该节点或关系的原文摘录"
}
```

必填：`source_title`、`quote`。`source_url` 可选。

### Node（产业节点）

```json
{
  "node_id": "lidar_system",
  "canonical_name_zh": "激光雷达系统",
  "canonical_name_en": "LiDAR system",
  "aliases": ["激光雷达", "LiDAR"],
  "definition": "...",
  "entity_type": "system",
  "evidence": [],
  "confidence": "HIGH",
  "status": "ACTIVE",
  "notes": null
}
```

### Edge（边）

```json
{
  "edge_namespace": "industrial_flow",
  "edge_id": "laser_to_lidar",
  "from_node": "laser",
  "to_node": "lidar_system",
  "edge_type": "material_flow",
  "description": "...",
  "evidence": [],
  "confidence": "HIGH",
  "notes": null
}
```

### GraphRegistrationBatch（图谱注册批量）

```json
{
  "batch_id": "batch_001",
  "task_description": "...",
  "nodes_to_upsert": [],
  "edges_to_upsert": [],
  "rejected_or_pending": []
}
```

响应示例：

```json
{
  "batch_id": "batch_001",
  "nodes_created": 2,
  "nodes_updated": 0,
  "edges_created": 1,
  "edges_updated": 0,
  "rejected_or_pending_stored": 0,
  "errors": []
}
```

### Industry（行业）

```json
{
  "industry_id": "intelligent_driving",
  "name_zh": "智能驾驶",
  "name_en": "Intelligent Driving",
  "aliases": ["自动驾驶"],
  "industry_type": "curated_view",
  "description": "...",
  "status": "ACTIVE",
  "notes": null
}
```

### IndustryNodeMapping（行业节点映射）

```json
{
  "mapping_id": "intelligent_driving_contains_lidar_system",
  "industry_id": "intelligent_driving",
  "node_id": "lidar_system",
  "role": "核心产品",
  "weight": 0.9,
  "confidence": "HIGH",
  "evidence": [],
  "status": "ACTIVE",
  "notes": null
}
```

### Company（公司）

```json
{
  "company_id": "hesai_technology",
  "name_zh": "禾赛科技",
  "name_en": "Hesai Technology",
  "aliases": ["Hesai"],
  "stock_codes": ["HSAI"],
  "description": "...",
  "country": "CN",
  "province": "上海",
  "city": "上海",
  "founded_year": 2014,
  "employee_count": 1000,
  "revenue_cny": 1800000000,
  "market_cap_cny": 12000000000,
  "net_profit_cny": -50000000,
  "company_type": "public",
  "status": "ACTIVE",
  "notes": null
}
```

### CompanyNodeExposure（公司节点暴露）

```json
{
  "exposure_id": "hesai_technology_produce_lidar_system",
  "company_id": "hesai_technology",
  "node_id": "lidar_system",
  "activity_type": "produce",
  "role": "激光雷达整机厂商",
  "weight": 0.95,
  "confidence": "HIGH",
  "evidence": [],
  "status": "ACTIVE",
  "as_of_date": "2024-12-31",
  "notes": null
}
```

### BusinessRegistrationBatch（业务注册批量）

```json
{
  "batch_id": "business_batch_001",
  "task_description": "...",
  "industries_to_upsert": [],
  "industry_node_mappings_to_upsert": [],
  "companies_to_upsert": [],
  "company_node_exposures_to_upsert": []
}
```

响应示例：

```json
{
  "batch_id": "business_batch_001",
  "industries_created": 1,
  "industries_updated": 0,
  "mappings_created": 1,
  "mappings_updated": 0,
  "companies_created": 1,
  "companies_updated": 0,
  "exposures_created": 1,
  "exposures_updated": 0,
  "errors": []
}
```

### Person（人员）

```json
{
  "person_id": "person_zhang_san",
  "name_zh": "张三",
  "name_en": "Zhang San",
  "aliases": [],
  "gender": "male",
  "birth_year": 1975,
  "nationality": "CN",
  "id_card_hash": null,
  "profile": "某科技公司创始人",
  "status": "ACTIVE",
  "notes": null
}
```

### 事实关系

人员 → 公司（`/factual-graph/relations/person-company`）：

```json
{
  "relation_domain": "person_company",
  "relation_id": "zhang_san_shareholder_hesai",
  "person_id": "person_zhang_san",
  "company_id": "hesai_technology",
  "relation_type": "shareholder",
  "subtype": "董事长",
  "equity_ratio": 0.15,
  "amount_cny": 15000000,
  "source": "年报",
  "evidence": [],
  "confidence": "HIGH",
  "status": "ACTIVE",
  "start_date": "2020-01-01",
  "end_date": null,
  "is_history": false,
  "notes": null
}
```

人员 → 人员（`/factual-graph/relations/person-person`）：

```json
{
  "relation_domain": "person_person",
  "relation_id": "zhang_san_spouse_li_si",
  "from_person_id": "person_zhang_san",
  "to_person_id": "person_li_si",
  "relation_type": "spouse",
  "subtype": "配偶",
  "source": "工商登记",
  "evidence": [],
  "confidence": "MEDIUM",
  "status": "ACTIVE",
  "start_date": null,
  "end_date": null,
  "is_history": false,
  "notes": null
}
```

公司 → 公司（`/factual-graph/relations/company-company`）：

```json
{
  "relation_domain": "company_company",
  "relation_id": "hesai_supplier_of_robosense",
  "from_company_id": "hesai_technology",
  "to_company_id": "robosense",
  "relation_type": "supplier",
  "amount_cny": 50000000,
  "contract_no": "PO-2024-001",
  "proportion": 0.1,
  "source": "公告",
  "evidence": [],
  "confidence": "HIGH",
  "status": "ACTIVE",
  "start_date": null,
  "end_date": null,
  "is_history": false,
  "notes": null
}
```

---

## 枚举值

### EntityType（实体类型）

`material`, `component`, `device`, `module`, `subsystem`, `system`, `platform`, `infrastructure`, `application_system`, `service`, `technology_capability`, `unknown`

### EdgeNamespace / EdgeType

| 命名空间 | 类型 |
|---|---|
| `industrial_flow` | `material_flow`, `composition`, `energy_flow`, `information_flow`, `capability_supply`, `service_flow` |
| `ontology` | `alias_of`, `is_a`, `variant_of`, `related_term` |

### Status / Confidence

- `status`：`ACTIVE`, `PENDING`, `REJECTED`
- `confidence`：`HIGH`, `MEDIUM`, `LOW`

### IndustryType

`formal_industry`, `curated_view`, `theme_view`

### CompanyType

`public`, `private`, `state_owned`, `startup`, `unknown`

### CompanyActivityType

`rnd`, `design`, `manufacture`, `produce`, `integrate`, `operate`, `provide_service`, `procure`, `use`, `unknown`

### PersonCompanyRelationType

`shareholder`, `executive`, `legal_representative`, `actual_controller`, `supervisor`, `director`, `board_chair`, `general_manager`, `history_role`

### PersonPersonRelationType

`relative`, `spouse`, `parent_child`, `sibling`, `partner`, `colleague`, `trust`, `associate`

### CompanyCompanyRelationType

`supplier`, `customer`, `partner`, `investor`, `investee`, `competitor`, `client`, `contractor`, `guarantor`, `creditor`, `debtor`, `lessee`, `lessor`

---

## 列表查询参数

### GET /nodes

- `page`（默认 1）
- `page_size`（默认 20，最大 1000）
- `entity_type`
- `status`
- `search`

### GET /edges

- `page`, `page_size`
- `edge_namespace`
- `edge_type`
- `from_node`
- `to_node`

### GET /industries

- `page`, `page_size`
- `industry_type`
- `status`
- `search`

### GET /companies

- `page`, `page_size`
- `country`
- `company_type`
- `status`
- `search`

### GET /companies/{id}/exposures

- `activity_type`

### GET /factual-graph/persons

- `page`, `page_size`
- `search`

### GET /factual-graph/relations

- `page`, `page_size`
- `relation_domain`
- `relation_type`
- `person_id`
- `company_id`
