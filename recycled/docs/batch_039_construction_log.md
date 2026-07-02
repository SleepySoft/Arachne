# Batch 039 Construction Log

**Date:** 2026-05-25
**Companies:** 000950.SZ – 000962.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+4)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `riboflavin` | 核黄素 | material |
| 2 | `non_woven_fabric` | 无纺布 | material |
| 3 | `tin_ingot` | 锡锭 | material |
| 4 | `titanium_product` | 钛产品 | material |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `tin_metal_to_tin_ingot` | tin_metal → tin_ingot | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `chongqing_pharma` | 重药控股股份有限公司 | 000950.SZ | 重庆 | 重庆 |
| 2 | `cnhtc` | 中国重汽集团济南卡车股份有限公司 | 000951.SZ | 山东 | 济南 |
| 3 | `guangji_pharma` | 湖北广济药业股份有限公司 | 000952.SZ | 湖北 | 武穴 |
| 4 | `hehua` | 广西河池化工股份有限公司 | 000953.SZ | 广西 | 河池 |
| 5 | `xinlong` | 欣龙控股(集团)股份有限公司 | 000955.SZ | 海南 | 海口 |
| 6 | `zhongtong_bus` | 中通客车股份有限公司 | 000957.SZ | 山东 | 聊城 |
| 7 | `spic_financial` | 国家电投集团东方新能源股份有限公司 | 000958.SZ | 河北 | 石家庄 |
| 8 | `shougang_steel` | 北京首钢股份有限公司 | 000959.SZ | 北京 | 北京 |
| 9 | `ytc` | 云南锡业股份有限公司 | 000960.SZ | 云南 | 昆明 |
| 10 | `orient_tantalum` | 宁夏东方钽业股份有限公司 | 000962.SZ | 宁夏 | 石嘴山 |

## 4. Company Node Exposures (+12)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 重药控股 | pharmaceutical_distribution | provide_service | 医药流通服务商 | 0.95 |
| 中国重汽 | truck | manufacture | 载重汽车制造商 | 0.9 |
| 中国重汽 | bus | manufacture | 客车底盘制造商 | 0.75 |
| 广济药业 | riboflavin | produce | 核黄素生产商 | 0.95 |
| 河化股份 | urea | produce | 尿素生产商 | 0.9 |
| 欣龙控股 | non_woven_fabric | produce | 无纺布生产商 | 0.9 |
| 中通客车 | bus | manufacture | 客车制造商 | 0.95 |
| 电投产融 | coal_power_generation | operate | 火电运营商 | 0.85 |
| 首钢股份 | steel_plate | produce | 钢材生产商 | 0.9 |
| 锡业股份 | tin_ingot | produce | 锡锭生产商 | 0.95 |
| 东方钽业 | tantalum | produce | 钽金属制品生产商 | 0.9 |
| 东方钽业 | titanium_product | produce | 钛产品生产商 | 0.75 |

---

**Graph increment:** Nodes +4, Edges +1
