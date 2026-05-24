# UI 架构重构：从侧边栏模式到工作区模式

**日期**: 2026-05-24  
**作者**: Kimi Code CLI  
**状态**: 已完成

---

## 1. 背景与动机

### 原架构的问题

原前端架构将 **产业图**、**行业**、**公司** 作为同级顶级菜单：

```
[ 产业图 ] [ 行业 ] [ 公司 ]
```

在这种设计下：
- **认知混淆**: "行业"和"公司"不是视图，而是数据列表。用户点击后左侧显示列表，中间仍然是产业图。
- **视图切换嵌套过深**: 在公司视图下，又嵌套了 [关系网络] / [产业图] / [版本] 的切换，导致"我到底在看什么？"的困惑。
- **扩展性差**: 公司视图的新功能（版本管理、上下游分析）和产业图的逻辑纠缠在一起。

### 新架构的目标

将顶层菜单从 **"数据分类"** 切换为 **"工作区隔离"**：
- **产业图工作区**: 专注于 IndustrialNode + INDUSTRIAL_FLOW（产业本体）。
- **公司视图工作区**: 专注于 Company + INFERRED_UPSTREAM（企业供应链网络）。

两套视图完全隔离，各自拥有独立的左侧导航、中间画布和右侧详情面板。

---

## 2. 架构对比

### 2.1 原架构（Before）

```
顶部: [ 产业图 ] [ 行业 ] [ 公司 ]

产业图模式:
  左侧: FilterPanel
  中间: GraphCanvas（产业图）
  右侧: NodeDetail / EdgeDetail

行业模式:
  左侧: IndustrySidebar
  中间: GraphCanvas（产业图）
  右侧: IndustryDetail

公司模式:
  左侧: CompanySidebar
  中间: GraphCanvas（产业图） ← 或 CompanyNetworkCanvas（公司关系图）
  右侧: CompanyDetail / CompanyViewVersions（右侧面板）
  顶部 toolbar: [ 关系网络 ] [ 产业图 ] [ 版本 ]
```

### 2.2 新架构（After）

```
顶部: [ 产业图 ] [ 公司视图 ]

产业图工作区:
  顶部 Stats: [ 产业图 | 公司视图 ]  节点 426  关系 358
  左侧 Tab: [ 过滤 ] [ 行业 ] [ 公司 ]
    过滤 → FilterPanel
    行业 → IndustrySidebar
    公司 → CompanySidebar
  中间: GraphCanvas（始终为产业图）
  右侧: NodeDetail / EdgeDetail / IndustryDetail / CompanyDetail

公司视图工作区:
  顶部 Stats: [ 产业图 | 公司视图 ]  公司 200  推断关系 1142
  左侧 Tab: [ 版本 ] [ 公司列表 ]
    版本 → CompanyViewVersions（精简列表 + 重算按钮）
    公司列表 → CompanySidebar
  中间: CompanyNetworkCanvas（始终为公司关系网络）
  右侧: CompanyDetail
```

---

## 3. 状态模型变更

### 3.1 原状态

```typescript
type ViewMode = "graph" | "industries" | "companies";

const [viewMode, setViewMode] = useState<ViewMode>("graph");
const [companyNetworkVisible, setCompanyNetworkVisible] = useState(false);
```

### 3.2 新状态

```typescript
type MainView = "industrial_graph" | "company_graph";
type IndustrialSubView = "filter" | "industry" | "company";
type CompanySubView = "version" | "company_list";

const [mainView, setMainView] = useState<MainView>("industrial_graph");
const [industrialSubView, setIndustrialSubView] = useState<IndustrialSubView>("filter");
const [companySubView, setCompanySubView] = useState<CompanySubView>("version");
```

---

## 4. 文件变更清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `frontend/src/components/StatsBar.tsx` | 重写 | 顶级菜单改为 `[产业图 \| 公司视图]`；Stats 根据当前视图动态显示（节点/关系 vs 公司/推断关系） |
| `frontend/src/App.tsx` | 重写 | 状态机重构为工作区隔离模式；新增 `SubTab` 组件用于左侧二级导航 |
| `frontend/src/components/CompanyViewVersions.tsx` | 重写 | 从全宽表格改为紧凑型卡片列表，适配 w-56 侧边栏宽度；保留重算、删除、进度显示功能 |
| `docs/ui_architecture_refactor_2026-05-24.md` | 新增 | 本文档 |

---

## 5. 关键设计决策

### 5.1 为什么保留单一的 `rightPanel`？

两个工作区的右侧详情面板（NodeDetail、EdgeDetail、IndustryDetail、CompanyDetail）高度复用。通过 `panel` 状态统一控制，避免代码重复。

### 5.2 公司视图下的 "公司列表" 有什么作用？

在公司视图下点击左侧"公司列表"中的公司，右侧显示 **CompanyDetail**，同时中间的公司关系网络 **高亮该公司节点**。这与产业图下"公司"列表的行为对称（产业图下高亮的是该公司暴露的工业节点）。

### 5.3 CompanyViewVersions 为什么放在左侧而不是右侧？

为了保持两个工作区的 **布局对称性**：
- 产业图: 左侧导航 → 中间图 → 右侧详情
- 公司视图: 左侧导航 → 中间图 → 右侧详情

如果版本管理放在右侧，会破坏"左侧=导航/列表"的心智模型。因此将版本列表精简为卡片形式，适配窄侧边栏。

### 5.4 子导航 Tab 的样式

使用 **底部边框激活线**（`border-b-2 border-cyan-500`）而非填充色，与顶级菜单的填充按钮形成视觉层级区分：
- 顶级: 填充色块（重要）
- 二级: 下划线（次要）

---

## 6. 后续可扩展方向

### 产业图工作区
- **路径分析**: 新增左侧 Tab "路径"，支持起点-终点的产业路径搜索
- **冲突检测**: 新增左侧 Tab "冲突"，显示 PENDING/REJECTED 的节点和边
- **批量操作**: 在"过滤"Tab 中支持批量激活/归档节点

### 公司视图工作区
- **上下游分析**: CompanyDetail 中扩展为完整的上下游树（不仅直接邻居）
- **相似公司推荐**: 基于共享暴露节点推荐同行/竞争对手
- **时间轴**: 版本对比功能，查看两个版本之间关系网络的变化

---

## 7. 兼容性说明

- **后端 API 无变更**: 本次重构纯前端，所有 `/api/v1/*` 端点保持不变。
- **路由无变更**: 无 URL 路由变化，状态完全由 React 前端管理。
- **数据无变更**: Neo4j 和 PostgreSQL 中的数据不受影响。
