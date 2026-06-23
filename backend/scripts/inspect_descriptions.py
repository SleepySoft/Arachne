from neo4j import GraphDatabase
import json

uri = "bolt://localhost:7687"
auth = ("neo4j", "arachne123")

old_labels = ["物料流", "组成", "构成", "能量流", "信息流", "能力供给", "服务流", "产出"]

with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r:INDUSTRIAL_FLOW]->()
            RETURN r.edge_id AS edge_id, r.edge_type AS edge_type, r.description AS description
            LIMIT 200
        """)
        rows = [dict(r) for r in result]

for r in rows:
    desc = r["description"] or ""
    hits = [l for l in old_labels if l in desc]
    if hits:
        print(r["edge_id"], r["edge_type"], "|", hits, "|", desc[:80])
