import json, sys
n = sys.argv[1]
data = json.load(open(f'data/stock_batches/batch_{n}.json', encoding='utf-8'))
print(f'Batch {n}: {len(data)} companies')
for d in data:
    print(f"  {d['ts_code']} {d['name']} - {d['industry']}")
    print(f"    main: {d.get('main_business', '')[:80]}...")
