# Batch 028 Construction Log

**Date:** 2026-05-25
**Companies:** 000779.SZ – 000792.SZ (10 companies)
**Status:** ✅ Submitted successfully (2 edge errors: referenced nodes not yet in graph)

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `engineering_consulting_service` | 工程咨询服务 | service |
| 2 | `nylon_filament` | 锦纶长丝 | material |
| 3 | `nylon_chip` | 锦纶切片 | material |
| 4 | `home_materials_retail` | 家居建材零售 | service |
| 5 | `gypsum_board` | 石膏板 | material |
| 6 | `light_steel_keel` | 轻钢龙骨 | component |
| 7 | `mineral_wool_board` | 矿棉板 | material |
| 8 | `potassium_sulfate` | 硫酸钾 | material |
| 9 | `lithium_carbonate` | 碳酸锂 | material |

## 2. New Industrial Edges (+3, 2 errors)

| # | Edge ID | From Node → To Node | Type | Status |
|---|---------|---------------------|------|--------|
| 1 | `flow_nylon_chip_to_filament` | nylon_chip → nylon_filament | material_flow | ✅ |
| 2 | `flow_gypsum_to_board` | gypsum → gypsum_board | material_flow | ❌ (gypsum missing) |
| 3 | `flow_keel_to_gypsum_board` | light_steel_keel → gypsum_board | composition | ✅ |
| 4 | `flow_potassium_chloride_to_fertilizer` | potassium_chloride → chemical_fertilizer | material_flow | ✅ |
| 5 | `flow_lithium_carbonate_to_battery` | lithium_carbonate → lithium_ion_battery | material_flow | ❌ (lithium_ion_battery missing) |

## 3. Companies Registered (+10 created)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `gs_consulting` | 甘肃工程咨询集团股份有限公司 | 000779.SZ | 甘肃 | 兰州市 | 687 |
| 2 | `henshen_new_material` | 恒申新材股份有限公司 | 000782.SZ | 福建 | 福州市 | 4,871 |
| 3 | `cj_securities` | 长江证券股份有限公司 | 000783.SZ | 湖北 | 武汉市 | 7,203 |
| 4 | `juran_smart_home` | 居然智家新零售连锁集团有限公司 | 000785.SZ | 北京 | 北京市 | 7,045 |
| 5 | `bnmc` | 北新集团建材股份有限公司 | 000786.SZ | 北京 | 北京市 | 28,293 |
| 6 | `beida_pharm` | 北大医药股份有限公司 | 000788.SZ | 重庆 | 重庆市 | 1,199 |
| 7 | `wannianqing` | 江西万年青水泥股份有限公司 | 000789.SZ | 江西 | 南昌市 | 3,092 |
| 8 | `huashen_tech` | 华神科技集团股份有限公司 | 000790.SZ | 四川 | 成都市 | 596 |
| 9 | `gansu_energy` | 甘肃电投能源发展股份有限公司 | 000791.SZ | 甘肃 | 兰州市 | 1,154 |
| 10 | `salt_lake` | 青海盐湖工业股份有限公司 | 000792.SZ | 青海 | 格尔木市 | 8,463 |

## 4. Company Node Exposures (+23 created)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 甘咨询 | engineering_consulting_service | operate | 工程咨询服务提供商 | 0.9 |
| 恒申新材 | nylon_filament | produce | 锦纶长丝生产商 | 0.9 |
| 恒申新材 | nylon_chip | produce | 锦纶切片生产商 | 0.8 |
| 长江证券 | securities_brokerage | operate | 证券经纪服务商 | 0.9 |
| 长江证券 | securities_underwriting | operate | 证券承销保荐服务商 | 0.7 |
| 长江证券 | asset_management_service | operate | 资产管理服务商 | 0.7 |
| 居然智家 | home_materials_retail | operate | 家居建材零售商 | 0.9 |
| 居然智家 | furniture | operate | 家具零售商 | 0.7 |
| 北新建材 | gypsum_board | produce | 石膏板生产商 | 0.9 |
| 北新建材 | light_steel_keel | produce | 轻钢龙骨生产商 | 0.8 |
| 北新建材 | mineral_wool_board | produce | 矿棉板生产商 | 0.7 |
| 北大医药 | pharmaceutical_product | manufacture | 药品制造商 | 0.9 |
| 万年青 | cement | produce | 水泥生产商 | 0.9 |
| 万年青 | ready_mix_concrete | produce | 混凝土生产商 | 0.8 |
| 华神科技 | traditional_chinese_medicine | manufacture | 中成药制造商 | 0.7 |
| 华神科技 | biological_product | manufacture | 生物制品制造商 | 0.7 |
| 甘肃能源 | hydro_power_generation | operate | 水电运营商 | 0.9 |
| 甘肃能源 | wind_power_generation | operate | 风电运营商 | 0.8 |
| 甘肃能源 | electricity_power | produce | 电力生产商 | 0.8 |
| 盐湖股份 | potassium_chloride | produce | 氯化钾生产商 | 0.9 |
| 盐湖股份 | chemical_fertilizer | produce | 钾肥生产商 | 0.9 |
| 盐湖股份 | potassium_sulfate | produce | 硫酸钾生产商 | 0.7 |
| 盐湖股份 | lithium_carbonate | produce | 碳酸锂生产商 | 0.7 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_028_graph",
    "status": 201,
    "nodes_created": 9,
    "nodes_updated": 0,
    "edges_created": 3,
    "edges_updated": 0,
    "errors": [
      {"type": "edge", "id": "flow_gypsum_to_board", "error": "'NoneType' object is not subscriptable"},
      {"type": "edge", "id": "flow_lithium_carbonate_to_battery", "error": "'NoneType' object is not subscriptable"}
    ]
  },
  "business_batch": {
    "batch_id": "batch_028_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 23,
    "exposures_updated": 0,
    "errors": []
  }
}
```

## 6. Design Notes

- **恒申新材** 构建了锦纶产业链核心环节：`nylon_chip` → `nylon_filament`，从切片到长丝的 material_flow 代表了化纤行业的典型生产路径。恒申新材是全球最大的己内酰胺和锦纶切片生产商之一。
- **北新建材** 是全球最大的石膏板产业集团，新增 `gypsum_board`、`light_steel_keel`、`mineral_wool_board` 三个节点，其中石膏板与龙骨形成 composition 关系（龙骨作为骨架支撑石膏板），是建筑装修材料的标准系统组合。
- **盐湖股份** 是中国最大的钾肥生产基地，暴露到 `potassium_chloride`（氯化钾）、`chemical_fertilizer`（钾肥）、`potassium_sulfate`（硫酸钾）和 `lithium_carbonate`（碳酸锂），体现了传统钾肥企业向新能源锂材料延伸的战略转型。
- **甘肃能源** 作为清洁能源企业，同时运营 `hydro_power_generation` 和 `wind_power_generation`，与 batch 016 的甘肃电投形成呼应，但业务侧重略有不同。
- **两个 edge 错误说明**：`flow_gypsum_to_board` 因 `gypsum`（石膏）节点尚未创建而失败；`flow_lithium_carbonate_to_battery` 因 `lithium_ion_battery` 节点尚未创建而失败。这两个节点将在后续批次中补充创建，届时可重新提交这些边。

---

**Total Graph after Batch 028:**
- Nodes: 544 (535 + 9)
- Edges: 430 (427 + 3)
