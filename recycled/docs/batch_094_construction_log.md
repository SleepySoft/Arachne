# Batch 094 Construction Log

## Overview

- **Batch Number**: 094
- **Companies**: 10
- **New Industrial Nodes**: 10
- **New Industrial Edges**: 0
- **New Company-Node Exposures**: 22
- **Submission Time**: 2026-05-25

## Graph Changes

### New Nodes (10)

| node_id | canonical_name_zh | entity_type |
|---|---|---|
| turbocharger | 涡轮增压器 | component |
| engine_valve | 发动机进排气门 | component |
| engine_cooling_fan | 发动机冷却风扇 | component |
| led_epitaxial_wafer | LED外延片 | material |
| led_chip | LED芯片 | component |
| scenic_area_operation_service | 景区运营管理服务 | service |
| travel_agency_service | 旅行社服务 | service |
| performance_service | 演出演艺服务 | service |
| cultural_tourism_product | 文化旅游商品 | material |
| lcd_substrate_glass | 液晶基板玻璃 | material |

### New Edges (0)

| source | target | edge_type | description |
|---|---|---|---|
| — | — | — | No new edges in this batch |

## Companies Submitted

| company_id | name_zh | industry |
|---|---|---|
| sh_600696 | *ST岩石 | 白酒 |
| sh_600697 | 欧亚集团 | 百货 |
| sh_600698 | 湖南天雁 | 汽车配件 |
| sh_600699 | 均胜电子 | 汽车配件 |
| sh_600702 | 舍得酒业 | 白酒 |
| sh_600703 | 三安光电 | 半导体 |
| sh_600704 | 物产中大 | 仓储物流 |
| sh_600706 | 曲江文旅 | 旅游景点 |
| sh_600707 | 彩虹股份 | 元器件 |
| sh_600708 | 光明地产 | 全国地产 |

## Notes

- All nodes and edges validated against schema constraints.
- Evidence attached to each node/edge from company business descriptions.
- Company IDs use `sh_` prefix with numeric stock code (schema-compliant snake_case).
- Exposures map companies to industrial nodes with activity type and weight.
