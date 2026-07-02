# Batch 003 产业图构建日志

## 任务概述

为 `data/stock_batches/batch_003.json` 中的 **10家上市公司** 构建产业实体图和公司视图。

## 涉及公司

| 股票代码 | 公司简称 | 公司ID | 核心业务 |
|---|---|---|---|
| 000028.SZ | 国药一致 | sinopharm_unified | 制药、医药批发零售 |
| 000029.SZ | 深深房A | shenzhen_fang_a | 房地产开发、物业租赁 |
| 000030.SZ | 富奥股份 | fawer_parts | 底盘/制动/传动/转向/电子/发动机附件 |
| 000031.SZ | 大悦城 | joy_city | 住宅、商业物业、工业物业、酒店 |
| 000032.SZ | 深桑达A | sunda_a | 高科技产业工程、大数据服务、通信设备 |
| 000034.SZ | 神州数码 | digital_china | IT硬件分销（笔记本/服务器/网络/存储） |
| 000035.SZ | 中国天楹 | china_tianying | 垃圾焚烧发电、环保装备、环卫服务、风电 |
| 000036.SZ | 华联控股 | hualian_holding | 房地产开发、物业租赁管理 |
| 000037.SZ | 深南电A | shennan_electric | 燃煤/燃气发电、供电供热、储能技术 |
| 000039.SZ | 中集集团 | cimc_group | 集装箱、半挂车、能源化工装备、海工装备 |

## 数据来源

- **Tushare**: 获取了各公司的基本资料、财务指标（ROE）、市值数据（daily_basic）。
- **网络搜索**: 核查了富奥股份六大产品系列、深桑达A高科技产业工程+中国电子云业务、中国天楹环保+新能源布局、中集集团各业务板块全球地位、国药一致医药批发零售结构等关键信息。
- **年报/公开资料**: 所有节点和边的证据均引用自公司2024/2025年年报或行业常识。

## 产业图构建成果

### 新建产业节点

本次共新建 **28个产业节点**。

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **医药** | pharmaceutical_raw_material | 医药原料药 | material | 国药一致 |
| **汽车零部件** | automotive_brake_system | 汽车制动系统 | subsystem | 富奥股份 |
| **汽车零部件** | automotive_transmission_system | 汽车传动系统 | subsystem | 富奥股份 |
| **汽车零部件** | automotive_steering_system | 汽车转向系统 | subsystem | 富奥股份 |
| **汽车零部件** | automotive_electronics | 汽车电子电器 | component | 富奥股份 |
| **汽车零部件** | automotive_engine_accessory | 汽车发动机附件 | component | 富奥股份 |
| **汽车零部件** | automotive_environment_system | 汽车环境系统 | subsystem | 富奥股份 |
| **地产** | industrial_property | 工业物业 | component | 大悦城 |
| **酒店** | hotel_operation_service | 酒店经营服务 | service | 大悦城 |
| **高科技工程** | high_tech_industrial_engineering | 高科技产业工程服务 | service | 深桑达A |
| **大数据** | big_data_service | 大数据服务 | service | 深桑达A |
| **IT服务** | information_system_integration | 信息系统集成服务 | service | 深桑达A |
| **通信** | communication_device | 通信设备 | device | 深桑达A |
| **电源** | module_power_supply | 模块电源 | component | 深桑达A |
| **IT设备** | laptop_computer | 笔记本电脑 | device | 神州数码 |
| **IT设备** | network_equipment | 网络设备 | device | 神州数码 |
| **IT设备** | storage_equipment | 存储设备 | device | 神州数码 |
| **IT设备** | office_equipment | 办公设备 | device | 神州数码 |
| **环保** | waste_incineration_equipment | 垃圾焚烧发电设备 | device | 中国天楹 |
| **环保** | municipal_waste_treatment | 城市生活垃圾处理服务 | service | 中国天楹 |
| **环保** | urban_sanitation_service | 城乡环卫一体化服务 | service | 中国天楹 |
| **能源** | heating_supply | 供热服务 | service | 深南电A |
| **能源** | energy_storage_technology | 储能技术服务 | service | 深南电A |
| **运输装备** | road_transport_vehicle | 道路运输车辆 | device | 中集集团 |
| **运输装备** | energy_chemical_equipment | 能源化工装备 | device | 中集集团 |
| **运输装备** | offshore_engineering_equipment | 海洋工程装备 | device | 中集集团 |
| **运输装备** | airport_equipment | 空港装备 | device | 中集集团 |
| **物流** | logistics_service | 物流服务 | service | 中集集团 |

### 已有节点复用

复用了现有图谱中的大量节点，包括：
- **医药链**: pharmaceutical_product, pharmaceutical_distribution, pharmaceutical_retail, medical_device
- **房地产链**: land, cement, construction_service, residential_property, commercial_property, property_management_service, housing_rental_service
- **汽车零部件链**: automotive_steel, automotive_aluminum, chassis_system, suspension_system
- **IT链**: it_hardware, it_distribution_service, server_hardware, semiconductor_device, display_module, software_license
- **环保/能源链**: waste_to_energy, wind_power_generation, coal_power_generation, gas_power_generation, electricity_power
- **港口物流链**: container, shipping_service

### 新建产业流边

本次共新建 **28条产业流边**，涵盖以下核心产业链：

