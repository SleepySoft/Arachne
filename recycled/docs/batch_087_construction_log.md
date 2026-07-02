# Batch 087 Construction Log

**Date:** 2026-05-25
**Companies:** 600608.SH – 600618.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `garden_design` | 园林设计 | service |
| 2 | `transportation` | 运输业 | service |
| 3 | `gold_jewelry` | 黄金珠宝首饰 | material |
| 4 | `natural_gas_pipeline` | 天然气长输管道 | infrastructure |
| 5 | `city_gas` | 城市燃气 | service |
| 6 | `polyvinyl_chloride` | 聚氯乙烯 | material |
| 7 | `caustic_soda` | 烧碱 | material |
| 8 | `chlorine_product` | 氯产品 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `natural_gas_pipeline_to_city_gas` | natural_gas_pipeline → city_gas | capability_supply |
| 2 | `polyvinyl_chloride_to_plastic` | polyvinyl_chloride → plastic | material_flow |
| 3 | `caustic_soda_to_chemical_industry` | caustic_soda → chemical_industry | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `st_huke` | 上海宽频科技股份有限公司 | 600608.SH | 上海 | 上海市 |
| 2 | `jinbei_auto` | 沈阳金杯汽车股份有限公司 | 600609.SH | 辽宁 | 沈阳市 |
| 3 | `zhongyida` | 上海中毅达股份有限公司 | 600610.SH | 上海 | 上海市 |
| 4 | `dazhong_transport` | 大众交通(集团)股份有限公司 | 600611.SH | 上海 | 上海市 |
| 5 | `laofengxiang` | 老凤祥股份有限公司 | 600612.SH | 上海 | 上海市 |
| 6 | `shenqi` | 上海神奇制药投资管理股份有限公司 | 600613.SH | 上海 | 上海市 |
| 7 | `xinyuan` | 鑫源智造(上海)股份有限公司 | 600615.SH | 上海 | 上海市 |
| 8 | `jinfeng_wine` | 上海金枫酒业股份有限公司 | 600616.SH | 上海 | 上海市 |
| 9 | `guoxin_energy` | 山西省国新能源股份有限公司 | 600617.SH | 山西 | 太原市 |
| 10 | `chlor_alkali` | 上海氯碱化工股份有限公司 | 600618.SH | 上海 | 上海市 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| *ST沪科 | nonferrous_metal | procure | 有色金属贸易商 | 0.95 |
| *ST沪科 | ferrous_metal | procure | 黑色金属贸易商 | 0.9 |
| *ST沪科 | chemical_product | procure | 化工原料贸易商 | 0.9 |
| 金杯汽车 | automobile | manufacture | 汽车制造商 | 0.95 |
| 金杯汽车 | automobile_part | manufacture | 汽车零部件制造商 | 0.95 |
| 中毅达 | garden_design | provide_service | 园林设计服务商 | 0.95 |
| 中毅达 | construction | operate | 园林工程运营商 | 0.9 |
| 大众交通 | transportation | operate | 运输业运营商 | 0.95 |
| 大众交通 | tourism_catering | operate | 旅游饮食运营商 | 0.85 |
| 大众交通 | passenger_transport | operate | 客运运营商 | 0.9 |
| 老凤祥 | gold_jewelry | produce | 黄金珠宝首饰生产商 | 0.95 |
| 老凤祥 | arts_and_crafts | produce | 工艺美术品生产商 | 0.85 |
| 老凤祥 | pen | produce | 笔类文具制品生产商 | 0.8 |
| 神奇制药 | pharmaceutical | produce | 药品生产商 | 0.95 |
| 神奇制药 | investment_management | operate | 医药投资运营商 | 0.85 |
| 鑫源智造 | coating | produce | 涂料生产商 | 0.95 |
| 鑫源智造 | pen | manufacture | 制笔制造商 | 0.9 |
| 金枫酒业 | liquor | produce | 酒类生产商 | 0.95 |
| 金枫酒业 | warehousing | provide_service | 仓储货运服务商 | 0.85 |
| 国新能源 | natural_gas_pipeline | operate | 天然气长输管道运营商 | 0.95 |
| 国新能源 | city_gas | operate | 城市燃气运营商 | 0.95 |
| 国新能源 | heating_supply | provide_service | 供热供应商 | 0.85 |
| 氯碱化工 | polyvinyl_chloride | produce | 聚氯乙烯生产商 | 0.95 |
| 氯碱化工 | caustic_soda | produce | 烧碱生产商 | 0.95 |
| 氯碱化工 | chlorine_product | produce | 氯产品生产商 | 0.9 |
| 氯碱化工 | chemical_product | produce | 化工产品生产商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
