# Batch 091 Construction Log

## Overview

- **Batch Number**: 091
- **Companies**: 10
- **New Industrial Nodes**: 13
- **New Industrial Edges**: 3
- **New Company-Node Exposures**: 26
- **Submission Time**: 2026-05-25

## Graph Changes

### New Nodes (13)

| node_id | canonical_name_zh | entity_type |
|---|---|---|
| tech_park_operation_service | 科技产业园区运营服务 | service |
| automotive_glass | 汽车玻璃 | component |
| taxi_operation_service | 出租汽车运营服务 | service |
| chinese_medicine_preparation | 中药制剂 | material |
| chemical_drug_preparation | 化学药品制剂 | material |
| health_food | 保健食品 | material |
| sapphire_crystal_material | 蓝宝石晶体材料 | material |
| single_crystal_furnace | 单晶炉 | device |
| sapphire_product | 蓝宝石制品 | component |
| semiconductor_backend_service | 半导体后工序服务 | service |
| telecom_cable | 通信电缆 | component |
| printing_material | 印刷材料 | material |
| financial_equipment | 金融设备 | device |

### New Edges (3)

| source | target | edge_type | description |
|---|---|---|---|
| float_glass | automotive_glass | material_flow | 浮法玻璃经深加工制成汽车玻璃 |
| sapphire_crystal_material | sapphire_product | material_flow | 蓝宝石晶体材料经加工制成蓝宝石制品 |
| single_crystal_furnace | sapphire_crystal_material | capability_supply | 单晶炉提供晶体生长能力，产出蓝宝石晶体材料 |

## Companies Submitted

| company_id | name_zh | industry |
|---|---|---|
| sh_600658 | 电子城 | 园区开发 |
| sh_600660 | 福耀玻璃 | 汽车配件 |
| sh_600661 | 昂立教育 | 文教休闲 |
| sh_600662 | 外服控股 | 文教休闲 |
| sh_600663 | 陆家嘴 | 园区开发 |
| sh_600664 | 哈药股份 | 化学制药 |
| sh_600665 | 天地源 | 全国地产 |
| sh_600666 | 奥瑞德 | 元器件 |
| sh_600667 | 太极实业 | 半导体 |
| sh_600668 | 尖峰集团 | 水泥 |

## Notes

- All nodes and edges validated against schema constraints.
- Evidence attached to each node/edge from company business descriptions.
- Company IDs use `sh_` prefix with numeric stock code (schema-compliant snake_case).
- Exposures map companies to industrial nodes with activity type and weight.
