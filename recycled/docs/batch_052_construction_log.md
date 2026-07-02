# Batch 052 Construction Log

**Date:** 2026-05-25
**Companies:** 600136.SH – 600153.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `film_tv` | 影视传媒 | service |
| 2 | `sports_service` | 体育服务 | service |
| 3 | `underwear` | 内衣 | material |
| 4 | `tourism_service` | 旅游服务 | service |
| 5 | `automobile_clutch` | 汽车离合器 | component |
| 6 | `clean_energy_supply` | 清洁能源供应 | service |
| 7 | `shipbuilding` | 船舶制造 | system |
| 8 | `solar_cell` | 太阳能电池 | component |
| 9 | `consumer_battery` | 消费类电池 | component |
| 10 | `supply_chain_service` | 供应链服务 | service |

## 2. New Industrial Edges (+2)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `solar_cell_to_solar_panel` | solar_cell → solar_panel | composition |
| 2 | `automobile_clutch_to_automobile` | automobile_clutch → automobile | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `st_mingcheng` | 武汉明诚文化体育集团股份有限公司 | 600136.SH | 湖北 | 武汉 |
| 2 | `langsha` | 四川浪莎控股股份有限公司 | 600137.SH | 四川 | 宜宾 |
| 3 | `cyts` | 中青旅控股股份有限公司 | 600138.SH | 北京 | 北京 |
| 4 | `xingfa_group` | 湖北兴发化工集团股份有限公司 | 600141.SH | 湖北 | 宜昌 |
| 5 | `changchun_yidong` | 长春一东离合器股份有限公司 | 600148.SH | 吉林 | 长春 |
| 6 | `langfang_dev` | 廊坊发展股份有限公司 | 600149.SH | 河北 | 廊坊 |
| 7 | `cssc` | 中国船舶工业股份有限公司 | 600150.SH | 上海 | 上海 |
| 8 | `aerospace_mech` | 上海航天汽车机电股份有限公司 | 600151.SH | 上海 | 上海 |
| 9 | `victor_tech` | 维科技术股份有限公司 | 600152.SH | 浙江 | 宁波 |
| 10 | `cnd` | 厦门建发股份有限公司 | 600153.SH | 福建 | 厦门 |

## 4. Company Node Exposures (+19)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| ST明诚 | film_tv | provide_service | 影视传媒服务商 | 0.85 |
| ST明诚 | sports_service | provide_service | 体育服务运营商 | 0.8 |
| 浪莎股份 | underwear | produce | 内衣制造商 | 0.9 |
| 浪莎股份 | textile_product | produce | 纺织品生产商 | 0.85 |
| 中青旅 | tourism_service | provide_service | 旅游服务提供商 | 0.95 |
| 兴发集团 | phosphorus_chemical | produce | 磷化工产品生产商 | 0.95 |
| 兴发集团 | chemical_fertilizer | produce | 化学肥料生产商 | 0.9 |
| 长春一东 | automobile_clutch | manufacture | 汽车离合器制造商 | 0.95 |
| 长春一东 | automobile_part | manufacture | 汽车零部件制造商 | 0.9 |
| 廊坊发展 | trade_agent | provide_service | 贸易及供能服务商 | 0.8 |
| 廊坊发展 | clean_energy_supply | provide_service | 清洁能源供应商 | 0.75 |
| 中国船舶 | shipbuilding | manufacture | 船舶制造商 | 0.95 |
| 中国船舶 | ship_accessory | manufacture | 船舶配件制造商 | 0.85 |
| 航天机电 | solar_cell | manufacture | 太阳能电池制造商 | 0.9 |
| 航天机电 | automobile_part | manufacture | 汽车零部件制造商 | 0.8 |
| 维科技术 | consumer_battery | manufacture | 消费类电池制造商 | 0.9 |
| 维科技术 | lithium_battery | manufacture | 锂电池制造商 | 0.85 |
| 建发股份 | supply_chain_service | provide_service | 供应链服务商 | 0.95 |
| 建发股份 | real_estate_development | operate | 房地产开发运营商 | 0.85 |

---

**Graph increment:** Nodes +9, Edges +2
