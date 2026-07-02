# Batch 035 Construction Log

**Date:** 2026-05-25
**Companies:** 000893.SZ – 000903.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+4)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `potassium_ore` | 钾盐矿石 | material |
| 2 | `phosphate_ore` | 磷矿石 | material |
| 3 | `aerospace_application_product` | 航天应用产品 | device |
| 4 | `connected_vehicle_device` | 车联网设备 | device |

## 2. New Industrial Edges (+7)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_potassium_ore_to_chloride` | potassium_ore → potassium_chloride | material_flow |
| 2 | `flow_phosphate_ore_to_compound_fertilizer` | phosphate_ore → compound_fertilizer | material_flow |
| 3 | `flow_iron_ore_to_steel_plate` | iron_ore → steel_plate | material_flow |
| 4 | `flow_iron_ore_to_steel_bar` | iron_ore → steel_bar | material_flow |
| 5 | `compound_fertilizer_is_a_chemical_fertilizer` | compound_fertilizer → chemical_fertilizer | is_a |
| 6 | `aerospace_product_to_satellite_comm` | aerospace_application_product → satellite_communication | composition |
| 7 | `connected_vehicle_to_automotive_electronics` | connected_vehicle_device → automotive_electronics | composition |

## 3. Companies Registered / Verified (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `asia_potash` | 亚钾国际投资(广州)股份有限公司 | 000893.SZ | 广东 | 广州 | 5,808 |
| 2 | `shuanghui_dev` | 河南双汇投资发展股份有限公司 | 000895.SZ | 河南 | 漯河 | 46,352 |
| 3 | `yuneng_holdings` | 河南豫能控股股份有限公司 | 001896.SZ | 河南 | 郑州 | 3,457 |
| 4 | `tianjin_jinbin` | 天津津滨发展股份有限公司 | 000897.SZ | 天津 | 天津 | 297 |
| 5 | `angang_steel` | 鞍钢股份有限公司 | 000898.SZ | 辽宁 | 鞍山 | 23,990 |
| 6 | `ganeng_power` | 江西赣能股份有限公司 | 000899.SZ | 江西 | 南昌 | 1,022 |
| 7 | `modern_investment` | 现代投资股份有限公司 | 000900.SZ | 湖南 | 长沙 | 2,767 |
| 8 | `aerospace_tech` | 航天科技控股集团股份有限公司 | 000901.SZ | 黑龙江 | 哈尔滨 | 6,043 |
| 9 | `xinyangfeng` | 新洋丰农业科技股份有限公司 | 000902.SZ | 湖北 | 荆门 | 8,315 |
| 10 | `st_yundong` | 昆明云内动力股份有限公司 | 000903.SZ | 云南 | 昆明 | 2,594 |

## 4. Company Node Exposures (+20)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 亚钾国际 | potassium_chloride | produce | 氯化钾生产商 | 0.9 |
| 亚钾国际 | chemical_fertilizer | produce | 化肥生产商 | 0.8 |
| 双汇发展 | meat_product | produce | 肉类产品生产商 | 0.95 |
| 豫能控股 | coal_power_generation | operate | 火电运营商 | 0.9 |
| 豫能控股 | hydro_power_generation | operate | 水电运营商 | 0.7 |
| 津滨发展 | real_estate_development | operate | 房地产开发商 | 0.9 |
| 鞍钢股份 | steel_plate | produce | 钢板生产商 | 0.9 |
| 鞍钢股份 | steel_bar | produce | 棒材/钢筋生产商 | 0.8 |
| 鞍钢股份 | special_steel | produce | 特钢生产商 | 0.7 |
| 赣能股份 | coal_power_generation | operate | 火电运营商 | 0.8 |
| 赣能股份 | hydro_power_generation | operate | 水电运营商 | 0.8 |
| 赣能股份 | electricity_power | produce | 电力生产商 | 0.9 |
| 现代投资 | highway_operation_service | operate | 高速公路运营商 | 0.95 |
| 航天科技 | automotive_electronics | manufacture | 汽车电子制造商 | 0.85 |
| 航天科技 | aerospace_application_product | manufacture | 航天应用产品制造商 | 0.8 |
| 航天科技 | connected_vehicle_device | manufacture | 车联网设备制造商 | 0.75 |
| 新洋丰 | compound_fertilizer | produce | 复合肥生产商 | 0.95 |
| 新洋丰 | chemical_fertilizer | produce | 化肥生产商 | 0.85 |
| ST云动 | diesel_engine | manufacture | 柴油发动机制造商 | 0.9 |
| ST云动 | automotive_part | manufacture | 汽车配件制造商 | 0.7 |

---

**Total Graph after Batch 035:**
- Nodes: 603 (599 + 4)
- Edges: 461 (454 + 7)
- Companies: 10 verified/upserted