1. **医药链**: pharmaceutical_raw_material → pharmaceutical_product; medical_device → pharmaceutical_distribution
2. **汽车零部件链**: automotive_steel → automotive_brake_system/transmission_system/steering_system/engine_accessory/environment_system; automotive_aluminum → automotive_brake_system
3. **地产链**: construction_service → industrial_property; industrial_property → property_management_service
4. **高科技/IT链**: server_hardware → big_data_service/information_system_integration; semiconductor_device → laptop_computer/network_equipment/storage_equipment; display_module → laptop_computer; it_hardware → office_equipment
5. **环保链**: waste_incineration_equipment → waste_to_energy; municipal_waste_treatment → waste_to_energy; urban_sanitation_service → municipal_waste_treatment
6. **能源链**: coal_power_generation/gas_power_generation → heating_supply; electricity_power → energy_storage_technology
7. **运输装备链**: steel_sheet → road_transport_vehicle; container/road_transport_vehicle/energy_chemical_equipment → logistics_service; offshore_engineering_equipment → shipping_service

### 公司视图构建成果

**10家公司** 全部创建成功，共建立 **45条 CompanyNodeExposure**。

| 公司 | 暴露节点数 | 核心暴露 |
|---|---|---|
| 国药一致 | 4 | pharmaceutical_product (produce), pharmaceutical_distribution (provide_service), pharmaceutical_retail (provide_service), medical_device (procure) |
| 深深房A | 3 | residential_property (produce), property_management_service (provide_service), housing_rental_service (provide_service) |
| 富奥股份 | 7 | chassis_system, automotive_brake_system, automotive_transmission_system, automotive_steering_system, automotive_electronics, automotive_engine_accessory, automotive_environment_system (全部 manufacture) |
| 大悦城 | 4 | residential_property, commercial_property, industrial_property (produce), hotel_operation_service (operate) |
| 深桑达A | 5 | high_tech_industrial_engineering, big_data_service, information_system_integration (provide_service), communication_device, module_power_supply (manufacture) |
| 神州数码 | 5 | it_distribution_service (provide_service), server_hardware, network_equipment, storage_equipment, laptop_computer (procure) |
| 中国天楹 | 4 | waste_to_energy (operate), waste_incineration_equipment (manufacture), urban_sanitation_service (provide_service), wind_power_generation (operate) |
| 华联控股 | 3 | residential_property (produce), property_management_service, housing_rental_service (provide_service) |
| 深南电A | 4 | coal_power_generation, gas_power_generation (operate), heating_supply, energy_storage_technology (provide_service) |
| 中集集团 | 6 | container, road_transport_vehicle, energy_chemical_equipment, offshore_engineering_equipment, airport_equipment (manufacture), logistics_service (provide_service) |

## 系统最终状态

```
Total nodes: 158 (新增28)
Total edges: 141 (新增28)
Total companies: 30 (新增10)
Total exposures: 74 (新增45)
```

## 发现与启发

### 1. 产业链覆盖广度
- **富奥股份** 暴露了7个汽车零部件节点，是本次暴露节点最多的制造业公司，反映了其作为一汽集团核心零部件平台的全面配套能力。
- **中集集团** 横跨物流装备（集装箱、半挂车、空港装备）和能源装备（LNG装备、海工装备）两大领域，体现了其"物流+能源"双轮驱动的产业格局。

### 2. 服务业节点的重要性
- 本次新建了大量 **service 类型节点**（high_tech_industrial_engineering, big_data_service, logistics_service, urban_sanitation_service 等），进一步验证了产业图中"服务"与"实体"同等重要的设计原则。
- **深桑达A** 的核心业务是"高科技产业工程服务"（收入占比93%），这不是制造实体而是工程服务，必须用 service 类型表达。
- **神州数码** 的核心是"IT分销服务"，不是制造IT设备，而是 procuring + providing_service it_distribution_service。

### 3. 多元化公司的节点暴露策略
- **大悦城** 不仅有住宅和商业地产，还有工业物业和酒店经营，4个暴露节点覆盖了其全部业态。
- **中国天楹** 采用"环保+新能源"双引擎，暴露节点同时覆盖了 waste_to_energy（环保）和 wind_power_generation（新能源）。
- **深桑达A** 的收入结构中高科技产业工程服务占绝对主导（629亿 vs 大数据20亿），暴露权重相应设置得更高。

### 4. 网络核查的价值
- 通过网络搜索确认了富奥股份的"环境系统"实质是汽车空调/热管理系统，与已有 automotive_steel/chassis_system 形成完整汽车零部件链。
- 确认了深桑达A的母公司中国电子的战略定位，以及"中国电子云"在数据要素领域的核心地位。
- 确认了中国天楹的"风光储氢氨醇一体化"是规划中的前沿业务，尚未产生实质收入，因此未将其绿氢/绿氨节点纳入产业图（避免引入未成熟产业概念）。
- 确认了中集集团在集装箱、半挂车、罐式集装箱、登机桥等细分领域的全球第一地位。

### 5. 数据质量与Tushare局限
- `fina_indicator` 接口的 revenue 字段在2026Q1财报季数据不完整，换用 `income` 接口获取2025年报数据成功。
- `fina_mainbz`（主营构成）接口数据存在但编码为乱码，不影响使用（可直接读取数值）。
- 总市值数据（daily_basic）获取成功，单位为元。

## 待后续完善

1. **行业过滤器配置**: 本次未新建行业过滤器（industry），后续可为 batch_003 的公司配置行业视图（如"医药流通"、"汽车零部件"、"房地产开发"等）。
2. **公司关系推断**: 可为 batch_003 的公司构建 inferred_industrial_relation。例如：
   - 富奥股份（manufacture automotive_brake_system）→ 中集集团（manufacture road_transport_vehicle）已有产业链关系
   - 国药一致（procure medical_device）→ 深桑达A（manufacture communication_device）无直接产业链关系
3. **前端视图**: 可在前端查看 batch_003 公司的临时子图和暴露关系。
