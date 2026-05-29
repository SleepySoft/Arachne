import json

for n in range(101, 106):
    with open(f'data/stock_batches/batch_{n}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    out_path = f'tmp_script/_batch_{n}_dump.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"=== Batch {n}: {len(data)} companies ===\n\n")
        for i, c in enumerate(data):
            f.write(f"--- {c['ts_code']} | {c['name']} | {c['industry']} ---\n")
            f.write(f"fullname: {c['fullname']}\n")
            f.write(f"main_business: {c['main_business']}\n")
            f.write(f"business_scope: {c['business_scope'][:200]}...\n")
            f.write(f"area: {c['area']}, province: {c.get('province','')}, city: {c.get('city','')}\n")
            f.write(f"employees: {c.get('employees','')}, reg_capital: {c.get('reg_capital','')}\n\n")
    print(f"Dumped batch {n} to {out_path}")
