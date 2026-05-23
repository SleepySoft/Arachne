import tushare as ts
import os
pro = ts.pro_api(os.environ.get('TUSHARE_TOKEN'))

codes = ['000042.SZ', '001914.SZ', '000045.SZ', '000048.SZ', '000049.SZ',
         '000050.SZ', '000055.SZ', '000056.SZ', '000058.SZ', '000059.SZ']

print('=== INCOME ===')
for code in codes:
    df = pro.income(ts_code=code, period='20251231')
    if not df.empty:
        row = df.iloc[0]
        print(f"{code}: revenue={row.get('total_revenue')}, net={row.get('n_income_attr_p')}")
    else:
        print(f'{code}: NO')

print()
print('=== DAILY_BASIC ===')
for code in codes:
    df = pro.daily_basic(ts_code=code, trade_date='20260522')
    if not df.empty:
        print(f"{code}: mv={df.iloc[0].get('total_mv')}")
    else:
        print(f'{code}: NO')
