# Batch 002 产业图构建日志

## 任务概述
为 `data/stock_batches/batch_002.json` 中的10家深圳上市公司构建产业实体图和公司视图。

## 涉及公司

| 股票代码 | 公司简称 | 公司ID | 核心业务 |
|---|---|---|---|
| 000014.SZ | 沙河股份 | shahe_property | 房地产开发、物业租赁、物业管理 |
| 000016.SZ | *ST康佳A | konka_group | 彩电、白电、半导体、PCB |
| 000017.SZ | 深中华A | shenzhonghua_a | 珠宝黄金、自行车、锂电池材料 |
| 000019.SZ | 深粮控股 | shenliang_holdings | 粮油贸易、仓储、加工、茶叶 |
| 000020.SZ | 深华发A | shenhuafa_a | 液晶显示器、注塑件、电路板 |
| 000021.SZ | 深科技 | shenzhen_kaifa | 存储半导体封测、高端制造、智能电表 |
| 001872.SZ | 招商港口 | cms_port | 港口装卸、保税仓储、航运 |
| 000025.SZ | 特力A | teli_a | 珠宝零售、汽车销售/维修/检测 |
| 000026.SZ | 飞亚达 | fiyta | 手表制造、机芯研发、名表连锁零售 |
| 000027.SZ | 深圳能源 | shenzhen_energy | 煤电/气电/风电/光伏/水电/垃圾发电、燃气供应 |

## 数据来源
- **Tushare**: 获取了各公司的基本资料、财务指标（扣非净利润）和主营构成（按产品/行业）。
- **网络搜索**: 确认了深科技的存储半导体封测产业链地位（长鑫存储核心封测厂商）、飞亚达的自主机芯技术、深圳能源的清洁能源装机结构等关键信息。
- **年报/公开资料**: 所有节点和边的证据均引用自公司2024年年报或行业常识。

## 产业图构建成果

### 新建产业节点
本次共新建 **58个产业节点**（原计划55个，修复过程中补充3个）。

**按类别划分：**

| 类别 | 代表节点 | 数量 |
|---|---|---|
| 建筑材料 | 螺纹钢、冷轧钢板、不锈钢 | 3 |
| 家电/消费电子 | 彩色电视机、电冰箱、洗衣机、手机 | 4 |
| 电子/半导体 | 印制电路板、覆铜板、半导体器件、显示模组、DRAM芯片、NAND Flash芯片、内存条模组、闪存盘、封装基板、硬盘驱动器、磁头、硬盘盘片 | 12 |
| 珠宝/钟表 | 贵金属、黄金珠宝、手表、手表机芯、钟表零部件 | 5 |
| 自行车 | 自行车、电动自行车 | 2 |
| 粮油食品 | 农产品、粮油、茶叶、调味品、食品原料、粮食仓储服务、粮食加工 | 7 |
| 港口物流 | 集装箱、散杂货、港口运营服务、集装箱装卸服务、保税仓储服务、航运服务 | 6 |
| 汽车服务 | 汽车销售服务、汽车维修保养服务、汽车检测服务、珠宝零售服务 | 4 |
| 能源 | 煤炭、电力、燃煤发电、燃气发电、风力发电、光伏发电、水力发电、垃圾焚烧发电、污泥处理、污水处理、城市燃气供应、电力输送、电力配送 | 13 |
| 建筑/地产服务 | 建筑设计服务 | 1 |
| 其他 | 包装材料、塑胶原料等（复用已有） | - |

### 新建/更新产业流边
本次共涉及 **63条产业流边**，最终成功创建/更新 **58条**。

**关键产业链：**

1. **房地产开发链**: 土地 → 建筑设计服务 → 建筑施工服务(水泥+螺纹钢输入) → 商品住宅/商业地产 → 物业管理服务/住房租赁服务
2. **家电制造链**: 半导体器件/PCB/显示模组/冷轧钢板/塑胶原料 → 彩电/冰箱/洗衣机
3. **存储半导体链**: 石英砂 → 硅材料 → 存储晶圆 → DRAM芯片/NAND Flash芯片 → 内存条模组/U盘；磁头+盘基片 → 硬盘驱动器
4. **粮油供应链**: 农产品 → 粮食仓储服务/粮食加工 → 粮油/食品原料/茶叶/调味品
5. **能源链**: 煤炭/天然气 → 燃煤发电/燃气发电 → 电力 → 电力输送 → 电力配送；天然气 → 城市燃气供应
6. **手表制造链**: 不锈钢/手表机芯/钟表零部件 → 手表 → 钟表零售服务
7. **港口物流链**: 航运服务 → 港口运营服务 → 集装箱装卸服务/保税仓储服务

