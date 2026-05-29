# Batch 089 Construction Log

**Date:** 2026-05-25
**Companies:** 600633.SH – 600643.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `advertising` | 广告 | service |
| 2 | `tunnel_bridge_facility` | 隧桥设施 | infrastructure |
| 3 | `fluoropolymer` | 含氟聚合物 | material |
| 4 | `cfc_substitute` | CFC替代品 | material |
| 5 | `audio_visual` | 网络视听 | service |
| 6 | `online_game` | 网络游戏 | service |
| 7 | `golf` | 高尔夫 | service |
| 8 | `cultural_supplies` | 文化用品 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `tunnel_bridge_facility_to_transportation` | tunnel_bridge_facility → transportation | capability_supply |
| 2 | `fluoropolymer_to_chemical_industry` | fluoropolymer → chemical_industry | material_flow |
| 3 | `online_game_to_internet` | online_game → internet | service_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `zheshu` | 浙报数字文化集团股份有限公司 | 600633.SH | 浙江 | 杭州市 |
| 2 | `dazhong_public` | 上海大众公用事业(集团)股份有限公司 | 600635.SH | 上海 | 上海市 |
| 3 | `st_guohua` | 国新文化控股股份有限公司 | 600636.SH | 上海 | 上海市 |
| 4 | `oriental_pearl` | 东方明珠新媒体股份有限公司 | 600637.SH | 上海 | 上海市 |
| 5 | `xinhuangpu` | 上海新黄浦实业集团股份有限公司 | 600638.SH | 上海 | 上海市 |
| 6 | `pudong_jinqiao` | 上海浦东金桥出口加工区开发股份有限公司 | 600639.SH | 上海 | 上海市 |
| 7 | `guomai_culture` | 新国脉数字文化股份有限公司 | 600640.SH | 上海 | 上海市 |
| 8 | `xiandao` | 上海万业企业股份有限公司 | 600641.SH | 上海 | 上海市 |
| 9 | `shenergy` | 申能股份有限公司 | 600642.SH | 上海 | 上海市 |
| 10 | `aijian` | 上海爱建集团股份有限公司 | 600643.SH | 上海 | 上海市 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 浙数文化 | advertising | provide_service | 广告服务商 | 0.95 |
| 浙数文化 | new_media_technology | provide_service | 新媒体技术服务商 | 0.9 |
| 浙数文化 | cultural_supplies | produce | 文化用品生产商 | 0.85 |
| 大众公用 | city_gas | operate | 城市燃气运营商 | 0.95 |
| 大众公用 | tunnel_bridge_facility | operate | 隧桥设施运营商 | 0.9 |
| 大众公用 | sewage_treatment | operate | 污水处理运营商 | 0.9 |
| *ST国化 | fluoropolymer | produce | 含氟聚合物生产商 | 0.95 |
| *ST国化 | cfc_substitute | produce | CFC替代品生产商 | 0.95 |
| *ST国化 | fluorine_refrigerant | produce | 氟致冷剂生产商 | 0.9 |
| 东方明珠 | audio_visual | provide_service | 网络视听服务商 | 0.95 |
| 东方明珠 | online_game | provide_service | 网络游戏服务商 | 0.9 |
| 东方明珠 | internet | provide_service | 互联网服务商 | 0.85 |
| 新黄浦 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 新黄浦 | industrial | operate | 工业运营商 | 0.8 |
| 浦东金桥 | real_estate_development | operate | 房地产销售运营商 | 0.95 |
| 浦东金桥 | real_estate_leasing | operate | 房地产租赁运营商 | 0.9 |
| 国脉文化 | tourism_service | provide_service | 旅游预订服务商 | 0.95 |
| 国脉文化 | hotel_service | operate | 酒店经营商 | 0.9 |
| 先导基电 | real_estate_development | operate | 商品房开发商 | 0.95 |
| 先导基电 | hotel_service | operate | 酒店运营商 | 0.85 |
| 先导基电 | golf | operate | 高尔夫运营商 | 0.8 |
| 申能股份 | power_generation | operate | 电力运营商 | 0.95 |
| 申能股份 | oil_gas | operate | 石油天然气运营商 | 0.9 |
| 爱建集团 | industrial | operate | 工业运营商 | 0.9 |
| 爱建集团 | commercial | operate | 商业运营商 | 0.85 |
| 爱建集团 | tourism_service | provide_service | 旅游饮食服务商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
