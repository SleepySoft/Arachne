# Batch 023 Construction Log

**Date:** 2026-05-25  
**Companies:** 000700.SZ – 000711.SZ (10 companies)  
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+27)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `automotive_bumper` | 汽车保险杠 | component |
| 2 | `automotive_molding_trim` | 汽车装饰件 | component |
| 3 | `electronic_information_service` | 电子信息服务 | service |
| 4 | `feed` | 饲料 | material |
| 5 | `meat_product` | 肉食品 | material |
| 6 | `polyester_chip` | 聚酯切片 | material |
| 7 | `polyester_bottle_chip` | 聚酯瓶片 | material |
| 8 | `poy` | 涤纶预取向丝 | material |
| 9 | `fdy` | 涤纶全拉伸丝 | material |
| 10 | `dty` | 涤纶拉伸变形丝 | material |
| 11 | `polyester_staple` | 涤纶短纤 | material |
| 12 | `ammonium_chloride` | 氯化铵 | material |
| 13 | `special_steel` | 特殊钢材 | material |
| 14 | `gear_steel` | 齿轮钢 | material |
| 15 | `bearing_steel` | 轴承钢 | material |
| 16 | `spring_steel` | 弹簧钢 | material |
| 17 | `tool_die_steel` | 工模具钢 | material |
| 18 | `high_temperature_alloy_steel` | 高温合金钢 | material |
| 19 | `steel_plate` | 板材 | material |
| 20 | `steel_bar` | 棒材 | material |
| 21 | `steel_wire_rod` | 线材 | material |
| 22 | `steel_section` | 型材 | material |
| 23 | `genetic_testing_service` | 基因检测服务 | service |
| 24 | `gene_sequencing_equipment` | 基因测序设备 | device |
| 25 | `gene_sequencing_reagent` | 基因测序试剂 | material |
| 26 | `smart_ecological_operation` | 智慧生态运营 | service |
| 27 | `clean_energy_service` | 清洁能源服务 | service |

## 2. New Industrial Edges (+18, 1 updated)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `flow_bumper_to_car` | automotive_bumper → passenger_car | composition |
| 2 | `flow_trim_to_car` | automotive_molding_trim → passenger_car | composition |
| 3 | `flow_feed_to_pig` | feed → live_pig | material_flow |
| 4 | `flow_pig_to_meat` | live_pig → meat_product | material_flow |
| 5 | `flow_pta_to_chip` | pta → polyester_chip | material_flow |
| 6 | `flow_chip_to_filament` | polyester_chip → polyester_filament | material_flow |
| 7 | `flow_chip_to_staple` | polyester_chip → polyester_staple | material_flow |
| 8 | `flow_chip_to_bottle_chip` | polyester_chip → polyester_bottle_chip | material_flow |
| 9 | `flow_poy_to_fdy` | poy → fdy | material_flow |
| 10 | `flow_poy_to_dty` | poy → dty | material_flow |
| 11 | `flow_salt_to_soda` | salt_product → soda_ash | material_flow |
| 12 | `flow_soda_to_ammonium` | soda_ash → ammonium_chloride | material_flow |
| 13 | `is_a_gear_steel` | gear_steel → special_steel | is_a (ontology) |
| 14 | `is_a_bearing_steel` | bearing_steel → special_steel | is_a (ontology) |
| 15 | `is_a_spring_steel` | spring_steel → special_steel | is_a (ontology) |
| 16 | `is_a_tool_die_steel` | tool_die_steel → special_steel | is_a (ontology) |
| 17 | `is_a_ht_alloy_steel` | high_temperature_alloy_steel → special_steel | is_a (ontology) |
| 18 | `flow_reagent_to_testing` | gene_sequencing_reagent → genetic_testing_service | service_flow |
| 19 | `flow_equipment_to_testing` | gene_sequencing_equipment → genetic_testing_service | capability_supply |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City | Employees |
|---|-----------|------|-----------|----------|------|-----------|
| 1 | `mosu_tech` | 江南模塑科技股份有限公司 | 000700.SZ | 江苏 | 无锡市 | 5,880 |
| 2 | `xiamen_xinda` | 厦门信达股份有限公司 | 000701.SZ | 福建 | 厦门市 | 3,998 |
| 3 | `zhenghong_tech` | 湖南正虹科技发展股份有限公司 | 000702.SZ | 湖南 | 岳阳市 | 639 |
| 4 | `hengyi_petrochemical` | 恒逸石化股份有限公司 | 000703.SZ | 广西 | 钦州市 | 16,014 |
| 5 | `zhejiang_zhenyuan` | 浙江震元股份有限公司 | 000705.SZ | 浙江 | 绍兴市 | 2,073 |
| 6 | `shuanghuan_tech` | 湖北双环科技股份有限公司 | 000707.SZ | 湖北 | 孝感市 | 1,222 |
| 7 | `citic_special_steel` | 中信泰富特钢集团股份有限公司 | 000708.SZ | 湖北 | 黄石市 | 31,584 |
| 8 | `hegang_share` | 河钢股份有限公司 | 000709.SZ | 河北 | 石家庄市 | 29,939 |
| 9 | `berry_genomics` | 成都市贝瑞和康基因技术股份有限公司 | 000710.SZ | 四川 | 成都市 | 1,402 |
| 10 | `st_jinglan` | 铟靶新材(哈尔滨)股份有限公司 | 000711.SZ | 黑龙江 | 哈尔滨市 | 537 |

