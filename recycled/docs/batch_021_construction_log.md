# Batch 021 Construction Log

**Date:** 2026-05-25  
**Companies:** 000670.SZ – 000683.SZ (10 companies)  
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+22)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `smart_processor` | 智能处理器 | component |
| 2 | `mobile_terminal` | 移动互联终端 | device |
| 3 | `smart_home_device` | 智能家居设备 | device |
| 4 | `wearable_device` | 可穿戴设备 | device |
| 5 | `cement_product` | 水泥制品 | component |
| 6 | `digital_marketing_service` | 数字营销服务 | service |
| 7 | `internet_media_service` | 互联网媒体服务 | service |
| 8 | `viscose_staple` | 粘胶短丝 | material |
| 9 | `pulp_for_viscose` | 粘胶浆粕 | material |
| 10 | `canvas_fabric` | 帆布 | material |
| 11 | `tire_cord_fabric` | 帘子布 | material |
| 12 | `automotive_bearing` | 汽车轴承 | component |
| 13 | `bulldozer` | 推土机 | device |
| 14 | `excavator` | 挖掘机 | device |
| 15 | `road_roller` | 压路机 | device |
| 16 | `visual_content_service` | 视觉内容服务 | service |
| 17 | `stock_image` | 正版图片素材 | material |
| 18 | `power_dispatching_system` | 电力调度系统 | subsystem |
| 19 | `power_protection_system` | 电力保护系统 | subsystem |
| 20 | `power_automation_system` | 配电自动化系统 | subsystem |
| 21 | `natural_alkali` | 天然碱 | material |
| 22 | `baking_soda` | 小苏打 | material |

## 2. New Industrial Edges (+16)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_smart_processor_to_mobile_terminal` | smart_processor → mobile_terminal | composition |
| 2 | `flow_smart_processor_to_smart_home` | smart_processor → smart_home_device | composition |
| 3 | `flow_smart_processor_to_wearable` | smart_processor → wearable_device | composition |
| 4 | `flow_cement_to_cement_product` | cement → cement_product | material_flow |
| 5 | `flow_pulp_to_viscose_fiber` | pulp_for_viscose → viscose_fiber | material_flow |
| 6 | `flow_pulp_to_viscose_filament` | pulp_for_viscose → viscose_filament | material_flow |
| 7 | `flow_pulp_to_viscose_staple` | pulp_for_viscose → viscose_staple | material_flow |
| 8 | `flow_viscose_to_canvas` | viscose_fiber → canvas_fabric | material_flow |
| 9 | `flow_viscose_to_tire_cord` | viscose_fiber → tire_cord_fabric | material_flow |
| 10 | `flow_bearing_to_automotive_bearing` | bearing → automotive_bearing | composition |
| 11 | `flow_construction_machinery_to_bulldozer` | construction_machinery → bulldozer | composition |
| 12 | `flow_construction_machinery_to_excavator` | construction_machinery → excavator | composition |
| 13 | `flow_construction_machinery_to_road_roller` | construction_machinery → road_roller | composition |
| 14 | `flow_stock_image_to_visual_content` | stock_image → visual_content_service | service_flow |
| 15 | `flow_natural_alkali_to_soda_ash` | natural_alkali → soda_ash | material_flow |
| 16 | `flow_soda_ash_to_baking_soda` | soda_ash → baking_soda | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `yingfang_micro` | 盈方微电子股份有限公司 | 000670.SZ | 湖北 | 荆州市 | 133 |
| 2 | `shangfeng_cement` | 甘肃上峰水泥股份有限公司 | 000672.SZ | 甘肃 | 白银市 | 2,581 |
| 3 | `zhidu_share` | 智度科技股份有限公司 | 000676.SZ | 广东 | 广州市 | 456 |
| 4 | `st_hailong` | 恒天海龙股份有限公司 | 000677.SZ | 山东 | 潍坊市 | 984 |
| 5 | `xiangyang_bearing` | 襄阳汽车轴承股份有限公司 | 000678.SZ | 湖北 | 襄阳市 | 2,486 |
| 6 | `dalian_friendship` | 大连友谊(集团)股份有限公司 | 000679.SZ | 辽宁 | 大连市 | 332 |
| 7 | `shantui_share` | 山推工程机械股份有限公司 | 000680.SZ | 山东 | 济宁市 | 7,247 |
| 8 | `visual_china` | 视觉(中国)文化发展股份有限公司 | 000681.SZ | 江苏 | 常州市 | 466 |
| 9 | `dongfang_electronics` | 东方电子股份有限公司 | 000682.SZ | 山东 | 烟台市 | 8,153 |
| 10 | `boyuan_chemical` | 内蒙古博源化工股份有限公司 | 000683.SZ | 内蒙古 | 鄂尔多斯市 | 4,755 |

