# Batch 083 Construction Log

**Date:** 2026-05-25
**Companies:** 600563.SH – 600575.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `film_capacitor` | 薄膜电容器 | component |
| 2 | `corrugated_paperboard` | 箱纸板 | material |
| 3 | `carton` | 纸箱 | material |
| 4 | `medium_thick_plate` | 中厚板 | material |
| 5 | `hot_rolled_coil` | 热轧卷板 | material |
| 6 | `financial_software` | 金融软件 | service |
| 7 | `beer` | 啤酒 | material |
| 8 | `coal_railway_transport` | 煤炭铁路运输 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `film_capacitor_to_electronic_device` | film_capacitor → electronic_device | composition |
| 2 | `corrugated_paperboard_to_carton` | corrugated_paperboard → carton | material_flow |
| 3 | `hot_rolled_coil_to_automobile` | hot_rolled_coil → automobile | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `faratronic` | 厦门法拉电子股份有限公司 | 600563.SH | 福建 | 厦门市 |
| 2 | `jichuan` | 湖北济川药业股份有限公司 | 600566.SH | 湖北 | 黄冈市 |
| 3 | `shan_ying` | 山鹰国际控股股份公司 | 600567.SH | 上海 | 上海市 |
| 4 | `st_zhongzhu` | 中珠医疗控股股份有限公司 | 600568.SH | 湖北 | 潜江市 |
| 5 | `anyang_steel` | 安阳钢铁股份有限公司 | 600569.SH | 河南 | 安阳市 |
| 6 | `hundsun` | 恒生电子股份有限公司 | 600570.SH | 浙江 | 杭州市 |
| 7 | `sunyar` | 信雅达科技股份有限公司 | 600571.SH | 浙江 | 杭州市 |
| 8 | `conba` | 浙江康恩贝制药股份有限公司 | 600572.SH | 浙江 | 杭州市 |
| 9 | `huiquan` | 福建省燕京惠泉啤酒股份有限公司 | 600573.SH | 福建 | 泉州市 |
| 10 | `huaihe_energy` | 淮河能源(集团)股份有限公司 | 600575.SH | 安徽 | 淮南市 |

## 4. Company Node Exposures (+28)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 法拉电子 | film_capacitor | manufacture | 薄膜电容器制造商 | 0.95 |
| 法拉电子 | metallized_film | produce | 金属化膜生产商 | 0.9 |
| 济川药业 | pharmaceutical | produce | 药品生产商 | 0.95 |
| 济川药业 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 山鹰国际 | corrugated_paperboard | produce | 箱纸板生产商 | 0.95 |
| 山鹰国际 | carton | produce | 纸箱生产商 | 0.95 |
| 山鹰国际 | paper | produce | 造纸商 | 0.9 |
| ST中珠 | medical_service | provide_service | 医疗服务商 | 0.95 |
| ST中珠 | pharmaceutical | produce | 药品生产商 | 0.9 |
| ST中珠 | real_estate_development | operate | 房地产开发运营商 | 0.85 |
| 安阳钢铁 | medium_thick_plate | produce | 中厚板生产商 | 0.95 |
| 安阳钢铁 | hot_rolled_coil | produce | 热轧卷板生产商 | 0.95 |
| 安阳钢铁 | high_speed_wire_rod | produce | 高速线材生产商 | 0.9 |
| 安阳钢铁 | steel | produce | 钢材生产商 | 0.95 |
| 恒生电子 | financial_software | provide_service | 金融软件服务商 | 0.95 |
| 恒生电子 | system_integration | provide_service | 系统集成服务商 | 0.9 |
| 恒生电子 | software | provide_service | 软件服务商 | 0.9 |
| 信雅达 | electronic_image_processing | provide_service | 电子影像处理系统服务商 | 0.95 |
| 信雅达 | customer_service_system | provide_service | 客户服务中心系统服务商 | 0.9 |
| 信雅达 | software | provide_service | 软件服务商 | 0.85 |
| 康恩贝 | modern_botanical_medicine | produce | 现代植物药生产商 | 0.95 |
| 康恩贝 | chemical_drug | produce | 化学药生产商 | 0.9 |
| 康恩贝 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 惠泉啤酒 | beer | produce | 啤酒生产商 | 0.95 |
| 惠泉啤酒 | beverage | produce | 饮料生产商 | 0.85 |
| 淮河能源 | coal | operate | 煤炭经营商 | 0.95 |
| 淮河能源 | coal_railway_transport | operate | 煤炭铁路运输运营商 | 0.9 |
| 淮河能源 | bulk_cargo_handling | operate | 大宗散货装卸运营商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
