import json, os
os.chdir('C:/D/code/Arachne')
with open('data/stock_batches/batch_010.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for c in data:
    print(c['ts_code'], '|', c['name'], '|', c['industry'], '|', c['main_business'][:100])
