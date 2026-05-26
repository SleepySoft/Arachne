# Batch 054 Construction Log

**Date:** 2026-05-25
**Companies:** 600166.SH – 600177.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+7)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `automobile` | 汽车整车 | system |
| 2 | `heating_supply` | 供热服务 | service |
| 3 | `water_treatment` | 水务处理 | service |
| 4 | `construction_machinery` | 工程机械 | device |
| 5 | `construction_engineering` | 建筑工程 | service |
| 6 | `integrated_circuit` | 集成电路 | component |
| 7 | `synthetic_diamond` | 人造金刚石 | material |
| 8 | `fiberglass` | 玻璃纤维 | material |
| 9 | `garment` | 服装 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `fiberglass_to_composite_material` | fiberglass → composite_material | composition |
| 2 | `synthetic_diamond_to_cutting_tool` | synthetic_diamond → cutting_tool | material_flow |
| 3 | `construction_machinery_to_construction_engineering` | construction_machinery → construction_engineering | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `foton_motor` | 北汽福田汽车股份有限公司 | 600166.SH | 北京 | 北京 |
| 2 | `lianmei` | 联美量子股份有限公司 | 600167.SH | 辽宁 | 沈阳 |
| 3 | `wuhan_water` | 武汉三镇实业控股股份有限公司 | 600168.SH | 湖北 | 武汉 |
| 4 | `st_taiyuan` | 太原重工股份有限公司 | 600169.SH | 山西 | 太原 |
| 5 | `shanghai_const` | 上海建工集团股份有限公司 | 600170.SH | 上海 | 上海 |
| 6 | `belling` | 上海贝岭股份有限公司 | 600171.SH | 上海 | 上海 |
| 7 | `yellow_river` | 河南黄河旋风股份有限公司 | 600172.SH | 河南 | 许昌 |
| 8 | `wolong_new_energy` | 卧龙新能源集团股份有限公司 | 600173.SH | 浙江 | 绍兴 |
| 9 | `china_jushi` | 中国巨石股份有限公司 | 600176.SH | 浙江 | 嘉兴 |
| 10 | `youngor` | 雅戈尔时尚股份有限公司 | 600177.SH | 浙江 | 宁波 |

## 4. Company Node Exposures (+19)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 福田汽车 | automobile | manufacture | 汽车整车制造商 | 0.95 |
| 福田汽车 | automobile_part | manufacture | 汽车零部件制造商 | 0.9 |
| 福田汽车 | new_energy_vehicle | manufacture | 新能源汽车制造商 | 0.85 |
| 联美控股 | heating_supply | provide_service | 供热服务供应商 | 0.95 |
| 联美控股 | water_supply | provide_service | 供水服务供应商 | 0.85 |
| 武汉控股 | water_treatment | provide_service | 水务处理运营商 | 0.95 |
| ST太重 | construction_machinery | manufacture | 工程机械制造商 | 0.9 |
| ST太重 | special_steel | produce | 特种钢生产商 | 0.85 |
| 上海建工 | construction_engineering | provide_service | 建筑工程承包商 | 0.95 |
| 上海贝岭 | integrated_circuit | manufacture | 集成电路制造商 | 0.9 |
| 上海贝岭 | semiconductor_device | manufacture | 半导体器件制造商 | 0.85 |
| 黄河旋风 | synthetic_diamond | produce | 人造金刚石生产商 | 0.95 |
| 黄河旋风 | cutting_tool | manufacture | 切削工具制造商 | 0.8 |
| 卧龙新能 | real_estate_development | operate | 房地产开发运营商 | 0.9 |
| 卧龙新能 | wind_power_equipment | manufacture | 风电设备制造商 | 0.75 |
| 中国巨石 | fiberglass | produce | 玻璃纤维生产商 | 0.95 |
| 中国巨石 | composite_material | produce | 复合材料生产商 | 0.85 |
| 雅戈尔 | garment | produce | 服装生产商 | 0.9 |
| 雅戈尔 | real_estate_development | operate | 房地产开发运营商 | 0.85 |

---

**Graph increment:** Nodes +7, Edges +3
