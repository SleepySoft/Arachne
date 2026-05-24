# Batch 011 产业图构建日志

## 批次信息
- **批次号**: batch_011
- **处理日期**: 2026-05-24
- **公司数量**: 10家

## 公司列表
| 股票代码 | 公司名称 | 行业 | 地区 |
|---------|---------|------|------|
| 000518.SZ | 四环生物 | 生物制药 | 江苏无锡 |
| 000519.SZ | 中兵红箭 | 专用机械 | 河南南阳 |
| 000520.SZ | 凤凰航运 | 水运 | 湖北武汉 |
| 000521.SZ | 长虹美菱 | 家用电器 | 安徽合肥 |
| 000523.SZ | 红棉股份 | 食品 | 广东广州 |
| 000524.SZ | 岭南控股 | 旅游服务 | 广东广州 |
| 000525.SZ | 红太阳 | 农药化肥 | 江苏南京 |
| 000526.SZ | 学大教育 | 文教休闲 | 福建厦门 |
| 000528.SZ | 柳工 | 工程机械 | 广西柳州 |
| 000529.SZ | 广弘控股 | 食品 | 广东广州 |

## 已有实体检查
在构建前查询了系统中已有节点（235个）和边（190条）。其中6家公司已存在于系统中（广弘控股、柳工、红太阳、学大教育、岭南控股、红棉股份），采用upsert策略更新其信息并补充暴露关系。

## 新增产业节点（19个）
- **机械零部件**: cylinder_liner（气缸套）、aluminum_piston（铝活塞）
- **军工产品**: artillery_shell（炮弹）、rocket（火箭弹）、missile（导弹）
- **车辆**: modified_vehicle（改装车）、special_purpose_vehicle（专用车）
- **航运**: vessel（船舶）、vessel_repair_service（船舶维修服务）、pilotage_service（引航服务）、freight_forwarding_service（货运代理服务）
- **化工原料**: sulfonic_acid（磺酸）、glycerin（甘油）、aes_surfactant（AES表面活性剂）
- **旅游服务**: business_travel_service（商旅服务）、scenic_area_service（景区服务）、car_rental_service（汽车租赁服务）
- **冷链**: cold_storage_equipment（冷藏设备）、cold_storage_facility（冷藏设施）

## 新增产业边（20条）
重点构建了以下产业链关系：
- 钢材→气缸套/炮弹/火箭弹/导弹（material_flow）
- 铝合金→铝活塞（material_flow）
- 石化产品→磺酸/AES（material_flow）
- 磺酸/甘油/AES→洗涤剂（material_flow）
- 船舶→航运服务/维修服务（service_flow）
- 旅游服务→商旅/景区/汽车租赁（service_flow）
- 制冷压缩机→冷藏设备（composition）
- 冷藏设备/设施→食品冷链服务（capability_supply）

## 公司视图设计
每家公司根据其主营业务映射到相应的产业节点：
- **四环生物**: biological_drug(manufacture)、traditional_chinese_medicine(manufacture)、greening_construction_service(provide_service)
- **中兵红箭**: cylinder_liner、aluminum_piston、superhard_material、artillery_shell、rocket、missile（均为manufacture）
- **凤凰航运**: shipping_service(operate)、vessel_repair_service、pilotage_service、freight_forwarding_service、logistics_service（均为provide_service）
- **长虹美菱**: refrigerator、air_conditioner、washing_machine、kitchen_appliance、small_home_appliance、medical_cold_storage（均为manufacture）
- **红棉股份**: detergent、sulfonic_acid、glycerin、aes_surfactant（均为manufacture）
- **岭南控股**: business_travel_service、hotel_operation_service、catering_service、exhibition_service、scenic_area_service、car_rental_service
- **红太阳**: pesticide、chemical_fertilizer（均为manufacture）
- **学大教育**: education_service(provide_service)
- **柳工**: construction_machinery(manufacture)
- **广弘控股**: food_cold_chain_service(operate)、cold_storage_equipment(manufacture)、cold_storage_facility(operate)

## 提交结果
- Graph Batch: 19节点创建，20边创建，0错误
- Business Batch: 10公司更新/创建，39暴露创建/更新，0错误

## 发现与启发
1. **中兵红箭的业务特殊性**: 该公司横跨内燃机配件、超硬材料和军品三大领域，产业跨度极大。军品节点（炮弹、火箭弹、导弹）在产业图中属于新增，其原材料主要是钢材，这与一般机械制造业共享上游供应链。
2. **红棉股份的化工原料产出**: 该公司不仅生产终端消费品（洗涤剂），还生产上游化工原料（磺酸、AES、甘油），在产业图中同时占据中游和下游位置。
3. **航运服务业节点设计**: 凤凰航运的业务涵盖船舶租赁、维修、引航、货代和综合物流，需要拆分出多个服务节点才能准确表达其业务全貌。
4. **已存在公司的处理**: 系统中已有6家公司的记录，通过upsert机制更新了其公司信息，并补充了新的暴露关系。这种设计避免了重复创建，保持了数据一致性。
