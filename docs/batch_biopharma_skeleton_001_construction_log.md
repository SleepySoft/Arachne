# Batch Biopharma Skeleton 001 构建日志

**构建时间**: 2026-07-02  
**数据批次**: `data/stock_batches/batch_biopharma_skeleton_001.json`  
**映射批次**: `data/stock_batches/batch_biopharma_mappings_001.json`  
**覆盖行业**: 生物医药（biopharma）

---

## 一、研究背景

生物医药/生物技术产业是 Arachne 继半导体之后的下一个重点研究领域。本次批次聚焦**生物制药制造主线**，建立从上游原材料/设备、中游单元工艺到下游产品/服务的骨架节点与关系，为后续公司暴露、竞争分析和投资研究提供产业本体基础。

### 参考来源

- [生物医药产业链图谱全景分析 - ByDrug](https://bydrug.pharmcube.com/news/detail/e51d10e5815159883c005a883203940b)
- [Insight into Development and Smart Transformation of Biopharmaceutical Industry in China](https://p7f.vogel.de/companies/67/92/6792fcfe2dcb0/2025----------------------------------------1-23.pdf)
- [Industrial Production of Therapeutic Proteins: Cell Lines, Cell Culture, and Purification](https://pmc.ncbi.nlm.nih.gov/articles/PMC7121293/)
- [Vertical Integration of Disposables in Biopharmaceutical Drug Substance Manufacturing](https://www.bioprocessintl.com/monoclonal-antibodies/vertical-integration-of-disposables-in-biopharmaceutical-drug-substance-manufacturing)
- [Smart process analytics for the end-to-end batch manufacturing of monoclonal antibodies](https://web.mit.edu/braatzgroup/Hong_ComputChemEng_2023.pdf)
- [Biopharmaceutical drug delivery and phototherapy using protein crystals](https://www.sciencedirect.com/science/article/abs/pii/S0169409X24003028)
- [Recent Developments in Bioprocessing of Recombinant Proteins](https://www.frontiersin.org/journals/bioengineering-and-biotechnology/articles/10.3389/fbioe.2019.00420/full)
- [An Investor's Guide to the Biopharmaceutical Value Chain](https://www.drugpatentwatch.com/blog/an-investors-guide-to-the-biopharmaceutical-value-chain-a-comparative-analysis-of-risks-and-opportunities-in-generic-and-biosimilar-markets/)

---

## 二、基础设施调整

### 2.1 CLI 后端端口修正

**问题**: `cli/arachne_cli.py` 的 `BASE_URL` 仍指向 `http://localhost:8005/api/v1`，而当前后端实际运行在 `16060`。  
**修复**: 将 `BASE_URL` 更新为 `http://localhost:16060/api/v1`。

---

## 三、产业图构建（Neo4j）

### 3.1 新增节点（32个）

**制造流程（9个）**:
- `biopharmaceutical_manufacturing` (process) — 生物制药制造（聚合流程）
- `cell_culture_process` (process) — 细胞培养工艺
- `fermentation_process` (process) — 发酵工艺
- `harvest_clarification_process` (process) — 收获澄清工艺
- `chromatography_purification_process` (process) — 层析纯化工艺
- `virus_inactivation_process` (process) — 病毒灭活工艺
- `ultrafiltration_diafiltration_process` (process) — 超滤透析工艺
- `formulation_process` (process) — 制剂工艺
- `fill_finish_process` (process) — 灌装冻干工艺

**上游原材料与耗材（7个）**:
- `cell_culture_medium` (material) — 细胞培养基
- `culture_serum` (material) — 培养血清
- `excipient` (material) — 药用辅料
- `chromatography_resin` (material) — 层析填料
- `filter_membrane` (material) — 过滤膜
- `single_use_bag` (material) — 一次性生物反应袋
- `water_for_injection` (material) — 注射用水

**上游设备（6个）**:
- `bioreactor` (device) — 生物反应器
- `chromatography_system` (device) — 层析系统
- `filtration_system` (device) — 过滤系统
- `filling_machine` (device) — 灌装机
- `freeze_dryer` (device) — 冻干机
- `cell_analyzer` (device) — 细胞分析仪

**下游产品（5个）**:
- `monoclonal_antibody` (material) — 单克隆抗体
- `recombinant_protein` (material) — 重组蛋白
- `cell_therapy_product` (material) — 细胞治疗产品
- `gene_therapy_product` (material) — 基因治疗产品
- `biosimilar` (material) — 生物类似药

**研发与外包服务（5个）**:
- `contract_research_organization` (service) — CRO
- `contract_manufacturing_organization` (service) — CMO/CDMO
- `contract_sales_organization` (service) — CSO
- `clinical_trial_service` (service) — 临床试验服务
- `drug_discovery_service` (service) — 药物发现服务

### 3.2 复用已有节点

- `vaccine`, `blood_product`, `biological_drug`, `pharmaceutical_product`
- `chemical_drug`, `traditional_chinese_medicine`
- `pharmaceutical_intermediate`, `pharmaceutical_raw_material`
- `pharmaceutical_distribution`, `pharmaceutical_retail`
- `medical_device`, `medical_service`

### 3.3 新增边（56条）

**本体关系（18条）**:
- 8条 `part_of`: 各单元工艺 → `biopharmaceutical_manufacturing`
- 7条 `is_a`: 单抗/疫苗/重组蛋白/血制品/细胞治疗/基因治疗/生物类似药 → `biological_drug`
- 3条 `is_a`: 生物药/化学药/中成药 → `pharmaceutical_product`

**产业流关系（38条）**:
- 物料输入: 培养基、血清、中间体、原料药、辅料、注射用水、层析填料、过滤膜、一次性袋 → 各工艺
- 设备使能: 生物反应器、层析系统、过滤系统、灌装机、冻干机、细胞分析仪 → 各工艺
- 工艺产出: 细胞培养/发酵 → 收获澄清 → 层析纯化 → 病毒灭活 → 超滤透析 → 制剂 → 灌装冻干 → 各产品
- 服务提供: CRO → 药物发现 → 临床试验 → 生物制药制造；CMO/CDMO → 生物制药制造；CSO → 医药分销
- 聚合产出: `biopharmaceutical_manufacturing` → `pharmaceutical_distribution`

---

## 四、行业视图配置（PostgreSQL）

为 `biopharma` 行业新增 **38** 条 `IndustryNodeMapping`，覆盖本次新增的全部节点以及部分已有节点：

| 角色 | 节点数 | 示例 |
|---|---|---|
| 核心制造流程 | 1 | biopharmaceutical_manufacturing |
| 上游单元工艺 | 2 | cell_culture_process, fermentation_process |
| 下游单元工艺 | 6 | harvest_clarification_process, chromatography_purification_process 等 |
| 上游原材料 | 7 | cell_culture_medium, pharmaceutical_raw_material 等 |
| 上游耗材 | 4 | chromatography_resin, filter_membrane 等 |
| 上游设备 | 6 | bioreactor, chromatography_system 等 |
| 核心产品 | 7 | monoclonal_antibody, vaccine, blood_product 等 |
| 研发/生产/销售服务 | 5 | CRO, CMO/CDMO, CSO, clinical_trial_service, drug_discovery_service |
| 下游流通服务 | 3 | pharmaceutical_distribution, pharmaceutical_retail, medical_service |

---

## 五、验证结果

### 5.1 提交结果

```
Graph batch: 32 nodes_created, 56 edges_created, 0 errors
Business batch: 38 mappings_created, 0 errors
```

### 5.2 图谱统计

- 提交前: 875 节点 / 688 边
- 提交后: 907 节点 / 744 边
- `biopharma` 行业子图: 42 节点 / 60 边

### 5.3 质量检查

运行 `POST /api/v1/admin/db-checks/run-all`:
- 无新增重复边、自环边
- 无新增 `input_to_product_direct_edge` 违规
- 新增节点均非孤立节点
- 预先存在的 `orphan_nodes`、`dangling_industry_mappings`、`dangling_company_exposures` 等问题与本次批次无关

---

## 六、后续工作

1. **细化上游**: 补充培养基组分（氨基酸、维生素、葡萄糖）、细胞系/菌种库、质粒/病毒载体等更细粒度节点。
2. **化学药与中药**: 建立 `chemical_drug_synthesis_process`（化学合成工艺）、`traditional_chinese_medicine_processing`（中药炮制工艺）等流程节点。
3. **医疗器械**: 独立于生物药的医疗器械产业链仍需扩展（影像设备、高值耗材、IVD 等）。
4. **公司暴露**: 将药明康德、凯莱英、泰格医药、恒瑞医药、百济神州等代表性公司映射到本骨架节点。
5. **WebBridge 深度研究**: 待浏览器扩展连接后，可利用网页自动化抓取最新行业报告、政策文件和企业供应链信息。
