from neo4j import GraphDatabase
import json

uri = "bolt://localhost:7687"
auth = ("neo4j", "arachne123")

with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
        result = session.run("""
            MATCH (a)-[r:INDUSTRIAL_FLOW {edge_type: 'capability_supply'}]->(b)
            RETURN a.node_id AS src, a.entity_type AS src_type, a.canonical_name_zh AS src_name,
                   b.node_id AS dst, b.entity_type AS dst_type, b.canonical_name_zh AS dst_name,
                   r.edge_id AS edge_id, r.description AS description
            LIMIT 100
        """)
        rows = [dict(r) for r in result]
        print(json.dumps(rows, ensure_ascii=False, indent=2))
