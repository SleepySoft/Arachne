# Batch 068 Construction Log

**Date:** 2026-05-25
**Companies:** 600353.SH – 600365.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+5)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `vacuum_electronic_device` | 真空电子器件 | component |
| 2 | `cigarette_paper` | 卷烟纸 | material |
| 3 | `tourism_investment` | 旅游投资 | service |
| 4 | `power_semiconductor` | 功率半导体 | component |
| 5 | `aluminum_alloy` | 铝合金 | material |
| 6 | `copper_smelting` | 铜冶炼 | service |
| 7 | `precious_metal` | 贵金属 | material |
| 8 | `wine` | 葡萄酒 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `vacuum_electronic_device_to_switchgear` | vacuum_electronic_device → switchgear | composition |
| 2 | `copper_smelting_to_electronic_component` | copper_smelting → electronic_component | material_flow |
| 3 | `aluminum_alloy_to_automobile` | aluminum_alloy → automobile | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `xuguang_elec` | 成都旭光电子股份有限公司 | 600353.SH | 四川 | 成都 |
| 2 | `dunhuang_seed` | 甘肃省敦煌种业集团股份有限公司 | 600354.SH | 甘肃 | 酒泉 |
| 3 | `hengfeng_paper` | 牡丹江恒丰纸业股份有限公司 | 600356.SH | 黑龙江 | 牡丹江 |
| 4 | `cits_union` | 国旅文化投资集团股份有限公司 | 600358.SH | 江西 | 南昌 |
| 5 | `xinong` | 新疆塔里木农业综合开发股份有限公司 | 600359.SH | 新疆 | 阿拉尔 |
| 6 | `huaweimicro` | 吉林华微电子股份有限公司 | 600360.SH | 吉林 | 吉林 |
| 7 | `innovation_material` | 创新新材料科技股份有限公司 | 600361.SH | 北京 | 北京 |
| 8 | `jiangxi_copper` | 江西铜业股份有限公司 | 600362.SH | 江西 | 鹰潭 |
| 9 | `lianchuang_opt` | 江西联创光电科技股份有限公司 | 600363.SH | 江西 | 南昌 |
| 10 | `st_tongpu` | 通化葡萄酒股份有限公司 | 600365.SH | 吉林 | 通化 |

## 4. Company Node Exposures (+22)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 旭光电子 | vacuum_electronic_device | manufacture | 真空电子器件制造商 | 0.95 |
| 旭光电子 | switchgear | manufacture | 开关设备制造商 | 0.9 |
| 旭光电子 | high_voltage_switchgear | manufacture | 高压开关设备制造商 | 0.85 |
| 敦煌种业 | seed | produce | 种子生产商 | 0.95 |
| 敦煌种业 | agricultural_product | produce | 农产品生产商 | 0.85 |
| 恒丰纸业 | cigarette_paper | produce | 卷烟纸生产商 | 0.95 |
| 恒丰纸业 | specialty_paper | produce | 特种纸生产商 | 0.9 |
| 国旅联合 | tourism_investment | provide_service | 旅游投资服务商 | 0.85 |
| 国旅联合 | tourism_service | provide_service | 旅游服务商 | 0.8 |
| 新农开发 | cotton | produce | 棉花生产商 | 0.95 |
| 新农开发 | cotton_product | produce | 棉制品生产商 | 0.85 |
| 华微电子 | power_semiconductor | manufacture | 功率半导体制造商 | 0.95 |
| 华微电子 | semiconductor_device | manufacture | 半导体器件制造商 | 0.9 |
| 创新新材 | aluminum_alloy | produce | 铝合金生产商 | 0.95 |
| 创新新材 | aluminum_product | produce | 铝加工产品生产商 | 0.9 |
| 江西铜业 | copper_smelting | operate | 铜冶炼运营商 | 0.95 |
| 江西铜业 | precious_metal | produce | 贵金属生产商 | 0.85 |
| 江西铜业 | nonferrous_metal_mining | operate | 有色金属采选运营商 | 0.9 |
| 联创光电 | led_display | manufacture | LED显示器件制造商 | 0.9 |
| 联创光电 | optoelectronic_device | manufacture | 光电子器件制造商 | 0.9 |
| ST通葡 | wine | produce | 葡萄酒生产商 | 0.95 |
| ST通葡 | liquor | produce | 酒类生产商 | 0.85 |

---

**Graph increment:** Nodes +5, Edges +3
