# 代码目录清理报告

> 日期：2026-06-18（2026-06-18 更新，统一临时脚本到根级 `temp/`）  
> 目标：把临时/一次性脚本归档到根级 `temp/`，把可复用脚本集中到 `scripts/` 与 `backend/scripts/`，减少根目录和 `backend/` 下的杂乱文件，确保项目主目录只保留程序必须的代码与配置。

---

## 1. 清理策略

| 类别 | 存放位置 | 说明 |
|---|---|---|
| **可复用脚本** | `scripts/`（项目根级）<br>`backend/scripts/` | 通用系统管理、数据导入导出、验证调试、股票批量处理、业务批量提交等 |
| **临时/一次性脚本** | `temp/`（项目根级） | 特定任务（如半导体/WF6 专题、某一批次构造、一次性清理、调试）完成后大概率不再使用 |
| **保留原处** | 项目根目录、`backend/` 根目录 | 入口配置：`README.md`、`AGENTS.md`、`docker-compose.yml`、各 `requirements.txt`、`Dockerfile` 等 |

> **注意**：`backend/temp/` 已被移除，所有临时脚本统一归档到项目根级 `temp/`，避免在 `backend/` 主目录中保留非程序代码。

---

## 2. 移动清单

### 2.1 根目录 → `scripts/`（可复用系统脚本）

| 文件 | 原位置 | 新位置 | 移动理由 |
|---|---|---|---|
| `arachne_manager.py` | 项目根目录 | `scripts/arachne_manager.py` | 跨平台系统管理器，用于启停 Neo4j / 后端 / 前端，长期复用 |
| `start-all.ps1` | 项目根目录 | `scripts/start-all.ps1` | 一键启动全系统的 PowerShell 脚本，长期复用 |
| `stop-all.ps1` | 项目根目录 | `scripts/stop-all.ps1` | 一键停止全系统的 PowerShell 脚本，长期复用 |

> 注：
> - `arachne_manager.py` 内部的 `PROJECT_ROOT` 已由 `Path(__file__).parent` 改为 `Path(__file__).parent.parent`，确保从 `scripts/` 运行仍能正确定位项目根目录。
> - `start-all.ps1` 原先用 `$MyInvocation.MyCommand.Definition` 取脚本路径后再取一次父目录；脚本移动到 `scripts/` 后这会把 `scripts/` 当成项目根目录，导致找不到 Neo4j。已改为 `$projectRoot = Split-Path -Parent $PSScriptRoot`。
> - `stop-all.ps1` 中停止后端的端口原来写死为 `8005`，与 `start-all.ps1` 启动的 `16060` 不一致，已修正为 `16060`。

### 2.2 根目录 → `temp/`（临时脚本/产物）

| 文件 | 原位置 | 新位置 | 移动理由 |
|---|---|---|---|
| `check_nodes.py` | 项目根目录 | `temp/check_nodes.py` | 硬编码旧端口 `8005` 和若干批次节点列表的一次性检查脚本 |
| `webbridge_request.json` | 项目根目录 | `temp/webbridge_request.json` | 单次浏览器自动化请求的记录文件，无复用价值 |

### 2.3 `backend/` 根目录与 `backend/temp/` → `temp/`（专题/一次性脚本与产物）

