# Batch 043 Construction Log

**Date:** 2026-05-25
**Companies:** 600007.SH – 600020.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+3)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `office_building` | 写字楼 | infrastructure |
| 2 | `rare_earth_steel` | 稀土钢 | material |
| 3 | `waste_incineration` | 垃圾焚烧 | service |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `rare_earth_to_steel` | rare_earth_steel → steel_plate | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `china_world` | 中国国际贸易中心股份有限公司 | 600007.SH | 北京 | 北京 |
| 2 | `capital_env` | 北京首创生态环保集团股份有限公司 | 600008.SH | 北京 | 北京 |
| 3 | `shanghai_airport` | 上海国际机场股份有限公司 | 600009.SH | 上海 | 上海 |
| 4 | `baotou_steel` | 内蒙古包钢钢联股份有限公司 | 600010.SH | 内蒙古 | 包头 |
| 5 | `huaneng_power` | 华能国际电力股份有限公司 | 600011.SH | 北京 | 北京 |
| 6 | `wantong_highway` | 安徽皖通高速公路股份有限公司 | 600012.SH | 安徽 | 合肥 |
| 7 | `huaxia_bank` | 华夏银行股份有限公司 | 600015.SH | 北京 | 北京 |
| 8 | `minsheng_bank` | 中国民生银行股份有限公司 | 600016.SH | 北京 | 北京 |
| 9 | `baosteel` | 宝山钢铁股份有限公司 | 600019.SH | 上海 | 上海 |
| 10 | `zhongyuan_highway` | 河南中原高速公路股份有限公司 | 600020.SH | 河南 | 郑州 |

## 4. Company Node Exposures (+12)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 中国国贸 | office_building | operate | 写字楼物业运营商 | 0.9 |
| 首创环保 | waste_water_treatment | operate | 污水处理运营商 | 0.9 |
| 首创环保 | waste_incineration | operate | 固废处理运营商 | 0.85 |
| 上海机场 | airport_operation_service | operate | 机场运营商 | 0.95 |
| 包钢股份 | rare_earth_steel | produce | 稀土钢生产商 | 0.9 |
| 包钢股份 | steel_plate | produce | 板材生产商 | 0.85 |
| 华能国际 | coal_power_generation | operate | 火电运营商 | 0.95 |
| 皖通高速 | highway_operation_service | operate | 高速公路运营商 | 0.9 |
| 华夏银行 | banking_service | provide_service | 商业银行 | 0.95 |
| 民生银行 | banking_service | provide_service | 商业银行 | 0.95 |
| 宝钢股份 | steel_plate | produce | 综合钢铁生产商 | 0.95 |
| 中原高速 | highway_operation_service | operate | 高速公路运营商 | 0.9 |

---

**Graph increment:** Nodes +3, Edges +1
