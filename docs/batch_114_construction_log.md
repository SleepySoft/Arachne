# Batch 114 产业图构建日志

## 批次信息
- **批次号**: 114
- **股票代码范围**: 002016.SZ - 002027.SZ
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要
- 新建产业节点：16个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：25条

## 新增节点详情

| node_id | canonical_name_zh | entity_type | 代表公司 |
|---------|-------------------|-------------|---------|
| `anti_infective_drug` | 抗感染药物 | material | 京新药业 |
| `cardiovascular_drug` | 心脑血管药物 | material | 京新药业 |
| `embroidery_machine` | 绣花机 | device | 中捷资源 |
| `in_vitro_diagnostic_reagent` | 体外诊断试剂 | material | 科华生物 |
| `medical_instrument` | 医疗仪器 | device | 科华生物 |
| `aircraft_maintenance` | 航空维修 | service | 海特高新 |
| `aviation_testing` | 航空检测 | service | 海特高新 |
| `home_appliance_retail` | 家电零售 | service | ST易购 |
| `electronics_retail` | 电子产品零售 | service | ST易购 |
| `connector` | 连接器 | component | 航天电器 |
| `mobile_phone_battery` | 手机电池 | component | 航天电器 |
| `drill_chuck` | 钻夹头 | component | 山东威达 |
| `power_tool_switch` | 电动工具开关 | component | 山东威达 |
| `intelligent_manufacturing` | 智能制造 | service | 山东威达 |
| `advertising_media` | 广告媒体 | service | 分众传媒 |
| `building_media` | 楼宇媒体 | service | 分众传媒 |

## 关键发现

1. **ST易购** (002024) 是中国最大的家电零售企业之一（原苏宁易购），新建 `home_appliance_retail` 和 `electronics_retail` 节点，填补了零售渠道领域的空白。
2. **分众传媒** (002027) 是中国最大的楼宇电梯媒体运营商，`advertising_media` 和 `building_media` 节点的加入丰富了广告传媒产业图谱。
3. **航天电器** (002025) 是中国航天科工集团旗下连接器企业，新建 `connector` 和 `mobile_phone_battery` 节点，与宏发股份（batch_110）的继电器、低压电器形成了电子元器件控制器件的完整体系。
4. **海特高新** (002023) 是中国最大的民营航空维修企业，新建 `aircraft_maintenance` 和 `aviation_testing` 节点，与航发动力（batch_110）的航空发动机制造和航天电子（batch_109）的航天电子设备共同构建了中国航空产业链。
5. **科华生物** (002022) 是中国体外诊断行业的先驱企业，新建 `in_vitro_diagnostic_reagent` 和 `medical_instrument` 节点。
