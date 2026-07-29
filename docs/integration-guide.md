# Arachne 集成指南

> 本文档面向集成方（包括 AI 代理）。按步骤执行即可完成集成。

---

## 1. 概述

Arachne 是一个产业本体图谱系统，提供：

- **产业图谱浏览**：节点、关系、行业、公司的可视化与查询
- **推理引擎**：从节点出发，沿物料链展开上下游关系
- **嵌入式推理视图**：通过 URL 参数即可展示推理结果

集成方式有两种：

| 方式 | 适合场景 | 实现 |
|------|---------|------|
| **nginx 代理** | 自有系统，Arachne 页面和服务直接转发 | 反向代理 + JWT 鉴权 |
| **组件嵌入** | 第三方系统，嵌入推理视图 | iframe（embed.html）或 React 组件 |

两种方式共用同一套后端 API 和鉴权机制。

---

## 2. 快速开始（30 秒集成）

最小可用集成——无鉴权，只读嵌入推理视图：

```
https://your-arachne-host/embed.html?seed=humanoid_robot&engine=arachne_flow&task_type=association
```

参数说明：

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `seed` | 是 | - | 起点节点 ID，逗号分隔多个 |
| `engine` | 否 | `arachne_flow` | `arachne_flow` 或 `legacy` |
| `task_type` | 否 | `association` | 推理任务类型 |
| `max_depth` | 否 | `2` | 遍历深度 |
| `direction` | 否 | `forward` | `forward` / `backward` / `both` |
| `outputs` | 否 | 引擎默认 | 逗号分隔的输出类型 |
| `resolve` | 否 | `0` | `1` = 将 seed 当名称搜索解析 |
| `view` | 否 | - | 已发布视图的 UUID |
| `title` | 否 | 起点名称 | 自定义标题 |
| `refresh` | 否 | `0` | `1` = 忽略视图缓存重新推理 |

**无鉴权时默认只读**：可以浏览和推理，但不能创建/修改/删除数据。

---

## 3. 获取集成配置

Arachne 以自身为主，提供完整的集成清单。集成方只需取一次即可知道全部对接要求。

### 请求

```
GET /integration/config
```

> **安全限制**：
> - 前缀为 `/integration`（不在 `/api/v1` 下）
> - 不出现在 OpenAPI / Swagger 文档中
> - 仅接受本地/私有 IP 请求（127.0.0.1、10.x、172.16-31.x、192.168.x）
> - nginx 反向代理场景下，请求来自本机，可正常访问

### 响应示例

```json
{
  "service": "Arachne Industrial Ontology Graph",
  "version": "1.0.0",
  "auth": {
    "mode": "jwt",
    "accepted_scopes": ["read_only", "read_write"],
    "token_header": "Authorization",
    "token_format": "Bearer <jwt>",
    "required_claims": ["sub", "scope", "exp"],
    "expected_issuer": "your-host",
    "expected_audience": "arachne",
    "jwks_url": "https://your-host/.well-known/jwks.json",
    "jwks_refresh_seconds": 3600
  },
  "scope_model": {
    "read_only": "GET + 只读 POST（推理/查询）；所有写操作返回 403",
    "read_write": "全部端点，包括创建/修改/删除"
  },
  "api": {
    "base_url": "/api/v1",
    "read_only_post_paths": [
      "/api/v1/reasoning/execute",
      "/api/v1/reasoning/query",
      ...
    ],
    "key_endpoints": { ... }
  },
  "embed": {
    "reasoning_url_template": "/embed.html?seed={seed}&engine={engine}&task_type={task_type}",
    "published_view_url_template": "/embed.html?view={view_id}",
    "supported_params": { ... }
  },
  "published_views": { ... }
}
```

**集成方应读取此端点，按照返回的 auth 契约签发 JWT。**

---

## 4. 鉴权（JWT）

### 4.1 工作原理

```
集成方（授权方）                    Arachne（资源方）
─────────────                    ──────────────
1. 用户登录/校验
2. 生成 RSA 密钥对
3. 暴露 JWKS 端点
4. 按 Arachne 契约签发 JWT ──────>  5. 从 JWKS 获取公钥验签
   (iss, aud, scope, exp, kid)      6. 读取 scope 执行只读/可写控制
                                    7. 无 token = 只读
```

### 4.2 JWT 契约

