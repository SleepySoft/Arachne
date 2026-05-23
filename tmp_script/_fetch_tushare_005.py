import os, sys, json
import tushare as ts

os.chdir('C:/D/code/Arachne')

pro = ts.pro_api(os.environ.get('TUSHARE_TOKEN'))

with open('data/stock_batches/batch_005.json', 'r', encoding='utf-8') as f:
    companies = json.load(f)

results = {}
for c in companies:
    ts_code = c['ts_code']
    symbol = c['symbol']
    print(f"Fetching {ts_code} {c['name']} ...")
    try:
        # 财务数据
        fin = pro.fina_indicator(ts_code=ts_code, period='20241231', fields='ts_code,ann_date,end_date,revenue,operate_profit,netprofit_yoy,grossprofit_margin')
        # 公司基本信息
        basic = pro.stock_company(ts_code=ts_code, fields='ts_code,employees,reg_capital,setup_date,website,email')
        results[ts_code] = {
            'basic': basic.to_dict('records') if basic is not None and not basic.empty else [],
            'finance': fin.to_dict('records') if fin is not None and not fin.empty else []
        }
    except Exception as e:
        print(f"  Error: {e}")
        results[ts_code] = {'error': str(e)}

with open('tmp_script/tushare_005_data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved to tmp_script/tushare_005_data.json")
