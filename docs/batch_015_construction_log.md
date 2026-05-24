# Batch 015 产业图构建日志

## 批次信息
- **批次号**: batch_015
- **处理日期**: 2026-05-24
- **公司数量**: 10家

## 公司列表
| 股票代码 | 公司名称 | 行业 | 地区 |
|---------|---------|------|------|
| 000566.SZ | 海南海药 | 化学制药 | 海南海口 |
| 000567.SZ | 海德股份 | 多元金融 | 海南海口 |
| 000568.SZ | 泸州老窖 | 白酒 | 四川泸州 |
| 000570.SZ | 苏常柴A | 农用机械 | 江苏常州 |
| 000571.SZ | 新大洲A | 煤炭开采 | 海南海口 |
| 000572.SZ | 海马汽车 | 汽车整车 | 海南海口 |
| 000573.SZ | 粤宏远A | 区域地产 | 广东东莞 |
| 000576.SZ | 甘化科工 | 电气设备 | 广东江门 |
| 000581.SZ | 威孚高科 | 汽车配件 | 江苏无锡 |
| 000582.SZ | 北部湾港 | 港口 | 广西北海 |

## 已有实体检查
在构建前查询了系统中已有节点。威孚高科所在的汽车产业链已有automotive_engine、automotive_environment_system等节点；北部湾港所在的港口产业已有port_operation_service、shipping_service、container_handling_service等节点。

## 新增产业节点（16个）
- **金融服务**: non_performing_asset_management（不良资产管理）
- **农业机械**: diesel_engine（柴油机）、combine_harvester（联合收割机）、agricultural_transport_vehicle（农用运输车）、agricultural_machinery（农业机械）
- **食品**: beef_product（牛肉食品）
- **汽车制造**: automotive_manufacturing（汽车制造）
- **地产/资源**: industrial_zone_development（工业区开发）、recycled_lead（再生铅）
- **军工**: military_power_supply（军用电源）、special_alloy_product（特种合金制品）
- **汽车零部件**: fuel_injection_system（燃油喷射系统）、exhaust_aftertreatment_system（尾气后处理系统）、intake_system（进气系统）
- **港口服务**: shipping_agency_service（船舶代理服务）、stevedoring_service（装卸堆存服务）

## 新增产业边（14条）
重点构建了以下产业链关系：
- 柴油机→联合收割机/农用运输车（composition）
- 联合收割机/农用运输车→农业机械（composition）
- 牛肉食品→食品原料（material_flow）
- 汽车制造→公路运输车辆（service_flow）
- 再生铅→铅锌金属（material_flow）
- 高温合金→特种合金制品（material_flow）
- 燃油喷射系统/尾气后处理系统/进气系统→汽车发动机（composition）
- 柴油→燃油喷射系统（material_flow）
- 装卸堆存/船舶代理→港口运营（service_flow）

## 公司视图设计
- **海南海药**: pharmaceutical_product、biological_drug、chemical_drug、traditional_chinese_medicine（均为manufacture）
- **海德股份**: non_performing_asset_management(operate)
- **泸州老窖**: liquor(manufacture)
- **苏常柴A**: diesel_engine、combine_harvester、agricultural_transport_vehicle、agricultural_machinery（均为manufacture）
- **新大洲A**: beef_product(manufacture)、coal(produce)、logistics_service(operate)
- **海马汽车**: automotive_manufacturing、road_transport_vehicle（均为manufacture），automotive_sales_service(operate)
- **粤宏远A**: real_estate_development、industrial_zone_development（均为operate），coal(produce)、recycled_lead(manufacture)
- **甘化科工**: power_supply_system、military_power_supply、special_alloy_product（均为manufacture）
- **威孚高科**: fuel_injection_system、exhaust_aftertreatment_system、intake_system（均为manufacture）
- **北部湾港**: port_operation_service、shipping_service、stevedoring_service、shipping_agency_service、container_handling_service

## 提交结果
- Graph Batch: 16节点创建，14边创建，0错误
- Business Batch: 10公司创建，31暴露创建，0错误

## 发现与启发
1. **威孚高科的三系统产品**: 柴油燃油喷射系统、尾气后处理系统和进气系统均直接连接到汽车发动机这一subsystem节点，形成了"进气→燃烧→喷射→排气"的完整发动机工作循环产业图。这是batch_015中最具技术深度的产业链设计。
2. **苏常柴A的农业机械链**: "柴油机→联合收割机/农用运输车→农业机械"形成了清晰的农机产业链层级。柴油机作为通用动力单元，可服务于多种农业机械，体现了动力平台化特征。
3. **海南的上市公司集群**: 本批次中有4家公司（海南海药、海德股份、新大洲A、海马汽车）注册于海南海口，但它们的产业暴露完全不相关（医药、金融、食品/煤炭、汽车），体现了地域集中但产业分散的上市格局。
4. **粤宏远A的跨行业特征**: 房地产、工业区开发、原煤开采和再生铅业务四大板块在产业图上彼此独立。再生铅业务连接到已有节点lead_zinc_metal，形成了铅金属的回收再利用循环。
5. **甘化科工的军工转型**: 该公司由传统制糖企业转型为军工电子和特种合金企业。其special_alloy_product节点与batch_013中万泽股份的高温合金节点通过high_temperature_alloy→special_alloy_product边形成上下游关系，实现了跨批次产业连接。

## 五批次总体统计
- **总新增节点**: 99个（batch_011: 19, batch_012: 15, batch_013: 22, batch_014: 27, batch_015: 16）
- **总新增边**: 83条（batch_011: 20, batch_012: 16, batch_013: 13, batch_014: 20, batch_015: 14）
- **总新增/更新公司**: 50家
- **总新增/更新暴露**: 约184个
