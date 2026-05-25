# Batch 033 Construction Log

**Date:** 2026-05-25
**Companies:** 000860.SZ – 000880.SZ (10 companies)
**Status:** ✅ Submitted successfully (2 edge errors: public_transportation, ship missing)

---

## 1. New Industrial Nodes (+6, 2 updated)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `meat_product` | 肉类产品 | material |
| 2 | `vegetable_fruit_beverage` | 果蔬饮料 | material |
| 3 | `bus` | 客车 | system |
| 4 | `new_energy_vehicle` | 新能源汽车 | system |
| 5 | `wine` | 葡萄酒 | material |
| 6 | `brandy` | 白兰地 | material |
| 7 | `marine_engine` | 船用发动机 | component |
| 8 | `gearbox` | 齿轮箱 | component |

## 2. New Industrial Edges (+2)

| # | Edge ID | From Node → To Node | Type | Status |
|---|---------|---------------------|------|--------|
| 1 | `flow_live_pig_to_meat` | live_pig → meat_product | material_flow | ✅ |
| 2 | `flow_bus_to_transport` | bus → public_transportation | service_flow | ❌ (public_transportation missing) |
| 3 | `flow_wine_to_brandy` | wine → brandy | material_flow | ✅ |
| 4 | `flow_marine_engine_to_ship` | marine_engine → ship | composition | ❌ (ship missing) |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `shunxin_agriculture` | 北京顺鑫农业股份有限公司 | 000860.SZ | 北京 | 北京市 | 3,739 |
| 2 | `yinxing_energy` | 宁夏银星能源股份有限公司 | 000862.SZ | 宁夏 | 银川市 | 556 |
| 3 | `sanxiang_impression` | 三湘印象股份有限公司 | 000863.SZ | 上海 | 上海市 | 334 |
| 4 | `ankai_bus` | 安徽安凯汽车股份有限公司 | 000868.SZ | 安徽 | 合肥市 | 1,881 |
| 5 | `changyu` | 烟台张裕葡萄酿酒股份有限公司 | 000869.SZ | 山东 | 烟台市 | 2,158 |
| 6 | `spic_green_energy` | 国电投绿色能源股份有限公司 | 000875.SZ | 吉林 | 长春市 | 3,731 |
| 7 | `new_hope` | 新希望六和股份有限公司 | 000876.SZ | 四川 | 绵阳市 | 41,327 |
| 8 | `tianshan_cement` | 天山材料股份有限公司 | 000877.SZ | 新疆 | 乌鲁木齐市 | 51,423 |
| 9 | `yunnan_copper` | 云南铜业股份有限公司 | 000878.SZ | 云南 | 昆明市 | 9,465 |
| 10 | `weichai_heavy_machinery` | 潍柴重机股份有限公司 | 000880.SZ | 山东 | 潍坊市 | 2,204 |

## 4. Company Node Exposures (+28)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 顺鑫农业 | liquor | produce | 白酒生产商 | 0.9 |
| 顺鑫农业 | meat_product | produce | 肉类产品生产商 | 0.8 |
| 顺鑫农业 | vegetable_fruit_beverage | produce | 果蔬饮料生产商 | 0.6 |
| 银星能源 | wind_power_generation | operate | 风力发电运营商 | 0.9 |
| 银星能源 | solar_power_generation | operate | 太阳能发电运营商 | 0.8 |
| 三湘印象 | real_estate_development | operate | 房地产开发商 | 0.8 |
| 三湘印象 | film_television | operate | 影视文化运营商 | 0.6 |
| 安凯客车 | bus | manufacture | 客车制造商 | 0.9 |
| 安凯客车 | new_energy_vehicle | manufacture | 新能源汽车制造商 | 0.8 |
| 安凯客车 | commercial_vehicle | manufacture | 商用车制造商 | 0.7 |
| 张裕A | wine | produce | 葡萄酒生产商 | 0.9 |
| 张裕A | brandy | produce | 白兰地生产商 | 0.7 |
| 电投绿能 | coal_power_generation | operate | 火电运营商 | 0.8 |
| 电投绿能 | hydro_power_generation | operate | 水电运营商 | 0.7 |
| 电投绿能 | wind_power_generation | operate | 风电运营商 | 0.8 |
| 电投绿能 | solar_power_generation | operate | 光伏发电运营商 | 0.7 |
| 电投绿能 | heating_supply | produce | 热力供应商 | 0.8 |
| 新希望 | feed | produce | 饲料生产商 | 0.9 |
| 新希望 | livestock_breeding | operate | 养殖服务商 | 0.9 |
| 新希望 | meat_product | produce | 肉制品加工商 | 0.8 |
| 天山股份 | cement | produce | 水泥生产商 | 0.9 |
| 云南铜业 | copper | produce | 阴极铜生产商 | 0.9 |
| 云南铜业 | sulfuric_acid | produce | 硫酸生产商 | 0.7 |
| 云南铜业 | gold | produce | 黄金生产商 | 0.6 |
| 云南铜业 | silver | produce | 白银生产商 | 0.6 |
| 潍柴重机 | marine_engine | manufacture | 船用发动机制造商 | 0.9 |
| 潍柴重机 | generator_set | manufacture | 发电机组制造商 | 0.8 |
| 潍柴重机 | gearbox | manufacture | 齿轮箱制造商 | 0.8 |

---

**Total Graph after Batch 033:**
- Nodes: 589 (583 + 6 + 2U)
- Edges: 446 (444 + 2)
