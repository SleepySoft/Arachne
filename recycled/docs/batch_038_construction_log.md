# Batch 038 Construction Log

**Date:** 2026-05-25
**Companies:** 000930.SZ – 000949.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `starch` | 淀粉 | material |
| 2 | `fuel_ethanol` | 燃料乙醇 | material |
| 3 | `monosodium_glutamate` | 味精 | material |
| 4 | `citric_acid` | 柠檬酸 | material |
| 5 | `alumina` | 氧化铝 | material |
| 6 | `aluminum_product` | 铝产品 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `starch_to_fuel_ethanol` | starch → fuel_ethanol | material_flow |
| 2 | `alumina_to_aluminum_product` | alumina → aluminum_product | material_flow |
| 3 | `coal_to_alumina` | coal → alumina | energy_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `cofco_tech` | 中粮生物科技股份有限公司 | 000930.SZ | 安徽 | 蚌埠 |
| 2 | `zhongguancun` | 北京中关村科技发展(控股)股份有限公司 | 000931.SZ | 北京 | 北京 |
| 3 | `valin_steel` | 湖南华菱钢铁股份有限公司 | 000932.SZ | 湖南 | 长沙 |
| 4 | `shenhuo` | 河南神火煤电股份有限公司 | 000933.SZ | 河南 | 商丘 |
| 5 | `sichuan_shuangma` | 四川双马水泥股份有限公司 | 000935.SZ | 四川 | 成都 |
| 6 | `huaxi_share` | 江苏华西村股份有限公司 | 000936.SZ | 江苏 | 江阴 |
| 7 | `jizhong_energy` | 冀中能源股份有限公司 | 000937.SZ | 河北 | 邢台 |
| 8 | `unisplendour` | 紫光股份有限公司 | 000938.SZ | 北京 | 北京 |
| 9 | `nantian_info` | 云南南天电子信息产业股份有限公司 | 000948.SZ | 云南 | 昆明 |
| 10 | `xinxiang_chemical` | 新乡化纤股份有限公司 | 000949.SZ | 河南 | 新乡 |

## 4. Company Node Exposures (+16)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 中粮科技 | starch | produce | 淀粉生产商 | 0.9 |
| 中粮科技 | fuel_ethanol | produce | 燃料乙醇生产商 | 0.85 |
| 中粮科技 | monosodium_glutamate | produce | 味精生产商 | 0.8 |
| 中粮科技 | citric_acid | produce | 柠檬酸生产商 | 0.8 |
| 中关村 | chemical_drug | produce | 生物医药企业 | 0.7 |
| 华菱钢铁 | steel_plate | produce | 钢板生产商 | 0.9 |
| 神火股份 | coal | produce | 煤炭生产商 | 0.85 |
| 神火股份 | alumina | produce | 氧化铝生产商 | 0.85 |
| 神火股份 | aluminum_product | produce | 铝产品生产商 | 0.85 |
| 四川双马 | cement | produce | 水泥生产商 | 0.9 |
| 华西股份 | viscose_fiber | produce | 粘胶纤维生产商 | 0.85 |
| 冀中能源 | coal | produce | 煤炭生产商 | 0.9 |
| 紫光股份 | it_equipment | manufacture | IT设备与通讯产品供应商 | 0.85 |
| 南天信息 | software_service | provide_service | 金融信息化软件服务商 | 0.9 |
| 新乡化纤 | viscose_filament | produce | 粘胶长丝生产商 | 0.9 |
| 新乡化纤 | viscose_staple | produce | 粘胶短纤维生产商 | 0.85 |

---

**Graph increment:** Nodes +6, Edges +3
