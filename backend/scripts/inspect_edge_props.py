from neo4j import GraphDatabase
import json

uri = "bolt://localhost:7687"
auth = ("neo4j", "arachne123")

with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r:INDUSTRIAL_FLOW]->()
            RETURN DISTINCT keys(r) AS props LIMIT 10
        """)
        rows = [dict(r) for r in result]
print(json.dumps(rows, ensure_ascii=False, indent=2))
