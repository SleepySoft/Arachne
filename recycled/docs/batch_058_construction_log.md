# Batch 058 Construction Log

**Date:** 2026-05-25
**Companies:** 600217.SH – 600229.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `e_waste_recycling` | 电子废弃物回收 | service |
| 2 | `diesel_engine` | 柴油发动机 | component |
| 3 | `aluminum_product` | 铝加工产品 | material |
| 4 | `air_transport` | 航空运输 | service |
| 5 | `cosmetics` | 化妆品 | material |
| 6 | `pesticide` | 农药 | material |
| 7 | `urea` | 尿素 | material |
| 8 | `internet_advertising` | 互联网广告 | service |
| 9 | `publishing_media` | 出版传媒 | service |
| 10 | `zirconium_product` | 锆系列产品 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `aluminum_product_to_automobile` | aluminum_product → automobile | composition |
| 2 | `diesel_engine_to_agricultural_machinery` | diesel_engine → agricultural_machinery | composition |
| 3 | `urea_to_fertilizer` | urea → chemical_fertilizer | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `zhongzai_zihuan` | 中再资源环境股份有限公司 | 600217.SH | 陕西 | 铜川 |
| 2 | `quanchai_power` | 安徽全柴动力股份有限公司 | 600218.SH | 安徽 | 滁州 |
| 3 | `nanshan_aluminum` | 山东南山铝业股份有限公司 | 600219.SH | 山东 | 烟台 |
| 4 | `hainan_airlines` | 海南航空控股股份有限公司 | 600221.SH | 海南 | 海口 |
| 5 | `tailong_pharma` | 河南太龙药业股份有限公司 | 600222.SH | 河南 | 郑州 |
| 6 | `freda` | 鲁商福瑞达医药股份有限公司 | 600223.SH | 山东 | 淄博 |
| 7 | `hengtong` | 浙江亨通控股股份有限公司 | 600226.SH | 浙江 | 湖州 |
| 8 | `cht` | 贵州赤天化股份有限公司 | 600227.SH | 贵州 | 贵阳 |
| 9 | `st_fanli` | 返利网数字科技股份有限公司 | 600228.SH | 江西 | 赣州 |
| 10 | `city_media` | 青岛城市传媒股份有限公司 | 600229.SH | 山东 | 青岛 |

## 4. Company Node Exposures (+19)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 中再资环 | e_waste_recycling | provide_service | 电子废弃物回收服务商 | 0.95 |
| 中再资环 | environmental_service | provide_service | 环保服务提供商 | 0.85 |
| 全柴动力 | diesel_engine | manufacture | 柴油发动机制造商 | 0.95 |
| 全柴动力 | automobile_part | manufacture | 汽车零部件制造商 | 0.85 |
| 南山铝业 | aluminum_product | produce | 铝加工产品生产商 | 0.95 |
| 南山铝业 | aerospace_metal | produce | 航空航天金属生产商 | 0.85 |
| 海航控股 | air_transport | operate | 航空运输运营商 | 0.95 |
| 太龙药业 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 福瑞达 | cosmetics | produce | 化妆品生产商 | 0.85 |
| 福瑞达 | biomaterial | produce | 生物基材料生产商 | 0.8 |
| 福瑞达 | real_estate_development | operate | 房地产开发运营商 | 0.75 |
| 亨通股份 | pesticide | produce | 农药生产商 | 0.9 |
| 亨通股份 | veterinary_medicine | produce | 兽药生产商 | 0.85 |
| 亨通股份 | zirconium_product | produce | 锆系列产品生产商 | 0.8 |
| 赤天化 | urea | produce | 尿素生产商 | 0.95 |
| 赤天化 | methanol | produce | 甲醇生产商 | 0.9 |
| 赤天化 | pharmaceutical | produce | 药品生产商 | 0.75 |
| *ST返利 | internet_advertising | provide_service | 互联网广告服务商 | 0.9 |
| 城市传媒 | publishing_media | provide_service | 出版传媒服务商 | 0.95 |

---

**Graph increment:** Nodes +6, Edges +3
