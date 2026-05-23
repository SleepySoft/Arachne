# Batch 001 产业图与公司视图构建日志

**构建时间**: 2026-05-23  
**数据批次**: `data/stock_batches/batch_001.json`  
**覆盖公司**: 10家上市公司  

---

## 一、基础设施准备

### 1.1 PostgreSQL 安装与配置
- **问题发现**: 系统代码已设计好 PostgreSQL 层，但本地未安装 PostgreSQL，导致 industries/companies API 返回空。
- **解决过程**: 
  - 尝试使用 `winget` 安装 PostgreSQL 16，下载成功但安装程序超时。
  - 检查发现 `C:\Program Files\PostgreSQL\16` 已存在，说明安装实际成功。
  - 服务无法启动，日志显示端口 5432 被占用（TIME_WAIT 状态）。
  - 修改 `postgresql.conf` 端口为 5433，成功启动。
  - 修改 `backend/app/config.py` 中的 `POSTGRES_URL` 端口为 5433。
  - 创建数据库 `arachne`。
  - 重启后端，4张表（companies, company_node_exposures, industries, industry_node_mappings）自动初始化成功。

### 1.2 后端程序错误修复
在构建过程中发现并修复了以下程序错误：

**Bug 1: Industry schema 缺少 `aliases` 字段**
- 现象: `POST /api/v1/business-batches` 返回 `'Industry' object has no attribute 'aliases'`
- 原因: `industry_storage.py` 的 `create_industry` 访问 `data.aliases`，但 `Industry` schema 未定义该字段
- 修复: 在 `backend/app/models/industry_schema.py` 中为 `Industry` 添加 `aliases: List[str] = Field(default_factory=list)`

**Bug 2: Evidence 对象 JSON 序列化失败**
- 现象: `POST /api/v1/business-batches` 返回 `Object of type Evidence is not JSON serializable`
- 原因: `industry_storage.py` 和 `company_storage.py` 中使用 `json.dumps(data.evidence)` 直接序列化 Pydantic 模型列表
- 修复: 改为 `json.dumps([e.model_dump(mode='json') for e in data.evidence])`

**Bug 3: 子图 API 中 Neo4j DateTime 未转换**
- 现象: `GET /api/v1/industries/{id}/subgraph` 和 `GET /api/v1/companies/{id}/subgraph` 返回 500
- 原因: `industries.py` 和 `companies.py` 中从 Neo4j 获取节点后直接 `IndustrialNode(**props)`，未将 `neo4j.time.DateTime` 转为 Python `datetime`
- 修复: 导入并使用 `_to_datetime()` 和 `_evidence_from_db()` 转换时间字段和 evidence 字段

**Bug 4: 子图 API 中 relationship 序列化问题**
- 现象: 使用 `await result.data()` 后，`record["r"]` 变为 tuple 而非 Relationship 对象
- 原因: `result.data()` 将 Neo4j 类型序列化为基本 Python 类型
- 修复: 修改 Cypher 查询，不返回整个 relationship 对象，而是显式返回需要的属性字段

---

## 二、数据获取与分析

### 2.1 Tushare 数据获取
使用 tushare pro API 获取10家公司的财务和市场数据：
- `income` — 利润表（营收、净利润）
- `balancesheet` — 资产负债表
- `fina_indicator` — 财务指标（ROE、PE、PB 等）
- `daily_basic` — 市值数据
- `stock_company` — 公司详细信息

**发现**: `fina_mainbz`（主营业务构成）接口对这批公司无数据返回，可能受限于积分权限。最终分析主要依赖 `batch_001.json` 中的 `main_business` 和 `business_scope` 字段。

### 2.2 各公司产业分析摘要

