# Batch 053 Construction Log

**Date:** 2026-05-25
**Companies:** 600155.SH – 600165.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+7)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `securities_service` | 证券服务 | service |
| 2 | `plastic_pipe` | 塑料管材 | component |
| 3 | `ramie_textile` | 苎麻纺织 | material |
| 4 | `fluorochemical` | 氟化工产品 | material |
| 5 | `vaccine` | 疫苗 | material |
| 6 | `blood_product` | 血液制品 | material |
| 7 | `wind_power` | 风力发电 | service |
| 8 | `activated_carbon` | 活性炭 | material |
| 9 | `biomaterial` | 生物基材料 | material |

## 2. New Industrial Edges (+2)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `fluorochemical_to_refrigerant` | fluorochemical → refrigerant | material_flow |
| 2 | `blood_product_to_vaccine` | blood_product → vaccine | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `huachang_yunxin` | 华创云信数字技术股份有限公司 | 600155.SH | 北京 | 北京 |
| 2 | `huasheng` | 湖南华升股份有限公司 | 600156.SH | 湖南 | 长沙 |
| 3 | `yongtai_energy` | 永泰能源集团股份有限公司 | 600157.SH | 山西 | 晋中 |
| 4 | `zhongti` | 中体产业集团股份有限公司 | 600158.SH | 天津 | 天津 |
| 5 | `dalong_realestate` | 北京市大龙伟业房地产开发股份有限公司 | 600159.SH | 北京 | 北京 |
| 6 | `juhua` | 浙江巨化股份有限公司 | 600160.SH | 浙江 | 衢州 |
| 7 | `tiantan_bio` | 北京天坛生物制品股份有限公司 | 600161.SH | 北京 | 北京 |
| 8 | `xiangjiang_holdings` | 深圳香江控股股份有限公司 | 600162.SH | 广东 | 深圳 |
| 9 | `zhongmin_energy` | 中闽能源股份有限公司 | 600163.SH | 福建 | 福州 |
| 10 | `st_ningke` | 宁夏中科生物科技股份有限公司 | 600165.SH | 宁夏 | 石嘴山 |

## 4. Company Node Exposures (+16)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 华创云信 | securities_service | provide_service | 证券服务商 | 0.9 |
| 华创云信 | plastic_pipe | produce | 塑料管材生产商 | 0.8 |
| 华升股份 | ramie_textile | produce | 苎麻纺织品生产商 | 0.9 |
| 华升股份 | textile_product | produce | 纺织品生产商 | 0.85 |
| 永泰能源 | coal | produce | 煤炭生产商 | 0.95 |
| 永泰能源 | power_generation | operate | 火力发电运营商 | 0.9 |
| 中体产业 | sports_service | provide_service | 体育服务运营商 | 0.9 |
| 大龙地产 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 巨化股份 | fluorochemical | produce | 氟化工产品生产商 | 0.95 |
| 巨化股份 | chlor_alkali_product | produce | 氯碱化工产品生产商 | 0.9 |
| 天坛生物 | vaccine | produce | 疫苗生产商 | 0.95 |
| 天坛生物 | blood_product | produce | 血液制品生产商 | 0.95 |
| 香江控股 | real_estate_development | operate | 房地产开发运营商 | 0.9 |
| 中闽能源 | wind_power | operate | 风力发电运营商 | 0.95 |
| ST宁科 | activated_carbon | produce | 活性炭生产商 | 0.85 |
| ST宁科 | biomaterial | produce | 生物基材料生产商 | 0.8 |

---

**Graph increment:** Nodes +7, Edges +2
