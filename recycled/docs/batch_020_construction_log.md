# Batch 020 Construction Log

**Date:** 2026-05-24  
**Companies:** 000652.SZ – 000669.SZ (10 companies)  
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+21)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `clean_material` | 洁净材料 | material |
| 2 | `iron_ore` | 铁矿石 | material |
| 3 | `community_life_service` | 社区生活服务 | service |
| 4 | `cemented_carbide` | 硬质合金 | material |
| 5 | `tungsten` | 钨 | material |
| 6 | `molybdenum` | 钼 | material |
| 7 | `tantalum` | 钽 | material |
| 8 | `niobium` | 铌 | material |
| 9 | `rare_refractory_metal` | 稀有难熔金属 | material |
| 10 | `pet_bottle` | PET瓶 | component |
| 11 | `bottle_preform` | 瓶胚 | component |
| 12 | `beverage_packaging` | 饮料包装 | component |
| 13 | `beverage_processing` | 饮料加工 | service |
| 14 | `pet_resin` | PET树脂 | material |
| 15 | `formaldehyde` | 甲醛 | material |
| 16 | `impregnated_paper` | 浸渍纸 | material |
| 17 | `adhesive` | 胶粘剂 | material |
| 18 | `forest_chemical_product` | 林化产品 | material |
| 19 | `pipeline_transportation` | 管道运输 | service |
| 20 | `natural_gas_pipeline` | 天然气长输管道 | infrastructure |
| 21 | `urban_gas_network` | 城市燃气管网 | infrastructure |

## 2. New Industrial Edges (+18)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_tungsten_to_carbide` | tungsten → cemented_carbide | material_flow |
| 2 | `flow_tungsten_to_rare` | tungsten → rare_refractory_metal | composition |
| 3 | `flow_moly_to_rare` | molybdenum → rare_refractory_metal | composition |
| 4 | `flow_tantalum_to_rare` | tantalum → rare_refractory_metal | composition |
| 5 | `flow_niobium_to_rare` | niobium → rare_refractory_metal | composition |
| 6 | `flow_pet_resin_to_preform` | pet_resin → bottle_preform | material_flow |
| 7 | `flow_preform_to_bottle` | bottle_preform → pet_bottle | material_flow |
| 8 | `flow_pet_bottle_to_packaging` | pet_bottle → beverage_packaging | composition |
| 9 | `flow_beverage_to_packaging` | beverage_processing → beverage_packaging | service_flow |
| 10 | `flow_timber_to_forest_chem` | timber → forest_chemical_product | material_flow |
| 11 | `flow_forest_chem_to_formaldehyde` | forest_chemical_product → formaldehyde | material_flow |
| 12 | `flow_forest_chem_to_adhesive` | forest_chemical_product → adhesive | material_flow |
| 13 | `flow_formaldehyde_to_adhesive` | formaldehyde → adhesive | material_flow |
| 14 | `flow_impregnated_to_board` | impregnated_paper → artificial_board | material_flow |
| 15 | `flow_natgas_to_pipeline` | natural_gas → natural_gas_pipeline | material_flow |
| 16 | `flow_pipeline_to_city_gas` | natural_gas_pipeline → city_gas_supply | service_flow |
| 17 | `flow_pipeline_to_transport` | natural_gas_pipeline → pipeline_transportation | service_flow |
| 18 | `flow_urban_to_city_gas` | urban_gas_network → city_gas_supply | service_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `taida_share` | 泰达股份 | 000652.SZ | 天津 | 天津市 | 1,619 |
| 2 | `jinling_mining` | 金岭矿业 | 000655.SZ | 山东 | 淄博市 | 1,834 |
| 3 | `st_jinke` | *ST金科 | 000656.SZ | 重庆 | 重庆市 | 3,660 |
| 4 | `zhongwu_high_tech` | 中钨高新 | 000657.SZ | 海南 | 海口市 | 8,848 |
| 5 | `zhuhai_zhongfu` | 珠海中富 | 000659.SZ | 广东 | 珠海市 | 1,638 |
| 6 | `changchun_high_tech` | 长春高新 | 000661.SZ | 吉林 | 长春市 | 11,547 |
| 7 | `yongan_forestry` | 永安林业 | 000663.SZ | 福建 | 三明市 | 386 |
| 8 | `hubei_guangdian` | 湖北广电 | 000665.SZ | 湖北 | 武汉市 | 6,165 |
| 9 | `st_rongkong` | *ST荣控 | 000668.SZ | 山东 | 青岛市 | 86 |
| 10 | `st_jinhong` | ST金鸿 | 000669.SZ | 湖南 | 衡阳市 | 852 |

