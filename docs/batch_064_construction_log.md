# Batch 064 Construction Log

**Date:** 2026-05-25
**Companies:** 600300.SH – 600312.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+11)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `soy_milk_powder` | 豆奶粉 | material |
| 2 | `nonferrous_metal_mining` | 有色金属采选 | service |
| 3 | `industrial_sewing_machine` | 工业缝纫机 | device |
| 4 | `vehicle_axle` | 车桥 | component |
| 5 | `special_vehicle` | 专用车 | system |
| 6 | `vinegar` | 食醋 | material |
| 7 | `soy_sauce` | 酱油 | material |
| 8 | `carbon_steel` | 碳钢 | material |
| 9 | `stainless_steel` | 不锈钢 | material |
| 10 | `newsprint` | 新闻纸 | material |
| 11 | `mdi` | MDI | material |
| 12 | `high_voltage_switchgear` | 高压开关设备 | device |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `vinegar_to_food` | vinegar → food | material_flow |
| 2 | `carbon_steel_to_construction` | carbon_steel → construction_material | material_flow |
| 3 | `mdi_to_polyurethane` | mdi → polyurethane | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `vivi` | 维维食品饮料股份有限公司 | 600300.SH | 江苏 | 徐州 |
| 2 | `huaxi_nonferrous` | 广西华锡有色金属股份有限公司 | 600301.SH | 广西 | 南宁 |
| 3 | `st_standard` | 西安标准工业股份有限公司 | 600302.SH | 陕西 | 西安 |
| 4 | `sg_auto` | 辽宁曙光汽车集团股份有限公司 | 600303.SH | 辽宁 | 丹东 |
| 5 | `hengshun` | 江苏恒顺醋业股份有限公司 | 600305.SH | 江苏 | 镇江 |
| 6 | `jiugang` | 甘肃酒钢集团宏兴钢铁股份有限公司 | 600307.SH | 甘肃 | 嘉峪关 |
| 7 | `huatai_paper` | 山东华泰纸业股份有限公司 | 600308.SH | 山东 | 东营 |
| 8 | `wanhua_chem` | 万华化学集团股份有限公司 | 600309.SH | 山东 | 烟台 |
| 9 | `guangxi_energy` | 广西能源股份有限公司 | 600310.SH | 广西 | 贺州 |
| 10 | `pinggao_elec` | 河南平高电气股份有限公司 | 600312.SH | 河南 | 平顶山 |

## 4. Company Node Exposures (+28)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 维维股份 | soy_milk_powder | produce | 豆奶粉生产商 | 0.95 |
| 维维股份 | beverage | produce | 饮料生产商 | 0.85 |
| 维维股份 | food | produce | 食品生产商 | 0.8 |
| 华锡有色 | nonferrous_metal_mining | operate | 有色金属采选运营商 | 0.95 |
| 华锡有色 | rare_earth_metal | produce | 稀有金属生产商 | 0.85 |
| ST标准 | industrial_sewing_machine | manufacture | 工业缝纫机制造商 | 0.95 |
| ST标准 | textile_machinery | manufacture | 纺织机械制造商 | 0.9 |
| 曙光股份 | vehicle_axle | manufacture | 车桥制造商 | 0.9 |
| 曙光股份 | bus | manufacture | 客车制造商 | 0.85 |
| 曙光股份 | special_vehicle | manufacture | 专用车制造商 | 0.8 |
| 曙光股份 | automobile_part | manufacture | 汽车零部件制造商 | 0.85 |
| 恒顺醋业 | vinegar | produce | 食醋生产商 | 0.95 |
| 恒顺醋业 | soy_sauce | produce | 酱油生产商 | 0.9 |
| 恒顺醋业 | food | produce | 食品生产商 | 0.8 |
| 酒钢宏兴 | carbon_steel | produce | 碳钢生产商 | 0.95 |
| 酒钢宏兴 | stainless_steel | produce | 不锈钢生产商 | 0.9 |
| 酒钢宏兴 | steel_plate | produce | 钢铁板材生产商 | 0.85 |
| 华泰股份 | newsprint | produce | 新闻纸生产商 | 0.95 |
| 华泰股份 | cultural_paper | produce | 文化纸生产商 | 0.9 |
| 华泰股份 | paper | produce | 纸制品生产商 | 0.85 |
| 万华化学 | mdi | produce | MDI生产商 | 0.95 |
| 万华化学 | chemical_product | produce | 化工产品生产商 | 0.9 |
| 万华化学 | polyurethane | produce | 聚氨酯生产商 | 0.9 |
| 广西能源 | power_generation | operate | 发电业务运营商 | 0.95 |
| 广西能源 | hydro_power | operate | 水力发电运营商 | 0.85 |
| 平高电气 | high_voltage_switchgear | manufacture | 高压开关设备制造商 | 0.95 |
| 平高电气 | switchgear | manufacture | 开关设备制造商 | 0.9 |
| 平高电气 | power_distribution_equipment | manufacture | 配电设备制造商 | 0.85 |

---

**Graph increment:** Nodes +11, Edges +3
