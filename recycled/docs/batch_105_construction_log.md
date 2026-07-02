# Batch 105 产业图构建日志

## 批次信息
- **批次号**: 105
- **股票代码范围**: 600826.SH - 600838.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_105_nodes`)：补充6个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_105_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：6个（`supermarket_chain`, `pawnbroking_service`, `pharmaceutical_wholesale`, `metro_operation`, `elevator`, `daily_chemical_product`）
- 节点更新：1个（`escalator` 已在batch_104中创建，batch_105中复用并确认）
- 新建产业边：1条
- 新建公司：10家
- 新建暴露关系：19条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `supermarket_chain` | 超市连锁 | service | 通过统一品牌、统一采购、统一管理和统一配送体系，在多个地点开设分店进行商品零售的连锁经营模式，销售品类涵盖食品、日用品、生鲜、家电等。 |
| `pawnbroking_service` | 典当服务 | service | 以货币借贷为经营方式，以物品质押为融资条件，向当户提供短期、小额、快速的融资服务，并在约定期限内由当户赎回当物的特种金融服务。 |
| `pharmaceutical_wholesale` | 医药批发 | service | 药品经营企业从药品生产企业或其他药品批发企业采购药品，再销售给药品零售企业、医疗机构或其他药品使用单位的药品流通环节服务。 |
| `metro_operation` | 地铁运营 | service | 对城市地铁系统进行日常运营管理和维护的服务活动，包括列车调度运行、车站管理、票务服务、设备维护、安全保障等，为城市公共交通提供大运量、快速、准点的轨道客运服务。 |
| `elevator` | 电梯 | device | 以电力驱动、沿固定导轨运行的箱式垂直运输设备，用于建筑物内人员或货物的升降运送，是高层建筑中不可或缺的垂直交通设施。 |
| `daily_chemical_product` | 日用化工产品 | material | 用于日常生活清洁、护理、美化等用途的化学制品，包括洗涤剂、洗衣粉、洗洁精、化妆品、口腔护理用品、消杀用品等。 |

## 新增边详情

| edge_id | from_node | to_node | edge_type | description |
|---------|-----------|---------|-----------|-------------|
| `elevator_parts_to_elevator` | `elevator_parts` | `elevator` | `composition` | 电梯配件（控制系统、曳引机、门机等）组装构成电梯整机 |

---

## 各公司分析与构建详情

### 1. 兰生股份 (sh_600826) — 外贸/工业
**主营业务**: 外贸、工业；主要产品：机电产品、纺织原料及制品、鞋类、塑料及其制品、玩具

**产业节点分析**:
- **服务**: 外贸服务 (`foreign_trade_service`)
- **产出**: 机电产品 (`electromechanical_product`)、纺织品 (`textile_product`)

**暴露关系**:
- provide_service foreign_trade_service
- produce electromechanical_product, textile_product

**策略**: 兰生股份（东浩兰生会展集团）的核心业务为外贸服务，同时经营机电和纺织产品的生产制造。

---

### 2. 百联股份 (sh_600827) — 超市连锁/百货/建材
**主营业务**: 连锁超市业务、建材业务、百货业务、房屋出租

**产业节点分析**:
- **运营**: 超市连锁 (`supermarket_chain`)、百货零售 (`department_store`)
- **运营**: 建材 (`building_material`)、房屋租赁 (`property_rental`)

**缺失节点补充**:
- 缺少 **超市连锁** (`supermarket_chain`) 节点，新建。

**暴露关系**:
- operate supermarket_chain, department_store
- operate building_material, property_rental

**策略**: 百联股份为上海国资旗下的大型商业零售集团，业务覆盖超市连锁、百货、建材和房屋租赁四大板块。

---

### 3. 茂业商业 (sh_600828) — 百货零售
**主营业务**: 商品零售

**产业节点分析**:
- **运营**: 百货零售 (`department_store`)

**暴露关系**:
- operate department_store

---

### 4. 人民同泰 (sh_600829) — 医药批发/零售
**主营业务**: 医药批发、医药零售等医药商业业务

**产业节点分析**:
- **服务**: 医药批发 (`pharmaceutical_wholesale`)、医药零售 (`pharmaceutical_retail`)

**缺失节点补充**:
- 缺少 **医药批发** (`pharmaceutical_wholesale`) 节点，新建。

**暴露关系**:
- provide_service pharmaceutical_wholesale, pharmaceutical_retail

**策略**: 人民同泰为哈药集团旗下的医药商业平台，覆盖医药批发和零售两大业务。新建 `pharmaceutical_wholesale` 节点以完善医药流通产业链图谱。

---

### 5. XD香溢融 (sh_600830) — 商品销售/餐饮/保险/典当
**主营业务**: 商品销售、餐饮、保险服务、典当

**产业节点分析**:
- **运营**: 商品销售/百货 (`department_store`)
- **服务**: 典当服务 (`pawnbroking_service`)

**缺失节点补充**:
- 缺少 **典当服务** (`pawnbroking_service`) 节点，新建。

**暴露关系**:
- operate department_store (weight=0.6)
- provide_service pawnbroking_service (weight=1.0)

**策略**: 香溢融通的典当业务是其区别于一般商业企业的特色金融服务，赋予最高权重。商品销售业务权重降低为0.6。

---

### 6. 广电网络 (sh_600831) — 有线电视/宽带/智慧业务
**主营业务**: 从传统有线电视传输业务发展为以视频、数据、智慧三大业务为主业

**产业节点分析**:
- **服务**: 有线电视网络服务 (`cable_tv_network_service`)、宽带网络服务 (`broadband_network_service`)

**暴露关系**:
- provide_service cable_tv_network_service, broadband_network_service

**策略**: 广电网络为陕西省广电网络运营商，正从传统有线电视向"视频+数据+智慧"三主业转型。

---

### 7. 第一医药 (sh_600833) — 医药零售/批发
**主营业务**: 医药零售及批发

**产业节点分析**:
- **服务**: 医药零售 (`pharmaceutical_retail`)、医药批发 (`pharmaceutical_wholesale`)

**暴露关系**:
- provide_service pharmaceutical_retail (weight=1.0)
- provide_service pharmaceutical_wholesale (weight=0.9)

**策略**: 第一医药为上海地区老牌医药零售企业，医药零售为主业，医药批发为补充业务。

---

### 8. 申通地铁 (sh_600834) — 地铁运营
**主营业务**: 地铁运营

**产业节点分析**:
- **运营**: 地铁运营 (`metro_operation`)

**缺失节点补充**:
- 缺少 **地铁运营** (`metro_operation`) 节点，新建。

**暴露关系**:
- operate metro_operation

**策略**: 申通地铁为上海地铁的运营主体之一，是中国A股市场唯一的地铁运营上市公司。

---

### 9. 上海机电 (sh_600835) — 电梯/自动扶梯
**主营业务**: 电梯及自动扶梯产品

**产业节点分析**:
- **产出**: 电梯 (`elevator`)、自动扶梯 (`escalator`)

**缺失节点补充**:
- 缺少 **电梯** (`elevator`) 节点，新建。
- `escalator` 节点在 batch_104 中已创建，本批次复用。
- 新建边：`elevator_parts` → `elevator`（composition）

**暴露关系**:
- produce elevator, escalator

**策略**: 上海机电为上海电气集团旗下电梯制造企业，产品覆盖电梯和自动扶梯两大品类。`escalator` 节点在 batch_104（隧道股份关联场景）中已预先创建，本批次复用。

---

### 10. 上海九百 (sh_600838) — 百货/洗涤化工
**主营业务**: 百货零售批发、洗涤化工产品

**产业节点分析**:
- **运营**: 百货零售 (`department_store`)
- **产出**: 日用化工产品 (`daily_chemical_product`)

**缺失节点补充**:
- 缺少 **日用化工产品** (`daily_chemical_product`) 节点，新建。

**暴露关系**:
- operate department_store
- produce daily_chemical_product

**策略**: 上海九百为上海地区老牌商业企业，同时经营洗涤化工产品的生产制造。

---

## 启发与发现

1. **医药流通产业链的完善**: 本批次新建了 `pharmaceutical_wholesale`（医药批发）节点，与已有的 `pharmaceutical_retail`（医药零售）节点共同构成了完整的医药流通服务谱系。人民同泰和第一医药均涉及批发和零售两个环节，但业务侧重点不同（人民同泰偏重批发，第一医药偏重零售），权重差异化有助于后续分析。

2. **零售业态的细分**: 本批次涉及多种零售业态：
   - 百货零售 (`department_store`)：茂业商业、益民集团、上海九百
   - 超市连锁 (`supermarket_chain`)：百联股份
   - 医药零售 (`pharmaceutical_retail`)：人民同泰、第一医药
   - 汽车贸易 (`automotive_trade`)：上海物贸（batch_104）
   
   这体现了零售业态在产业图中的多样化映射需求。

3. **特种金融服务的节点化**: 香溢融通的典当业务促使新建 `pawnbroking_service` 节点。典当作为一种特殊的短期融资服务，在产业金融图谱中具有一定的 niche 价值。

4. **城市交通基础设施**: 申通地铁的地铁运营业务促使新建 `metro_operation` 节点。城市轨道交通是城市公共交通体系的核心组成部分，与已有的公路运营等节点共同构成城市交通服务谱系。

5. **电梯产业链的节点衔接**: 上海机电同时生产电梯和自动扶梯，`escalator` 节点在 batch_104 中因隧道股份（地铁站应用场景）而预先创建，本批次复用。同时新建 `elevator` 节点并建立与 `elevator_parts` 的 composition 关系，完善了电梯产业链图谱。
