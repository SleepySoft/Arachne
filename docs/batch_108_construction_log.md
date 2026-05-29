# Batch 108 产业图构建日志

## 批次信息
- **批次号**: 108
- **股票代码范围**: 600863.SH - 600873.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_108_nodes`)：补充7个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_108_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：7个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：28条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `nucleotide` | 核苷酸 | material | 由含氮碱基、五碳糖和磷酸基团组成的生物小分子，在食品工业中用作呈味剂（呈味核苷酸二钠，I+G）。 |
| `recombinant_human_insulin` | 重组人胰岛素 | material | 利用基因重组技术生产的人胰岛素，与人自身胰岛素氨基酸序列完全一致，用于治疗糖尿病。 |
| `infusion_solution` | 大输液制品 | material | 容量不小于50ml并直接由静脉滴注输入体内的无菌液体制剂，是临床治疗中用量最大的药品剂型之一。 |
| `carbon_fiber_composite_conductor` | 碳纤维复合芯导线 | component | 以碳纤维复合材料棒作为芯体、外层绞合铝线的架空输电导线，可大幅提高输电容量并降低线路损耗。 |
| `petroleum_engineering_service` | 石油工程技术服务 | service | 为油气勘探、开发、生产全过程提供的技术服务和工程施工服务，包括钻井、测井、压裂、油田地面建设等。 |
| `amino_acid` | 氨基酸 | material | 含有氨基和羧基的一类有机化合物，是构成蛋白质的基本单位，在食品、饲料、医药领域广泛应用。 |
| `organic_fertilizer` | 有机肥 | material | 主要来源于植物和（或）动物，施于土壤以提供植物营养的含碳物料，能改善土壤结构、提高土壤肥力。 |

---

## 各公司分析与构建详情

### 1. 华能蒙电 (sh_600863) — 火力发电/风电/供热
**主营业务**: 电力、热力。火力发电、风力发电以及其他新能源发电和供应

**暴露关系**:
- operate thermal_power_generation
- operate wind_power_generation
- provide_service heat_supply
- procure coal

---

### 2. 哈投股份 (sh_600864) — 热电/证券
**主营业务**: 热电业务和证券业务

**暴露关系**:
- operate thermal_power_generation
- provide_service securities_brokerage

---

### 3. 百大集团 (sh_600865) — 百货/旅游
**主营业务**: 百货、旅游服务

**暴露关系**:
- operate department_store
- provide_service tourism_service

---

### 4. 星湖科技 (sh_600866) — 核苷酸/味精/酱油/原料药
**主营业务**: 肌苷、利巴韦林、脯氨酸、腺苷及其他、呈味核苷酸、味精、酱油

**暴露关系**:
- produce nucleotide
- produce monosodium_glutamate
- produce soy_sauce
- produce pharmaceutical_raw_material

**策略**: 星湖科技是全球主要的呈味核苷酸（I+G）生产商之一，与味精形成协同鲜味效应。`nucleotide` 节点的加入丰富了食品添加剂产业图谱。

---

### 5. 通化东宝 (sh_600867) — 重组人胰岛素/大输液/中成药
**主营业务**: 主要产品为重组人胰岛素冻干粉及注射液、大输液制品、镇脑宁胶囊、东宝甘泰片、塑钢窗等

**暴露关系**:
- produce recombinant_human_insulin (weight=1.0)
- produce infusion_solution (weight=0.8)
- produce chinese_patent_medicine (weight=0.6)

**策略**: 通化东宝是中国重组人胰岛素产业的开创者，`recombinant_human_insulin` 节点的加入对糖尿病治疗产业链具有重要意义。

---

### 6. 梅雁吉祥 (sh_600868) — 水电/制造业
**主营业务**: 电力生产、生产制造加工业

**暴露关系**:
- produce electricity_power
- provide_service manufacturing

---

### 7. 远东股份 (sh_600869) — 电线电缆/碳纤维导线
**主营业务**: 主要产品：电力电缆、电气装备用电线电缆、裸导线、碳纤维复合芯软铝导线等

**暴露关系**:
- produce power_cable
- produce wire_cable
- produce carbon_fiber_composite_conductor

**策略**: 远东股份是全球领先的电线电缆制造商，其碳纤维复合芯导线（ACCC）技术代表了输电线路的先进方向。`carbon_fiber_composite_conductor` 节点的加入完善了新能源输配电产业链。

---

### 8. 石化油服 (sh_600871) — 油气勘探开发工程服务
**主营业务**: 油气勘探开发工程施工与技术服务

**暴露关系**:
- provide_service petroleum_exploration
- provide_service petroleum_engineering_service

**策略**: 石化油服是中国石化集团旗下专业化油服公司，员工超过5.7万人，是全球最大的石油工程技术服务公司之一。`petroleum_engineering_service` 节点的加入对能源产业链至关重要。

---

### 9. 中炬高新 (sh_600872) — 调味品/汽车配件/房地产
**主营业务**: 主要以调味品、汽车配件、房地产及园区服务为主导

**暴露关系**:
- produce food_condiment
- produce auto_parts
- operate real_estate_development

**策略**: 复用系统中已有的 `food_condiment` 节点映射调味品业务。

---

### 10. 梅花生物 (sh_600873) — 味精/氨基酸/有机肥
**主营业务**: 味精、氨基酸、有机肥等生物发酵产品的生产及销售

**暴露关系**:
- produce monosodium_glutamate
- produce amino_acid
- produce organic_fertilizer

**策略**: 梅花生物是全球最大的味精和氨基酸生产企业之一，`amino_acid` 和 `organic_fertilizer` 节点的加入完善了生物发酵产业链图谱。

---

## 启发与发现

1. **生物发酵产业链的完善**：本批次通过星湖科技、梅花生物和通化东宝三家公司，构建了从上游原料（氨基酸、核苷酸）到中游制剂（味精、酱油、大输液）再到下游应用（医药、食品、农业）的完整生物发酵产业图谱。

2. **糖尿病治疗产业链**：通化东宝的 `recombinant_human_insulin` 节点是中国生物制药产业的重要里程碑。胰岛素作为糖尿病治疗的核心药物，其产业链节点对后续分析制药企业竞争格局具有重要价值。

3. **新能源输配电技术**：远东股份的 `carbon_fiber_composite_conductor` 代表了输电线路材料的革命性进步，其轻质高强的特性使得在不更换铁塔的情况下即可大幅提升线路输送容量。

4. **能源服务产业链**：石化油服的 `petroleum_engineering_service` 节点与此前已有的 `petroleum_exploration` 节点形成了"勘探-工程服务"的上下游关系，进一步完善了石油天然气产业链。
