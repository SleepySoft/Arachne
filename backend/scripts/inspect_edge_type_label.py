from neo4j import GraphDatabase
import json

uri = "bolt://localhost:7687"
auth = ("neo4j", "arachne123")

with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r:INDUSTRIAL_FLOW]->()
            WHERE r.edge_type_label IS NOT NULL
            RETURN r.edge_type_label AS label, count(r) AS cnt
            ORDER BY cnt DESC
        """)
        rows = [dict(r) for r in result]
        total = session.run("""
            MATCH ()-[r:INDUSTRIAL_FLOW]->()
            WHERE r.edge_type_label IS NOT NULL
            RETURN count(r) AS total
        """).single()["total"]

out_path = r"C:\D\Code\git\Arachne\data\backups\edge_type_label_dist.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"rows": rows, "total": total}, f, ensure_ascii=False, indent=2)
print(f"Wrote {out_path}, total edges with edge_type_label: {total}")
