# Batch 031 Construction Log

**Date:** 2026-05-25
**Companies:** 000820.SZ – 000831.SZ (10 companies)
**Status:** ✅ Submitted successfully (1 edge error: flat_glass missing)

---

## 1. New Industrial Nodes (+5, 1 updated)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `energy_efficiency_engineering` | 节能环保工程 | service |
| 2 | `packaging_machinery` | 包装机械 | device |
| 3 | `soda_ash` | 纯碱 | material |
| 4 | `cold_rolled_silicon_steel` | 冷轧硅钢 | material |
| 5 | `rare_earth_oxide` | 稀土氧化物 | material |
| 6 | `rare_earth_metal` | 稀土金属 | material |

## 2. New Industrial Edges (+2, 1 error)

| # | Edge ID | From Node → To Node | Type | Status |
|---|---------|---------------------|------|--------|
| 1 | `flow_soda_ash_to_glass` | soda_ash → flat_glass | material_flow | ❌ (flat_glass missing) |
| 2 | `flow_rare_earth_oxide_to_metal` | rare_earth_oxide → rare_earth_metal | material_flow | ✅ |
| 3 | `flow_rare_earth_metal_to_magnet` | rare_earth_metal → ndfeb_magnet | material_flow | ✅ |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `shenwu_energy_saving` | 神雾节能股份有限公司 | 000820.SZ | 江西 | 南昌市 | 175 |
| 2 | `jingshan_light_machinery` | 湖北京山轻工机械股份有限公司 | 000821.SZ | 湖北 | 荆门市 | 5,166 |
| 3 | `shandong_haihua` | 山东海化股份有限公司 | 000822.SZ | 山东 | 潍坊市 | 4,451 |
| 4 | `chaoshen_electronics` | 广东汕头超声电子股份有限公司 | 000823.SZ | 广东 | 汕头市 | 7,531 |
| 5 | `taigang_stainless` | 山西太钢不锈钢股份有限公司 | 000825.SZ | 山西 | 太原市 | 13,080 |
| 6 | `tus_environment` | 启迪环境科技发展股份有限公司 | 000826.SZ | 湖北 | 宜昌市 | 42,617 |
| 7 | `dongguan_holdings` | 东莞发展控股股份有限公司 | 000828.SZ | 广东 | 东莞市 | 864 |
| 8 | `tianyin_holdings` | 天音通信控股股份有限公司 | 000829.SZ | 江西 | 赣州市 | 3,558 |
| 9 | `luxi_chemical` | 鲁西化工集团股份有限公司 | 000830.SZ | 山东 | 聊城市 | 12,124 |
| 10 | `china_rare_earth` | 中国稀土集团资源科技股份有限公司 | 000831.SZ | 江西 | 赣州市 | 528 |

## 4. Company Node Exposures (+19)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| *ST节能 | energy_efficiency_engineering | operate | 节能环保工程承包商 | 0.9 |
| ST京机 | packaging_machinery | manufacture | 包装机械制造商 | 0.9 |
| ST京机 | automotive_part | manufacture | 汽车零部件制造商 | 0.7 |
| 山东海化 | soda_ash | produce | 纯碱生产商 | 0.9 |
| 山东海化 | caustic_soda | produce | 烧碱生产商 | 0.8 |
| 超声电子 | pcb | manufacture | 印制线路板制造商 | 0.9 |
| 超声电子 | lcd_panel | manufacture | 液晶显示器制造商 | 0.8 |
| 太钢不锈 | stainless_steel | produce | 不锈钢生产商 | 0.9 |
| 太钢不锈 | cold_rolled_silicon_steel | produce | 冷轧硅钢生产商 | 0.8 |
| 太钢不锈 | steel_plate | produce | 碳钢板材生产商 | 0.7 |
| *ST启环 | solid_waste_treatment | operate | 固废处置运营商 | 0.9 |
| *ST启环 | municipal_waste_treatment | operate | 城市废弃物处理运营商 | 0.7 |
| 东莞控股 | highway_operation_service | operate | 高速公路运营商 | 0.9 |
| 天音控股 | mobile_terminal | operate | 手机分销商 | 0.9 |
| 天音控股 | liquor | operate | 酒类产品经销商 | 0.6 |
| 鲁西化工 | urea | produce | 尿素生产商 | 0.9 |
| 鲁西化工 | compound_fertilizer | produce | 复合肥生产商 | 0.8 |
| 中国稀土 | rare_earth_oxide | produce | 稀土氧化物生产商 | 0.9 |
| 中国稀土 | rare_earth_metal | produce | 稀土金属生产商 | 0.8 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_031_graph",
    "status": 201,
    "nodes_created": 5,
    "nodes_updated": 1,
    "edges_created": 2,
    "edges_updated": 0,
    "errors": [{"type": "edge", "id": "flow_soda_ash_to_glass", "error": "'NoneType' object is not subscriptable"}]
  },
  "business_batch": {
    "batch_id": "batch_031_business",
    "status": 201,
    "companies_created": 10,
    "exposures_created": 19,
    "errors": []
  }
}
```

---

**Total Graph after Batch 031:**
- Nodes: 570 (560 + 5 + 1U)
- Edges: 441 (436 + 2)
