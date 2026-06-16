---
name: arachne-api
description: 通过 Arachne CLI（arachne_cli.py）或前端界面操作产业本体图，包括批量注册节点/关系/公司/行业/映射/暴露，以及行业、公司和查询管理。当用户要求通过命令行或 API 添加、创建、注册、更新、查询或操作 Arachne 图谱实体（节点、边、公司、行业、映射、批量、事实关系）时触发。
---

# Arachne CLI 操作技能

使用本技能通过 `cli/arachne_cli.py` 或前端界面操作 Arachne 系统。CLI 封装了后端 API，默认连接 `http://localhost:8005/api/v1`；前端界面则通过左侧“行业”侧边栏和右侧面板完成行业的 CRUD 与映射管理。在判断一个候选词是否应该成为节点之前，先参考 `arachne-graph` 技能中的本体规则；本技能解决的是“决定之后如何通过 CLI 或 UI 提交数据”。

## 运行方式

CLI 位于项目根目录的 `cli/arachne_cli.py`，依赖 `httpx`：

```bash
# 进入 cli 目录并激活虚拟环境（Windows）
cd cli
.\venv\Scripts\activate
python arachne_cli.py --help
```

如果虚拟环境不可用，可直接安装依赖：

```bash
pip install -r cli/requirements.txt
python cli/arachne_cli.py --help
```

## 全局规则

- 所有 ID 必须匹配正则 `^[a-z][a-z0-9_]*$`，长度 3–64（`relation_id` 最长 128）。仅允许小写蛇形命名。
- `HIGH` 置信度或 `ACTIVE` 状态**必须至少有一条证据**，且 `source_title` 和 `quote` 不能为空。
- `source_url` 为可选项。
- 不要提供由后端自动生成的 `*_uuid` 字段。
- 创建前先使用 `query` 或 `list` 命令检查节点/公司/行业是否已存在，避免重复。
- 快速添加草稿节点时，只需中文名或英文名之一；系统会自动生成 `draft_{uuid}` 占位 ID 并设为 `PENDING` 状态，后续由 AI 或管理员补全。
- 映射节点到行业时，先确认目标 `node_id` 已在 Neo4j 中存在；否则映射会创建成功但无法在行业子图中显示。
- 关于本体决策（是否建新节点、是否别名、是否拒绝、是否登记为行业）请咨询 `arachne-graph` 技能。

## 核心操作流程

### 1. 批量注册节点和关系（最常用）

将节点和边整理为 `GraphRegistrationBatch` JSON 文件，然后提交：

```bash
python cli/arachne_cli.py submit graph_batch_001.json
```

`graph_batch_001.json` 示例：

```json
{
  "batch_id": "batch_001",
  "task_description": "注册激光雷达产业链节点与关系",
  "nodes_to_upsert": [
    {
      "node_id": "lidar_system",
      "canonical_name_zh": "激光雷达系统",
      "canonical_name_en": "LiDAR system",
      "aliases": ["激光雷达", "LiDAR"],
      "definition": "通过发射激光并接收回波来测量目标距离和轮廓的传感系统。",
      "entity_type": "system",
      "evidence": [
        {
          "source_title": "激光雷达技术白皮书",
          "source_url": "https://example.com/lidar-whitepaper.pdf",
          "quote": "激光雷达系统由激光发射器、扫描机构和接收器组成。"
        }
      ],
      "confidence": "HIGH",
      "status": "ACTIVE"
    },
    {
      "node_id": "laser",
      "canonical_name_zh": "激光器",
      "definition": "能够产生并发射激光的光源器件。",
      "entity_type": "component",
      "evidence": [
        {
          "source_title": "激光原理与应用",
          "quote": "激光器是产生激光的核心器件。"
        }
      ],
      "confidence": "HIGH",
      "status": "ACTIVE"
    }
  ],
  "edges_to_upsert": [
    {
      "edge_namespace": "industrial_flow",
      "edge_id": "laser_to_lidar",
      "from_node": "laser",
      "to_node": "lidar_system",
      "edge_type": "material_flow",
      "description": "激光器为激光雷达系统提供探测光源。",
      "evidence": [
        {
          "source_title": "激光雷达拆解报告",
          "quote": "该系统采用1550nm光纤激光器作为发射源。"
        }
      ],
      "confidence": "HIGH"
    }
  ],
  "rejected_or_pending": []
}
```

### 2. 批量注册行业、公司、映射和暴露

使用 `business-batch` 命令提交 `BusinessRegistrationBatch`：

