import requests
API = 'http://localhost:8000/api/v1'

# 1. 所有节点
r = requests.get(f'{API}/nodes?page=1&page_size=200')
nodes = r.json()['items']
with open('tmp_script/all_nodes.txt', 'w', encoding='utf-8') as f:
    for n in sorted(nodes, key=lambda x: x['node_id']):
        f.write(f"{n['node_id']}: {n['canonical_name_zh']} ({n['entity_type']})\n")

# 2. 所有边
r = requests.get(f'{API}/edges?page=1&page_size=500')
edges = r.json()['items']
with open('tmp_script/all_edges.txt', 'w', encoding='utf-8') as f:
    for e in sorted(edges, key=lambda x: x['edge_id']):
        f.write(f"{e['edge_id']}: {e['from_node']} --[{e['edge_type']}]--> {e['to_node']}\n")

# 3. 已有公司
r = requests.get(f'{API}/companies?page=1&page_size=100')
companies = r.json()['items']
with open('tmp_script/all_companies.txt', 'w', encoding='utf-8') as f:
    for c in companies:
        f.write(f"{c['company_id']}: {c['name_zh']} ({c['stock_codes']})\n")

print(f"Nodes: {len(nodes)}, Edges: {len(edges)}, Companies: {len(companies)}")