| 字段 | 必填 | 说明 |
|------|------|------|
| `sub` | 是 | 用户/客户端标识 |
| `scope` | 是 | `read_only` 或 `read_write` |
| `exp` | 是 | 过期时间（Unix 时间戳） |
| `iss` | 是* | 签发方，需匹配 `expected_issuer` |
| `aud` | 是* | 受众，需匹配 `expected_audience`（固定值 `arachne`） |
| `kid` | 是 | JWT 头中的密钥 ID，用于 JWKS 查找 |

> *`iss` 和 `aud` 仅在 Arachne 配置了对应值时校验。

### 4.3 默认行为（重要）

| 场景 | 权限 |
|------|------|
| 无 `Authorization` 头 | **只读**（可浏览、推理，不可写） |
| 有效 JWT + `scope: read_write` | 读写 |
| 有效 JWT + `scope: read_only` | 只读 |
| 过期/无效 JWT | **只读**（降级，不拒绝） |
| 本地 IP + `JWT_LOCAL_BYPASS=true` | **读写**（独立运行/管理） |

这意味着：**即使不做任何鉴权，嵌入的视图也能正常展示推理结果**。鉴权仅用于升级到可写权限。

### 4.3.1 独立运行（本地绕过）

`AUTH_MODE=jwt` 模式下，`JWT_LOCAL_BYPASS=true`（默认）时，来自本地/私有 IP 的请求自动获得 `read_write` 权限，无需 JWT。

| 部署场景 | 配置 | 本地访问 | 外部访问 |
|---------|------|---------|---------|
| 纯独立运行 | `AUTH_MODE=disabled` | 读写 | 读写（无鉴权） |
| 独立 + 远程只读 | `AUTH_MODE=jwt`（默认 bypass） | 读写（本地绕过） | 只读（需 JWT 升级） |
| nginx 代理集成 | `AUTH_MODE=jwt` + `JWT_LOCAL_BYPASS=false` | 需 JWT | 需 JWT |

> **nginx 场景必须设 `JWT_LOCAL_BYPASS=false`**：nginx 转发的请求源 IP 是本机，否则所有请求都会获得读写权限，鉴权形同虚设。

### 4.4 Arachne 侧配置

```bash
# .env 或环境变量
AUTH_MODE=jwt
JWT_ISSUER=your-host-system
JWT_AUDIENCE=arachne
JWT_JWKS_URL=https://your-host/.well-known/jwks.json
JWT_JWKS_REFRESH_SECONDS=3600
```

### 4.5 密钥轮换

1. JWKS 端点添加新密钥（新 `kid`）
2. 用新密钥签发新 token
3. Arachne 遇到未知 `kid` 时自动刷新 JWKS
4. 旧 token 过期后，从 JWKS 移除旧密钥
5. Arachne 无需重启

---

## 5. 嵌入推理视图

### 5.1 iframe 嵌入

```html
<iframe
  src="https://arachne-host/embed.html?seed=humanoid_robot&engine=arachne_flow"
  width="100%"
  height="600"
  frameborder="0"
></iframe>
```

### 5.2 带鉴权的嵌入

通过 `postMessage` 从父窗口注入 token：

```javascript
// 父页面
const iframe = document.querySelector("iframe");
iframe.addEventListener("load", () => {
  iframe.contentWindow.postMessage(
    { type: "arachne-token", token: jwtToken },
    "https://arachne-host"
  );
});
```

> Arachne embed 页面监听 `postMessage` 并将 token 注入 API 请求头。
> 也可通过 nginx 设置 httpOnly cookie，embed 页面自动携带。

### 5.3 已发布视图（稳定短链接）

适用于需要固定 URL 的场景（如报告、仪表盘）：

```
# 1. 创建发布视图（需要写权限）
POST /api/v1/published-views
{
  "title": "人形机器人产业链",
  "params": {
    "seed": "humanoid_robot",
    "engine": "arachne_flow",
    "task_type": "association"
  }
}

# 响应
{ "view_id": "4c336bbd-2577-4ec8-9caa-4052b0fd6a65", ... }

# 2. 嵌入
https://arachne-host/embed.html?view=4c336bbd-2577-4ec8-9caa-4052b0fd6a65
```

可选 `result_snapshot` 字段缓存推理结果，embed 页面直接展示无需重新推理（`&refresh=1` 可强制刷新）。

---

## 6. API 调用

### 6.1 只读端点（无需鉴权）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/query/health` | 系统健康检查 |
| GET | `/api/v1/nodes/fuzzy-search?query=芯片` | 模糊搜索节点 |
| POST | `/api/v1/reasoning/execute` | 执行推理 |
| POST | `/api/v1/reasoning/query` | 搜索对象 |
| GET | `/api/v1/published-views` | 列出已发布视图 |
| GET | `/api/v1/published-views/{id}` | 获取已发布视图 |
| GET | `/api/v1/industries` | 列出行业 |
| GET | `/api/v1/companies` | 列出公司 |

