# Biopharma arachne-flow files

生物医药产业链流程文件（2026-07-27 手工建模，非生成器产物）。
数据来源：legacy 产业图骨架批次（`docs/batch_biopharma_skeleton_001_construction_log.md`，
32 节点 / 56 边）+ 公开工艺资料补充（CHO 表达、Protein A 亲和层析、低温乙醇分离、
AAV 载体制备、CAR-T 转导、化学合成、中药炮制提取等）。

## Layout

- **共享上游链**（被产品文件 include）：
  - `biologics_manufacturing.yaml` — 生物药公共链：细胞培养/发酵 → 收获澄清 → 层析纯化
    → 病毒灭活 → 超滤透析 → 制剂 → 灌装冻干 → `biological_drug`
  - `viral_vector_manufacturing.yaml` — 病毒载体公共链：质粒 + HEK293 → 载体生产 → 层析纯化 → `viral_vector`
- **独立制造链**：
  - `chemical_drug_manufacturing.yaml` — 化学药：基础化工原料 → 中间体 → API → 制剂（附抗生素、麻醉药品）
  - `traditional_chinese_medicine_manufacturing.yaml` — 中药：中药材 → 炮制 → 提取 → 制剂（附中成药制剂）
  - `blood_product.yaml` — 血液制品：原料血浆 → 低温乙醇分离 → 层析精制 → 制剂 → 灌装
- **产品链**（basis 衍生自公共链，只写特征投入）：
  - `monoclonal_antibody.yaml` — 单抗（CHO 细胞、Protein A 填料）+ 生物类似药变体
  - `recombinant_protein.yaml` — 重组蛋白（微生物表达宿主）
  - `vaccine.yaml` — 疫苗（毒种、佐剂）
  - `cell_therapy.yaml` — 细胞治疗/CAR-T（患者 T 细胞、病毒载体转导）
  - `gene_therapy.yaml` — 基因治疗/AAV（病毒载体 → 制剂灌装）

## 建模决策（新增内容时遵守）

- **RESOURCE/METHOD 复用 legacy 节点 id**：但此前 `local:` 仅用于显示名——自 2026-07-27 起，
  flow 引用的 RESOURCE/METHOD 已全部登记进 PG/legacy（见下「flow 节点补全」条目），
  新资源（如 `cho_cell_line`、`plasmid_dna`、`human_plasma`）不再是 local-only。
- **METHOD 复用 legacy process 节点 id**（`cell_culture_process`、`formulation_process` 等，
  PG 有中文名）；新 METHOD（`chemical_drug_synthesis_process`、`traditional_chinese_medicine_processing`
  源自骨架日志待建清单；`tcm_extraction_process`、`cold_ethanol_fractionation_process`、
  `viral_vector_production_process`、`gene_transduction_process`）已于 2026-07-27 通过
  `batch_flow_node_completion_001.json` 正式登记进 legacy 图（含证据、industrial_flow 边），
  PG/Neo4j 均有完整 metadata。
- **RESOURCE 已全部登记进 legacy 图**：本目录 flow 文件引用的所有 RESOURCE（含此前 local-only 的
  `cho_cell_line`、`plasmid_dna`、`viral_vector`、工艺中间体等 25 个）已于 2026-07-27 通过
  `batch_flow_node_completion_001.json` 登记（关键实体 HIGH+ACTIVE 带权威证据，工艺中间体
  MEDIUM+PENDING）。`local:` 中文名保留作为冗余显示名，与 PG canonical_name_zh 一致。
- **产品变体用 basis**：单抗/疫苗/重组蛋白衍自 `biological_drug`，生物类似药衍自
  `monoclonal_antibody`，麻醉药品衍自 `chemical_drug`，中成药制剂衍自
  `traditional_chinese_medicine`（同 ssd/lpddr5 惯例，不用 component）。
- **抗生素与其它化学药一致经制剂**：`act_produce_antibiotic` 以 `active_pharmaceutical_ingredient`
  为 feedstock（保留与 legacy 边一致）+ `excipient`，并 `ref formulation_process`；
  不再允许绕过制剂步骤的单独产物分支。
- **聚合流程 METHOD 不作 method_ref**：`biopharmaceutical_manufacturing` 这类 umbrella 流程
  被多个产品 action ref 时，merged 视图（按 method_ref 合并跨 flow action）会把它塌缩成枢纽：
  上游变成各产品特征投入的并集，下游出现「既产出又投入」的自环（单抗既被产出又作 biosimilar
  的 basis 投入）。产品 stub 与 `act_produce_anesthetic` / `act_produce_chinese_patent_medicine`
  惯例一致，不写 ref。
- **CDMO 用 tool 角色**挂在细胞培养与 API 合成 ACTION 上（同 foundry/osat 惯例）。
- **病毒载体在细胞治疗中是 carrier**（基因递送载体），在基因治疗中是 feedstock（主成分）。

## 刻意未建模 / legacy 数据疑点

- `blood_product → vaccine`（legacy material_input）语义可疑，flow 中未采纳。
- `pharmaceutical_raw_material`（医药原料药）与 `active_pharmaceutical_ingredient`（原料药）
  在 legacy 中并存且语义重叠；flow 化学药链只用后者，前者待人工归一。
- CXO 研发/临床/销售服务（CRO/CSO/clinical_trial）非物料链，不建 flow 文件；
  仅 CDMO 作为 tool 出现。
- 医疗器械（medical_device）不属于生物医药制造链，未建模。

## Validation

- 10 个文件全部通过 `scripts/preview_flows.py --category biopharma`（0 errors / 0 warnings），
  并已编译入 Neo4j flow 图（`scripts/compile_flows.py --category biopharma`）。
- `--dangling` 检查：无断链中间品；无上游项均为合理源头（原料/细胞株/设备/CDMO），
  无下游项均为终端药品。
- 推理冒烟（`scripts/smoke_flow_reasoning.py`）：monoclonal_antibody / vaccine /
  chemical_drug / viral_vector 关联推理均 success；wuxi_biologics 公司上下文
  peers 5 / upstream 10 / downstream 21 / related 15。
