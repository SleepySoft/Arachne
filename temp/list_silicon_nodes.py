import json
with open('industrial_nodes.json','r',encoding='utf-8') as f:
    nodes=json.load(f)
for n in nodes:
    if 'silicon' in n['node_id'] or 'chip' in n['node_id'] or 'semiconductor' in n['node_id']:
        print(n['node_id'], n.get('canonical_name_zh'), n.get('entity_type'))
