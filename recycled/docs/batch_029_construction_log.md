# Batch 029 Construction Log

**Date:** 2026-05-25
**Companies:** 000793.SZ – 000803.SZ (10 companies)
**Status:** ✅ Submitted successfully (1 edge error: referenced node not yet in graph)

---

## 1. New Industrial Nodes (+10)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `culture_tourism_service` | 文旅服务 | service |
| 2 | `micro_motor` | 微电机 | component |
| 3 | `marine_fishery` | 海洋渔业 | service |
| 4 | `aquatic_product` | 水产品 | material |
| 5 | `truck` | 重型卡车 | system |
| 6 | `broadcasting_equipment` | 广播电视设备 | device |
| 7 | `set_top_box` | 机顶盒 | device |
| 8 | `film_television` | 影视制作 | service |
| 9 | `cultural_entertainment` | 文化娱乐 | service |
| 10 | `organic_waste_treatment` | 有机废弃物处理 | service |

## 2. New Industrial Edges (+4, 1 error)

| # | Edge ID | From Node → To Node | Type | Status |
|---|---------|---------------------|------|--------|
| 1 | `flow_ndfeb_to_micro_motor` | ndfeb_magnet → micro_motor | composition | ❌ (ndfeb_magnet missing) |
| 2 | `flow_fishery_to_aquatic` | marine_fishery → aquatic_product | material_flow | ✅ |
| 3 | `flow_diesel_engine_to_truck` | diesel_engine → truck | composition | ✅ |
| 4 | `flow_broadcast_to_stb` | broadcasting_equipment → set_top_box | composition | ✅ |
| 5 | `flow_film_to_entertainment` | film_television → cultural_entertainment | service_flow | ✅ |

## 3. Companies Registered (+10 created)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `st_huawen` | 华闻传媒投资集团股份有限公司 | 000793.SZ | 海南 | 海口市 | 368 |
| 2 | `inovance` | 英洛华科技股份有限公司 | 000795.SZ | 浙江 | 金华市 | 3,781 |
| 3 | `caissa_tourism` | 凯撒同盛发展股份有限公司 | 000796.SZ | 海南 | 三亚市 | 1,298 |
| 4 | `china_wuyi` | 中国武夷实业股份有限公司 | 000797.SZ | 福建 | 福州市 | 2,994 |
| 5 | `cnfic` | 中水集团远洋股份有限公司 | 000798.SZ | 北京 | 北京市 | 792 |
| 6 | `jiuguijiu` | 酒鬼酒股份有限公司 | 000799.SZ | 湖南 | 湘西州 | 2,166 |
| 7 | `faw_jiefang` | 一汽解放集团股份有限公司 | 000800.SZ | 吉林 | 长春市 | 22,264 |
| 8 | `sichuan_jiuzhou` | 四川九洲电器股份有限公司 | 000801.SZ | 四川 | 绵阳市 | 2,155 |
| 9 | `bj_culture` | 北京京西文化旅游股份有限公司 | 000802.SZ | 北京 | 北京市 | 200 |
| 10 | `shandong_huanneng` | 山高环能集团股份有限公司 | 000803.SZ | 山东 | 济南市 | 1,143 |

## 4. Company Node Exposures (+18 created)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| *ST华闻 | media | operate | 文化传媒运营商 | 0.7 |
| *ST华闻 | culture_tourism_service | operate | 文旅服务运营商 | 0.8 |
| 英洛华 | ndfeb_magnet | produce | 钕铁硼磁材生产商 | 0.9 |
| 英洛华 | micro_motor | produce | 微电机生产商 | 0.8 |
| 凯撒旅业 | tourism_service | operate | 旅游服务运营商 | 0.9 |
| 中国武夷 | construction_service | operate | 建筑工程承包商 | 0.9 |
| 中国武夷 | real_estate_development | operate | 房地产开发商 | 0.8 |
| 中水渔业 | marine_fishery | operate | 远洋渔业运营商 | 0.9 |
| 中水渔业 | aquatic_product | produce | 水产品生产商 | 0.8 |
| 酒鬼酒 | liquor | produce | 白酒生产商 | 0.9 |
| 一汽解放 | truck | manufacture | 重型卡车制造商 | 0.9 |
| 一汽解放 | commercial_vehicle | manufacture | 商用车制造商 | 0.8 |
| 四川九洲 | broadcasting_equipment | manufacture | 广播电视设备制造商 | 0.8 |
| 四川九洲 | set_top_box | manufacture | 机顶盒制造商 | 0.8 |
| 北京文化 | film_television | operate | 影视制作运营商 | 0.9 |
| 北京文化 | cultural_entertainment | operate | 文化娱乐运营商 | 0.8 |
| 山高环能 | municipal_waste_treatment | operate | 城市废弃物处理运营商 | 0.8 |
| 山高环能 | organic_waste_treatment | operate | 有机废弃物处理运营商 | 0.9 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_029_graph",
    "status": 201,
    "nodes_created": 10,
    "nodes_updated": 0,
    "edges_created": 4,
    "edges_updated": 0,
    "errors": [
      {"type": "edge", "id": "flow_ndfeb_to_micro_motor", "error": "'NoneType' object is not subscriptable"}
    ]
  },
  "business_batch": {
    "batch_id": "batch_029_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 18,
    "exposures_updated": 0,
    "errors": []
  }
}
```

## 6. Design Notes

- **英洛华** 是稀土永磁材料和微电机双主业企业。计划构建 `ndfeb_magnet` → `micro_motor` 的 composition 边，但 `ndfeb_magnet` 节点尚未创建（应为 `ndfeb` 或类似 ID），后续批次补充创建该节点后可重新提交此边。
- **一汽解放** 是中国最大的商用车企业，新增 `truck`（重型卡车）节点，与已有 `diesel_engine` 形成 composition 关系（柴油发动机→重卡），是商用车产业链的典型动力匹配模式。
- **四川九洲** 构建 `broadcasting_equipment` → `set_top_box` 的 composition 关系，体现了广电设备从系统到终端的层级结构。与 batch 028 的创维数字共同丰富了数字电视/智能终端节点生态。
- **北京文化** 构建 `film_television` → `cultural_entertainment` 的 service_flow，展示了影视内容作为文化娱乐产业核心产出的产业逻辑。
- **山高环能** 是有机固废处理领域的领先企业，暴露到 `municipal_waste_treatment` 和新增的 `organic_waste_treatment`，与 batch 022 的军信环保形成同业映射。
- **中水渔业** 是A股唯一远洋渔业上市公司，新增 `marine_fishery` → `aquatic_product` 的 material_flow，构建从捕捞到加工的水产产业链。

---

**Total Graph after Batch 029:**
- Nodes: 554 (544 + 10)
- Edges: 434 (430 + 4)