## 4. Company Node Exposures (+35)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 盈方微 | smart_processor | manufacture | 智能处理器设计制造商 | 0.9 |
| 盈方微 | semiconductor_device | manufacture | 集成电路芯片研发商 | 0.8 |
| 盈方微 | mobile_terminal | design | 移动终端解决方案提供商 | 0.6 |
| 盈方微 | smart_home_device | design | 智能家居解决方案提供商 | 0.5 |
| 盈方微 | wearable_device | design | 可穿戴设备解决方案提供商 | 0.5 |
| 上峰水泥 | cement | produce | 水泥生产商 | 0.9 |
| 上峰水泥 | cement_product | produce | 水泥制品生产商 | 0.8 |
| 智度股份 | internet_media_service | operate | 互联网媒体运营商 | 0.8 |
| 智度股份 | digital_marketing_service | operate | 数字营销服务商 | 0.8 |
| 智度股份 | advertising_service | operate | 广告服务运营商 | 0.6 |
| ST海龙 | viscose_fiber | produce | 粘胶纤维生产商 | 0.9 |
| ST海龙 | viscose_filament | produce | 粘胶长丝生产商 | 0.9 |
| ST海龙 | viscose_staple | produce | 粘胶短丝生产商 | 0.9 |
| ST海龙 | pulp_for_viscose | produce | 粘胶浆粕生产商 | 0.8 |
| ST海龙 | canvas_fabric | produce | 帆布生产商 | 0.7 |
| ST海龙 | tire_cord_fabric | produce | 帘子布生产商 | 0.7 |
| 襄阳轴承 | bearing | manufacture | 轴承制造商 | 0.9 |
| 襄阳轴承 | rolling_bearing | manufacture | 滚动轴承制造商 | 0.9 |
| 襄阳轴承 | automotive_bearing | manufacture | 汽车轴承制造商 | 0.8 |
| 大连友谊 | department_store | operate | 百货零售商 | 0.8 |
| 大连友谊 | hotel_operation_service | operate | 酒店运营商 | 0.6 |
| 大连友谊 | real_estate_development | operate | 房地产开发商 | 0.5 |
| 山推股份 | bulldozer | manufacture | 推土机制造商 | 0.9 |
| 山推股份 | excavator | manufacture | 挖掘机制造商 | 0.8 |
| 山推股份 | road_roller | manufacture | 压路机制造商 | 0.8 |
| 山推股份 | construction_machinery | manufacture | 工程机械综合制造商 | 0.9 |
| 视觉中国 | visual_content_service | provide_service | 视觉内容服务商 | 0.9 |
| 视觉中国 | stock_image | provide_service | 正版图片素材提供商 | 0.9 |
| 东方电子 | power_dispatching_system | manufacture | 电力调度系统制造商 | 0.9 |
| 东方电子 | power_protection_system | manufacture | 电力保护系统制造商 | 0.9 |
| 东方电子 | power_automation_system | manufacture | 配电自动化系统制造商 | 0.9 |
| 东方电子 | power_distribution_equipment | manufacture | 配电设备制造商 | 0.7 |
| 博源化工 | natural_alkali | produce | 天然碱生产商 | 0.9 |
| 博源化工 | soda_ash | produce | 纯碱生产商 | 0.9 |
| 博源化工 | baking_soda | produce | 小苏打生产商 | 0.9 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_021_graph",
    "status": 201,
    "nodes_created": 22,
    "nodes_updated": 0,
    "edges_created": 16,
    "edges_updated": 0
  },
  "business_batch": {
    "batch_id": "batch_021_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 35,
    "exposures_updated": 0
  }
}
```

## 6. Design Notes

- **盈方微** 的智能处理器产业链展示了芯片设计企业如何连接到下游终端设备（移动终端、智能家居、可穿戴设备），通过 `smart_processor` 作为核心组件节点串联三条产品线。
- **ST海龙** 的粘胶纤维产业链完整地构建了从 `pulp_for_viscose`（浆粕）→ `viscose_fiber`/`viscose_filament`/`viscose_staple` → `canvas_fabric`/`tire_cord_fabric` 的物料流，体现了传统纺织化工的上下游关系。
- **视觉中国** 构建了独特的视觉内容服务产业链：`stock_image`（素材）→ `visual_content_service`（服务），将数字内容资产化。
- **东方电子** 聚焦于电力系统三大子系统（调度、保护、自动化），反映了电网智能化的核心需求。
- **博源化工** 以天然碱为起点，延伸出 `natural_alkali` → `soda_ash` → `baking_soda` 的碱化工链条。

---

**Total Graph after Batch 021:**
- Nodes: 448 (426 + 22)
- Edges: 374 (358 + 16)
