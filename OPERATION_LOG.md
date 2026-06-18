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

---

## 阶段六：上市公司产业图批量构建（Batches 100-105）

### 6.1 构建概况

基于 tushare 沪深A股数据，对股票代码 600764.SH - 600838.SH 范围内的上市公司进行产业图批量构建。

| 批次 | 股票代码范围 | 公司数 | 新建节点 | 新建边 | 新建暴露 |
|------|-------------|--------|---------|--------|---------|
| 100 | 600764-600776 | 10 | 13 | 0 | 34 |
| 101 | 600777-600789 | 10 | 1 | 1 | 34 |
| 102 | 600790-600800 | 10 | 5 | 1 | 27 |
| 103 | 600801-600814 | 10 | 6 | 2 | 28 |
| 104 | 600815-600825 | 10 | 5 | 1 | 21 |
| 105 | 600826-600838 | 10 | 6 | 1 | 19 |
| **合计** | — | **60** | **36** | **6** | **163** |

### 6.2 图统计（Batches 100-105 完成后）

```
总节点数: 1107
总边数: 534
```

### 6.3 关键发现

1. **数据库信息滞后问题**：tushare 的 `main_business` 字段存在明显滞后，特别是发生重大资产重组的公司：
   - **宇通重工 (600817)**：数据库标注"集成电路/家电"，实际为"环卫装备/矿机/工程机械"
   - **金开新能 (600821)**：数据库标注"商业零售"，实际已转型为"风力发电/光伏发电"
   
   解决方式：通过 Web 搜索（新浪财经、公司年报）交叉验证主营业务信息。

2. **节点复用率高**：60家公司共产生163条暴露关系，仅新建36个产业节点，说明系统中已有节点覆盖了大部分产业实体。

3. **产业链补全效应**：
   - 钢铁产品分类：`steel_strand`（钢绞线）、`steel_long_product`（长材）
   - 水泥产业链：`clinker`（水泥熟料）
   - 清洁能源：`wind_power_generation`（风力发电）
   - 化纤产业链：`nylon_industrial_yarn`（尼龙工业丝）
   - 城市交通：`metro_operation`（地铁运营）
   - 医药流通：`pharmaceutical_wholesale`（医药批发）

4. **构建方式**：每批次采用两步提交——先提交 `GraphRegistrationBatch`（补充缺失节点和边），再提交 `BusinessRegistrationBatch`（注册公司和暴露关系），确保产业节点先存在于图中，再建立公司映射。

---

## 阶段七：上市公司产业图批量构建（Batches 106-110）

### 7.1 构建概况

基于 tushare 沪深A股数据，对股票代码 600839.SH - 600897.SH 范围内的上市公司进行产业图批量构建。

| 批次 | 股票代码范围 | 公司数 | 新建节点 | 新建边 | 新建暴露 |
|------|-------------|--------|---------|--------|---------|
| 106 | 600839-600850 | 10 | 6 | 0 | 27 |
| 107 | 600851-600862 | 10 | 6 | 0 | 22 |
| 108 | 600863-600873 | 10 | 7 | 0 | 28 |
| 109 | 600874-600884 | 10 | 6 | 0 | 22 |
| 110 | 600885-600897 | 10 | 13 | 3 | 29 |
| **合计** | — | **50** | **38** | **3** | **128** |

### 7.2 图统计（Batches 106-110 完成后）

```
总节点数: 1145
总边数: 537
```

### 7.3 关键新建节点

