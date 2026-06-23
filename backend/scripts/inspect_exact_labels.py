from neo4j import GraphDatabase
import json

uri = "bolt://localhost:7687"
auth = ("neo4j", "arachne123")

# 旧中文标签 -> 新中文标签（按当前 edge_type 决定 capability 分支）
old_to_new_by_edge_type = {
    "material_input": {"物料流": "物料输入"},
    "energy_input": {"能量流": "能量输入"},
    "information_input": {"信息流": "信息输入"},
    "equipment_enablement": {"能力供给": "设备使能"},
    "capability_enablement": {"能力供给": "能力使能"},
    "service_provision": {"服务流": "服务提供"},
    "process_output": {"产出": "工艺产出"},
    "structural_composition": {"组成/构成": "结构组成"},
}

with GraphDatabase.driver(uri, auth=auth) as driver:
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r:INDUSTRIAL_FLOW]->()
            RETURN r.edge_id AS edge_id, r.edge_type AS edge_type, r.description AS description
        """)
        rows = [dict(r) for r in result]

summary = {}
examples = {}
for r in rows:
    et = r["edge_type"]
    desc = r["description"] or ""
    mapping = old_to_new_by_edge_type.get(et, {})
    for old, new in mapping.items():
        if old in desc:
            summary.setdefault(et, {}).setdefault(old, 0)
            summary[et][old] += 1
            examples.setdefault(et, {})[old] = desc[:80]

# Write to file to avoid console encoding issues
out_path = r"C:\D\Code\git\Arachne\data\backups\exact_label_hits.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"summary": summary, "examples": examples, "total": len(rows)}, f, ensure_ascii=False, indent=2)
print(f"Wrote {out_path}")
