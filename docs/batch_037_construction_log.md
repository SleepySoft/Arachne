# Batch 037 Construction Log

**Date:** 2026-05-25
**Companies:** 000919.SZ – 000929.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+5)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `electric_motor` | 电动机 | device |
| 2 | `composite_ro_membrane` | 复合反渗透膜 | material |
| 3 | `steel_cord` | 钢帘线 | material |
| 4 | `railway_freight_car` | 铁路货车 | device |
| 5 | `malt` | 麦芽 | material |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `malt_to_beer` | malt → beer | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `jinling_pharm` | 金陵药业股份有限公司 | 000919.SZ | 江苏 | 南京 |
| 2 | `wodun_tech` | 沃顿科技股份有限公司 | 000920.SZ | 贵州 | 贵阳 |
| 3 | `hisense_appliance` | 海信家电集团股份有限公司 | 000921.SZ | 广东 | 佛山 |
| 4 | `jiadian_motor` | 哈尔滨电气集团佳木斯电机股份有限公司 | 000922.SZ | 黑龙江 | 佳木斯 |
| 5 | `hegang_resources` | 河钢资源股份有限公司 | 000923.SZ | 河北 | 张家口 |
| 6 | `zhonghe_tech` | 浙江众合科技股份有限公司 | 000925.SZ | 浙江 | 杭州 |
| 7 | `fuxing_share` | 湖北福星科技股份有限公司 | 000926.SZ | 湖北 | 孝感 |
| 8 | `china_railway_materials` | 中国铁路物资股份有限公司 | 000927.SZ | 天津 | 天津 |
| 9 | `sinosteel_intl` | 中钢国际工程技术股份有限公司 | 000928.SZ | 吉林 | 吉林 |
| 10 | `st_lanhuang` | 兰州黄河企业股份有限公司 | 000929.SZ | 甘肃 | 兰州 |

## 4. Company Node Exposures (+14)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 金陵药业 | chemical_drug | produce | 化学药品生产商 | 0.9 |
| 金陵药业 | pharmaceutical_product | produce | 医药产品制造商 | 0.85 |
| 沃顿科技 | composite_ro_membrane | produce | 复合反渗透膜生产商 | 0.85 |
| 沃顿科技 | railway_freight_car | manufacture | 铁路货车制造商 | 0.7 |
| 海信家电 | refrigerator | manufacture | 冰箱制造商 | 0.9 |
| 海信家电 | air_conditioner | manufacture | 空调制造商 | 0.9 |
| 佳电股份 | electric_motor | manufacture | 电动机制造商 | 0.9 |
| 河钢资源 | iron_ore | produce | 铁矿石生产商 | 0.8 |
| 众合科技 | semiconductor_device | manufacture | 半导体节能材料制造商 | 0.75 |
| 福星股份 | steel_cord | produce | 钢帘线生产商 | 0.9 |
| 中国铁物 | logistics_service | provide_service | 轨道交通供应链服务商 | 0.9 |
| 中钢国际 | engineering_construction_service | provide_service | 工业工程总承包服务商 | 0.9 |
| 兰州黄河 | beer | produce | 啤酒生产商 | 0.9 |
| 兰州黄河 | malt | produce | 麦芽生产商 | 0.8 |

---

**Graph increment:** Nodes +5, Edges +1
