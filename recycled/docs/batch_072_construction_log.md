# Batch 072 Construction Log

**Date:** 2026-05-25
**Companies:** 600405.SH – 600420.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `telecom_power_supply` | 通信电源 | device |
| 2 | `photovoltaic_inverter` | 光伏逆变器 | device |
| 3 | `power_grid_automation` | 电网自动化 | service |
| 4 | `rail_transit_electrical` | 轨道交通电气 | service |
| 5 | `ac_motor` | 交流电机 | component |
| 6 | `dc_motor` | 直流电机 | component |
| 7 | `commercial_vehicle` | 商用车 | system |
| 8 | `dairy_product` | 乳制品 | material |
| 9 | `antibiotic` | 抗生素 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `telecom_power_supply_to_communication_equipment` | telecom_power_supply → communication_equipment | composition |
| 2 | `photovoltaic_inverter_to_solar_panel` | photovoltaic_inverter → solar_panel | composition |
| 3 | `commercial_vehicle_to_automobile` | commercial_vehicle → automobile | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `dianyuan` | 北京动力源科技股份有限公司 | 600405.SH | 北京 | 北京市 |
| 2 | `nari` | 国电南瑞科技股份有限公司 | 600406.SH | 江苏 | 南京市 |
| 3 | `antai` | 山西安泰集团股份有限公司 | 600408.SH | 山西 | 介休市 |
| 4 | `sanyou_chem` | 唐山三友化工股份有限公司 | 600409.SH | 河北 | 唐山市 |
| 5 | `teamsun` | 北京华胜天成科技股份有限公司 | 600410.SH | 北京 | 北京市 |
| 6 | `yiwu_market` | 浙江中国小商品城集团股份有限公司 | 600415.SH | 浙江 | 义乌市 |
| 7 | `xiangdian` | 湘潭电机股份有限公司 | 600416.SH | 湖南 | 湘潭市 |
| 8 | `jac` | 安徽江淮汽车集团股份有限公司 | 600418.SH | 安徽 | 合肥市 |
| 9 | `tianrun_dairy` | 新疆天润乳业股份有限公司 | 600419.SH | 新疆 | 乌鲁木齐市 |
| 10 | `sinopharm_modern` | 上海现代制药股份有限公司 | 600420.SH | 上海 | 上海市 |

## 4. Company Node Exposures (+30)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 动力源 | telecom_power_supply | manufacture | 通信电源制造商 | 0.95 |
| 动力源 | photovoltaic_inverter | manufacture | 光伏逆变器制造商 | 0.9 |
| 动力源 | ups | manufacture | 不间断电源制造商 | 0.9 |
| 动力源 | power_supply | manufacture | 电源设备制造商 | 0.85 |
| 国电南瑞 | power_grid_automation | provide_service | 电网自动化服务商 | 0.95 |
| 国电南瑞 | substation_automation | provide_service | 变电站自动化服务商 | 0.9 |
| 国电南瑞 | rail_transit_electrical | provide_service | 轨道交通电气服务商 | 0.9 |
| 国电南瑞 | power_distribution_equipment | manufacture | 配电设备制造商 | 0.85 |
| 安泰集团 | coke | produce | 焦炭生产商 | 0.95 |
| 安泰集团 | pig_iron | produce | 生铁生产商 | 0.9 |
| 安泰集团 | cement | produce | 水泥生产商 | 0.9 |
| 安泰集团 | power_generation | operate | 发电运营商 | 0.85 |
| 三友化工 | soda_ash | produce | 纯碱生产商 | 0.95 |
| 三友化工 | chemical_product | produce | 化工产品生产商 | 0.9 |
| 华胜天成 | software | provide_service | 软件服务商 | 0.95 |
| 华胜天成 | system_integration | provide_service | 系统集成服务商 | 0.9 |
| 华胜天成 | it_service | provide_service | IT服务商 | 0.9 |
| 小商品城 | commodity_market | operate | 商品市场运营商 | 0.95 |
| 小商品城 | real_estate_development | operate | 房地产开发运营商 | 0.85 |
| 小商品城 | hotel_service | operate | 酒店服务商 | 0.8 |
| 湘电股份 | ac_motor | manufacture | 交流电机制造商 | 0.95 |
| 湘电股份 | dc_motor | manufacture | 直流电机制造商 | 0.9 |
| 湘电股份 | pump | manufacture | 水泵制造商 | 0.9 |
| 江淮汽车 | commercial_vehicle | manufacture | 商用车制造商 | 0.95 |
| 江淮汽车 | passenger_car | manufacture | 乘用车制造商 | 0.9 |
| 江淮汽车 | automobile | manufacture | 汽车整车制造商 | 0.95 |
| 天润乳业 | dairy_product | produce | 乳制品生产商 | 0.95 |
| 天润乳业 | food | produce | 食品生产商 | 0.85 |
| 国药现代 | antibiotic | produce | 抗生素生产商 | 0.95 |
| 国药现代 | pharmaceutical | produce | 药品生产商 | 0.9 |

---

**Graph increment:** Nodes +9, Edges +3
