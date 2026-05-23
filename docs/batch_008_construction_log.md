# Batch 008 产业图与公司视图构建日志

**构建时间**: 2026-05-23
**数据来源**: `data/stock_batches/batch_008.json`
**涉及公司**: 10家中国公司

---

## 一、准备与查询

### 已有实体查询
构建前系统中已有237个产业节点、80家公司。

---

## 二、产业图构建

### 新建产业节点（7个）

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **化肥** | potassium_chloride | 氯化钾 | material | 藏格矿业 |
| **IT** | industrial_internet_platform | 工业互联网平台 | service | 云鼎科技 |
| **矿业** | smart_mining_service | 智能矿山服务 | service | 云鼎科技 |
| **装备** | machine_tool | 机床 | device | 沈阳机床 |
| **航空** | aircraft | 航空器 | device | 渤海租赁 |
| **化纤** | viscose_fiber | 粘胶纤维 | material | 吉林化纤 |
| **化工** | caustic_soda | 烧碱 | material | 湖北宜化 |

### 新建产业流边（2条）

1. **化肥**: potassium_chloride → chemical_fertilizer（氯化钾作为化肥原料）
2. **装备**: steel_sheet → machine_tool（钢材作为机床原材料）

---

## 三、公司视图构建

### 10家公司全部创建成功

| 股票代码 | 公司名 | 公司ID | 核心产业 |
|---|---|---|---|
| 000408.SZ | 藏格矿业 | zangge_mining | 氯化钾开采 |
| 000409.SZ | 云鼎科技 | yunding_tech | 工业互联网、智能矿山 |
| 000410.SZ | 沈阳机床 | shenyang_machine_tool | 数控机床 |
| 000411.SZ | 英特集团 | inte_group | 医药流通 |
| 000415.SZ | 渤海租赁 | bohai_leasing | 飞机/集装箱租赁 |
| 000417.SZ | 合百集团 | hebai_group | 百货零售 |
| 000419.SZ | 通程控股 | tongcheng | 商贸、酒店、旅游 |
| 000420.SZ | 吉林化纤 | jilin_chemical_fiber | 粘胶纤维 |
| 000421.SZ | 南京公用 | nanjing_public | 公用事业、房地产 |
| 000422.SZ | 湖北宜化 | hubei_yihua | 化肥、氯碱化工 |

### 公司节点暴露（23条）

| 公司 | 暴露节点数 | 关键暴露 |
|---|---|---|
| 藏格矿业 | 1 | potassium_chloride (produce) |
| 云鼎科技 | 4 | industrial_internet_platform, smart_mining_service, cloud_solution, information_system_integration (provide_service) |
| 沈阳机床 | 1 | machine_tool (manufacture) |
| 英特集团 | 4 | pharmaceutical_distribution, medical_device, traditional_chinese_medicine, textile_product (provide_service) |
| 渤海租赁 | 2 | aircraft, container (operate) |
| 合百集团 | 1 | chain_retail_service (provide_service) |
| 通程控股 | 3 | chain_retail_service, hotel_operation_service, tourism_service |
| 吉林化纤 | 1 | viscose_fiber (manufacture) |
| 南京公用 | 3 | residential_property, tourism_service, chain_retail_service |
| 湖北宜化 | 3 | chemical_fertilizer, plastic_resin, caustic_soda (manufacture) |

---

## 四、系统状态更新

```
Total nodes: 244 (+7)
Total edges: 185 (+2)
Total companies: 90 (+10)
Total exposures: 211 (+23)
```

---

## 五、关键发现与启发

### 1. 工业互联网与智能矿山的节点创设
- 云鼎科技代表了传统IT服务向垂直行业（矿山、能源）的深化。`industrial_internet_platform`和`smart_mining_service`的建立，标志着产业图从通用IT服务向行业专用服务的扩展。
- 这与batch_006中的`telecom_software`、batch_005中的`electronic_component_distribution_service`形成了服务业态的层次结构：通用IT → 行业IT → 工业平台。

### 2. 租赁公司的产业暴露处理
- 渤海租赁是典型的金融租赁企业，本身不生产实体产品。但在产业图中，其拥有的`aircraft`和`container`资产需要被记录。
- 采用`operate`活动类型来反映租赁公司对实物资产的运营管理角色，这是金融资本与产业实体结合的一种表达方式。
- 但这也意味着产业图开始涉及"资产所有权"维度，与传统"生产/服务"维度有所扩展。

### 3. 人造纤维与合成纤维的并列
- `viscose_fiber`（粘胶纤维，人造纤维）与batch_007的`polyester_filament`（涤纶长丝，合成纤维）在产业图中并列存在。
- 两者虽然都是化学纤维，但原料来源（天然纤维素vs石油化工）和生产工艺（湿法纺丝vs熔体纺丝）截然不同，独立节点有助于区分纺织原材料的技术路线。

### 4. 氯碱化工的节点补充
- `caustic_soda`（烧碱）与已有`chemical_fertilizer`、`plastic_resin`共同构成了湖北宜化的三大产品线。
- 烧碱是重要的基础化工原料，其节点的建立为后续造纸、纺织印染、水处理等下游产业提供了上游连接点。

### 5. 医药流通的重复暴露模式
- 英特集团作为医药流通商，同时暴露了`pharmaceutical_distribution`、`medical_device`、`traditional_chinese_medicine`三个节点，均为`provide_service`类型。
- 这与batch_005的ST海王（医药制造+流通）形成了对比：制造型医药企业暴露`manufacture`，流通型企业暴露`provide_service`。

---

## 六、后续批次建议

1. **工程机械**: batch_009中的徐工机械（000425）与中联重科（batch_007）同属工程机械行业，可直接复用`construction_machinery`节点。
2. **造纸**: batch_009中的ST晨鸣（000488）主营机制纸，需要新建`paper_product`节点。
3. **高速公路**: batch_009中的粤高速A（000429）需要新建`highway_operation_service`节点。
4. **旅游**: batch_009中的张家界（000430）和batch_008中的通程控股均可复用`tourism_service`。
5. **健康保障服务**: batch_009中的国新健康（000503）需要新建`health_insurance_service`或`health_management_service`节点。
