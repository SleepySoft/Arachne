# Batch 036 Construction Log

**Date:** 2026-05-25
**Companies:** 000905.SZ – 000917.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+3)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `wood_floor` | 木地板 | component |
| 2 | `motorcycle` | 摩托车整车 | device |
| 3 | `mechanism_paper` | 机制纸 | material |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `artificial_board_to_wood_floor` | artificial_board → wood_floor | composition |
| 2 | `bagasse_pulp_to_mechanism_paper` | bagasse_pulp → mechanism_paper | material_flow |
| 3 | `motorcycle_engine_to_motorcycle` | motorcycle_engine → motorcycle | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `xiamen_port` | 厦门港务发展股份有限公司 | 000905.SZ | 福建 | 厦门 | 4,631 |
| 2 | `zheshang_zhongtuo` | 浙商中拓集团股份有限公司 | 000906.SZ | 浙江 | 杭州 | 2,408 |
| 3 | `st_jingfeng` | 石药集团湖南景峰医药股份有限公司 | 000908.SZ | 湖南 | 常德 | 547 |
| 4 | `st_shuyuan` | 数源科技股份有限公司 | 000909.SZ | 浙江 | 杭州 | 353 |
| 5 | `dare_power` | 大亚圣象家居股份有限公司 | 000910.SZ | 江苏 | 镇江 | 5,064 |
| 6 | `st_guangtang` | 广西农投糖业集团股份有限公司 | 000911.SZ | 广西 | 南宁 | 2,603 |
| 7 | `lutianhua` | 四川泸天化股份有限公司 | 000912.SZ | 四川 | 泸州 | 2,869 |
| 8 | `qianjiang_motor` | 浙江钱江摩托股份有限公司 | 000913.SZ | 浙江 | 台州 | 5,602 |
| 9 | `huatiedayin` | 山东华特达因健康股份有限公司 | 000915.SZ | 山东 | 临沂 | 1,759 |
| 10 | `dian_guang_media` | 湖南电广传媒股份有限公司 | 000917.SZ | 湖南 | 长沙 | 2,383 |

## 4. Company Node Exposures (+16)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 厦门港务 | port_operation_service | operate | 港口运营服务商 | 0.9 |
| 浙商中拓 | logistics_service | provide_service | 供应链及物流服务商 | 0.85 |
| ST景峰 | chemical_drug | produce | 化学药品生产商 | 0.9 |
| ST景峰 | pharmaceutical_product | produce | 医药产品制造商 | 0.85 |
| *ST数源 | color_tv | manufacture | 彩色电视机制造商 | 0.8 |
| 大亚圣象 | wood_floor | manufacture | 木地板制造商 | 0.9 |
| 大亚圣象 | artificial_board | manufacture | 人造板制造商 | 0.85 |
| *ST广糖 | white_sugar | produce | 白砂糖生产商 | 0.9 |
| *ST广糖 | mechanism_paper | produce | 机制纸生产商 | 0.75 |
| 泸天化 | urea | produce | 尿素生产商 | 0.95 |
| 泸天化 | chemical_fertilizer | produce | 化肥生产商 | 0.85 |
| 钱江摩托 | motorcycle | manufacture | 摩托车整车制造商 | 0.9 |
| 钱江摩托 | motorcycle_engine | manufacture | 摩托车发动机制造商 | 0.85 |
| 华特达因 | chemical_drug | produce | 化学药品生产商 | 0.8 |
| 电广传媒 | film_television | operate | 影视内容制作运营商 | 0.85 |
| 电广传媒 | advertising_service | provide_service | 广告服务提供商 | 0.8 |

---

**Total Graph after Batch 036:**
- Nodes: 606 (603 + 3)
- Edges: 464 (461 + 3)
- Companies: 10 registered