| 公司 | 核心产业 | 原材料/输入 | 产出/服务 |
|---|---|---|---|
| 平安银行 | 金融服务 | 公众存款 | 贷款服务、同业拆借、债券投资 |
| 万科A | 房地产 | 土地、水泥、施工服务 | 商品住宅、商业地产、物业服务 |
| *ST国华 | 软件安全 | 操作系统、服务器、安全数据库 | 移动应用安全服务 |
| 深振业A | 房地产 | 土地、建筑材料 | 商品住宅、物业租赁 |
| 全新好 | 物业运营 | 物业资产 | 物业管理、房屋租赁 |
| 神州高铁 | 轨道交通 | 轨道车辆、信号系统、供电系统 | 轨道运维服务 |
| 中国宝安 | 新材料/新能源/生物医药/地产 | 天然石墨、针状焦、锂盐、硅材料 | 锂电池材料、光伏组件、药品、住宅 |
| *ST美丽 | 园林绿化 | 苗木、土壤、园艺材料 | 绿化施工、景观设计、生态修复 |
| 深物业A | 房地产 | 土地、建筑材料 | 商品住宅、物业管理 |
| 南玻A | 玻璃制造/新能源 | 石英砂、纯碱、天然气、硅材料 | 浮法玻璃、工程玻璃、电子玻璃、光伏玻璃、光伏组件 |

---

## 三、产业图构建（Neo4j）

### 3.1 新增节点（24个）

**金融服务（5个）**:
- `public_deposit` (material) — 公众存款
- `loan_service` (service) — 贷款服务
- `interbank_lending_service` (service) — 同业拆借服务
- `bond_investment_service` (service) — 债券投资服务
- `financial_bond` (component) — 金融债券

**房地产（7个）**:
- `land` (material) — 土地
- `residential_property` (component) — 商品住宅
- `commercial_property` (component) — 商业地产
- `property_management_service` (service) — 物业服务
- `housing_rental_service` (service) — 房屋租赁服务
- `construction_service` (service) — 建筑施工服务
- `cement` (material) — 水泥

**轨道交通（4个）**:
- `rail_vehicle` (device) — 轨道车辆
- `signaling_system` (subsystem) — 信号系统
- `power_supply_system` (subsystem) — 供电系统
- `rail_maintenance_service` (service) — 轨道运维服务

**园林绿化（6个）**:
- `nursery_stock` (material) — 苗木
- `soil` (material) — 土壤
- `gardening_material` (material) — 园艺材料
- `landscape_design_service` (service) — 景观设计服务
- `greening_construction_service` (service) — 绿化施工服务
- `ecological_restoration_service` (service) — 生态修复服务

**新能源（2个）**:
- `silicon_material` (material) — 硅材料
- `photovoltaic_module` (device) — 光伏组件

### 3.2 新增边（22条）

核心产业链关系：
- 金融链: `public_deposit` → `loan_service` / `interbank_lending_service` / `bond_investment_service`
- 房地产链: `land` → `residential_property` / `commercial_property`; `cement` → `construction_service` → `residential_property` / `commercial_property`
- 物业链: `residential_property` → `property_management_service` / `housing_rental_service`
- 轨道交通链: `rail_vehicle` / `signaling_system` / `power_supply_system` → `rail_maintenance_service`
- 园林绿化链: `nursery_stock` / `soil` / `gardening_material` / `landscape_design_service` → `greening_construction_service` → `ecological_restoration_service`
- 光伏链: `silicon_material` → `photovoltaic_module`; `pv_glass` → `photovoltaic_module` (composition)

### 3.3 已有节点复用
复用了现有图谱中的24个节点，包括：
- 石英砂、纯碱、天然气、浮法玻璃、工程玻璃、电子玻璃、光伏玻璃
- 天然石墨、针状焦、锂盐、锂电池负极、锂电池正极
- 操作系统、服务器硬件、安全数据库、移动应用安全服务
- 药品、医疗器械、医药分销、医药零售

### 3.4 构建后图谱统计
- **总节点**: 72（新增24，原有48）
- **总边**: 55（新增22，原有33）
- **节点类型分布**: material(22), service(19), component(15), device(9), subsystem(5), infrastructure(1), application_system(1)
- **边类型分布**: material_flow(21), service_flow(19), composition(9), capability_supply(4), information_flow(1), energy_flow(1)

---

## 四、行业过滤器配置（PostgreSQL）

配置了8个行业过滤器：

| industry_id | 名称 | 包含节点数 |
|---|---|---|
| banking | 银行业 | 5 |
| real_estate | 房地产业 | 7 |
| software_security | 软件与信息安全 | 5 |
| rail_transportation | 轨道交通 | 4 |
| landscaping | 园林绿化 | 6 |
| new_energy_materials | 新能源新材料 | 8 |
| biopharma | 生物医药 | 4 |
| glass_manufacturing | 玻璃制造 | 7 |

