# Batch 014 产业图构建日志

## 批次信息
- **批次号**: batch_014
- **处理日期**: 2026-05-24
- **公司数量**: 10家

## 公司列表
| 股票代码 | 公司名称 | 行业 | 地区 |
|---------|---------|------|------|
| 000554.SZ | 泰山石油 | 石油贸易 | 山东泰安 |
| 000555.SZ | 神州信息 | 软件服务 | 广东深圳 |
| 000557.SZ | 西部创业 | 铁路 | 宁夏银川 |
| 000558.SZ | 天府文旅 | 旅游景点 | 四川成都 |
| 000559.SZ | 万向钱潮 | 汽车配件 | 浙江杭州 |
| 000560.SZ | 我爱我家 | 房产服务 | 云南昆明 |
| 000561.SZ | 烽火电子 | 通信设备 | 陕西宝鸡 |
| 000563.SZ | 陕国投A | 多元金融 | 陕西西安 |
| 000564.SZ | 供销大集 | 百货 | 陕西西安 |
| 000565.SZ | 渝三峡A | 染料涂料 | 重庆 |

## 已有实体检查
在构建前查询了系统中已有节点。万向钱潮所在的汽车零部件产业已有automotive_transmission_system、automotive_brake_system、chassis_system、suspension_system、bearing等节点，可复用并补充新的细分节点。

## 新增产业节点（27个）
- **石油**: gasoline（汽油）、diesel（柴油）、fuel_retail_service（成品油零售服务）、cng_station（加气站）
- **金融科技**: atm_machine（ATM机）、software_development_service（软件开发服务）、fintech_service（金融科技服务）
- **运输/物流**: rail_transport_service（铁路运输服务）、warehouse_service（仓储服务）
- **消费品**: wine（葡萄酒）
- **汽车零部件**: universal_joint（万向节）、wheel_hub_unit（轮毂单元）、automotive_exhaust_system（汽车排气系统）、fuel_tank（燃油箱）、machinery_part（工程机械零部件）
- **房地产服务**: real_estate_agency_service（房地产经纪服务）、residential_asset_management（住宅资产管理）、commercial_property_operation（商业地产运营）
- **电子制造**: electroacoustic_device（电声器材）、wire_cable（电线电缆）、textile_machinery（纺织机械）
- **金融**: trust_service（信托服务）
- **零售**: department_store（百货零售）
- **涂料**: paint（油漆）、coating（涂料）、synthetic_resin（合成树脂）、metal_packaging（金属包装）

## 新增产业边（20条）
重点构建了以下产业链关系：
- 石油炼制→汽油/柴油（service_flow）
- 汽油/柴油→成品油零售（service_flow）
- 天然气→加气站（material_flow）
- 软件开发→金融科技（capability_supply）
- IT硬件/软件→ATM机（composition）
- 铁路车辆→铁路运输（service_flow）
- 仓储→物流（service_flow）
- 万向节→传动系统、轮毂单元/轴承→底盘系统（composition）
- 排气系统→汽车环境系统、燃油箱→底盘系统（composition）
- 机械零部件→工程机械（composition）
- 百货零售→连锁零售（service_flow）
- 合成树脂→油漆/涂料（material_flow）
- 油漆→建筑施工（material_flow）

## 公司视图设计
- **泰山石油**: gasoline、diesel、fuel_retail_service、natural_gas、lpg
- **神州信息**: software_development_service、fintech_service、atm_machine、information_system_integration
- **西部创业**: rail_transport_service、warehouse_service、logistics_service、wine、hotel_operation_service、catering_service
- **天府文旅**: real_estate_development、tourism_service
- **万向钱潮**: universal_joint、wheel_hub_unit、bearing、chassis_system、suspension_system、automotive_transmission_system、automotive_brake_system、automotive_exhaust_system、fuel_tank、machinery_part
- **我爱我家**: real_estate_agency_service、residential_asset_management、commercial_property_operation、property_management_service
- **烽火电子**: communication_equipment、electroacoustic_device、wire_cable、textile_machinery
- **陕国投A**: trust_service、real_estate_development
- **供销大集**: department_store、chain_retail_service
- **渝三峡A**: paint、coating、synthetic_resin、metal_packaging

## 提交结果
- Graph Batch: 27节点创建，20边创建，0错误
- Business Batch: 10公司创建，42暴露创建，0错误

## 发现与启发
1. **万向钱潮的底盘系统完整性**: 该公司几乎覆盖了汽车底盘的所有关键零部件——万向节（传动）、轮毂单元（行走）、轴承（转动支撑）、悬架系统（减震）、制动系统（安全）、燃油箱（存储）和排气系统（环保）。在产业图上，这些零部件节点共同组成了底盘系统这一subsystem，体现了模块化制造的特征。
2. **泰山石油的非油品业务**: 该公司的经营范围极其广泛，除了成品油和天然气外，还涉及便利店、汽车维修、充电桩、氢能等。但核心产业暴露仍集中在fuel_retail_service和cng_station。
3. **烽火电子的纺织机械**: 作为一家军工通信企业，其业务范围中意外包含高端纺织机械。经核查，这源于其历史沿革和子公司业务，在产业图上保留为独立节点。
4. **涂料产业链的构建**: 渝三峡A的"合成树脂→油漆/涂料→建筑施工"构成了完整的涂料产业流，合成树脂作为上游原材料节点可与batch_011中红棉股份的化工原料节点形成潜在的跨批次产业关联。
