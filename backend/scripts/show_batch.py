import json
import sys

batch_file = sys.argv[1] if len(sys.argv) > 1 else '../data/stock_batches/batch_001.json'
with open(batch_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, c in enumerate(data):
    ts = c['ts_code']
    name = c['name']
    ind = c['industry']
    cat = c['broad_category']
    mb = c.get('main_business', '')[:60]
    print(f"{i+1}. {ts} | {name} | {ind} | {cat}")
    print(f"   {mb}")
