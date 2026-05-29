# Batch 115 产业图构建日志

## 批次信息
- **批次号**: 115
- **股票代码范围**: 002028.SZ - 002037.SZ
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要
- 新建产业节点：23个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：33条

## 新增节点详情

| node_id | canonical_name_zh | entity_type | 代表公司 |
|---------|-------------------|-------------|---------|
| `power_automation_protection` | 电力自动化保护设备 | device | 思源电气 |
| `high_voltage_switch` | 高压开关 | device | 思源电气 |
| `mutual_inductor` | 互感器 | device | 思源电气 |
| `power_capacitor` | 电力电容器 | component | 思源电气 |
| `jacket` | 茄克 | material | 七匹狼 |
| `t_shirt` | T恤 | material | 七匹狼 |
| `trousers` | 裤装 | material | 七匹狼 |
| `cotton_padded_garment` | 棉褛 | material | 七匹狼 |
| `sweater` | 毛衫 | material | 七匹狼 |
| `tire_mold` | 轮胎模具 | device | 巨轮智能 |
| `cookware` | 炊具 | device | 苏泊尔 |
| `passenger_cableway` | 客运索道 | infrastructure | 丽江股份 |
| `performance` | 演出服务 | service | 丽江股份 |
| `waste_incineration_power_generation` | 垃圾焚烧发电 | service | 旺能环境 |
| `waste_treatment` | 垃圾处理 | service | 旺能环境 |
| `gas_stove` | 燃气灶具 | device | 华帝股份 |
| `water_heater` | 热水器 | device | 华帝股份 |
| `range_hood` | 抽油烟机 | device | 华帝股份 |
| `disinfection_cabinet` | 消毒柜 | device | 华帝股份 |
| `camera_module` | 摄像头模组 | component | 联创电子 |
| `touch_display_module` | 触控显示模组 | component | 联创电子 |
| `detonator` | 雷管 | material | 保利联合 |
| `industrial_explosive` | 工业炸药 | material | 保利联合 |

## 关键发现

1. **思源电气** (002028) 是中国电力设备行业的龙头企业，新建 `power_automation_protection`、`high_voltage_switch`、`mutual_inductor` 和 `power_capacitor` 四个节点，极大丰富了输配电设备产业链。
2. **七匹狼** (002029) 是中国男装茄克品类的开创者，新建了 `jacket`、`t_shirt`、`trousers`、`cotton_padded_garment` 和 `sweater` 五个服装品类节点，完善了纺织服装产业图谱。
3. **华帝股份** (002035) 是中国厨电行业的知名品牌，新建 `gas_stove`、`water_heater`、`range_hood` 和 `disinfection_cabinet` 四个节点，与苏泊尔的 `cookware` 和 `kitchen_appliance` 节点共同构建了厨房电器产业图谱。
4. **联创电子** (002036) 是光学镜头和摄像头模组的重要供应商，新建 `camera_module` 和 `touch_display_module` 节点，完善了消费电子上游光学产业链。
5. **保利联合** (002037) 是中国保利集团旗下的民爆器材生产企业，新建 `detonator` 和 `industrial_explosive` 节点，填补了民用爆破器材领域的空白。
6. **旺能环境** (002034) 是中国垃圾焚烧发电行业的领先企业，新建 `waste_incineration_power_generation` 和 `waste_treatment` 节点，完善了环保能源产业链。
