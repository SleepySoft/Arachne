# Batch 088 Construction Log

**Date:** 2026-05-25
**Companies:** 600619.SH – 600630.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `air_conditioner_compressor` | 空调压缩机 | component |
| 2 | `heat_pump` | 热泵 | device |
| 3 | `capacitor` | 电容器 | component |
| 4 | `automotive_interior` | 汽车内饰 | material |
| 5 | `textile_new_material` | 纺织新材料 | material |
| 6 | `engineering_survey` | 工程勘察 | service |
| 7 | `municipal_design` | 市政设计 | service |
| 8 | `apparel_brand` | 服饰品牌 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `air_conditioner_compressor_to_air_conditioner` | air_conditioner_compressor → air_conditioner | composition |
| 2 | `capacitor_to_electronic_device` | capacitor → electronic_device | composition |
| 3 | `tire_to_automobile` | tire → automobile | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `highly` | 上海海立(集团)股份有限公司 | 600619.SH | 上海 | 上海市 |
| 2 | `tianchen` | 上海市天宸股份有限公司 | 600620.SH | 上海 | 上海市 |
| 3 | `huaxin` | 上海华鑫股份有限公司 | 600621.SH | 上海 | 上海市 |
| 4 | `everbright_jiabao` | 光大嘉宝股份有限公司 | 600622.SH | 上海 | 上海市 |
| 5 | `huayi` | 上海华谊集团股份有限公司 | 600623.SH | 上海 | 上海市 |
| 6 | `st_fuhua` | 上海复旦复华科技股份有限公司 | 600624.SH | 上海 | 上海市 |
| 7 | `shenda` | 上海申达股份有限公司 | 600626.SH | 上海 | 上海市 |
| 8 | `new_world` | 上海新世界股份有限公司 | 600628.SH | 上海 | 上海市 |
| 9 | `arcplus` | 华东建筑集团股份有限公司 | 600629.SH | 上海 | 上海市 |
| 10 | `dragon_head` | 上海龙头(集团)股份有限公司 | 600630.SH | 上海 | 上海市 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 海立股份 | air_conditioner_compressor | manufacture | 空调压缩机制造商 | 0.95 |
| 海立股份 | heat_pump | manufacture | 热泵制造商 | 0.9 |
| 天宸股份 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 天宸股份 | property_management | provide_service | 物业管理服务商 | 0.85 |
| 天宸股份 | passenger_transport | operate | 客运运营商 | 0.8 |
| 华鑫股份 | securities_service | provide_service | 证券服务商 | 0.95 |
| 华鑫股份 | financial_service | provide_service | 金融服务商 | 0.9 |
| 光大嘉宝 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 光大嘉宝 | capacitor | manufacture | 电容器制造商 | 0.9 |
| 华谊集团 | tire | produce | 轮胎生产商 | 0.95 |
| 华谊集团 | rubber_product | produce | 橡胶制品生产商 | 0.85 |
| ST复华 | manufacturing | operate | 制造业运营商 | 0.9 |
| ST复华 | real_estate_development | operate | 园区房地产运营商 | 0.85 |
| ST复华 | software | provide_service | 软件开发服务商 | 0.85 |
| 申达股份 | automotive_interior | produce | 汽车内饰生产商 | 0.95 |
| 申达股份 | textile_new_material | produce | 纺织新材料生产商 | 0.95 |
| 申达股份 | textile_product | produce | 纺织品生产商 | 0.9 |
| 新世界 | commercial | operate | 商业运营商 | 0.95 |
| 新世界 | retail | operate | 零售运营商 | 0.9 |
| 新世界 | department_store | operate | 百货运营商 | 0.95 |
| 华建集团 | engineering_survey | provide_service | 工程勘察服务商 | 0.95 |
| 华建集团 | municipal_design | provide_service | 市政设计服务商 | 0.95 |
| 华建集团 | construction_design | provide_service | 建筑设计服务商 | 0.95 |
| 龙头股份 | apparel_brand | operate | 服饰品牌运营商 | 0.95 |
| 龙头股份 | apparel | produce | 服装生产商 | 0.9 |
| 龙头股份 | textile_product | produce | 纺织品生产商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
