# Batch 071 Construction Log

**Date:** 2026-05-25
**Companies:** 600390.SH – 600403.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `superhard_material` | 超硬材料 | material |
| 2 | `battery_cathode_material` | 电池正极材料 | material |
| 3 | `aeroengine_part` | 航空发动机零部件 | component |
| 4 | `gas_turbine_part` | 燃气轮机零部件 | component |
| 5 | `rare_earth_metal` | 稀有稀土金属 | material |
| 6 | `catalytic_material` | 催化材料 | material |
| 7 | `alloy_structural_steel` | 合金结构钢 | material |
| 8 | `superalloy` | 高温合金 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `aeroengine_part_to_aircraft_engine` | aeroengine_part → aircraft_engine | composition |
| 2 | `battery_cathode_material_to_lithium_battery` | battery_cathode_material → lithium_battery | composition |
| 3 | `superalloy_to_aircraft_engine` | superalloy → aircraft_engine | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `minmetals_capital` | 五矿资本股份有限公司 | 600390.SH | 湖南 | 长沙市 |
| 2 | `aeroengine_tech` | 中国航发航空科技股份有限公司 | 600391.SH | 四川 | 成都市 |
| 3 | `shenghe_resources` | 盛和资源控股股份有限公司 | 600392.SH | 四川 | 成都市 |
| 4 | `panjiang` | 贵州盘江精煤股份有限公司 | 600395.SH | 贵州 | 六盘水市 |
| 5 | `huadian_liaoning` | 华电辽宁能源发展股份有限公司 | 600396.SH | 辽宁 | 沈阳市 |
| 6 | `jiangtungsten` | 江西江州联合造船有限责任公司 | 600397.SH | 江西 | 九江市 |
| 7 | `hla` | 海澜之家集团股份有限公司 | 600398.SH | 江苏 | 无锡市 |
| 8 | `fushun_special_steel` | 抚顺特殊钢股份有限公司 | 600399.SH | 辽宁 | 抚顺市 |
| 9 | `hongdou` | 红豆集团股份有限公司 | 600400.SH | 江苏 | 无锡市 |
| 10 | `dayou_energy` | 河南大有能源股份有限公司 | 600403.SH | 河南 | 三门峡市 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 五矿资本 | superhard_material | produce | 超硬材料生产商 | 0.9 |
| 五矿资本 | battery_cathode_material | produce | 电池正极材料生产商 | 0.85 |
| 五矿资本 | securities_service | provide_service | 证券服务商 | 0.95 |
| 五矿资本 | financial_service | provide_service | 综合金融服务商 | 0.9 |
| 航发科技 | aeroengine_part | manufacture | 航空发动机零部件制造商 | 0.95 |
| 航发科技 | gas_turbine_part | manufacture | 燃气轮机零部件制造商 | 0.9 |
| 航发科技 | aircraft_engine | manufacture | 航空发动机制造商 | 0.85 |
| 盛和资源 | rare_earth_metal | produce | 稀有稀土金属生产商 | 0.95 |
| 盛和资源 | catalytic_material | produce | 催化材料生产商 | 0.9 |
| 盛和资源 | rare_earth_mining | operate | 稀土矿山开采运营商 | 0.9 |
| 盘江股份 | coal | produce | 煤炭生产商 | 0.95 |
| 盘江股份 | coal_mining | operate | 煤炭开采运营商 | 0.9 |
| 华电辽能 | power_generation | operate | 火力发电运营商 | 0.95 |
| 华电辽能 | heating_supply | provide_service | 热力供应商 | 0.9 |
| 江钨装备 | coal_mining | operate | 煤炭开采运营商 | 0.95 |
| 江钨装备 | coal | operate | 煤炭经营商 | 0.9 |
| 海澜之家 | apparel | operate | 服装品牌运营商 | 0.95 |
| 海澜之家 | retail | operate | 零售运营商 | 0.9 |
| 抚顺特钢 | alloy_structural_steel | produce | 合金结构钢生产商 | 0.95 |
| 抚顺特钢 | superalloy | produce | 高温合金生产商 | 0.95 |
| 抚顺特钢 | stainless_steel | produce | 不锈钢生产商 | 0.9 |
| 抚顺特钢 | steel | produce | 特钢生产商 | 0.85 |
| 红豆股份 | apparel | produce | 服装生产商 | 0.95 |
| 红豆股份 | textile_product | produce | 纺织品生产商 | 0.9 |
| 大有能源 | coal | operate | 煤炭经营商 | 0.95 |
| 大有能源 | coal_mining | operate | 煤炭开采运营商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
