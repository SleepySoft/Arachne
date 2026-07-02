# Batch 013 产业图构建日志

## 批次信息
- **批次号**: batch_013
- **处理日期**: 2026-05-24
- **公司数量**: 10家

## 公司列表
| 股票代码 | 公司名称 | 行业 | 地区 |
|---------|---------|------|------|
| 000543.SZ | 皖能电力 | 火力发电 | 安徽合肥 |
| 000544.SZ | 中原环保 | 环境保护 | 河南郑州 |
| 000545.SZ | 金浦钛业 | 化工原料 | 吉林吉林 |
| 000546.SZ | 金圆股份 | 环境保护 | 吉林长春 |
| 000547.SZ | 航天发展 | 通信设备 | 福建福州 |
| 000548.SZ | 湖南投资 | 路桥 | 湖南长沙 |
| 000550.SZ | 江铃汽车 | 汽车整车 | 江西南昌 |
| 000551.SZ | 创元科技 | 专用机械 | 江苏苏州 |
| 000552.SZ | 甘肃能化 | 煤炭开采 | 甘肃白银 |
| 000553.SZ | 安道麦A | 农药化肥 | 湖北荆州 |

## 已有实体检查
在构建前查询了系统中已有节点。江铃汽车与batch_012的佛山照明所在的汽车产业链已有automotive_transmission_system、automotive_brake_system、chassis_system、suspension_system等节点，可直接复用。

## 新增产业节点（22个）
- **磨料磨具**: grinding_wheel（固结磨具）、coated_abrasive（涂附磨具）
- **化工**: titanium_dioxide（钛白粉）、titanium_ore（钛矿）
- **地产**: real_estate_development（房地产开发，已存在但确认）
- **军工/通信**: generator_set（发电机组）、communication_equipment（通信设备）
- **基础设施**: highway（高速公路）、urban_complex（城市综合体）
- **汽车零部件**: automotive_engine（汽车发动机）、light_truck（轻型卡车）、pickup_truck（皮卡）、suv（SUV）、heavy_truck（重型卡车）、commercial_vehicle（商用车）、cast_part（铸件）
- **精密制造**: cleanroom_equipment（洁净设备）、insulator（绝缘子）、bearing（轴承）、surveying_instrument（测绘仪器）、abrasive_tool（磨具）、abrasive_material（磨料）

## 新增产业边（13条）
重点构建了以下产业链关系：
- 钛矿→钛白粉（material_flow）
- 水泥→房地产开发（material_flow）
- 高速公路→高速公路运营服务（service_flow）
- 城市综合体→物业管理服务（service_flow）
- 发动机→轻型卡车/重型卡车（composition）
- 铸件→发动机（composition）
- 轻型卡车/重型卡车/商用车→公路运输车辆（composition）
- 绝缘子→配电设备（composition）
- 磨料→磨具（composition）

## 公司视图设计
- **皖能电力**: electricity_power、heating_supply、power_plant_operation、coal_power_generation、solar_power_generation、wind_power_generation
- **中原环保**: grinding_wheel、coated_abrasive、heating_supply、waste_water_treatment
- **金浦钛业**: titanium_dioxide(manufacture)、titanium_ore(procure)
- **金圆股份**: cement(manufacture)、real_estate_development(operate)
- **航天发展**: generator_set、communication_equipment（均为manufacture）
- **湖南投资**: highway、highway_operation_service、hotel_operation_service、property_management_service
- **江铃汽车**: light_truck、pickup_truck、suv、heavy_truck、commercial_vehicle、automotive_engine、cast_part（均为manufacture）
- **创元科技**: cleanroom_equipment、insulator、bearing、surveying_instrument、abrasive_tool、abrasive_material（均为manufacture）
- **甘肃能化**: coal(produce)
- **安道麦A**: pesticide、chemical_fertilizer、petrochemical_product（均为manufacture）

## 提交结果
- Graph Batch: 22节点创建，13边创建，0错误
- Business Batch: 10公司创建，37暴露创建，0错误

## 发现与启发
1. **江铃汽车的产品矩阵**: 该公司产品线极其丰富，覆盖轻型卡车、皮卡、SUV、重型卡车和商用车，并自产发动机和铸件。在产业图中，发动机作为subsystem节点连接到各类整车，铸件作为component节点连接到发动机，形成了"铸件→发动机→整车"的三级产业链。
2. **创元科技的精密制造集群**: 该公司横跨洁净设备、绝缘子、轴承、测绘仪器和磨具磨料五大制造业细分领域，彼此间无直接产业流关系，体现了精密制造企业的多元化特征。
3. **中原环保的三元业务**: 磨料磨具（制造业）、热力供应（能源业）和污水处理（环保业）三大业务板块在产业图上完全独立，这是一家典型的产业转型企业。
4. **金浦钛业的产业链定位**: 钛矿→钛白粉→涂料/塑料，该公司占据产业链的中上游。为其建立钛矿采购暴露（procure），表达其原材料依赖。