```bash
python cli/arachne_cli.py business-batch business_batch_001.json
```

`business_batch_001.json` 示例：

```json
{
  "batch_id": "business_batch_001",
  "task_description": "批量注册智能驾驶行业、公司与节点暴露",
  "industries_to_upsert": [
    {
      "industry_id": "intelligent_driving",
      "name_zh": "智能驾驶",
      "industry_type": "curated_view",
      "status": "ACTIVE"
    }
  ],
  "industry_node_mappings_to_upsert": [
    {
      "mapping_id": "intelligent_driving_contains_lidar_system",
      "industry_id": "intelligent_driving",
      "node_id": "lidar_system",
      "role": "核心产品",
      "weight": 0.9,
      "confidence": "HIGH",
      "evidence": [
        {
          "source_title": "智能驾驶产业链报告",
          "quote": "激光雷达系统是智能驾驶感知层的核心产品。"
        }
      ],
      "status": "ACTIVE",
      "notes": "核心传感器"
    }
  ],
  "companies_to_upsert": [
    {
      "company_id": "hesai_technology",
      "name_zh": "禾赛科技",
      "country": "CN",
      "company_type": "public",
      "status": "ACTIVE"
    }
  ],
  "company_node_exposures_to_upsert": [
    {
      "exposure_id": "hesai_technology_produce_lidar_system",
      "company_id": "hesai_technology",
      "node_id": "lidar_system",
      "activity_type": "produce",
      "weight": 0.95,
      "status": "ACTIVE"
    }
  ]
}
```

### 3. 单独管理行业

```bash
# 列出行业
python cli/arachne_cli.py industry list --search 驾驶

# 查看行业详情
python cli/arachne_cli.py industry get intelligent_driving

# 创建行业
python cli/arachne_cli.py industry create --json industry.json

# 更新行业
python cli/arachne_cli.py industry update intelligent_driving --json industry_update.json

# 删除行业
python cli/arachne_cli.py industry delete intelligent_driving

# 查看行业子图
python cli/arachne_cli.py industry subgraph intelligent_driving

# 查看行业映射
python cli/arachne_cli.py industry mappings intelligent_driving

# 添加节点映射
python cli/arachne_cli.py industry add-mapping intelligent_driving --json mapping.json

# 更新节点映射（可修改 role/weight/confidence/evidence/status/notes）
python cli/arachne_cli.py industry update-mapping intelligent_driving intelligent_driving_contains_lidar_system --json mapping_update.json

# 删除节点映射
python cli/arachne_cli.py industry del-mapping intelligent_driving intelligent_driving_contains_lidar_system
```

`mapping.json` 示例（创建）：

```json
{
  "mapping_id": "intelligent_driving_contains_lidar_system",
  "industry_id": "intelligent_driving",
  "node_id": "lidar_system",
  "role": "核心产品",
  "weight": 0.9,
  "confidence": "HIGH",
  "evidence": [
    {
      "source_title": "智能驾驶产业链报告",
      "quote": "激光雷达系统是智能驾驶感知层的核心产品。"
    }
  ],
  "status": "ACTIVE",
  "notes": "核心传感器"
}
```

`mapping_update.json` 示例（更新，只传需要修改的字段）：

```json
{
  "role": "关键零部件",
  "weight": 0.85,
  "confidence": "MEDIUM",
  "status": "ACTIVE"
}
```

#### 通过前端界面管理行业映射

除了 CLI，也可以直接在前端操作：

1. 切换到左侧“行业”子标签，搜索并点击目标行业。
2. 在右侧面板点击“添加”按钮，搜索节点并填写角色、权重、置信度、证据后保存。
3. 已有映射卡片右侧提供编辑/删除按钮。
4. 在产业图谱中右键节点 →“关联行业”，也可以把当前节点关联到新行业。

### 4. 快速添加草稿节点（最小阻力入口）

当只需要先记录一个名称、后续再补全定义和证据时，使用 `quick-node`：

```bash
# 只提供中文名
python cli/arachne_cli.py quick-node --name-zh "激光雷达"

# 同时提供中英文和类型
python cli/arachne_cli.py quick-node --name-zh "激光雷达" --name-en "LiDAR" --entity-type system --notes "待 AI 补全定义"
```

系统会：
- 自动生成 `draft_{uuid}` 占位 `node_id`
- 默认 `entity_type = unknown`、`confidence = LOW`、`status = PENDING`
- 定义留空，后续通过 `PUT /nodes/{node_id}` 补全

