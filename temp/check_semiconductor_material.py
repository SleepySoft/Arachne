import json
with open('industrial_nodes.json','r',encoding='utf-8') as f:
    nodes=json.load(f)
found=False
for n in nodes:
    if n['node_id']=='semiconductor_material':
        print(n)
        found=True
        break
if not found:
    print('not found')
