# Batch 081 Construction Log

**Date:** 2026-05-25
**Companies:** 600537.SH – 600549.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `silicon_ingot` | 硅棒 | material |
| 2 | `water_purifier_faucet` | 净水龙头 | device |
| 3 | `cotton_seed` | 棉种 | material |
| 4 | `malt` | 大麦芽 | material |
| 5 | `intelligent_textile_equipment` | 智能化纺织成套设备 | system |
| 6 | `tungsten_concentrate` | 钨精矿 | material |
| 7 | `cemented_carbide` | 硬质合金 | material |
| 8 | `gold_jewelry` | 黄金珠宝饰品 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `silicon_ingot_to_solar_cell` | silicon_ingot → solar_cell | material_flow |
| 2 | `tungsten_concentrate_to_cemented_carbide` | tungsten_concentrate → cemented_carbide | material_flow |
| 3 | `cemented_carbide_to_cutting_tool` | cemented_carbide → cutting_tool | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `st_yijing` | 亿晶光电科技股份有限公司 | 600537.SH | 江苏 | 常州市 |
| 2 | `guofa` | 北海国发川山生物股份有限公司 | 600538.SH | 广西 | 北海市 |
| 3 | `shitou` | 太原狮头水泥股份有限公司 | 600539.SH | 山西 | 太原市 |
| 4 | `xinsai` | 新疆赛里木现代农业股份有限公司 | 600540.SH | 新疆 | 博尔塔拉 |
| 5 | `st_mogao` | 甘肃莫高实业发展股份有限公司 | 600543.SH | 甘肃 | 兰州市 |
| 6 | `saurer` | 卓郎智能技术股份有限公司 | 600545.SH | 新疆 | 乌鲁木齐市 |
| 7 | `shanmei_intl` | 山煤国际能源集团股份有限公司 | 600546.SH | 山西 | 太原市 |
| 8 | `shandong_gold` | 山东黄金矿业股份有限公司 | 600547.SH | 山东 | 济南市 |
| 9 | `shenzhen_expressway` | 深圳高速公路集团股份有限公司 | 600548.SH | 广东 | 深圳市 |
| 10 | `xiamen_tungsten` | 厦门钨业股份有限公司 | 600549.SH | 福建 | 厦门市 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| *ST亿晶 | silicon_ingot | produce | 硅棒生产商 | 0.95 |
| *ST亿晶 | solar_cell | produce | 太阳能电池片生产商 | 0.95 |
| *ST亿晶 | photovoltaic | produce | 光伏组件生产商 | 0.9 |
| 国发股份 | pesticide | produce | 农药生产商 | 0.95 |
| 国发股份 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 国发股份 | hotel_service | operate | 酒店服务商 | 0.8 |
| 狮头股份 | water_purifier_faucet | manufacture | 净水龙头制造商 | 0.95 |
| 狮头股份 | water_treatment | operate | 污水处理运营商 | 0.9 |
| 新赛股份 | cotton | produce | 棉花生产商 | 0.95 |
| 新赛股份 | cotton_seed | produce | 棉种生产商 | 0.9 |
| *ST莫高 | malt | produce | 大麦芽生产商 | 0.95 |
| *ST莫高 | wine | produce | 葡萄酒生产商 | 0.9 |
| *ST莫高 | licorice | produce | 甘草系列产品生产商 | 0.85 |
| 卓郎智能 | intelligent_textile_equipment | manufacture | 智能化纺织成套设备制造商 | 0.95 |
| 卓郎智能 | textile_machinery | manufacture | 纺织机械制造商 | 0.9 |
| 山煤国际 | coal | operate | 煤炭经营商 | 0.95 |
| 山煤国际 | coal_mining | operate | 煤炭开采运营商 | 0.9 |
| 山东黄金 | gold | produce | 黄金生产商 | 0.95 |
| 山东黄金 | gold_jewelry | produce | 黄金珠宝饰品生产商 | 0.9 |
| 深高速 | expressway | operate | 高速公路运营商 | 0.95 |
| 深高速 | toll_road | operate | 路桥收费运营商 | 0.9 |
| 厦门钨业 | tungsten_concentrate | produce | 钨精矿生产商 | 0.95 |
| 厦门钨业 | cemented_carbide | produce | 硬质合金生产商 | 0.95 |
| 厦门钨业 | cutting_tool | produce | 切削刀具生产商 | 0.9 |
| 厦门钨业 | rare_earth_metal | produce | 稀土金属生产商 | 0.85 |
| 厦门钨业 | lithium_battery | produce | 锂电池生产商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
