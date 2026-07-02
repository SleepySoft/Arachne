# Batch 067 Construction Log

**Date:** 2026-05-25
**Companies:** 600338.SH – 600352.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+7)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `lead_zinc` | 铅锌 | material |
| 2 | `petroleum_engineering` | 石油工程 | service |
| 3 | `industrial_park` | 产业园区 | infrastructure |
| 4 | `gas_meter` | 燃气表 | device |
| 5 | `pump` | 泵 | device |
| 6 | `smart_terminal` | 智能终端 | device |
| 7 | `pta` | PTA | material |
| 8 | `polyester_filament` | 涤纶长丝 | material |
| 9 | `dye` | 染料 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `lead_zinc_to_battery` | lead_zinc → battery | material_flow |
| 2 | `pta_to_polyester_filament` | pta → polyester_filament | material_flow |
| 3 | `pump_to_hydraulic_system` | pump → hydraulic_system | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `tibet_summit` | 西藏珠峰资源股份有限公司 | 600338.SH | 西藏 | 拉萨 |
| 2 | `cnpc_eng` | 中国石油集团工程股份有限公司 | 600339.SH | 新疆 | 克拉玛依 |
| 3 | `st_chinafortune` | 华夏幸福基业股份有限公司 | 600340.SH | 河北 | 廊坊 |
| 4 | `aeropower` | 陕西航天动力高科技股份有限公司 | 600343.SH | 陕西 | 西安 |
| 5 | `yangtze_com` | 武汉长江通信产业集团股份有限公司 | 600345.SH | 湖北 | 武汉 |
| 6 | `hengli_petro` | 恒力石化股份有限公司 | 600346.SH | 辽宁 | 大连 |
| 7 | `huayang` | 山西华阳集团新能股份有限公司 | 600348.SH | 山西 | 阳泉 |
| 8 | `sd_expressway` | 山东高速股份有限公司 | 600350.SH | 山东 | 济南 |
| 9 | `yabao_pharma` | 亚宝药业集团股份有限公司 | 600351.SH | 山西 | 运城 |
| 10 | `longsheng` | 浙江龙盛集团股份有限公司 | 600352.SH | 浙江 | 绍兴 |

## 4. Company Node Exposures (+21)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 西藏珠峰 | lead_zinc | produce | 铅锌生产商 | 0.95 |
| 西藏珠峰 | mineral_mining | operate | 矿产开采运营商 | 0.9 |
| 中油工程 | petroleum_engineering | provide_service | 石油工程承包商 | 0.95 |
| 中油工程 | construction_engineering | provide_service | 建筑工程承包商 | 0.85 |
| *ST华幸 | industrial_park | operate | 产业园区运营商 | 0.9 |
| *ST华幸 | real_estate_development | operate | 房地产开发运营商 | 0.85 |
| 航天动力 | gas_meter | manufacture | 燃气表制造商 | 0.9 |
| 航天动力 | pump | manufacture | 泵制造商 | 0.9 |
| 航天动力 | hydraulic_system | manufacture | 液压系统制造商 | 0.85 |
| 长江通信 | smart_terminal | manufacture | 智能终端制造商 | 0.9 |
| 长江通信 | communication_equipment | manufacture | 通信设备制造商 | 0.85 |
| 恒力石化 | pta | produce | PTA生产商 | 0.95 |
| 恒力石化 | polyester_filament | produce | 涤纶长丝生产商 | 0.95 |
| 恒力石化 | chemical_product | produce | 化工产品生产商 | 0.9 |
| 华阳股份 | coal | produce | 煤炭生产商 | 0.95 |
| 华阳股份 | power_generation | operate | 发电运营商 | 0.85 |
| 山东高速 | expressway | operate | 高速公路运营商 | 0.95 |
| 山东高速 | toll_road | operate | 路桥收费运营商 | 0.9 |
| 亚宝药业 | chinese_patent_medicine | produce | 中成药生产商 | 0.95 |
| 浙江龙盛 | dye | produce | 染料生产商 | 0.95 |
| 浙江龙盛 | chemical_intermediate | produce | 化工中间体生产商 | 0.85 |

---

**Graph increment:** Nodes +7, Edges +3
