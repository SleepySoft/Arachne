# Batch 107 产业图构建日志

## 批次信息
- **批次号**: 107
- **股票代码范围**: 600851.SH - 600862.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要

本次提交通过两个步骤完成：
1. **GraphRegistrationBatch** (`batch_107_nodes`)：补充6个缺失的产业节点
2. **BusinessRegistrationBatch** (`batch_107_business`)：注册10家公司及其产业节点暴露

### 提交结果
- 新建产业节点：6个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：22条

---

## 新增节点详情

| node_id | canonical_name_zh | entity_type | definition |
|---------|-------------------|-------------|------------|
| `plush_textile` | 长毛绒纺织 | material | 以起毛组织或割绒工艺在织物表面形成致密、丰满绒毛层的纺织面料，广泛用于玩具、服装、家居装饰等领域。 |
| `highway_bridge_construction` | 公路桥梁施工 | service | 对公路、桥梁、隧道等交通基础设施进行土建施工、结构安装和路面铺设的工程建设服务。 |
| `security_service` | 安保服务 | service | 为社会公共安全领域提供的专业化安全保护服务，包括视频监控、入侵报警、门禁控制、安保人员派遣等。 |
| `gas_storage_equipment` | 气体储运装备 | device | 用于压缩气体、液化气体的储存、运输和配送的专用压力容器及配套设备，包括低温储罐、高压气瓶、长管拖车等。 |
| `human_resource_service` | 人力资源服务 | service | 为企业或个人提供的人力资源管理外包服务，包括人才招聘、劳务派遣、薪酬管理、社保代理、培训发展等。 |
| `aviation_new_material` | 航空新材料 | material | 专门用于航空器制造的高性能结构材料和功能材料，包括碳纤维复合材料、高温合金、钛合金、特种陶瓷、隐身材料等。 |

---

## 各公司分析与构建详情

### 1. 海欣股份 (sh_600851) — 长毛绒纺织/医药/金融投资
**主营业务**: 长毛绒纺织、医药、金融投资等

**暴露关系**:
- produce plush_textile (weight=1.0)
- produce pharmaceutical_manufacturing (weight=0.7)
- provide_service financial_investment (weight=0.6)

---

### 2. 龙建股份 (sh_600853) — 公路桥梁施工
**主营业务**: 公路桥梁施工建设

**暴露关系**:
- provide_service highway_bridge_construction (weight=1.0)
- provide_service bridge_construction (weight=0.9)

**策略**: 龙建股份拥有公路工程施工总承包特级资质，核心业务是公路桥梁施工。系统中已有 `bridge_construction` 节点，本批次新建更精确的 `highway_bridge_construction` 节点。

---

### 3. 春兰股份 (sh_600854) — 空调器
**主营业务**: 空调器

**暴露关系**:
- produce air_conditioner (weight=1.0)
- produce compressor (weight=0.7)

---

### 4. 航天长峰 (sh_600855) — 安保/医疗器械/电子信息
**主营业务**: 安保业务、医疗器械与工程服务业务以及电子信息业务

**暴露关系**:
- provide_service security_service (weight=1.0)
- produce medical_device (weight=0.8)
- produce electronic_information (weight=0.8)

---

### 5. 宁波中百 (sh_600857) — 商业/软件
**主营业务**: 商业、软件业务

**暴露关系**:
- operate department_store (weight=1.0)
- provide_service software_development_service (weight=0.5)

---

### 6. 银座股份 (sh_600858) — 商品零售/供电/供汽
**主营业务**: 商品零售、供电、供汽

**暴露关系**:
- operate department_store (weight=1.0)
- produce electricity_power (weight=0.6)
- produce steam_supply (weight=0.6)

---

### 7. 王府井 (sh_600859) — 百货零售
**主营业务**: 百货零售

**暴露关系**:
- operate department_store

---

### 8. 京城股份 (sh_600860) — 气体储运装备
**主营业务**: 气体储运装备业务

**暴露关系**:
- produce gas_storage_equipment

---

### 9. 北京人力 (sh_600861) — 人力资源服务
**主营业务**: 人力资源服务

**暴露关系**:
- provide_service human_resource_service

---

### 10. 中航高科 (sh_600862) — 航空新材料/智能装备
**主营业务**: 航空新材料、高端智能装备、轨道交通、汽车、医疗器械、装备制造、房地产、创新创业投资等

**暴露关系**:
- produce aviation_new_material (weight=1.0)
- produce intelligent_equipment (weight=0.8)
- produce medical_device (weight=0.5)
- operate real_estate_development (weight=0.4)

---

## 启发与发现

1. **纺织服装产业的细分**：海欣股份的长毛绒纺织业务促使新建 `plush_textile` 节点。此前系统中已有 `flax_textile`、`wool_textile` 等节点，长毛绒纺织的加入使纺织材料分类更加完善。

2. **基础设施建设的精准映射**：龙建股份的核心竞争力是公路桥梁施工，新建 `highway_bridge_construction` 节点比泛化的 `bridge_construction` 更能精准反映企业的专业施工领域。

3. **人力资源服务的产业化**：北京人力（原北京城乡）是A股市场稀缺的纯正人力资源服务标的。`human_resource_service` 节点的加入填补了产业图在服务业领域的空白。

4. **航空新材料的重要性**：中航高科隶属于中国航空工业集团，其航空新材料业务（主要是预浸料和蜂窝芯材）是国产大飞机C919和歼击机等航空器的关键材料供应商。`aviation_new_material` 节点的加入对航空产业链具有重要意义。
