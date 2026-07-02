# Batch 041 Construction Log

**Date:** 2026-05-25
**Companies:** 000977.SZ – 000990.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+7)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `cvt_transmission` | 无级变速器 | component |
| 2 | `dct_transmission` | 双离合变速器 | component |
| 3 | `hybrid_power_system` | 混合动力系统 | subsystem |
| 4 | `electric_drive_system` | 电驱动系统 | subsystem |
| 5 | `coking_coal` | 焦煤 | material |
| 6 | `petroleum_resin` | 石油树脂 | material |
| 7 | `donkey_hide_gelatin` | 驴胶补血产品 | material |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `coking_coal_to_steel_plate` | coking_coal → steel_plate | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `inspur` | 浪潮电子信息产业股份有限公司 | 000977.SZ | 山东 | 济南 |
| 2 | `guilin_tourism` | 桂林旅游股份有限公司 | 000978.SZ | 广西 | 桂林 |
| 3 | `zhongtai_auto` | 众泰汽车股份有限公司 | 000980.SZ | 浙江 | 金华 |
| 4 | `shanzi_hitech` | 山子高科技股份有限公司 | 000981.SZ | 甘肃 | 兰州 |
| 5 | `shanxi_coking` | 山西焦煤能源集团股份有限公司 | 000983.SZ | 山西 | 太原 |
| 6 | `daqing_huake` | 大庆华科股份有限公司 | 000985.SZ | 黑龙江 | 大庆 |
| 7 | `yuexiu_capital` | 广州越秀资本控股集团股份有限公司 | 000987.SZ | 广东 | 广州 |
| 8 | `huagong_tech` | 华工科技产业股份有限公司 | 000988.SZ | 湖北 | 武汉 |
| 9 | `jiuzhitang` | 九芝堂股份有限公司 | 000989.SZ | 湖南 | 长沙 |
| 10 | `chengzhi` | 诚志股份有限公司 | 000990.SZ | 江西 | 南昌 |

## 4. Company Node Exposures (+12)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 浪潮信息 | server_hardware | manufacture | 服务器制造商 | 0.95 |
| 桂林旅游 | tourism_service | operate | 旅游服务运营商 | 0.9 |
| 众泰汽车 | automotive_part | manufacture | 汽车整车及配件制造商 | 0.85 |
| 山子高科 | cvt_transmission | manufacture | 无级变速器制造商 | 0.9 |
| 山子高科 | dct_transmission | manufacture | 双离合变速器制造商 | 0.85 |
| 山子高科 | hybrid_power_system | manufacture | 混合动力系统制造商 | 0.8 |
| 山西焦煤 | coking_coal | produce | 焦煤生产商 | 0.95 |
| 大庆华科 | petroleum_resin | produce | 石油树脂生产商 | 0.85 |
| 大庆华科 | polypropylene | produce | 聚丙烯生产商 | 0.85 |
| 九芝堂 | chinese_patent_medicine | produce | 中成药生产商 | 0.9 |
| 九芝堂 | donkey_hide_gelatin | produce | 驴胶补血产品生产商 | 0.85 |
| 诚志股份 | chemical_product | produce | 精细化工产品生产商 | 0.75 |

---

**Graph increment:** Nodes +7, Edges +1
