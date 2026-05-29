# Batch 084 Construction Log

**Date:** 2026-05-25
**Companies:** 600576.SH – 600585.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `enameled_wire` | 漆包电磁线 | material |
| 2 | `power_cable` | 电线电缆 | component |
| 3 | `desulfurization_byproduct` | 脱硫副产品 | material |
| 4 | `chemical_equipment` | 化工装备 | device |
| 5 | `industrial_motor` | 工业驱动及控制电机 | component |
| 6 | `electric_bicycle` | 电动自行车 | system |
| 7 | `mining_automation` | 矿山自动化 | service |
| 8 | `ocean_engineering` | 海洋工程 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `enameled_wire_to_motor` | enameled_wire → motor | composition |
| 2 | `industrial_motor_to_industrial_equipment` | industrial_motor → industrial_equipment | composition |
| 3 | `ocean_engineering_to_offshore_oil` | ocean_engineering → offshore_oil | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `xiangyuan` | 浙江祥源文旅股份有限公司 | 600576.SH | 浙江 | 杭州市 |
| 2 | `jinda` | 铜陵精达特种电磁线股份有限公司 | 600577.SH | 安徽 | 铜陵市 |
| 3 | `jingneng_power` | 北京京能电力股份有限公司 | 600578.SH | 北京 | 北京市 |
| 4 | `sinochem_equip` | 中化装备科技(青岛)股份有限公司 | 600579.SH | 山东 | 青岛市 |
| 5 | `wolong` | 卧龙电气驱动集团股份有限公司 | 600580.SH | 浙江 | 绍兴市 |
| 6 | `st_bayi` | 新疆八一钢铁股份有限公司 | 600581.SH | 新疆 | 乌鲁木齐市 |
| 7 | `tiandi` | 天地科技股份有限公司 | 600582.SH | 北京 | 北京市 |
| 8 | `cooec` | 海洋石油工程股份有限公司 | 600583.SH | 天津 | 天津市 |
| 9 | `jcet` | 江苏长电科技股份有限公司 | 600584.SH | 江苏 | 无锡市 |
| 10 | `conch` | 安徽海螺水泥股份有限公司 | 600585.SH | 安徽 | 芜湖市 |

## 4. Company Node Exposures (+28)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 祥源文旅 | real_estate_development | operate | 房地产开发运营商 | 0.95 |
| 祥源文旅 | hotel_service | operate | 连锁酒店运营商 | 0.9 |
| 祥源文旅 | tourism_investment | operate | 文旅投资运营商 | 0.85 |
| 精达股份 | enameled_wire | produce | 漆包电磁线生产商 | 0.95 |
| 精达股份 | bare_copper_wire | produce | 裸铜线生产商 | 0.9 |
| 精达股份 | power_cable | produce | 电线电缆生产商 | 0.9 |
| 京能电力 | power_generation | operate | 发电运营商 | 0.95 |
| 京能电力 | heating_supply | provide_service | 热力供应商 | 0.9 |
| 京能电力 | desulfurization_byproduct | produce | 脱硫副产品生产商 | 0.8 |
| 中化装备 | chemical_equipment | manufacture | 化工装备制造商 | 0.95 |
| 中化装备 | chemical_industry | operate | 化工行业服务商 | 0.85 |
| 卧龙电驱 | industrial_motor | manufacture | 工业电机制造商 | 0.95 |
| 卧龙电驱 | medium_high_voltage_motor | manufacture | 中高压电机制造商 | 0.9 |
| 卧龙电驱 | household_appliance_motor | manufacture | 家用电器电机制造商 | 0.9 |
| 卧龙电驱 | electric_bicycle | manufacture | 电动自行车制造商 | 0.85 |
| *ST八钢 | high_speed_wire_rod | produce | 高速线材生产商 | 0.95 |
| *ST八钢 | rebar | produce | 螺纹钢生产商 | 0.95 |
| *ST八钢 | hot_rolled_coil | produce | 热轧卷板生产商 | 0.9 |
| *ST八钢 | steel | produce | 钢铁生产商 | 0.95 |
| 天地科技 | mining_automation | provide_service | 矿山自动化服务商 | 0.95 |
| 天地科技 | coal_washing_equipment | manufacture | 煤炭洗选装备制造商 | 0.9 |
| 天地科技 | coal_mining | operate | 煤炭开采运营商 | 0.85 |
| 海油工程 | ocean_engineering | operate | 海洋工程运营商 | 0.95 |
| 海油工程 | offshore_oil | provide_service | 海上油气工程服务商 | 0.9 |
| 长电科技 | integrated_circuit_packaging | provide_service | 集成电路封装测试服务商 | 0.95 |
| 长电科技 | semiconductor_device | manufacture | 半导体分立器件制造商 | 0.9 |
| 海螺水泥 | cement | produce | 水泥生产商 | 0.95 |
| 海螺水泥 | building_material | produce | 建材生产商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