#### 查看草稿 / 待完善节点

```bash
python cli/arachne_cli.py query --draft-only
```

这会返回 `node_id` 以 `draft_` 开头、或 `status=PENDING`、或 `entity_type=unknown`、或定义缺失的节点，方便 AI 批量补全。

#### 通过前端界面快速添加

在产业图模式下，顶部搜索框右侧的 ⚡ 按钮可展开“快速添加草稿节点”表单，只需填写中文名或英文名即可创建。创建后的草稿节点会：
- 立即显示在图谱中（灰色 unknown 类型）
- 在节点详情页顶部显示“草稿节点 / 待完善”提示
- 通过搜索框右侧的 🔔 按钮查看所有草稿节点列表

### 5. 单独管理公司

```bash
# 列出公司
python cli/arachne_cli.py company list --search 禾赛

# 查看公司详情
python cli/arachne_cli.py company get hesai_technology

# 创建公司
python cli/arachne_cli.py company create --json company.json

# 更新公司
python cli/arachne_cli.py company update hesai_technology --json company_update.json

# 删除公司
python cli/arachne_cli.py company delete hesai_technology

# 查看公司临时子图
python cli/arachne_cli.py company subgraph hesai_technology

# 查看公司暴露
python cli/arachne_cli.py company exposures hesai_technology

# 添加节点暴露
python cli/arachne_cli.py company add-exposure hesai_technology --json exposure.json

# 删除节点暴露
python cli/arachne_cli.py company del-exposure hesai_technology hesai_technology_produce_lidar_system
```

### 6. 查询图谱

```bash
# 图谱统计
python cli/arachne_cli.py query --stats

# 列出所有节点
python cli/arachne_cli.py query --list-nodes

# 搜索节点
python cli/arachne_cli.py query --search 激光雷达

# 节点子图
python cli/arachne_cli.py query --subgraph lidar_system --depth 2

# 节点邻居
python cli/arachne_cli.py query --neighbors lidar_system
```

## 创建前检查：避免重复

使用 `query` 或 `industry`/`company` 命令检查目标是否已存在：

```bash
# 检查节点
python cli/arachne_cli.py query --search lidar_system

# 检查公司
python cli/arachne_cli.py company list --search hesai

# 检查行业
python cli/arachne_cli.py industry list --search 智能驾驶
```

如果实体已存在，而用户只想补充关系，请使用 `add-mapping`、`add-exposure` 或批量接口，不要重复创建实体。

## CLI 未直接覆盖的操作

当前 `arachne_cli.py` 未提供单独的节点/边/人员/事实关系管理命令。对于这些情况，推荐做法：

1. **节点和边**：整理为 `GraphRegistrationBatch`，使用 `submit` 命令批量提交。
2. **人员与事实关系**：CLI 暂不支持，可直接调用后端 API（参见 references/API_REFERENCE.md）作为补充。

## 常见错误处理

- `HTTP Error 422`：ID 格式错误、缺少必需证据、或枚举值错误。阅读错误详情。
- `HTTP Error 409`：节点/边/公司/行业 ID 重复。使用更新命令或跳过。
- `HTTP Error 404`：引用的节点/公司/行业尚未创建。先创建被引用实体。
- `Connection refused`：CLI 默认连接 `localhost:8005`，请确认服务已启动。

## 常用枚举值速查

| 字段 | 允许取值 |
|---|---|
| `entity_type` | `material`, `component`, `device`, `module`, `subsystem`, `system`, `platform`, `infrastructure`, `application_system`, `service`, `technology_capability`, `unknown` |
| `edge_namespace` | `industrial_flow`, `ontology` |
| `industrial_flow` 的 `edge_type` | `material_flow`, `composition`, `energy_flow`, `information_flow`, `capability_supply`, `service_flow` |
| `ontology` 的 `edge_type` | `alias_of`, `is_a`, `variant_of`, `related_term` |
| `status` | `ACTIVE`, `PENDING`, `REJECTED`, `ARCHIVED` |
| `confidence` | `HIGH`, `MEDIUM`, `LOW` |
| `industry_type` | `formal_industry`, `curated_view`, `theme_view` |
| `company_type` | `public`, `private`, `state_owned`, `startup`, `unknown` |
| `activity_type` | `rnd`, `design`, `manufacture`, `produce`, `integrate`, `operate`, `provide_service`, `procure`, `use`, `unknown` |

完整 CLI 命令列表见 references/CLI_REFERENCE.md，底层 API schema 和枚举见 references/API_REFERENCE.md。
