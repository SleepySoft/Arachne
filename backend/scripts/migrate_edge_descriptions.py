#!/usr/bin/env python3
"""
将 Neo4j 中 INDUSTRIAL_FLOW 边的 edge_type_label 和 description 里的旧中文标签
替换为 EDGE_TYPE_LABELS 中的新描述。

替换策略：
- edge_type_label：按 edge_type 直接覆盖为新标签。
- description：只在旧标签不被其他中文字符紧邻时替换（避免破坏“服务流程”“信息流向”等自然词语）。
"""
import re
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "arachne123")

# edge_type -> 新中文标签
EDGE_TYPE_LABELS = {
    "material_input": "物料输入",
    "energy_input": "能量输入",
    "information_input": "信息输入",
    "equipment_enablement": "设备使能",
    "process_output": "工艺产出",
    "service_provision": "服务提供",
    "capability_enablement": "能力使能",
    "structural_composition": "结构组成",
    "supply_relation": "供应关系",
    "unknown": "未知关系",
}

# 旧中文标签 -> 对应的新中文标签（按 edge_type 在运行时决定 capability 分支）
OLD_TO_NEW_LABELS = {
    "material_input": {"物料流": "物料输入"},
    "energy_input": {"能量流": "能量输入"},
    "information_input": {"信息流": "信息输入"},
    "equipment_enablement": {"能力供给": "设备使能"},
    "process_output": {"产出": "工艺产出"},
    "service_provision": {"服务流": "服务提供"},
    "capability_enablement": {"能力供给": "能力使能"},
    "structural_composition": {"组成/构成": "结构组成"},
}


def make_pattern(old: str) -> re.Pattern:
    # 旧标签不被其他中文字符紧邻时才匹配
    return re.compile(rf"(?<![\u4e00-\u9fa5]){re.escape(old)}(?![\u4e00-\u9fa5])")


def update_description(desc: str, mapping: dict[str, str]) -> tuple[str, int]:
    total = 0
    for old, new in mapping.items():
        pattern = make_pattern(old)
        desc, count = pattern.subn(new, desc)
        total += count
    return desc, total


def main():
    with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
        with driver.session() as session:
            # 1. 更新 edge_type_label
            updated_label_count = 0
            for edge_type, new_label in EDGE_TYPE_LABELS.items():
                result = session.run(
                    """
                    MATCH ()-[r:INDUSTRIAL_FLOW]->()
                    WHERE r.edge_type = $edge_type
                    SET r.edge_type_label = $new_label
                    RETURN count(r) AS updated
                    """,
                    edge_type=edge_type,
                    new_label=new_label,
                )
                updated_label_count += result.single()["updated"]
            print(f"Updated edge_type_label on {updated_label_count} edges")

            # 2. 安全替换 description 中的旧标签
            desc_updated = 0
            desc_replacements = 0
            for edge_type, mapping in OLD_TO_NEW_LABELS.items():
                result = session.run(
                    """
                    MATCH ()-[r:INDUSTRIAL_FLOW]->()
                    WHERE r.edge_type = $edge_type
                    RETURN r.edge_id AS edge_id, r.description AS description
                    """,
                    edge_type=edge_type,
                )
                for record in result:
                    old_desc = record["description"] or ""
                    new_desc, count = update_description(old_desc, mapping)
                    if count > 0:
                        session.run(
                            """
                            MATCH ()-[r:INDUSTRIAL_FLOW {edge_id: $edge_id}]->()
                            SET r.description = $new_desc
                            """,
                            edge_id=record["edge_id"],
                            new_desc=new_desc,
                        )
                        desc_updated += 1
                        desc_replacements += count
            print(f"Updated description on {desc_updated} edges, total replacements: {desc_replacements}")

            # 3. 验证残留的 edge_type_label
            result = session.run("""
                MATCH ()-[r:INDUSTRIAL_FLOW]->()
                WHERE r.edge_type_label IN ['物料流', '能量流', '信息流', '能力供给', '服务流', '产出', '组成/构成']
                RETURN count(r) AS remaining
            """)
            print(f"Remaining old edge_type_label: {result.single()['remaining']}")

            # 4. 输出新 edge_type_label 分布
            result = session.run("""
                MATCH ()-[r:INDUSTRIAL_FLOW]->()
                WHERE r.edge_type_label IS NOT NULL
                RETURN r.edge_type_label AS label, count(r) AS cnt
                ORDER BY cnt DESC
            """)
            print("New edge_type_label distribution:")
            for record in result:
                print(f"  {record['label']:20s} {record['cnt']}")


if __name__ == "__main__":
    main()
