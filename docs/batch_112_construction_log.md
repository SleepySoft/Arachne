# Batch 112 产业图构建日志

## 批次信息
- **批次号**: 112
- **股票代码范围**: 600986.SH, 600988.SH, 600990.SH, 600992.SH, 600993.SH, 600995.SH, 600997.SH, 002017.SZ, 002003.SZ, 002004.SZ
- **公司数量**: 10家
- **处理时间**: 2026-05-28

## 执行摘要
- 新建产业节点：16个
- 新建产业边：0条
- 新建公司：10家
- 新建暴露关系：27条

## 新增节点详情

| node_id | canonical_name_zh | entity_type | 代表公司 |
|---------|-------------------|-------------|---------|
| `digital_marketing` | 数字营销 | service | 浙文互联 |
| `gold` | 黄金 | material | 赤峰黄金 |
| `bismuth` | 铋 | material | 赤峰黄金 |
| `palladium` | 钯 | material | 赤峰黄金 |
| `rhodium` | 铑 | material | 赤峰黄金 |
| `radar` | 雷达 | device | 四创电子 |
| `rf_component` | 射频组件 | component | 四创电子 |
| `communication_engineering` | 通信工程 | service | 四创电子 |
| `steel_wire_rope` | 钢丝绳 | component | 贵绳股份 |
| `steel_wire` | 钢丝 | component | 贵绳股份 |
| `hemorrhoid_medicine` | 痔疮药 | material | 马应龙 |
| `energy_storage` | 储能 | service | 南网储能 |
| `chip_card` | 芯片卡 | component | 东信和平 |
| `button` | 钮扣 | component | 伟星股份 |
| `zipper` | 拉链 | component | 伟星股份 |
| `garment_accessory` | 服装辅料 | component | 伟星股份 |

## 关键发现

1. **赤峰黄金** (600988) 同时产出黄金、白银、铋、钯、铑五种稀贵金属，本批次新建了除银以外的4个贵金属节点，极大丰富了有色金属产业图谱。
2. **四创电子** (600990) 是中国电科旗下雷达和通信企业，新建 `radar`、`rf_component` 和 `communication_engineering` 三个节点，完善了雷达通信产业链。
3. **南网储能** (600995) 是中国南方电网旗下的储能上市平台，`energy_storage` 节点的加入对新能源产业链具有重要意义。
4. **伟星股份** (002003) 是全球最大的钮扣和拉链生产企业之一，新建 `button`、`zipper` 和 `garment_accessory` 三个节点填补了服装辅料领域的空白。
5. **马应龙** (600993) 是拥有400多年历史的中药老字号，以痔疮药闻名，新建 `hemorrhoid_medicine` 节点。
