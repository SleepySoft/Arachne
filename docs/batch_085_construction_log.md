# Batch 085 Construction Log

**Date:** 2026-05-25
**Companies:** 600586.SH – 600596.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `flat_glass` | 平板玻璃 | material |
| 2 | `sterilization_equipment` | 消毒灭菌设备 | device |
| 3 | `pharmaceutical_equipment` | 制药设备 | device |
| 4 | `amino_composite_material` | 氨基复合材料 | material |
| 5 | `idc` | 互联网数据中心 | service |
| 6 | `bearing` | 轴承 | component |
| 7 | `high_performance_aluminum_sheet` | 高性能铝合金板材 | material |
| 8 | `glyphosate` | 草甘膦 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flat_glass_to_construction` | flat_glass → construction | material_flow |
| 2 | `bearing_to_automobile` | bearing → automobile | composition |
| 3 | `glyphosate_to_pesticide` | glyphosate → pesticide | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `jinjing` | 山东金晶科技股份有限公司 | 600586.SH | 山东 | 淄博市 |
| 2 | `shinva` | 山东新华医疗器械股份有限公司 | 600587.SH | 山东 | 淄博市 |
| 3 | `yonyou` | 用友网络科技股份有限公司 | 600588.SH | 北京 | 北京市 |
| 4 | `dawei` | 大位数据科技(广东)集团股份有限公司 | 600589.SH | 广东 | 揭阳市 |
| 5 | `tellhow` | 泰豪科技股份有限公司 | 600590.SH | 江西 | 南昌市 |
| 6 | `longxi` | 福建龙溪轴承(集团)股份有限公司 | 600592.SH | 福建 | 漳州市 |
| 7 | `dalian_shengya` | 大连圣亚旅游控股股份有限公司 | 600593.SH | 辽宁 | 大连市 |
| 8 | `yibai` | 贵州益佰制药股份有限公司 | 600594.SH | 贵州 | 贵阳市 |
| 9 | `zhongfu` | 河南中孚实业股份有限公司 | 600595.SH | 河南 | 郑州市 |
| 10 | `xinan` | 浙江新安化工集团股份有限公司 | 600596.SH | 浙江 | 杭州市 |

## 4. Company Node Exposures (+30)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 金晶科技 | flat_glass | produce | 平板玻璃生产商 | 0.95 |
| 金晶科技 | soda_ash | produce | 纯碱生产商 | 0.9 |
| 新华医疗 | sterilization_equipment | manufacture | 消毒灭菌设备制造商 | 0.95 |
| 新华医疗 | radiotherapy_equipment | manufacture | 放射诊断及治疗设备制造商 | 0.9 |
| 新华医疗 | pharmaceutical_equipment | manufacture | 制药设备制造商 | 0.9 |
| 用友网络 | application_software | provide_service | 应用软件服务商 | 0.95 |
| 用友网络 | software | provide_service | 软件服务商 | 0.95 |
| 用友网络 | it_service | provide_service | IT服务商 | 0.9 |
| 大位科技 | amino_composite_material | produce | 氨基复合材料生产商 | 0.95 |
| 大位科技 | phthalic_anhydride | produce | 苯酐生产商 | 0.9 |
| 大位科技 | plasticizer | produce | 增塑剂生产商 | 0.9 |
| 大位科技 | idc | operate | 互联网数据中心运营商 | 0.85 |
| 大位科技 | cloud_computing | provide_service | 云计算服务商 | 0.85 |
| 泰豪科技 | smart_grid_device | manufacture | 智能电力设备制造商 | 0.95 |
| 泰豪科技 | electric_motor | manufacture | 电机制造商 | 0.9 |
| 泰豪科技 | energy_saving | provide_service | 节能服务商 | 0.85 |
| 龙溪股份 | bearing | manufacture | 轴承制造商 | 0.95 |
| 龙溪股份 | automobile_part | manufacture | 汽车配件制造商 | 0.9 |
| 大连圣亚 | scenic_spot | operate | 景点运营商 | 0.95 |
| 大连圣亚 | catering_service | operate | 餐饮服务商 | 0.85 |
| 大连圣亚 | tourism_service | provide_service | 旅游服务商 | 0.85 |
| 益佰制药 | otc_drug | produce | OTC药品生产商 | 0.95 |
| 益佰制药 | prescription_drug | produce | 处方药生产商 | 0.95 |
| 益佰制药 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 中孚实业 | high_performance_aluminum_sheet | produce | 高性能铝合金板材生产商 | 0.95 |
| 中孚实业 | can_body_stock | produce | 易拉罐料生产商 | 0.9 |
| 中孚实业 | aluminum_foil | produce | 铝箔生产商 | 0.9 |
| 新安股份 | glyphosate | produce | 草甘膦生产商 | 0.95 |
| 新安股份 | organosilicon | produce | 有机硅生产商 | 0.95 |
| 新安股份 | pesticide | produce | 农药生产商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
