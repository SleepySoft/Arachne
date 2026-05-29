# Batch 060 Construction Log

**Date:** 2026-05-25
**Companies:** 600241.SH – 600256.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `new_energy_battery` | 新能源电池 | component |
| 2 | `machine_tool` | 机床设备 | device |
| 3 | `elevator_parts` | 电梯配件 | component |
| 4 | `toothpaste` | 牙膏 | material |
| 5 | `daily_chemical` | 日用化工 | material |
| 6 | `commerce_tourism` | 商贸旅游 | service |
| 7 | `cotton_product` | 棉花及棉制品 | material |
| 8 | `fruit_vegetable_product` | 果蔬制品 | material |
| 9 | `copper_alloy` | 铜合金材料 | material |
| 10 | `lng` | 液化天然气 | material |
| 11 | `petroleum_exploration` | 石油勘探开采 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `new_energy_battery_to_electric_vehicle` | new_energy_battery → new_energy_vehicle | composition |
| 2 | `copper_alloy_to_electronic_component` | copper_alloy → electronic_component | material_flow |
| 3 | `lng_to_natural_gas_supply` | lng → natural_gas_supply | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `sdwh` | 辽宁时代万恒股份有限公司 | 600241.SH | 辽宁 | 大连 |
| 2 | `st_haihua` | 青海华鼎实业股份有限公司 | 600243.SH | 青海 | 西宁 |
| 3 | `vantone` | 北京万通新发展集团股份有限公司 | 600246.SH | 北京 | 北京 |
| 4 | `shaanxi_const` | 陕西建工集团股份有限公司 | 600248.SH | 陕西 | 西安 |
| 5 | `lmz` | 柳州两面针股份有限公司 | 600249.SH | 广西 | 柳州 |
| 6 | `nj_commerce` | 南京商贸旅游股份有限公司 | 600250.SH | 江苏 | 南京 |
| 7 | `guannong` | 新疆冠农股份有限公司 | 600251.SH | 新疆 | 铁门关 |
| 8 | `zhongheng` | 广西梧州中恒集团股份有限公司 | 600252.SH | 广西 | 梧州 |
| 9 | `xinke_material` | 安徽鑫科新材料股份有限公司 | 600255.SH | 安徽 | 芜湖 |
| 10 | `guanghui_energy` | 广汇能源股份有限公司 | 600256.SH | 新疆 | 乌鲁木齐 |

## 4. Company Node Exposures (+25)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 时代万恒 | new_energy_battery | manufacture | 新能源电池制造商 | 0.95 |
| 时代万恒 | timber | produce | 木材生产商 | 0.8 |
| *ST海华 | machine_tool | manufacture | 机床设备制造商 | 0.9 |
| *ST海华 | elevator_parts | manufacture | 电梯配件制造商 | 0.85 |
| *ST海华 | gearbox | manufacture | 齿轮箱制造商 | 0.8 |
| 万通发展 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 陕建股份 | construction_engineering | provide_service | 建筑工程承包商 | 0.95 |
| 陕建股份 | petrochemical_installation | provide_service | 石油化工安装承包商 | 0.9 |
| 两面针 | toothpaste | produce | 牙膏生产商 | 0.95 |
| 两面针 | daily_chemical | produce | 日用化工产品生产商 | 0.9 |
| 南京商旅 | commerce_tourism | provide_service | 商贸旅游服务商 | 0.85 |
| 南京商旅 | textile_product | procure | 纺织品贸易商 | 0.8 |
| 冠农股份 | fruit_vegetable_product | produce | 果蔬制品生产商 | 0.9 |
| 冠农股份 | cotton_product | produce | 棉花及棉制品生产商 | 0.9 |
| 冠农股份 | sugar | produce | 食糖生产商 | 0.85 |
| 冠农股份 | tomato_product | produce | 番茄制品生产商 | 0.85 |
| 中恒集团 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 中恒集团 | chinese_patent_medicine | produce | 中成药生产商 | 0.85 |
| 中恒集团 | real_estate_development | operate | 房地产开发运营商 | 0.8 |
| 鑫科材料 | copper_alloy | produce | 铜合金材料生产商 | 0.95 |
| 鑫科材料 | special_cable | produce | 特种电缆生产商 | 0.85 |
| 广汇能源 | lng | produce | 液化天然气生产商 | 0.95 |
| 广汇能源 | coal | produce | 煤炭生产商 | 0.95 |
| 广汇能源 | petroleum_exploration | operate | 石油勘探开采运营商 | 0.9 |
| 广汇能源 | natural_gas_supply | provide_service | 天然气供应商 | 0.85 |

---

**Graph increment:** Nodes +9, Edges +3
