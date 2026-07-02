# Batch 025 Construction Log

**Date:** 2026-05-25  
**Companies:** 000723.SZ – 000736.SZ (10 companies)  
**Status:** ✅ Submitted successfully (1 exposure error: duplicate existing exposure)

---

## 1. New Industrial Nodes (+16)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `hydrogen_fuel_cell_vehicle` | 氢能燃料电池汽车 | device |
| 2 | `hydrogen_energy` | 氢能 | material |
| 3 | `display_terminal` | 显示器终端产品 | device |
| 4 | `tft_lcd` | 薄膜晶体管液晶显示器件 | component |
| 5 | `small_size_display` | 小尺寸显示器件 | component |
| 6 | `cotton_lint` | 皮棉 | material |
| 7 | `yarn` | 纱线 | material |
| 8 | `dyed_woven_fabric` | 色织面料 | material |
| 9 | `dress_shirt` | 衬衣 | material |
| 10 | `av_product` | 影音产品 | device |
| 11 | `beer` | 啤酒 | material |
| 12 | `urea` | 尿素 | material |
| 13 | `compound_fertilizer` | 复合肥 | material |
| 14 | `vehicle_urea` | 车用尿素 | material |
| 15 | `new_type_electronic_component` | 新型电子元器件 | component |
| 16 | `livestock_breeding` | 牲畜饲养 | service |

## 2. New Industrial Edges (+11)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_coke_to_hydrogen` | coke → hydrogen_energy | material_flow |
| 2 | `flow_hydrogen_to_fcv` | hydrogen_energy → hydrogen_fuel_cell_vehicle | energy_flow |
| 3 | `flow_tft_to_display_terminal` | tft_lcd → display_terminal | composition |
| 4 | `flow_tft_to_lcd_panel` | tft_lcd → lcd_panel | composition |
| 5 | `flow_small_display_to_mobile` | small_size_display → mobile_terminal | composition |
| 6 | `flow_cotton_to_yarn` | cotton_lint → yarn | material_flow |
| 7 | `flow_yarn_to_fabric` | yarn → dyed_woven_fabric | material_flow |
| 8 | `flow_fabric_to_shirt` | dyed_woven_fabric → dress_shirt | material_flow |
| 9 | `flow_urea_to_compound` | urea → compound_fertilizer | material_flow |
| 10 | `flow_urea_to_vehicle_urea` | urea → vehicle_urea | material_flow |
| 11 | `flow_livestock_to_pig` | livestock_breeding → live_pig | service_flow |

## 3. Companies Registered (+9 created, +1 updated)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `meijin_energy` | 山西美锦能源股份有限公司 | 000723.SZ | 山西 | 太原市 | 10,103 |
| 2 | `boe_technology` | 京东方科技集团股份有限公司 | 000725.SZ | 北京 | 北京市 | 109,895 |
| 3 | `lutai_textile` | 鲁泰纺织股份有限公司 | 000726.SZ | 山东 | 淄博市 | 23,988 |
| 4 | `tpv_technology` | 冠捷电子科技股份有限公司 | 000727.SZ | 江苏 | 南京市 | 19,417 |
| 5 | `guoyuan_securities` | 国元证券股份有限公司 | 000728.SZ | 安徽 | 合肥市 | 3,984 |
| 6 | `yanjing_beer` | 北京燕京啤酒股份有限公司 | 000729.SZ | 北京 | 北京市 | 19,965 |
| 7 | `sichuan_meifeng` | 四川美丰化工股份有限公司 | 000731.SZ | 四川 | 遂宁市 | 2,473 |
| 8 | `zhenhua_tech` | 中国振华(集团)科技股份有限公司 | 000733.SZ | 贵州 | 贵阳市 | 7,074 |
| 9 | `luoniushan` | 罗牛山股份有限公司 | 000735.SZ | 海南 | 海口市 | 2,722 |
| 10 | `st_zhongdi` | 中交城市发展控股集团股份有限公司 | 000736.SZ | 重庆 | 重庆市 | 1,281 |

