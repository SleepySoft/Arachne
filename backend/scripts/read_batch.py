import json
import sys

batch_file = sys.argv[1] if len(sys.argv) > 1 else 'batch_001.json'
with open(batch_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, company in enumerate(data):
    print(f'{i+1}. {company["ts_code"]} | {company["name"]} | {company["industry"]} | {company["broad_category"]}')
    mb = company.get('main_business', '')
    print(f'   main_business: {mb[:100]}...' if len(mb) > 100 else f'   main_business: {mb}')
    print()