| 文件 | 原位置 | 新位置 | 移动理由 |
|---|---|---|---|
| `add_semiconductor_relations.py` | `backend/` / `backend/temp/` | `temp/add_semiconductor_relations.py` | 一次性补充半导体产业流关系 |
| `add_wf6_company_exposures.py` | `backend/` / `backend/temp/` | `temp/add_wf6_company_exposures.py` | WF6 专题：为特定公司添加暴露关系 |
| `add_wf6_industry_mappings.py` | `backend/` / `backend/temp/` | `temp/add_wf6_industry_mappings.py` | WF6 专题：为行业添加节点映射 |
| `add_wf6_route.py` | `backend/` / `backend/temp/` | `temp/add_wf6_route.py` | WF6 专题：批量创建节点与关系 |
| `construct_company_view.py` | `backend/scripts/` / `backend/temp/` | `temp/construct_company_view.py` | 针对 `batch_001` 公司视图的一次性构造脚本 |
| `construct_industrial_graph.py` | `backend/scripts/` / `backend/temp/` | `temp/construct_industrial_graph.py` | 针对 `batch_001` 产业图的一次性构造脚本 |
| `construct_industrial_graph_v2.py` | `backend/scripts/` / `backend/temp/` | `temp/construct_industrial_graph_v2.py` | `construct_industrial_graph.py` 的迭代版本，同一次任务 |
| `dump_semiconductor_graph.py` | `backend/` / `backend/temp/` | `temp/dump_semiconductor_graph.py` | 一次性导出半导体行业子图 |
| `generate_semiconductor_report.py` | `backend/` / `backend/temp/` | `temp/generate_semiconductor_report.py` | 生成半导体公司研究报告的一次性脚本 |
| `import_semiconductor_companies_batch1.py` | `backend/` / `backend/temp/` | `temp/import_semiconductor_companies_batch1.py` | 半导体公司第一批导入 |
| `import_semiconductor_companies_batch2.py` | `backend/` / `backend/temp/` | `temp/import_semiconductor_companies_batch2.py` | 半导体公司第二批导入 |
| `search_semiconductor.py` | `backend/` / `backend/temp/` | `temp/search_semiconductor.py` | 半导体专题的临时搜索脚本 |
| `webbridge_helper.py` | `backend/` / `backend/temp/` | `temp/webbridge_helper.py` | 配合单次 WebBridge 会话的临时辅助脚本 |
| `semiconductor_dump2.txt` | `backend/` / `backend/temp/` | `temp/semiconductor_dump2.txt` | 半导体子图导出的文本产物 |
| `all_industries.json` | `backend/scripts/` / `backend/temp/` | `temp/all_industries.json` | 股票行业统计的一次性输出产物 |
| `output.txt` | `backend/scripts/` / `backend/temp/` | `temp/output.txt` | 某次脚本运行的文本输出产物 |
| `cleanup_company_view_neo4j.py` | `backend/scripts/` | `temp/cleanup_company_view_neo4j.py` | 一次性清理旧 Company View 数据 |
| `debug_subgraph.py` | `backend/scripts/` | `temp/debug_subgraph.py` | 一次性子图调试脚本 |
| `uvicorn.log` | `backend/` 根目录 | `temp/uvicorn.log` | 后端运行时日志，非程序代码 |

### 2.4 保留在 `backend/scripts/` 的可复用脚本

以下脚本具有通用性，继续保留在 `backend/scripts/`：

- `batch_all_stocks.py` / `batch_all_stocks_resume.py`
- `batch_stocks.py` / `batch_stocks_incremental.py`
- `export_db.py` / `import_db.py`
- `fetch_and_filter.py`
- `fetch_tushare_data.py` / `fetch_tushare_data_v2.py`
- `read_batch.py` / `show_batch.py` / `summarize_data.py`
- `submit_business_batch.py` / `submit_industrial_graph.py`
- `verify_graph.py`

---

## 3. 文档更新

`AGENTS.md` 中的系统管理入口路径已同步更新：

```markdown
- `scripts/arachne_manager.py` — Python cross-platform manager (`start/stop/status/stats/logs`)
- `scripts/start-all.ps1` / `scripts/stop-all.ps1` — PowerShell one-click scripts
```

---

## 4. 结果

- 项目根目录 **0 个脚本**，只剩核心配置文件与文档。
- `backend/` 根目录 **0 个脚本/产物**，只保留 `Dockerfile`、`requirements.txt` 等程序必需配置。
- `backend/temp/` 已移除，避免主目录中出现非代码归档。
- `backend/scripts/` 精简为 **16 个可复用脚本**。
- 所有临时/一次性脚本与运行时产物统一归档到根级 `temp/`。

> 建议后续新增脚本时先判断：若为通用工具则放入 `scripts/` 或 `backend/scripts/`；若为一次性专题任务脚本，任务完成后主动移入 `temp/`。
