# Batch 047 Construction Log

**Date:** 2026-05-25
**Companies:** 600072.SH – 600084.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `canned_food` | 罐头食品 | material |
| 2 | `chlor_alkali_product` | 氯碱化工产品 | material |
| 3 | `container_floor` | 集装箱底板 | component |
| 4 | `phosphorus_chemical` | 磷化工产品 | material |
| 5 | `anesthetic_product` | 麻醉药品 | material |
| 6 | `ship_accessory` | 船舶配件 | component |

## 2. New Industrial Edges (+1)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `phosphorus_chemical_to_fertilizer` | phosphorus_chemical → chemical_fertilizer | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `cssc_tech` | 中船科技股份有限公司 | 600072.SH | 上海 | 上海 |
| 2 | `bright_meat` | 上海光明肉业集团股份有限公司 | 600073.SH | 上海 | 上海 |
| 3 | `xinjiang_tianye` | 新疆天业股份有限公司 | 600075.SH | 新疆 | 石河子 |
| 4 | `kangxin` | 康欣新材料科技股份有限公司 | 600076.SH | 湖北 | 孝感 |
| 5 | `chengxing` | 江苏澄星磷化工股份有限公司 | 600078.SH | 江苏 | 江阴 |
| 6 | `st_renfu` | 人福医药集团股份公司 | 600079.SH | 湖北 | 武汉 |
| 7 | `st_jinhua` | 金花企业(集团)股份有限公司 | 600080.SH | 陕西 | 西安 |
| 8 | `dongfeng_tech` | 东风电子科技股份有限公司 | 600081.SH | 湖北 | 武汉 |
| 9 | `st_haitai` | 天津海泰科技发展股份有限公司 | 600082.SH | 天津 | 天津 |
| 10 | `st_niya` | 中信国安葡萄酒业股份有限公司 | 600084.SH | 新疆 | 伊犁 |

## 4. Company Node Exposures (+11)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 中船科技 | ship_accessory | manufacture | 船舶配件制造商 | 0.8 |
| 光明肉业 | canned_food | produce | 罐头食品生产商 | 0.85 |
| 光明肉业 | meat_product | produce | 肉类产品生产商 | 0.9 |
| 新疆天业 | chlor_alkali_product | produce | 氯碱化工产品生产商 | 0.9 |
| 康欣新材 | container_floor | manufacture | 集装箱底板制造商 | 0.9 |
| 澄星股份 | phosphorus_chemical | produce | 磷化工产品生产商 | 0.95 |
| 人福医药 | anesthetic_product | produce | 麻醉药品生产商 | 0.9 |
| ST金花 | chinese_patent_medicine | produce | 中成药生产商 | 0.85 |
| 东风科技 | automotive_electronics | manufacture | 汽车电子及零部件制造商 | 0.9 |
| ST海泰 | real_estate_development | operate | 园区开发运营商 | 0.85 |
| *ST尼雅 | wine | produce | 葡萄酒生产商 | 0.9 |

---

**Graph increment:** Nodes +6, Edges +1
