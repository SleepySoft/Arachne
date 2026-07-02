# Batch 007 产业图与公司视图构建日志

**构建时间**: 2026-05-23
**数据来源**: `data/stock_batches/batch_007.json`
**涉及公司**: 10家中国公司

---

## 一、准备与查询

### 已有实体查询
构建前系统中已有221个产业节点、60家公司。

### 关键网络核查
- **东方盛虹（000301.SZ）**: 经网络核查，东方盛虹已完成从传统纺织企业向大型石化-化纤一体化企业的战略转型。当前核心产业为**炼化（1,600万吨/年原油加工）**、**PTA（390万吨/年）**、**涤纶长丝（360万吨/年）**及**EVA树脂（50万吨/年）**。原始json中的"纺织,贸易,电力,热能,房地产"信息严重过时，本次构建基于2024年年报最新业务披露，建立了从原油采购到化纤/新材料制造的完整产业链暴露。

---

## 二、产业图构建

### 新建产业节点（9个）

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **机械** | construction_machinery | 工程机械 | device | 中联重科 |
| **纺织** | textile_product | 纺织品 | material | 常山北明 |
| **煤炭** | coke | 焦炭 | material | 国际实业 |
| **石化** | pta | 精对苯二甲酸 | material | 东方盛虹 |
| **化纤** | polyester_filament | 涤纶长丝 | material | 东方盛虹 |
| **化工** | eva_resin | EVA树脂 | material | 东方盛虹 |
| **电力** | power_distribution_equipment | 配电设备 | device | 许继电气 |
| **医药** | blood_product | 血液制品 | material | 派林生物 |
| **家电** | refrigeration_compressor | 制冷压缩机 | component | 长虹华意 |

### 新建产业流边（6条）

1. **煤炭**: coal → coke（烟煤高温干馏制焦炭）
2. **石化**: refining_service → pta（炼化一体化产出PTA）
3. **化纤**: pta → polyester_filament（PTA聚合纺丝制涤纶长丝）
4. **化工**: refining_service → eva_resin（乙烯共聚制EVA）
5. **光伏**: eva_resin → photovoltaic_module（EVA胶膜封装光伏组件）
6. **家电**: refrigeration_compressor → refrigerator（压缩机组装成冰箱）

---

## 三、公司视图构建

### 10家公司全部创建成功

| 股票代码 | 公司名 | 公司ID | 核心产业 |
|---|---|---|---|
| 000157.SZ | 中联重科 | zoomlion | 工程机械 |
| 000158.SZ | 常山北明 | changshan_beiming | 棉纺织、软件IT |
| 000159.SZ | 国际实业 | guoji_industry | 煤炭焦炭贸易、房地产 |
| 000301.SZ | 东方盛虹 | eastern_shenghong | 炼化、PTA、涤纶、EVA |
| 000400.SZ | 许继电气 | xj_electric | 配电设备、智能电表 |
| 000401.SZ | 金隅冀东 | jinyu_jidong | 水泥制造 |
| 000402.SZ | 金融街 | financial_street | 商业地产开发运营 |
| 000403.SZ | 派林生物 | pailin_biological | 血液制品 |
| 000404.SZ | 长虹华意 | changhong_huayi | 冰箱压缩机 |
| 000407.SZ | 胜利股份 | shengli | 天然气、农化、塑胶贸易 |

### 公司节点暴露（26条）

| 公司 | 暴露节点数 | 关键暴露 |
|---|---|---|
| 中联重科 | 1 | construction_machinery (manufacture) |
| 常山北明 | 2 | textile_product (manufacture), information_system_integration (provide_service) |
| 国际实业 | 3 | coal (provide_service), coke (provide_service), residential_property (produce) |
| 东方盛虹 | 6 | crude_oil (procure), refining_service (operate), pta (manufacture), polyester_filament (manufacture), eva_resin (manufacture), petrochemical_product (manufacture) |
| 许继电气 | 3 | power_distribution_equipment (manufacture), smart_meter (manufacture), electricity_distribution (provide_service) |
| 金隅冀东 | 1 | cement (manufacture) |
| 金融街 | 4 | residential_property (produce), commercial_property (produce), property_management_service (provide_service), housing_rental_service (provide_service) |
| 派林生物 | 2 | blood_product (manufacture), biological_drug (manufacture) |
| 长虹华意 | 1 | refrigeration_compressor (manufacture) |
| 胜利股份 | 3 | natural_gas (provide_service), chemical_fertilizer (provide_service), plastic_resin (provide_service) |

---

## 四、系统状态更新

```
Total nodes: 230 (+9)
Total edges: 183 (+6)
Total companies: 70 (+10)
Total exposures: 188 (+26)
```

---

## 五、关键发现与启发

### 1. 民营炼化巨头的产业链构建
- 东方盛虹是batch_007中最复杂的产业链案例。公司实现了"原油 → 炼油 → PX/PTA → 涤纶长丝"和"原油 → 炼油 → 乙烯 → EVA"两条产业主线。
- 在产业图中，东方盛虹同时暴露了`crude_oil`（采购）、`refining_service`（运营）、`pta`/`polyester_filament`/`eva_resin`/`petrochemical_product`（制造），完整反映了其纵向一体化特征。
- **启发**: 对于一体化巨头， company's exposures 可以跨越产业链多个环节（上游采购→中游运营→下游制造），这是产业图准确反映企业商业模式的关键。

### 2. 传统产业的节点补充
- `coke`（焦炭）节点的建立填补了煤炭→钢铁产业链的中间环节。国际实业作为贸易商，虽非生产者，但通过贸易活动连接了coal和coke两个节点。
- `refrigeration_compressor`（制冷压缩机）作为冰箱的核心部件，建立了与已有`refrigerator`节点的组成关系，完善了家电产业链。

### 3. 血液制品的独立节点
- `blood_product`从`biological_drug`中独立出来，因为血液制品（血浆提取）与重组蛋白、疫苗等生物药在生产工艺和监管体系上有显著差异。
- 派林生物同时暴露到`blood_product`和`biological_drug`，体现了血液制品在医药分类中的双重属性。

### 4. 双主业企业的暴露策略
- 常山北明是典型的"传统纺织+软件IT"双主业企业。其暴露同时覆盖了`textile_product`（制造）和`information_system_integration`（服务），权重分别为0.7和0.8，反映了两个业务并重的格局。
- 软件业务的权重略高，体现了公司向数字化转型的战略方向。

### 5. 贸易型企业的暴露边界
- 国际实业和胜利股份均为贸易型企业。它们的暴露使用了`provide_service`活动类型，而非`manufacture`或`produce`，准确反映了贸易中介属性。
- 产业图不记录具体的贸易流，但公司通过暴露到多个产业节点，反映了其贸易范围的广度。

---

## 六、后续批次建议

1. **化肥化工**: batch_008中的湖北宜化（000422）主营尿素、磷酸二铵、PVC、烧碱等，可复用已有`chemical_fertilizer`节点，可能需要新建`urea`（尿素）节点。
2. **钾盐矿业**: batch_008中的藏格矿业（000408）主营氯化钾，需要新建`potassium_chloride`节点。
3. **机床制造**: batch_008中的沈阳机床（000410）需要新建`machine_tool`节点。
4. **粘胶纤维**: batch_008中的吉林化纤（000420）主营粘胶长丝，需要新建`viscose_fiber`节点与已有`polyester_filament`形成对比。
