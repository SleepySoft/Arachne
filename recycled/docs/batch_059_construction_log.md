# Batch 059 Construction Log

**Date:** 2026-05-25
**Companies:** 600230.SH – 600239.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `tdi` | 甲苯二异氰酸酯 | material |
| 2 | `textile_machinery` | 纺织机械 | device |
| 3 | `flax_textile` | 亚麻纺织 | material |
| 4 | `express_delivery` | 快递服务 | service |
| 5 | `specialty_paper` | 特种纸 | material |
| 6 | `hydro_power` | 水力发电 | service |
| 7 | `film_capacitor` | 薄膜电容器 | component |
| 8 | `liquor` | 酒类 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `tdi_to_polyurethane` | tdi → polyurethane | material_flow |
| 2 | `textile_machinery_to_textile_product` | textile_machinery → textile_product | capability_supply |
| 3 | `hydro_power_to_power_grid` | hydro_power → power_grid | energy_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `czdahua` | 沧州大化股份有限公司 | 600230.SH | 河北 | 沧州 |
| 2 | `lingang` | 凌源钢铁股份有限公司 | 600231.SH | 辽宁 | 朝阳 |
| 3 | `jinying` | 浙江金鹰股份有限公司 | 600232.SH | 浙江 | 舟山 |
| 4 | `yto_express` | 圆通速递股份有限公司 | 600233.SH | 辽宁 | 大连 |
| 5 | `kexin` | 山西科新发展股份有限公司 | 600234.SH | 山西 | 太原 |
| 6 | `minfeng_paper` | 民丰特种纸股份有限公司 | 600235.SH | 浙江 | 嘉兴 |
| 7 | `guiguan_power` | 广西桂冠电力股份有限公司 | 600236.SH | 广西 | 南宁 |
| 8 | `tongfeng_elec` | 安徽铜峰电子股份有限公司 | 600237.SH | 安徽 | 铜陵 |
| 9 | `st_yedao` | 海南椰岛(集团)股份有限公司 | 600238.SH | 海南 | 海口 |
| 10 | `st_yuncheng` | 云南城投置业股份有限公司 | 600239.SH | 云南 | 昆明 |

## 4. Company Node Exposures (+18)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 沧州大化 | tdi | produce | TDI生产商 | 0.95 |
| 沧州大化 | urea | produce | 尿素生产商 | 0.9 |
| 凌钢股份 | steel_plate | produce | 钢铁板材生产商 | 0.95 |
| 凌钢股份 | special_steel | produce | 特种钢生产商 | 0.85 |
| 金鹰股份 | textile_machinery | manufacture | 纺织机械制造商 | 0.9 |
| 金鹰股份 | flax_textile | produce | 亚麻纺织品生产商 | 0.85 |
| 金鹰股份 | textile_product | produce | 纺织品生产商 | 0.8 |
| 圆通速递 | express_delivery | provide_service | 快递服务提供商 | 0.95 |
| 圆通速递 | logistics_service | provide_service | 综合物流服务商 | 0.9 |
| 科新发展 | wine | procure | 红酒贸易商 | 0.8 |
| 民丰特纸 | specialty_paper | produce | 特种纸生产商 | 0.95 |
| 桂冠电力 | hydro_power | operate | 水力发电运营商 | 0.95 |
| 桂冠电力 | power_generation | operate | 电力运营商 | 0.9 |
| 铜峰电子 | film_capacitor | manufacture | 薄膜电容器制造商 | 0.95 |
| 铜峰电子 | electronic_component | manufacture | 电子元器件制造商 | 0.85 |
| *ST椰岛 | liquor | produce | 酒类生产商 | 0.9 |
| *ST椰岛 | real_estate_development | operate | 房地产开发运营商 | 0.75 |
| ST云城 | real_estate_development | operate | 房地产开发运营商 | 0.95 |

---

**Graph increment:** Nodes +6, Edges +3
