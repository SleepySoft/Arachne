# Batch 109 产业图构建日志

## 批次信息
- **批次号**: 109
- **股票代码范围**: 600874.SH - 600884.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_109_nodes`)：补充6个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_109_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：6个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：22条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `sewage_treatment` | 污水处理 | service | 采用物理、化学和生物等方法对生活和工业废水进行净化处理，使其达到排放标准或回用要求的环保工程服务。 |
| `toll_road` | 收费公路 | infrastructure | 通过收取车辆通行费来回收建设投资和运营维护成本的收费性公路或桥梁。 |
| `aerospace_electronic_equipment` | 航天电子设备 | device | 专门用于航天器的电子设备系统，包括导航、测控通信、遥感、电源、姿态控制等系统。 |
| `cheese` | 奶酪 | material | 以牛奶、羊奶等鲜奶为原料，经凝乳酶或酸化使蛋白质凝固、排去乳清后发酵成熟的乳制品。 |
| `liquid_milk` | 液态奶 | material | 以生鲜牛（羊）乳为原料，经标准化、均质、杀菌等工艺加工制成的液体乳制品，是乳制品消费的主力品类。 |
| `lithium_ion_battery_material` | 锂离子电池材料 | material | 用于制造锂离子电池的关键功能性材料，包括正极材料、负极材料、电解液和隔膜。 |

---

## 各公司分析与构建详情

### 1. 创业环保 (sh_600874) — 污水处理/收费公路
**主营业务**: 污水处理及污水处理厂建设业务、道路及收费站业务

**暴露关系**:
- provide_service sewage_treatment (weight=1.0)
- operate toll_road (weight=0.8)

---

### 2. 东方电气 (sh_600875) — 发电设备
**主营业务**: 主要产品为火力发电设备、水力发电设备、风力发电设备、核能发电设备以及燃气发电设备等

**暴露关系**:
- produce power_generation_equipment (weight=1.0)
- produce thermal_power_generation (weight=0.9)
- produce wind_power_generation (weight=0.9)

**策略**: 东方电气是全球最大的发电设备制造和电站工程总承包企业之一，产品覆盖水火风光核气六大发电类型。映射到 `power_generation_equipment` 和主要发电类型的运营节点。

---

### 3. 凯盛新能 (sh_600876) — 浮法玻璃/光伏玻璃
**主营业务**: 浮法平板玻璃的制造和销售

**暴露关系**:
- produce float_glass (weight=1.0)
- produce pv_glass (weight=0.8)

**策略**: 复用系统中已有的 `pv_glass` 节点映射光伏玻璃业务。

---

### 4. 电科芯片 (sh_600877) — 集成电路
**主营业务**: ⚠️ tushare标注为"摩托车"，实际为集成电路设计、制造、销售

**⚠️ 数据勘误**:
- tushare数据库中电科芯片的 `main_business` 标注为"摩托车"，存在严重错误
- 经 `business_scope` 核实，实际主营业务为：电子元器件制造、集成电路设计、集成电路制造、集成电路销售、5G通信技术服务、物联网技术服务

**暴露关系**:
- produce integrated_circuit

**策略**: 电科芯片（原声光电科）是中国电科旗下的集成电路企业。复用系统中已有的 `integrated_circuit` 节点。

---

### 5. 航天电子 (sh_600879) — 航天电子设备
**主营业务**: 航天电子设备

**暴露关系**:
- produce aerospace_electronic_equipment

---

### 6. 博瑞传播 (sh_600880) — 印刷/广告/新闻纸
**主营业务**: 印刷业务、广告业务、新闻纸销售业务、发行投递业务

**暴露关系**:
- provide_service printing_service
- provide_service advertising_service
- produce newsprint

---

### 7. 亚泰集团 (sh_600881) — 水泥/房地产
**主营业务**: 水泥、商品房

**暴露关系**:
- produce cement
- operate real_estate_development

---

### 8. 妙可蓝多 (sh_600882) — 奶酪/液态奶
**主营业务**: 以奶酪、液态奶为核心的特色乳制品的研发、生产和销售

**暴露关系**:
- produce cheese (weight=1.0)
- produce liquid_milk (weight=1.0)
- produce dairy_product (weight=1.0)

---

### 9. 博闻科技 (sh_600883) — 水泥粉磨
**主营业务**: 水泥粉磨与销售

**暴露关系**:
- produce cement

---

### 10. 杉杉股份 (sh_600884) — 服装/锂电材料
**主营业务**: 西服、休闲服、锂离子电池材料、衬衫

**暴露关系**:
- produce suit (weight=0.6)
- produce casual_wear (weight=0.6)
- produce lithium_ion_battery_material (weight=1.0)
- produce shirt (weight=0.5)

**策略**: 杉杉股份已从传统的服装企业成功转型为锂离子电池材料龙头，其负极材料出货量全球领先。服装业务权重降低，锂电材料作为核心业务赋予最高权重。

---

## 启发与发现

1. **数据库勘误的再次确认**：电科芯片（600877）是本轮次的第二个严重数据错误案例，tushare的 `main_business` 标注为"摩托车"，而 `business_scope` 明确显示为集成电路业务。这再次证明在产业图构建中交叉验证数据库信息的必要性。

2. **乳制品产业链的细化**：妙可蓝多的奶酪和液态奶业务促使新建 `cheese` 和 `liquid_milk` 节点。此前系统中已有 `dairy_product` 节点，但奶酪和液态奶作为乳制品的两大主力品类，值得单独建节点以支持更精细的产业链分析。

3. **新能源材料产业链**：杉杉股份的 `lithium_ion_battery_material` 节点（负极材料）与此前已有的 `battery_cathode_material`（正极材料）节点共同构成了锂电池材料的核心骨架，对新能源汽车产业链分析具有重要支撑作用。

4. **航天产业链的延伸**：航天电子的 `aerospace_electronic_equipment` 节点与航发动力（batch_110）的 `aero_engine` 节点共同构建了中国航天军工产业链的关键环节。
