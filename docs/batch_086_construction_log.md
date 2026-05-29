# Batch 086 Construction Log

**Date:** 2026-05-25
**Companies:** 600597.SH – 600606.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `rice` | 大米 | material |
| 2 | `fireworks` | 烟花 | material |
| 3 | `pcb_product` | PCB产品 | component |
| 4 | `consumer_electronics` | 消费电子 | device |
| 5 | `intelligent_security` | 智能安防 | system |
| 6 | `logistics_park` | 物流园区 | infrastructure |
| 7 | `wind_power` | 风力发电 | service |
| 8 | `copper_trade` | 铜贸易 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `rice_to_food` | rice → food | material_flow |
| 2 | `pcb_product_to_electronic_device` | pcb_product → electronic_device | composition |
| 3 | `wind_power_to_power_generation` | wind_power → power_generation | service_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `bright_dairy` | 光明乳业股份有限公司 | 600597.SH | 上海 | 上海市 |
| 2 | `beidahuang` | 黑龙江北大荒农业股份有限公司 | 600598.SH | 黑龙江 | 哈尔滨市 |
| 3 | `st_panda` | 熊猫金控股份有限公司 | 600599.SH | 湖南 | 长沙市 |
| 4 | `tsingtao` | 青岛啤酒股份有限公司 | 600600.SH | 山东 | 青岛市 |
| 5 | `founder_tech` | 方正科技集团股份有限公司 | 600601.SH | 广东 | 珠海市 |
| 6 | `cloud_intelligence` | 云赛智联股份有限公司 | 600602.SH | 上海 | 上海市 |
| 7 | `guanghui_logistics` | 广汇物流股份有限公司 | 600603.SH | 新疆 | 乌鲁木齐市 |
| 8 | `shibei` | 上海市北高新股份有限公司 | 600604.SH | 上海 | 上海市 |
| 9 | `huitong` | 上海汇通能源股份有限公司 | 600605.SH | 上海 | 上海市 |
| 10 | `greenland` | 绿地控股集团股份有限公司 | 600606.SH | 上海 | 上海市 |

## 4. Company Node Exposures (+24)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 光明乳业 | dairy_product | produce | 乳制品生产商 | 0.95 |
| 光明乳业 | food | produce | 食品生产商 | 0.9 |
| 北大荒 | rice | produce | 大米生产商 | 0.95 |
| 北大荒 | agricultural_product | produce | 农产品生产商 | 0.9 |
| *ST熊猫 | fireworks | produce | 烟花生产商 | 0.95 |
| *ST熊猫 | entertainment | operate | 烟花燃放运营商 | 0.9 |
| 青岛啤酒 | beer | produce | 啤酒生产商 | 0.95 |
| 青岛啤酒 | beverage | produce | 饮料生产商 | 0.9 |
| 方正科技 | pcb_product | manufacture | PCB产品制造商 | 0.95 |
| 方正科技 | computer | manufacture | 计算机制造商 | 0.9 |
| 方正科技 | system_integration | provide_service | 系统集成服务商 | 0.9 |
| 云赛智联 | consumer_electronics | produce | 消费电子生产商 | 0.95 |
| 云赛智联 | intelligent_security | provide_service | 智能安防服务商 | 0.95 |
| 云赛智联 | software | provide_service | 软件服务商 | 0.9 |
| 广汇物流 | logistics_park | operate | 物流园区运营商 | 0.95 |
| 广汇物流 | logistics | provide_service | 物流服务商 | 0.9 |
| 市北高新 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 市北高新 | investment_management | operate | 投资管理运营商 | 0.85 |
| 汇通能源 | wind_power | operate | 风力发电运营商 | 0.95 |
| 汇通能源 | power_generation | operate | 发电运营商 | 0.9 |
| 汇通能源 | copper_trade | operate | 铜贸易商 | 0.85 |
| 绿地控股 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 绿地控股 | residential_circulation | operate | 住宅流通运营商 | 0.9 |
| 绿地控股 | property_management | provide_service | 物业管理服务商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
