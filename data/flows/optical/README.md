# Optical communication arachne-flow files

光通信/光模块产业链流程图：光组件（shared）→ 光模块（含技术变体）→ CPO。

## 结构

**共享组件链（被模块流程 include）**
- `optical_subassembly_packaging.yaml` — 激光器芯片/探测器芯片/光隔离器/精密光学元件/陶瓷管壳 → TOSA/ROSA（METHOD: `optical_subassembly_packaging`）

**模块流程**
- `optical_module_integration.yaml` — TOSA + ROSA + DSP电芯片 + FAU → 光模块（METHOD: `optical_module_packaging_testing`）；硅光模块/LPO光模块用 `basis` 衍生

**下一代形态**
- `cpo_integration.yaml` — 光芯片 + FAU → 光引擎（METHOD: `optical_engine_integration`）→ CPO（`ethernet_switch` 以 `requirement` 角色作为需求侧对接）

## 建模说明

- 三个 METHOD（`optical_subassembly_packaging` / `optical_module_packaging_testing` / `optical_engine_integration`）均为真实工艺节点，已通过 `graph_batch_optical_comm_001/002` 登记进 Neo4j+PG，并在 legacy 图建有 `process_output` 对齐边，非 PG-only 合成 METHOD。
- 光芯片细分（EML/PLC/AWG/硅光）在 legacy 图以 ontology `is_a`/`variant_of` 挂在 `optical_chip` 下；flow 中只引用关键 RESOURCE，不重复展开芯片制造链（InP 衬底链待后续补建）。
- 技术变体用 `basis` 角色衍生（与 robotics/semiconductor 惯例一致）。