| 节点 | 类型 | 代表性公司 | 产业链意义 |
|------|------|-----------|-----------|
| `compressor` | device | 四川长虹 | 家电核心零部件 |
| `sewing_machine` | device | 上工申贝 | 纺织设备消费端 |
| `lead_acid_battery` | device | 万里股份 | 传统储能电池 |
| `intelligent_building` | system | 电科数字 | 楼宇智能化 |
| `security_service` | service | 航天长峰 | 安防安保服务 |
| `human_resource_service` | service | 北京人力 | 人力资源外包 |
| `aviation_new_material` | material | 中航高科 | 航空复合材料 |
| `recombinant_human_insulin` | material | 通化东宝 | 糖尿病治疗药物 |
| `nucleotide` | material | 星湖科技 | 食品鲜味剂 |
| `carbon_fiber_composite_conductor` | component | 远东股份 | 新型输电导线 |
| `petroleum_engineering_service` | service | 石化油服 | 油气工程服务 |
| `cheese` | material | 妙可蓝多 | 乳制品细分品类 |
| `liquid_milk` | material | 妙可蓝多/伊利 | 乳制品主力品类 |
| `lithium_ion_battery_material` | material | 杉杉股份 | 锂电负极材料 |
| `relay` | component | 宏发股份 | 电力控制器件 |
| `low_voltage_electrical` | component | 宏发股份 | 低压配电器件 |
| `contactor` | component | 宏发股份 | 电磁控制开关 |
| `aero_engine` | system | 航发动力 | 航空发动机 |
| `electronic_aluminum_foil` | material | 新疆众和 | 电容器核心材料 |
| `formed_foil` | material | 新疆众和 | 电容器中间材料 |
| `etched_foil` | material | 新疆众和 | 电容器原材料 |
| `air_ground_service` | service | 厦门空港 | 机场地勤服务 |

### 7.4 新增产业链

**铝电解电容器材料链**：
```
aluminum_ingot → electronic_aluminum_foil → etched_foil → formed_foil
```

### 7.5 数据勘误记录

- **电科芯片 (600877)**：tushare 标注"摩托车"，实际为"集成电路设计/制造/销售"

### 7.6 累计统计（Batches 100-110）

| 指标 | 数值 |
|------|------|
| 总批次 | 11个 (100-110) |
| 总 Company | 110家 |
| 总新建节点 | 74个 |
| 总新建边 | 9条 |
| 总新建暴露 | 291条 |
| 图节点总数 | 1145 |
| 图边总数 | 537 |

---

## 阶段八：上市公司产业图批量构建（Batches 111-115）

### 8.1 构建概况

| 批次 | 股票代码范围 | 公司数 | 新建节点 | 新建边 | 新建暴露 |
|------|-------------|--------|---------|--------|---------|
| 111 | 600900, 600960, 600963, 600966, 600967, 600969, 600975, 600976, 600980, 600985 | 10 | 17 | 0 | 31 |
| 112 | 600986, 600988, 600990, 600992, 600993, 600995, 600997, 002017, 002003, 002004 | 10 | 16 | 0 | 27 |
| 113 | 002005-002015 | 10 | 17 | 0 | 26 |
| 114 | 002016-002027 | 10 | 16 | 0 | 25 |
| 115 | 002028-002037 | 10 | 23 | 0 | 33 |
| **合计** | — | **50** | **89** | **0** | **142** |

### 8.2 图统计（Batches 111-115 完成后）

```
总节点数: 1234
总边数: 537
```

### 8.3 关键新建节点

