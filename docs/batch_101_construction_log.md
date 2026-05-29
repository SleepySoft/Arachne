# Batch 101 产业图构建日志

## 批次信息
- **批次号**: 101
- **股票代码范围**: 600777.SH - 600789.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_101_nodes`)：补充缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_101_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：1个 (`steel_strand` 钢绞线)
- 新建产业边：1条 (`steel_wire_rod` → `steel_strand`)
- 新建公司：10家
- 新建暴露关系：34条

---

## 各公司分析与构建详情

### 1. *ST新潮 (sh_600777) — 石油开采
**主营业务**: 原油及天然气的勘探、开采和销售

**产业节点分析**:
- **产出**: 原油 (`crude_oil`)、天然气 (`natural_gas`)
- **运营**: 石油勘探开采 (`petroleum_exploration`)

**暴露关系**:
- `sh_600777_produce_crude_oil` → produce crude_oil
- `sh_600777_produce_natural_gas` → produce natural_gas
- `sh_600777_operate_petroleum_exploration` → operate petroleum_exploration

**策略**: 系统中已有原油、天然气和石油勘探开采节点，直接复用，建立produce和operate暴露。

---

### 2. 友好集团 (sh_600778) — 百货/综合商业
**主营业务**: 商业、公用事业(供暖)、酒店服务业、外贸出口、工业、房地产、广告业、旅游业

**产业节点分析**:
- **运营**: 百货零售 (`department_store`)
- **服务**: 供热服务 (`heating_supply`)、酒店服务 (`hotel`)、旅游服务 (`tourism_service`)

**暴露关系**:
- `sh_600778_operate_department_store` → operate department_store (weight=1.0)
- `sh_600778_provide_heating_supply` → provide_service heating_supply (weight=0.7)
- `sh_600778_operate_hotel` → operate hotel (weight=0.7)
- `sh_600778_provide_tourism_service` → provide_service tourism_service (weight=0.5)

**策略**: 友好集团为多元化商业集团，核心业务是百货零售，其余业务为辅助。对不同业务赋予不同权重。

---

### 3. 水井坊 (sh_600779) — 白酒
**主营业务**: 高档酒、中低档酒、药业、印刷包装产品

**产业节点分析**:
- **产出**: 白酒 (`baijiu` / `liquor`)

**暴露关系**:
- `sh_600779_produce_baijiu` → produce baijiu
- `sh_600779_produce_liquor` → produce liquor

**策略**: 水井坊为白酒生产企业，核心产出为白酒。系统中已有 `baijiu` 和 `liquor` 节点，直接复用。

---

### 4. 通宝能源 (sh_600780) — 火力发电
**主营业务**: 火力发电、配电业务及燃气业务

**产业节点分析**:
- **运营**: 火力发电服务 (`thermal_power_generation`)
- **产出**: 电力 (`electricity_power`)
- **输入**: 煤炭 (`coal`) — 火力发电的主要燃料

**暴露关系**:
- `sh_600780_operate_thermal_power_generation` → operate thermal_power_generation
- `sh_600780_produce_electricity_power` → produce electricity_power
- `sh_600780_procure_coal` → procure coal

**策略**: 火力发电企业，运营发电设施并产出电力，需要采购煤炭作为燃料。建立了完整的输入-运营-产出链。

---

### 5. 新钢股份 (sh_600782) — 普钢
**主营业务**: 中厚板、热轧卷板、冷轧卷板、线棒材、钢绞线等钢材产品

**产业节点分析**:
- **产出**: 中厚板 (`medium_thick_plate`)、热轧卷板 (`hot_rolled_coil`)、冷轧钢板 (`steel_sheet`)、棒材 (`steel_bar`)、钢绞线 (`steel_strand`)

**缺失节点补充**:
- 查询发现系统中缺少 **钢绞线** (`steel_strand`) 节点，遂新建。
- 钢绞线定义：由多根高强度冷拉光圆钢丝或刻痕钢丝按一定规则绞合而成的钢铁制品，广泛应用于预应力混凝土结构、桥梁拉索、岩土锚固、大型建筑等领域。
- 新建边：`steel_wire_rod` (线材) → `steel_strand` (钢绞线)，material_flow

**暴露关系**:
- `sh_600782_produce_medium_thick_plate` → produce medium_thick_plate
- `sh_600782_produce_hot_rolled_coil` → produce hot_rolled_coil
- `sh_600782_produce_steel_sheet` → produce steel_sheet
- `sh_600782_produce_steel_bar` → produce steel_bar
- `sh_600782_produce_steel_strand` → produce steel_strand

**策略**: 新钢股份为大型钢铁联合企业，产品线丰富。系统中已有大部分钢材节点，仅需补充钢绞线。

---

### 6. 鲁信创投 (sh_600783) — 创业投资/磨料磨具
**主营业务**: 创业投资业务；兼营磨料磨具、涂附磨具等

**产业节点分析**:
- **服务**: 股权投资服务 (`equity_investment_service`) — 创业投资本质属于股权投资范畴，复用已有节点
- **产出**: 磨料 (`abrasive_material`)、涂附磨具 (`coated_abrasive`)

**暴露关系**:
- `sh_600783_provide_equity_investment_service` → provide_service equity_investment_service (weight=1.0)
- `sh_600783_produce_abrasive_material` → produce abrasive_material (weight=0.6)
- `sh_600783_produce_coated_abrasive` → produce coated_abrasive (weight=0.6)

**策略**: 鲁信创投主业为创业投资，副业为磨料磨具制造。创业投资与系统中已有"股权投资服务" (`equity_investment_service`) 高度重合，直接复用。副业权重降低为0.6。

---

### 7. 鲁银投资 (sh_600784) — 综合类（钢铁+医药+纺织+羊绒+盐）
**主营业务**: 钢铁、医药、纺织；兼营羊绒制品、盐及盐化工产品

**产业节点分析**:
- **产出**: 螺纹钢 (`steel_rebar`)、医药原料药 (`pharmaceutical_raw_material`)、纺织品 (`textile_product`)、羊绒制品 (`cashmere_product`)、盐产品 (`salt_product`)

**暴露关系**:
- `sh_600784_produce_steel_rebar` → produce steel_rebar (weight=0.8)
- `sh_600784_produce_pharmaceutical_raw_material` → produce pharmaceutical_raw_material (weight=0.7)
- `sh_600784_produce_textile_product` → produce textile_product (weight=0.7)
- `sh_600784_produce_cashmere_product` → produce cashmere_product (weight=0.6)
- `sh_600784_produce_salt_product` → produce salt_product (weight=0.6)

**策略**: 鲁银投资为多元化投资集团，涉及钢铁、医药、纺织、羊绒和盐化工。主业钢铁权重最高，其余业务依次递减。

---

### 8. 新华百货 (sh_600785) — 百货/乳制品
**主营业务**: 商业零售业务，乳制品生产销售

**产业节点分析**:
- **运营**: 百货零售 (`department_store`)
- **产出**: 乳制品 (`dairy_product`)

**暴露关系**:
- `sh_600785_operate_department_store` → operate department_store (weight=1.0)
- `sh_600785_produce_dairy_product` → produce dairy_product (weight=0.7)

**策略**: 新华百货主业为百货零售，兼有乳制品生产。百货零售为核心业务，乳制品生产为次要业务。

---

### 9. 中储股份 (sh_600787) — 仓储物流
**主营业务**: 期现货交割物流、大宗商品供应链、物流+互联网、消费品物流、工程物流、金融物流

**产业节点分析**:
- **运营**: 仓储服务 (`warehouse_service`)、物流服务 (`logistics_service`)
- **服务**: 供应链服务 (`supply_chain_service`)

**暴露关系**:
- `sh_600787_operate_warehouse_service` → operate warehouse_service
- `sh_600787_operate_logistics_service` → operate logistics_service
- `sh_600787_provide_supply_chain_service` → provide_service supply_chain_service

**策略**: 中储股份为核心仓储物流企业，三大业务板块（仓储、物流、供应链）均赋予高权重。

---

### 10. 鲁抗医药 (sh_600789) — 化学制药
**主营业务**: 普药及半合抗原料药、普药及半合抗制剂、兽用抗生素

**产业节点分析**:
- **产出**: 化学原料药 (`active_pharmaceutical_ingredient`)、抗生素 (`antibiotic`)、抗生素制剂 (`antibiotic_preparation`)、兽药 (`veterinary_medicine`)

**暴露关系**:
- `sh_600789_produce_active_pharmaceutical_ingredient` → produce active_pharmaceutical_ingredient
- `sh_600789_produce_antibiotic` → produce antibiotic
- `sh_600789_produce_antibiotic_preparation` → produce antibiotic_preparation
- `sh_600789_produce_veterinary_medicine` → produce veterinary_medicine

**策略**: 鲁抗医药为老牌化学制药企业，核心产品覆盖人用和兽用抗生素全产业链。四个产业节点系统中均已存在，直接复用。

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `steel_strand` | 钢绞线 | material | 由多根高强度冷拉光圆钢丝或刻痕钢丝按一定规则绞合而成的钢铁制品，广泛应用于预应力混凝土结构、桥梁拉索、岩土锚固、大型建筑等领域。 |

## 新增边详情

| edge_id | from_node | to_node | edge_type | description |
|---------|-----------|---------|-----------|-------------|
| `steel_wire_rod_to_steel_strand` | `steel_wire_rod` | `steel_strand` | `material_flow` | 线材（盘条）经过拉拔、绞合等工艺加工成钢绞线 |

---

## 启发与发现

1. **钢铁产业链完整性**：新钢股份涉及的产品线（中厚板、热轧卷板、冷轧卷板、棒材、钢绞线）覆盖了建筑、机械、汽车、能源等多个下游行业，体现了普钢企业的产品多样性。

2. **多元化集团的处理策略**：友好集团、鲁银投资这类业务高度多元化的公司，需要对不同业务赋予差异化权重，以反映各业务板块在公司收入结构中的实际占比。

3. **投资类企业的节点映射**：鲁信创投这类创业投资企业，其核心"产出"并非实体产品，而是资本配置和投资管理服务。在产业图中，应将其映射到`equity_investment_service`等服务型节点，而非试图将其归入实体产品类别。

4. **能源产业链的输入-产出关系**：通宝能源的火力发电业务具有典型的输入（煤炭）- 运营（火力发电）- 产出（电力）链条，这种完整的链条有助于后续推导上下游公司关系。
