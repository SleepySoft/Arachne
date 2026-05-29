import json
for n in range(100, 106):
    with open(f'data/stock_batches/batch_{n}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'=== Batch {n}: {len(data)} companies ===')
    for c in data:
        mb = c.get('main_business', '')
        print(f"  {c['ts_code']} | {c['name']} | {c['industry']} | {mb[:50]}...")
    print()
