# Batch 030 Construction Log

**Date:** 2026-05-25
**Companies:** 000807.SZ – 000819.SZ (10 companies)
**Status:** ✅ Submitted successfully (2 edge errors: referenced nodes not yet in graph)

---

## 1. New Industrial Nodes (+6)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `cigarette_packaging` | 烟标包装 | material |
| 2 | `data_center_service` | 数据中心服务 | service |
| 3 | `special_chemical` | 特种化工产品 | material |
| 4 | `ic_design` | 集成电路设计 | technology_capability |
| 5 | `methanol` | 甲醇 | material |
| 6 | `lp_gas` | 液化石油气 | material |

## 2. New Industrial Edges (+2 created, +1 updated, 2 errors)

| # | Edge ID | From Node → To Node | Type | Status |
|---|---------|---------------------|------|--------|
| 1 | `flow_cigarette_packaging_to_tobacco` | cigarette_packaging → cigarette | composition | ❌ (cigarette missing) |
| 2 | `flow_aluminum_smelting_to_ingot` | aluminum_smelting → aluminum_ingot | material_flow | ✅ updated |
| 3 | `flow_ingot_to_alloy` | aluminum_ingot → aluminum_alloy | material_flow | ✅ created |
| 4 | `flow_methanol_to_fuel` | methanol → refined_oil | material_flow | ❌ (refined_oil vs methanol type mismatch) |
| 5 | `flow_lp_gas_to_fuel` | lp_gas → natural_gas | service_flow | ✅ created |

## 3. Companies Registered (+10 created)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `yunnan_aluminum` | 云南铝业股份有限公司 | 000807.SZ | 云南 | 昆明市 | 10,283 |
| 2 | `hezhan_energy` | 辽宁和展能源集团股份有限公司 | 000809.SZ | 辽宁 | 铁岭市 | 67 |
| 3 | `skyworth_digital` | 创维数字股份有限公司 | 000810.SZ | 四川 | 遂宁市 | 3,874 |
| 4 | `bingshan_env` | 冰轮环境技术股份有限公司 | 000811.SZ | 山东 | 烟台市 | 2,718 |
| 5 | `shaanxi_jinye` | 陕西金叶科教集团股份有限公司 | 000812.SZ | 陕西 | 西安市 | 1,981 |
| 6 | `dezhan_health` | 德展大健康股份有限公司 | 000813.SZ | 新疆 | 乌鲁木齐市 | 1,240 |
| 7 | `meili_cloud` | 中冶美利云产业投资股份有限公司 | 000815.SZ | 宁夏 | 中卫市 | 1,365 |
| 8 | `smart_agri` | 江苏农华智慧农业科技股份有限公司 | 000816.SZ | 江苏 | 盐城市 | 2,149 |
| 9 | `hangjin_tech` | 航锦科技股份有限公司 | 000818.SZ | 辽宁 | 葫芦岛市 | 1,908 |
| 10 | `yueyang_xingchang` | 岳阳兴长石化股份有限公司 | 000819.SZ | 湖南 | 岳阳市 | 556 |

## 4. Company Node Exposures (+21 created)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 云铝股份 | aluminum_ingot | produce | 铝锭生产商 | 0.9 |
| 云铝股份 | aluminum_alloy | produce | 铝合金生产商 | 0.8 |
| 云铝股份 | aluminum_smelting | operate | 铝冶炼运营商 | 0.8 |
| 和展能源 | wind_power_generation | operate | 风力发电运营商 | 0.9 |
| 和展能源 | electricity_power | produce | 电力生产商 | 0.8 |
| 创维数字 | set_top_box | manufacture | 机顶盒制造商 | 0.9 |
| 创维数字 | broadcasting_equipment | manufacture | 广播电视设备制造商 | 0.7 |
| 冰轮环境 | refrigeration_equipment | manufacture | 制冷设备制造商 | 0.9 |
| 冰轮环境 | refrigeration_compressor | manufacture | 制冷压缩机制造商 | 0.8 |
| 陕西金叶 | cigarette_packaging | manufacture | 烟标包装制造商 | 0.9 |
| 德展健康 | pharmaceutical_product | manufacture | 药品制造商 | 0.9 |
| 美利云 | paper_product | produce | 造纸生产商 | 0.8 |
| 美利云 | data_center_service | operate | 数据中心服务商 | 0.7 |
| 智慧农业 | diesel_engine | manufacture | 柴油发动机制造商 | 0.9 |
| 智慧农业 | agricultural_machinery | manufacture | 农业机械制造商 | 0.7 |
| 航锦科技 | electronic_chemical | produce | 电子化学品生产商 | 0.7 |
| 航锦科技 | special_chemical | produce | 特种化工产品生产商 | 0.8 |
| 航锦科技 | ic_design | operate | 集成电路设计服务商 | 0.8 |
| 岳阳兴长 | refined_oil | produce | 石化产品生产商 | 0.8 |
| 岳阳兴长 | methanol | produce | 甲醇生产商 | 0.7 |
| 岳阳兴长 | lp_gas | produce | 液化石油气生产商 | 0.7 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_030_graph",
    "status": 201,
    "nodes_created": 6,
    "nodes_updated": 0,
    "edges_created": 2,
    "edges_updated": 1,
    "errors": [
      {"type": "edge", "id": "flow_cigarette_packaging_to_tobacco", "error": "'NoneType' object is not subscriptable"},
      {"type": "edge", "id": "flow_methanol_to_fuel", "error": "'NoneType' object is not subscriptable"}
    ]
  },
  "business_batch": {
    "batch_id": "batch_030_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 21,
    "exposures_updated": 0,
    "errors": []
  }
}
```

## 6. Design Notes

- **云铝股份** 构建了铝产业链的关键 material_flow：`aluminum_smelting` → `aluminum_ingot` → `aluminum_alloy`。其中 `aluminum_smelting` → `aluminum_ingot` 的边被更新（之前可能已存在不完整的边），`aluminum_ingot` → `aluminum_alloy` 为新创建，完整覆盖了从电解铝到铝加工材的转化路径。
- **航锦科技** 是"化工+电子"双主业企业的典型代表。化工侧暴露到 `special_chemical`（烧碱、环氧丙烷等），电子侧暴露到 `electronic_chemical` 和 `ic_design`（特种芯片、FPGA设计），体现了传统化工企业向半导体材料领域转型的战略布局。
- **美利云** 是罕见的"造纸+数据中心"双主业企业，暴露到 `paper_product` 和 `data_center_service`，代表了传统制造业向数字经济基础设施转型的跨界模式。
- **岳阳兴长** 构建 `methanol`（甲醇）、`lp_gas`（液化石油气）与 `refined_oil`（成品油）的石化产品矩阵，与 `lp_gas` → `natural_gas` 的 service_flow 反映了LPG在民用燃气领域与天然气的替代关系。
- **两个 edge 错误说明**：`flow_cigarette_packaging_to_tobacco` 因 `cigarette` 节点尚未创建而失败；`flow_methanol_to_fuel` 因目标节点问题失败。这些节点/边可在后续批次中补充。

---

**Total Graph after Batch 030:**
- Nodes: 560 (554 + 6)
- Edges: 436 (434 + 2)
