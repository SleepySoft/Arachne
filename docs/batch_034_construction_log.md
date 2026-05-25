# Batch 034 Construction Log

**Date:** 2026-05-25
**Companies:** 000881.SZ – 000903.SZ (20 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+5)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `radiation_technology` | 核技术应用 | technology_capability |
| 2 | `polymer_material` | 高分子材料 | material |
| 3 | `rubber_seal` | 橡胶密封件 | component |
| 4 | `scenic_area` | 旅游景区 | service |
| 5 | `ropeway` | 客运索道 | infrastructure |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_polymer_to_seal` | polymer_material → rubber_seal | material_flow |

## 3. Companies Registered (+20)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `cgnn_tech` | 中广核核技术发展股份有限公司 | 000881.SZ | 辽宁 | 大连市 | 4,338 |
| 2 | `bhg_mall` | 北京华联商厦股份有限公司 | 000882.SZ | 北京 | 北京市 | 1,119 |
| 3 | `hubei_energy` | 湖北能源集团股份有限公司 | 000883.SZ | 湖北 | 武汉市 | 4,629 |
| 4 | `citydev_env` | 城发环境股份有限公司 | 000885.SZ | 河南 | 郑州市 | 4,573 |
| 5 | `hainan_expressway` | 海南高速公路股份有限公司 | 000886.SZ | 海南 | 海口市 | 1,527 |
| 6 | `zhongding` | 安徽中鼎密封件股份有限公司 | 000887.SZ | 安徽 | 宣城市 | 22,935 |
| 7 | `emei_shan` | 峨眉山旅游股份有限公司 | 000888.SZ | 四川 | 乐山市 | 2,034 |
| 8 | `zhongjiabochuang` | 中嘉博创信息技术股份有限公司 | 000889.SZ | 河北 | 秦皇岛市 | 2,331 |
| 9 | `farsighted` | 江苏法尔胜股份有限公司 | 000890.SZ | 江苏 | 无锡市 | 347 |
| 10 | `huanrui_century` | 欢瑞世纪联合股份有限公司 | 000892.SZ | 重庆 | 重庆市 | 141 |
| 11 | `asia_potash` | 亚钾国际投资(广州)股份有限公司 | 000893.SZ | 广东 | 广州市 | 5,808 |
| 12 | `shuanghui` | 河南双汇投资发展股份有限公司 | 000895.SZ | 河南 | 漯河市 | 46,352 |
| 13 | `yuneeng_holdings` | 河南豫能控股股份有限公司 | 001896.SZ | 河南 | 郑州市 | 3,457 |
| 14 | `tianjin_jinbin` | 天津津滨发展股份有限公司 | 000897.SZ | 天津 | 天津市 | 297 |
| 15 | `angang_steel` | 鞍钢股份有限公司 | 000898.SZ | 辽宁 | 鞍山市 | 23,990 |
| 16 | `ganeng_power` | 江西赣能股份有限公司 | 000899.SZ | 江西 | 南昌市 | 1,022 |
| 17 | `modern_investment` | 现代投资股份有限公司 | 000900.SZ | 湖南 | 长沙市 | 2,767 |
| 18 | `aerospace_tech` | 航天科技控股集团股份有限公司 | 000901.SZ | 黑龙江 | 哈尔滨市 | 6,043 |
| 19 | `xinyangfeng` | 新洋丰农业科技股份有限公司 | 000902.SZ | 湖北 | 荆门市 | 8,315 |
| 20 | `st_yundong` | 昆明云内动力股份有限公司 | 000903.SZ | 云南 | 昆明市 | 2,594 |

## 4. Company Node Exposures (+39)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 中广核技 | radiation_technology | operate | 核技术应用服务商 | 0.7 |
| 中广核技 | polymer_material | produce | 高分子材料生产商 | 0.6 |
| 华联股份 | department_store | operate | 百货零售商 | 0.9 |
| 湖北能源 | hydro_power_generation | operate | 水电运营商 | 0.9 |
| 湖北能源 | coal_power_generation | operate | 火电运营商 | 0.8 |
| 湖北能源 | natural_gas | produce | 天然气输配商 | 0.6 |
| 城发环境 | municipal_waste_treatment | operate | 城市废弃物处理运营商 | 0.9 |
| 城发环境 | highway_operation_service | operate | 高速公路运营商 | 0.7 |
| 海南高速 | highway_operation_service | operate | 高速公路运营商 | 0.9 |
| 海南高速 | real_estate_development | operate | 房地产开发商 | 0.6 |
| 海南高速 | tourism_service | operate | 旅游服务运营商 | 0.6 |
| 中鼎股份 | rubber_seal | manufacture | 橡胶密封件制造商 | 0.9 |
| 中鼎股份 | automotive_part | manufacture | 汽车零部件制造商 | 0.8 |
| 峨眉山A | scenic_area | operate | 旅游景区运营商 | 0.9 |
| 峨眉山A | ropeway | operate | 客运索道运营商 | 0.8 |
| 中嘉博创 | communication_equipment | manufacture | 通信设备制造商 | 0.8 |
| 法尔胜 | steel_wire | produce | 钢丝生产商 | 0.9 |
| 法尔胜 | steel_rope | produce | 钢丝绳生产商 | 0.8 |
| 欢瑞世纪 | film_television | operate | 影视内容供应商 | 0.9 |
| 欢瑞世纪 | cultural_entertainment | operate | 文化娱乐运营商 | 0.7 |
| 亚钾国际 | potassium_chloride | produce | 钾肥生产商 | 0.9 |
| 亚钾国际 | chemical_fertilizer | produce | 化肥生产商 | 0.8 |
| 双汇发展 | meat_product | produce | 肉类产品生产商 | 0.9 |
| 双汇发展 | feed | produce | 饲料生产商 | 0.7 |
| 豫能控股 | coal_power_generation | operate | 火电运营商 | 0.9 |
| 豫能控股 | wind_power_generation | operate | 风电运营商 | 0.7 |
| 津滨发展 | real_estate_development | operate | 房地产开发商 | 0.9 |
| 鞍钢股份 | steel_plate | produce | 钢材综合生产商 | 0.9 |
| 鞍钢股份 | steel_bar | produce | 热轧钢材生产商 | 0.8 |
| 赣能股份 | coal_power_generation | operate | 火电运营商 | 0.8 |
| 赣能股份 | hydro_power_generation | operate | 水电运营商 | 0.8 |
| 赣能股份 | electricity_power | produce | 电力生产商 | 0.8 |
| 现代投资 | highway_operation_service | operate | 高速公路运营商 | 0.9 |
| 航天科技 | communication_equipment | manufacture | 汽车电子/物联网设备制造商 | 0.8 |
| 航天科技 | automotive_electronics | manufacture | 汽车电子制造商 | 0.8 |
| 新洋丰 | compound_fertilizer | produce | 磷复肥生产商 | 0.9 |
| 新洋丰 | chemical_fertilizer | produce | 化肥综合生产商 | 0.8 |
| ST云动 | diesel_engine | manufacture | 柴油发动机制造商 | 0.9 |
| ST云动 | automotive_part | manufacture | 汽车配件制造商 | 0.7 |

---

**Total Graph after Batch 034:**
- Nodes: 594 (589 + 5)
- Edges: 449 (446 + 1)
- Companies: 349 (309 + 20)
