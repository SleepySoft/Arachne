import json
for n in [37, 38, 39, 40]:
    with open(f'data/stock_batches/batch_{n:03d}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(f'tmp_script/_batch_{n}_summary.txt', 'w', encoding='utf-8') as out:
        out.write(f'Batch {n}\n')
        for c in data:
            out.write(f"{c['ts_code']} | {c['name']} | {c['industry']} | {c.get('main_business','')[:40]}\n")
