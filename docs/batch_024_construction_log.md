# Batch 024 Construction Log

**Date:** 2026-05-25  
**Companies:** 000712.SZ – 000722.SZ (10 companies)  
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+11)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `rice_seed` | 水稻种子 | material |
| 2 | `corn_seed` | 玉米种子 | material |
| 3 | `seed_production` | 种子生产 | service |
| 4 | `black_sesame_product` | 黑芝麻食品 | material |
| 5 | `sesame_beverage` | 芝麻饮料 | material |
| 6 | `news_media_service` | 新闻媒体服务 | service |
| 7 | `publishing_service` | 出版服务 | service |
| 8 | `cultural_industry_service` | 文化产业服务 | service |
| 9 | `industrial_park_operation` | 产业园运营 | service |
| 10 | `catering_service` | 餐饮服务 | service |
| 11 | `industrial_food` | 工业化食品 | material |
| 12 | `medical_elderly_care_service` | 医疗养老服务 | service |

## 2. New Industrial Edges (+9)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_seed_production_to_rice` | seed_production → rice_seed | service_flow |
| 2 | `flow_seed_production_to_corn` | seed_production → corn_seed | service_flow |
| 3 | `flow_sesame_to_black_sesame` | grain_oil → black_sesame_product | material_flow |
| 4 | `flow_sesame_to_beverage` | grain_oil → sesame_beverage | material_flow |
| 5 | `flow_publishing_to_culture` | publishing_service → cultural_industry_service | service_flow |
| 6 | `flow_news_to_culture` | news_media_service → cultural_industry_service | service_flow |
| 7 | `flow_industrial_park_to_zone_dev` | industrial_park_operation → industrial_zone_development | service_flow |
| 8 | `flow_catering_to_industrial_food` | catering_service → industrial_food | service_flow |
| 9 | `flow_medical_to_elderly_care` | medical_service → medical_elderly_care_service | service_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `jinlong_share` | 广东锦龙发展股份有限公司 | 000712.SZ | 广东 | 东莞市 | 1,237 |
| 2 | `guotou_fengle` | 国投丰乐种业股份有限公司 | 000713.SZ | 安徽 | 合肥市 | 1,461 |
| 3 | `zhongxing_commercial` | 中兴-沈阳商业大厦(集团)股份有限公司 | 000715.SZ | 辽宁 | 沈阳市 | 1,031 |
| 4 | `black_sesame_group` | 南方黑芝麻集团股份有限公司 | 000716.SZ | 广西 | 玉林市 | 1,623 |
| 5 | `zhongnan_steel` | 广东中南钢铁股份有限公司 | 000717.SZ | 广东 | 韶关市 | 5,155 |
| 6 | `suning_global` | 苏宁环球股份有限公司 | 000718.SZ | 吉林 | 吉林市 | 935 |
| 7 | `zhongyuan_media` | 中原大地传媒股份有限公司 | 000719.SZ | 河南 | 焦作市 | 12,774 |
| 8 | `xinneng_taishan` | 山东新能泰山发电股份有限公司 | 000720.SZ | 山东 | 泰安市 | 637 |
| 9 | `xian_catering` | 西安饮食股份有限公司 | 000721.SZ | 陕西 | 西安市 | 3,106 |
| 10 | `hunan_development` | 湖南能源集团发展股份有限公司 | 000722.SZ | 湖南 | 长沙市 | 196 |

## 4. Company Node Exposures (+27)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 锦龙股份 | securities_brokerage | operate | 证券经纪服务商 | 0.8 |
| 锦龙股份 | securities_underwriting | operate | 证券承销与保荐服务商 | 0.7 |
| 国投丰乐 | rice_seed | produce | 水稻种子生产商 | 0.9 |
| 国投丰乐 | corn_seed | produce | 玉米种子生产商 | 0.9 |
| 国投丰乐 | seed_production | operate | 种子生产服务商 | 0.9 |
| 国投丰乐 | pesticide | produce | 农化产品生产商 | 0.6 |
| 中兴商业 | department_store | operate | 百货零售商 | 0.9 |
| 黑芝麻 | black_sesame_product | produce | 黑芝麻食品生产商 | 0.9 |
| 黑芝麻 | sesame_beverage | produce | 芝麻饮料生产商 | 0.8 |
| 黑芝麻 | grain_oil | produce | 粮油食品生产商 | 0.6 |
| 中南股份 | steel_plate | produce | 板材生产商 | 0.9 |
| 中南股份 | steel_wire_rod | produce | 线材生产商 | 0.8 |
| 中南股份 | steel_bar | produce | 棒材生产商 | 0.8 |
| 苏宁环球 | real_estate_development | operate | 房地产开发商 | 0.9 |
| 苏宁环球 | ready_mixed_concrete | produce | 商品混凝土生产商 | 0.6 |
| 中原传媒 | news_media_service | operate | 新闻媒体运营商 | 0.8 |
| 中原传媒 | publishing_service | operate | 出版服务商 | 0.9 |
| 中原传媒 | cultural_industry_service | operate | 文化产业运营商 | 0.8 |
| 中原传媒 | education_service | operate | 教育产业运营商 | 0.6 |
| 新能泰山 | industrial_park_operation | operate | 产业园运营商 | 0.8 |
| 新能泰山 | wire_cable | manufacture | 电线电缆制造商 | 0.8 |
| 新能泰山 | industrial_zone_development | operate | 工业区开发商 | 0.5 |
| 西安饮食 | catering_service | operate | 餐饮服务商 | 0.9 |
| 西安饮食 | industrial_food | produce | 工业化食品生产商 | 0.7 |
| 湖南发展 | hydro_power_generation | operate | 水力发电运营商 | 0.9 |
| 湖南发展 | medical_service | operate | 医疗服务运营商 | 0.7 |
| 湖南发展 | medical_elderly_care_service | operate | 医养结合服务商 | 0.7 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_024_graph",
    "status": 201,
    "nodes_created": 11,
    "nodes_updated": 1,
    "edges_created": 9,
    "edges_updated": 0
  },
  "business_batch": {
    "batch_id": "batch_024_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 27,
    "exposures_updated": 0
  }
}
```

## 6. Design Notes

- **国投丰乐** 构建了种子产业链的完整表达：`seed_production`（种子生产服务）→ `rice_seed`/`corn_seed`（种子产品），同时关联已有的 `pesticide`（农药）节点，体现了种业与农化的协同。
- **中原传媒** 构建了文化传媒产业的服务层级：`news_media_service` 和 `publishing_service` 作为子服务，通过 service_flow 汇入 `cultural_industry_service`，展示了文化产业的聚合结构。
- **黑芝麻** 以 `grain_oil`（粮油）为上游原料节点，分化为 `black_sesame_product` 和 `sesame_beverage` 两条产品线，体现了农产品深加工的价值链延伸。
- **西安饮食** 的"餐饮+工业化食品"模式通过 `catering_service` → `industrial_food` 的 service_flow 边表达，揭示了传统餐饮企业向食品工业转型的路径。
- **湖南发展** 的水电+医养结合模式体现了公用事业企业向大健康领域的多元化拓展。`medical_service` → `medical_elderly_care_service` 的 service_flow 边反映了医疗与养老的融合趋势。

---

**Total Graph after Batch 024:**
- Nodes: 503 (492 + 11)
- Edges: 408 (399 + 9)
