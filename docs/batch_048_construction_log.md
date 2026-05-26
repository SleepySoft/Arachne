# Batch 048 Construction Log

**Date:** 2026-05-25
**Companies:** 600085.SH – 600094.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+4)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `herb_medicine` | 中草药 | material |
| 2 | `petroleum_product` | 石油制品 | material |
| 3 | `electric_vessel` | 电动船 | system |
| 4 | `aerospace_metal` | 航空航天金属 | material |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `aerospace_metal_to_aircraft` | aerospace_metal → aircraft | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `tongrentang` | 北京同仁堂股份有限公司 | 600085.SH | 北京 | 北京 |
| 2 | `orient_elec` | 东方电气股份有限公司 | 600086.SH | 四川 | 成都 |
| 3 | *ST美亿 | 新疆美亿家股份有限公司 | 600088.SH | 新疆 | 乌鲁木齐 |
| 4 | `tongfang` | 同方股份有限公司 | 600100.SH | 北京 | 北京 |
| 5 | `shentong_metro` | 上海申通地铁股份有限公司 | 600834.SH | 上海 | 上海 |
| 6 | `jiangxi_guotai` | 江西国泰集团股份有限公司 | 603977.SH | 江西 | 南昌 |
| 7 | `st_xintai` | 上海新泰科技集团股份有限公司 | 600728.SH | 上海 | 上海 |
| 8 | `st_zhongji` | 中基健康股份有限公司 | 600972.SH | 新疆 | 乌鲁木齐 |
| 9 | `csic_power` | 中国船舶重工集团动力股份有限公司 | 600482.SH | 北京 | 北京 |
| 10 | `bgi` | 华大基因股份有限公司 | 300676.SZ | 广东 | 深圳 |

## 4. Company Node Exposures (+12)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 同仁堂 | herb_medicine | procure | 中草药采购商 | 0.85 |
| 同仁堂 | chinese_patent_medicine | produce | 中成药生产商 | 0.95 |
| 东方电气 | power_generation_equipment | manufacture | 发电设备制造商 | 0.95 |
| *ST美亿 | petroleum_product | trade | 石油制品贸易商 | 0.9 |
| 同方股份 | computer_hardware | manufacture | 计算机硬件制造商 | 0.85 |
| 同方股份 | software_system | provide_service | 软件及IT服务商 | 0.8 |
| 申通地铁 | rail_transit | operate | 城市轨道交通运营商 | 0.95 |
| 国泰集团 | explosives | manufacture | 民用爆破器材制造商 | 0.9 |
| ST新泰 | semiconductor_device | manufacture | 半导体器件制造商 | 0.85 |
| ST中基 | tomato_product | produce | 番茄制品生产商 | 0.9 |
| 中国动力 | electric_vessel | manufacture | 电动船制造商 | 0.85 |
| 华大基因 | biotech_service | provide_service | 基因测序及生物技术服务商 | 0.95 |

---

**Graph increment:** Nodes +4, Edges +1
