# Batch 062 Construction Log

**Date:** 2026-05-25
**Companies:** 600271.SH – 600283.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `private_network_comm` | 专网通信 | service |
| 2 | `quantum_crypto` | 量子保密通信 | service |
| 3 | `steam_supply` | 蒸汽供应 | service |
| 4 | `fatty_alcohol` | 脂肪醇 | material |
| 5 | `antitumor_drug` | 抗肿瘤药 | material |
| 6 | `department_store` | 百货零售 | service |
| 7 | `platinum_mesh` | 铂网 | component |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `private_network_comm_to_optical_fiber` | private_network_comm → optical_fiber | composition |
| 2 | `steam_supply_to_chemical_industry` | steam_supply → chemical_industry | energy_flow |
| 3 | `antitumor_drug_to_pharmaceutical` | antitumor_drug → pharmaceutical | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `aisino` | 航天信息股份有限公司 | 600271.SH | 北京 | 北京 |
| 2 | `kaikai` | 上海开开实业股份有限公司 | 600272.SH | 上海 | 上海 |
| 3 | `jiahua_energy` | 浙江嘉化能源化工股份有限公司 | 600273.SH | 浙江 | 嘉兴 |
| 4 | `hengrui_pharma` | 江苏恒瑞医药股份有限公司 | 600276.SH | 江苏 | 连云港 |
| 5 | `oricorient` | 东方国际创业股份有限公司 | 600278.SH | 上海 | 上海 |
| 6 | `chongqing_port` | 重庆港股份有限公司 | 600279.SH | 重庆 | 重庆 |
| 7 | `central_mall` | 南京中央商场(集团)股份有限公司 | 600280.SH | 江苏 | 南京 |
| 8 | `huayang_material` | 山西华阳新材料股份有限公司 | 600281.SH | 山西 | 太原 |
| 9 | `nangang_steel` | 南京钢铁股份有限公司 | 600282.SH | 江苏 | 南京 |
| 10 | `qianjiang_water` | 钱江水利开发股份有限公司 | 600283.SH | 浙江 | 杭州 |

## 4. Company Node Exposures (+23)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 航天信息 | private_network_comm | provide_service | 专网通信服务商 | 0.95 |
| 航天信息 | quantum_crypto | provide_service | 量子保密通信服务商 | 0.85 |
| 航天信息 | communication_equipment | manufacture | 通信设备制造商 | 0.8 |
| 开开实业 | garment | produce | 服装生产商 | 0.85 |
| 开开实业 | textile_product | produce | 纺织品生产商 | 0.8 |
| 嘉化能源 | steam_supply | provide_service | 蒸汽供热供应商 | 0.95 |
| 嘉化能源 | chlor_alkali_product | produce | 氯碱化工产品生产商 | 0.9 |
| 嘉化能源 | fatty_alcohol | produce | 脂肪醇生产商 | 0.85 |
| 恒瑞医药 | antitumor_drug | produce | 抗肿瘤药生产商 | 0.95 |
| 恒瑞医药 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 东方创业 | import_export_trade | provide_service | 进出口贸易服务商 | 0.9 |
| 东方创业 | textile_product | procure | 纺织品贸易商 | 0.85 |
| 重庆港 | port_logistics | operate | 港口物流运营商 | 0.95 |
| 重庆港 | logistics_service | provide_service | 综合物流服务商 | 0.85 |
| 中央商场 | department_store | operate | 百货零售运营商 | 0.95 |
| 中央商场 | retail_channel | operate | 零售渠道运营商 | 0.85 |
| 华阳新材 | chlor_alkali_product | produce | 氯碱化工产品生产商 | 0.9 |
| 华阳新材 | pvc | produce | 聚氯乙烯生产商 | 0.85 |
| 华阳新材 | platinum_mesh | manufacture | 铂网制造商 | 0.8 |
| 南钢股份 | steel_plate | produce | 钢铁板材生产商 | 0.95 |
| 南钢股份 | special_steel | produce | 特种钢生产商 | 0.9 |
| 钱江水利 | water_supply | provide_service | 供水服务商 | 0.95 |
| 钱江水利 | hydro_power | operate | 水力发电运营商 | 0.85 |

---

**Graph increment:** Nodes +6, Edges +3
