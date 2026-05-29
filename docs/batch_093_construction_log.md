# Batch 093 Construction Log

## Overview

- **Batch Number**: 093
- **Companies**: 10
- **New Industrial Nodes**: 18
- **New Industrial Edges**: 0
- **New Company-Node Exposures**: 41
- **Submission Time**: 2026-05-25

## Graph Changes

### New Nodes (18)

| node_id | canonical_name_zh | entity_type |
|---|---|---|
| special_vessel | 特种船舶 | system |
| frp_product | 玻璃钢制品 | component |
| marine_furniture | 船舶家具 | component |
| synthetic_fiber | 合成纤维 | material |
| petroleum_product | 石油产品 | material |
| wool_textile | 毛纺织品 | material |
| ammonium_bicarbonate | 碳酸氢铵 | material |
| ammonium_chloride | 氯化铵 | material |
| dimethyl_ether | 二甲醚 | material |
| melamine | 三聚氰胺 | material |
| sodium_nitrate | 硝酸钠 | material |
| sodium_nitrite | 亚硝酸钠 | material |
| m_phenylenediamine | 间苯二胺 | material |
| n_butylaldehyde | 正丁醛 | material |
| isobutylaldehyde | 异丁醛 | material |
| octanol | 辛醇 | material |
| cyclohexanone | 环己酮 | material |
| inland_river_ferry | 内河客滚运输服务 | service |
| coastal_chemical_transport | 沿海化工品运输服务 | service |

### New Edges (0)

| source | target | edge_type | description |
|---|---|---|---|
| — | — | — | No new edges in this batch |

## Companies Submitted

| company_id | name_zh | industry |
|---|---|---|
| sh_600684 | 珠江股份 | 区域地产 |
| sh_600685 | 中船防务 | 船舶 |
| sh_600686 | 金龙汽车 | 汽车整车 |
| sh_600688 | 上海石化 | 石油加工 |
| sh_600689 | 上海三毛 | 综合类 |
| sh_600690 | 海尔智家 | 家用电器 |
| sh_600691 | 潞化科技 | 农药化肥 |
| sh_600692 | 亚通股份 | 区域地产 |
| sh_600693 | 东百集团 | 百货 |
| sh_600694 | 大商股份 | 百货 |

## Notes

- All nodes and edges validated against schema constraints.
- Evidence attached to each node/edge from company business descriptions.
- Company IDs use `sh_` prefix with numeric stock code (schema-compliant snake_case).
- Exposures map companies to industrial nodes with activity type and weight.