### 6.2 写端点（需要 `scope: read_write`）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/nodes` | 创建节点 |
| POST | `/api/v1/edges` | 创建关系 |
| POST | `/api/v1/industries` | 创建行业 |
| POST | `/api/v1/companies` | 创建公司 |
| POST | `/api/v1/published-views` | 发布视图 |
| PUT/DELETE | `/api/v1/nodes/{id}` | 修改/删除节点 |
| ... | ... | 其他 CRUD |

### 6.3 调用示例

```bash
# 只读调用（无 token）
curl https://arachne-host/api/v1/reasoning/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "demo",
    "task_type": "association",
    "source_nodes": ["humanoid_robot"],
    "requested_outputs": ["temporary_graph", "paths"],
    "engine": "arachne_flow"
  }'

# 写操作（需要 JWT）
curl https://arachne-host/api/v1/published-views \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title": "demo", "params": {"seed": "chip"}}'
```

每个响应都带 `X-Arachne-Scope` 头（`read_only` 或 `read_write`），前端可据此控制 UI。

---

## 7. 前端只读模式

当 Arachne 检测到只读权限时：

- **主界面**：所有创建/编辑/删除按钮自动隐藏（通过 AuthContext + CSS）
- **推理视图**：正常展示，深度挖掘和切换引擎可用（均为只读操作）
- **embed 页面**：本身就是只读设计，无需额外处理

集成方无需在前端做任何只读控制——Arachne 自己处理。

---

## 8. AI 集成检查清单

如果你是 AI 代理，按以下步骤执行：

- [ ] **步骤 1**：从 Arachne 获取集成配置
  - `GET /integration/config`（需从本地 IP 访问）
  - 读取 `auth.mode`、`auth.expected_issuer`、`auth.expected_audience`
  - 读取 `embed.reasoning_url_template` 了解嵌入格式

- [ ] **步骤 2**：如果 `auth.mode == "jwt"`，准备 JWT 签发
  - 生成 RSA 密钥对（2048 位）
  - 暴露 JWKS 端点：`GET /.well-known/jwks.json`
  - 按契约签发 JWT：`iss` = expected_issuer, `aud` = "arachne", `scope` = "read_write" 或 "read_only"

- [ ] **步骤 3**：配置 Arachne 环境变量
  - `AUTH_MODE=jwt`
  - `JWT_JWKS_URL=<你的 JWKS 端点>`
  - `JWT_ISSUER=<你的 issuer>`
  - `JWT_AUDIENCE=arachne`

- [ ] **步骤 4**：嵌入推理视图
  - 拼接 URL：`/embed.html?seed=<node_id>&engine=arachne_flow`
  - 或创建发布视图获取稳定 `view_id`：`POST /api/v1/published-views`

- [ ] **步骤 5**：验证
  - 无 token 时 GET 请求正常，POST 写操作返回 403
  - 带 `scope: read_write` 的 JWT 时写操作正常
  - 响应头 `X-Arachne-Scope` 反映当前权限

- [ ] **步骤 6**（可选）：nginx 代理配置
  - 代理 `/api/*` -> Arachne 后端
  - 代理 `/embed.html` -> Arachne 前端
  - 代理 `/integration/config` -> Arachne 后端
  - 设置 httpOnly cookie 传递 JWT（或由前端添加 Authorization 头）

---

## 9. 环境变量速查

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AUTH_MODE` | `disabled` | `disabled` / `header` / `jwt` / `custom` |
| `AUTH_SCOPE_HEADER` | `X-Arachne-Scope` | header 模式读取的请求头名 |
| `JWT_ISSUER` | (空) | 期望的 JWT 签发方 |
| `JWT_AUDIENCE` | `arachne` | 期望的 JWT 受众 |
| `JWT_JWKS_URL` | (空) | JWKS 端点 URL |
| `JWT_JWKS_REFRESH_SECONDS` | `3600` | JWKS 缓存刷新间隔 |
| `JWT_LOCAL_BYPASS` | `true` | jwt 模式下本地 IP 是否自动获得读写权限（nginx 后必须设 `false`） |

**`AUTH_MODE=disabled`**：独立运行模式，全部读写，无鉴权（开发/单机部署默认）。
**`AUTH_MODE=jwt`**：生产集成模式，无 token = 只读，有效 JWT 升级权限。
