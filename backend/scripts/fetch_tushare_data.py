import tushare as ts
import os
import time
import json
import sys

ts.set_token(os.environ['TUSHARE_TOKEN'])
pro = ts.pro_api()

stocks = ['000001.SZ','000002.SZ','000004.SZ','000006.SZ','000007.SZ','000008.SZ','000009.SZ','000010.SZ','000011.SZ','000012.SZ']

results = {}
for ts_code in stocks:
    print(f'Fetching {ts_code}...')
    try:
        # Main business composition (most recent year)
        df_mainbz = pro.fina_mainbz_v2(ts_code=ts_code, type='1', period='20241231')
        time.sleep(0.3)
        
        # Income statement
        df_income = pro.income(ts_code=ts_code, period='20241231', fields='ts_code,total_revenue,net_profit')
        time.sleep(0.3)
        
        # Daily basic (latest market data)
        df_basic = pro.daily_basic(ts_code=ts_code, fields='ts_code,total_mv,circ_mv,total_share,float_share')
        time.sleep(0.3)
        
        results[ts_code] = {
            'main_business': json.loads(df_mainbz.to_json(orient='records')) if df_mainbz is not None and not df_mainbz.empty else [],
            'income': json.loads(df_income.to_json(orient='records')) if df_income is not None and not df_income.empty else [],
            'daily_basic': json.loads(df_basic.to_json(orient='records')) if df_basic is not None and not df_basic.empty else [],
        }
        print(f'  main_biz rows: {len(results[ts_code]["main_business"])}')
    except Exception as e:
        print(f'  ERROR: {e}')

output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'stock_batches', 'batch_001_tushare_data.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'Saved to {output_path}')
