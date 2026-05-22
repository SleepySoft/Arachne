# Arachne 系统构建操作日志

## 日期：2026-05-21 ~ 2026-05-22

---

## 阶段一：基础系统构建

### 1.1 后端（FastAPI + Neo4j 架构）

- **Schema 迁移**：将 `core_schema.py` 完整迁移至 `backend/app/models/schemas.py`
  - 包含 6 个枚举类型、12 个 Pydantic 模型
  - 添加了 `IndustrialNodeCreate/Update`、`IndustrialFlowEdgeCreate/Update`、`OntologyEdgeCreate/Update` 等 DTO
- **存储层**：实现 `neo4j_storage.py`，封装全部 Cypher 查询（异步驱动）
- **内存 Fallback**：因环境无法连接 Neo4j，实现 `memory_storage.py` 作为 fallback
  - 保持与 neo4j_storage 完全相同的函数签名
  - 使用 Python 字典实现图遍历、子图查询、路径搜索
- **服务层**：`graph_service.py` 实现节点/边 CRUD、批量处理、冲突检测
- **路由层**：`nodes.py`、`edges.py`、`batches.py`、`query.py` 四个路由模块
- **API 验证**：`/health` 200 OK，`/api/v1/docs` Swagger UI 正常

### 1.2 前端（React + TypeScript + Cytoscape.js）

- **技术栈**：React 18 + TypeScript + Vite + Tailwind CSS + Cytoscape.js + dagre 布局
- **核心组件**：
  - `GraphCanvas.tsx`：Cytoscape.js 图可视化，支持 dagre 自动布局
  - `FilterPanel.tsx`：按关系命名空间、实体类型、状态、置信度过滤
  - `SearchPanel.tsx`：实时搜索节点（名称/别名）
  - `NodeDetail/EdgeDetail`：点击详情面板
  - `NodeForm/EdgeForm`：增删改查表单
  - `BatchUploader.tsx`：JSON 批量上传
- **构建验证**：`npm run build` 通过，生成 `dist/` 目录

### 1.3 CLI 工具

- **路径**：`cli/arachne_cli.py`
- **功能**：
  - `submit <json_file>`：提交 GraphRegistrationBatch
  - `query --stats`：图统计
  - `query --subgraph <node_id> --depth N`：子图查询
  - `query --neighbors <node_id>`：邻接查询
  - `query --list-nodes --search <关键词>`：节点搜索

---

## 阶段二：Prompt 设计

### 2.1 发现+分析 Prompt（`prompts/discovery_analysis.md`）

- **目标**：对候选实体进行深度分析，决定新建/合并/拒绝
- **核心流程**：
  1. 查询已有实体（名称/别名匹配）
  2. 判断别名 → merge_alias
  3. 判断等价 → merge_duplicate
  4. 判断子类 → create_subclass + is_a
  5. 判断变体 → create_variant + variant_of
  6. 判断公司/概念/标签 → reject
- **关键约束**：分类不是关系、名称不是实体、拒绝规则明确

### 2.2 信息提取 Prompt（`prompts/information_extraction.md`）

- **目标**：从行业资料中提取产业实体和关系
- **实体提取范围**：材料、部件、器件、模块、系统、平台、服务
- **关系提取**：
  - 6 类产业流关系（material_flow, composition, energy_flow, information_flow, capability_supply, service_flow）
  - 4 类本体关系（alias_of, is_a, variant_of, related_term）
- **输出格式**：标准 GraphRegistrationBatch JSON

### 2.3 提交方式 Prompt（`prompts/submission.md`）

- **目标**：指导将分析结果格式化为标准提交格式
- **节点规范**：node_id 命名规则、definition 质量要求、entity_type 选择
- **Evidence 规范**：HIGH/ACTIVE 必须有 evidence
- **关系规范**：方向统一、禁止自环、alias_of description 要求
- **提交方式**：CLI 工具 / curl / 前端批量上传

---

## 阶段三：数据准备与图谱构建

### 3.1 数据来源

- **国家统计局**：GB/T 4754-2017《国民经济行业分类》
- **工信部/国家统计局**：《战略性新兴产业分类（2018）》《工业战略性新兴产业分类目录（2023）》
- **处理方式**：从行业分类中"解读"底层产业实体和产业链关系，而非直接导入分类名称

### 3.2 设计原则

- ❌ 不直接登记行业分类名称（如"高端装备制造产业"是统计口径，不是实体）
- ✅ 从分类中提取底层实体（如硅晶圆、锂电池电芯、数控机床）
- ✅ 建立实体间的产业流关系（上游→下游）
- ✅ 拒绝公司/概念/标签，保持底层事实图的纯净

### 3.3 构建的产业链