| 节点 | 类型 | 代表性公司 | 产业链意义 |
|------|------|-----------|-----------|
| `piston` | component | 渤海汽车 | 发动机核心零部件 |
| `armored_vehicle` | system | 内蒙一机 | 军工地面装备 |
| `railway_vehicle` | system | 内蒙一机 | 轨道交通装备 |
| `ferrite` | material | 北矿科技 | 磁性材料基础 |
| `gold` | material | 赤峰黄金 | 贵金属 |
| `palladium` | material | 赤峰黄金 | 汽车催化剂金属 |
| `rhodium` | material | 赤峰黄金 | 贵金属催化剂 |
| `radar` | device | 四创电子 | 国防电子信息 |
| `energy_storage` | service | 南网储能 | 新能源配套 |
| `button` | component | 伟星股份 | 服装辅料 |
| `zipper` | component | 伟星股份 | 服装辅料 |
| `laser_marking_machine` | device | 大族激光 | 激光加工设备 |
| `laser_welding_machine` | device | 大族激光 | 激光加工设备 |
| `human_serum_albumin` | material | 华兰生物 | 血液制品 |
| `electrolytic_capacitor_paper` | material | 凯恩股份 | 电容器特种纸 |
| `clean_energy` | service | 协鑫能科 | 清洁能源服务 |
| `home_appliance_retail` | service | ST易购 | 家电零售渠道 |
| `electronics_retail` | service | ST易购 | 3C零售渠道 |
| `connector` | component | 航天电器 | 电子连接器 |
| `aircraft_maintenance` | service | 海特高新 | 航空MRO |
| `power_automation_protection` | device | 思源电气 | 电网保护 |
| `high_voltage_switch` | device | 思源电气 | 输配电开关 |
| `tire_mold` | device | 巨轮智能 | 轮胎核心模具 |
| `cookware` | device | 苏泊尔 | 厨房炊具 |
| `waste_incineration_power_generation` | service | 旺能环境 | 垃圾资源化 |
| `gas_stove` | device | 华帝股份 | 厨电核心产品 |
| `range_hood` | device | 华帝股份 | 厨电核心产品 |
| `camera_module` | component | 联创电子 | 手机光学模组 |
| `touch_display_module` | component | 联创电子 | 触显一体化 |
| `detonator` | material | 保利联合 | 民爆器材 |
| `industrial_explosive` | material | 保利联合 | 工程爆破 |

### 8.4 累计统计（Batches 100-115）

| 指标 | 数值 |
|------|------|
| 总批次 | 16个 (100-115) |
| 总 Company | 160家 |
| 总新建节点 | 163个 |
| 总新建边 | 9条 |
| 总新建暴露 | 433条 |
| 图节点总数 | 1234 |
| 图边总数 | 537 |

---

## Phase 9 — Batches 116-120 提交 (2026-05-28)

### 9.1 批次提交记录

| 批次 | 公司数 | 新建节点 | 新建边 | 新建暴露 | 状态 |
|------|--------|---------|--------|---------|------|
| Batch 116 | 10 | 43 | 43 | 70 | ✅ 成功 |
| Batch 117 | 10 | 23 | 20 | 45 | ✅ 成功 |
| Batch 118 | 10 | 37 | 30 | 56 | ✅ 成功 |
| Batch 119 | 10 | 26 | 22 | 58 | ✅ 成功 |
| Batch 120 | 10 | 28 | 27 | 55 | ✅ 成功 |
| **合计** | **50** | **157** | **142** | **284** | ✅ |

### 9.2 提交后图统计

```
总节点数: 1391
总边数: 679
```

### 9.3 关键新建节点

| 节点 | 类型 | 代表性公司 | 产业链意义 |
|------|------|-----------|-----------|
| `gene_engineering_drug` | material | 双鹭药业 | 生物制药核心技术 |
| `modified_plastic` | material | 金发科技 | 新材料改性 |
| `gas_turbine_power` | service | 中国动力 | 船舶动力系统 |
| `lead_zinc_alloy` | material | 株冶集团 | 有色金属冶炼 |
| `offshore_wind_power_equipment` | system | 宝胜股份 | 海上风电装备 |
| `health_examination` | service | 美年健康 | 健康体检服务 |
| `audio_system` | system | 国光电器 | 电声设备 |
| `smart_chip` | component | 紫光国微 | 智能安全芯片 |
| `international_engineering_contracting` | service | 中工国际 | 海外工程承包 |
| `commercial_bank` | service | 中国银行 | 商业银行服务 |
| `crystalline_silicon_solar_cell` | component | 横店东磁 | 光伏电池片 |
| `railway_transport` | service | 大秦铁路 | 煤炭铁路专线 |
| `spandex` | material | 华峰化学 | 氨纶纤维 |
| `refractory_material` | material | 瑞泰科技 | 熔铸耐火材料 |
| `artificial_intelligence` | technology_capability | 东华软件 | AI技术应用 |

### 9.4 累计统计（Batches 100-120）

| 指标 | 数值 |
|------|------|
| 总批次 | 21个 (100-120) |
| 总 Company | 210家 |
| 总新建节点 | 320个 |
| 总新建边 | 151条 |
| 总新建暴露 | 717条 |
| 图节点总数 | 1391 |
| 图边总数 | 679 |


