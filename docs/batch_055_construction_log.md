# Batch 055 Construction Log

**Date:** 2026-05-25
**Companies:** 600178.SH – 600188.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `auto_engine` | 汽车发动机 | component |
| 2 | `container_shipping` | 集装箱航运 | service |
| 3 | `tire` | 轮胎 | component |
| 4 | `copper_clad_laminate` | 覆铜板 | component |
| 5 | `optical_glass` | 光学玻璃 | material |
| 6 | `defense_equipment` | 防务装备 | system |
| 7 | `duty_free` | 免税商品 | service |
| 8 | `monosodium_glutamate` | 味精 | material |
| 9 | `water_supply_service` | 供水服务 | service |
| 10 | `coal_mining` | 煤炭开采 | service |

## 2. New Industrial Edges (+4)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `auto_engine_to_automobile` | auto_engine → automobile | composition |
| 2 | `tire_to_automobile` | tire → automobile | composition |
| 3 | `copper_clad_laminate_to_pcb` | copper_clad_laminate → printed_circuit_board | composition |
| 4 | `optical_glass_to_defense_equipment` | optical_glass → defense_equipment | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `dongan_power` | 哈尔滨东安汽车动力股份有限公司 | 600178.SH | 黑龙江 | 哈尔滨 |
| 2 | `antong` | 安通控股股份有限公司 | 600179.SH | 福建 | 泉州 |
| 3 | `st_ruimao` | 瑞茂通供应链管理股份有限公司 | 600180.SH | 山东 | 烟台 |
| 4 | `giti_tire` | 佳通轮胎股份有限公司 | 600182.SH | 黑龙江 | 牡丹江 |
| 5 | `shengyi_tech` | 广东生益科技股份有限公司 | 600183.SH | 广东 | 东莞 |
| 6 | `norinco_optical` | 北方光电股份有限公司 | 600184.SH | 湖北 | 襄阳 |
| 7 | `zhuhai_dutyfree` | 珠海珠免集团股份有限公司 | 600185.SH | 广东 | 珠海 |
| 8 | `lotus_holdings` | 莲花控股股份有限公司 | 600186.SH | 河南 | 周口 |
| 9 | `st_guozhong` | 黑龙江国中水务股份有限公司 | 600187.SH | 黑龙江 | 哈尔滨 |
| 10 | `yankuang_energy` | 兖矿能源集团股份有限公司 | 600188.SH | 山东 | 济宁 |

## 4. Company Node Exposures (+21)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 东安动力 | auto_engine | manufacture | 汽车发动机制造商 | 0.95 |
| 东安动力 | automobile_part | manufacture | 汽车零部件制造商 | 0.9 |
| 安通控股 | container_shipping | operate | 集装箱航运运营商 | 0.95 |
| 安通控股 | logistics_service | provide_service | 综合物流服务商 | 0.9 |
| *ST瑞茂 | supply_chain_service | provide_service | 供应链服务商 | 0.9 |
| *ST瑞茂 | coal | procure | 煤炭贸易商 | 0.85 |
| S佳通 | tire | manufacture | 轮胎制造商 | 0.95 |
| 生益科技 | copper_clad_laminate | manufacture | 覆铜板制造商 | 0.95 |
| 生益科技 | printed_circuit_board | manufacture | 印制电路板制造商 | 0.9 |
| 光电股份 | optical_glass | produce | 光学玻璃生产商 | 0.9 |
| 光电股份 | defense_equipment | manufacture | 防务装备制造商 | 0.85 |
| 光电股份 | optoelectronic_device | manufacture | 光电子器件制造商 | 0.8 |
| 珠免集团 | duty_free | operate | 免税商品运营商 | 0.95 |
| 珠免集团 | real_estate_development | operate | 房地产开发运营商 | 0.8 |
| 莲花控股 | monosodium_glutamate | produce | 味精生产商 | 0.95 |
| 莲花控股 | flour | produce | 面粉生产商 | 0.85 |
| *ST国中 | water_supply_service | provide_service | 供水服务运营商 | 0.95 |
| *ST国中 | water_treatment | provide_service | 污水处理运营商 | 0.9 |
| 兖矿能源 | coal_mining | operate | 煤炭开采运营商 | 0.95 |
| 兖矿能源 | coal | produce | 煤炭生产商 | 0.95 |
| 兖矿能源 | methanol | produce | 甲醇生产商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +4
