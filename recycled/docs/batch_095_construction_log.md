# Batch 095 Construction Log

## Overview

- **Batch Number**: 095
- **Companies**: 10
- **New Industrial Nodes**: 10
- **New Industrial Edges**: 1
- **New Company-Node Exposures**: 25
- **Submission Time**: 2026-05-25

## Graph Changes

### New Nodes (10)

| node_id | canonical_name_zh | entity_type |
|---|---|---|
| diesel_generator_set | 柴油发电机组 | system |
| outdoor_power_equipment | 户外动力设备 | system |
| pv_product | 光伏产品 | material |
| nonferrous_mining_service | 有色金属采选服务 | service |
| metal_financial_service | 金属金融服务 | service |
| pharmaceutical_manufacturing | 医药制造服务 | service |
| strontium_compound | 锶化合物 | material |
| automotive_body_part | 汽车车身零部件 | component |
| digital_medical_system | 数字医疗系统 | system |
| heat_supply | 热力供应服务 | service |
| container_transport_service | 集装箱运输服务 | service |

### New Edges (1)

| source | target | edge_type | description |
|---|---|---|---|
| diesel_generator_set | ship | composition | 柴油发电机组可作为船舶辅助发电设备 |

## Companies Submitted

| company_id | name_zh | industry |
|---|---|---|
| sh_600710 | 苏美达 | 商贸代理 |
| sh_600711 | 盛屯矿业 | 小金属 |
| sh_600712 | 南宁百货 | 百货 |
| sh_600713 | 南京医药 | 医药商业 |
| sh_600714 | 金瑞矿业 | 化工原料 |
| sh_600715 | 文投控股 | 影视音像 |
| sh_600716 | 凤凰股份 | 区域地产 |
| sh_600717 | 天津港 | 港口 |
| sh_600718 | 东软集团 | 软件服务 |
| sh_600719 | 大连热电 | 供气供热 |

## Notes

- All nodes and edges validated against schema constraints.
- Evidence attached to each node/edge from company business descriptions.
- Company IDs use `sh_` prefix with numeric stock code (schema-compliant snake_case).
- Exposures map companies to industrial nodes with activity type and weight.
