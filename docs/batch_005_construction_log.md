# Batch 005 产业图与公司视图构建日志

**构建时间**: 2026-05-23
**数据来源**: `data/stock_batches/batch_005.json`
**涉及公司**: 10家中国公司

---

## 一、准备与查询

### 已有实体查询
在构建前，查询了系统中已有的产业节点（171个）和公司（40家）。
关键已有节点包括：
- `precious_metal`（贵金属）— 可用于中金岭南伴生金银
- `agricultural_product`（农产品）— 农产品批发市场的上游
- `semiconductor_device`（半导体器件）— 华强分销、长城电脑、特发设备的上游
- `communication_device` / `network_equipment` / `mobile_phone` — 中兴已有节点
- `construction_service` — 北方国际直接复用
- `laptop_computer` / `server_hardware` — 长城电脑产品线
- `steel_sheet` — 华控赛格环保设备原材料
- `packaging_material` — 华侨城纸包装上游
- `quartz_sand` / `aluminum_panel` — 特发信息原材料
- `pharmaceutical_raw_material` / `food_ingredient` / `pharmaceutical_distribution` — 海王医药链

### 数据来源
- **Tushare**: 获取了公司基本财务指标和员工数据。
- **年报/公开资料**: 节点和边的证据引用均来自公司2024年年报或产业常识。

---

## 二、产业图构建

### 新建产业节点（19个）

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **铅锌链** | lead_zinc_ore | 铅锌矿石 | material | 中金岭南 |
| **铅锌链** | lead_zinc_metal | 铅锌金属 | material | 中金岭南 |
| **铅锌链** | sulfuric_acid | 工业硫酸 | material | 中金岭南 |
| **农批** | agricultural_wholesale_service | 农产品批发服务 | service | 农产品 |
| **分销** | electronic_component_distribution_service | 电子元器件分销服务 | service | 深圳华强 |
| **通信** | telecom_software | 电信软件 | application_system | 中兴通讯 |
| **电脑** | desktop_computer | 台式电脑 | device | 中国长城 |
| **电脑** | computer_peripheral | 电脑外设 | device | 中国长城 |
| **环保** | environmental_protection_equipment | 环保设备 | device | 华控赛格 |
| **环保** | environmental_protection_material | 环保材料 | material | 华控赛格 |
| **旅游** | tourism_service | 旅游服务 | service | 华侨城A |
| **包装** | paper_packaging_product | 纸包装制品 | component | 华侨城A |
| **光通信** | optical_fiber_cable | 光缆 | component | 特发信息 |
| **光通信** | optical_transmission_equipment | 光传输设备 | device | 特发信息 |
| **电子** | electronic_capacitor | 电子电容器 | component | 特发信息 |
| **电子** | cable_tv_equipment | 有线电视设备 | device | 特发信息 |
| **医药** | traditional_chinese_medicine | 中成药 | material | ST海王 |
| **医药** | biological_drug | 生物药 | material | ST海王 |
| **医药** | dietary_supplement | 膳食补充剂 | material | ST海王 |

### 复用已有节点
- `precious_metal` — 中金岭南伴生金银复用
- `communication_device` / `network_equipment` / `mobile_phone` — 中兴通讯直接复用，未新建通信节点
- `construction_service` — 北方国际直接复用
- `laptop_computer` / `server_hardware` — 中国长城复用
- `residential_property` / `commercial_property` — 华侨城A复用
- `pharmaceutical_product` / `pharmaceutical_distribution` — ST海王复用

### 新建产业流边（17条）

1. **铅锌链**: lead_zinc_ore → lead_zinc_metal（冶炼）
2. **铅锌链**: lead_zinc_ore → sulfuric_acid（副产硫酸）
3. **铅锌链**: lead_zinc_ore → precious_metal（伴生回收）
4. **农批**: agricultural_product → agricultural_wholesale_service（流通服务）
5. **分销**: semiconductor_device → electronic_component_distribution_service（分销服务）
6. **电脑**: semiconductor_device → desktop_computer（组成关系）
7. **电脑**: semiconductor_device → computer_peripheral（组成关系）
8. **环保**: steel_sheet → environmental_protection_equipment（原材料）
9. **包装**: packaging_material → paper_packaging_product（加工关系）
10. **光通信**: quartz_sand → optical_fiber_cable（光纤原料）
11. **光通信**: optical_fiber_cable → optical_transmission_equipment（系统组成）
12. **电子**: aluminum_panel → electronic_capacitor（电容原料）
13. **电子**: electronic_capacitor → cable_tv_equipment（器件组成）
14. **电子**: semiconductor_device → cable_tv_equipment（芯片组成）
15. **医药**: pharmaceutical_raw_material → traditional_chinese_medicine（原料药→中成药）
16. **医药**: pharmaceutical_raw_material → biological_drug（原料药→生物药）
17. **医药**: food_ingredient → dietary_supplement（食品原料→保健品）

---

## 三、公司视图构建

