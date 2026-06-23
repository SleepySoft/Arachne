#!/usr/bin/env python3
"""
将 Neo4j 中 IndustrialNode 的 entity_type 从旧分类迁移到新分类。

默认映射（保守策略，复杂类型需后续人工复核）：
- material           -> material
- component          -> part
- device             -> device
- module             -> system
- subsystem          -> system
- system             -> system
- platform           -> platform
- infrastructure     -> infrastructure
- application_system -> software
- service            -> service
- technology_capability -> technology_capability
- process            -> process
- unknown / null     -> unknown
"""
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "arachne123")

MIGRATION_MAP = {
    "material": "material",
    "component": "part",
    "device": "device",
    "module": "system",
    "subsystem": "system",
    "system": "system",
    "platform": "platform",
    "infrastructure": "infrastructure",
    "application_system": "software",
    "service": "service",
    "technology_capability": "technology_capability",
    "process": "process",
    "unknown": "unknown",
}


def main():
    with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
        with driver.session() as session:
            # 先统计旧类型分布
            result = session.run(
                """
                MATCH (n:IndustrialNode)
                RETURN n.entity_type AS et, count(n) AS cnt
                ORDER BY cnt DESC
                """
            )
            print("Before migration:")
            before = {rec["et"]: rec["cnt"] for rec in result}
            for et, cnt in sorted(before.items(), key=lambda x: -x[1]):
                print(f"  {et or 'NULL':30s} {cnt}")

            # 迁移已知旧类型
            updated = 0
            for old_type, new_type in MIGRATION_MAP.items():
                result = session.run(
                    """
                    MATCH (n:IndustrialNode {entity_type: $old_type})
                    SET n.entity_type = $new_type
                    RETURN count(n) AS cnt
                    """,
                    old_type=old_type,
                    new_type=new_type,
                )
                cnt = result.single()["cnt"]
                updated += cnt
                print(f"  {old_type:20s} -> {new_type:20s}: {cnt}")

            # 处理 entity_type 为空/null 的节点
            result = session.run(
                """
                MATCH (n:IndustrialNode)
                WHERE n.entity_type IS NULL
                SET n.entity_type = 'unknown'
                RETURN count(n) AS cnt
                """
            )
            null_cnt = result.single()["cnt"]
            if null_cnt:
                print(f"  NULL/undefined       -> unknown             : {null_cnt}")
                updated += null_cnt

            print(f"\nTotal updated: {updated}")

            # 验证新类型分布
            result = session.run(
                """
                MATCH (n:IndustrialNode)
                RETURN n.entity_type AS et, count(n) AS cnt
                ORDER BY cnt DESC
                """
            )
            print("\nAfter migration:")
            for rec in result:
                print(f"  {rec['et'] or 'NULL':30s} {rec['cnt']}")

            # 检查是否还有旧类型残留
            old_types = set(MIGRATION_MAP.keys())
            result = session.run(
                """
                MATCH (n:IndustrialNode)
                WHERE n.entity_type IN $old_types
                RETURN count(n) AS remaining
                """,
                old_types=list(old_types),
            )
            remaining = result.single()["remaining"]
            print(f"\nRemaining old-type nodes: {remaining}")


if __name__ == "__main__":
    main()
