#!/usr/bin/env python3
"""
迁移 Neo4j 中 INDUSTRIAL_FLOW 边的 edge_type 到新的 IndustrialFlowType 枚举。

映射规则：
- material_flow      -> material_input
- energy_flow        -> energy_input
- information_flow   -> information_input
- composition        -> structural_composition
- produces           -> process_output
- service_flow       -> service_provision
- capability_supply  -> equipment_enablement   (当起点 entity_type 为 device 时)
- capability_supply  -> capability_enablement  (其他情况)

注意：本脚本不修改边的 description 文本，只修改 edge_type。
"""
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "arachne123")

DIRECT_MAPPINGS = {
    "material_flow": "material_input",
    "energy_flow": "energy_input",
    "information_flow": "information_input",
    "composition": "structural_composition",
    "produces": "process_output",
    "service_flow": "service_provision",
}


def main():
    with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
        with driver.session() as session:
            # 1. 直接映射的旧类型
            for old_type, new_type in DIRECT_MAPPINGS.items():
                result = session.run(
                    """
                    MATCH ()-[r:INDUSTRIAL_FLOW {edge_type: $old_type}]->()
                    SET r.edge_type = $new_type
                    RETURN count(r) AS updated
                    """,
                    old_type=old_type,
                    new_type=new_type,
                )
                record = result.single()
                print(f"{old_type:20s} -> {new_type:25s}: {record['updated']} edges")

            # 2. capability_supply 按起点 entity_type 拆分
            result = session.run(
                """
                MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW {edge_type: 'capability_supply'}]->(b:IndustrialNode)
                WHERE a.entity_type = 'device'
                SET r.edge_type = 'equipment_enablement'
                RETURN count(r) AS updated
                """
            )
            record = result.single()
            print(f"{'capability_supply':20s} -> {'equipment_enablement':25s}: {record['updated']} edges")

            result = session.run(
                """
                MATCH (a:IndustrialNode)-[r:INDUSTRIAL_FLOW {edge_type: 'capability_supply'}]->(b:IndustrialNode)
                WHERE a.entity_type <> 'device'
                SET r.edge_type = 'capability_enablement'
                RETURN count(r) AS updated
                """
            )
            record = result.single()
            print(f"{'capability_supply':20s} -> {'capability_enablement':25s}: {record['updated']} edges")

            # 3. 验证是否还有旧类型残留
            result = session.run(
                """
                MATCH ()-[r:INDUSTRIAL_FLOW]->()
                WHERE r.edge_type IN ['material_flow', 'energy_flow', 'information_flow',
                                      'composition', 'produces', 'service_flow', 'capability_supply']
                RETURN count(r) AS remaining
                """
            )
            record = result.single()
            print(f"Remaining old-type edges: {record['remaining']}")

            # 4. 输出新类型分布
            result = session.run(
                """
                MATCH ()-[r:INDUSTRIAL_FLOW]->()
                RETURN r.edge_type AS edge_type, count(r) AS cnt
                ORDER BY cnt DESC
                """
            )
            print("\nNew edge type distribution:")
            for record in result:
                print(f"  {record['edge_type']:30s} {record['cnt']}")


if __name__ == "__main__":
    main()
