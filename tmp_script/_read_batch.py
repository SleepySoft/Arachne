import json
import sys

batch_num = sys.argv[1] if len(sys.argv) > 1 else "011"
path = f"data/stock_batches/batch_{batch_num}.json"

data = json.load(open(path, encoding='utf-8'))
print(f"Batch {batch_num}: {len(data)} companies")
for d in data:
    print(f"  {d['ts_code']} {d['name']} - {d['industry']}")