## 4. Company Node Exposures (+39)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 模塑科技 | automotive_bumper | manufacture | 汽车保险杠制造商 | 0.9 |
| 模塑科技 | automotive_molding_trim | manufacture | 汽车装饰件制造商 | 0.9 |
| 模塑科技 | medical_device | manufacture | 医疗器械制造商 | 0.4 |
| 厦门信达 | electronic_information_service | operate | 电子信息服务商 | 0.7 |
| 厦门信达 | trade_service | operate | 贸易商 | 0.7 |
| 厦门信达 | real_estate_development | operate | 房地产开发商 | 0.5 |
| 正虹科技 | feed | produce | 饲料生产商 | 0.9 |
| 正虹科技 | meat_product | produce | 肉食品生产商 | 0.8 |
| 正虹科技 | live_pig | produce | 生猪养殖商 | 0.6 |
| 恒逸石化 | pta | produce | PTA生产商 | 0.9 |
| 恒逸石化 | polyester_chip | produce | 聚酯切片生产商 | 0.9 |
| 恒逸石化 | polyester_bottle_chip | produce | 聚酯瓶片生产商 | 0.8 |
| 恒逸石化 | poy | produce | 涤纶预取向丝生产商 | 0.9 |
| 恒逸石化 | fdy | produce | 涤纶全拉伸丝生产商 | 0.9 |
| 恒逸石化 | dty | produce | 涤纶拉伸变形丝生产商 | 0.9 |
| 恒逸石化 | polyester_staple | produce | 涤纶短纤生产商 | 0.8 |
| 恒逸石化 | polyester_filament | produce | 涤纶长丝生产商 | 0.8 |
| 浙江震元 | pharmaceutical_distribution | operate | 医药批发分销商 | 0.8 |
| 浙江震元 | pharmaceutical_retail | operate | 医药零售商 | 0.7 |
| 浙江震元 | pharmaceutical_product | manufacture | 医药产品制造商 | 0.6 |
| 双环科技 | soda_ash | produce | 纯碱生产商 | 0.9 |
| 双环科技 | ammonium_chloride | produce | 氯化铵生产商 | 0.8 |
| 中信特钢 | special_steel | produce | 特殊钢材综合制造商 | 0.9 |
| 中信特钢 | gear_steel | produce | 齿轮钢制造商 | 0.8 |
| 中信特钢 | bearing_steel | produce | 轴承钢制造商 | 0.8 |
| 中信特钢 | spring_steel | produce | 弹簧钢制造商 | 0.8 |
| 中信特钢 | tool_die_steel | produce | 工模具钢制造商 | 0.8 |
| 中信特钢 | high_temperature_alloy_steel | produce | 高温合金钢制造商 | 0.7 |
| 河钢股份 | steel_plate | produce | 板材生产商 | 0.9 |
| 河钢股份 | steel_bar | produce | 棒材生产商 | 0.8 |
| 河钢股份 | steel_wire_rod | produce | 线材生产商 | 0.8 |
| 河钢股份 | steel_section | produce | 型材生产商 | 0.8 |
| 河钢股份 | steel_sheet | produce | 冷轧钢板生产商 | 0.6 |
| 贝瑞基因 | genetic_testing_service | provide_service | 基因检测服务商 | 0.9 |
| 贝瑞基因 | gene_sequencing_equipment | manufacture | 基因测序设备销售商 | 0.7 |
| 贝瑞基因 | gene_sequencing_reagent | manufacture | 基因测序试剂销售商 | 0.7 |
| ST京蓝 | smart_ecological_operation | operate | 智慧生态运营商 | 0.8 |
| ST京蓝 | clean_energy_service | operate | 清洁能源综合服务商 | 0.7 |
| ST京蓝 | solid_waste_treatment | operate | 固废治理运营商 | 0.6 |

## 5. API Submission Results

```json
{
  "graph_batch": {
    "batch_id": "batch_023_graph",
    "status": 201,
    "nodes_created": 27,
    "nodes_updated": 0,
    "edges_created": 18,
    "edges_updated": 1,
    "errors": []
  },
  "business_batch": {
    "batch_id": "batch_023_business",
    "status": 201,
    "companies_created": 10,
    "companies_updated": 0,
    "exposures_created": 39,
    "exposures_updated": 0
  }
}
```

## 6. Design Notes

- **恒逸石化** 的聚酯产业链是本批次最复杂的物料流网络。以 `pta` 为起点，经过 `polyester_chip`（聚酯切片）分化为三条支线：涤纶长丝（POY→FDY/DTY）、涤纶短纤和聚酯瓶片。完整覆盖了PTA-聚酯-化纤/瓶片的产业链。
- **中信特钢** 构建了特钢领域的本体分类体系。以 `special_steel` 为父节点，通过5条 ontology `is_a` 边连接齿轮钢、轴承钢、弹簧钢、工模具钢和高温合金钢，实现了概念层级的精确表达。
- **正虹科技** 构建了"饲料→生猪→肉食品"的农业产业化链条，从上游投入品到下游消费品形成完整闭环。
- **贝瑞基因** 的基因检测服务链展示了"设备+试剂+服务"的三角关系：`gene_sequencing_equipment` 提供 capability，`gene_sequencing_reagent` 提供 service_flow，`genetic_testing_service` 作为核心服务节点。
- **河钢股份** 作为普钢代表，与中信特钢（特钢）形成互补，覆盖了板材、棒材、线材、型材四大普钢品类。

---

**Total Graph after Batch 023:**
- Nodes: 492 (465 + 27)
- Edges: 399 (381 + 18)
