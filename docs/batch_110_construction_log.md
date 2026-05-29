# Batch 110 产业图构建日志

## 批次信息
- **批次号**: 110
- **股票代码范围**: 600885.SH - 600897.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_110_nodes`)：补充13个缺失的产业节点，新建3条产业边
2. **BusinessRegistrationBatch** (`batch_110_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：13个
- 新建产业边：3条
- 新建公司：10家
- 新建暴露关系：29条（1条因后端错误未成功）

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `relay` | 继电器 | component | 当输入量达到一定值时，输出量将发生跳跃式变化的自动控制器件，广泛应用于电力保护、工业控制、通信设备、汽车电子等领域。 |
| `low_voltage_electrical` | 低压电器 | component | 工作在交流1200V或直流1500V及以下电路中起通断、保护、控制或调节作用的电器设备和器件。 |
| `contactor` | 接触器 | component | 利用电磁原理自动控制的开关电器，用于频繁接通和分断交直流主电路及大容量控制电路。 |
| `automation_equipment` | 自动化设备 | device | 用于实现生产过程或作业流程自动化的机电一体化设备系统，包括PLC、变频器、伺服系统、工业机器人等。 |
| `ice_cream` | 冰淇淋 | material | 以牛奶、奶粉、奶油等为主要原料，经混合、灭菌、均质、凝冻、硬化等工艺制成的体积膨胀的冷冻饮品。 |
| `milk_powder` | 奶粉 | material | 以生鲜牛（羊）乳为主要原料，经浓缩、干燥等工艺去除大部分水分后制成的粉状乳制品。 |
| `electronic_aluminum_foil` | 电子铝箔 | material | 用于制造铝电解电容器电极的高纯度铝箔，是铝电解电容器的核心原材料。 |
| `high_purity_aluminum` | 高纯铝 | material | 纯度达到99.9%以上的高纯度金属铝，主要用于制造电子铝箔、半导体靶材、航空航天合金等高端领域。 |
| `aluminum_rod` | 铝杆 | material | 通过连铸连轧工艺生产的圆形截面铝及铝合金长条材料，是制造电线电缆、架空导线的原材料。 |
| `formed_foil` | 化成箔 | material | 以电子铝箔为基材，经电化学阳极氧化处理在表面形成致密氧化铝电介质的铝箔材料，是铝电解电容器制造中的关键中间材料。 |
| `etched_foil` | 腐蚀箔 | material | 以电子铝箔为基材，通过电化学腐蚀工艺在表面形成微米级孔洞结构以大幅增加比表面积的铝箔材料。 |
| `aero_engine` | 航空发动机 | system | 为航空器提供推进动力的热力机械装置，是飞机的'心脏'，集气动热力学、结构力学、材料科学、控制技术于一体。 |
| `air_ground_service` | 机场地面服务 | service | 为航空器在地面停靠期间及旅客在机场候机楼内提供的各类保障服务，包括飞机引导、客舱清洁、行李装卸、配餐供应等。 |

## 新增边详情

| edge_id | from_node | to_node | edge_type | description |
|---------|-----------|---------|-----------|-------------|
| `aluminum_ingot_to_electronic_aluminum_foil` | `aluminum_ingot` | `electronic_aluminum_foil` | `material_flow` | 高纯度铝锭经过轧制加工成电子铝箔 |
| `electronic_aluminum_foil_to_etched_foil` | `electronic_aluminum_foil` | `etched_foil` | `material_flow` | 电子铝箔经电化学腐蚀工艺加工成腐蚀箔 |
| `etched_foil_to_formed_foil` | `etched_foil` | `formed_foil` | `material_flow` | 腐蚀箔经阳极氧化化成工艺加工成化成箔 |

---

## 各公司分析与构建详情

### 1. 宏发股份 (sh_600885) — 继电器/低压电器/接触器
**主营业务**: 研制、生产和销售继电器、低压电器、接触器、自动化设备及相关的电子元器件和组件

**暴露关系**:
- produce relay (weight=1.0)
- produce low_voltage_electrical (weight=1.0)
- produce contactor (weight=1.0)
- produce automation_equipment (weight=0.8)

**策略**: 宏发股份是全球最大的继电器制造商之一，`relay` 节点的加入填补了产业图在电子元器件控制器件领域的空白。

---

### 2. 国投电力 (sh_600886) — 水电/电力生产
**主营业务**: 电力的生产和供应

**暴露关系**:
- operate hydro_power_generation (weight=1.0)
- produce electricity_power (weight=1.0)

---

### 3. 伊利股份 (sh_600887) — 乳制品
**主营业务**: 液体乳系列、冷饮产品系列、奶粉及奶食品、混和饲料、方便食品

