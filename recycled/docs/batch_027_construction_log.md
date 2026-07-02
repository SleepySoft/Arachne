# Batch 027 Construction Log

**Date:** 2026-05-25
**Companies:** 000758.SZ – 000778.SZ (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+9)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `non_ferrous_metal_engineering` | 有色金属工程 | service |
| 2 | `automotive_surface_plate` | 汽车表面板 | material |
| 3 | `home_appliance_steel` | 家电板 | material |
| 4 | `chromium_iron_alloy` | 铬铁合金 | material |
| 5 | `chromite` | 铬铁矿 | material |
| 6 | `chinese_patent_medicine` | 中成药制剂 | material |
| 7 | `aluminum_profile` | 铝合金型材 | material |
| 8 | `ductile_iron_pipe` | 球墨铸铁管 | component |
| 9 | `casting_product` | 铸造制品 | component |

## 2. New Industrial Edges (+6)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_chromite_to_chromium_alloy` | chromite → chromium_iron_alloy | material_flow |
| 2 | `flow_chromium_alloy_to_stainless` | chromium_iron_alloy → stainless_steel | material_flow |
| 3 | `flow_automotive_plate_to_car` | automotive_surface_plate → passenger_car | composition |
| 4 | `flow_home_appliance_steel_to_appliance` | home_appliance_steel → kitchen_appliance | composition |
| 5 | `flow_aluminum_profile_to_aircraft` | aluminum_profile → aircraft | composition |
| 6 | `flow_ductile_iron_to_water_supply` | ductile_iron_pipe → tap_water_supply | service_flow |

## 3. Companies Registered (+10 created)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `cnmc` | 中国有色金属建设股份有限公司 | 000758.SZ | 北京 | 北京市 | 4,911 |
| 2 | `zhongbai_group` | 中百控股集团股份有限公司 | 000759.SZ | 湖北 | 武汉市 | 14,045 |
| 3 | `benxi_steel` | 本钢板材股份有限公司 | 000761.SZ | 辽宁 | 本溪市 | 12,155 |
| 4 | `tibet_mining` | 西藏矿业发展股份有限公司 | 000762.SZ | 西藏 | 拉萨市 | 412 |
| 5 | `tonghua_jinma` | 通化金马药业集团股份有限公司 | 000766.SZ | 吉林 | 通化市 | 1,532 |
| 6 | `jinkong_power` | 晋能控股山西电力股份有限公司 | 000767.SZ | 山西 | 太原市 | 7,064 |
| 7 | `avic_xifei` | 中航西安飞机工业集团股份有限公司 | 000768.SZ | 陕西 | 西安市 | 24,751 |
| 8 | `gf_securities` | 广发证券股份有限公司 | 000776.SZ | 广东 | 广州市 | 13,640 |
| 9 | `cnncc_valve` | 中核苏阀科技实业股份有限公司 | 000777.SZ | 江苏 | 苏州市 | 1,027 |
| 10 | `xinxing_ductile` | 新兴铸管股份有限公司 | 000778.SZ | 河北 | 邯郸市 | 14,115 |

## 4. Company Node Exposures (+26 created)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 中色股份 | copper | produce | 铜资源开发商 | 0.7 |
| 中色股份 | lead_zinc_metal | produce | 铅锌资源开发商 | 0.7 |
| 中色股份 | non_ferrous_metal_engineering | operate | 国际有色工程承包商 | 0.9 |
| 中百集团 | chain_retail_service | operate | 连锁零售服务商 | 0.9 |
| 中百集团 | trade_service | operate | 商品批发商 | 0.6 |
| 本钢板材 | steel_plate | produce | 板材生产商 | 0.9 |
| 本钢板材 | automotive_surface_plate | produce | 汽车表面板生产商 | 0.8 |
| 本钢板材 | home_appliance_steel | produce | 家电板生产商 | 0.7 |
| 本钢板材 | steel_sheet | produce | 冷轧钢板生产商 | 0.6 |
| 西藏矿业 | chromium_iron_alloy | produce | 铬铁合金生产商 | 0.9 |
| 西藏矿业 | chromite | produce | 铬铁矿生产商 | 0.9 |
| 通化金马 | traditional_chinese_medicine | manufacture | 中成药制造商 | 0.9 |
| 通化金马 | chinese_patent_medicine | manufacture | 中成药制剂生产商 | 0.9 |
| 晋控电力 | electricity_power | produce | 电力生产商 | 0.9 |
| 晋控电力 | heating_supply | produce | 热力供应商 | 0.8 |
| 晋控电力 | coal_power_generation | operate | 燃煤发电运营商 | 0.7 |
| 中航西飞 | aerospace_precision_part | manufacture | 航空零部件制造商 | 0.9 |
| 中航西飞 | aluminum_profile | manufacture | 铝合金型材制造商 | 0.8 |
| 中航西飞 | aircraft | manufacture | 航空器制造商 | 0.7 |
| 广发证券 | securities_brokerage | operate | 证券经纪服务商 | 0.9 |
| 广发证券 | securities_underwriting | operate | 证券承销保荐服务商 | 0.7 |
| 广发证券 | asset_management_service | operate | 资产管理服务商 | 0.7 |
| 中核科技 | valve | manufacture | 工业阀门制造商 | 0.9 |
| 新兴铸管 | ductile_iron_pipe | manufacture | 球墨铸铁管制造商 | 0.9 |
| 新兴铸管 | casting_product | manufacture | 铸造制品制造商 | 0.8 |
| 新兴铸管 | steel_plate | produce | 钢材生产商 | 0.7 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_027_graph",
    "status": 201,
    "nodes_created": 9,
    "nodes_updated": 0,
    "edges_created": 6,
    "edges_updated": 0
  },
  "business_batch": {
    "batch_id": "batch_027_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 26,
    "exposures_updated": 0,
    "errors": []
  }
}
```

## 6. Design Notes

- **中色股份** 是"资源+工程"双轮驱动模式的典型代表，同时暴露到 `copper`、`lead_zinc_metal` 资源开发节点和新增的 `non_ferrous_metal_engineering` 工程服务节点，体现了国际工程承包与矿产资源开发的协同。
- **本钢板材** 新增 `automotive_surface_plate` 和 `home_appliance_steel` 两个高品质特种钢节点，与已有 `steel_plate`、`steel_sheet` 形成完整板材产品矩阵，代表了板材龙头企业的产品结构特征。
- **西藏矿业** 构建了国内唯一的铬系资源全产业链：`chromite` → `chromium_iron_alloy` → `stainless_steel`，从铬铁矿到铬铁合金再到不锈钢的完整 material_flow，填补了铬系产业链空白。
- **中航西飞** 新增 `aluminum_profile` 节点，与 `aerospace_precision_part` 和 `aircraft` 共同构成航空制造的三层布局（材料-零部件-整机）。
- **新兴铸管** 是全球最大的球墨铸铁管生产商，新增 `ductile_iron_pipe` 和 `casting_product` 节点，与 `steel_plate` 形成铸管+钢材的双主业结构。

---

**Total Graph after Batch 027:**
- Nodes: 535 (526 + 9)
- Edges: 427 (421 + 6)
