# 公司视图与行业视图设计方案

## 1. 核心概念

现有**产业视图**描述的是物料/技术/产品之间的**物理与技术关系**（供给侧技术链）。在此基础上，新增两个维度：

| 视图 | 粒度 | 核心问题 | 实体 |
|------|------|----------|------|
| **产业视图** | 中观 | "什么东西由什么东西组成/转化而来？" | 材料、设备、组件、系统 |
| **行业视图** | 宏观 | "这个行业包含哪些子行业？与哪些行业相邻？" | 行业、子行业 |
| **公司视图** | 微观 | "哪家公司生产什么？与谁竞争/合作？" | 公司、企业 |

三个视图之间的关系：

```
行业视图（Industry）          ← 宏观分类与关联
    │
    │ covers（覆盖）
    ▼
产业视图（IndustrialNode）     ← 已有：技术链与物料流
    │
    │ produced_by（由...生产）
    ▼
公司视图（Company）            ← 微观主体与商业关系
```

## 2. 新增数据模型

### 2.1 行业（Industry）

```python
class Industry(BaseModel):
    industry_id: str                    # 唯一标识，如 "solar_energy"
    name_zh: str
    name_en: Optional[str] = None
    aliases: List[str] = []
    definition: str
    
    # 层级
    parent_industry: Optional[str] = None   # 父行业ID，如 "new_energy"
    industry_level: int = 1                 # 层级：1=一级行业，2=二级...
    
    # 规模与指标
    market_size_usd: Optional[float] = None
    china_market_share: Optional[float] = None   # 0.0~1.0
    annual_growth_rate: Optional[float] = None   # 如 0.15 表示 15%
    key_metrics: List[str] = []                  # ["装机量", "组件产量"]
    
    # 元数据
    evidence: List[Evidence] = []
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.ACTIVE
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### 2.2 公司（Company）

```python
class Company(BaseModel):
    company_id: str                     # 唯一标识，如 "longi_green_energy"
    name_zh: str
    name_en: Optional[str] = None
    aliases: List[str] = []             # ["隆基", "隆基股份"]
    
    # 资本市场
    ticker: Optional[str] = None        # "601012.SH"
    stock_exchange: Optional[str] = None
    
    # 基本信息
    country: str                        # "CN"
    province: Optional[str] = None
    city: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    
    # 财务（可选，支持年度快照）
    revenue_cny: Optional[float] = None         # 年度营收（人民币）
    market_cap_cny: Optional[float] = None      # 市值
    net_profit_cny: Optional[float] = None
    
    # 分类
    company_type: CompanyType           # public / private / state_owned / joint_venture
    status: NodeStatus = NodeStatus.ACTIVE
    
    # 元数据
    evidence: List[Evidence] = []
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CompanyType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    STATE_OWNED = "state_owned"
    JOINT_VENTURE = "joint_venture"
    FOREIGN_INVESTED = "foreign_invested"
```

## 3. 新增关系类型

### 3.1 行业-行业关系

| 边类型 | 命名空间 | 方向 | 语义 |
|--------|----------|------|------|
| `is_sub_industry_of` | `industry_hierarchy` | 子行业 → 父行业 | "硅片子行业属于光伏行业" |
| `is_adjacent_to` | `industry_hierarchy` | 双向 | "光伏行业与风电行业相邻" |
| `is_upstream_of` | `industry_hierarchy` | 上游 → 下游 | "硅料行业是硅片行业的上游" |

### 3.2 公司-行业关系

| 边类型 | 命名空间 | 方向 | 语义 |
|--------|----------|------|------|
| `belongs_to` | `company_industry` | 公司 → 行业 | "隆基绿能属于光伏行业" |
| `is_leader_in` | `company_industry` | 公司 → 行业 | "隆基绿能是硅片行业的龙头" |
| `is_new_entrant_to` | `company_industry` | 公司 → 行业 | "某某公司新进入光伏行业" |

### 3.3 公司-产业节点关系（最关键）

| 边类型 | 命名空间 | 方向 | 语义 |
|--------|----------|------|------|
| `produces` | `company_product` | 公司 → 产业节点 | "隆基绿能生产单晶硅片" |
| `uses_technology` | `company_product` | 公司 → 产业节点 | "隆基绿能使用单晶拉棒技术" |
| `develops` | `company_product` | 公司 → 产业节点 | "宁德时代研发固态电池" |

### 3.4 公司-公司关系

| 边类型 | 命名空间 | 方向 | 语义 |
|--------|----------|------|------|
| `supplies_to` | `company_business` | 供应商 → 客户 | "通威股份供应多晶硅给隆基绿能" |
| `competes_with` | `company_business` | 双向 | "隆基绿能与TCL中环竞争" |
| `partners_with` | `company_business` | 双向 | "宁德时代与特斯拉合作" |
| `invests_in` | `company_business` | 投资方 → 被投方 | "高瓴资本投资宁德时代" |
| `acquires` | `company_business` | 收购方 → 被收购方 | "A公司收购B公司" |
| `is_subsidiary_of` | `company_business` | 子公司 → 母公司 | "比亚迪半导体是比亚迪子公司" |

## 4. 视图映射规则

### 4.1 行业 → 产业（覆盖关系）

一个行业覆盖一组产业节点。例如：

```
光伏行业（solar_energy）
  covers:
    - polysilicon（多晶硅）
    - monocrystalline_silicon_ingot（单晶硅棒）
    - silicon_wafer（硅片）
    - solar_cell（太阳能电池片）
    - solar_module（光伏组件）
    - inverter（逆变器）
    - photovoltaic_power_station（光伏电站）
