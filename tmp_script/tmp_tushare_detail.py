import os
import sys
sys.path.insert(0, 'backend')
import tushare as ts
import json

ts.set_token(os.environ.get('TUSHARE_TOKEN'))
pro = ts.pro_api()

codes = ['000014.SZ','000016.SZ','000017.SZ','000019.SZ','000020.SZ','000021.SZ','001872.SZ','000025.SZ','000026.SZ','000027.SZ']

results = {}
for code in codes:
    print(f"\n========== {code} ==========")
    # Fina indicator
    try:
        fin = pro.fina_indicator(ts_code=code, period='20241231')
        if fin is not None and not fin.empty:
            row = fin.iloc[0]
            revenue = row.get('revenue')
            profit = row.get('profit_dedt')
            total_assets = row.get('total_assets')
            print(f"revenue={revenue}, profit_dedt={profit}, total_assets={total_assets}")
    except Exception as e:
        print(f"fina error: {e}")
    
    # Main business composition
    try:
        main = pro.fina_mainbz(ts_code=code, period='20241231', type='P')
        if main is not None and not main.empty:
            print("Main business (by product):")
            for _, row in main.iterrows():
                name = row.get('bz_item', '')
                income = row.get('bz_sales', '')
                ratio = row.get('bz_profit', '')
                print(f"  {name}: sales={income}, profit={ratio}")
        else:
            print("No mainbz P data")
    except Exception as e:
        print(f"mainbz P error: {e}")
    
    # By industry
    try:
        main2 = pro.fina_mainbz(ts_code=code, period='20241231', type='I')
        if main2 is not None and not main2.empty:
            print("Main business (by industry):")
            for _, row in main2.iterrows():
                name = row.get('bz_item', '')
                income = row.get('bz_sales', '')
                print(f"  {name}: sales={income}")
        else:
            print("No mainbz I data")
    except Exception as e:
        print(f"mainbz I error: {e}")
