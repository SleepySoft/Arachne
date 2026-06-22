import json
with open('industrial_flow_edges.json','r',encoding='utf-8') as f:
    edges=json.load(f)
for e in edges:
    if 'silicon' in e['__from'] or 'silicon' in e['__to'] or 'wafer' in e['__from'] or 'wafer' in e['__to'] or 'semiconductor_device' in e['__from'] or 'semiconductor_device' in e['__to']:
        print(e['__from'], '->', e['__to'], e.get('edge_type'), e.get('description'))
print('--- ontology ---')
with open('ontology_edges.json','r',encoding='utf-8') as f:
    edges=json.load(f)
for e in edges:
    if 'silicon' in e['__from'] or 'silicon' in e['__to'] or 'wafer' in e['__from'] or 'wafer' in e['__to'] or 'semiconductor_device' in e['__from'] or 'semiconductor_device' in e['__to']:
        print(e['__from'], '->', e['__to'], e.get('edge_type'), e.get('description'))
