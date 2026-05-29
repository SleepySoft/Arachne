# Batch 111 产业图构建日志

## 批次信息
- **批次号**: 111
- **股票代码范围**: 600900.SH, 600960.SH, 600963.SH, 600966.SH, 600967.SH, 600969.SH, 600975.SH, 600976.SH, 600980.SH, 600985.SH
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要
- 新建产业节点：17个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：31条

## 新增节点详情

| node_id | canonical_name_zh | entity_type | 代表公司 |
|---------|-------------------|-------------|---------|
| `piston` | 活塞 | component | 渤海汽车 |
| `wheel_hub` | 轮毂 | component | 渤海汽车 |
| `automotive_air_conditioner` | 汽车空调 | component | 渤海汽车 |
| `shock_absorber` | 减震器 | component | 渤海汽车 |
| `coated_paper` | 涂布纸 | material | 岳阳林纸 |
| `white_cardboard` | 白卡纸 | material | 博汇纸业 |
| `writing_paper` | 书写纸 | material | 博汇纸业 |
| `offset_paper` | 胶印纸 | material | 博汇纸业 |
| `armored_vehicle` | 装甲车辆 | system | 内蒙一机 |
| `railway_vehicle` | 铁路车辆 | system | 内蒙一机 |
| `metallurgical_machinery` | 冶金机械 | device | 内蒙一机 |
| `industrial_gas` | 工业气体 | material | 郴电国际 |
| `waste_heat_power_generation` | 余热发电 | service | 郴电国际 |
| `breeding_pig` | 种猪 | material | 新五丰 |
| `pork_product` | 猪肉制品 | material | 新五丰 |
| `ferrite` | 铁氧体 | material | 北矿科技 |
| `magnetic_device` | 磁性器件 | component | 北矿科技 |

## 关键发现

1. **长江电力** (600900) 是全球最大的水电上市公司，映射到 `hydro_power_generation` 和 `electricity_power`。
2. **内蒙一机** (600967) 是中国坦克装甲车辆的主要生产基地，新建 `armored_vehicle` 节点对军工产业链具有重要意义。
3. **新五丰** (600975) 是湖南省最大的生猪养殖企业，新建 `breeding_pig` 和 `pork_product` 节点完善了生猪产业链。
4. **北矿科技** (600980) 的铁氧体和磁性器件业务新建了 `ferrite` 和 `magnetic_device` 节点，填补了磁性材料领域的空白。
5. **淮北矿业** (600985) 是华东地区大型煤炭企业，员工近4万人，覆盖煤炭、焦炭和煤化工全产业链。
