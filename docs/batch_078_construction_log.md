# Batch 078 Construction Log

**Date:** 2026-05-25
**Companies:** 600502.SH – 600512.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `engineering_general_contracting` | 工程总承包 | service |
| 2 | `equity_investment` | 股权投资 | service |
| 3 | `rebar` | 螺纹钢 | material |
| 4 | `leaf_spring` | 汽车板簧 | component |
| 5 | `iron_concentrate` | 铁精粉 | material |
| 6 | `raw_coal` | 原煤 | material |
| 7 | `denim` | 牛仔布 | material |
| 8 | `pharmaceutical_commerce` | 医药商业 | service |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `rebar_to_construction` | rebar → construction | material_flow |
| 2 | `leaf_spring_to_automobile` | leaf_spring → automobile | composition |
| 3 | `iron_concentrate_to_steel` | iron_concentrate → steel | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `anhui_construction` | 安徽建工集团股份有限公司 | 600502.SH | 安徽 | 合肥市 |
| 2 | `huali_family` | 华丽家族股份有限公司 | 600503.SH | 上海 | 上海市 |
| 3 | `xichang_power` | 四川西昌电力股份有限公司 | 600505.SH | 四川 | 西昌市 |
| 4 | `unified_co` | 统一低碳科技(新疆)股份有限公司 | 600506.SH | 新疆 | 库尔勒市 |
| 5 | `fangda_special_steel` | 方大特钢科技股份有限公司 | 600507.SH | 江西 | 南昌市 |
| 6 | `shanghai_energy` | 上海大屯能源股份有限公司 | 600508.SH | 上海 | 上海市 |
| 7 | `tianfu_energy` | 新疆天富能源股份有限公司 | 600509.SH | 新疆 | 石河子市 |
| 8 | `black_peony` | 黑牡丹(集团)股份有限公司 | 600510.SH | 江苏 | 常州市 |
| 9 | `sinopharm_co` | 国药集团药业股份有限公司 | 600511.SH | 北京 | 北京市 |
| 10 | `tengda` | 腾达建设集团股份有限公司 | 600512.SH | 浙江 | 台州市 |

## 4. Company Node Exposures (+26)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 安徽建工 | engineering_general_contracting | operate | 工程总承包商 | 0.95 |
| 安徽建工 | construction | operate | 建筑施工运营商 | 0.95 |
| 安徽建工 | municipal_engineering | operate | 市政工程运营商 | 0.9 |
| 华丽家族 | equity_investment | operate | 股权投资运营商 | 0.95 |
| 华丽家族 | financial_service | provide_service | 金融服务商 | 0.85 |
| 西昌电力 | power_distribution | operate | 电力配供运营商 | 0.95 |
| 西昌电力 | power_supply | provide_service | 电力供应服务商 | 0.9 |
| 统一股份 | pear | produce | 香梨生产商 | 0.95 |
| 统一股份 | fruit | produce | 果品生产商 | 0.9 |
| 统一股份 | liquor | produce | 酒类生产商 | 0.85 |
| 方大特钢 | rebar | produce | 螺纹钢生产商 | 0.95 |
| 方大特钢 | leaf_spring | produce | 汽车板簧生产商 | 0.95 |
| 方大特钢 | spring_flat_steel | produce | 弹簧扁钢生产商 | 0.9 |
| 方大特钢 | iron_concentrate | produce | 铁精粉生产商 | 0.9 |
| 上海能源 | raw_coal | produce | 原煤生产商 | 0.95 |
| 上海能源 | coal_washing | operate | 选煤运营商 | 0.9 |
| 上海能源 | railway_transport | operate | 铁路运输运营商 | 0.85 |
| 天富能源 | power_generation | operate | 发电运营商 | 0.95 |
| 天富能源 | heating_supply | provide_service | 热力供应商 | 0.9 |
| 黑牡丹 | denim | produce | 牛仔布生产商 | 0.95 |
| 黑牡丹 | apparel | produce | 服装生产商 | 0.9 |
| 国药股份 | pharmaceutical_commerce | operate | 医药商业运营商 | 0.95 |
| 国药股份 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 腾达建设 | municipal_engineering | operate | 市政工程运营商 | 0.95 |
| 腾达建设 | highway_operation | operate | 公路运营运营商 | 0.9 |
| 腾达建设 | expressway | operate | 高速公路运营商 | 0.85 |

---

**Graph increment:** Nodes +8, Edges +3
