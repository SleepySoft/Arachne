import json

for i in range(11, 16):
    with open(f'data/stock_batches/batch_{i:03d}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    out = []
    for c in data:
        out.append({
            'ts_code': c['ts_code'],
            'name': c['name'],
            'fullname': c['fullname'],
            'industry': c['industry'],
            'area': c['area'],
            'province': c.get('province'),
            'city': c.get('city'),
            'employees': c.get('employees'),
            'reg_capital': c.get('reg_capital'),
            'setup_date': c.get('setup_date'),
            'list_date': c.get('list_date'),
            'main_business': c.get('main_business', ''),
            'business_scope': c.get('business_scope', '')
        })
    with open(f'tmp_script/batch_{i:03d}_summary.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f'Dumped batch_{i:03d}')
