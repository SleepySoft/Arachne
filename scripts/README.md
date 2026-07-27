# Arachne 运维与数据脚本说明

给人和 AI Agent 的快速上手指南：**先查这里再找脚本，不要重新造轮子**。

## 0. 通用约定（所有脚本适用）

- **运行方式**：在仓库根目录，一律用后端虚拟环境运行（依赖已装好）：
  ```powershell
  backend\venv\Scripts\python.exe scripts\<脚本名>.py [参数]
  ```
- **服务依赖**：后端 API `http://localhost:16060`（AGENTS.md 写的 8000 已过时）；
  Neo4j `bolt://localhost:7687`（neo4j/arachne123）；PG `localhost:5433/arachne`（postgres/postgres）。
  可用 `curl http://localhost:16060/api/v1/query/health` 确认在线。
- **中文输出乱码**：PowerShell 里先执行
  `$env:PYTHONIOENCODING='utf-8'; [Console]::OutputEncoding=[Text.Encoding]::UTF8`
- **优先走 API，不直接写库**：节点/边/公司/行业一律通过后端 API（批次接口），
  直接 asyncpg/neo4j 写库仅限无 API 覆盖的特例（如 flow METHOD 的 PG-only 元数据）。
- **PowerShell 内联 Python 是坑**：`python -c "..."` 的引号转义经常被 PowerShell 吃掉，
  超过一行的逻辑请写成脚本文件再跑。
- **不要用 PowerShell `Get-Content/Set-Content` 改写含中文的文件**（GBK 损坏不可逆），
  用编辑器或 `StrReplaceFile/WriteFile`。
- `temp/` 是草稿区（gitignored）：一次性批次生成器、临时检查脚本放那里；
  **可复用脚本必须放本目录并在下表登记**。

## 1. 脚本清单

### 系统管理

| 脚本 | 用途 | 写库? |
|---|---|---|
| `start-all.ps1` / `stop-all.ps1` | 一键启停 Neo4j + PG + 后端 + 前端 | - |
| `restart-backend.ps1` | 重启后端（**新增 flow 文件后必须重启**，include 图有进程内缓存） | - |
| `arachne_manager.py` | 跨平台进程管理（status/start/stop 各组件），`python scripts/arachne_manager.py status` | - |

### 备份 / 导入导出

| 脚本 | 用途 | 写库? |
|---|---|---|
| `export_db.py` | 导出 Neo4j + PG 全量到 JSON（默认 `data/ArachneData/newest`） | 否 |
| `import_db.py` | 从 export 产物恢复（`--clear --yes` 清库导入，**危险**） | **是** |
| `backup_neo4j_graph.py` | 只备份 Neo4j 节点与边到 JSON | 否 |
| `cleanup_test_data.py` | 删除 `is_test=true` 的测试数据（`--dry-run` 先看数量） | **是** |
| `migrate_prov_to_provn.py` | PROV JSON → PROV-N 迁移（PROV 已弃用，仅供参考） | 是 |

### arachne-flow 流程文件工作流

| 脚本 | 用途 | 写库? |
|---|---|---|
| `preview_flows.py` | 批量校验 flow YAML（`--category biopharma` 限定目录），退出码可入 CI | 否 |
| `compile_flows.py` | 编译 flow 到 Neo4j（`--category` 或 `--flow-id`），**先 preview 再 compile** | **是** |
| `extract_flow_pg_gaps.py` | 提取遗漏：flow 引用 vs PG 节点 + PG 字段完整性 + Neo4j↔PG 一致性，报告到 `temp/flow_pg_gap_report.json` | 否 |
| `smoke_flow_reasoning.py` | flow 推理冒烟（association / cross_graph_context），**演示正确请求格式** | 否 |
| `backend/scripts/flow_context.py` | flow 写作上下文工具：`<词>` 查重/找上下游/对 legacy；`--dangling` 断链报告 | 否 |

### 公司 / 行业数据

| 脚本 | 用途 | 写库? |
|---|---|---|
| `audit_node_company_exposures.py` | 审计节点→公司暴露覆盖：`--industry biopharma` 或 `--nodes a b c`，列出无暴露节点 | 否 |
| `cli/arachne_cli.py`（在 cli/ 目录） | 节点/边/行业/公司/映射/暴露的 CRUD 与批量提交，见 `skills/arachne-api/SKILL.md` | 是 |

## 2. 典型工作流

**新增/修改 flow 文件后：**
```powershell
backend\venv\Scripts\python.exe scripts\preview_flows.py --category biopharma
scripts\restart-backend.ps1          # 有新文件时必须重启（include 缓存）
backend\venv\Scripts\python.exe scripts\compile_flows.py --category biopharma
backend\venv\Scripts\python.exe backend\scripts\flow_context.py --dangling
backend\venv\Scripts\python.exe scripts\extract_flow_pg_gaps.py
backend\venv\Scripts\python.exe scripts\smoke_flow_reasoning.py
```

**写 flow 之前（查重/找接链点）：**
```powershell
backend\venv\Scripts\python.exe backend\scripts\flow_context.py <关键词>
```

**补公司数据：**
```powershell
backend\venv\Scripts\python.exe scripts\audit_node_company_exposures.py --industry biopharma
# 找到无暴露节点 → 调研公司 → 组 BusinessRegistrationBatch → cli business-batch 提交
backend\venv\Scripts\python.exe scripts\smoke_flow_reasoning.py --company <company_id>
```

## 3. 常见误用（血泪教训）

1. **推理请求格式**：种子字段是 `source_nodes`（字符串数组），不是 `source_object_ids`；
   方向枚举是 `both`，不是 `bidirectional`。照抄 `smoke_flow_reasoning.py`。
2. **新增 flow 文件后不重启后端就编译/查 effective 子图** → include 解析不到，必须 `restart-backend.ps1`。
3. **flow 引用 PG 不存在的 RESOURCE/METHOD** → 显示退化为 id。真实体走 GraphRegistrationBatch
   登记进 Neo4j+PG；集成类合成 METHOD（`integration_of_*`）按先例只补 PG 行。
   用 `extract_flow_pg_gaps.py` 检查。
4. **测试数据忘标 `is_test: true`** → cleanup 捕不到，变成脏数据（曾有 2 个 draft 测试节点因此残留）。
5. **CLI 默认端口 8005 是错的** → `cli/arachne_cli.py` 连接失败时检查后端实际端口（16060）。
6. **手工补链记录**：`data/flows/<category>/README.md` 记录了生成器之外的手工修改，
   重跑生成器前必读，否则手工补链会被覆盖。
