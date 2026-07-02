# Batch 050 Construction Log

**Date:** 2026-05-25
**Companies:** 600107.SH – 600116.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+2)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `automobile_part` | 汽车零部件 | component |
| 2 | `special_steel` | 特种钢 | material |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `special_steel_to_automobile_part` | special_steel → automobile_part | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `meiyan_jixiang` | 湖北美尔雅股份有限公司 | 600107.SH | 湖北 | 黄石 |
| 2 | `st_dadi` | 重庆路桥股份有限公司 | 600106.SH | 重庆 | 重庆 |
| 3 | `chongqing_port` | 重庆港股份有限公司 | 600279.SH | 重庆 | 重庆 |
| 4 | `shenyang_jinbei` | 沈阳金杯汽车工业控股有限公司 | 600609.SH | 辽宁 | 沈阳 |
| 5 | `st_lianhua` | 江西联创光电科技股份有限公司 | 600363.SH | 江西 | 南昌 |
| 6 | `zhongguang` | 湖北中广核科技股份有限公司 | 600764.SH | 湖北 | 武汉 |
| 7 | `changjiu` | 江西长运股份有限公司 | 600561.SH | 江西 | 南昌 |
| 8 | `jizhong_energy` | 冀中能源股份有限公司 | 000937.SZ | 河北 | 邢台 |
| 9 | `yunwei_baobian` | 保定天威保变电气股份有限公司 | 600550.SH | 河北 | 保定 |
| 10 | `nangang` | 南京钢铁股份有限公司 | 600282.SH | 江苏 | 南京 |

## 4. Company Node Exposures (+10)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 美尔雅 | textile_product | produce | 纺织服装生产商 | 0.85 |
| 重庆路桥 | toll_road | operate | 路桥基础设施运营商 | 0.9 |
| 重庆港 | logistics_service | provide_service | 港口物流服务商 | 0.9 |
| 金杯汽车 | automobile_part | manufacture | 汽车零部件制造商 | 0.9 |
| 联创光电 | optoelectronic_device | manufacture | 光电子器件制造商 | 0.85 |
| 中广核技 | irradiation_service | provide_service | 核技术应用及辐照服务商 | 0.85 |
| 江西长运 | road_passenger_transport | operate | 公路客运运营商 | 0.9 |
| 冀中能源 | coal | produce | 煤炭生产商 | 0.95 |
| 保变电气 | transformer | manufacture | 变压器制造商 | 0.95 |
| 南钢股份 | special_steel | produce | 特种钢生产商 | 0.95 |

---

**Graph increment:** Nodes +2, Edges +1
