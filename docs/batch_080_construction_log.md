# Batch 080 Construction Log

**Date:** 2026-05-25
**Companies:** 600525.SH – 600536.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `ev_material` | 电动汽车相关材料 | material |
| 2 | `smart_factory_equipment` | 智能工厂装备 | device |
| 3 | `smart_grid_device` | 智能电网设备 | device |
| 4 | `electrostatic_precipitator` | 电除尘器 | device |
| 5 | `polyester_top` | 涤纶毛条 | material |
| 6 | `railway_project` | 铁路工程 | service |
| 7 | `molded_bottle` | 模制瓶 | component |
| 8 | `electrolytic_lead` | 电解铅 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `ev_material_to_electric_vehicle` | ev_material → electric_vehicle | composition |
| 2 | `smart_grid_device_to_power_grid` | smart_grid_device → power_grid | composition |
| 3 | `electrostatic_precipitator_to_power_plant` | electrostatic_precipitator → power_plant | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `st_changyuan` | 长园科技集团股份有限公司 | 600525.SH | 广东 | 深圳市 |
| 2 | `feida_env` | 浙江菲达环保科技股份有限公司 | 600526.SH | 浙江 | 绍兴市 |
| 3 | `jiangnan_gaoxian` | 江苏江南高纤股份有限公司 | 600527.SH | 江苏 | 苏州市 |
| 4 | `crec_industrial` | 中铁高新工业股份有限公司 | 600528.SH | 北京 | 北京市 |
| 5 | `shandong_pharma_glass` | 山东省药用玻璃股份有限公司 | 600529.SH | 山东 | 淄博市 |
| 6 | `sjtu_only` | 上海交大昂立股份有限公司 | 600530.SH | 上海 | 上海市 |
| 7 | `yuguang` | 河南豫光金铅股份有限公司 | 600531.SH | 河南 | 济源市 |
| 8 | `qixia` | 南京栖霞建设股份有限公司 | 600533.SH | 江苏 | 南京市 |
| 9 | `tasly` | 天士力医药集团股份有限公司 | 600535.SH | 天津 | 天津市 |
| 10 | `css` | 中国软件与技术服务股份有限公司 | 600536.SH | 北京 | 北京市 |

## 4. Company Node Exposures (+27)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| ST长园 | ev_material | produce | 电动汽车材料生产商 | 0.95 |
| ST长园 | smart_factory_equipment | manufacture | 智能工厂装备制造商 | 0.95 |
| ST长园 | smart_grid_device | manufacture | 智能电网设备制造商 | 0.95 |
| 菲达环保 | electrostatic_precipitator | manufacture | 电除尘器制造商 | 0.95 |
| 菲达环保 | pneumatic_conveying | provide_service | 气力输送服务商 | 0.9 |
| 菲达环保 | desulfurization_product | manufacture | 脱硫产品制造商 | 0.9 |
| 江南高纤 | polyester_top | produce | 涤纶毛条生产商 | 0.95 |
| 江南高纤 | polyester_staple_fiber | produce | 涤纶短纤维生产商 | 0.95 |
| 江南高纤 | chemical_fiber | produce | 化纤产品生产商 | 0.9 |
| 中铁工业 | railway_project | operate | 铁路工程运营商 | 0.95 |
| 中铁工业 | rail_transit_equipment | manufacture | 轨道交通装备制造商 | 0.9 |
| 山东药玻 | molded_bottle | manufacture | 模制瓶制造商 | 0.95 |
| 山东药玻 | ampoule | manufacture | 安瓿制造商 | 0.9 |
| 山东药玻 | butyl_rubber_stopper | manufacture | 丁基胶塞制造商 | 0.9 |
| 山东药玻 | pharmaceutical_packaging | manufacture | 药用包装制造商 | 0.95 |
| 交大昂立 | health_food | produce | 保健食品生产商 | 0.95 |
| 交大昂立 | food | produce | 食品生产商 | 0.9 |
| 豫光金铅 | electrolytic_lead | produce | 电解铅生产商 | 0.95 |
| 豫光金铅 | silver_product | produce | 白银生产商 | 0.9 |
| 豫光金铅 | gold | produce | 黄金生产商 | 0.9 |
| 栖霞建设 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 天士力 | chinese_patent_medicine | produce | 中药生产商 | 0.95 |
| 天士力 | chemical_drug | produce | 化学药生产商 | 0.9 |
| 天士力 | biological_drug | produce | 生物药生产商 | 0.9 |
| 中国软件 | system_software | provide_service | 系统软件服务商 | 0.95 |
| 中国软件 | application_software | provide_service | 应用软件服务商 | 0.95 |
| 中国软件 | software_export | provide_service | 软件出口加工服务商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
