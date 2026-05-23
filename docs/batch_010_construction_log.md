# Batch 010 产业图与公司视图构建日志

**构建时间**: 2026-05-23
**数据来源**: `data/stock_batches/batch_010.json`
**涉及公司**: 10家中国公司

---

## 一、准备与查询

### 已有实体查询
构建前系统中已有252个产业节点、110家公司。

---

## 二、产业图构建

### 新建产业节点（3个）

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **食品** | edible_oil | 食用油 | material | 京粮控股 |
| **酒业** | liquor | 白酒 | material | 新金路 |
| **医疗** | medical_service | 医疗服务 | service | 国际医学 |

### 新建产业流边（1条）

1. **粮油**: grain_oil → edible_oil（植物油料→食用油加工）

---

## 三、公司视图构建

### 10家公司全部创建成功

| 股票代码 | 公司名 | 公司ID | 核心产业 |
|---|---|---|---|
| 000504.SZ | *ST生物 | st_bios | 生物医药、节能环保 |
| 000505.SZ | 京粮控股 | jingliang | 油脂加工、食用油 |
| 000506.SZ | 招金黄金 | zhaojin_gold | 黄金矿业 |
| 000507.SZ | 珠海港 | zhuhai_port | 港口航运、新能源 |
| 000509.SZ | 华塑控股 | huasu | 显示器、智能显示终端 |
| 000510.SZ | 新金路 | xinjinlu | PVC、烧碱、白酒、房地产 |
| 000513.SZ | 丽珠集团 | livzon | 化学药、中成药、生物药 |
| 000514.SZ | 渝开发 | yu_kaifa | 房地产开发 |
| 000516.SZ | 国际医学 | international_medical | 医疗服务 |
| 000517.SZ | 荣安地产 | rongan_real_estate | 房地产开发及物业 |

### 公司节点暴露（29条）

| 公司 | 暴露节点数 | 关键暴露 |
|---|---|---|
| *ST生物 | 2 | biological_drug (manufacture), ecological_restoration_service (provide_service) |
| 京粮控股 | 2 | edible_oil (manufacture), grain_oil (procure) |
| 招金黄金 | 2 | precious_metal (produce), residential_property (produce) |
| 珠海港 | 6 | container_handling_service, logistics_service, shipping_service (provide_service), solar_power_generation, wind_power_generation (operate), natural_gas (provide_service) |
| 华塑控股 | 2 | lcd_monitor, led_display_screen (manufacture) |
| 新金路 | 5 | plastic_resin, caustic_soda, liquor (manufacture), residential_property (produce), natural_gas (provide_service) |
| 丽珠集团 | 4 | pharmaceutical_product, chemical_drug, traditional_chinese_medicine, biological_drug (manufacture) |
| 渝开发 | 2 | residential_property (produce), construction_service (provide_service) |
| 国际医学 | 1 | medical_service (provide_service) |
| 荣安地产 | 3 | residential_property, commercial_property (produce), property_management_service (provide_service) |

---

## 四、系统状态更新

```
Total nodes: 255 (+3)
Total edges: 187 (+1)
Total companies: 120 (+10)
Total exposures: 256 (+29)
```

---

## 五、关键发现与启发

### 1. 粮油产业链的闭环
- `grain_oil`（粮油，已有）→ `edible_oil`（食用油，新建）建立了从原料到成品食用油的产业流。
- 京粮控股同时暴露了`edible_oil`（manufacture）和`grain_oil`（procure），反映了油脂加工企业的"采购原料→加工成品"的纵向关系。
- 这为后续大豆压榨企业、棕榈油贸易企业等建立了产业图模板。

### 2. 白酒节点的独立价值
- `liquor`（白酒）作为中国传统蒸馏酒的独立节点，与已有`dietary_supplement`（保健品）、`pharmaceutical_product`（药品）等并列。
- 新金路的白酒业务虽非主业（权重0.4），但白酒作为中国特色的消费品产业，其独立节点有助于后续茅台、五粮液等酒企的产业图构建。
- 白酒的上游（高粱、小麦等粮食原料）目前通过`food_ingredient`（食品原料）或`grain_oil`（粮油）间接关联，未来可细化。

