import os
import sys
sys.path.insert(0, 'backend')
import tushare as ts

ts.set_token(os.environ.get('TUSHARE_TOKEN'))
pro = ts.pro_api()

codes = ['000014.SZ','000016.SZ','000017.SZ','000019.SZ','000020.SZ','000021.SZ','001872.SZ','000025.SZ','000026.SZ','000027.SZ']

# Get basic stock info
df = pro.stock_basic(exchange='SZSE', list_status='L', fields='ts_code,symbol,name,fullname,industry,list_date,province,city')
sz = df[df['ts_code'].isin(codes)]
print("=== Stock Basic ===")
print(sz.to_string())

# Get financial data for each
print("\n=== Financial Overview ===")
for code in codes:
    try:
        fin = pro.fina_indicator(ts_code=code, period='20241231')
        if fin is not None and not fin.empty:
            row = fin.iloc[0]
            print(f"{code}: revenue={row.get('revenue', 'N/A')}, profit={row.get('profit_dedt', 'N/A')}, employees={row.get('emp_num', 'N/A')}")
        else:
            print(f"{code}: no fina_indicator data")
    except Exception as e:
        print(f"{code}: error - {e}")
