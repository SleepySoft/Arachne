# Batch 022 Construction Log

**Date:** 2026-05-25  
**Companies:** 000685.SZ – 000698.SZ (10 companies)  
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+17)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `port_passenger_service` | 港口客运服务 | service |
| 2 | `securities_brokerage` | 证券经纪服务 | service |
| 3 | `securities_underwriting` | 证券承销与保荐服务 | service |
| 4 | `securities_proprietary_trading` | 证券自营业务 | service |
| 5 | `asset_management_service` | 资产管理服务 | service |
| 6 | `margin_trading_service` | 融资融券服务 | service |
| 7 | `clean_coal_power_generation` | 洁净煤燃烧发电 | service |
| 8 | `pharmaceutical_intermediate` | 医药中间体 | material |
| 9 | `pesticide_intermediate` | 农药中间体 | material |
| 10 | `heating_engineering_service` | 供暖工程服务 | service |
| 11 | `industrial_steam` | 工业蒸汽 | material |
| 12 | `printing_service` | 印刷业务 | service |
| 13 | `motorcycle_engine` | 摩托车发动机 | subsystem |
| 14 | `aerospace_precision_part` | 航空精密零部件 | component |
| 15 | `aircraft_structural_part` | 飞机结构件 | component |
| 16 | `paste_pvc_resin` | 糊树脂 | material |
| 17 | `propylene` | 丙烯 | material |

## 2. New Industrial Edges (+7)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_pharma_intermediate_to_api` | pharmaceutical_intermediate → active_pharmaceutical_ingredient | material_flow |
| 2 | `flow_pesticide_intermediate_to_pesticide` | pesticide_intermediate → pesticide | material_flow |
| 3 | `flow_heating_engineering_to_supply` | heating_engineering_service → heating_supply | service_flow |
| 4 | `flow_aerospace_part_to_aircraft` | aerospace_precision_part → aircraft | composition |
| 5 | `flow_structural_part_to_aircraft` | aircraft_structural_part → aircraft | composition |
| 6 | `flow_refinery_to_propylene` | refining_service → propylene | service_flow |
| 7 | `variant_paste_pvc` | paste_pvc_resin → pvc | variant_of (ontology) |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `zhongshan_public` | 中山公用事业集团股份有限公司 | 000685.SZ | 广东 | 中山市 | 5,794 |
| 2 | `northeast_securities` | 东北证券股份有限公司 | 000686.SZ | 吉林 | 长春市 | 3,656 |
| 3 | `guocheng_mining` | 国城矿业股份有限公司 | 000688.SZ | 四川 | 阿坝州 | 3,190 |
| 4 | `baoxin_energy` | 广东宝丽华新能源股份有限公司 | 000690.SZ | 广东 | 梅州市 | 1,258 |
| 5 | `st_yatai` | 甘肃亚太实业发展股份有限公司 | 000691.SZ | 甘肃 | 兰州市 | 412 |
| 6 | `huitian_thermal` | 沈阳惠天热电股份有限公司 | 000692.SZ | 辽宁 | 沈阳市 | 1,254 |
| 7 | `binhai_energy` | 天津滨海能源发展股份有限公司 | 000695.SZ | 天津 | 天津市 | 196 |
| 8 | `zongshen_power` | 重庆宗申动力机械股份有限公司 | 001696.SZ | 重庆 | 重庆市 | 9,459 |
| 9 | `lianshi_aviation` | 炼石航空科技股份有限公司 | 000697.SZ | 陕西 | 咸阳市 | 2,458 |
| 10 | `st_shenhua` | 沈阳化工股份有限公司 | 000698.SZ | 辽宁 | 沈阳市 | 1,484 |

