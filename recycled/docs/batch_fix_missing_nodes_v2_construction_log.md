# Batch Fix Missing Nodes v2 Construction Log

**Date:** 2026-05-25
**Type:** 错误修复与数据补充
**Status:** ✅ 全部修复成功

---

## 修复背景

在 batches 031–033 的提交过程中，共有 **5 条边因引用的目标节点不存在而失败**。此前采用"后续批次自然补充"的增量策略，但这种方式导致边数据不完整且错误信息不清晰。本次修复通过**网络搜索补充缺失节点的可靠数据**，并重新提交失败的边。

## 1. 新增 Industrial Nodes (+5)

| # | Node ID | Name (ZH) | Entity Type | 数据来源 |
|---|---------|-----------|-------------|----------|
| 1 | `flat_glass` | 平板玻璃 | material | GB/T15764-2008《平板玻璃术语》、头豹研究院行业报告 |
| 2 | `sugar_cane` | 甘蔗 | material | OECD-FAO 农业展望、百度百科"甘蔗制糖" |
| 3 | `oilfield_service` | 油气田服务 | service | 中国油田服务行业研究报告、新疆科力新三板公开转让说明书 |
| 4 | `public_transportation` | 公共交通 | service | 百度百科"公共交通"、CJJ/T 114-2007《城市公共交通分类标准》 |
| 5 | `ship` | 船舶 | system | 华南理工大学《船舶与海洋结构物构造》、前瞻产业研究院 |

### 节点详情

**`flat_glass`（平板玻璃）**
- 以石英砂、纯碱、石灰石、长石等无机矿物为主要原料，经1600℃高温熔融、成型（主要为浮法工艺）、退火等工序制成的板状钠钙硅酸盐玻璃。
- 关键数据：纯碱占原材料成本的54%，石英砂占27%；浮法工艺占比80%-90%。
- 下游应用：建筑采光（最大）、汽车车窗（约20%）、光伏面板、电子显示。

**`sugar_cane`（甘蔗）**
- 禾本科甘蔗属热带及亚热带多年生草本植物，茎秆富含蔗糖（12%-18%）。
- 关键数据：占全球食糖产量86%以上；中国主产区为广西、云南、广东、海南。
- 综合利用：蔗渣造纸/环保餐具、糖蜜发酵生产酒精和酵母、滤泥制有机肥。

**`oilfield_service`（油气田服务）**
- 为石油天然气勘探、钻井、完井、采油、增产、集输及后期维护提供工程技术支持和解决方案的生产性服务行业。
- 五大板块：地球物理勘探、钻井完井、测井录井、油气生产处理、油田信息化建设。
- 2025年全球市场规模约1459亿美元。

**`public_transportation`（公共交通）**
- 城市或城际范围内向公众开放的、定线运营的客运交通服务系统。
- 涵盖：公共汽车、轨道交通（地铁/轻轨/有轨电车）、BRT、渡轮、索道等。
- 城市客运骨干，缓解交通拥堵的关键基础设施。

**`ship`（船舶）**
- 能航行或停泊于水域进行运输或作业的交通工具，由船体、推进系统、导航设备和功能舱室组成。
- 按用途分：运输船（货船/客船/油轮/集装箱船）、工程船、渔业船、军用舰艇等。
- 现代船舶多为钢制结构，采用内燃机或电力推进。

## 2. 修复 Industrial Edges (+5)

| # | Edge ID | From Node → To Node | Type | 原批次 |
|---|---------|---------------------|------|--------|
| 1 | `flow_soda_ash_to_glass` | soda_ash → flat_glass | material_flow | 031 |
| 2 | `flow_sugar_cane_to_white_sugar` | sugar_cane → white_sugar | material_flow | 032 |
| 3 | `flow_drilling_tool_to_oilfield` | oil_drilling_tool → oilfield_service | composition | 032 |
| 4 | `flow_bus_to_transport` | bus → public_transportation | service_flow | 033 |
| 5 | `flow_marine_engine_to_ship` | marine_engine → ship | composition | 033 |

## 3. 后端缺陷修复

**问题：** `neo4j_storage.py` 中 `create_industrial_flow_edge` 和 `create_ontology_edge` 在节点缺失时未处理 `None` 结果，导致抛出 `'NoneType' object is not subscriptable`。

**修复：** 在两个函数中添加 `None` 防御：
```python
record = await result.single()
if record is None:
    raise ValueError(f"Cannot create edge: from_node '{edge.from_node}' or to_node '{edge.to_node}' does not exist")
```

## 4. API Submission Results

```json
{
  "batch_id": "batch_fix_missing_nodes_v2_graph",
  "status": 201,
  "nodes_created": 5,
  "nodes_updated": 0,
  "edges_created": 5,
  "edges_updated": 0,
  "errors": []
}
```

---

**Total Graph after Fix:**
- Nodes: 599 (594 + 5)
- Edges: 454 (449 + 5)
- Companies: 349
