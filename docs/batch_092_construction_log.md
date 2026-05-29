# Batch 092 Construction Log

## Overview

- **Batch Number**: 092
- **Companies**: 10
- **New Industrial Nodes**: 13
- **New Industrial Edges**: 1
- **New Company-Node Exposures**: 26
- **Submission Time**: 2026-05-25

## Graph Changes

### New Nodes (13)

| node_id | canonical_name_zh | entity_type |
|---|---|---|
| ophthalmic_eye_drop | 眼科用滴眼液 | material |
| chinese_patent_medicine_liquid | 中成药液体制剂 | material |
| hydrophilic_aluminum_foil | 亲水铝箔 | material |
| tungsten_material | 钨材料 | material |
| ferromanganese | 锰铁合金 | material |
| ferrochrome | 铬铁合金 | material |
| smart_property_management | 智能化物业管理服务 | service |
| commercial_housing_rental | 商品房租赁服务 | service |
| water_tourism_service | 水上旅游服务 | service |
| bicycle_part | 自行车零部件 | component |
| gas_appliance | 燃气具 | component |
| domestic_trade_service | 国内贸易服务 | service |
| foreign_trade_service | 外贸进出口服务 | service |

### New Edges (1)

| source | target | edge_type | description |
|---|---|---|---|
| cement | ready_mixed_concrete | material_flow | 水泥是生产混凝土的主要原料 |

## Companies Submitted

| company_id | name_zh | industry |
|---|---|---|
| sh_600671 | 天目药业 | 中成药 |
| sh_600673 | 东阳光 | 综合类 |
| sh_600674 | 川投能源 | 水力发电 |
| sh_600675 | 中华企业 | 区域地产 |
| sh_600676 | 交运股份 | 汽车配件 |
| sh_600678 | ST金顶 | 水泥 |
| sh_600679 | 上海凤凰 | 文教休闲 |
| sh_600681 | 百川能源 | 供气供热 |
| sh_600682 | 南京新百 | 生物制药 |
| sh_600683 | 京投发展 | 区域地产 |

## Notes

- All nodes and edges validated against schema constraints.
- Evidence attached to each node/edge from company business descriptions.
- Company IDs use `sh_` prefix with numeric stock code (schema-compliant snake_case).
- Exposures map companies to industrial nodes with activity type and weight.