## 10. Batches 121-125 提交记录 (2026-05-28)

### 10.1 批次提交记录

| 批次 | 公司数 | 新建节点 | 新建边 | 新建暴露 | 状态 |
|------|--------|---------|--------|---------|------|
| Batch 121 | 10 | 24 | 23 | 59 | ✅ 成功 |
| Batch 122 | 10 | 29 | 26 | 55 | ✅ 成功 |
| Batch 123 | 10 | 28 | 14 | 55 | ✅ 成功 |
| Batch 124 | 10 | 26 | 10 | 59 | ✅ 成功 |
| Batch 125 | 10 | 34 | 25 | 62 | ✅ 成功 |
| 修复节点 | - | 26 | - | - | ✅ 成功 |
| 修复边 | - | - | 51 | - | ✅ 成功 |
| **合计** | **50** | **167** | **149** | **290** | ✅ |

> 注：原始提交产生 51 条边错误（缺失父级基础设施节点），已通过补充 26 个基础设施节点和 51 条修复边全部解决。

### 10.2 提交后图统计

```
总节点数: ~1558
总边数: ~828
```

### 10.3 关键新建节点

| 节点 | 类型 | 代表性公司 | 产业链意义 |
|------|------|-----------|-----------|
| `air_transport` | service | 中国国航 | 航空运输服务 |
| `carbon_black` | material | 黑猫股份 | 橡胶补强剂 |
| `power_battery` | component | 国轩高科 | 动力电池 |
| `wind_turbine_blade` | component | 中材科技 | 风电叶片 |
| `pvc_resin` | material | 中泰化学 | 聚氯乙烯树脂 |
| `aluminum_die_casting` | component | 广东鸿图 | 汽车压铸件 |
| `industrial_explosive` | material | 易普力 | 民用爆破器材 |
| `zipper` | component | 浔兴股份 | 服饰辅料 |
| `railway_passenger_transport` | service | 广深铁路 | 铁路客运 |
| `construction_steel` | material | 三钢闽光 | 建筑钢材 |
| `lithium_separator_pipe` | component | 沧州明珠 | 锂电池隔膜 |

### 10.4 累计统计（Batches 100-125）

| 指标 | 数值 |
|------|------|
| 总批次 | 26个 (100-125) |
| 总 Company | 260家 |
| 总新建节点 | ~487个 |
| 总新建边 | ~300条 |
| 总新建暴露 | 1007条 |
| 图节点总数 | ~1558 |
| 图边总数 | ~828 |


## Phase 11 — 架构重构：废弃公司视图，确立两域架构 (2026-05-30)

### 11.1 设计决策

**原因**：
1. **探索优于全量**：公司视图的批量计算（全量公司间上下游推导）成本高、时效性差，实际使用中动态计算单公司产业上下文更具价值
2. **域边界纯净**：新架构只有两个持久化域——**产业图**（Industrial Graph）和**事实关系图**（Factual Graph）。公司视图作为第三域会造成概念混杂，破坏浏览时的单域隔离原则
3. **事实关系图承载公司关联**：公司-公司之间的业务关系（供应商、客户、投资方等）将通过事实关系图采集和存储，而非从产业图推导

**新架构**：
```
┌─────────────────────────────────────────┐
│  域A: 产业图（Industrial Graph）         │
│  Neo4j: :IndustrialNode                 │
│         :INDUSTRIAL_FLOW / :ONTOLOGY    │
├─────────────────────────────────────────┤
│  域B: 事实关系图（Factual Graph）        │
│  Neo4j: :Person / :Company              │
│         :SHAREHOLDER_OF / :SPOUSE...    │
├─────────────────────────────────────────┤
│  桥接层: PG company_node_exposures      │
│  （跨域探索时应用层拼接，非Neo4j边）    │
└─────────────────────────────────────────┘
```

### 11.2 清理操作

