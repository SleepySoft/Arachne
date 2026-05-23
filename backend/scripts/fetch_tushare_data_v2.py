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
    data = {}
    try:
        # Income statement
        df_income = pro.income(ts_code=ts_code, period='20231231', fields='ts_code,total_revenue,net_profit')
        time.sleep(0.3)
        data['income'] = json.loads(df_income.to_json(orient='records')) if df_income is not None and not df_income.empty else []
    except Exception as e:
        print(f'  income error: {e}')
        data['income'] = []
    
    try:
        # Balance sheet
        df_bal = pro.balancesheet(ts_code=ts_code, period='20231231', fields='ts_code,total_assets,total_liabilities')
        time.sleep(0.3)
        data['balancesheet'] = json.loads(df_bal.to_json(orient='records')) if df_bal is not None and not df_bal.empty else []
    except Exception as e:
        print(f'  balancesheet error: {e}')
        data['balancesheet'] = []
    
    try:
        # Fina indicator
        df_ind = pro.fina_indicator(ts_code=ts_code, period='20231231')
        time.sleep(0.3)
        data['fina_indicator'] = json.loads(df_ind.to_json(orient='records')) if df_ind is not None and not df_ind.empty else []
    except Exception as e:
        print(f'  fina_indicator error: {e}')
        data['fina_indicator'] = []
    
    try:
        # Daily basic (latest)
        df_basic = pro.daily_basic(ts_code=ts_code, fields='ts_code,total_mv,circ_mv,total_share,float_share,pe_ttm,pb')
        time.sleep(0.3)
        data['daily_basic'] = json.loads(df_basic.to_json(orient='records')) if df_basic is not None and not df_basic.empty else []
    except Exception as e:
        print(f'  daily_basic error: {e}')
        data['daily_basic'] = []
    
    try:
        # Stock company detail
        df_comp = pro.stock_company(exchange='SZSE', ts_code=ts_code)
        time.sleep(0.3)
        data['stock_company'] = json.loads(df_comp.to_json(orient='records')) if df_comp is not None and not df_comp.empty else []
    except Exception as e:
        print(f'  stock_company error: {e}')
        data['stock_company'] = []
    
    results[ts_code] = data
    print('  income=' + str(len(data['income'])) + ' bal=' + str(len(data['balancesheet'])) + ' ind=' + str(len(data['fina_indicator'])) + ' basic=' + str(len(data['daily_basic'])) + ' comp=' + str(len(data['stock_company'])))

output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'stock_batches', 'batch_001_tushare_data.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'Saved to {output_path}')
