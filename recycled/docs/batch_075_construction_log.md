# Batch 075 Construction Log

**Date:** 2026-05-25
**Companies:** 600459.SH – 600476.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `precious_metal_functional_material` | 贵金属特种功能材料 | material |
| 2 | `integrated_circuit` | 集成电路 | component |
| 3 | `semiconductor_discrete_device` | 半导体分立器件 | component |
| 4 | `led_product` | LED产品 | component |
| 5 | `water_supply` | 自来水供应 | service |
| 6 | `city_sewage_treatment` | 城市污水处理 | service |
| 7 | `sea_cucumber` | 海参 | material |
| 8 | `phosphate_fertilizer` | 磷肥 | material |
| 9 | `power_generation_equipment` | 发电设备 | device |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `integrated_circuit_to_electronic_device` | integrated_circuit → electronic_device | composition |
| 2 | `led_product_to_lighting` | led_product → lighting | composition |
| 3 | `power_generation_equipment_to_power_generation` | power_generation_equipment → power_generation | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `sino_platinum` | 贵研铂业股份有限公司 | 600459.SH | 云南 | 昆明市 |
| 2 | `silan` | 杭州士兰微电子股份有限公司 | 600460.SH | 浙江 | 杭州市 |
| 3 | `hongcheng_env` | 江西洪城环境股份有限公司 | 600461.SH | 江西 | 南昌市 |
| 4 | `airport_co` | 北京空港科技园区股份有限公司 | 600463.SH | 北京 | 北京市 |
| 5 | `haodangjia` | 山东好当家海洋发展股份有限公司 | 600467.SH | 山东 | 威海市 |
| 6 | `baili_elec` | 天津百利特精电气股份有限公司 | 600468.SH | 天津 | 天津市 |
| 7 | `aeolus` | 风神轮胎股份有限公司 | 600469.SH | 河南 | 焦作市 |
| 8 | `liuguo_chem` | 安徽六国化工股份有限公司 | 600470.SH | 安徽 | 铜陵市 |
| 9 | `huaguang` | 无锡华光环保能源集团股份有限公司 | 600475.SH | 江苏 | 无锡市 |
| 10 | `st_xiangyou` | 湖南湘邮科技股份有限公司 | 600476.SH | 湖南 | 长沙市 |

## 4. Company Node Exposures (+29)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 贵研铂业 | precious_metal_functional_material | produce | 贵金属功能材料生产商 | 0.95 |
| 贵研铂业 | catalytic_functional_material | produce | 催化功能材料生产商 | 0.9 |
| 贵研铂业 | nonferrous_metal | produce | 有色金属生产商 | 0.9 |
| 士兰微 | integrated_circuit | manufacture | 集成电路制造商 | 0.95 |
| 士兰微 | semiconductor_discrete_device | manufacture | 半导体分立器件制造商 | 0.9 |
| 士兰微 | led_product | manufacture | LED产品制造商 | 0.9 |
| 士兰微 | electronic_component | manufacture | 电子元器件制造商 | 0.85 |
| 洪城环境 | water_supply | provide_service | 自来水供应商 | 0.95 |
| 洪城环境 | city_sewage_treatment | operate | 污水处理运营商 | 0.9 |
| 洪城环境 | gas_energy | provide_service | 燃气能源供应商 | 0.85 |
| 空港股份 | industrial_park | operate | 产业园区运营商 | 0.95 |
| 空港股份 | real_estate_development | operate | 房地产开发运营商 | 0.9 |
| 空港股份 | construction | operate | 建筑施工运营商 | 0.85 |
| 好当家 | sea_cucumber | produce | 海参生产商 | 0.95 |
| 好当家 | seafood | produce | 海产品生产商 | 0.9 |
| 好当家 | aquaculture | operate | 水产养殖运营商 | 0.9 |
| 百利电气 | power_distribution_equipment | manufacture | 输配电设备制造商 | 0.95 |
| 百利电气 | pump | manufacture | 水泵制造商 | 0.9 |
| 百利电气 | tungsten_molybdenum_product | produce | 钨钼制品生产商 | 0.85 |
| 风神股份 | tire | manufacture | 轮胎制造商 | 0.95 |
| 风神股份 | automobile_part | manufacture | 汽车零部件制造商 | 0.9 |
| 六国化工 | phosphate_fertilizer | produce | 磷肥生产商 | 0.95 |
| 六国化工 | chemical_product | produce | 化工产品生产商 | 0.9 |
| 华光环能 | power_generation_equipment | manufacture | 发电设备制造商 | 0.95 |
| 华光环能 | environmental_equipment | manufacture | 环保设备制造商 | 0.9 |
| 华光环能 | energy_supply | provide_service | 能源供应服务商 | 0.85 |
| *ST湘邮 | software | provide_service | 软件服务商 | 0.95 |
| *ST湘邮 | system_integration | provide_service | 系统集成服务商 | 0.9 |
| *ST湘邮 | postal_equipment | manufacture | 邮政设备制造商 | 0.85 |

---

**Graph increment:** Nodes +9, Edges +3