| 操作 | 详情 |
|------|------|
| 移动文件 | `company_view_schema.py`, `company_view.py`(router), `company_view.py`(service), `company_view_neo4j.py` → `recycled/company_view/` |
| 移除引用 | `main.py` 中注销 `/api/v1/company-view` router |
| 移除触发 | `business_batches.py` 中移除提交后自动触发 `company_view_compute` 的逻辑 |
| 移除表 | `database_postgres.py` 中移除 `company_view_versions` 表创建 |
| 清理脚本 | `export_db.py` / `import_db.py` 移除 `--no-company-view` 选项及公司视图数据导入导出逻辑 |
| Neo4j清理 | 删除 `:INFERRED_UPSTREAM` 关系 **17,168** 条，删除 `:Company` 节点 **1,300** 个 |

### 11.3 保留的能力

- **公司CRUD** (`/api/v1/companies/*`)：完整保留，作为事实关系图的数据源
- **公司-产业暴露** (`company_node_exposures`)：保留在PG中，作为两域之间的桥接
- **单公司产业上下文**：`GET /api/v1/companies/{id}/industrial-context` 已在 `backend/app/routers/explore.py` 实现（不持久化，实时计算）

### 11.4 后续计划（2026-06-15 更新：均已实现后端）

1. **Phase 11b**: 事实关系图 Schema + Storage + Router（Person + 三类关系）已在 `backend/app/models/factual_graph_schema.py`、`backend/app/services/factual_graph_storage.py`、`backend/app/routers/factual_graph.py` 实现
2. **Phase 11c**: 跨域探索接口（统一的 `/api/v1/explore/*`）已在 `backend/app/routers/explore.py` 实现


---

## 日期：2026-06-16

### 半导体公司研究工作流第 4 步：产业链分类与研报生成

- **目标**：按产业链上中下游分类整理已录入的 93 家国内外半导体公司，生成研报文档。
- **执行内容**：
  1. 补充半导体产业图缺失的上下游 `industrial_flow` 关系 36 条，覆盖材料→硅片、晶圆→制造、芯片→封测、芯片→终端应用等链路。
  2. 基于 PostgreSQL 中 `created_at >= 2026-06-18` 的 131 条暴露关系，筛选出 93 家半导体公司。
  3. 按 **上游材料、上游设备、EDA/IP、芯片设计、晶圆制造、封装测试** 六大环节进行分类。
  4. 生成 Markdown 研报：`docs/semiconductor_company_research_report.md`。
- **产出统计**：
  - 公司总数：93
  - 暴露关系：131
  - 按国家/地区分布：CN 43、US 23、JP 13、TW 4、KR 2、NL 2、CH 1、DE 1、FR 1、GB 1、IE 1、IL 1
- **相关脚本**：
  - `backend/add_semiconductor_relations.py`：补充产业图关系
  - `backend/generate_semiconductor_report.py`：生成研报


---

## 日期：2026-06-16（追加）

### 专题补充：六氟化钨（WF6）与替代路线

- **背景**：用户关注近期热门的六氟化钨供应链及替代路线。
- **研究工作**：
  1. 通过网络搜索梳理 WF6 在半导体 CVD/ALD 钨薄膜中的作用、供应风险（日本断供传闻）及氟污染瓶颈。
  2. 整理主要替代路线：五氯化钨（WCl5）、六氯化钨（WCl6）、六羰基钨（W(CO)6）、ALD 钼（Mo）薄膜。
  3. 在产业本体图中补充 7 个节点与 8 条产业流/本体关系，覆盖 WF6 → 钨薄膜 → 芯片及替代路线。
  4. 将新节点映射到 `semiconductor_industry`。
  5. 在 `docs/semiconductor_company_research_report.md` 末尾追加专题章节，分析国内已录入 93 家公司中的 WF6 相关布局与缺口。
- **关键结论**：
  - 已录入的 93 家公司中直接覆盖 WF6 合成/量产的标的稀缺；华特气体仅做纯化、雅克科技无 WF6 业务。
  - 后续若扩展半导体公司样本，建议补充中船特气、昊华科技、和远气体、金宏气体等电子特气龙头。
- **相关脚本**：
  - `backend/add_wf6_route.py`：补充产业图节点/关系
  - `backend/add_wf6_industry_mappings.py`：补充行业映射