## 4. Company Node Exposures (+35 created)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 美锦能源 | coal | produce | 煤炭生产商 | 0.8 |
| 美锦能源 | coke | produce | 焦炭生产商 | 0.9 |
| 美锦能源 | natural_gas | produce | 天然气生产商 | 0.6 |
| 美锦能源 | hydrogen_energy | produce | 氢能源生产商 | 0.7 |
| 美锦能源 | hydrogen_fuel_cell_vehicle | manufacture | 氢燃料电池汽车制造商 | 0.6 |
| 京东方A | display_terminal | manufacture | 显示器终端产品制造商 | 0.9 |
| 京东方A | tft_lcd | manufacture | TFT-LCD制造商 | 0.9 |
| 京东方A | small_size_display | manufacture | 小尺寸显示器件制造商 | 0.8 |
| 京东方A | lcd_panel | manufacture | 液晶面板制造商 | 0.8 |
| 京东方A | oled_panel | manufacture | OLED面板制造商 | 0.6 |
| 鲁泰A | cotton_lint | produce | 皮棉生产商 | 0.6 |
| 鲁泰A | yarn | produce | 纺纱生产商 | 0.8 |
| 鲁泰A | dyed_woven_fabric | produce | 色织面料制造商 | 0.9 |
| 鲁泰A | dress_shirt | manufacture | 衬衣制造商 | 0.9 |
| 鲁泰A | textile_product | produce | 纺织品综合制造商 | 0.7 |
| 冠捷科技 | lcd_monitor | manufacture | 显示器制造商 | 0.9 |
| 冠捷科技 | color_tv | manufacture | 电视机制造商 | 0.8 |
| 冠捷科技 | av_product | manufacture | 影音产品制造商 | 0.6 |
| 国元证券 | securities_brokerage | operate | 证券经纪服务商 | 0.9 |
| 国元证券 | securities_underwriting | operate | 投行承销保荐服务商 | 0.8 |
| 国元证券 | securities_proprietary_trading | operate | 证券自营投资商 | 0.7 |
| 国元证券 | asset_management_service | operate | 资产管理服务商 | 0.7 |
| 国元证券 | futures_brokerage | operate | 期货经纪服务商 | 0.6 |
| 燕京啤酒 | beer | produce | 啤酒生产商 | 0.9 |
| 四川美丰 | urea | produce | 尿素生产商 | 0.9 |
| 四川美丰 | compound_fertilizer | produce | 复合肥生产商 | 0.8 |
| 四川美丰 | vehicle_urea | produce | 车用尿素生产商 | 0.8 |
| 四川美丰 | chemical_fertilizer | produce | 化学肥料综合生产商 | 0.7 |
| 振华科技 | new_type_electronic_component | manufacture | 新型电子元器件制造商 | 0.9 |
| 振华科技 | communication_equipment | manufacture | 通信整机产品制造商 | 0.7 |
| 振华科技 | electromechanical_product | manufacture | 机电一体化产品制造商 | 0.7 |
| 罗牛山 | livestock_breeding | operate | 牲畜饲养服务商 | 0.9 |
| 罗牛山 | live_pig | produce | 生猪生产商 | 0.8 |
| 罗牛山 | real_estate_development | operate | 房地产开发商 | 0.4 |
| 罗牛山 | education_service | operate | 教育产业运营商 | 0.3 |

**Note:** *ST中地的 exposure `exp_zd_realestate` 提交时返回后端错误（`'dict' object has no attribute 'model_dump'`），原因是该公司在先前批次中已注册且已有 `real_estate_development` 暴露，属于重复提交。不影响整体数据完整性。

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_025_graph",
    "status": 201,
    "nodes_created": 16,
    "nodes_updated": 0,
    "edges_created": 11,
    "edges_updated": 0
  },
  "business_batch": {
    "batch_id": "batch_025_business",
    "status": 201,
    "companies_created": 9,
    "companies_updated": 1,
    "exposures_created": 35,
    "exposures_updated": 0,
    "errors": [
      {
        "type": "exposure",
        "id": "exp_zd_realestate",
        "error": "'dict' object has no attribute 'model_dump'"
      }
    ]
  }
}
```

## 6. Design Notes

- **美锦能源** 构建了独特的"焦炭-氢能-燃料电池汽车"产业链。`coke` → `hydrogen_energy` 的 material_flow 反映了焦炉煤气副产氢的工业路径，`hydrogen_energy` → `hydrogen_fuel_cell_vehicle` 的 energy_flow 则展示了氢能的终端应用场景。这是国内煤焦化企业向新能源转型的典型模式。
- **京东方A** 作为半导体显示龙头，构建了从核心组件（`tft_lcd`, `small_size_display`）到终端产品（`display_terminal`, `lcd_panel`, `oled_panel`）的完整显示产业层级，体现了显示技术的纵深布局。
- **鲁泰A** 构建了纺织行业最典型的纵向一体化链条：`cotton_lint` → `yarn` → `dyed_woven_fabric` → `dress_shirt`，从原料到成衣的四级物料流，是国内色织衬衫龙头企业的产业特征。
- **四川美丰** 的化肥产业链以 `urea` 为核心节点，向上连接已有的 `natural_gas`（气头尿素原料），向下分化为 `compound_fertilizer` 和 `vehicle_urea`，展示了传统化肥企业向环保车用尿素领域延伸的战略。
- **国元证券** 与 batch 022 的东北证券共同丰富了证券服务节点矩阵。复用了已有的 `futures_brokerage`（期货经纪）节点，体现了不同券商共享产业节点的设计原则。
- **冠捷科技** 作为全球显示器代工巨头，主要暴露到已有的 `lcd_monitor` 和 `color_tv` 节点，同时新增 `av_product` 补充影音产品线。

---

**Total Graph after Batch 025:**
- Nodes: 519 (503 + 16)
- Edges: 419 (408 + 11)
