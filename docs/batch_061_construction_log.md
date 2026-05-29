# Batch 061 Construction Log

**Date:** 2026-05-25
**Companies:** 600257.SH – 600269.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `aquatic_product` | 水产品 | material |
| 2 | `hotel` | 酒店服务 | service |
| 3 | `rare_earth_metal` | 稀土金属 | material |
| 4 | `tungsten` | 钨 | material |
| 5 | `lighting_equipment` | 照明设备 | device |
| 6 | `mining_truck` | 矿用自卸车 | device |
| 7 | `forest_chemical` | 林化产品 | material |
| 8 | `power_grid_protection` | 电网保护自动化 | service |
| 9 | `expressway` | 高速公路 | infrastructure |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `aquatic_product_to_food` | aquatic_product → food | material_flow |
| 2 | `forest_chemical_to_timber` | forest_chemical → timber | material_flow |
| 3 | `power_grid_protection_to_power_grid` | power_grid_protection → power_grid | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `dahu` | 大湖健康产业股份有限公司 | 600257.SH | 湖南 | 常德 |
| 2 | `btg_hotels` | 北京首旅酒店(集团)股份有限公司 | 600258.SH | 北京 | 北京 |
| 3 | `chinanonferrous` | 中稀有色金属股份有限公司 | 600259.SH | 海南 | 海口 |
| 4 | `yankon` | 浙江阳光照明电器集团股份有限公司 | 600261.SH | 浙江 | 绍兴 |
| 5 | `northhaul` | 内蒙古北方重型汽车股份有限公司 | 600262.SH | 内蒙古 | 包头 |
| 6 | `st_jinggu` | 云南景谷林业股份有限公司 | 600265.SH | 云南 | 普洱 |
| 7 | `ucd` | 北京城建投资发展股份有限公司 | 600266.SH | 北京 | 北京 |
| 8 | `hisun_pharma` | 浙江海正药业股份有限公司 | 600267.SH | 浙江 | 台州 |
| 9 | `guodian_nanz` | 国电南京自动化股份有限公司 | 600268.SH | 江苏 | 南京 |
| 10 | `ganyue` | 江西赣粤高速公路股份有限公司 | 600269.SH | 江西 | 南昌 |

## 4. Company Node Exposures (+20)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 大湖股份 | aquatic_product | produce | 水产品生产商 | 0.9 |
| 大湖股份 | chinese_patent_medicine | produce | 中成药生产商 | 0.8 |
| 大湖股份 | baijiu | produce | 白酒生产商 | 0.75 |
| 首旅酒店 | hotel | operate | 酒店运营商 | 0.95 |
| 首旅酒店 | tourism_service | provide_service | 旅游服务商 | 0.8 |
| 中稀有色 | rare_earth_metal | produce | 稀土金属生产商 | 0.95 |
| 中稀有色 | tungsten | produce | 钨生产商 | 0.9 |
| 阳光照明 | lighting_equipment | manufacture | 照明设备制造商 | 0.95 |
| 阳光照明 | led_display | manufacture | LED显示器件制造商 | 0.85 |
| 北方股份 | mining_truck | manufacture | 矿用自卸车制造商 | 0.95 |
| 北方股份 | construction_machinery | manufacture | 工程机械制造商 | 0.85 |
| *ST景谷 | forest_chemical | produce | 林化产品生产商 | 0.9 |
| *ST景谷 | timber | produce | 林木产品生产商 | 0.85 |
| 城建发展 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 海正药业 | chemical_pharmaceutical | produce | 化学制药生产商 | 0.95 |
| 海正药业 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 国电南自 | power_grid_protection | provide_service | 电网保护自动化服务商 | 0.95 |
| 国电南自 | power_automation | manufacture | 电力自动化设备制造商 | 0.9 |
| 赣粤高速 | expressway | operate | 高速公路运营商 | 0.95 |
| 赣粤高速 | toll_road | operate | 路桥收费运营商 | 0.9 |

---

**Graph increment:** Nodes +6, Edges +3
