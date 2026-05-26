import json, os
for n in range(35, 41):
    path = f'data/stock_batches/batch_{n:03d}.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'Batch {n}: {len(data)} companies')
        for c in data[:3]:
            print(f'  {c["ts_code"]}: {c["name"]} ({c["industry"]})')
        if len(data) > 3:
            print(f'  ... and {len(data)-3} more')
    else:
        print(f'Batch {n}: NOT FOUND')
