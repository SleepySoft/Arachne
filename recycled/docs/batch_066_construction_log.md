# Batch 066 Construction Log

**Date:** 2026-05-25
**Companies:** 600327.SH – 600337.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `salt` | 食盐 | material |
| 2 | `sodium_metal` | 金属钠 | material |
| 3 | `liquid_chlorine` | 液氯 | material |
| 4 | `magnetic_material` | 磁性材料 | material |
| 5 | `zinc_product` | 锌产品 | material |
| 6 | `herbal_tea` | 凉茶 | material |
| 7 | `natural_gas_supply` | 天然气供应 | service |
| 8 | `coke` | 焦炭 | material |
| 9 | `refrigerator` | 冰箱冷柜 | device |
| 10 | `furniture` | 家具 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `salt_to_food` | salt → food | material_flow |
| 2 | `zinc_product_to_galvanized_steel` | zinc_product → steel_plate | material_flow |
| 3 | `natural_gas_supply_to_heating` | natural_gas_supply → heating_supply | energy_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `da_orient` | 无锡商业大厦大东方股份有限公司 | 600327.SH | 江苏 | 无锡 |
| 2 | `cnsalt_chem` | 中盐内蒙古化工股份有限公司 | 600328.SH | 内蒙古 | 阿拉善盟 |
| 3 | `dartong` | 津药达仁堂集团股份有限公司 | 600329.SH | 天津 | 天津 |
| 4 | `tdg` | 天通控股股份有限公司 | 600330.SH | 浙江 | 嘉兴 |
| 5 | `hongda` | 四川宏达股份有限公司 | 600331.SH | 四川 | 德阳 |
| 6 | `baiyunshan` | 广州白云山医药集团股份有限公司 | 600332.SH | 广东 | 广州 |
| 7 | `ccgas` | 长春燃气股份有限公司 | 600333.SH | 吉林 | 长春 |
| 8 | `sinomach_auto` | 国机汽车股份有限公司 | 600335.SH | 天津 | 天津 |
| 9 | `aucma` | 澳柯玛股份有限公司 | 600336.SH | 山东 | 青岛 |
| 10 | `st_markor` | 美克国际家居用品股份有限公司 | 600337.SH | 江西 | 赣州 |

## 4. Company Node Exposures (+24)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 大东方 | department_store | operate | 百货零售运营商 | 0.9 |
| 大东方 | auto_retail | operate | 汽车零售运营商 | 0.85 |
| 大东方 | supermarket | operate | 超市运营商 | 0.8 |
| 中盐化工 | salt | produce | 食盐生产商 | 0.95 |
| 中盐化工 | sodium_metal | produce | 金属钠生产商 | 0.9 |
| 中盐化工 | liquid_chlorine | produce | 液氯生产商 | 0.85 |
| 中盐化工 | chlor_alkali_product | produce | 氯碱化工产品生产商 | 0.8 |
| 达仁堂 | chinese_patent_medicine | produce | 中成药生产商 | 0.95 |
| 天通股份 | magnetic_material | produce | 磁性材料生产商 | 0.95 |
| 天通股份 | communication_equipment | manufacture | 通信设备制造商 | 0.85 |
| 宏达股份 | zinc_product | produce | 锌产品生产商 | 0.95 |
| 宏达股份 | phosphorus_chemical | produce | 磷化工产品生产商 | 0.9 |
| 白云山 | pharmaceutical | produce | 药品生产商 | 0.95 |
| 白云山 | herbal_tea | produce | 凉茶生产商 | 0.85 |
| 白云山 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 长春燃气 | natural_gas_supply | provide_service | 天然气供应商 | 0.95 |
| 长春燃气 | coke | produce | 焦炭生产商 | 0.85 |
| 长春燃气 | heating_supply | provide_service | 供热供应商 | 0.8 |
| 国机汽车 | auto_trade | provide_service | 汽车贸易服务商 | 0.95 |
| 澳柯玛 | refrigerator | manufacture | 冰箱冷柜制造商 | 0.95 |
| 澳柯玛 | air_conditioner | manufacture | 空调器制造商 | 0.85 |
| 澳柯玛 | lithium_battery | manufacture | 锂电池制造商 | 0.8 |
| ST美克 | furniture | produce | 家具生产商 | 0.95 |
| ST美克 | home_decoration | provide_service | 家居装饰服务商 | 0.8 |

---

**Graph increment:** Nodes +6, Edges +3