### 公司视图构建成果

**10家公司** 全部创建成功，共建立 **47条 CompanyNodeExposure**。

| 公司 | 暴露节点数 | 核心暴露 |
|---|---|---|
| 沙河股份 | 4 | residential_property, commercial_property, property_management_service, housing_rental_service |
| 康佳 | 5 | color_tv, refrigerator, washing_machine, pcb_board, semiconductor_device |
| 深中华A | 4 | gold_jewelry, bicycle, electric_bicycle, lithium_battery_anode |
| 深粮控股 | 5 | grain_storage_service, grain_processing, grain_oil, tea, food_ingredient |
| 深华发A | 3 | lcd_monitor, injection_molding_part, pcb_board |
| 深科技 | 6 | dram_chip, nand_flash_chip, hard_disk_platter, magnetic_head, smart_meter, memory_dimm |
| 招商港口 | 4 | port_operation_service, container_handling_service, bonded_warehousing_service, shipping_service |
| 特力A | 4 | jewelry_retail_service, automotive_sales_service, automotive_maintenance_service, automotive_inspection_service |
| 飞亚达 | 4 | watch, watch_movement, watch_component, watch_retail_service |
| 深圳能源 | 8 | coal_power_generation, gas_power_generation, wind_power_generation, solar_power_generation, hydro_power_generation, waste_to_energy, city_gas_supply, electricity_power |

## 系统最终状态

```
Total nodes: 130
Total edges: 113
Node types: service=42, material=35, component=25, device=21, subsystem=5, application_system=1, infrastructure=1
Edge types: material_flow=42, service_flow=31, composition=28, energy_flow=7, capability_supply=4, information_flow=1
```

## 发现与问题

### 1. 程序Bug修复
在提交过程中发现 `neo4j_storage.py` 中的 `_evidence_to_db` 函数存在bug：
- **问题**: `update_edge` 调用 `_evidence_to_db(value)` 时，value 来自 `model_dump()` 的 dict 列表，但函数期望 `Evidence` 对象列表，导致 `AttributeError`。
- **影响**: batch_001 中已存在的5条边（cement_to_construction 等）在 update 时失败。
- **修复**: 修改 `_evidence_to_db` 以同时处理 `Evidence` 对象和 dict 两种格式。

### 2. 节点遗漏
在数据构造过程中遗漏了3个节点：
- `magnetic_head`（磁头）：深科技核心产品
- `hard_disk_platter`（硬盘盘片）：深科技核心产品
- `watch_retail_service`（钟表零售服务）：飞亚达核心业务

原因：在批量构造节点定义时，误将部分节点当作"已有节点"而跳过。后续通过 Neo4j 查询验证发现缺失，已补充创建。

### 3. 产业链交叉发现
- **深华发A 与 康佳** 在 PCB 产业节点交汇：两家公司均生产印制电路板（pcb_board），形成同业/相似关系的基础。
- **深中华A 与 特力A** 在黄金珠宝产业交汇：深中华A生产黄金珠宝，特力A运营珠宝零售服务，形成典型的上下游关系（produce → retail）。
- **沙河股份 与 batch_001 地产公司** 在房地产产业链上高度重叠，大量复用了已有节点（land, cement, construction_service, residential_property 等）。

### 4. 设计启发
- **能源企业的节点暴露策略**: 深圳能源同时运营6种发电方式和城市燃气供应，其暴露关系数量最多（8条）。这提示对于综合性能源集团，需要细化到具体发电类型（煤电、气电、风电、光伏、水电、垃圾发电），而不能简单用一个"电力生产"节点概括，否则无法体现其在新能源转型中的产业结构。
- **服务类节点的必要性**: 本次新建了大量服务类节点（港口运营、汽车销售、珠宝零售、电力输送/配送等），验证了系统设计中 "service" 作为 entity_type 的重要性。产业图不仅包含物理产品，也必须包含各类生产性/流通性服务。
- **证据的重要性**: 所有节点和边均附有证据（年报引用或行业常识），这保证了产业图的可审计性和可信度。在批量提交时，证据字段的序列化兼容性需要特别注意。

## 待后续完善
- 可为 batch_002 的公司构建 **inferred_industrial_relation**（由产业图推导的公司间上下游关系）。例如：深中华A（锂电池负极材料）→ 深中华A（电动自行车）已有产业链关系，但公司间关系尚未推导。
- 可为深圳能源的 **sludge_treatment**（污泥处理）和 **waste_water_treatment**（污水处理）补充暴露关系（当前未暴露，因年报中提及但收入占比不明确）。
