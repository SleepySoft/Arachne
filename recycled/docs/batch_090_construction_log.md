# Batch 090 Construction Log

**Date:** 2026-05-25
**Companies:** 600644.SH – 600657.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `power_transformation_equipment` | 输变电设备 | device |
| 2 | `ac_motor` | 交流电动机 | component |
| 3 | `carrier_wave_communication` | 载波通信 | service |
| 4 | `life_science` | 生命科技 | service |
| 5 | `raw_water_supply` | 原水供应 | service |
| 6 | `lamp_bulb` | 灯泡 | component |
| 7 | `automotive_electronics` | 汽车电子 | component |
| 8 | `security_fire_system` | 安防消防系统集成 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `power_transformation_equipment_to_power_grid` | power_transformation_equipment → power_grid | composition |
| 2 | `lamp_bulb_to_lighting` | lamp_bulb → lighting | composition |
| 3 | `automotive_electronics_to_automobile` | automotive_electronics → automobile | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `leshan_power` | 乐山电力股份有限公司 | 600644.SH | 四川 | 乐山市 |
| 2 | `zhongyuanxiehe` | 中源协和细胞基因工程股份有限公司 | 600645.SH | 天津 | 天津市 |
| 3 | `waigaoqiao` | 上海外高桥集团股份有限公司 | 600648.SH | 上海 | 上海市 |
| 4 | `chengtou` | 上海城投控股股份有限公司 | 600649.SH | 上海 | 上海市 |
| 5 | `jinjiang_online` | 上海锦江在线网络服务股份有限公司 | 600650.SH | 上海 | 上海市 |
| 6 | `feile_audio` | 上海飞乐音响股份有限公司 | 600651.SH | 上海 | 上海市 |
| 7 | `shenhua` | 上海申华控股股份有限公司 | 600653.SH | 上海 | 上海市 |
| 8 | `coa_security` | 中安科股份有限公司 | 600654.SH | 上海 | 上海市 |
| 9 | `yuyuan` | 上海豫园旅游商城(集团)股份有限公司 | 600655.SH | 上海 | 上海市 |
| 10 | `cinda_realestate` | 信达地产股份有限公司 | 600657.SH | 北京 | 北京市 |

## 4. Company Node Exposures (+33)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 乐山电力 | power_installation | provide_service | 电力设施承装服务商 | 0.95 |
| 乐山电力 | power_transformation_equipment | manufacture | 输变电设备制造商 | 0.9 |
| 乐山电力 | ac_motor | produce | 交流电动机生产商 | 0.85 |
| 乐山电力 | carrier_wave_communication | provide_service | 载波通信服务商 | 0.85 |
| 乐山电力 | power_generation | operate | 地方电力运营商 | 0.95 |
| 中源协和 | life_science | provide_service | 生命科技服务商 | 0.95 |
| 中源协和 | biotechnology | produce | 生物技术产品生产商 | 0.9 |
| 外高桥 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 外高桥 | trade_logistics | provide_service | 贸易物流服务商 | 0.9 |
| 外高桥 | hotel_service | operate | 酒店经营管理商 | 0.85 |
| 城投控股 | raw_water_supply | provide_service | 原水供应服务商 | 0.95 |
| 城投控股 | sewage_treatment | operate | 污水处理运营商 | 0.95 |
| 锦江在线 | hotel_service | operate | 酒店运营商 | 0.95 |
| 锦江在线 | catering_service | operate | 餐饮服务商 | 0.9 |
| 锦江在线 | passenger_transport | operate | 客运运营商 | 0.9 |
| 锦江在线 | logistics | provide_service | 物流服务商 | 0.85 |
| 飞乐音响 | lamp_bulb | manufacture | 灯泡制造商 | 0.95 |
| 飞乐音响 | lighting_fixture | manufacture | 灯具制造商 | 0.9 |
| 飞乐音响 | audio_equipment | manufacture | 音响产品制造商 | 0.9 |
| 申华控股 | automotive_service | provide_service | 汽车消费服务商 | 0.95 |
| 申华控股 | new_energy | produce | 新能源产品生产商 | 0.85 |
| 申华控股 | real_estate_development | operate | 房地产运营商 | 0.85 |
| 中安科 | security_fire_system | provide_service | 安防消防系统集成商 | 0.95 |
| 中安科 | automotive_electronics | manufacture | 汽车电子制造商 | 0.9 |
| 中安科 | wire_harness | manufacture | 线束制造商 | 0.85 |
| 中安科 | communication_equipment | manufacture | 无线通信设备制造商 | 0.85 |
| 豫园股份 | gold_ornament | produce | 黄金饰品生产商 | 0.95 |
| 豫园股份 | department_store | operate | 百货运营商 | 0.95 |
| 豫园股份 | catering_service | operate | 饮食服务商 | 0.9 |
| 豫园股份 | pharmaceutical | produce | 药品生产商 | 0.85 |
| 信达地产 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 信达地产 | real_estate_investment | operate | 房地产投资运营商 | 0.9 |
| 信达地产 | property_management | provide_service | 物业管理服务商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
