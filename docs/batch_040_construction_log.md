# Batch 040 Construction Log

**Date:** 2026-05-25
**Companies:** 000963.SZ – 000975.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+5)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `ventilation_fan` | 风机 | device |
| 2 | `coalbed_methane` | 煤层气 | material |
| 3 | `non_crystalline_alloy` | 非晶合金 | material |
| 4 | `magnetic_material` | 磁性材料 | material |
| 5 | `tomato_product` | 番茄制品 | material |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `non_crystalline_is_a_magnetic` | non_crystalline_alloy → magnetic_material | is_a (ontology) |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `huadong_pharma` | 华东医药股份有限公司 | 000963.SZ | 浙江 | 杭州 |
| 2 | `tianbao_infrastructure` | 天津市房地产发展(集团)股份有限公司 | 000965.SZ | 天津 | 天津 |
| 3 | `changyuan_power` | 国家能源集团长源电力股份有限公司 | 000966.SZ | 湖北 | 武汉 |
| 4 | `yingfeng_env` | 盈峰环境科技集团股份有限公司 | 000967.SZ | 浙江 | 绍兴 |
| 5 | `lanyan` | 山西蓝焰控股股份有限公司 | 000968.SZ | 山西 | 晋城 |
| 6 | `at_m` | 安泰科技股份有限公司 | 000969.SZ | 北京 | 北京 |
| 7 | `zhongke_sanhuan` | 北京中科三环高技术股份有限公司 | 000970.SZ | 北京 | 北京 |
| 8 | `st_zhongji` | 中基健康产业股份有限公司 | 000972.SZ | 新疆 | 乌鲁木齐 |
| 9 | `fosu_tech` | 佛山佛塑科技集团股份有限公司 | 000973.SZ | 广东 | 佛山 |
| 10 | `shanjin_intl` | 山金国际黄金股份有限公司 | 000975.SZ | 内蒙古 | 赤峰 |

## 4. Company Node Exposures (+10)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 华东医药 | chemical_drug | produce | 化学药品生产商 | 0.9 |
| 天保基建 | real_estate_development | operate | 房地产开发商 | 0.9 |
| 长源电力 | coal_power_generation | operate | 火电运营商 | 0.9 |
| 盈峰环境 | ventilation_fan | manufacture | 风机制造商 | 0.9 |
| 蓝焰控股 | coalbed_methane | produce | 煤层气开发商 | 0.95 |
| 安泰科技 | non_crystalline_alloy | produce | 非晶合金材料制造商 | 0.9 |
| 中科三环 | magnetic_material | produce | 磁性材料制造商 | 0.95 |
| ST中基 | tomato_product | produce | 番茄制品生产商 | 0.9 |
| 佛塑科技 | plastic_film | produce | 高分子功能薄膜制造商 | 0.85 |
| 山金国际 | gold_metal | produce | 黄金生产商 | 0.9 |

---

**Graph increment:** Nodes +5, Edges +1
