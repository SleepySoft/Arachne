import os
import json
import tushare as ts

pro = ts.pro_api(os.environ['TUSHARE_TOKEN'])

# Read batch
batch = json.load(open('data/stock_batches/batch_011.json', encoding='utf-8'))

tushare_data = {}
for company in batch:
    ts_code = company['ts_code']
    print(f"Fetching {ts_code} {company['name']}...")
    try:
        # Company basic info
        df = pro.stock_company(exchange=company['exchange'], ts_code=ts_code)
        basic = df.to_dict('records')[0] if not df.empty else {}

        # Main business detail
        df2 = pro.fina_indicator(ts_code=ts_code, limit=1)
        fina = df2.to_dict('records')[0] if not df2.empty else {}

        tushare_data[ts_code] = {
            'basic': basic,
            'fina': fina,
            'batch': company
        }
    except Exception as e:
        print(f"  Error: {e}")
        tushare_data[ts_code] = {'error': str(e), 'batch': company}

# Save
out_path = 'data/stock_batches/batch_011_tushare_data.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(tushare_data, f, ensure_ascii=False, indent=2)
print(f"Saved to {out_path}")
