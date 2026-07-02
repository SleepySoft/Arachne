# Batch 113 产业图构建日志

## 批次信息
- **批次号**: 113
- **股票代码范围**: 002005.SZ - 002015.SZ
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要
- 新建产业节点：17个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：26条

## 新增节点详情

| node_id | canonical_name_zh | entity_type | 代表公司 |
|---------|-------------------|-------------|---------|
| `building_material_machinery` | 建材机械 | device | 精工科技 |
| `carbon_fiber_equipment` | 碳纤维设备 | device | 精工科技 |
| `human_serum_albumin` | 人血白蛋白 | material | 华兰生物 |
| `intravenous_immunoglobulin` | 静注人免疫球蛋白 | material | 华兰生物 |
| `laser_marking_machine` | 激光打标机 | device | 大族激光 |
| `laser_welding_machine` | 激光焊接机 | device | 大族激光 |
| `cnc_machine` | 数控机床 | device | 大族激光 |
| `automated_conveying_system` | 自动化输送系统 | system | 天奇股份 |
| `warehousing_system` | 仓储系统 | system | 天奇股份 |
| `intelligent_logistics` | 智能物流 | service | 传化智联 |
| `central_air_conditioner` | 中央空调 | system | 盾安环境 |
| `electrolytic_capacitor_paper` | 电解电容器纸 | material | 凯恩股份 |
| `filter_paper` | 滤纸 | material | 凯恩股份 |
| `color_printing_packaging` | 彩印包装 | material | 永新股份 |
| `aluminized_packaging` | 镀铝包装 | material | 永新股份 |
| `clean_energy` | 清洁能源 | service | 协鑫能科 |
| `integrated_energy_service` | 综合能源服务 | service | 协鑫能科 |

## 关键发现

1. **大族激光** (002008) 是中国激光设备龙头企业，员工超过1.6万人，新建 `laser_marking_machine`、`laser_welding_machine` 和 `cnc_machine` 三个节点。
2. **华兰生物** (002007) 是中国最大的血液制品企业之一，新建 `human_serum_albumin` 和 `intravenous_immunoglobulin` 节点对生物医药产业链具有重要意义。
3. **凯恩股份** (002012) 是全球电解电容器纸的主要供应商，与batch_110中新疆众和的 `electronic_aluminum_foil`、`formed_foil`、`etched_foil` 节点共同构成了铝电解电容器的完整上游材料链。
4. **传化智联** (002010) 是中国领先的智能物流平台，`intelligent_logistics` 节点的加入丰富了现代物流产业图谱。
5. **协鑫能科** (002015) 是协鑫集团旗下的清洁能源和综合能源服务平台，新建 `clean_energy` 和 `integrated_energy_service` 节点。