## 4. Company Node Exposures (+41)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 泰达股份 | ecological_restoration_service | operate | 生态环保服务商 | 0.6 |
| 泰达股份 | real_estate_development | operate | 区域开发商 | 0.5 |
| 泰达股份 | trade_service | operate | 能源贸易商 | 0.5 |
| 泰达股份 | clean_material | manufacture | 洁净材料制造商 | 0.4 |
| 金岭矿业 | iron_ore | produce | 铁矿石生产商 | 0.9 |
| *ST金科 | real_estate_development | operate | 房地产开发商 | 0.9 |
| *ST金科 | community_life_service | operate | 社区生活服务商 | 0.5 |
| *ST金科 | hotel_operation_service | operate | 酒店运营商 | 0.3 |
| *ST金科 | greening_construction_service | provide_service | 园林服务商 | 0.3 |
| *ST金科 | construction_service | operate | 装饰工程施工商 | 0.3 |
| *ST金科 | solar_power_generation | operate | 新能源发电运营商 | 0.2 |
| 中钨高新 | cemented_carbide | manufacture | 硬质合金制造商 | 0.9 |
| 中钨高新 | tungsten | manufacture | 钨制品制造商 | 0.8 |
| 中钨高新 | molybdenum | manufacture | 钼制品制造商 | 0.6 |
| 中钨高新 | tantalum | manufacture | 钽制品制造商 | 0.5 |
| 中钨高新 | niobium | manufacture | 铌制品制造商 | 0.5 |
| 中钨高新 | rare_refractory_metal | manufacture | 稀有难熔金属制造商 | 0.9 |
| 珠海中富 | pet_bottle | manufacture | PET瓶制造商 | 0.9 |
| 珠海中富 | bottle_preform | manufacture | 瓶胚制造商 | 0.8 |
| 珠海中富 | beverage_packaging | manufacture | 饮料包装制造商 | 0.8 |
| 珠海中富 | beverage_processing | operate | 饮料加工商 | 0.4 |
| 珠海中富 | pet_resin | manufacture | PET树脂制造商 | 0.3 |
| 长春高新 | biological_drug | manufacture | 基因工程药物制造商 | 0.9 |
| 长春高新 | pharmaceutical_product | manufacture | 药品制造商 | 0.8 |
| 长春高新 | traditional_chinese_medicine | manufacture | 中成药制造商 | 0.5 |
| 永安林业 | forestry | operate | 林业经营商 | 0.7 |
| 永安林业 | wood_product | manufacture | 木材产品制造商 | 0.6 |
| 永安林业 | timber | produce | 原木生产商 | 0.5 |
| 永安林业 | artificial_board | manufacture | 人造板制造商 | 0.4 |
| 永安林业 | formaldehyde | manufacture | 甲醛制造商 | 0.5 |
| 永安林业 | impregnated_paper | manufacture | 浸渍纸制造商 | 0.4 |
| 永安林业 | adhesive | manufacture | 胶粘剂制造商 | 0.5 |
| 永安林业 | forest_chemical_product | manufacture | 林化产品制造商 | 0.5 |
| 湖北广电 | cable_tv_network_service | operate | 有线电视网络运营商 | 0.9 |
| 湖北广电 | cable_tv_equipment | manufacture | 有线电视设备制造商 | 0.4 |
| *ST荣控 | real_estate_development | operate | 房地产开发商 | 0.9 |
| ST金鸿 | natural_gas | operate | 天然气运营商 | 0.8 |
| ST金鸿 | city_gas_supply | operate | 城市燃气供应商 | 0.9 |
| ST金鸿 | pipeline_transportation | operate | 管道运输运营商 | 0.7 |
| ST金鸿 | natural_gas_pipeline | operate | 长输管道运营商 | 0.8 |
| ST金鸿 | urban_gas_network | operate | 城市管网运营商 | 0.7 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_020_graph",
    "status": 201,
    "nodes_created": 21,
    "nodes_updated": 0,
    "edges_created": 18,
    "edges_updated": 0
  },
  "business_batch": {
    "batch_id": "batch_020_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 41,
    "exposures_updated": 0
  }
}
```

## 6. Design Notes

- **中钨高新**业务覆盖钨、钼、钽、铌和硬质合金五条线，新建了`rare_refractory_metal`（稀有难熔金属）作为聚合节点，便于后续同类企业归类。
- **珠海中富**的PET瓶产业链从树脂→瓶胚→PET瓶→饮料包装形成完整物料流，并补充了饮料加工服务节点。
- **永安林业**从林业经营延伸至木材加工、林化产品、甲醛和胶粘剂，展示了从上游林业到下游精细化工的产业路径。
- **ST金鸿**以天然气长输管道和城市燃气管网为基础，新增了`pipeline_transportation`和天然气管网基础设施节点，与已有的`natural_gas`和`city_gas_supply`形成完整燃气供应链。
- 3家房地产相关企业（泰达股份、*ST金科、*ST荣控）共用已有`real_estate_development`节点，*ST金科还引入了社区生活服务节点以体现其多元化业务。

---

**Total Graph after Batch 020:**
- Nodes: 475 (454 + 21)
- Edges: 373 (355 + 18)
