# Batch 102 产业图构建日志

## 批次信息
- **批次号**: 102
- **股票代码范围**: 600790.SH - 600800.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_102_nodes`)：补充5个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_102_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：5个
- 新建产业边：1条
- 新建公司：10家
- 新建暴露关系：27条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `coke_oven_gas` | 焦炉煤气 | material | 炼焦过程中煤在焦炉炭化室内经高温干馏产生的可燃气体，主要成分为氢气和甲烷，是焦炭生产的重要副产品，可用于燃料或化工原料。 |
| `cultural_paper` | 文化纸 | material | 用于书写、印刷、办公和文化传播用途的纸类产品，包括双胶纸、铜版纸、书写纸等，区别于包装纸和新闻纸。 |
| `food_packaging_paper` | 食品包装原纸 | material | 专门用于食品直接接触包装的纸类原材料，具有良好的阻隔性、安全性和印刷适性，经淋膜或涂布后可制成纸杯、纸碗、食品纸盒等。 |
| `smart_card` | 智能卡 | component | 内嵌集成电路芯片的塑料卡片，可实现数据存储、身份识别、电子支付等功能，包括金融IC卡、社保卡、交通卡、门禁卡等。 |
| `security_printing` | 证券印刷 | service | 采用特种纸张、防伪油墨、微缩文字、全息图案等防伪技术，印制钞票、有价证券、重要票据、证件等高安全等级印刷品的专门印刷服务。 |

## 新增边详情

| edge_id | from_node | to_node | edge_type | description |
|---------|-----------|---------|-----------|-------------|
| `coal_to_coke` | `coal` | `coke` | `material_flow` | 煤炭在高温干馏条件下转化为焦炭 |

---

## 各公司分析与构建详情

### 1. 轻纺城 (sh_600790) — 纺织品市场运营
**主营业务**: 纺织品销售及加工,市场租赁,酒类销售,建材销售

**产业节点分析**:
- **产出/销售**: 纺织品 (`textile_product`)
- **运营**: 商业地产运营 (`commercial_property_operation`) — 映射其"市场租赁"核心业务

**暴露关系**:
- produce textile_product (weight=1.0)
- operate commercial_property_operation (weight=1.0)

**策略**: 轻纺城的核心商业模式是"纺织品专业市场运营商"，既从事纺织品销售加工，也通过市场租赁为商户提供经营场所。使用 `commercial_property_operation` 来映射市场租赁业务，而非新建节点。

---

### 2. 京能置业 (sh_600791) — 房地产开发
**主营业务**: 房地产开发与经营

**暴露关系**:
- operate real_estate_development (weight=1.0)

---

### 3. 云煤能源 (sh_600792) — 焦炭加工
**主营业务**: 生产和销售焦炭,煤气,蒸汽,余热发电,煤焦化工副产品

**产业节点分析**:
- **产出**: 焦炭 (`coke`)、焦炉煤气 (`coke_oven_gas`)、工业蒸汽 (`industrial_steam`)
- **运营**: 余热发电 (`thermal_power_generation`)
- **输入**: 煤炭 (`coal`)

**缺失节点补充**: 系统中缺少 **焦炉煤气** (`coke_oven_gas`) 节点。焦炉煤气是炼焦过程的重要副产品，不同于城市燃气，应单独建节点。

**暴露关系**:
- produce coke (weight=1.0)
- produce coke_oven_gas (weight=0.8)
- produce industrial_steam (weight=0.8)
- operate thermal_power_generation (weight=0.7)
- procure coal (weight=1.0)

**策略**: 云煤能源是完整的煤化工企业，主业为焦炭生产，副产煤气和蒸汽，并利用余热发电。建立了完整的输入-产出链。

---

### 4. 宜宾纸业 (sh_600793) — 造纸
**主营业务**: 生产销售新闻纸,文化纸,食品包装原纸

**产业节点分析**:
- **产出**: 新闻纸 (`newsprint`)、文化纸 (`cultural_paper`)、食品包装原纸 (`food_packaging_paper`)

**缺失节点补充**:
- 系统中已有 `newsprint`（新闻纸）
- 缺少 **文化纸** (`cultural_paper`) 节点
- 缺少 **食品包装原纸** (`food_packaging_paper`) 节点

**暴露关系**:
- produce newsprint (weight=1.0)
- produce cultural_paper (weight=1.0)
- produce food_packaging_paper (weight=1.0)

**策略**: 宜宾纸业的产品线覆盖了印刷书写用纸和食品包装用纸两大品类，三个节点分别对应其核心产品。

---

### 5. 保税科技 (sh_600794) — 仓储物流
**主营业务**: 液体化工品,固体干散货仓储业务及代理等物流服务业务

**暴露关系**:
- operate warehouse_service (weight=1.0)
- operate bonded_warehousing_service (weight=1.0)
- operate logistics_service (weight=0.8)

---

### 6. 国电电力 (sh_600795) — 火力发电
**主营业务**: 电力

**暴露关系**:
- operate thermal_power_generation (weight=1.0)
- produce electricity_power (weight=1.0)
- procure coal (weight=1.0)

**策略**: 国电电力为大型发电企业，火力发电为主，需要采购煤炭作为燃料。

---

### 7. 钱江生化 (sh_600796) — 农药/兽药
**主营业务**: 杀菌剂类农药,生长调节剂类农药,杀虫剂类农药,兽药

**暴露关系**:
- produce pesticide (weight=1.0)
- produce pesticide_formulation (weight=1.0)
- produce veterinary_medicine (weight=0.8)

---

### 8. 浙大网新 (sh_600797) — 软件服务/网络设备
**主营业务**: 网络设备与终端,软件外包与服务

**暴露关系**:
- produce network_equipment (weight=1.0)
- provide_service software_development_service (weight=1.0)

---

### 9. 宁波海运 (sh_600798) — 水运
**主营业务**: 国内沿海,长江中下游,国际船舶普通货物运输

**暴露关系**:
- operate shipping_service (weight=1.0)

---

### 10. 渤海化学 (sh_600800) — 印刷/房地产
**主营业务**: 卡类产品,包装印刷产品,有价证券产品,电脑表格产品的印制及房地产开发业务

**产业节点分析**:
- **产出**: 智能卡 (`smart_card`)
- **服务**: 证券印刷 (`security_printing`)、包装印刷 (`printing_service`)
- **运营**: 房地产开发 (`real_estate_development`)

**缺失节点补充**:
- 缺少 **智能卡** (`smart_card`) 节点 — 内嵌芯片的塑料卡片
- 缺少 **证券印刷** (`security_printing`) 节点 — 高安全等级的防伪印刷服务

**暴露关系**:
- produce smart_card (weight=1.0)
- provide_service security_printing (weight=1.0)
- provide_service printing_service (weight=0.8)
- operate real_estate_development (weight=0.5)

**策略**: 渤海化学虽然被分类为"化工原料"行业，但实际主营业务是印刷（智能卡、证券、包装）和房地产。这一案例说明Tushare的行业分类仅反映历史渊源，实际业务需要结合 `main_business` 和 `business_scope` 仔细分析，避免误判。

---

## 启发与发现

1. **行业分类与实际的偏差**：渤海化学被Tushare分类为"化工原料"，但实际主营业务是印刷和房地产。这提醒我们在构建产业图时，**必须以公司的实际主营业务为准，而非仅依赖行业分类标签**。

2. **副产品节点的处理**：云煤能源的焦炉煤气是焦炭生产的副产品。在产业图中，副产品应作为独立节点存在（`coke_oven_gas`），因为它可以作为其他产业的输入（如燃料、化工原料）。

3. **纸类产品细分**：宜宾纸业的产品线展示了造纸行业的细分：新闻纸（信息传播）、文化纸（书写印刷）、食品包装原纸（食品包装）。三者面向完全不同的下游市场，应分别建节点。

4. **商业地产运营作为映射节点**：轻纺城的"市场租赁"业务本质上属于商业地产运营范畴，复用 `commercial_property_operation` 节点即可准确映射，无需新建"市场租赁"节点，保持了产业图的简洁性。
