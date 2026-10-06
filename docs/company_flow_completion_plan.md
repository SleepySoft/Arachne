# 公司产业暴露与 arachne_flow 补全计划

## 目标与边界

目标是让指定证券池中的每一家经营主体同时具备可核验的公司记录、公司产业暴露、共享产业实体和原生 arachne_flow 流程覆盖。基金、ETF 等非公司标的不伪装成公司，后续由独立的基金或主题模型承载。

公司是事实主体，通过 `company_node_exposures` 连接产业实体；公司名称和股票代码不进入产业节点。Flow 按可复用产业过程建设，不按公司建设。

## 完成标准

一家公司只有同时满足以下条件才标记为完成：

1. 证券代码精确解析到唯一公司；名称或别名仅作为精确兜底。
2. 暴露覆盖年报披露的全部主要业务；存在分部收入时，覆盖至少 90% 的主营收入。
3. 每条暴露包含 `activity_type`、`weight`、`as_of_date` 和公司级证据。
4. 每个暴露 `node_id` 指向已经归一的共享产业实体。
5. 暴露实体在 legacy 图中具有合理的产业关系。
6. 暴露实体作为 RESOURCE、METHOD 或 ACTION 的 `method_ref` 原生进入 arachne_flow。
7. Flow 中间产物不存在意外断链，PG 元数据无缺失。
8. 公司上下文推理和全图高亮冒烟通过。

暴露条数不是完成标准。业务集中的公司可以只有一条暴露，但必须有证据说明它覆盖了公司的主要业务。

## 证据规则

公司暴露优先使用年度报告、招股书、交易所公告和公司官方产品资料。产业流程优先使用国家或行业标准、监管文件、厂商技术手册和权威技术资料。新闻和市场概念只用于发现候选，不直接形成 `ACTIVE/HIGH` 数据。

公司证据回答“公司经营什么”，流程证据回答“产业实体如何参与输入、动作和产出”。两类证据分别维护。

## 执行批次

1. 电力设备、输配电、发电与储能。
2. 食品、饮料和消费家电。
3. 电子元件、光学和特种材料。
4. 航空、交通和工业装备。
5. 医疗、金融、教育、房地产等服务流程。
6. 对只有一条暴露的公司进行主营业务完整性复核。

每批依次执行：来源整理、候选抽取、实体归一、GraphRegistrationBatch、Flow YAML、BusinessRegistrationBatch、preview、compile、断链检查、PG 缺口检查、公司推理冒烟、全量覆盖审计、数据库导出。

## 自动质量门槛

使用 `scripts/audit_company_flow_coverage.py` 生成覆盖矩阵。最终目标：

- 公司标的解析率 100%。
- 零暴露公司 0。
- 无效暴露节点 0。
- arachne_flow 全覆盖公司 100%。
- 部分覆盖和零覆盖公司均为 0。
- Flow 引用缺失 PG 元数据 0。
- 非终端中间产物意外断链 0。

黄色暴露覆盖层只用于兼容显示，不计入原生 Flow 完成率。

## 提交边界

代码和审计工具提交到 Arachne；节点、边、Flow 文件及数据库导出提交到 ArachneData；Arachne 单独更新 ArachneData 指针；FinanceDashboard 单独更新 Arachne 指针。每个产业批次保持独立提交。

## 2026-10-06 验收结果

FinanceDashboard 当前有 84 个标的，其中 83 个为公司，医疗器械 ETF 作为非公司标的排除。最终审计结果：

- 83/83 公司按证券代码或精确名称解析；
- 83/83 公司至少有一条产业暴露；
- 146 条公司产业暴露全部指向有效的 legacy 产业实体；
- 146/146 暴露均具备 activity type、weight、观察日期、证据和 ACTIVE 状态；
- 83/83 公司暴露实体全部原生进入 arachne_flow，部分覆盖和零覆盖均为 0；
- 对单暴露公司按 2025 年报分部收入复核，补充 18 条主要业务暴露，单暴露公司从 57 家降至 46 家；业务集中的剩余公司保留单暴露；
- 删除两条缺少公司级证据的推断性暴露：风华高科的锂电池电芯、长鑫科技的氢氟酸采购；
- 新增 12 个稳定产业实体和 12 条 legacy 产业关系，并补齐对应 Flow。

验收命令：

```powershell
backend\venv\Scripts\python.exe scripts\preview_flows.py
backend\venv\Scripts\python.exe scripts\audit_company_flow_coverage.py `
  --finance-data-dir C:\D\code\FinanceDashboard\data `
  --fail-on-gaps
backend\venv\Scripts\python.exe scripts\smoke_flow_reasoning.py
```

`extract_flow_pg_gaps.py` 仍会报告历史 Flow 的 36 个 RESOURCE 和 28 个 METHOD 缺少 PG 元数据。这些节点不属于本证券池的公司暴露实体，本轮没有新增此类缺口；它们作为 Arachne 全局元数据治理任务继续保留。
