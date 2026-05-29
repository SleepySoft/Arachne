# Batch 063 Construction Log

**Date:** 2026-05-25
**Companies:** 600284.SH – 600299.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `municipal_engineering` | 市政工程 | service |
| 2 | `asphalt` | 沥青 | material |
| 3 | `chinese_medicine_plaster` | 中药膏剂 | material |
| 4 | `optomechatronics` | 光机电一体化 | service |
| 5 | `information_security` | 信息安全 | service |
| 6 | `float_glass` | 浮法玻璃 | material |
| 7 | `cashmere_product` | 羊绒制品 | material |
| 8 | `yeast` | 酵母 | material |
| 9 | `nutritional_additive` | 营养添加剂 | material |
| 10 | `silicone` | 有机硅 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `asphalt_to_road` | asphalt → road | composition |
| 2 | `yeast_to_food` | yeast → food | material_flow |
| 3 | `silicone_to_electronic_material` | silicone → electronic_material | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `pudong_construction` | 上海浦东建设股份有限公司 | 600284.SH | 上海 | 上海 |
| 2 | `lingrui_pharma` | 河南羚锐制药股份有限公司 | 600285.SH | 河南 | 信阳 |
| 3 | `suhao_fashion` | 江苏苏豪时尚集团股份有限公司 | 600287.SH | 江苏 | 南京 |
| 4 | `daheng_tech` | 大恒新纪元科技股份有限公司 | 600288.SH | 北京 | 北京 |
| 5 | `st_eastcom` | 亿阳信通股份有限公司 | 600289.SH | 黑龙江 | 哈尔滨 |
| 6 | `spic_hydro` | 国家电投集团水电股份有限公司 | 600292.SH | 重庆 | 重庆 |
| 7 | `sanxia_newmat` | 湖北三峡新型建材股份有限公司 | 600293.SH | 湖北 | 宜昌 |
| 8 | `erdos` | 内蒙古鄂尔多斯资源股份有限公司 | 600295.SH | 内蒙古 | 鄂尔多斯 |
| 9 | `angelyeast` | 安琪酵母股份有限公司 | 600298.SH | 湖北 | 宜昌 |
| 10 | `adisseo` | 蓝星安迪苏股份有限公司 | 600299.SH | 北京 | 北京 |

## 4. Company Node Exposures (+23)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 浦东建 | municipal_engineering | provide_service | 市政工程承包商 | 0.95 |
| 浦东建 | asphalt | produce | 沥青生产商 | 0.85 |
| 浦东建 | construction_engineering | provide_service | 建筑工程承包商 | 0.9 |
| 羚锐制药 | chinese_medicine_plaster | produce | 中药膏剂生产商 | 0.95 |
| 羚锐制药 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 苏豪时尚 | commodity_circulation | provide_service | 商品流通服务商 | 0.85 |
| 苏豪时尚 | garment | produce | 服装生产商 | 0.8 |
| 大恒科技 | optomechatronics | provide_service | 光机电一体化服务商 | 0.85 |
| 大恒科技 | optoelectronic_device | manufacture | 光电子器件制造商 | 0.8 |
| ST信通 | information_security | provide_service | 信息安全服务商 | 0.9 |
| ST信通 | communication_network_support | provide_service | 通信网络支撑服务商 | 0.85 |
| 电投水电 | power_generation | operate | 发电业务运营商 | 0.95 |
| 电投水电 | environmental_service | provide_service | 环保服务提供商 | 0.85 |
| 三峡新材 | float_glass | produce | 浮法玻璃生产商 | 0.95 |
| 三峡新材 | glass | produce | 玻璃生产商 | 0.85 |
| 鄂尔多斯 | cashmere_product | produce | 羊绒制品生产商 | 0.95 |
| 鄂尔多斯 | textile_product | produce | 纺织品生产商 | 0.85 |
| 鄂尔多斯 | power_generation | operate | 电力运营商 | 0.8 |
| 安琪酵母 | yeast | produce | 酵母生产商 | 0.95 |
| 安琪酵母 | food_additive | produce | 食品添加剂生产商 | 0.9 |
| 安迪苏 | nutritional_additive | produce | 营养添加剂生产商 | 0.9 |
| 安迪苏 | silicone | produce | 有机硅生产商 | 0.85 |
| 安迪苏 | chemical_product | produce | 化工产品生产商 | 0.8 |

---

**Graph increment:** Nodes +9, Edges +3
