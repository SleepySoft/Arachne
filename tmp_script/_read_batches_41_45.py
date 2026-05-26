import json
for n in range(41, 46):
    with open(f'data/stock_batches/batch_{n:03d}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'=== Batch {n} ===')
    for c in data:
        print(f"{c['ts_code']} | {c['name']} | {c['industry']} | {c.get('main_business','')[:50]}")
    print()
