# Batch 103 产业图构建日志

## 批次信息
- **批次号**: 103
- **股票代码范围**: 600801.SH - 600814.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_103_nodes`)：补充6个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_103_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：6个
- 新建产业边：2条
- 新建公司：10家
- 新建暴露关系：28条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `clinker` | 水泥熟料 | material | 水泥生产过程中的半加工原料，由石灰石、黏土等原料经1450℃左右高温煅烧后的烧结产物，加水研磨后即成为水泥成品。 |
| `lng_production` | LNG生产 | service | 将天然气经净化处理后，通过低温液化工艺（-162℃）转化为液化天然气（LNG）的生产服务，便于天然气的储运和贸易。 |
| `energy_tech_service` | 能源技术服务 | service | 为能源行业提供的技术咨询、工程设计、项目管理、技术开发、技术转让等专业服务，涵盖清洁能源、节能环保等领域。 |
| `biotech_agri_drug` | 生物农药 | material | 利用生物活体（微生物、植物、动物）或其代谢产物制成的农药制剂，具有低毒、低残留、环境友好等特点，用于农业病虫害防治。 |
| `steel_long_product` | 长材 | material | 钢材按形状分类中的一类，指截面呈长条状的钢材产品，包括螺纹钢、圆钢、线材、型钢等，主要用于建筑结构、机械制造等领域。 |
| `nylon_industrial_yarn` | 尼龙工业丝 | material | 以聚酰胺（尼龙）为原料纺制的高强度工业用长丝，具有优异的耐磨性、抗疲劳性和力学性能，是帘子布、帆布、传送带等工业织物的核心原料。 |

## 新增边详情

| edge_id | from_node | to_node | edge_type | description |
|---------|-----------|---------|-----------|-------------|
| `clinker_to_cement` | `clinker` | `cement` | `material_flow` | 水泥熟料经研磨后与适量石膏混合制成水泥成品 |
| `nylon_to_nylon_industrial_yarn` | `nylon` | `nylon_industrial_yarn` | `material_flow` | 尼龙切片经熔融纺丝工艺制成尼龙工业丝 |

---

## 各公司分析与构建详情

### 1. 华新建材 (sh_600801) — 水泥及制品
**主营业务**: 水泥及其制品生产、销售

**产业节点分析**:
- **产出**: 水泥 (`cement`)、水泥熟料 (`clinker`)、水泥制品 (`cement_product`)、混凝土 (`concrete`)、建筑材料 (`building_material`)
- **输入**: 煤炭 (`coal`)
- **产出/服务**: 包装材料 (`packaging_material`)、包装设备 (`packaging_equipment`)

**缺失节点补充**:
- 系统中缺少 **水泥熟料** (`clinker`) 节点。水泥熟料是水泥生产的关键中间产物，应单独建节点。
- 新建边：`clinker` → `cement`（material_flow）

**暴露关系**:
- produce cement, clinker, cement_product, concrete, building_material
- procure coal
- produce packaging_material, packaging_equipment

---

### 2. 福建水泥 (sh_600802) — 水泥
**主营业务**: 水泥、商品熟料

**产业节点分析**:
- **产出**: 水泥 (`cement`)、水泥熟料 (`clinker`)
- **输入**: 煤炭 (`coal`)

**暴露关系**:
- produce cement, clinker
- procure coal

**策略**: 福建水泥为纯水泥生产企业，复用新创建的 `clinker` 节点。

---

### 3. 新奥股份 (sh_600803) — 天然气/甲醇/能源化工
**主营业务**: 液化天然气生产/销售与投资、能源技术工程服务、甲醇等能源化工产品生产、煤炭开采、洗选与贸易、生物制农兽药原料药及制剂

**产业节点分析**:
- **产出/运营**: 液化天然气 (`lng`)、LNG生产服务 (`lng_production`)、甲醇 (`methanol`)、煤炭 (`coal`)
- **服务**: 能源技术服务 (`energy_tech_service`)
- **产出**: 生物农药 (`biotech_agri_drug`)

**缺失节点补充**:
- 缺少 **LNG生产** (`lng_production`) 节点
- 缺少 **能源技术服务** (`energy_tech_service`) 节点
- 缺少 **生物农药** (`biotech_agri_drug`) 节点

**暴露关系**:
- produce lng, methanol, coal
- operate lng_production
- provide_service energy_tech_service
- produce biotech_agri_drug

**策略**: 新奥股份为多元化能源化工企业，覆盖天然气全产业链（生产、技术、贸易）、煤化工和生物农药三大板块。

---

### 4. 悦达投资 (sh_600805) — 综合类投资
**主营业务**: 公路经营、物资贸易、生物制药、拖拉机

**产业节点分析**:
- **运营**: 公路经营 (`highway_operation`)
- **服务**: 物资贸易 (`commodity_trade`)
- **产出**: 拖拉机 (`tractor`)
- **产出**: 生物制药 (`biopharmaceutical`)

**暴露关系**:
- operate highway_operation
- provide_service commodity_trade
- produce tractor
- produce biopharmaceutical

**策略**: 悦达投资为多元化投资集团，四大业务板块均赋予较高权重。

---

### 5. 济高发展 (sh_600807) — 房地产+商业+矿业
**主营业务**: 房地产+商业、矿业投资、黄金制品

**产业节点分析**:
- **运营**: 房地产开发 (`real_estate_development`)、商业地产运营 (`commercial_property_operation`)
- **产出/运营**: 黄金制品 (`gold_product`)、有色金属 (`nonferrous_metal`)

**暴露关系**:
- operate real_estate_development, commercial_property_operation
- produce gold_product
- produce nonferrous_metal

**策略**: 济高发展主业为房地产和商业，同时涉足黄金和矿业领域。

---

### 6. 马钢股份 (sh_600808) — 普钢
**主营业务**: 钢铁产品的生产和销售，主要产品为板材、长材和轮轴

**产业节点分析**:
- **产出**: 钢材板材 (`steel_sheet`)、钢材 (`steel_plate`)、棒材 (`steel_bar`)、型钢 (`steel_section`)、车轮车轴 (`wheel_axle`)
- **输入**: 焦炭 (`coke`)

**缺失节点补充**:
- 缺少 **长材** (`steel_long_product`) 节点。马钢的长材产品（螺纹钢、线材等）需要统一归类。

**暴露关系**:
- produce steel_sheet, steel_plate, steel_bar, steel_section, wheel_axle, steel_long_product
- procure coke

**策略**: 马钢为大型钢铁联合企业，产品覆盖板材、长材、轮轴三大类。长材作为钢材重要品类，新建节点以完善钢材分类体系。

---

### 7. 山西汾酒 (sh_600809) — 白酒
**主营业务**: 白酒、配制酒

**产业节点分析**:
- **产出**: 白酒 (`baijiu`)、配制酒 (`liquor`)

**暴露关系**:
- produce baijiu, liquor

**策略**: 山西汾酒为中国名酒企业，直接复用已有白酒节点。

---

### 8. 神马股份 (sh_600810) — 化纤/帘子布/工业丝
**主营业务**: 帘子布、工业丝

**产业节点分析**:
- **产出**: 帘子布 (`tire_cord_fabric`)、工业丝 (`industrial_yarn`)、尼龙 (`nylon`)、合成纤维 (`synthetic_fiber`)
- **输入/产出**: 化工产品 (`chemical_product`)、合成材料 (`synthetic_material`)
- **设备**: 纺织设备 (`textile_equipment`)

**缺失节点补充**:
- 缺少 **尼龙工业丝** (`nylon_industrial_yarn`) 节点。神马股份的核心产品工业丝以尼龙为主要原料，应单独建节点以区分其他工业丝。
- 新建边：`nylon` → `nylon_industrial_yarn`（material_flow）

**暴露关系**:
- produce tire_cord_fabric, industrial_yarn, nylon, synthetic_fiber, nylon_industrial_yarn
- procure chemical_product
- produce synthetic_material
- produce textile_equipment

**策略**: 神马股份为全球领先的尼龙66工业丝和帘子布生产企业，产业链完整。新建 `nylon_industrial_yarn` 节点以精准映射其核心产品。

---

### 9. 华北制药 (sh_600812) — 化学制药
**主营业务**: 抗感染原料药及制剂、维生素等近600余个品规

**产业节点分析**:
- **产出**: 化学原料药 (`active_pharmaceutical_ingredient`)、抗生素 (`antibiotic`)、抗生素制剂 (`antibiotic_preparation`)、维生素 (`vitamin`)、兽药 (`veterinary_medicine`)、医药原料药 (`pharmaceutical_raw_material`)

**暴露关系**:
- produce active_pharmaceutical_ingredient, antibiotic, antibiotic_preparation, vitamin, veterinary_medicine, pharmaceutical_raw_material

**策略**: 华北制药为老牌国有制药企业，产品线覆盖人用药和兽用药全品类，所有节点系统中均已存在，直接复用。

---

### 10. 杭州解百 (sh_600814) — 百货零售
**主营业务**: 商品销售业务、广告业务

**产业节点分析**:
- **运营**: 百货零售 (`department_store`)

**暴露关系**:
- operate department_store

---

## 启发与发现

1. **水泥产业链的中间产物**: 水泥熟料 (`clinker`) 作为水泥生产的关键中间产物，此前系统中缺少该节点。华新建材和福建水泥均涉及熟料生产，新建该节点有助于完善水泥产业链图谱。

2. **能源企业的多元化**: 新奥股份的业务横跨天然气、煤化工、能源技术服务和生物农药四大领域，体现了现代能源企业从单一资源商向综合能源服务商转型的趋势。LNG生产 (`lng_production`) 和能源技术服务 (`energy_tech_service`) 两个服务型节点填补了产业图在天然气产业链下游服务环节的空白。

3. **化纤产业链的精细化**: 神马股份的核心产品是尼龙66工业丝，而此前系统中已有通用的 `industrial_yarn` 节点。通过新建 `nylon_industrial_yarn` 节点，可以在产业图中区分不同原料类型的工业丝，支持更精准的产业链分析。

4. **钢铁产品分类体系**: 马钢股份的产品线覆盖板材、长材、轮轴三大类，新建 `steel_long_product`（长材）节点完善了钢材产品分类体系，与已有的板材、型材等节点形成完整的钢材产品谱系。
