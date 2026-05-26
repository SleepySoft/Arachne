# Batch 044 Construction Log

**Date:** 2026-05-25
**Companies:** 600021.SH – 600037.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+5)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `oil_tanker` | 油轮 | device |
| 2 | `lubricant` | 润滑油 | material |
| 3 | `concrete_machinery` | 混凝土机械 | device |
| 4 | `road_paver` | 摊铺机 | device |
| 5 | `securities_service` | 证券服务 | service |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `crude_oil_to_gasoline` | crude_oil → gasoline | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `shanghai_electric_power` | 上海电力股份有限公司 | 600021.SH | 上海 | 上海 |
| 2 | `cosco_shipping_energy` | 中远海运能源运输股份有限公司 | 600026.SH | 上海 | 上海 |
| 3 | `sinopec` | 中国石油化工股份有限公司 | 600028.SH | 北京 | 北京 |
| 4 | `china_southern_airlines` | 中国南方航空股份有限公司 | 600029.SH | 广东 | 广州 |
| 5 | `citic_securities` | 中信证券股份有限公司 | 600030.SH | 广东 | 深圳 |
| 6 | `sany_heavy` | 三一重工股份有限公司 | 600031.SH | 湖南 | 长沙 |
| 7 | `fujian_highway` | 福建发展高速公路股份有限公司 | 600033.SH | 福建 | 福州 |
| 8 | `chutian_highway` | 湖北楚天智能交通股份有限公司 | 600035.SH | 湖北 | 武汉 |
| 9 | `cmb` | 招商银行股份有限公司 | 600036.SH | 广东 | 深圳 |
| 10 | `gehua` | 北京歌华有线电视网络股份有限公司 | 600037.SH | 北京 | 北京 |

## 4. Company Node Exposures (+14)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 上海电力 | coal_power_generation | operate | 火电及分布式能源运营商 | 0.9 |
| 中远海能 | oil_tanker | operate | 油轮运输运营商 | 0.95 |
| 中国石化 | gasoline | produce | 汽油生产商 | 0.95 |
| 中国石化 | lubricant | produce | 润滑油生产商 | 0.9 |
| 中国石化 | synthetic_resin | produce | 合成树脂生产商 | 0.85 |
| 南方航空 | air_transport_service | operate | 航空运输运营商 | 0.95 |
| 中信证券 | securities_service | provide_service | 综合证券服务商 | 0.95 |
| 三一重工 | concrete_machinery | manufacture | 混凝土机械制造商 | 0.95 |
| 三一重工 | excavator | manufacture | 挖掘机械制造商 | 0.9 |
| 三一重工 | road_paver | manufacture | 摊铺机制造商 | 0.8 |
| 福建高速 | highway_operation_service | operate | 高速公路运营商 | 0.9 |
| 楚天高速 | highway_operation_service | operate | 高速公路运营商 | 0.9 |
| 招商银行 | banking_service | provide_service | 商业银行 | 0.95 |
| 歌华有线 | cable_tv_network_service | operate | 有线电视网络运营商 | 0.9 |

---

**Graph increment:** Nodes +5, Edges +1
