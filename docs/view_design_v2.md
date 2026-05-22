# 公司视图与行业视图 — 可执行设计

基于现有产业视图，向下扩展公司层、向上扩展行业层。所有新增模型与现有 `IndustrialNode` / `GraphEdge` 零冲突。

---

## 一、数据模型（Schema 代码）

### 1.1 行业 Industry

```python
# backend/app/models/schemas.py

class Industry(BaseModel):
    """宏观行业分类节点"""
    industry_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$", min_length=3)
    name_zh: str
    name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    definition: str

    parent_industry: Optional[str] = None          # 父行业ID，null表示一级行业
    industry_level: int = Field(default=1, ge=1)   # 层级深度

    market_size_usd: Optional[float] = None
    china_market_share: Optional[float] = Field(None, ge=0, le=1)
    annual_growth_rate: Optional[float] = None
    key_metrics: List[str] = Field(default_factory=list)

    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.ACTIVE
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("name_zh", "definition")
    @classmethod
    def non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("cannot be empty")
        return v


class IndustryCreate(BaseModel):
    industry_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$", min_length=3)
    name_zh: str
    name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    definition: str
    parent_industry: Optional[str] = None
    market_size_usd: Optional[float] = None
    china_market_share: Optional[float] = None
    annual_growth_rate: Optional[float] = None
    key_metrics: List[str] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.PENDING
    notes: Optional[str] = None


class IndustryUpdate(BaseModel):
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    aliases: Optional[List[str]] = None
    definition: Optional[str] = None
    parent_industry: Optional[str] = None
    market_size_usd: Optional[float] = None
    china_market_share: Optional[float] = None
    annual_growth_rate: Optional[float] = None
    key_metrics: Optional[List[str]] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    status: Optional[NodeStatus] = None
    notes: Optional[str] = None
```

### 1.2 公司 Company

```python
class CompanyType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    STATE_OWNED = "state_owned"
    JOINT_VENTURE = "joint_venture"
    FOREIGN_INVESTED = "foreign_invested"


class Company(BaseModel):
    """微观企业主体节点"""
    company_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$", min_length=3)
    name_zh: str
    name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)

    ticker: Optional[str] = None
    stock_exchange: Optional[str] = None

    country: str = "CN"
    province: Optional[str] = None
    city: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = Field(None, ge=0)

    revenue_cny: Optional[float] = None
    market_cap_cny: Optional[float] = None
    net_profit_cny: Optional[float] = None

    company_type: CompanyType = CompanyType.PRIVATE
    status: NodeStatus = NodeStatus.ACTIVE

    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CompanyCreate(BaseModel):
    company_id: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$", min_length=3)
    name_zh: str
    name_en: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    ticker: Optional[str] = None
    stock_exchange: Optional[str] = None
    country: str = "CN"
    province: Optional[str] = None
    city: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    revenue_cny: Optional[float] = None
    market_cap_cny: Optional[float] = None
    net_profit_cny: Optional[float] = None
    company_type: CompanyType = CompanyType.PRIVATE
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    status: NodeStatus = NodeStatus.PENDING
    notes: Optional[str] = None


class CompanyUpdate(BaseModel):
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    aliases: Optional[List[str]] = None
    ticker: Optional[str] = None
    stock_exchange: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    revenue_cny: Optional[float] = None
    market_cap_cny: Optional[float] = None
    net_profit_cny: Optional[float] = None
    company_type: Optional[CompanyType] = None
    evidence: Optional[List[Evidence]] = None
    confidence: Optional[Confidence] = None
    status: Optional[NodeStatus] = None
    notes: Optional[str] = None
```

### 1.3 新增边类型

