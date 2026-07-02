# Batch 106 产业图构建日志

## 批次信息
- **批次号**: 106
- **股票代码范围**: 600839.SH - 600850.SH（含601607.SH）
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_106_nodes`)：补充6个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_106_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：6个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：27条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `compressor` | 压缩机 | device | 将低压气体提升为高压气体的流体机械，广泛应用于制冷空调、石油化工、天然气输送、气动工具等领域。 |
| `sewing_machine` | 缝纫机 | device | 用一根或多根缝纫线，在缝料上形成线迹，使一层或多层缝料交织或缝合起来的机器，包括家用缝纫机和工业缝纫机两大类。 |
| `coal_chemical_product` | 煤化工产品 | material | 以煤炭为原料，通过化学加工方法（气化、液化、焦化、干馏等）转化生产的化学品和能源产品。 |
| `service_outsourcing` | 服务外包 | service | 企业将非核心业务或特定服务流程委托给外部专业服务提供商完成的商业模式，包括ITO、BPO和KPO等。 |
| `lead_acid_battery` | 铅蓄电池 | device | 以二氧化铅为正极、海绵状铅为负极、稀硫酸为电解液的二次电池，广泛应用于汽车启动、电动自行车、通信基站备用电源等领域。 |
| `intelligent_building` | 智能建筑 | system | 利用计算机技术、通信技术、控制技术等对建筑设备进行自动化监控和管理，为用户提供高效、舒适、便利的人性化建筑环境。 |

---

## 各公司分析与构建详情

### 1. 四川长虹 (sh_600839) — 家用电器/IT/房地产
**主营业务**: 电视机、冰箱、空调、压缩机、视听产品、电池、手机等产品的生产销售，IT产品销售及房地产开发

**产业节点分析**:
- **产出**: 电视 (`tv_set`)、冰箱 (`refrigerator`)、空调 (`air_conditioner`)、压缩机 (`compressor`)、电池 (`battery`)、手机 (`mobile_phone`)
- **运营**: 房地产开发 (`real_estate_development`)

**暴露关系**: 7条，涵盖produce和operate，权重按核心业务到次要业务递减。

---

### 2. 动力新科 (sh_600841) — 柴油机
**主营业务**: 柴油机及其配件的生产及销售

**暴露关系**:
- produce diesel_engine

---

### 3. 上工申贝 (sh_600843) — 缝制设备
**主营业务**: 工业缝纫机、家用缝纫机及特种用途工业定制机器的研发、生产和销售

**暴露关系**:
- produce industrial_sewing_machine (weight=1.0)
- produce sewing_machine (weight=0.8)

**策略**: 上工申贝同时覆盖工业和家用缝纫机市场，系统中已有 `industrial_sewing_machine` 节点，本批次新建 `sewing_machine` 节点以覆盖家用市场。

---

### 4. 金煤科技 (sh_600844) — 煤化工
**主营业务**: 主要从事煤化工产品的生产

**暴露关系**:
- produce coal_chemical_product

---

### 5. 宝信软件 (sh_600845) — 软件开发/系统集成/智能交通
**主营业务**: 计算机、自动化、网络通讯系统及软硬件产品的研究、设计、开发、制造、集成及相应的外包、维修、咨询等服务

**暴露关系**:
- provide_service software_development_service
- provide_service service_outsourcing
- provide_service information_system_integration
- provide_service intelligent_transport_system

**策略**: 宝信软件是中国宝武钢铁集团旗下的IT子公司，是工业软件和信息化领域的龙头企业。复用系统中已有的 `software_development_service`、`information_system_integration` 和 `intelligent_transport_system` 节点。

---

### 6. 同济科技 (sh_600846) — 房地产/建筑施工
**主营业务**: 商品房、建筑施工

**暴露关系**:
- operate real_estate_development
- provide_service construction_engineering

---

### 7. 万里股份 (sh_600847) — 铅蓄电池
**主营业务**: 铅蓄电池的研发、生产、销售

**暴露关系**:
- produce lead_acid_battery

---

### 8. 上海临港 (sh_600848) — 科技产业园区
**主营业务**: 科技产业园区开发建设、运营服务

**暴露关系**:
- operate tech_park_operation_service
- operate property_rental

**策略**: 复用系统中已有的 `tech_park_operation_service` 节点。

---

### 9. 上海医药 (sh_601607) — 医药制造/流通
**主营业务**: 原料药和各种剂型的医药产品、保健品、医疗器械及相关产品的研发、制造和销售

**暴露关系**:
- produce pharmaceutical_manufacturing
- provide_service pharmaceutical_wholesale
- provide_service pharmaceutical_retail
- produce medical_device

**策略**: 上海医药是中国第二大全国性医药流通企业和领先的医药制造商，覆盖医药全产业链。员工近5万人，是国内医药行业的巨头企业。

---

### 10. 电科数字 (sh_600850) — IT基础设施/智能建筑
**主营业务**: 面向IT基础设施的系统集成和专业服务、软件和行业解决方案、IT产品增值销售、智能建筑与机房

**暴露关系**:
- provide_service information_system_integration
- provide_service software_development_service
- provide_service intelligent_building

---

## 启发与发现

1. **家电产业链的完整性**：四川长虹作为中国老牌家电企业，其产品覆盖了电视、冰箱、空调、压缩机、电池、手机等多个品类。压缩机节点的加入完善了家电核心零部件的产业图谱。

2. **工业软件的重要性**：宝信软件和电科数字代表了中国工业信息化和数字化转型的核心力量。它们的业务高度依赖 `software_development_service`、`system_integration` 和 `intelligent_transport_system` 等已有服务型节点，说明产业图在IT服务领域的覆盖已经较为完善。

3. **缝纫机市场的细分**：上工申贝同时生产工业和家用缝纫机，而系统中此前仅有 `industrial_sewing_machine` 节点。新建 `sewing_machine` 节点反映了产业图中对消费端和生产端设备区分的需要。
