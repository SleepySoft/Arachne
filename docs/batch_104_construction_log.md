# Batch 104 产业图构建日志

## 批次信息
- **批次号**: 104
- **股票代码范围**: 600815.SH - 600825.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_104_nodes`)：补充5个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_104_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：5个
- 新建产业边：1条
- 新建公司：10家
- 新建暴露关系：21条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `sanitation_equipment` | 环卫装备 | device | 用于城市环境卫生作业的专业机械设备，包括清扫车、洒水车、垃圾收运车、除雪设备等，应用于城市道路清洁、垃圾收集转运等市政环卫领域。 |
| `automotive_trade` | 汽车贸易 | service | 从事汽车整车及配件的批发、零售、进出口贸易的流通服务，涵盖新车销售、二手车交易、汽车零部件分销等业务。 |
| `wind_power_generation` | 风力发电 | service | 利用风力发电机组将风能转化为电能的清洁能源发电服务，包括陆上风电和海上风电两种主要形式。 |
| `book_publishing` | 图书出版 | service | 将作者的作品经过编辑、排版、印刷、装订等工序制作成图书出版物并向市场发行的文化产业服务，涵盖教育出版、大众出版、专业出版等领域。 |
| `tunnel_engineering` | 隧道工程 | service | 在地下或山体中开挖、支护、衬砌并建成可供交通、管线、水利等用途的地下通道工程服务，涵盖钻爆法、盾构法、沉管法等多种施工技术。 |

## 新增边详情

| edge_id | from_node | to_node | edge_type | description |
|---------|-----------|---------|-----------|-------------|
| `tunnel_engineering_to_infrastructure_construction` | `tunnel_engineering` | `infrastructure_construction` | `service_flow` | 隧道工程是基础设施建设的重要组成部分，为交通、市政等基础设施提供地下通道 |

---

## 各公司分析与构建详情

### 1. 厦工股份 (sh_600815) — 工程机械
**主营业务**: 装载机、挖掘机和小型工程机械等工程机械产品及其配件的制造、加工和销售

**产业节点分析**:
- **产出**: 装载机 (`wheel_loader`)、挖掘机 (`excavator`)、工程机械 (`construction_machinery`)、工程机械配件 (`construction_machinery_parts`)
- **产出**: 矿山机械 (`mining_machinery`)、液压动力元件 (`hydraulic_power_unit`)

**暴露关系**:
- produce wheel_loader, excavator, construction_machinery, construction_machinery_parts
- produce mining_machinery, hydraulic_power_unit

**策略**: 厦工股份为老牌工程机械制造商，核心产品装载机和挖掘机系统中已有节点，直接复用。

---

### 2. 建元信托 (sh_600816) — 金融信托
**主营业务**: 金融信托业务

**产业节点分析**:
- **服务**: 信托服务 (`trust_service`)、金融服务 (`financial_service`)

**暴露关系**:
- provide_service trust_service, financial_service

**策略**: 建元信托为专业信托公司，直接映射到已有金融服务节点。

---

### 3. 宇通重工 (sh_600817) — 环卫/矿机/工程机械
**主营业务**: 经Web验证，宇通重工（原ST宏盛）主营业务为环卫装备、新能源环卫车、矿用装备及工程机械

**⚠️ 数据勘误**:
- tushare数据库中宇通重工的 `main_business` 标注为"集成电路产品,家电产品"，存在明显错误
- 经新浪财经及公司公告核实，宇通重工实际主营业务为：环卫装备、新能源环卫车、矿用装备、工程机械

**产业节点分析**:
- **产出**: 环卫装备 (`sanitation_equipment`)、新能源环卫车 (`new_energy_sanitation_vehicle`)
- **产出**: 矿山机械 (`mining_machinery`)、工程机械 (`construction_machinery`)
- **产出**: 环保设备 (`environmental_protection_equipment`)

**缺失节点补充**:
- 缺少 **环卫装备** (`sanitation_equipment`) 节点，新建。

**暴露关系**:
- produce sanitation_equipment, mining_machinery, construction_machinery, environmental_protection_equipment
- produce new_energy_sanitation_vehicle

**策略**: 宇通重工是从原ST宏盛重组而来的公司，tushare数据库中主营业务信息滞后。通过Web核实后，准确映射到环卫装备、矿机和工程机械三大板块。

---

### 4. ST中路 (sh_600818) — 自行车/康体设备
**主营业务**: 自行车、康体设备

**产业节点分析**:
- **产出**: 自行车 (`bicycle`)
- **产出/运营**: 康体设备 (`fitness_equipment`)

**暴露关系**:
- produce bicycle
- produce fitness_equipment

**策略**: ST中路（中路股份）主业为自行车制造，同时经营康体设备业务。

---

### 5. 耀皮玻璃 (sh_600819) — 玻璃
**主营业务**: 浮法玻璃、加工玻璃

**产业节点分析**:
- **产出**: 浮法玻璃 (`float_glass`)、加工玻璃 (`processed_glass`)、汽车玻璃 (`automotive_glass`)、玻璃 (`glass`)

**暴露关系**:
- produce float_glass, processed_glass, automotive_glass, glass

**策略**: 耀皮玻璃为综合玻璃制造商，产品覆盖建筑玻璃和汽车玻璃两大领域。

---

### 6. 隧道股份 (sh_600820) — 城市基础设施建设
**主营业务**: 投资、设计、施工、运营一体化的城市基础设施建设运营

**产业节点分析**:
- **运营/服务**: 基础设施建设 (`infrastructure_construction`)、隧道工程 (`tunnel_engineering`)、市政工程 (`municipal_engineering`)

**缺失节点补充**:
- 缺少 **隧道工程** (`tunnel_engineering`) 节点，新建。
- 新建边：`tunnel_engineering` → `infrastructure_construction`（service_flow）

**暴露关系**:
- operate infrastructure_construction
- provide_service tunnel_engineering
- provide_service municipal_engineering

**策略**: 隧道股份为上海国资旗下的基建龙头企业，以隧道工程为核心竞争力。新建 `tunnel_engineering` 节点以精准映射其专业施工能力。

---

### 7. 金开新能 (sh_600821) — 新能源发电
**主营业务**: 经Web验证，金开新能（原津劝业）已从零售业转型为新能源发电企业，主营风力发电和光伏发电

**⚠️ 数据勘误**:
- tushare数据库中金开新能的 `main_business` 标注为"商业零售"，存在严重滞后
- 经公司2024年年度报告及新浪财经核实，金开新能于2020年完成重大资产重组，主营业务已全面转型为风力发电和光伏发电

**产业节点分析**:
- **运营**: 风力发电 (`wind_power_generation`)、光伏发电 (`photovoltaic_module`)、太阳能发电 (`solar_power_generation`)

**缺失节点补充**:
- 缺少 **风力发电** (`wind_power_generation`) 节点，新建。

**暴露关系**:
- operate wind_power_generation
- operate photovoltaic_module
- operate solar_power_generation

**策略**: 金开新能是典型的"借壳转型"案例，从传统零售业彻底转型为清洁能源运营商。Web核实确保产业节点映射的准确性。

---

### 8. 上海物贸 (sh_600822) — 汽车贸易/有色金属
**主营业务**: 汽车贸易、化工等生产资料的批发与零售、有色金属平台交易

**产业节点分析**:
- **服务**: 汽车贸易 (`automotive_trade`)、有色金属贸易 (`nonferrous_metal_trade`)

**缺失节点补充**:
- 缺少 **汽车贸易** (`automotive_trade`) 节点，新建。

**暴露关系**:
- provide_service automotive_trade
- provide_service nonferrous_metal_trade

**策略**: 上海物贸为物资贸易流通企业，核心业务为汽车贸易和有色金属交易。新建 `automotive_trade` 节点以完善汽车产业链的流通环节。

---

### 9. 益民集团 (sh_600824) — 百货零售
**主营业务**: 百货零售业

**产业节点分析**:
- **运营**: 百货零售 (`department_store`)

**暴露关系**:
- operate department_store

---

### 10. 新华传媒 (sh_600825) — 出版/图书
**主营业务**: 图书、音像制品、文教用品、报刊广告

**产业节点分析**:
- **服务**: 图书出版 (`book_publishing`)、出版传媒 (`publishing_media`)
- **产出**: 文具 (`stationery`)

**缺失节点补充**:
- 缺少 **图书出版** (`book_publishing`) 节点，新建。

**暴露关系**:
- provide_service book_publishing, publishing_media
- produce stationery

**策略**: 新华传媒为上海新华发行集团旗下出版传媒企业，是上海地区重要的图书出版和发行机构。

---

## 启发与发现

1. **数据库信息的时效性问题**: 本批次出现两例tushare主营业务信息严重滞后的情况：
   - **宇通重工** (600817)：数据库标注为"集成电路/家电"，实际为"环卫装备/矿机/工程机械"
   - **金开新能** (600821)：数据库标注为"商业零售"，实际已转型为"风力发电/光伏发电"
   
   这凸显了在产业图构建过程中，对存量数据库信息进行Web交叉验证的必要性。尤其是发生重大资产重组、借壳上市、主营业务转型的公司，数据库信息往往存在明显滞后。

2. **新能源发电的节点细分**: 金开新能的风力发电业务促使新建 `wind_power_generation` 节点。此前系统中已有 `solar_power_generation` 和 `photovoltaic_module` 节点，风力发电节点的加入使得清洁能源发电板块更加完整。

3. **贸易流通环节的节点映射**: 上海物贸的汽车贸易业务促使新建 `automotive_trade` 节点。在产业图中，贸易流通服务是连接生产制造和终端消费的重要环节，不应被忽视。

4. **出版传媒产业的数字化**: 新华传媒的主营业务涵盖图书出版、音像制品、文教用品和报刊广告，体现了传统出版传媒企业在数字化转型中的业务布局。`book_publishing` 节点的加入丰富了文化产业的服务型节点谱系。