```python
# 行业层级边
class IndustryHierarchyEdge(BaseModel):
    edge_id: str
    from_industry: str
    to_industry: str
    edge_type: Literal["is_sub_industry_of", "is_adjacent_to", "is_upstream_of"]
    description: str
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# 公司-产业边
class CompanyProductEdge(BaseModel):
    edge_id: str
    from_company: str
    to_node: str                        # 指向 IndustrialNode
    edge_type: Literal["produces", "uses_technology", "develops"]
    description: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    # attributes 示例: {"capacity_gw": 190, "market_share_percent": 35, "is_core_business": true}
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# 公司-公司商业边
class CompanyBusinessEdge(BaseModel):
    edge_id: str
    from_company: str
    to_company: str
    edge_type: Literal[
        "supplies_to", "competes_with", "partners_with",
        "invests_in", "acquires", "is_subsidiary_of"
    ]
    description: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    # attributes 示例: {"product": "polysilicon", "relationship_type": "strategic"}
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# 公司-行业边
class CompanyIndustryEdge(BaseModel):
    edge_id: str
    from_company: str
    to_industry: str
    edge_type: Literal["belongs_to", "is_leader_in", "is_new_entrant_to"]
    description: str
    evidence: List[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

---

## 二、Neo4j 存储设计

### 2.1 节点标签

```cypher
// 行业节点
(:Industry {industry_id, name_zh, name_en, ...})

// 公司节点
(:Company {company_id, name_zh, name_en, ticker, country, ...})

// 现有产业节点（不变）
(:IndustrialNode {node_id, ...})
```

### 2.2 关系类型

```cypher
// 行业层级
(ind:Industry)-[:IS_SUB_INDUSTRY_OF {edge_id, description, ...}]->(parent:Industry)
(ind1:Industry)-[:IS_ADJACENT_TO {edge_id, ...}]-(ind2:Industry)
(ind1:Industry)-[:IS_UPSTREAM_OF {edge_id, ...}]->(ind2:Industry)

// 公司-产业
(com:Company)-[:PRODUCES {edge_id, attributes, ...}]->(n:IndustrialNode)
(com:Company)-[:USES_TECHNOLOGY {edge_id, ...}]->(n:IndustrialNode)
(com:Company)-[:DEVELOPS {edge_id, ...}]->(n:IndustrialNode)

// 公司-公司
(c1:Company)-[:SUPPLIES_TO {edge_id, attributes, ...}]->(c2:Company)
(c1:Company)-[:COMPETES_WITH {edge_id, ...}]-(c2:Company)
(c1:Company)-[:PARTNERS_WITH {edge_id, ...}]-(c2:Company)
(c1:Company)-[:INVESTS_IN {edge_id, ...}]->(c2:Company)
(c1:Company)-[:ACQUIRES {edge_id, ...}]->(c2:Company)
(c1:Company)-[:IS_SUBSIDIARY_OF {edge_id, ...}]->(c2:Company)

// 公司-行业
(com:Company)-[:BELONGS_TO {edge_id, ...}]->(ind:Industry)
(com:Company)-[:IS_LEADER_IN {edge_id, ...}]->(ind:Industry)
```

### 2.3 关键 Cypher 查询

```cypher
// 查询某行业的全景：子行业 + 覆盖的产业节点 + 龙头公司
MATCH (ind:Industry {industry_id: $industry_id})
OPTIONAL MATCH (sub:Industry)-[:IS_SUB_INDUSTRY_OF]->(ind)
OPTIONAL MATCH (com:Company)-[:BELONGS_TO]->(ind)
OPTIONAL MATCH (com_leader:Company)-[:IS_LEADER_IN]->(ind)
OPTIONAL MATCH (n:IndustrialNode)
  WHERE n.node_id IN ind.covered_nodes
RETURN ind, collect(DISTINCT sub) AS sub_industries,
       collect(DISTINCT com) AS companies,
       collect(DISTINCT com_leader) AS leaders,
       collect(DISTINCT n) AS covered_nodes

// 查询某公司的产品组合
MATCH (com:Company {company_id: $company_id})
OPTIONAL MATCH (com)-[r:PRODUCES|USES_TECHNOLOGY|DEVELOPS]->(n:IndustrialNode)
RETURN com, collect({edge: r, node: n}) AS portfolio

// 查询某公司的商业生态（供应商+客户+竞争对手）
MATCH (com:Company {company_id: $company_id})
OPTIONAL MATCH (com)-[r1:SUPPLIES_TO]->(customer:Company)
OPTIONAL MATCH (supplier:Company)-[r2:SUPPLIES_TO]->(com)
OPTIONAL MATCH (com)-[r3:COMPETES_WITH]-(competitor:Company)
OPTIONAL MATCH (com)-[r4:PARTNERS_WITH]-(partner:Company)
RETURN com,
       collect(DISTINCT {company: customer, relation: r1}) AS customers,
       collect(DISTINCT {company: supplier, relation: r2}) AS suppliers,
       collect(DISTINCT {company: competitor, relation: r3}) AS competitors,
       collect(DISTINCT {company: partner, relation: r4}) AS partners

