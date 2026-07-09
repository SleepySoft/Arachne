# HBM 供应链数据 enrichment 效果评估

评估时间：2026-07-09
评估对象：`hbm`（高带宽存储器）

## 1. 已补充的数据

### 工业节点（上游/下游）
| 方向 | 节点 ID | 中文名 | 类型 |
|---|---|---|---|
| 上游 | `advanced_packaging` | 先进封装 | process |
| 上游 | `memory_die` | 存储芯片裸片 | part |
| 上游 | `tsv` | 硅通孔 | technology_capability |
| 上游 | `silicon_interposer` | 硅中介层 | part |
| 上游 | `microbump` | 微凸块 | part |
| 上游 | `underfill` | 底部填充胶 | material |
| 下游 | `gpu` | 图形处理器 | part |
| 下游 | `ai_accelerator` | AI 加速器 | part |
| 下游 | `server` | 服务器 | system |
| 下游 | `data_center` | 数据中心 | infrastructure |

### 关键工业流边
- 上游：
  - 子工艺：`memory_die -> die_stacking`, `memory_wafer -> tsv_interconnection`, `tsv -> tsv_interconnection`, `silicon_interposer -> silicon_interposer_integration`, `packaging_substrate -> silicon_interposer_integration`, `microbump -> bumping_process`, `underfill -> underfill_process`
  - 子工艺 → 工艺组：`die_stacking -> advanced_packaging`, `tsv_interconnection -> advanced_packaging`, `silicon_interposer_integration -> advanced_packaging`, `bumping_process -> advanced_packaging`, `underfill_process -> advanced_packaging`
  - 工艺组 → 产品：`advanced_packaging -> hbm`
  - 晶圆 → 裸片：`memory_wafer -> memory_die`
- 下游：`hbm -> gpu`, `hbm -> ai_accelerator`, `gpu -> server`, `ai_accelerator -> server`, `server -> data_center`

### 工艺组层次
- `advanced_packaging`（先进封装）已拆分为 process group，包含 5 个 `part_of` 子工艺：
  - `tsv_interconnection`（TSV 互连）
  - `die_stacking`（芯片堆叠）
  - `silicon_interposer_integration`（硅中介层集成）
  - `bumping_process`（凸块制作）
  - `underfill_process`（底部填充）
- 同时补充了 `advanced_packaging is_a chip_packaging_and_testing` 的本体关系。

### 公司暴露（CompanyNodeExposure）
- HBM 原厂：`sk_hynix`, `samsung_electronics`, `micron`
- 先进封装/OSAT：`tongfu_microelectronics`, `jcet`, `shenzhen_kaifa`
- 材料：`xingsen_technology`（硅中介层）, `shennan_circuits`（封装基板）, `jacques_technology`（底部填充胶）, `lianruixin_material`（球形硅微粉）, `huahai_chengke`（环氧塑封料）
- 模组/下游：`biwin_storage`, `longsys`

## 2. 推理效果对比

### `association`（工业图内关联）
- 修复前：`hbm` 孤立或只能依赖 `expand_ontology` 展开到 `memory_chip`。
- 修复后：`association --source hbm --direction both` 返回完整上游/下游链，包括先进封装、材料、GPU/AI 加速器、服务器、数据中心。

### `cross_graph_context`（跨图：工业节点 → 公司）
| 模式 | 公司数 | 暴露数 | 说明 |
|---|---|---|---|
| 默认 | 3 | 3 | 仅直接暴露到 `hbm` 的原厂 |
| `--expand-ontology` | 13 | 16 | 通过 `hbm is_a memory_chip` 展开，覆盖存储芯片生态 |
| `--neighbor-depth 1` | 13 | 14 | 覆盖 `hbm` 的 1 跳工业流邻居（OSAT、GPU/AI 加速器厂商） |
| `--neighbor-depth 2` | 39 | 40 | 覆盖 2 跳邻居，包含硅片、封装基板、底部填充胶、硅中介层等上游材料商 |

## 3. 关键修复

- **节点激活证据**：`neo4j_storage._node_from_record` 对无证据的 `ACTIVE`/`HIGH` 节点会降级为 `PENDING`/`MEDIUM`。 enrichment 脚本现在在激活下游节点时同时写入证据。
- **公司名去重**：`雅克科技` 已存在为 `jacques_technology`，脚本通过 `get_company_by_name_zh` 自动映射，避免重复创建。
- **跨图推理扩展**：`cross_graph_context` 现在支持 `expand_ontology` 和 `industrial_neighbor_depth`，可分别或组合使用。

## 4. 后续可改进

- 为 `hbm` 补充更多上游材料/设备公司（如光刻胶、CMP 材料、量测设备厂商）可进一步丰富 2 跳以上结果。
- 可将 `cross_graph_context` 的 `expand_ontology` 与 `industrial_neighbor_depth` 组合使用，以同时覆盖同义/上下位节点和供应链邻居。
