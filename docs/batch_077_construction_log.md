# Batch 077 Construction Log

**Date:** 2026-05-25
**Companies:** 600490.SH – 600501.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `nonferrous_metal_mining` | 有色金属采选 | service |
| 2 | `civil_construction` | 土建施工 | service |
| 3 | `textile_weaving` | 纺织织造 | service |
| 4 | `train_axle` | 车轴 | component |
| 5 | `agricultural_machinery` | 农业机械 | system |
| 6 | `germanium_product` | 锗产品 | material |
| 7 | `data_network_product` | 数据网络产品 | device |
| 8 | `pressure_vessel` | 压力容器 | device |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `train_axle_to_rail_transit` | train_axle → rail_transit | composition |
| 2 | `germanium_product_to_semiconductor` | germanium_product → semiconductor | material_flow |
| 3 | `pressure_vessel_to_chemical_industry` | pressure_vessel → chemical_industry | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `pengxin_resources` | 鹏欣环球资源股份有限公司 | 600490.SH | 上海 | 上海市 |
| 2 | `st_longyuan` | 龙元建设集团股份有限公司 | 600491.SH | 浙江 | 宁波市 |
| 3 | `fengzhu_textile` | 福建凤竹纺织科技股份有限公司 | 600493.SH | 福建 | 泉州市 |
| 4 | `jinxi_axle` | 晋西车轴股份有限公司 | 600495.SH | 山西 | 太原市 |
| 5 | `jinggong_steel` | 长江精工钢结构(集团)股份有限公司 | 600496.SH | 安徽 | 六安市 |
| 6 | `chihong` | 云南驰宏锌锗股份有限公司 | 600497.SH | 云南 | 曲靖市 |
| 7 | `fiberhome` | 烽火通信科技股份有限公司 | 600498.SH | 湖北 | 武汉市 |
| 8 | `keda_manufacturing` | 科达制造股份有限公司 | 600499.SH | 广东 | 佛山市 |
| 9 | `sinochem_intl` | 中化国际(控股)股份有限公司 | 600500.SH | 上海 | 上海市 |
| 10 | `aerosun` | 航天晨光股份有限公司 | 600501.SH | 江苏 | 南京市 |

## 4. Company Node Exposures (+28)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 鹏欣资源 | nonferrous_metal_mining | operate | 有色金属采选运营商 | 0.95 |
| 鹏欣资源 | nonferrous_metal | produce | 有色金属生产商 | 0.95 |
| 鹏欣资源 | precious_metal | produce | 贵金属生产商 | 0.9 |
| ST龙元 | civil_construction | operate | 土建施工运营商 | 0.95 |
| ST龙元 | construction | operate | 建筑施工运营商 | 0.9 |
| ST龙元 | building_design | provide_service | 建筑设计服务商 | 0.85 |
| 凤竹纺织 | textile_weaving | operate | 纺织织造运营商 | 0.95 |
| 凤竹纺织 | textile_product | produce | 纺织品生产商 | 0.9 |
| 凤竹纺织 | wastewater_treatment | operate | 污水处理运营商 | 0.85 |
| 晋西车轴 | train_axle | manufacture | 车轴制造商 | 0.95 |
| 晋西车轴 | rail_transit_equipment | manufacture | 轨道交通设备制造商 | 0.9 |
| 精工钢构 | steel_structure | produce | 钢结构生产商 | 0.95 |
| 精工钢构 | agricultural_machinery | manufacture | 农业机械制造商 | 0.9 |
| 驰宏锌锗 | zinc_product | produce | 锌产品生产商 | 0.95 |
| 驰宏锌锗 | lead_product | produce | 铅产品生产商 | 0.9 |
| 驰宏锌锗 | silver_product | produce | 银产品生产商 | 0.9 |
| 驰宏锌锗 | germanium_product | produce | 锗产品生产商 | 0.85 |
| 烽火通信 | communication_equipment | manufacture | 通信设备制造商 | 0.95 |
| 烽火通信 | optical_fiber_cable | manufacture | 光纤光缆制造商 | 0.95 |
| 烽火通信 | data_network_product | manufacture | 数据网络产品制造商 | 0.9 |
| 科达制造 | ceramic_machinery | manufacture | 陶瓷机械制造商 | 0.95 |
| 科达制造 | chinese_patent_medicine | produce | 中药产品生产商 | 0.85 |
| 中化国际 | chemical_logistics | provide_service | 化工物流服务商 | 0.9 |
| 中化国际 | plastic_raw_material | produce | 塑料原料生产商 | 0.9 |
| 中化国际 | rubber_product | produce | 橡胶制品生产商 | 0.85 |
| 航天晨光 | special_vehicle | manufacture | 专用车制造商 | 0.95 |
| 航天晨光 | bellows | manufacture | 波纹管制造商 | 0.9 |
| 航天晨光 | pressure_vessel | manufacture | 压力容器制造商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