// 从一家公司出发，展开混合供应链（公司商业关系 + 产业物料流）
MATCH path = (com:Company {company_id: $company_id})
  -[:PRODUCES]->(:IndustrialNode)
  -[:MATERIAL_FLOW|COMPOSITION*1..3]->(:IndustrialNode)
  <-[:PRODUCES]-(:Company)
RETURN path
LIMIT 50
```

---

## 三、API 路由设计

```python
# backend/app/routers/industries.py
router = APIRouter(prefix="/industries", tags=["industries"])

@router.post("", response_model=Industry, status_code=201)
async def create_industry(data: IndustryCreate): ...

@router.get("", response_model=PaginatedIndustries)
async def list_industries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    parent_industry: Optional[str] = None,
    search: Optional[str] = None,
): ...

@router.get("/{industry_id}", response_model=Industry)
async def get_industry(industry_id: str): ...

@router.put("/{industry_id}", response_model=Industry)
async def update_industry(industry_id: str, data: IndustryUpdate): ...

@router.delete("/{industry_id}", status_code=204)
async def delete_industry(industry_id: str): ...

@router.get("/{industry_id}/landscape")
async def get_industry_landscape(industry_id: str):
    """返回行业全景：子行业、公司、覆盖的产业节点"""
    ...

@router.get("/{industry_id}/companies")
async def get_industry_companies(industry_id: str): ...
```

```python
# backend/app/routers/companies.py
router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("", response_model=Company, status_code=201)
async def create_company(data: CompanyCreate): ...

@router.get("", response_model=PaginatedCompanies)
async def list_companies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    industry: Optional[str] = None,
    country: Optional[str] = None,
    company_type: Optional[str] = None,
    search: Optional[str] = None,
): ...

@router.get("/{company_id}", response_model=Company)
async def get_company(company_id: str): ...

@router.put("/{company_id}", response_model=Company)
async def update_company(company_id: str, data: CompanyUpdate): ...

@router.delete("/{company_id}", status_code=204)
async def delete_company(company_id: str): ...

@router.get("/{company_id}/portfolio")
async def get_company_portfolio(company_id: str):
    """公司产品组合：produces + uses_technology + develops"""
    ...

@router.get("/{company_id}/ecosystem")
async def get_company_ecosystem(company_id: str):
    """商业生态：供应商、客户、竞争对手、合作伙伴"""
    ...
```

```python
# backend/app/routers/query.py 扩展

@router.get("/company_supply_chain")
async def query_company_supply_chain(
    company_id: str,
    depth: int = Query(2, ge=1, le=5),
):
    """从一家公司出发，展开混合供应链
    
    路径：Company -(produces)-> IndustrialNode -(material_flow/composition)-> ...
          <-(produces)- Company
    """
    ...
```

---

## 四、前端设计

### 4.1 类型扩展

```typescript
// frontend/src/types/index.ts

export interface Industry {
  industry_id: string;
  name_zh: string;
  name_en?: string;
  aliases: string[];
  definition: string;
  parent_industry?: string;
  industry_level: number;
  market_size_usd?: number;
  china_market_share?: number;
  annual_growth_rate?: number;
  key_metrics: string[];
  evidence: Evidence[];
  confidence: Confidence;
  status: NodeStatus;
  notes?: string;
}

export interface Company {
  company_id: string;
  name_zh: string;
  name_en?: string;
  aliases: string[];
  ticker?: string;
  stock_exchange?: string;
  country: string;
  province?: string;
  city?: string;
  founded_year?: number;
  employee_count?: number;
  revenue_cny?: number;
  market_cap_cny?: number;
  net_profit_cny?: number;
  company_type: CompanyType;
  status: NodeStatus;
  evidence: Evidence[];
  confidence: Confidence;
  notes?: string;
}

export type CompanyType =
  | "public"
  | "private"
  | "state_owned"
  | "joint_venture"
  | "foreign_invested";

