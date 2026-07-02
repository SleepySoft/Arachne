# Batch 056 Construction Log

**Date:** 2026-05-25
**Companies:** 600189.SH – 600201.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+10)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `mineral_water` | 天然矿泉水 | material |
| 2 | `timber` | 木材 | material |
| 3 | `landscape_service` | 园林景观服务 | service |
| 4 | `sugar` | 食糖 | material |
| 5 | `switchgear` | 开关设备 | device |
| 6 | `large_motor` | 大中型电机 | device |
| 7 | `decoration_engineering` | 装饰工程 | service |
| 8 | `veterinary_medicine` | 兽药 | material |
| 9 | `animal_feed` | 饲料 | material |
| 10 | `diagnostic_product` | 诊断产品 | device |
| 11 | `baijiu` | 白酒 | material |
| 12 | `communication_chip` | 通信芯片 | component |
| 13 | `veterinary_biological` | 兽用生物制品 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `sugar_to_food` | sugar → food | material_flow |
| 2 | `animal_feed_to_meat_product` | animal_feed → meat_product | material_flow |
| 3 | `timber_to_furniture` | timber → furniture | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `quanyangquan` | 吉林泉阳泉股份有限公司 | 600189.SH | 吉林 | 长春 |
| 2 | `huazi_industry` | 包头华资实业股份有限公司 | 600191.SH | 内蒙古 | 包头 |
| 3 | `greatwall_elec` | 兰州长城电工股份有限公司 | 600192.SH | 甘肃 | 兰州 |
| 4 | `st_chuangxing` | 上海创兴资源开发股份有限公司 | 600193.SH | 上海 | 上海 |
| 5 | `cahic` | 中牧实业股份有限公司 | 600195.SH | 北京 | 北京 |
| 6 | `fosun_pharma` | 上海复星医药(集团)股份有限公司 | 600196.SH | 上海 | 上海 |
| 7 | `yilite` | 新疆伊力特实业股份有限公司 | 600197.SH | 新疆 | 可克达拉 |
| 8 | `datang_telecom` | 大唐电信科技股份有限公司 | 600198.SH | 北京 | 北京 |
| 9 | `jinzhongzi` | 安徽金种子酒业股份有限公司 | 600199.SH | 安徽 | 阜阳 |
| 10 | `jinyu_bio` | 金宇生物技术股份有限公司 | 600201.SH | 内蒙古 | 呼和浩特 |

## 4. Company Node Exposures (+20)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 泉阳泉 | mineral_water | produce | 天然矿泉水生产商 | 0.9 |
| 泉阳泉 | timber | produce | 木材生产商 | 0.8 |
| 泉阳泉 | landscape_service | provide_service | 园林景观服务商 | 0.75 |
| 泉阳泉 | furniture | produce | 定制家居生产商 | 0.75 |
| 华资实业 | sugar | produce | 食糖生产商 | 0.9 |
| 华资实业 | food | produce | 食品生产商 | 0.8 |
| 长城电工 | switchgear | manufacture | 开关设备制造商 | 0.95 |
| 长城电工 | large_motor | manufacture | 大中型电机制造商 | 0.9 |
| 长城电工 | power_distribution_equipment | manufacture | 配电设备制造商 | 0.85 |
| ST创兴 | decoration_engineering | provide_service | 装饰工程承包商 | 0.9 |
| 中牧股份 | veterinary_medicine | produce | 兽药生产商 | 0.95 |
| 中牧股份 | animal_feed | produce | 饲料生产商 | 0.9 |
| 复星医药 | pharmaceutical | produce | 药品生产商 | 0.95 |
| 复星医药 | diagnostic_product | manufacture | 诊断产品制造商 | 0.85 |
| 伊力特 | baijiu | produce | 白酒生产商 | 0.95 |
| 大唐电信 | communication_chip | manufacture | 通信芯片制造商 | 0.9 |
| 大唐电信 | integrated_circuit | manufacture | 集成电路制造商 | 0.85 |
| 金种子酒 | baijiu | produce | 白酒生产商 | 0.95 |
| 生物股份 | veterinary_biological | produce | 兽用生物制品生产商 | 0.95 |
| 生物股份 | veterinary_medicine | produce | 兽药生产商 | 0.9 |

---

**Graph increment:** Nodes +10, Edges +3