**产业链 A：半导体/电子信息**
```
工业硅 → 多晶硅 → 单晶硅锭 → 硅晶圆 → 半导体芯片
                                          ↓
显示面板 ←—— 智能手机 / 服务器 → 数据中心 → 云计算平台
PCB ←———
```

**产业链 B：新能源电池/电动汽车**
```
锂矿石 → 碳酸锂 → 正极材料 ─┐
              负极材料 ───┼→ 锂电池电芯 → 动力电池包 ──→ 电动汽车
              电解液 ────┤                              ↑
              隔膜 ──────┘                    驱动电机 ← 永磁材料 ← 稀土
                                              电机控制器 ← 芯片
                                              ↑
                                              钢材 ← 粗钢 ← 生铁 ← 铁矿石/焦炭
```

**产业链 C：光伏发电**
```
工业硅 → 多晶硅 → 太阳能电池 → 光伏组件 → 光伏逆变器
```

**产业链 D：风力发电**
```
稀土 → 永磁材料 → 风力发电机组
        ↑
      钢材 ───────────────────┘
```

**产业链 E：智能制造**
```
钢材 → 数控机床 ──→ 工业机器人
芯片 ─────────────→
```

### 3.4 种子数据统计

| 指标 | 数值 |
|------|------|
| 节点总数 | 36 |
| 边总数 | 37 |
| 材料 (material) | 17 |
| 设备 (device) | 6 |
| 部件 (component) | 3 |
| 模块 (module) | 2 |
| 系统 (system) | 6 |
| 基础设施 (infrastructure) | 1 |
| 平台 (platform) | 1 |
| 物质流 (material_flow) | 15 |
| 组成关系 (composition) | 17 |
| 能量流 (energy_flow) | 2 |
| 能力供给 (capability_supply) | 2 |
| 信息流 (information_flow) | 1 |
| 拒绝/待确认 | 7 |

### 3.5 被拒绝的项（设计原则体现）

| 候选词 | 拒绝原因 | 处理方式 |
|--------|---------|---------|
| 高端装备制造产业 | 统计分类口径，不是实体 | 作为视图层标签 |
| 新能源汽车产业 | 统计分类口径，不是实体 | 作为视图层标签 |
| 新一代信息技术产业 | 政策分类口径，不是实体 | 作为视图层标签 |
| 工业互联网 | 技术领域概念，非具体实体 | 细化为平台/网关后可登记 |
| 人工智能 | 宽泛技术领域，非具体实体 | 细化为AI芯片/模型后可登记 |
| 华为 | 公司实体 | 公司层未来映射 |
| 比亚迪 | 公司实体 | 公司层未来映射 |

---

## 阶段四：系统启动与数据验证

### 4.1 启动状态

- **后端**：`http://localhost:8000`（内存存储模式，PID: 48160）
- **前端**：`http://localhost:3000`（Vite preview，PID: 15712）
- **API 文档**：`http://localhost:8000/api/v1/docs`

### 4.2 数据导入

```bash
python cli/arachne_cli.py submit data/seed_industry_graph.json
```

**导入结果**：
- nodes_created: 36
- edges_created: 37
- rejected_or_pending_stored: 7
- errors: []

### 4.3 验证查询

**图统计**：
```bash
python cli/arachne_cli.py query --stats
```
结果：36 节点，37 边，全 ACTIVE 状态，全 HIGH 置信度

**子图查询（电动汽车，深度2）**：
```bash
python cli/arachne_cli.py query --subgraph electric_vehicle --depth 2
```
返回节点：电动汽车、动力电池包、驱动电机、电机控制器、钢材、锂电池电芯、永磁材料、粗钢、半导体芯片
返回边：energy_flow、composition、material_flow 等 10 条关系

---

## 阶段五：后续建议

### 5.1 Neo4j 部署

当前使用内存存储（重启后数据丢失）。建议用户环境网络恢复后：

```bash
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/arachne123 neo4j:5-community
```

然后修改 `backend/app/services/graph_service.py`：
```python
from app.services import neo4j_storage  # 恢复 Neo4j 存储
```

重新导入种子数据即可持久化。

### 5.2 扩展方向

1. **半导体产业链细化**：增加光刻机、EDA软件、IP核等节点
2. **生物产业链**：从战略性新兴产业分类中提取生物医药、基因编辑等
3. **航空航天产业链**：航空发动机、卫星、火箭等
4. **公司层映射**：实现 Company → Activity → Entity 的映射层
5. **事件系统**：事件 → 实体 → 影响传播

### 5.3 Agent 工作流

建议的自动化流程：
```
资料输入 → 信息提取 Prompt → 发现分析 Prompt（查询已有实体）→ 生成 JSON → 提交方式 Prompt → CLI submit → 人工复核
```