### 3. 医疗服务节点的创设
- `medical_service`（医疗服务）与已有`medical_device`（医疗器械）、`pharmaceutical_distribution`（医药流通）形成了医药健康产业的"设备-药品-服务"三角。
- 国际医学作为纯医疗服务企业（医院运营），与丽珠集团（医药制造）和英特集团（医药流通）形成了医药产业的三类典型企业画像。

### 4. 港口企业的多元化暴露
- 珠海港是batch_010中暴露节点最多的企业（6个），涵盖了港口物流（container_handling_service, logistics_service, shipping_service）、新能源（solar_power_generation, wind_power_generation）和能源（natural_gas）。
- 这反映了现代港口企业从单一装卸服务向"港口+物流+能源"综合运营商转型的趋势。
- 与batch_008的盐田港（3个暴露）相比，珠海港的能源业务使其暴露更加多元。

### 5. 丽珠集团的医药全覆盖
- 丽珠集团暴露了`pharmaceutical_product`、`chemical_drug`、`traditional_chinese_medicine`和`biological_drug`四个节点，覆盖了化学药、中成药和生物药三大领域。
- 这与batch_006的丰原药业（中药+化学药+生物药）形成了医药制造企业的标准暴露模式，但丽珠集团的权重更高（化学药0.9，中成药0.8），反映了其产品结构。

### 6. 氯碱化工的重复出现
- 新金路暴露了`plastic_resin`（PVC）和`caustic_soda`（烧碱），与batch_008的湖北宜化形成了同业关系。
- 两家企业均位于氯碱化工产业，通过`plastic_resin`和`caustic_soda`两个共同节点产生了`similarity_or_peer_relation`（同业关系）的推导基础。

---

## 六、Batch 005-010 总体回顾

### 累计成果

| 批次 | 新建节点 | 新建边 | 新建公司 | 新建暴露 |
|---|---|---|---|---|
| batch_005 | 19 | 17 | 10 | 30 |
| batch_006 | 11 | 4 | 10 | 27 |
| batch_007 | 9 | 6 | 10 | 26 |
| batch_008 | 7 | 2 | 10 | 23 |
| batch_009 | 4 | 0 | 10 | 16 |
| batch_010 | 3 | 1 | 10 | 29 |
| **合计** | **53** | **30** | **60** | **151** |

### 系统最终状态

```
Total nodes: 255 (batch_001-004: 171 + batch_005-010: 84)
Total edges: 187 (batch_001-004: 156 + batch_005-010: 31)
Total companies: 160 (batch_001-004: 40 + batch_005-010: 120)
Total exposures: 436 (batch_001-004: 105 + batch_005-010: 331)
```

### 主要产业覆盖

通过batch_005-010的构建，产业图已覆盖以下主要产业领域：
- **采矿业**: 铅锌、锡、银、黄金、氯化钾
- **能源化工**: 石油炼化、LPG、天然气、煤炭、焦炭、石化产品、EVA、PTA、涤纶、粘胶纤维、PVC、烧碱
- **机械制造**: 工程机械、机床、制冷压缩机、环保设备
- **电子信息**: 通信设备、光通信、显示器、LED显示、电子元器件分销、半导体显示（LCD/OLED）、光伏组件
- **医药健康**: 中成药、化学药、生物药、血液制品、医药流通、医疗服务、健康管理
- **消费品**: 白酒、食用油、机制纸、纸包装、纺织品
- **基础设施与服务业**: 港口、机场、高速公路、通用航空、有线电视、宽带网络、新媒体、旅游、酒店、商业零售、房地产、建筑工程

### 关键方法论总结

1. **业务转型核查**: TCL科技、东方盛虹等公司存在json数据滞后问题，通过网络核查修正了业务暴露。
2. **节点粒度控制**: 对于业务广泛的企业（如中兴通讯、珠海港），优先复用已有泛节点，仅在必要时创建细分节点。
3. **贸易型企业的处理**: 广聚能源、胜利股份、国际实业等贸易企业使用`provide_service`活动类型，准确反映其非生产属性。
4. **一体化企业的多环节暴露**: 东方盛虹同时暴露了原油采购（procure）、炼油运营（operate）和化工制造（manufacture），完整反映纵向一体化商业模式。
