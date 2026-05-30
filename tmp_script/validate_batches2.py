import json, re
for num in [128, 129]:
    g = json.load(open(f'tmp_script/batch_{num}_nodes.json', encoding='utf-8'))
    b = json.load(open(f'tmp_script/batch_{num}_business.json', encoding='utf-8'))
    snake = re.compile(r'^[a-z][a-z0-9_]*$')
    for n in g['nodes_to_upsert']:
        assert snake.match(n['node_id']) and len(n['node_id']) <= 64, 'invalid node_id: ' + n['node_id']
        for ev in n.get('evidence', []):
            assert ev['source_url'] is None, 'non-null source_url in node ' + n['node_id']
    for e in g['edges_to_upsert']:
        assert snake.match(e['edge_id']) and len(e['edge_id']) <= 64, 'invalid edge_id: ' + e['edge_id']
        for ev in e.get('evidence', []):
            assert ev['source_url'] is None, 'non-null source_url in edge ' + e['edge_id']
    for ex in b['company_node_exposures_to_upsert']:
        assert snake.match(ex['exposure_id']) and len(ex['exposure_id']) <= 64, 'invalid exposure_id: ' + ex['exposure_id']
        for ev in ex.get('evidence', []):
            assert ev['source_url'] is None, 'non-null source_url in exposure ' + ex['exposure_id']
    print(f'Batch {num}: all IDs snake_case, all source_url null -> OK')