每个行业映射都配置了 `role`（节点角色）和 `weight`（重要性权重）。

---

## 五、公司视图构建（PostgreSQL）

### 5.1 公司基本信息
创建了10家公司的完整档案，包括：
- 基本信息：company_id, name_zh, name_en, stock_codes
- 地理信息：country(CN), province, city
- 财务信息：founded_year, employee_count, revenue_cny, market_cap_cny
- 公司类型：全部为 public（上市公司）

### 5.2 公司与产业节点暴露关系
创建了29条 `CompanyNodeExposure` 记录：

| 公司 | 暴露节点数 | 主要 activity_type |
|---|---|---|
| 平安银行 | 4 | provide_service, use |
| 万科A | 3 | produce, provide_service |
| *ST国华 | 1 | provide_service |
| 深振业A | 2 | produce, provide_service |
| 全新好 | 2 | provide_service |
| 神州高铁 | 1 | provide_service |
| 中国宝安 | 5 | manufacture, produce |
| *ST美丽 | 3 | provide_service |
| 深物业A | 2 | produce, provide_service |
| 南玻A | 6 | manufacture |

---

## 六、验证结果

### 6.1 产业图验证
- `GET /api/v1/query/stats` — 72节点/55边，全部 ACTIVE/HIGH
- `GET /api/v1/industries/{id}/subgraph` — 测试通过
  - banking: 5 nodes, 4 edges
  - real_estate: 7 nodes, 8 edges
  - landscaping: 6 nodes, 5 edges
- `GET /api/v1/companies/{id}/subgraph` — 测试通过
  - pingan_bank: 4 nodes, 3 edges
  - vanke: 3 nodes, 2 edges
  - csgholding: 6 nodes, 2 edges

### 6.2 数据库验证
- PostgreSQL 4张表数据完整
- 8 industries + 46 mappings
- 10 companies + 29 exposures

---

## 七、关键发现与启发

### 7.1 产业分析发现
1. **多元化集团需拆分暴露**: 中国宝安横跨新材料、新能源、生物医药、房地产四大产业，单一公司需要关联多个产业节点。
2. **产业链上下游清晰**: 南玻A的玻璃制造链（石英砂→纯碱→天然气→浮法玻璃→各类深加工玻璃）和中国宝安的锂电池材料链（天然石墨/针状焦→负极材料）形成了明确的上下游关系。
3. **服务业与制造业区分**: 平安银行、*ST国华、神州高铁等公司属于服务提供型（provide_service），南玻A、中国宝安属于制造型（manufacture），万科A等属于生产型（produce）。

### 7.2 系统设计启发
1. **Neo4j evidence 存储**: Neo4j 不支持嵌套 Map，evidence 必须以 JSON 字符串存储。从 Neo4j 读取时需反序列化。
2. **datetime 兼容性**: `neo4j.time.DateTime` 需通过 `.to_native()` 转为 Python `datetime`，否则 Pydantic 验证失败。
3. **Relationship 序列化**: `await result.data()` 会将 Neo4j Relationship 序列化为 tuple，子图查询应避免返回完整 relationship，而是显式返回属性。
4. **Schema 一致性**: `Industry` 和 `Company` schema 应保持一致性（如都包含 `aliases` 字段）。

### 7.3 数据质量启发
1. Tushare 的 `fina_mainbz`（主营构成）接口对低积分用户可能不可用，需要备选数据来源。
2. 上市公司的 `business_scope`（经营范围）字段是产业分析的重要信息源，但需人工提炼核心产业关系。
3. 对于 *ST 公司（如 *ST国华、*ST美丽），虽然存在退市风险，但其产业关系仍然有效。

---

## 八、待完善事项

1. **反向查询 API**: `/api/v1/companies/by-node/{node_id}` 端点未实现，无法通过产业节点反向查找公司。
2. **公司关系推断**: Phase 2 计划中提到的 `inferred_industrial_relation`、`evidenced_business_relation`、`similarity_or_peer_relation` 尚未实现。
3. **前端视图**: Industry List/Detail Page、Company List/Detail Page 尚未构建。
4. **数据更新机制**: 公司财务数据（revenue、market_cap）是静态快照，需设计定期更新机制。
