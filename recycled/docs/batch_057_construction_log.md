# Batch 057 Construction Log

**Date:** 2026-05-25
**Companies:** 600202.SH – 600216.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+10)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `air_cooling_equipment` | 空冷设备 | device |
| 2 | `led_display` | LED显示器件 | component |
| 3 | `semiconductor_material` | 半导体材料 | material |
| 4 | `rare_earth_functional` | 稀土功能材料 | material |
| 5 | `pv_glass` | 光伏玻璃 | material |
| 6 | `natural_gas_supply` | 天然气供应 | service |
| 7 | `packaging_material` | 包装材料 | material |
| 8 | `tibetan_medicine` | 藏药 | material |
| 9 | `charging_pile` | 充电桩 | device |
| 10 | `industrial_automation` | 工业自动化 | service |
| 11 | `vitamin_e` | 维生素E | material |
| 12 | `chemical_pharmaceutical` | 化学制药 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `semiconductor_material_to_chip` | semiconductor_material → integrated_circuit | material_flow |
| 2 | `pv_glass_to_solar_panel` | pv_glass → solar_panel | composition |
| 3 | `charging_pile_to_new_energy_vehicle` | charging_pile → new_energy_vehicle | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `harbin_aircon` | 哈尔滨空调股份有限公司 | 600202.SH | 黑龙江 | 哈尔滨 |
| 2 | `furi_elec` | 福建福日电子股份有限公司 | 600203.SH | 福建 | 福州 |
| 3 | `grimn_advanced` | 有研新材料股份有限公司 | 600206.SH | 北京 | 北京 |
| 4 | `ancai_hitech` | 河南安彩高科股份有限公司 | 600207.SH | 河南 | 安阳 |
| 5 | `quzhou_dev` | 衢州信安发展股份有限公司 | 600208.SH | 浙江 | 衢州 |
| 6 | `zijiang` | 上海紫江企业集团股份有限公司 | 600210.SH | 上海 | 上海 |
| 7 | `tibet_rhodiola` | 西藏诺迪康药业股份有限公司 | 600211.SH | 西藏 | 拉萨 |
| 8 | `lvenergy` | 绿能慧充数字能源技术股份有限公司 | 600212.SH | 山东 | 临沂 |
| 9 | `paslin` | 派斯林数字科技股份有限公司 | 600215.SH | 吉林 | 长春 |
| 10 | `zhejiang_pharma` | 浙江医药股份有限公司 | 600216.SH | 浙江 | 绍兴 |

## 4. Company Node Exposures (+19)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 哈空调 | air_cooling_equipment | manufacture | 空冷设备制造商 | 0.95 |
| 哈空调 | air_conditioner | manufacture | 空调设备制造商 | 0.85 |
| 福日电子 | led_display | manufacture | LED显示器件制造商 | 0.9 |
| 福日电子 | display_device | manufacture | 显示器件制造商 | 0.85 |
| 有研新材 | semiconductor_material | produce | 半导体材料生产商 | 0.95 |
| 有研新材 | rare_earth_functional | produce | 稀土功能材料生产商 | 0.9 |
| 安彩高科 | pv_glass | produce | 光伏玻璃生产商 | 0.9 |
| 安彩高科 | natural_gas_supply | provide_service | 天然气供应商 | 0.85 |
| 衢州发展 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 紫江企业 | packaging_material | produce | 包装材料生产商 | 0.95 |
| 紫江企业 | pet_bottle | produce | PET瓶生产商 | 0.9 |
| 西藏药业 | tibetan_medicine | produce | 藏药生产商 | 0.95 |
| 西藏药业 | chinese_patent_medicine | produce | 中成药生产商 | 0.85 |
| 绿能慧充 | charging_pile | manufacture | 充电桩制造商 | 0.9 |
| 绿能慧充 | energy_storage | provide_service | 储能技术服务商 | 0.85 |
| 派斯林 | industrial_automation | provide_service | 工业自动化服务商 | 0.9 |
| 派斯林 | industrial_robot | manufacture | 工业机器人制造商 | 0.85 |
| 浙江医药 | chemical_pharmaceutical | produce | 化学制药生产商 | 0.95 |
| 浙江医药 | vitamin_e | produce | 维生素E生产商 | 0.9 |

---

**Graph increment:** Nodes +10, Edges +3
