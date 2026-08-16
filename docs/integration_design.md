# Arachne 嵌入与集成设计

> 本文档记录「把 Arachne 集成到其它系统、并只暴露部分能力」的**设计思想与决策依据**。
> 操作步骤与契约字段见 `docs/integration-guide.md`（怎么做）；本文回答**为什么这么做**。
> 相关实现：commit `952a236`（JWT + 默认只读 + 只读 UI + 集成指南）、`3b49b7e`（JWT local bypass）。

---

## 1. 要解决的问题

Arachne 是完整的图谱系统（浏览 + 编辑 + 推理），但集成方往往只要其中一小块能力，
比如「在我们的页面里展示一次产业推演」，甚至「只展示推演结论，不要任何交互」。

设计目标：

1. **可按粒度裁剪暴露面**：从整个 App 到单次推理结果，集成方各取所需。
2. **安全默认值**：未做任何鉴权配置时，暴露出去的界面/接口天然无害（只读）。
3. **Arachne 为集成权威方**：集成契约由 Arachne 自己发布，集成方自取，不靠口口相传。
4. **集成不改主体**：主应用的浏览/编辑能力不受嵌入场景影响，靠权限模型收敛而非拆代码。

## 2. 核心思想：三级暴露粒度

| 粒度 | 载体 | 集成方得到什么 | 推理是否实时 |
|---|---|---|---|
| 交互式推演 | `embed.html?seed=...&engine=...` | 嵌入式推理视图（可调深度/方向/引擎，均为只读操作） | 实时 |
| 固定推演结果 | `embed.html?view=<view_id>`（published view + `result_snapshot`） | 一个稳定短链接，直接渲染缓存结论 | 否（快照，`refresh=1` 可强制重算） |
| 纯数据 | `POST /api/v1/reasoning/execute` | JSON 结果（temporary_graph/paths/scores/company_exposures），UI 完全自绘 | 实时 |

要点：

- **embed 是独立前端入口**（`embed.html` → `src/embed.tsx` → `EmbedReasoningPage`），
  不加载主应用的浏览/编辑外壳。这从构建层面保证了「嵌出去的东西里没有编辑功能」，
  不依赖运行时隐藏按钮的可靠性。
- **published view 解决的是 URL 稳定性与免重算**：报告/仪表盘场景需要链接长期有效且
  打开即得；`result_snapshot` 把推理结果固化为内容，`view_id` 把参数固化为引用。
- **reasoning API 在只读白名单内**：推理是纯计算、不写库，因此归入 read_only 也可用的
  POST（`read_only_post_paths`），让「只嵌数据」的集成方完全绕开鉴权。

## 3. 权限模型：默认只读（secure by default）

核心决策：**无 token / 无效 token / 过期 token 一律降级为 `read_only`，而不是拒绝服务**。

理由：

- 嵌入场景的第一要求是「嵌进去就能用」。如果默认拒绝，每个集成方都必须先完成
  JWT 对接才能看到任何内容，集成摩擦过大。
- 只读态下所有写端点返回 403，推理/查询不受影响——泄露风险≈公开只读数据，
  这在系统定位（产业知识图谱）下是可接受的暴露面。
- 权限升级（→ `read_write`）才是需要证明身份的事，因此只有升级需要 JWT。

配套机制：

- `X-Arachne-Scope` 响应头让前端自己收敛 UI（主界面 `AuthContext` 轮询
  `/api/v1/auth/scope`，只读时通过 `data-write-only` + CSS 隐藏全部写操作按钮）——
  **只读控制由 Arachne 自己完成，集成方前端零成本**。
- `AUTH_MODE` 三档：`disabled`（单机/开发，全放开）、`header`（受信上游系统注入
  scope 头）、`jwt`（生产集成）。

### 3.1 JWT local bypass 决策（commit `3b49b7e`）

`AUTH_MODE=jwt` 时，来自本地/私有 IP 的请求默认获得 `read_write`
（`JWT_LOCAL_BYPASS=true`），保证系统管理员独立运维 Arachne 时无需给自己签 token。

**已知陷阱**：nginx 反代场景所有请求的源 IP 都是本机，bypass 会让鉴权形同虚设，
因此集成部署**必须显式设 `JWT_LOCAL_BYPASS=false`**。该注意事项同时写在
integration-guide 的环境变量表与正文中（属于「最容易配错的一项」）。

### 3.2 `/integration/config` 的访问限制

集成清单端点**故意不放在 `/api/v1` 下、不进 OpenAPI、只接受本地/私有 IP**：
它是给「部署在同一信任域的集成方运维/AI 代理」看的，包含 JWKS URL、issuer 等
安全契约细节，不应成为公网可枚举的攻击面信息。

## 4. 嵌入页的 token 注入

iframe 跨域拿不到父页面的登录态，设计两条注入通道：

1. `postMessage`（`{type: "arachne-token", token}`）——父页面持有 JWT 时主动推送；
2. nginx 设置 httpOnly cookie——嵌入页请求同源代理路径时自动携带。

两者都避免把 token 放进嵌入 URL（URL 会进日志/历史记录，token 不应出现在其中）。

## 5. 与其他文档/模块的关系

- `docs/integration-guide.md`：操作手册（步骤、契约字段、检查清单），本文的上手指引。
- `docs/reasoning_page_design.md`：主应用 `/reasoning` 页的信息架构；embed 页复用同一套
  推理 API 与结果信封（ReasoningResultEnvelope），但信息架构独立（无左栏四步，直接结果）。
- `backend/app/auth.py`：scope 解析与 JWT 验签（JWKS 缓存、kid 轮换自动刷新）。
- `backend/app/routers/integration.py`：`/integration/config` 清单端点。
- `backend/app/routers/published_views.py`：published view 的创建/读取/过期。

## 6. 刻意的取舍（trade-offs）

- **不做细粒度数据级授权**（如按行业/节点授权）：scope 只有 `read_only` / `read_write`
  两档。产业图谱数据在系统定位下属可公开只读，过早引入行列级权限会显著抬高
  集成与运维成本。若未来出现敏感数据，应在数据入口侧分级，而不是在推理出口侧补洞。
- **快照不过期强一致**：`result_snapshot` 是内容缓存，图数据演进后快照可能变旧；
  提供 `refresh=1` 重算 + 视图自动过期机制，而非实时失效广播——嵌入场景对
  实时性无要求，简单优先。
- **embed 页不复用主 App 路由**：独立入口导致少量组件重复，但换来嵌入产物
  与主应用的彻底隔离（构建产物更小、样式不串、权限天然收敛）。
