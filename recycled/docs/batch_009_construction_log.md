# Batch 009 产业图与公司视图构建日志

**构建时间**: 2026-05-23
**数据来源**: `data/stock_batches/batch_009.json`
**涉及公司**: 10家中国公司

---

## 一、准备与查询

### 已有实体查询
构建前系统中已有248个产业节点、100家公司。

---

## 二、产业图构建

### 新建产业节点（4个）

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **有色** | tin_metal | 锡金属 | material | 兴业银锡 |
| **交通** | highway_operation_service | 高速公路运营服务 | service | 粤高速A |
| **造纸** | paper_product | 机制纸 | material | ST晨鸣 |
| **医疗** | health_management_service | 健康管理服务 | service | 国新健康 |

### 新建产业流边（0条）
- 本批次未新建产业流边。tin_metal作为独立有色金属节点存在；highway_operation_service、paper_product、health_management_service均为终端产品/服务节点，其上游关系已由前期批次覆盖或属于已知产业链（如纸浆→机制纸，但纸浆节点暂未创建）。

---

## 三、公司视图构建

### 10家公司全部创建成功

| 股票代码 | 公司名 | 公司ID | 核心产业 |
|---|---|---|---|
| 000423.SZ | 东阿阿胶 | dongeejiao | 阿胶及中成药 |
| 000425.SZ | 徐工机械 | xcmg | 工程机械 |
| 000426.SZ | 兴业银锡 | xingye_yinxin | 锡、银、铅锌有色金属 |
| 000428.SZ | 华天酒店 | huatian_hotel | 酒店服务、房地产 |
| 000429.SZ | 粤高速A | guangdong_expressway | 高速公路运营 |
| 000430.SZ | 张家界 | zhangjiajie | 旅游景区、酒店 |
| 000488.SZ | ST晨鸣 | chenming_paper | 机制纸 |
| 000498.SZ | 山东路桥 | shandong_road_bridge | 路桥工程施工 |
| 000501.SZ | 武商集团 | wushang_group | 百货零售 |
| 000503.SZ | 国新健康 | guoxin_health | 健康保障服务 |

### 公司节点暴露（16条）

| 公司 | 暴露节点数 | 关键暴露 |
|---|---|---|
| 东阿阿胶 | 2 | traditional_chinese_medicine, dietary_supplement (manufacture) |
| 徐工机械 | 1 | construction_machinery (manufacture) |
| 兴业银锡 | 3 | tin_metal, precious_metal, lead_zinc_metal (produce) |
| 华天酒店 | 2 | hotel_operation_service (operate), residential_property (produce) |
| 粤高速A | 1 | highway_operation_service (operate) |
| 张家界 | 2 | tourism_service, hotel_operation_service (operate) |
| ST晨鸣 | 1 | paper_product (manufacture) |
| 山东路桥 | 1 | construction_service (provide_service) |
| 武商集团 | 1 | chain_retail_service (provide_service) |
| 国新健康 | 2 | health_management_service, big_data_service (provide_service) |

---

## 四、系统状态更新

```
Total nodes: 252 (+4)
Total edges: 186 (+0)
Total companies: 110 (+10)
Total exposures: 227 (+16)
```

---

## 五、关键发现与启发

### 1. 高速公路运营服务节点的创设
- `highway_operation_service`的设立填补了交通基础设施运营服务的空白。此前已有`container_handling_service`（港口）、`airport_operation_service`（机场），高速公路的加入使交通基础设施服务体系更加完整。
- 这体现了产业图从"工业生产"向"基础设施运营"的扩展。

### 2. 有色金属节点的差异化策略
- 兴业银锡暴露了`tin_metal`、`precious_metal`（银）和`lead_zinc_metal`（锌）三个节点，均为`produce`类型。
- 与batch_005的中金岭南（铅锌采选冶一体化，暴露lead_zinc_ore/lead_zinc_metal/sulfuric_acid）相比，兴业银锡的暴露更简洁，因为公司信息未明确区分采选和冶炼环节。
- **启发**: 产业暴露的粒度取决于公开信息的详细程度。信息充分时（如年报详述工艺流程），暴露可细化到产业链各环节；信息有限时，暴露到核心产品节点即可。

### 3. 健康管理服务的数字化特征
- 国新健康同时暴露了`health_management_service`和`big_data_service`，反映了现代医疗健康管理对数据技术的深度依赖。
- PBM（医药福利管理）、TPA（第三方理赔）等业务本质上是"医疗+数据+保险"的交叉服务，单一节点难以完整覆盖，因此以`health_management_service`作为泛化节点。

### 4. 机制纸与纸包装制品的区分
- `paper_product`（机制纸，文化用纸/铜版纸）与batch_005的`paper_packaging_product`（纸包装制品，纸箱/纸盒）在产业图中并列存在。
- 两者虽然都以纸浆为原料，但终端用途（书写印刷vs产品包装）和下游客户（出版社/办公室vs制造企业）完全不同，独立节点有助于区分造纸产业的细分方向。

### 5. 旅游企业的暴露模式
- 张家界和华天酒店均暴露了`hotel_operation_service`和`tourism_service`（张家界），反映了旅游产业的"景区+酒店"联动模式。
- 这与batch_005的华侨城A（旅游综合+房地产+纸包装）形成了旅游产业的层次：景区运营（张家界）→ 旅游综合体（华侨城A）。

---

## 六、后续批次建议

1. **白酒产业**: batch_010中的新金路（000510）涉及白酒生产，已新建`liquor`节点。
2. **医疗服务**: batch_010中的国际医学（000516）需要新建`medical_service`节点。
3. **食用油**: batch_010中的京粮控股（000505）需要新建`edible_oil`节点。
