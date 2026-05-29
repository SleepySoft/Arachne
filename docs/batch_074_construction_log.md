# Batch 074 Construction Log

**Date:** 2026-05-25
**Companies:** 600438.SH – 600458.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+7)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `aquatic_feed` | 水产饲料 | material |
| 2 | `polysilicon` | 多晶硅 | material |
| 3 | `solar_cell` | 太阳能电池 | component |
| 4 | `wig` | 假发饰品 | material |
| 5 | `upvc_pipe` | UPVC双壁波纹管 | component |
| 6 | `titanium_alloy` | 钛合金 | material |
| 7 | `polymer_damping_element` | 高分子减振降噪弹性元件 | component |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `polysilicon_to_solar_cell` | polysilicon → solar_cell | material_flow |
| 2 | `titanium_alloy_to_aircraft` | titanium_alloy → aircraft | material_flow |
| 3 | `upvc_pipe_to_construction` | upvc_pipe → construction | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `tongwei` | 通威股份有限公司 | 600438.SH | 四川 | 成都市 |
| 2 | `rebecca` | 河南瑞贝卡发制品股份有限公司 | 600439.SH | 河南 | 许昌市 |
| 3 | `sinomach_tongyong` | 国机通用机械科技股份有限公司 | 600444.SH | 安徽 | 合肥市 |
| 4 | `jinzheng` | 深圳市金证科技股份有限公司 | 600446.SH | 广东 | 深圳市 |
| 5 | `huafang` | 华纺股份有限公司 | 600448.SH | 山东 | 滨州市 |
| 6 | `ningxia_jiancai` | 宁夏建材集团股份有限公司 | 600449.SH | 宁夏 | 银川市 |
| 7 | `fuling_power` | 重庆涪陵电力实业股份有限公司 | 600452.SH | 重庆 | 重庆市 |
| 8 | `botong` | 西安博通资讯股份有限公司 | 600455.SH | 陕西 | 西安市 |
| 9 | `baoti` | 宝鸡钛业股份有限公司 | 600456.SH | 陕西 | 宝鸡市 |
| 10 | `tmt_newmaterial` | 株洲时代新材料科技股份有限公司 | 600458.SH | 湖南 | 株洲市 |

## 4. Company Node Exposures (+31)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 通威股份 | aquatic_feed | produce | 水产饲料生产商 | 0.95 |
| 通威股份 | livestock_feed | produce | 畜禽饲料生产商 | 0.9 |
| 通威股份 | polysilicon | produce | 多晶硅生产商 | 0.95 |
| 通威股份 | solar_cell | produce | 太阳能电池生产商 | 0.95 |
| 通威股份 | photovoltaic | produce | 光伏产品生产商 | 0.9 |
| 瑞贝卡 | wig | produce | 假发饰品生产商 | 0.95 |
| 瑞贝卡 | hair_product | produce | 发制品生产商 | 0.9 |
| 瑞贝卡 | apparel_accessory | produce | 服饰配饰生产商 | 0.85 |
| 国机通用 | upvc_pipe | manufacture | UPVC波纹管制造商 | 0.95 |
| 国机通用 | pe_pipe | manufacture | PE波纹管制造商 | 0.9 |
| 国机通用 | plastic_pipe | manufacture | 塑料管道制造商 | 0.9 |
| 金证股份 | financial_it | provide_service | 金融IT服务商 | 0.95 |
| 金证股份 | software | provide_service | 软件服务商 | 0.9 |
| 金证股份 | system_integration | provide_service | 系统集成服务商 | 0.9 |
| 华纺股份 | printed_fabric | produce | 印染布生产商 | 0.9 |
| 华纺股份 | cotton_yarn | produce | 棉纱生产商 | 0.85 |
| 华纺股份 | wool_fabric | produce | 呢绒面料生产商 | 0.85 |
| 华纺股份 | textile_product | produce | 纺织品生产商 | 0.9 |
| 宁夏建材 | cement | produce | 水泥生产商 | 0.95 |
| 宁夏建材 | plastic_pipe | produce | 塑料管材生产商 | 0.85 |
| 宁夏建材 | building_material | produce | 建材生产商 | 0.9 |
| 涪陵电力 | power_distribution | operate | 电力配供运营商 | 0.95 |
| 涪陵电力 | power_supply | provide_service | 电力供应服务商 | 0.9 |
| 博通股份 | software | provide_service | 软件服务商 | 0.95 |
| 博通股份 | system_integration | provide_service | 系统集成服务商 | 0.9 |
| 宝钛股份 | titanium_alloy | produce | 钛合金生产商 | 0.95 |
| 宝钛股份 | nonferrous_metal | produce | 有色金属生产商 | 0.9 |
| 宝钛股份 | metal_composite | produce | 金属复合材料生产商 | 0.85 |
| 时代新材 | polymer_damping_element | manufacture | 高分子减振降噪元件制造商 | 0.95 |
| 时代新材 | polymer_composite | manufacture | 高分子复合材料制造商 | 0.9 |
| 时代新材 | special_coating | manufacture | 特种涂料制造商 | 0.85 |

---

**Graph increment:** Nodes +7, Edges +3
