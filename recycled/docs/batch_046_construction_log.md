# Batch 046 Construction Log

**Date:** 2026-05-25
**Companies:** 600058.SH – 600071.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+5)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `shaoxing_wine` | 绍兴黄酒 | material |
| 2 | `injection` | 注射剂 | material |
| 3 | `pva_fiber` | PVA纤维 | material |
| 4 | `enamelled_wire` | 漆包线 | material |
| 5 | `optical_lens` | 光学镜片 | component |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `pva_fiber_to_cement` | pva_fiber → cement | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `minmetals_dev` | 五矿发展股份有限公司 | 600058.SH | 北京 | 北京 |
| 2 | `guyuelongshan` | 浙江古越龙山绍兴酒股份有限公司 | 600059.SH | 浙江 | 绍兴 |
| 3 | `hisense_visual` | 海信视像科技股份有限公司 | 600060.SH | 山东 | 青岛 |
| 4 | `sdic_capital` | 国投资本股份有限公司 | 600061.SH | 上海 | 上海 |
| 5 | `cr_double_crane` | 华润双鹤药业股份有限公司 | 600062.SH | 北京 | 北京 |
| 6 | `wanwei` | 安徽皖维高新材料股份有限公司 | 600063.SH | 安徽 | 巢湖 |
| 7 | `nanjing_gaoke` | 南京高科股份有限公司 | 600064.SH | 江苏 | 南京 |
| 8 | `yutong_bus` | 宇通客车股份有限公司 | 600066.SH | 河南 | 郑州 |
| 9 | `guancheng` | 冠城新材料股份有限公司 | 600067.SH | 福建 | 福州 |
| 10 | `phoenix_optical` | 凤凰光学股份有限公司 | 600071.SH | 江西 | 上饶 |

## 4. Company Node Exposures (+11)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 五矿发展 | steel_plate | procure | 钢材贸易商 | 0.9 |
| 古越龙山 | shaoxing_wine | produce | 绍兴黄酒生产商 | 0.95 |
| 海信视像 | color_tv | manufacture | 电视机制造商 | 0.95 |
| 国投资本 | securities_service | provide_service | 综合金融服务商 | 0.85 |
| 华润双鹤 | injection | produce | 注射剂生产商 | 0.9 |
| 皖维高新 | pva_fiber | produce | PVA纤维生产商 | 0.9 |
| 皖维高新 | cement | produce | 水泥生产商 | 0.8 |
| 南京高科 | real_estate_development | operate | 园区开发及房地产运营商 | 0.85 |
| 宇通客车 | bus | manufacture | 客车制造商 | 0.95 |
| 冠城新材 | enamelled_wire | produce | 漆包线生产商 | 0.9 |
| 凤凰光学 | optical_lens | manufacture | 光学镜片及镜头制造商 | 0.9 |

---

**Graph increment:** Nodes +5, Edges +1
