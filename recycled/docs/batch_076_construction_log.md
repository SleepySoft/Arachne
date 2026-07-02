# Batch 076 Construction Log

**Date:** 2026-05-25
**Companies:** 600477.SH – 600489.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `light_steel_structure` | 轻型钢结构 | material |
| 2 | `foam_nickel` | 泡沫镍 | material |
| 3 | `lithium_bromide_chiller` | 溴化锂制冷机 | device |
| 4 | `heat_exchanger` | 高效换热器 | device |
| 5 | `styrene` | 苯乙烯 | material |
| 6 | `pyrethroid` | 菊酯 | material |
| 7 | `optical_fiber_cable` | 光纤光缆 | component |
| 8 | `corticosteroid` | 皮质激素 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `light_steel_structure_to_construction` | light_steel_structure → construction | material_flow |
| 2 | `foam_nickel_to_battery` | foam_nickel → battery | composition |
| 3 | `optical_fiber_cable_to_communication_equipment` | optical_fiber_cable → communication_equipment | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `hangxiao` | 杭萧钢构股份有限公司 | 600477.SH | 浙江 | 杭州市 |
| 2 | `corun` | 湖南科力远新能源股份有限公司 | 600478.SH | 湖南 | 长沙市 |
| 3 | `qianjin_pharma` | 株洲千金药业股份有限公司 | 600479.SH | 湖南 | 株洲市 |
| 4 | `lingyun` | 凌云工业股份有限公司 | 600480.SH | 河北 | 保定市 |
| 5 | `shuangliang` | 双良节能系统股份有限公司 | 600481.SH | 江苏 | 无锡市 |
| 6 | `funeng` | 福建福能股份有限公司 | 600483.SH | 福建 | 福州市 |
| 7 | `yangnong` | 江苏扬农化工股份有限公司 | 600486.SH | 江苏 | 扬州市 |
| 8 | `hengtong` | 江苏亨通光电股份有限公司 | 600487.SH | 江苏 | 苏州市 |
| 9 | `tianjin_pharma` | 津药药业股份有限公司 | 600488.SH | 天津 | 天津市 |
| 10 | `zhongjin_gold` | 中金黄金股份有限公司 | 600489.SH | 北京 | 北京市 |

## 4. Company Node Exposures (+24)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 杭萧钢构 | light_steel_structure | produce | 轻型钢结构生产商 | 0.95 |
| 杭萧钢构 | steel_structure | produce | 钢结构生产商 | 0.9 |
| 杭萧钢构 | steel | produce | 钢材加工商 | 0.85 |
| 科力远 | foam_nickel | produce | 泡沫镍生产商 | 0.95 |
| 科力远 | battery_material | produce | 电池材料生产商 | 0.9 |
| 千金药业 | gynecology_chinese_patent_medicine | produce | 妇科中成药生产商 | 0.95 |
| 千金药业 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 凌云股份 | automobile_plastic_part | manufacture | 汽车塑料零部件制造商 | 0.95 |
| 凌云股份 | automobile_part | manufacture | 汽车零部件制造商 | 0.9 |
| 凌云股份 | plastic_pipe | manufacture | 塑料管道制造商 | 0.85 |
| 双良节能 | lithium_bromide_chiller | manufacture | 溴化锂制冷机制造商 | 0.95 |
| 双良节能 | heat_exchanger | manufacture | 换热器制造商 | 0.95 |
| 双良节能 | air_cooler | manufacture | 空冷器制造商 | 0.9 |
| 双良节能 | styrene | produce | 苯乙烯生产商 | 0.9 |
| 福能股份 | power_generation | operate | 电力运营商 | 0.95 |
| 福能股份 | textile_product | produce | 纺织品生产商 | 0.85 |
| 扬农化工 | pyrethroid | produce | 菊酯生产商 | 0.95 |
| 扬农化工 | pesticide | produce | 农药生产商 | 0.9 |
| 亨通光电 | optical_fiber_cable | manufacture | 光纤光缆制造商 | 0.95 |
| 亨通光电 | communication_equipment | manufacture | 通信设备制造商 | 0.9 |
| 津药药业 | corticosteroid | produce | 皮质激素生产商 | 0.95 |
| 津药药业 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 中金黄金 | gold | produce | 黄金生产商 | 0.95 |
| 中金黄金 | nonferrous_metal | produce | 有色金属生产商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