## 4. Company Node Exposures (+30)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 中山公用 | waste_water_treatment | operate | 污水处理运营商 | 0.8 |
| 中山公用 | solid_waste_treatment | operate | 固废处理运营商 | 0.7 |
| 中山公用 | tap_water_supply | operate | 自来水供应运营商 | 0.7 |
| 中山公用 | port_passenger_service | operate | 港口客运服务商 | 0.5 |
| 东北证券 | securities_brokerage | operate | 证券经纪服务商 | 0.9 |
| 东北证券 | securities_underwriting | operate | 证券承销与保荐服务商 | 0.8 |
| 东北证券 | securities_proprietary_trading | operate | 证券自营投资商 | 0.7 |
| 东北证券 | asset_management_service | operate | 资产管理服务商 | 0.7 |
| 东北证券 | margin_trading_service | operate | 融资融券服务商 | 0.6 |
| 国城矿业 | lead_zinc_ore | produce | 铅锌矿石生产商 | 0.9 |
| 国城矿业 | lead_zinc_metal | produce | 铅锌金属生产商 | 0.9 |
| 国城矿业 | sulfuric_acid | produce | 硫酸生产商 | 0.7 |
| 宝新能源 | clean_coal_power_generation | operate | 洁净煤发电运营商 | 0.9 |
| 宝新能源 | renewable_energy_power_generation | operate | 可再生能源发电运营商 | 0.8 |
| 宝新能源 | coal_power_generation | operate | 燃煤发电运营商 | 0.6 |
| *ST亚太 | pharmaceutical_intermediate | produce | 医药中间体生产商 | 0.9 |
| *ST亚太 | pesticide_intermediate | produce | 农药中间体生产商 | 0.9 |
| 惠天热电 | heating_supply | operate | 供热服务商 | 0.9 |
| 惠天热电 | heating_engineering_service | operate | 供暖工程服务商 | 0.8 |
| 滨海能源 | industrial_steam | produce | 工业蒸汽生产商 | 0.9 |
| 滨海能源 | electricity_power | produce | 电力生产商 | 0.9 |
| 滨海能源 | printing_service | operate | 印刷业务运营商 | 0.5 |
| 宗申动力 | motorcycle_engine | manufacture | 摩托车发动机制造商 | 0.9 |
| 炼石航空 | aerospace_precision_part | manufacture | 航空精密零部件制造商 | 0.9 |
| 炼石航空 | aircraft_structural_part | manufacture | 飞机结构件制造商 | 0.9 |
| ST沈化 | caustic_soda | produce | 烧碱生产商 | 0.9 |
| ST沈化 | paste_pvc_resin | produce | 糊树脂生产商 | 0.8 |
| ST沈化 | gasoline | produce | 汽油生产商 | 0.7 |
| ST沈化 | diesel | produce | 柴油生产商 | 0.7 |
| ST沈化 | propylene | produce | 丙烯生产商 | 0.7 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_022_graph",
    "status": 201,
    "nodes_created": 17,
    "nodes_updated": 0,
    "edges_created": 7,
    "edges_updated": 0
  },
  "business_batch": {
    "batch_id": "batch_022_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 30,
    "exposures_updated": 0
  }
}
```

## 6. Design Notes

- **东北证券** 构建了较为完整的证券服务节点群（经纪、承销、自营、资管、融资融券），展示了证券公司多元化业务结构。这些服务节点之间没有严格的产业流关系，属于平行金融服务类型。
- **炼石航空** 的航空零部件产业链直接连接到已有的 `aircraft` 节点，通过 composition 关系表达精密零部件和结构件作为飞机组成部分的定位。
- **ST沈化** 延伸了石油炼化下游产品链，新增 `propylene`（丙烯）节点，并通过 `refining_service` → `propylene` 的 service_flow 边与已有炼化服务衔接。糊树脂通过 ontology 的 `variant_of` 关系与已有 `pvc` 节点关联，避免了概念重复。
- **宝新能源** 的 `clean_coal_power_generation` 节点体现了传统煤电向清洁化升级的产业趋势，与已有的 `coal_power_generation` 和 `renewable_energy_power_generation` 形成互补。

---

**Total Graph after Batch 022:**
- Nodes: 465 (448 + 17)
- Edges: 381 (374 + 7)
