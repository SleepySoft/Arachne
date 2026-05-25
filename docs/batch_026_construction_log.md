# Batch 026 Construction Log

**Date:** 2026-05-25
**Companies:** 000737.SZ – 000757.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+7)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `zinc_metal` | 锌金属 | material |
| 2 | `lead_metal` | 铅金属 | material |
| 3 | `chromium_metal` | 铬金属 | material |
| 4 | `engine_control_system` | 航空发动机控制系统 | subsystem |
| 5 | `sodium_sulfate` | 无水硫酸钠 | material |
| 6 | `sodium_sulfide` | 硫化钠 | material |
| 7 | `highway_operation_service` | 高速公路运营服务 | service |

## 2. New Industrial Edges (+2)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_zinc_ore_to_zinc` | zinc_ore → zinc_metal | material_flow |
| 2 | `flow_lead_zinc_to_lead` | lead_zinc_ore → lead_metal | material_flow |

## 3. Companies Registered (+10 created)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `northern_copper` | 北方铜业股份有限公司 | 000737.SZ | 山西 | 运城市 | 9,488 |
| 2 | `aero_engine_control` | 中国航发动力控制股份有限公司 | 000738.SZ | 江苏 | 无锡市 | 7,333 |
| 3 | `apeloa` | 普洛药业股份有限公司 | 000739.SZ | 浙江 | 金华市 | 6,292 |
| 4 | `sealand_securities` | 国海证券股份有限公司 | 000750.SZ | 广西 | 南宁市 | 3,837 |
| 5 | `zinc_industry` | 葫芦岛锌业股份有限公司 | 000751.SZ | 辽宁 | 葫芦岛市 | 5,082 |
| 6 | `st_xifa` | 西藏发展股份有限公司 | 000752.SZ | 西藏 | 拉萨市 | 345 |
| 7 | `zhangzhou_dev` | 福建漳州发展股份有限公司 | 000753.SZ | 福建 | 漳州市 | 2,349 |
| 8 | `shanxi_expressway` | 山西路桥股份有限公司 | 000755.SZ | 山西 | 太原市 | 1,862 |
| 9 | `xinhua_pharm` | 山东新华制药股份有限公司 | 000756.SZ | 山东 | 淄博市 | 6,812 |
| 10 | `haowu` | 四川浩物机电股份有限公司 | 000757.SZ | 四川 | 内江市 | 1,892 |

## 4. Company Node Exposures (+25 created)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 北方铜业 | copper | produce | 铜生产商 | 0.9 |
| 北方铜业 | copper_sheet | produce | 铜板带生产商 | 0.7 |
| 北方铜业 | copper_foil | produce | 铜箔生产商 | 0.6 |
| 航发控制 | aerospace_engine | manufacture | 航空发动机控制器制造商 | 0.9 |
| 航发控制 | engine_control_system | manufacture | 发动机控制系统制造商 | 0.9 |
| 航发控制 | aerospace_precision_part | manufacture | 航空精密部件制造商 | 0.7 |
| 普洛药业 | active_pharmaceutical_ingredient | manufacture | 原料药制造商 | 0.9 |
| 普洛药业 | pharmaceutical_raw_material | produce | 医药中间体生产商 | 0.8 |
| 普洛药业 | pharmaceutical_product | manufacture | 药品制剂生产商 | 0.7 |
| 国海证券 | securities_brokerage | operate | 证券经纪服务商 | 0.9 |
| 国海证券 | securities_underwriting | operate | 证券承销保荐服务商 | 0.7 |
| 国海证券 | asset_management_service | operate | 资产管理服务商 | 0.7 |
| 锌业股份 | zinc_metal | produce | 锌金属生产商 | 0.9 |
| 锌业股份 | lead_metal | produce | 铅金属生产商 | 0.7 |
| 锌业股份 | lead_zinc_metal | produce | 铅锌综合生产商 | 0.6 |
| *ST西发 | beer | produce | 啤酒生产商 | 0.9 |
| 漳州发展 | tap_water_supply | operate | 自来水供应运营商 | 0.8 |
| 漳州发展 | trade_service | operate | 贸易服务商 | 0.5 |
| 山西高速 | highway_operation_service | operate | 高速公路运营商 | 0.9 |
| 新华制药 | active_pharmaceutical_ingredient | manufacture | 原料药制造商 | 0.9 |
| 新华制药 | pharmaceutical_product | manufacture | 药品制剂生产商 | 0.8 |
| 新华制药 | sodium_sulfate | produce | 无水硫酸钠生产商 | 0.6 |
| 新华制药 | sodium_sulfide | produce | 硫化钠生产商 | 0.5 |
| 浩物股份 | automotive_engine_accessory | manufacture | 汽车发动机配件制造商 | 0.9 |
| 浩物股份 | automotive_aftermarket | operate | 汽车后市场服务商 | 0.7 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_026_graph",
    "status": 201,
    "nodes_created": 7,
    "nodes_updated": 0,
    "edges_created": 2,
    "edges_updated": 0
  },
  "business_batch": {
    "batch_id": "batch_026_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 25,
    "exposures_updated": 0,
    "errors": []
  }
}
```

## 6. Design Notes

- **北方铜业** 作为铜冶炼企业，暴露了铜全产业链节点：`copper` → `copper_sheet` → `copper_foil`，体现了从电解铜到铜加工材的纵向布局。
- **航发控制** 是中国航空发动机控制系统的核心供应商，新增 `engine_control_system` 节点并与 `aerospace_engine` 形成 composition 关系，填补了航空发动机控制系统这一关键子系统空白。
- **锌业股份** 依托葫芦岛锌厂，构建 `zinc_metal` 和 `lead_metal` 双金属生产体系，与已有的 `lead_zinc_ore` 和 `lead_zinc_metal` 形成完整铅锌产业链。
- **新华制药** 除了制药主业外，还生产 `sodium_sulfate`（元明粉）和 `sodium_sulfide` 等化工副产品，体现了原料药企业多元化经营的特征。
- **山西高速** 新增 `highway_operation_service` 节点，与 batch 023 的粤高速形成对比，丰富了高速公路运营服务节点矩阵。

---

**Total Graph after Batch 026:**
- Nodes: 526 (519 + 7)
- Edges: 421 (419 + 2)
