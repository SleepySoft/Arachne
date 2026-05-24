import json

for i in range(11, 16):
    with open(f'data/stock_batches/batch_{i:03d}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"\n=== batch_{i:03d}: {len(data)} companies ===")
    for c in data:
        print(f"{c['ts_code']} | {c['name']} | {c['industry']} | {c['area']}")
        print(f"  main_business: {c.get('main_business','')}")
        print(f"  business_scope: {c.get('business_scope','')[:120]}...")