### 10家公司全部创建成功

| 股票代码 | 公司名 | 公司ID | 核心产业 |
|---|---|---|---|
| 000060.SZ | 中金岭南 | zhongjin_lingnan | 铅锌采选冶 |
| 000061.SZ | 农产品 | nongchanpin | 农产品批发市场运营 |
| 000062.SZ | 深圳华强 | shenzhen_huaqiang | 电子元器件分销 |
| 000063.SZ | 中兴通讯 | zte | 通信设备与终端 |
| 000065.SZ | 北方国际 | norinco_international | 国际工程承包 |
| 000066.SZ | 中国长城 | china_greatwall | 电脑及外设（信创） |
| 000068.SZ | 华控赛格 | huakong_saige | 环保设备及材料 |
| 000069.SZ | 华侨城A | overseas_chinese_town | 旅游综合、房地产、纸包装 |
| 000070.SZ | 特发信息 | teli_information | 光缆、光传输设备、电容器 |
| 000078.SZ | ST海王 | st_neptunus | 医药制造与流通 |

### 公司节点暴露（30条）

| 公司 | 暴露节点数 | 关键暴露 |
|---|---|---|
| 中金岭南 | 4 | lead_zinc_ore (produce), lead_zinc_metal (manufacture), sulfuric_acid (manufacture), precious_metal (manufacture) |
| 农产品 | 1 | agricultural_wholesale_service (provide_service) |
| 深圳华强 | 1 | electronic_component_distribution_service (provide_service) |
| 中兴通讯 | 4 | communication_device (manufacture), network_equipment (manufacture), mobile_phone (manufacture), telecom_software (provide_service) |
| 北方国际 | 1 | construction_service (provide_service) |
| 中国长城 | 4 | desktop_computer (manufacture), laptop_computer (manufacture), computer_peripheral (manufacture), server_hardware (manufacture) |
| 华控赛格 | 2 | environmental_protection_equipment (manufacture), environmental_protection_material (manufacture) |
| 华侨城A | 4 | tourism_service (operate), residential_property (produce), commercial_property (produce), paper_packaging_product (manufacture) |
| 特发信息 | 4 | optical_fiber_cable (manufacture), optical_transmission_equipment (manufacture), electronic_capacitor (manufacture), cable_tv_equipment (manufacture) |
| ST海王 | 5 | pharmaceutical_distribution (provide_service), pharmaceutical_product (manufacture), traditional_chinese_medicine (manufacture), biological_drug (manufacture), dietary_supplement (manufacture) |

---

## 四、系统状态更新

```
Total nodes: 190 (+19)
Total edges: 173 (+17)
Total companies: 50 (+10)
Total exposures: 135 (+30)
```

---

## 五、关键发现与启发

### 1. 铅锌产业链的补全
- 已有节点中缺乏有色金属采选冶的基础节点。batch_005通过中金岭南补全了 `lead_zinc_ore → lead_zinc_metal` 的核心链条，并延伸出 `sulfuric_acid` 和 `precious_metal` 副产品分支。
- 这为后续铜、铝等其他有色金属公司建立了参考模板。

### 2. 通信设备节点的复用策略
- 中兴通讯业务极广（无线、有线、光通信、终端、软件），但已有节点 `communication_device`、`network_equipment`、`mobile_phone` 已能覆盖其核心硬件产品线。
- 仅新建了 `telecom_software` 以补充软件维度，避免节点过度膨胀。
- 这说明产业图的构建应以**已有节点的饱和度**为判断标准，而非公司业务的完整映射。

### 3. 服务型企业的节点暴露特点
- 深圳华强（分销）、农产品（批发）、北方国际（工程承包）这类服务型企业，其暴露节点均为 **service** 类型节点，而非物理产品节点。
- 这与产业图"仅表达实体和服务关系"的原则一致：分销平台本身不是产品，而是使产品流通的**服务**。

### 4. 多元化企业的产业聚焦
- 华侨城A横跨旅游、房地产、纸包装三大产业，暴露节点覆盖了全部三个维度。但纸包装的权重设为0.5，反映了其非核心业务地位。
- 特发信息同时做光缆、光设备、电容器和有线电视设备，看似分散，实则围绕"光通信+电子元器件"两大技术底座，暴露权重均较高（0.8-1.0）。

### 5. ST公司的处理
- ST海王虽然带ST标识，但其医药制造和流通业务链条清晰，产业节点暴露完整。系统不因公司财务状态（ST）而降低产业节点构建的完整性。

---

## 六、后续批次建议

1. **新能源发电**: batch_006中的川能动力（风电、光伏）可复用 `wind_power_generation`、`solar_power_generation` 节点。
2. **港口/机场基础设施**: batch_006中的盐田港、深圳机场属于基础设施运营服务，可能需要新建 `port_operation_service` 和 `airport_operation_service`。
3. **半导体显示**: batch_006中的TCL科技涉及半导体显示，可复用已有 `lcd_panel` 等节点。
