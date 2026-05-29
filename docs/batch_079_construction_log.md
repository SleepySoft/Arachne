# Batch 079 Construction Log

**Date:** 2026-05-25
**Companies:** 600513.SH – 600523.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `graphite_electrode` | 石墨电极 | component |
| 2 | `carbon_block` | 炭块 | material |
| 3 | `low_carbon_energy_saving` | 低碳节能 | service |
| 4 | `power_grid_smart_operation` | 电网智能运维 | service |
| 5 | `maotai_liquor` | 茅台酒 | material |
| 6 | `semiconductor_packaging_mold` | 半导体塑封模具 | component |
| 7 | `led_bracket` | LED支架 | component |
| 8 | `aviation_part` | 航空零部件 | component |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `graphite_electrode_to_steel` | graphite_electrode → steel | material_flow |
| 2 | `semiconductor_packaging_mold_to_semiconductor_device` | semiconductor_packaging_mold → semiconductor_device | composition |
| 3 | `aviation_part_to_aircraft` | aviation_part → aircraft | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `lianhuan_pharma` | 江苏联环药业股份有限公司 | 600513.SH | 江苏 | 扬州市 |
| 2 | `hainan_airport` | 海南机场设施股份有限公司 | 600515.SH | 海南 | 海口市 |
| 3 | `fangda_carbon` | 方大炭素新材料科技股份有限公司 | 600516.SH | 甘肃 | 兰州市 |
| 4 | `sgcc_yingda` | 国网英大股份有限公司 | 600517.SH | 上海 | 上海市 |
| 5 | `kangmei` | 康美药业股份有限公司 | 600518.SH | 广东 | 揭阳市 |
| 6 | `maotai` | 贵州茅台酒股份有限公司 | 600519.SH | 贵州 | 遵义市 |
| 7 | `sanjiatech` | 铜陵三佳科技股份有限公司 | 600520.SH | 安徽 | 铜陵市 |
| 8 | `huahai` | 浙江华海药业股份有限公司 | 600521.SH | 浙江 | 台州市 |
| 9 | `zhongtian` | 江苏中天科技股份有限公司 | 600522.SH | 江苏 | 南通市 |
| 10 | `guihang` | 贵州贵航汽车零部件股份有限公司 | 600523.SH | 贵州 | 贵阳市 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 联环药业 | pharmaceutical | produce | 化学药品生产商 | 0.95 |
| 联环药业 | chemical_drug | produce | 化学原料药生产商 | 0.9 |
| 海南机场 | commercial | operate | 商业运营商 | 0.95 |
| 海南机场 | hotel_service | operate | 酒店服务商 | 0.9 |
| 海南机场 | real_estate_development | operate | 房地产开发运营商 | 0.9 |
| 方大炭素 | graphite_electrode | produce | 石墨电极生产商 | 0.95 |
| 方大炭素 | carbon_block | produce | 炭块生产商 | 0.9 |
| 方大炭素 | metallurgical_product | produce | 冶金产品生产商 | 0.85 |
| 国网英大 | low_carbon_energy_saving | provide_service | 低碳节能服务商 | 0.95 |
| 国网英大 | medium_low_voltage_electrical | manufacture | 中低压电气设备制造商 | 0.9 |
| 国网英大 | power_grid_smart_operation | provide_service | 电网智能运维服务商 | 0.95 |
| 康美药业 | chinese_medicine_decoction | produce | 中药饮片生产商 | 0.95 |
| 康美药业 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 贵州茅台 | maotai_liquor | produce | 茅台酒生产商 | 0.95 |
| 贵州茅台 | liquor | produce | 白酒生产商 | 0.95 |
| 三佳科技 | semiconductor_packaging_mold | manufacture | 半导体塑封模具制造商 | 0.95 |
| 三佳科技 | led_bracket | manufacture | LED支架制造商 | 0.9 |
| 华海药业 | pril_product | produce | 普利类产品生产商 | 0.95 |
| 华海药业 | sartan_product | produce | 沙坦类产品生产商 | 0.95 |
| 华海药业 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 中天科技 | telecom_product | manufacture | 电信产品制造商 | 0.95 |
| 中天科技 | power_cable | manufacture | 电力电缆制造商 | 0.9 |
| 中天科技 | new_energy | produce | 新能源产品生产商 | 0.9 |
| 贵航股份 | aviation_part | manufacture | 航空零部件制造商 | 0.95 |
| 贵航股份 | automobile_part | manufacture | 汽车零部件制造商 | 0.9 |
| 贵航股份 | rubber_plastic_product | produce | 橡胶塑料制品生产商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
