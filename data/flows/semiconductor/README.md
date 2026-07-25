# Semiconductor arachne-flow files

Generated from the current Neo4j industrial graph for arachne-flow engine debugging.

## Layout

- One YAML file per target product root (application systems, storage, data products).
- Each file is a **standalone** arachne-flow/v0.1 document.
- `manifest.yaml` lists all generated files and their sizes.

## Generation rules

The generator in `temp/generate_arachne_flow.py` follows `docs/design_v4.txt`:

1. Start from the product node (e.g. `smartphone`).
2. Walk upstream along `:INDUSTRIAL_FLOW` edges (`material_input`, `process_output`, etc.).
   `derived_from` edges are ignored because they express taxonomy, not material flow.
3. Expand abstract resource inputs via `is_a` ontology edges to concrete produced
   children (e.g. `chip` → `tested_chip`), and emit the abstract parent as an
   additional output of the concrete producer so the flow stays connected.
4. Legacy process/usage nodes become **METHOD** nodes.
5. Each METHOD occurrence in a product flow gets a unique **ACTION** node with a
   `[ACTION, ref, METHOD]` triple.
6. Process inputs/outputs become `[RESOURCE, input_role, ACTION]` /
   `[ACTION, output_role, RESOURCE]` triples.
7. When a process node is used as a resource input (e.g. `chip_design` as
   `information_input`), a synthetic RESOURCE is created for its output so that
   ACTION and RESOURCE remain disjoint classes.
8. Direct resource→resource edges are redirected to the ACTION that produces the
   target resource, or to a synthetic integration ACTION/METHOD pair.
9. `next` edges are added between consecutive ACTIONs that share a resource.
10. `output_role` is set to `intermediate` when the output resource is consumed
    by another ACTION in the flow, otherwise `primary_result`.
11. The legacy wafer-manufacturing graph contains an intentional CMP↔lithography
    loop for multi-layer processing. Since arachne-flow requires a DAG, the
    generator removes the back-edge that closes each cycle.

## Manual additions (2026-07-25, not in generator)

生成器之后的的手工补链，重新运行生成器时注意保留：

1. `ssd.yaml`：新增三个变体集成（`ssd → act_integrate_{nvme,consumer,enterprise}_ssd → *_ssd`），修复 ssd 无下游、三个变体无上游。
2. `server.yaml` / `data_center.yaml` / `personal_computer.yaml`：includes 增加 `ssd.yaml`。
3. `smartphone.yaml`：includes 增加 `dram_chip_manufacturing.yaml`，新增 `dram_chip → act_integrate_lpddr5 → lpddr5`（修复 lpddr5 无上游）。
4. `new_energy_vehicle.yaml`：includes 增加 `power_semiconductor_manufacturing.yaml`，新增 `power_device` 作为电驱/电控投入（修复 power_device 无下游）。
5. `wafer_fabrication_processes.yaml` / `dram_chip_manufacturing.yaml` / `power_semiconductor_manufacturing.yaml`：新增 `foundry` 和 `integrated_device_manufacturer` 作为 `tool` 角色的商业模式主体（晶圆代工/IDM 提供制造服务，同 osat 惯例），foundry 此前在 flow 图中完全缺失。

## Validation

All generated files were checked with `temp/validate_flows.py`:

- Every file is a **single connected graph**.
- Every file is **acyclic**.
- Triples conform to the four allowed patterns from `docs/design_v4.txt`.

## Known limitations

- Process-group subprocesses (`wafer_manufacturing` → lithography/etching/...)
  are *not* expanded, so each file stays compact and readable. A detailed version
  with `part_of` expansion can be generated if needed.
- Some target products (`photovoltaic_inverter`, `ssd`) have very short flows
  because the legacy graph does not yet connect them to a complete production
  chain (they are linked only by `structural_composition` without a producing
  process). They are represented with a synthetic integration ACTION.
- The generated files are intentionally **complete/standalone**; upstream
  subgraphs are duplicated across products. Future iterations can use the
  `include:` mechanism to share common wafer-manufacturing sub-flows.
- Synthetic output resources (e.g. `chip_design_output`) use generic local
  display names because `temp/full_graph.json` does not include canonical names.
