# Batch 073 Construction Log

**Date:** 2026-05-25
**Companies:** 600421.SH – 600436.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `funeral_service` | 殡葬服务 | service |
| 2 | `artemisinin_series` | 蒿甲醚系列产品 | material |
| 3 | `notoginseng_series` | 三七系列产品 | material |
| 4 | `nitric_acid` | 硝酸 | material |
| 5 | `formaldehyde` | 甲醛 | material |
| 6 | `carbonless_paper` | 无碳纸 | material |
| 7 | `navigation_control` | 导航控制系统 | system |
| 8 | `ammunition_info_system` | 弹药信息化系统 | system |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `formaldehyde_to_chemical_product` | formaldehyde → chemical_product | material_flow |
| 2 | `nitric_acid_to_fertilizer` | nitric_acid → fertilizer | material_flow |
| 3 | `navigation_control_to_defense_equipment` | navigation_control → defense_equipment | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `st_huarong` | 武汉华嵘控股股份有限公司 | 600421.SH | 湖北 | 武汉市 |
| 2 | `kunyao_group` | 昆药集团股份有限公司 | 600422.SH | 云南 | 昆明市 |
| 3 | `st_liuhua` | 柳州化工股份有限公司 | 600423.SH | 广西 | 柳州市 |
| 4 | `qingsong_jianhua` | 新疆青松建材化工(集团)股份有限公司 | 600425.SH | 新疆 | 阿拉尔市 |
| 5 | `hualu_hensheng` | 山东华鲁恒升化工股份有限公司 | 600426.SH | 山东 | 德州市 |
| 6 | `cosco_specialized` | 中远海运特种运输股份有限公司 | 600428.SH | 广东 | 广州市 |
| 7 | `sanyuan` | 北京三元食品股份有限公司 | 600429.SH | 北京 | 北京市 |
| 8 | `guanhao` | 广东冠豪高新技术股份有限公司 | 600433.SH | 广东 | 湛江市 |
| 9 | `norinco_nav` | 北方导航控制技术股份有限公司 | 600435.SH | 北京 | 北京市 |
| 10 | `pientzehuang` | 漳州片仔癀药业股份有限公司 | 600436.SH | 福建 | 漳州市 |

## 4. Company Node Exposures (+25)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| *ST华嵘 | funeral_service | operate | 殡葬服务运营商 | 0.95 |
| *ST华嵘 | cemetery | operate | 墓地运营商 | 0.9 |
| 昆药集团 | artemisinin_series | produce | 蒿甲醚系列产品生产商 | 0.95 |
| 昆药集团 | notoginseng_series | produce | 三七系列产品生产商 | 0.9 |
| 昆药集团 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| *ST柳化 | nitric_acid | produce | 硝酸生产商 | 0.95 |
| *ST柳化 | urea | produce | 尿素生产商 | 0.9 |
| *ST柳化 | formaldehyde | produce | 甲醛生产商 | 0.9 |
| *ST柳化 | methanol | produce | 甲醇生产商 | 0.85 |
| 青松建化 | cement | produce | 水泥生产商 | 0.95 |
| 青松建化 | building_material | produce | 建材生产商 | 0.9 |
| 华鲁恒升 | urea | produce | 尿素生产商 | 0.95 |
| 华鲁恒升 | formaldehyde | produce | 甲醛生产商 | 0.9 |
| 华鲁恒升 | chemical_product | produce | 化工产品生产商 | 0.85 |
| 中远海特 | shipping | operate | 航运运营商 | 0.95 |
| 中远海特 | logistics | provide_service | 物流服务商 | 0.9 |
| 三元股份 | dairy_product | produce | 乳制品生产商 | 0.95 |
| 三元股份 | food | produce | 食品生产商 | 0.85 |
| 冠豪高新 | carbonless_paper | produce | 无碳纸生产商 | 0.95 |
| 冠豪高新 | paper | produce | 造纸商 | 0.9 |
| 北方导航 | navigation_control | manufacture | 导航控制系统制造商 | 0.95 |
| 北方导航 | ammunition_info_system | manufacture | 弹药信息化系统制造商 | 0.9 |
| 北方导航 | special_vehicle | manufacture | 专用车制造商 | 0.8 |
| 片仔癀 | chinese_patent_medicine | produce | 中成药生产商 | 0.95 |
| 片仔癀 | pharmaceutical | produce | 药品生产商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
