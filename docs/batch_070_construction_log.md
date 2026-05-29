# Batch 070 Construction Log

**Date:** 2026-05-25
**Companies:** 600377.SH – 600389.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+11)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `catalyst` | 催化剂 | material |
| 2 | `specialty_gas` | 特种气体 | material |
| 3 | `specialty_valve` | 特种阀门 | component |
| 4 | `vacuum_switchgear` | 真空开关设备 | device |
| 5 | `health_product` | 保健品 | material |
| 6 | `cordyceps` | 冬虫夏草 | material |
| 7 | `iron_ore` | 铁矿石 | material |
| 8 | `bus_advertising` | 公交广告 | service |
| 9 | `auto_service` | 汽车服务 | service |
| 10 | `electrostatic_precipitator` | 电除尘器 | device |
| 11 | `desulfurization` | 脱硫设备 | device |
| 12 | `glyphosate` | 草甘膦 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `catalyst_to_chemical_industry` | catalyst → chemical_industry | capability_supply |
| 2 | `vacuum_switchgear_to_power_grid` | vacuum_switchgear → power_grid | composition |
| 3 | `electrostatic_precipitator_to_power_plant` | electrostatic_precipitator → power_generation | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `ninghu_expressway` | 江苏宁沪高速公路股份有限公司 | 600377.SH | 江苏 | 南京 |
| 2 | `haohua_tech` | 昊华化工科技集团股份有限公司 | 600378.SH | 四川 | 成都 |
| 3 | `baoguang` | 陕西宝光真空电器股份有限公司 | 600379.SH | 陕西 | 宝鸡 |
| 4 | `joincare` | 健康元药业集团股份有限公司 | 600380.SH | 广东 | 深圳 |
| 5 | `st_chuntian` | 青海春天药用资源科技股份有限公司 | 600381.SH | 青海 | 西宁 |
| 6 | `guangdong_mingzhu` | 广东明珠集团股份有限公司 | 600382.SH | 广东 | 梅州 |
| 7 | `gemdale` | 金地(集团)股份有限公司 | 600383.SH | 广东 | 深圳 |
| 8 | `beibamedia` | 北京巴士传媒股份有限公司 | 600386.SH | 北京 | 北京 |
| 9 | `longking` | 福建龙净环保股份有限公司 | 600388.SH | 福建 | 龙岩 |
| 10 | `jiangshan` | 南通江山农药化工股份有限公司 | 600389.SH | 江苏 | 南通 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 宁沪高速 | expressway | operate | 高速公路运营商 | 0.95 |
| 宁沪高速 | toll_road | operate | 路桥收费运营商 | 0.9 |
| 昊华科技 | catalyst | produce | 催化剂生产商 | 0.95 |
| 昊华科技 | specialty_gas | produce | 特种气体生产商 | 0.9 |
| 昊华科技 | specialty_valve | manufacture | 特种阀门制造商 | 0.85 |
| 昊华科技 | chemical_product | produce | 化工产品生产商 | 0.85 |
| 宝光股份 | vacuum_switchgear | manufacture | 真空开关设备制造商 | 0.95 |
| 宝光股份 | switchgear | manufacture | 开关设备制造商 | 0.9 |
| 宝光股份 | power_distribution_equipment | manufacture | 配电设备制造商 | 0.85 |
| 健康元 | health_product | produce | 保健品生产商 | 0.9 |
| 健康元 | pharmaceutical | produce | 药品生产商 | 0.85 |
| *ST春天 | cordyceps | produce | 冬虫夏草产品生产商 | 0.95 |
| *ST春天 | chinese_patent_medicine | produce | 中成药生产商 | 0.85 |
| 广东明珠 | iron_ore | produce | 铁矿石生产商 | 0.85 |
| 广东明珠 | land_development | operate | 土地开发运营商 | 0.8 |
| 金地集团 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 金地集团 | property_management | provide_service | 物业管理服务商 | 0.85 |
| 北巴传媒 | bus_advertising | provide_service | 公交广告服务商 | 0.9 |
| 北巴传媒 | auto_service | provide_service | 汽车服务商 | 0.85 |
| 龙净环保 | electrostatic_precipitator | manufacture | 电除尘器制造商 | 0.95 |
| 龙净环保 | desulfurization | manufacture | 脱硫设备制造商 | 0.9 |
| 龙净环保 | solid_waste_treatment | provide_service | 固废处理服务商 | 0.85 |
| 龙净环保 | environmental_service | provide_service | 环保服务提供商 | 0.9 |
| 江山股份 | glyphosate | produce | 草甘膦生产商 | 0.95 |
| 江山股份 | pesticide | produce | 农药生产商 | 0.9 |
| 江山股份 | caustic_soda | produce | 烧碱生产商 | 0.85 |

---

**Graph increment:** Nodes +11, Edges +3
