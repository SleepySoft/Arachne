# Batch 069 Construction Log

**Date:** 2026-05-25
**Companies:** 600366.SH – 600376.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `rare_earth_permanent_magnet` | 稀土永磁材料 | material |
| 2 | `barium_carbonate` | 碳酸钡 | material |
| 3 | `electrolytic_manganese_dioxide` | 电解二氧化锰 | material |
| 4 | `road_bridge` | 公路桥梁 | infrastructure |
| 5 | `printed_fabric` | 印染布 | material |
| 6 | `pbt_resin` | PBT树脂 | material |
| 7 | `starch_sugar` | 淀粉糖 | material |
| 8 | `avionics` | 航空电子 | system |
| 9 | `new_media` | 新媒体 | service |
| 10 | `heavy_truck` | 重型卡车 | system |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `rare_earth_permanent_magnet_to_motor` | rare_earth_permanent_magnet → large_motor | composition |
| 2 | `starch_sugar_to_beverage` | starch_sugar → beverage | material_flow |
| 3 | `avionics_to_aircraft` | avionics → trainer_aircraft | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `yunsheng` | 宁波韵升股份有限公司 | 600366.SH | 浙江 | 宁波 |
| 2 | `redstar_dev` | 贵州红星发展股份有限公司 | 600367.SH | 贵州 | 安顺 |
| 3 | `wuzhou_traffic` | 广西五洲交通股份有限公司 | 600368.SH | 广西 | 南宁 |
| 4 | `southwest_securities` | 西南证券股份有限公司 | 600369.SH | 重庆 | 重庆 |
| 5 | `st_sanfang` | 江苏三房巷聚材股份有限公司 | 600370.SH | 江苏 | 无锡 |
| 6 | `wanxiang_denong` | 万向德农股份有限公司 | 600371.SH | 黑龙江 | 哈尔滨 |
| 7 | `avic_systems` | 中航机载系统股份有限公司 | 600372.SH | 北京 | 北京 |
| 8 | `chinesemedia` | 中文天地出版传媒集团股份有限公司 | 600373.SH | 江西 | 上饶 |
| 9 | `hanma_tech` | 汉马科技集团股份有限公司 | 600375.SH | 安徽 | 马鞍山 |
| 10 | `shoukai` | 北京首都开发股份有限公司 | 600376.SH | 北京 | 北京 |

## 4. Company Node Exposures (+24)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 宁波韵升 | rare_earth_permanent_magnet | produce | 稀土永磁材料生产商 | 0.95 |
| 宁波韵升 | rare_earth_functional | produce | 稀土功能材料生产商 | 0.9 |
| 红星发展 | barium_carbonate | produce | 碳酸钡生产商 | 0.95 |
| 红星发展 | electrolytic_manganese_dioxide | produce | 电解二氧化锰生产商 | 0.9 |
| 红星发展 | chemical_product | produce | 化工产品生产商 | 0.85 |
| 五洲交通 | road_bridge | operate | 公路桥梁运营商 | 0.95 |
| 五洲交通 | toll_road | operate | 路桥收费运营商 | 0.9 |
| 西南证券 | securities_service | provide_service | 证券服务商 | 0.95 |
| 西南证券 | financial_service | provide_service | 金融服务商 | 0.9 |
| *ST三房 | printed_fabric | produce | 印染布生产商 | 0.9 |
| *ST三房 | pbt_resin | produce | PBT树脂生产商 | 0.85 |
| *ST三房 | textile_product | produce | 纺织品生产商 | 0.8 |
| 万向德农 | seed | produce | 种子生产商 | 0.95 |
| 万向德农 | starch_sugar | produce | 淀粉糖生产商 | 0.9 |
| 万向德农 | agricultural_product | produce | 农产品生产商 | 0.85 |
| 中航机载 | avionics | manufacture | 航空电子制造商 | 0.95 |
| 中航机载 | flight_control | manufacture | 飞行控制系统制造商 | 0.9 |
| 中航机载 | aircraft_electromechanical | manufacture | 航空机电系统制造商 | 0.9 |
| 中文传媒 | publishing_media | provide_service | 出版传媒服务商 | 0.95 |
| 中文传媒 | new_media | provide_service | 新媒体服务商 | 0.85 |
| 汉马科技 | heavy_truck | manufacture | 重型卡车制造商 | 0.95 |
| 汉马科技 | special_vehicle | manufacture | 专用车制造商 | 0.9 |
| 汉马科技 | automobile_part | manufacture | 汽车零部件制造商 | 0.85 |
| 首开股份 | real_estate_development | operate | 房地产开发运营商 | 0.95 |

---

**Graph increment:** Nodes +9, Edges +3
