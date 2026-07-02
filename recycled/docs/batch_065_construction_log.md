# Batch 065 Construction Log

**Date:** 2026-05-25
**Companies:** 600313.SH – 600326.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+10)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `seed` | 种子 | material |
| 2 | `agricultural_material` | 农资 | service |
| 3 | `daily_chemical_product` | 日用化学品 | material |
| 4 | `trainer_aircraft` | 教练机 | system |
| 5 | `general_aviation` | 通用航空 | service |
| 6 | `financial_service` | 金融服务 | service |
| 7 | `cpe` | 氯化聚乙烯 | material |
| 8 | `caustic_soda` | 烧碱 | material |
| 9 | `port_crane` | 港口起重机 | device |
| 10 | `offshore_equipment` | 海洋工程装备 | system |
| 11 | `solid_waste_treatment` | 固废处理 | service |
| 12 | `road_engineering` | 公路工程 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `seed_to_agricultural_product` | seed → agricultural_product | material_flow |
| 2 | `trainer_aircraft_to_aviation` | trainer_aircraft → air_transport | capability_supply |
| 3 | `port_crane_to_port_logistics` | port_crane → port_logistics | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `cn_agriseed` | 中农发种业集团股份有限公司 | 600313.SH | 北京 | 北京 |
| 2 | `jahwa` | 上海家化联合股份有限公司 | 600315.SH | 上海 | 上海 |
| 3 | `hongdu_aviation` | 江西洪都航空工业股份有限公司 | 600316.SH | 江西 | 南昌 |
| 4 | `xinli_finance` | 安徽新力金融股份有限公司 | 600318.SH | 安徽 | 合肥 |
| 5 | `yaxing_chem` | 潍坊亚星化学股份有限公司 | 600319.SH | 山东 | 潍坊 |
| 6 | `zpmc` | 上海振华重工(集团)股份有限公司 | 600320.SH | 上海 | 上海 |
| 7 | `tianjin_ucd` | 天津津投城市开发股份有限公司 | 600322.SH | 天津 | 天津 |
| 8 | `hanlan` | 瀚蓝环境股份有限公司 | 600323.SH | 广东 | 佛山 |
| 9 | `huafa` | 珠海华发实业股份有限公司 | 600325.SH | 广东 | 珠海 |
| 10 | `tibet_road` | 西藏天路股份有限公司 | 600326.SH | 西藏 | 拉萨 |

## 4. Company Node Exposures (+27)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 农发种业 | seed | produce | 种子生产商 | 0.95 |
| 农发种业 | agricultural_material | provide_service | 农资供应商 | 0.9 |
| 农发种业 | agricultural_product | produce | 农产品生产商 | 0.85 |
| 上海家化 | daily_chemical_product | produce | 日用化学品生产商 | 0.95 |
| 上海家化 | cosmetics | produce | 化妆品生产商 | 0.9 |
| 上海家化 | toothpaste | produce | 牙膏生产商 | 0.85 |
| 洪都航空 | trainer_aircraft | manufacture | 教练机制造商 | 0.95 |
| 洪都航空 | general_aviation | provide_service | 通用航空服务商 | 0.85 |
| 洪都航空 | defense_equipment | manufacture | 防务装备制造商 | 0.8 |
| 新力金融 | cement | produce | 水泥生产商 | 0.85 |
| 新力金融 | financial_service | provide_service | 金融服务商 | 0.8 |
| 亚星化学 | cpe | produce | 氯化聚乙烯生产商 | 0.95 |
| 亚星化学 | pvc | produce | 聚氯乙烯生产商 | 0.9 |
| 亚星化学 | caustic_soda | produce | 烧碱生产商 | 0.9 |
| 亚星化学 | chlor_alkali_product | produce | 氯碱化工产品生产商 | 0.85 |
| 振华重工 | port_crane | manufacture | 港口起重机制造商 | 0.95 |
| 振华重工 | offshore_equipment | manufacture | 海洋工程装备制造商 | 0.9 |
| 振华重工 | construction_machinery | manufacture | 工程机械制造商 | 0.85 |
| 津投城开 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 瀚蓝环境 | water_supply | provide_service | 供水服务商 | 0.95 |
| 瀚蓝环境 | sewage_treatment | provide_service | 污水处理服务商 | 0.9 |
| 瀚蓝环境 | solid_waste_treatment | provide_service | 固废处理服务商 | 0.9 |
| 瀚蓝环境 | power_generation | operate | 发电运营商 | 0.85 |
| 华发股份 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 西藏天路 | road_engineering | provide_service | 公路工程承包商 | 0.95 |
| 西藏天路 | cement | produce | 水泥生产商 | 0.85 |
| 西藏天路 | construction_engineering | provide_service | 建筑工程承包商 | 0.8 |

---

**Graph increment:** Nodes +10, Edges +3
