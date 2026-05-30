import json
for num in [128, 129]:
    g = json.load(open(f'tmp_script/batch_{num}_nodes.json', encoding='utf-8'))
    b = json.load(open(f'tmp_script/batch_{num}_business.json', encoding='utf-8'))
    print(f'Batch {num}: nodes={len(g["nodes_to_upsert"])}, edges={len(g["edges_to_upsert"])}, companies={len(b["companies_to_upsert"])}, exposures={len(b["company_node_exposures_to_upsert"])}')
    for n in g['nodes_to_upsert']:
        assert '_' in n['node_id'] or len(n['node_id']) >= 3, f'bad node_id: {n["node_id"]}'
    for e in g['edges_to_upsert']:
        assert e['edge_type'] in ['material_flow','composition','service_flow','energy_flow','information_flow','capability_supply'], f'bad edge_type: {e["edge_type"]}'
    for c in b['companies_to_upsert']:
        assert len(c['company_id']) >= 3, f'bad company_id: {c["company_id"]}'
    print('  Validation: OK')