```

**实现方式**：不存储为图边（因为一对多太稀疏），而是作为 `Industry` 节点的 `covered_nodes: List[str]` 属性。查询时通过 node_id 关联。

### 4.2 公司 → 产业（生产关系）

一家公司可以生产多个产业节点的产品：

```
隆基绿能（longi）
  produces:
    - monocrystalline_silicon_ingot（单晶硅棒）
    - silicon_wafer（硅片）
    - solar_cell（电池片）
    - solar_module（组件）
```

**实现方式**：存储为 `company_product` 命名空间的 `produces` 边。

### 4.3 公司 → 行业（归属关系）

一家公司可以属于多个行业：

```
比亚迪（byd）
  belongs_to:
    - new_energy_vehicle（新能源汽车行业）
    - power_battery（动力电池行业）
    - automotive_electronics（汽车电子行业）
```

## 5. 新增 API 设计

### 5.1 行业 CRUD

```
GET    /api/v1/industries              # 行业列表（分页、层级过滤）
POST   /api/v1/industries              # 创建行业
GET    /api/v1/industries/{id}         # 行业详情
PUT    /api/v1/industries/{id}         # 更新行业
DELETE /api/v1/industries/{id}         # 删除行业
```

### 5.2 公司 CRUD

```
GET    /api/v1/companies               # 公司列表（分页、行业过滤、搜索）
POST   /api/v1/companies               # 创建公司
GET    /api/v1/companies/{id}          # 公司详情
PUT    /api/v1/companies/{id}          # 更新公司
DELETE /api/v1/companies/{id}          # 删除公司
```

### 5.3 复合查询（核心）

```
GET /api/v1/industries/{id}/landscape
# 返回行业全景：
# {
#   industry: Industry,
#   sub_industries: [Industry],
#   companies: [Company],
#   covered_nodes: [IndustrialNode],
#   upstream_industries: [Industry],
#   downstream_industries: [Industry]
# }

GET /api/v1/companies/{id}/portfolio
# 返回公司产品组合：
# {
#   company: Company,
#   produces: [IndustrialNode],
#   develops: [IndustrialNode],
#   industries: [Industry]
# }

GET /api/v1/companies/{id}/ecosystem
# 返回公司商业生态：
# {
#   company: Company,
#   suppliers: [{company: Company, product: IndustrialNode}],
#   customers: [{company: Company, product: IndustrialNode}],
#   competitors: [Company],
#   partners: [Company]
# }

GET /api/v1/query/company_supply_chain?company_id=xxx&depth=2
# 从一家公司出发，展开供应链：
# 包含 company_business 边 + industrial_flow 边的混合路径
```

## 6. 前端设计

### 6.1 视图切换器

顶部栏增加三段式切换：

```
[产业视图]  [行业视图]  [公司视图]
```

### 6.2 行业视图

**布局**：左侧行业树 + 右侧详情面板

- **行业树**：可折叠的树形结构，展示行业层级
  - 一级行业：能源、半导体、汽车...
  - 二级行业：光伏、风电、锂电...
  - 三级行业：硅料、硅片、电池片...
- **点击行业**：右侧显示
  - 行业基本信息（规模、增速、关键指标）
  - 覆盖的产业节点列表（点击可跳转到产业视图）
  - 行业内的龙头公司列表
  - 上下游行业关联图

### 6.3 公司视图

**布局**：搜索/筛选栏 + 图画布 + 右侧面板

- **节点渲染**：
  - 公司节点：圆形，大小映射市值/营收，颜色映射行业
  - 产业节点：六边形（与产业视图区分），半透明，悬浮在公司节点周围
- **边渲染**：
  - `supplies_to`：实线箭头，标注产品名称
  - `competes_with`：红色虚线
  - `partners_with`：绿色虚线
  - `produces`：公司 → 产品，灰色细线
- **交互**：
  - 点击公司：显示公司详情（财务、产品组合、供应链）
  - 双击公司：展开该公司的供应商和客户
  - 悬浮在公司上：高亮其所有产品和关系
- **筛选**：
  - 按行业筛选公司
  - 按关系类型筛选边
  - 按营收规模筛选（滑块）
  - 仅显示上市公司

### 6.4 跨视图联动

```
行业视图点击"硅片"产业节点
  → 自动切换到产业视图，定位并高亮"硅片"节点