**暴露关系**:
- produce liquid_milk (weight=1.0)
- produce ice_cream (weight=1.0)
- produce milk_powder (weight=1.0)
- produce dairy_product (weight=1.0)
- produce feed (weight=0.6)

**策略**: 伊利股份是中国乳制品行业龙头企业，员工超过6.3万人。新建 `ice_cream` 和 `milk_powder` 节点以完善乳制品产业链图谱。

---

### 4. 新疆众和 (sh_600888) — 电子铝箔/高纯铝
**主营业务**: 主要产品：电子铝箔、精铝、普铝锭、铝杆、化成箔、腐蚀箔

**暴露关系**:
- produce electronic_aluminum_foil (weight=1.0)
- produce high_purity_aluminum (weight=1.0)
- produce aluminum_ingot (weight=0.8)
- produce aluminum_rod (weight=0.8)
- produce formed_foil (weight=0.9)
- produce etched_foil (weight=0.9)

**策略**: 新疆众和是全球最大的高纯铝和电子铝箔生产企业之一，产品覆盖了从 `aluminum_ingot` → `electronic_aluminum_foil` → `etched_foil` → `formed_foil` 的完整铝电解电容器材料产业链。本批次新建3条边以完整映射该产业链。

---

### 5. ST京化 (sh_600889) — 粘胶纤维/自来水
**主营业务**: 粘胶纤维和自来水的生产与经营

**暴露关系**:
- produce viscose_fiber (weight=1.0)
- produce tap_water (weight=1.0)

**策略**: 复用系统中已有的 `viscose_fiber` 节点。

---

### 6. ST大晟 (sh_600892) — 贸易业务
**主营业务**: 主要经营贸易业务

**暴露关系**:
- provide_service commodity_trade

---

### 7. 航发动力 (sh_600893) — 航空发动机
**主营业务**: 航空发动机批量制造及修理等

**暴露关系**:
- produce aero_engine (weight=1.0)

⚠️ **注意**: `sh_600893_provide_aero_engine_maintenance`（航空发动机修理服务）因后端 `model_dump` 错误未能成功提交。

**策略**: 航发动力是中国航空发动机集团的上市公司，是中国航空发动机研制生产的核心企业。`aero_engine` 节点的加入对航空军工产业链具有里程碑意义。

---

### 8. 广日股份 (sh_600894) — 电梯/零部件/物流
**主营业务**: 以电梯整机制造、电梯零部件生产及物流服务为主业

**暴露关系**:
- produce elevator (weight=1.0)
- produce elevator_parts (weight=0.9)
- provide_service logistics_service (weight=0.7)

---

### 9. 张江高科 (sh_600895) — 科技园区
**主营业务**: 园区内房地产租赁、园区内房地产销售

**暴露关系**:
- operate tech_park_operation_service (weight=1.0)
- operate property_rental (weight=1.0)

---

### 10. 厦门空港 (sh_600897) — 机场运营/地面服务
**主营业务**: 为国内外航空运输企业及旅客提供地面保障服务；候机楼商业场所出租和管理等

**暴露关系**:
- operate airport_operation_service (weight=1.0)
- provide_service air_ground_service (weight=1.0)
- provide_service cargo_handling (weight=0.7)
- operate warehouse_service (weight=0.6)

---

## 启发与发现

1. **铝电解电容器材料产业链的完整构建**：新疆众和的产品线覆盖了铝电解电容器材料的完整产业链：铝锭→电子铝箔→腐蚀箔→化成箔。本批次新建的3条边（`aluminum_ingot_to_electronic_aluminum_foil`、`electronic_aluminum_foil_to_etched_foil`、`etched_foil_to_formed_foil`）首次在产业图中构建了该细分产业链的完整链条。

2. **航空发动机——工业皇冠上的明珠**：航发动力的 `aero_engine` 节点是航空产业链中最核心的系统级节点。航空发动机被誉为"工业皇冠上的明珠"，其技术难度和战略价值远超一般工业产品。该节点的加入使产业图具备了分析航空军工产业链的能力。

3. **乳制品消费品的精细化**：伊利股份和妙可蓝多（batch_109）共同推动了乳制品节点的细化。`liquid_milk`、`ice_cream`、`milk_powder`、`cheese` 四个节点覆盖了乳制品消费的四大主力品类，使产业图在快消品领域的覆盖更加精准。

4. **电子元器件控制器件**：宏发股份的继电器、低压电器和接触器产品代表了电力控制和自动化领域的基础元器件。`relay`、`low_voltage_electrical`、`contactor` 三个节点的加入填补了产业图在低压电器控制领域的空白。
