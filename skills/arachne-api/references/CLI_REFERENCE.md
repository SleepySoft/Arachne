# Arachne CLI 命令参考

CLI 入口：`cli/arachne_cli.py`

默认服务地址：`http://localhost:8005/api/v1`

---

## 命令总览

```
python cli/arachne_cli.py <command> [options]
```

| 命令 | 说明 |
|---|---|
| `submit` | 提交 `GraphRegistrationBatch` JSON 文件 |
| `business-batch` | 提交 `BusinessRegistrationBatch` JSON 文件 |
| `industry` | 管理行业及其节点映射 |
| `company` | 管理公司及其节点暴露 |
| `query` | 查询图谱统计、节点、子图、邻居 |

---

## submit

提交产业节点/关系批量文件。

```bash
python cli/arachne_cli.py submit <json_file>
```

示例：

```bash
python cli/arachne_cli.py submit graph_batch_001.json
```

对应后端接口：`POST /api/v1/batches`

---

## business-batch

提交行业/公司/映射/暴露批量文件。

```bash
python cli/arachne_cli.py business-batch <json_file>
```

示例：

```bash
python cli/arachne_cli.py business-batch business_batch_001.json
```

对应后端接口：`POST /api/v1/business-batches`

---

## industry

### industry list

```bash
python cli/arachne_cli.py industry list [options]
```

选项：

- `--search <keyword>`：按名称/ID 搜索
- `--type {formal_industry,curated_view,theme_view}`：按类型筛选
- `--status {ACTIVE,PENDING,REJECTED,ARCHIVED}`：按状态筛选
- `--page <int>`：页码，默认 1
- `--page-size <int>`：每页数量，默认 20

示例：

```bash
python cli/arachne_cli.py industry list --search 驾驶 --type curated_view
```

### industry get

```bash
python cli/arachne_cli.py industry get <industry_id>
```

### industry create

```bash
python cli/arachne_cli.py industry create --json <json_file>
```

JSON 示例参见 API_REFERENCE.md 中的 Industry schema。

### industry update

```bash
python cli/arachne_cli.py industry update <industry_id> --json <json_file>
```

### industry delete

```bash
python cli/arachne_cli.py industry delete <industry_id>
```

### industry subgraph

```bash
python cli/arachne_cli.py industry subgraph <industry_id>
```

### industry mappings

```bash
python cli/arachne_cli.py industry mappings <industry_id> [options]
```

选项：`--page`, `--page-size`

### industry add-mapping

```bash
python cli/arachne_cli.py industry add-mapping <industry_id> --json <json_file>
```

JSON 示例参见 API_REFERENCE.md 中的 IndustryNodeMapping schema。

### industry del-mapping

```bash
python cli/arachne_cli.py industry del-mapping <industry_id> <mapping_id>
```

---

## company

### company list

```bash
python cli/arachne_cli.py company list [options]
```

选项：

- `--search <keyword>`：按名称/ID 搜索
- `--type {public,private,state_owned,startup,unknown}`：按公司类型筛选
- `--status {ACTIVE,PENDING,REJECTED,ARCHIVED}`：按状态筛选
- `--country <code>`：按国家筛选
- `--page <int>`：页码，默认 1
- `--page-size <int>`：每页数量，默认 20

示例：

```bash
python cli/arachne_cli.py company list --search 禾赛 --type public --country CN
```

### company get

```bash
python cli/arachne_cli.py company get <company_id>
```

### company create

```bash
python cli/arachne_cli.py company create --json <json_file>
```

JSON 示例参见 API_REFERENCE.md 中的 Company schema。

### company update

```bash
python cli/arachne_cli.py company update <company_id> --json <json_file>
```

### company delete

```bash
python cli/arachne_cli.py company delete <company_id>
```

### company subgraph

```bash
python cli/arachne_cli.py company subgraph <company_id>
```

### company exposures

```bash
python cli/arachne_cli.py company exposures <company_id> [options]
```

选项：`--page`, `--page-size`

### company add-exposure

```bash
python cli/arachne_cli.py company add-exposure <company_id> --json <json_file>
```

JSON 示例参见 API_REFERENCE.md 中的 CompanyNodeExposure schema。

### company del-exposure

```bash
python cli/arachne_cli.py company del-exposure <company_id> <exposure_id>
```

---

## query

### query --stats

```bash
python cli/arachne_cli.py query --stats
```

### query --list-nodes

```bash
python cli/arachne_cli.py query --list-nodes
```

### query --search

```bash
python cli/arachne_cli.py query --search <keyword>
```

### query --subgraph

```bash
python cli/arachne_cli.py query --subgraph <node_id> --depth 2
```

`--depth` 可选，默认 2。

### query --neighbors

```bash
python cli/arachne_cli.py query --neighbors <node_id>
```
