# Batch 032 Construction Log

**Date:** 2026-05-25
**Companies:** 000833.SZ – 000859.SZ (10 companies)
**Status:** ✅ Submitted successfully (2 edge errors: sugar_cane, oilfield_service missing)

---

## 1. New Industrial Nodes (+13, 1 updated)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `white_sugar` | 白砂糖 | material |
| 2 | `bagasse_pulp` | 蔗渣纸浆 | material |
| 3 | `pyrite` | 硫铁矿 | material |
| 4 | `machine_tool` | 机床 | device |
| 5 | `plastic_machinery` | 塑料机械 | device |
| 6 | `cable_tv_network` | 有线电视网 | infrastructure |
| 7 | `satellite_communication` | 卫星通信 | infrastructure |
| 8 | `almond_beverage` | 杏仁露 | material |
| 9 | `oil_drilling_tool` | 石油钻具 | component |
| 10 | `fracturing_equipment` | 压裂装备 | device |
| 11 | `ceramic_product` | 日用陶瓷 | material |
| 12 | `refractory_material` | 耐火材料 | material |
| 13 | `plastic_film` | 塑料薄膜 | material |
| 14 | `capacitor_film` | 电容器薄膜 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type | Status |
|---|---------|---------------------|------|--------|
| 1 | `flow_pyrite_to_sulfuric_acid` | pyrite → sulfuric_acid | material_flow | ✅ |
| 2 | `flow_bagasse_pulp_to_paper` | bagasse_pulp → paper_product | material_flow | ✅ |
| 3 | `flow_sugar_cane_to_white_sugar` | sugar_cane → white_sugar | material_flow | ❌ (sugar_cane missing) |
| 4 | `flow_cable_to_broadcast` | cable_tv_network → broadcasting_equipment | service_flow | ✅ |
| 5 | `flow_drilling_tool_to_oilfield` | oil_drilling_tool → oilfield_service | composition | ❌ (oilfield_service missing) |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `yuegui` | 广西粤桂广业控股股份有限公司 | 000833.SZ | 广西 | 贵港市 | 3,152 |
| 2 | `qinchuan_machine_tool` | 秦川机床工具集团股份公司 | 000837.SZ | 陕西 | 宝鸡市 | 9,203 |
| 3 | `caixin_dev` | 财信地产发展集团股份有限公司 | 000838.SZ | 重庆 | 重庆市 | 188 |
| 4 | `citic_guoan` | 中信国安信息产业股份有限公司 | 000839.SZ | 北京 | 北京市 | 10,195 |
| 5 | `chengde_lulu` | 承德露露股份公司 | 000848.SZ | 河北 | 承德市 | 1,292 |
| 6 | `huamao_textile` | 安徽华茂纺织股份有限公司 | 000850.SZ | 安徽 | 安庆市 | 3,822 |
| 7 | `sinopec_machinery` | 中石化石油机械股份有限公司 | 000852.SZ | 湖北 | 武汉市 | 4,745 |
| 8 | `jidd_equipment` | 唐山冀东装备工程股份有限公司 | 000856.SZ | 河北 | 唐山市 | 1,686 |
| 9 | `wuliangye` | 宜宾五粮液股份有限公司 | 000858.SZ | 四川 | 宜宾市 | 25,132 |
| 10 | `guofeng_new_material` | 安徽国风新材料股份有限公司 | 000859.SZ | 安徽 | 合肥市 | 1,698 |

## 4. Company Node Exposures (+20)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 粤桂股份 | white_sugar | produce | 白砂糖生产商 | 0.9 |
| 粤桂股份 | bagasse_pulp | produce | 蔗渣纸浆生产商 | 0.8 |
| 粤桂股份 | pyrite | produce | 硫铁矿生产商 | 0.7 |
| 粤桂股份 | sulfuric_acid | produce | 硫酸生产商 | 0.7 |
| 秦川机床 | machine_tool | manufacture | 机床制造商 | 0.9 |
| 秦川机床 | plastic_machinery | manufacture | 塑料机械制造商 | 0.7 |
| *ST发展 | real_estate_development | operate | 房地产开发商 | 0.9 |
| 国安股份 | cable_tv_network | operate | 有线电视网络运营商 | 0.8 |
| 国安股份 | satellite_communication | operate | 卫星通信运营商 | 0.7 |
| 承德露露 | almond_beverage | produce | 杏仁露生产商 | 0.9 |
| 华茂股份 | yarn | produce | 纱线生产商 | 0.9 |
| 华茂股份 | textile_product | produce | 纺织品综合制造商 | 0.8 |
| 石化机械 | oil_drilling_tool | manufacture | 石油钻具制造商 | 0.9 |
| 石化机械 | fracturing_equipment | manufacture | 压裂装备制造商 | 0.8 |
| 石化机械 | oilfield_service | operate | 油气田服务商 | 0.7 |
| 冀东装备 | ceramic_product | manufacture | 日用陶瓷制造商 | 0.8 |
| 冀东装备 | refractory_material | manufacture | 耐火材料制造商 | 0.8 |
| 五粮液 | liquor | produce | 白酒生产商 | 0.9 |
| 国风新材 | plastic_film | produce | 塑料薄膜生产商 | 0.9 |
| 国风新材 | capacitor_film | produce | 电容器薄膜生产商 | 0.7 |

---

**Total Graph after Batch 032:**
- Nodes: 583 (570 + 13 + 1U)
- Edges: 444 (441 + 3)
