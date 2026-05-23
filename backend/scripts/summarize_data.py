import json
import os

base_dir = os.path.join(os.path.dirname(__file__), '..', '..')

with open(os.path.join(base_dir, 'data', 'stock_batches', 'batch_001.json'), 'r', encoding='utf-8') as f:
    companies = json.load(f)

with open(os.path.join(base_dir, 'data', 'stock_batches', 'batch_001_tushare_data.json'), 'r', encoding='utf-8') as f:
    tushare_data = json.load(f)

summary = {}
for comp in companies:
    ts_code = comp['ts_code']
    td = tushare_data.get(ts_code, {})
    
    # Get latest daily_basic
    daily = td.get('daily_basic', [])
    latest_daily = daily[0] if daily else {}
    
    # Get income
    income = td.get('income', [])
    latest_income = income[0] if income else {}
    
    # Get fina_indicator
    ind = td.get('fina_indicator', [])
    latest_ind = ind[0] if ind else {}
    
    summary[ts_code] = {
        'name': comp['name'],
        'fullname': comp['fullname'],
        'industry': comp['industry'],
        'main_business': comp.get('main_business', ''),
        'business_scope': comp.get('business_scope', '')[:200] + '...' if len(comp.get('business_scope', '')) > 200 else comp.get('business_scope', ''),
        'employees': comp.get('employees', ''),
        'province': comp.get('province', ''),
        'city': comp.get('city', ''),
        'reg_capital': comp.get('reg_capital', ''),
        'setup_date': comp.get('setup_date', ''),
        'total_revenue': latest_income.get('total_revenue'),
        'net_profit': latest_income.get('net_profit'),
        'total_mv': latest_daily.get('total_mv'),
        'pe_ttm': latest_daily.get('pe_ttm'),
        'pb': latest_daily.get('pb'),
        'roe': latest_ind.get('roe'),
    }

output_path = os.path.join(base_dir, 'data', 'stock_batches', 'batch_001_summary.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print('Summary saved to', output_path)
for ts_code, data in summary.items():
    print('\n' + ts_code + ' ' + data['name'] + ' (' + data['industry'] + ')')
    print('  主营: ' + str(data['main_business']))
    print('  营收: ' + str(data['total_revenue']) + ' 净利润: ' + str(data['net_profit']) + ' 市值: ' + str(data['total_mv']) + '万')