产业视图点击"硅片"节点
  → 右键菜单："查看生产硅片的公司"
  → 切换到公司视图，筛选 produces=硅片 的公司

公司视图点击隆基绿能
  → 查看其产品组合
  → 点击"单晶硅片"
  → 切换到产业视图，高亮"单晶硅片"及其上下游
```

## 7. 数据示例

### 7.1 行业数据

```json
{
  "industry_id": "solar_energy",
  "name_zh": "光伏行业",
  "name_en": "Solar Energy Industry",
  "aliases": ["光伏发电", "太阳能发电"],
  "definition": "利用光伏效应将太阳能直接转化为电能的产业，涵盖硅料、硅片、电池片、组件、逆变器及电站运营。",
  "parent_industry": "new_energy",
  "industry_level": 2,
  "market_size_usd": 500000000000,
  "china_market_share": 0.85,
  "annual_growth_rate": 0.20,
  "key_metrics": ["全球光伏装机量(GW)", "中国组件产量(GW)", "硅料均价(元/kg)"],
  "evidence": [...],
  "confidence": "HIGH",
  "status": "ACTIVE"
}
```

### 7.2 公司数据

```json
{
  "company_id": "longi_green_energy",
  "name_zh": "隆基绿能科技股份有限公司",
  "name_en": "LONGi Green Energy Technology Co., Ltd.",
  "aliases": ["隆基绿能", "隆基", "隆基股份"],
  "ticker": "601012.SH",
  "stock_exchange": "上海证券交易所",
  "country": "CN",
  "province": "陕西",
  "city": "西安",
  "founded_year": 2000,
  "employee_count": 60000,
  "revenue_cny": 128998000000,
  "market_cap_cny": 150000000000,
  "company_type": "public",
  "status": "ACTIVE",
  "evidence": [
    {
      "source_title": "隆基绿能2023年年度报告",
      "source_url": "...",
      "quote": "公司实现营业收入1289.98亿元..."
    }
  ]
}
```

### 7.3 公司-产业关系

```json
{
  "edge_namespace": "company_product",
  "edge_type": "produces",
  "edge_id": "longi_produces_wafer",
  "from_node": "longi_green_energy",
  "to_node": "silicon_wafer",
  "description": "隆基绿能是全球最大的单晶硅片生产商，2023年硅片出货量超过100GW。",
  "attributes": {
    "capacity_gw": 190,
    "market_share_percent": 35,
    "is_core_business": true
  },
  "evidence": [...],
  "confidence": "HIGH"
}
```

### 7.4 公司-公司关系

```json
{
  "edge_namespace": "company_business",
  "edge_type": "supplies_to",
  "edge_id": "tongwei_supplies_longi",
  "from_node": "tongwei_co",
  "to_node": "longi_green_energy",
  "description": "通威股份向隆基绿能供应多晶硅料，是隆基的核心供应商之一。",
  "attributes": {
    "product": "polysilicon",
    "contract_value_cny": null,
    "relationship_type": "strategic"
  },
  "evidence": [...],
  "confidence": "HIGH"
}
```

## 8. 实施优先级

### Phase 1：基础模型 + 公司视图（1-2 周）
1. Schema 扩展：`Company` + `company_product` 边
2. Neo4j 存储层扩展
3. API：`/companies` CRUD + `/companies/{id}/portfolio`
4. 前端：公司视图基础渲染（节点 + produces 边）
5. Seed 数据：10-15 家龙头公司 + 其与产业节点的 produces 关系

### Phase 2：行业模型 + 视图切换（1 周）
1. Schema 扩展：`Industry` + `industry_hierarchy` 边
2. API：`/industries` CRUD + `/industries/{id}/landscape`
3. 前端：行业树 + 视图切换器
4. Seed 数据：5-8 个一级行业 + 15-20 个二级行业

### Phase 3：商业关系 + 复合查询（1-2 周）
1. Schema 扩展：`company_business` 边（supplies_to / competes_with / partners_with）
2. API：`/companies/{id}/ecosystem` + `/query/company_supply_chain`
3. 前端：公司生态图（供应商/客户/竞争/合作）
4. Seed 数据：20-30 条公司间关系

## 9. 设计原则延续

| 原则 | 在本设计中的体现 |
|------|-----------------|
| 事实只有一份 | 产业节点（硅片）只有一个，隆基"生产"它而不是重新定义一个"隆基硅片" |
| 分类不是关系 | `company_type`（public/private）是公司属性，不建边 |
| 方向统一 | `supplies_to` 统一为 供应商→客户，`is_sub_industry_of` 统一为 子→父 |
| 证据驱动 | 公司财务数据、市场份额、供应关系都必须有 evidence |
| 可扩展 | `attributes` 字典支持各关系类型的自定义字段，不改 Schema 即可扩展 |