---

## 日期：2026-06-16（追加 2）

### WF6 路线公司与物料关联补录

- **问题**：用户反馈专题中看不到关联公司，此前确实未将公司与 `tungsten_hexafluoride` 节点建立 `CompanyNodeExposure`。
- **补录公司**：
  - **液化空气（air_liquide）**：全球电子级 WF6 主要供应商，约 24% 供应能力
  - **林德（linde）**：全球电子级 WF6 主要供应商，约 21% 供应能力
  - **华特气体（huat_gas）**：根据客户需求供应纯化 WF6 产品（公司公开回应暂无合成产能）
- **依据**：Verified Market Reports 对 WF6 市场竞争格局的分析；华特气体投资者互动回复。
- **操作**：
  1. 通过 `POST /api/v1/companies/{id}/exposures` 新增 3 条暴露关系。
  2. 调整 `generate_semiconductor_report.py` 的日期过滤与上游材料节点列表，重新生成研报。
  3. 在研报专题中新增「已录入 93 家公司中的 WF6 关联企业」表格，并标注国内尚未录入的缺口玩家。
- **相关脚本**：
  - `backend/add_wf6_company_exposures.py`
  - `backend/generate_semiconductor_report.py`


---

## 日期：2026-06-16（追加 3）

### 前端节点关系面板优化

- **用户反馈**：节点详情里的「关联关系」区域看不到中文名字，且上游应放上面；点击关联节点应跳转并显示（即使被过滤器隐藏）。
- **改动内容**：
  1. `frontend/src/components/NodeEdgeList.tsx`
     - 拉取全量节点列表建立 `nodeMap`，用 `canonical_name_zh` 显示关联节点中文名。
     - 关联节点名称改为可点击按钮，点击后调用 `onSelectNode` 跳转到对应节点详情。
     - 调整顺序：**上游（incoming）放在上面，下游（outgoing）放在下面**。
     - 添加按钮样式（`text-cyan-400 hover:underline`），鼠标悬停显示 node_id。
  2. `frontend/src/components/NodeDetail.tsx`
     - 新增 `onSelectNode` prop，透传给 `NodeEdgeList`。
  3. `frontend/src/App.tsx`
     - 向 `NodeDetail` 传入 `handleNodeClick`，实现节点跳转。
  4. `frontend/src/components/GraphCanvas.tsx`
     - 高亮节点时先移除 `hidden` 类，确保被过滤器隐藏的节点能显示出来。
     - 对高亮节点的连接边做判断：若另一端点可见，则同步显示该边。
- **验证**：`npm run build` 通过，无 TypeScript 错误。


---

## 日期：2026-06-16（追加 4）

### 节点详情关联区域重构：折叠 + 关联公司/行业 + 异步加载

- **用户反馈**：节点详情里的「关联关系」区域需要做成可折叠；下方增加「关联公司」「关联行业」；查询慢时显示加载动画。
- **改动内容**：
  1. 新增 `frontend/src/components/NodeAssociations.tsx`
     - 用可折叠面板分别包裹：关联关系、关联公司、关联行业。
     - 「关联关系」默认展开，「关联公司/行业」默认收起，点击标题可展开/折叠。
     - 「关联公司」调用 `GET /api/v1/companies/by-node/{node_id}`，按需异步加载，显示 `Loader2` 转圈圈。
     - 「关联行业」调用 `GET /api/v1/industries/by-node/{node_id}`，按需异步加载。
     - 关联公司/行业条目显示中文名、国家/地区、活动类型/角色或行业类型/状态。
     - 公司/行业名称可点击，跳转对应详情面板。
  2. `frontend/src/components/NodeDetail.tsx`
     - 使用 `NodeAssociations` 替换原来的 `NodeEdgeList`。
     - 新增 `onSelectCompany`、`onSelectIndustry` props。
  3. `frontend/src/App.tsx`
     - 向 `NodeDetail` 传入 `handleSelectCompanyDetail` 和 `handleSelectIndustryDetail`。
- **验证**：`npm run build` 通过，无 TypeScript 错误。