export type ViewMode = "industry" | "industrial" | "company";
```

### 4.2 视图切换器（App.tsx 改造）

```tsx
// 顶部栏增加视图切换
<div className="flex items-center gap-1 rounded bg-slate-800 p-0.5">
  {(["industry", "industrial", "company"] as ViewMode[]).map((m) => (
    <button
      key={m}
      onClick={() => setViewMode(m)}
      className={cn(
        "rounded px-3 py-1 text-xs font-medium transition",
        viewMode === m
          ? "bg-cyan-600 text-white"
          : "text-slate-400 hover:text-slate-200"
      )}
    >
      {m === "industry" ? "行业视图" : m === "industrial" ? "产业视图" : "公司视图"}
    </button>
  ))}
</div>
```

### 4.3 行业视图组件

```
IndustryView
├── IndustryTree          # 左侧可折叠行业树
│   └── 层级：能源 > 新能源 > 光伏 > 硅料
├── IndustryDetailPanel   # 右侧详情
│   ├── 基本信息（规模、增速、关键指标）
│   ├── CoveredNodesList  # 覆盖的产业节点（点击跳转产业视图）
│   ├── CompanyRanking    # 行业龙头公司列表
│   └── AdjacentIndustries # 相邻行业图
└── 点击产业节点 → 自动切换到产业视图并高亮
```

### 4.4 公司视图组件

```
CompanyView
├── CompanySearchBar      # 搜索 + 行业筛选 + 规模滑块
├── CompanyGraphCanvas    # Cytoscape 画布
│   ├── 节点：Company（圆形，大小映射市值/营收）
│   ├── 节点：IndustrialNode（六边形，半透明，悬浮显示）
│   ├── 边：supplies_to（实线箭头，标注产品）
│   ├── 边：competes_with（红色虚线）
│   ├── 边：partners_with（绿色虚线）
│   ├── 边：produces（灰色细线，公司→产品）
│   └── 布局：力导向 + 手动拖拽
├── CompanyDetailPanel    # 右侧面板
│   ├── 基本信息 + 财务
│   ├── PortfolioTable    # 产品组合表格
│   ├── EcosystemTabs     # 供应商/客户/竞争/合作
│   └── 点击产品 → 跳转产业视图
└── 双击公司 → 展开其供应商和客户
```

### 4.5 跨视图联动

```typescript
// 产业视图右键菜单扩展
const nodeContextMenu = [
  { label: "查看详情", action: "detail" },
  { label: "展开邻接", action: "expand" },
  { label: "查看生产该产品的公司", action: "view_producers" },  // 新增
];

// view_producers 动作
function viewProducers(nodeId: string) {
  setViewMode("company");
  setCompanyFilters({ producesNodeId: nodeId });
}

// 行业视图点击产业节点
function onIndustryNodeClick(nodeId: string) {
  setViewMode("industrial");
  setHighlightNodeId(nodeId);
}
```

---

## 五、实施顺序（推荐）

### Week 1：Company + produces 边
1. `schemas.py` 增加 `Company`, `CompanyCreate`, `CompanyUpdate`
2. `neo4j_storage.py` 增加 Company CRUD
3. `companies.py` 路由（基础 CRUD）
4. `companies.py` 路由（`/portfolio` 复合查询）
5. 前端：`CompanyView` 基础框架 + `produces` 边渲染
6. Seed 数据：10 家龙头公司 + produces 关系

### Week 2：Industry + 视图切换
1. `schemas.py` 增加 `Industry`, `IndustryCreate`, `IndustryUpdate`
2. `neo4j_storage.py` 增加 Industry CRUD
3. `industries.py` 路由（含 `/landscape`）
4. 前端：`IndustryView` + `ViewModeSwitcher`
5. Seed 数据：8 个一级行业 + 15 个二级行业

### Week 3：Company 商业关系 + 生态图
1. `schemas.py` 增加 `CompanyBusinessEdge`
2. `neo4j_storage.py` 增加商业边 CRUD
3. `companies.py` 路由（`/ecosystem`）
4. `query.py` 扩展（`/company_supply_chain`）
5. 前端：生态图渲染（供应商/客户/竞争/合作）
6. Seed 数据：20-30 条公司间关系
