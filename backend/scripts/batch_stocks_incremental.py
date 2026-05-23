# -*- coding: utf-8 -*-
"""
Fetch A-share stocks from Tushare, filter by 4 broad industry categories,
fetch company details incrementally, and save into batch files (10 companies per file).
"""
import os
import json
import urllib.request
import time
import pandas as pd

TOKEN = os.environ['TUSHARE_TOKEN']
URL = 'http://api.tushare.pro'
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'stock_batches')

def tushare_query(api_name, params=None, fields=None):
    payload = {
        'api_name': api_name,
        'token': TOKEN,
        'params': params or {},
        'fields': fields
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    if result.get('code') != 0:
        raise Exception('API error: ' + str(result.get('msg')))
    df = pd.DataFrame(result['data']['items'], columns=result['data']['fields'])
    return df

# Mapping from Tushare industry names to our 4 broad categories
CATEGORY_MAP = {
    '新能源': 'new_energy_ev',
    '新能源汽车': 'new_energy_ev',
    '电气设备': 'new_energy_ev',
    '电源设备': 'new_energy_ev',
    '电池': 'new_energy_ev',
    '光伏设备': 'new_energy_ev',
    '电机': 'new_energy_ev',
    '电网设备': 'new_energy_ev',
    '风电设备': 'new_energy_ev',
    '储能': 'new_energy_ev',
    '锂电池': 'new_energy_ev',
    '太阳能电池': 'new_energy_ev',
    '充电桩': 'new_energy_ev',
    '电动车': 'new_energy_ev',
    '汽车整车': 'new_energy_ev',
    '汽车零部件': 'new_energy_ev',
    '汽车配件': 'new_energy_ev',

    '半导体': 'semiconductor_electronics',
    '电子制造': 'semiconductor_electronics',
    '电子元件': 'semiconductor_electronics',
    '集成电路': 'semiconductor_electronics',
    '芯片': 'semiconductor_electronics',
    '分立器件': 'semiconductor_electronics',
    'LED': 'semiconductor_electronics',
    '光学光电子': 'semiconductor_electronics',
    '面板': 'semiconductor_electronics',
    '印制电路板': 'semiconductor_electronics',
    '被动元件': 'semiconductor_electronics',
    '消费电子': 'semiconductor_electronics',
    '通信设备': 'semiconductor_electronics',
    '计算机设备': 'semiconductor_electronics',
    'IT设备': 'semiconductor_electronics',
    '软件服务': 'semiconductor_electronics',
    '通信服务': 'semiconductor_electronics',
    '元器件': 'semiconductor_electronics',
    '电子设备': 'semiconductor_electronics',

    '食品饮料': 'consumer_medicine',
    '白酒': 'consumer_medicine',
    '啤酒': 'consumer_medicine',
    '调味品': 'consumer_medicine',
    '乳制品': 'consumer_medicine',
    '食品': 'consumer_medicine',
    '医药制造': 'consumer_medicine',
    '生物制药': 'consumer_medicine',
    '医疗器械': 'consumer_medicine',
    '医疗服务': 'consumer_medicine',
    '中药': 'consumer_medicine',
    '化学制药': 'consumer_medicine',
    '医药商业': 'consumer_medicine',
    '医疗耗材': 'consumer_medicine',
    '保健品': 'consumer_medicine',
    '制药': 'consumer_medicine',
    '医药': 'consumer_medicine',
    '医疗': 'consumer_medicine',
    '药品': 'consumer_medicine',
    '酒类': 'consumer_medicine',
    '饮料': 'consumer_medicine',
    '休闲食品': 'consumer_medicine',
    '食品加工': 'consumer_medicine',
    '农产品加工': 'consumer_medicine',
    '养殖业': 'consumer_medicine',
    '种植业': 'consumer_medicine',

    '钢铁': 'traditional_manufacturing_resources',
    '煤炭开采': 'traditional_manufacturing_resources',
    '有色金属': 'traditional_manufacturing_resources',
    '化学制品': 'traditional_manufacturing_resources',
    '化工新材料': 'traditional_manufacturing_resources',
    '石油化工': 'traditional_manufacturing_resources',
    '石油加工': 'traditional_manufacturing_resources',
    '基础化学': 'traditional_manufacturing_resources',
    '化学原料': 'traditional_manufacturing_resources',
    '塑料': 'traditional_manufacturing_resources',
    '橡胶': 'traditional_manufacturing_resources',
    '造纸': 'traditional_manufacturing_resources',
    '建材': 'traditional_manufacturing_resources',
    '水泥': 'traditional_manufacturing_resources',
    '玻璃': 'traditional_manufacturing_resources',
    '陶瓷': 'traditional_manufacturing_resources',
    '纺织': 'traditional_manufacturing_resources',
    '服装': 'traditional_manufacturing_resources',
    '化工': 'traditional_manufacturing_resources',
    '化纤': 'traditional_manufacturing_resources',
    '农药': 'traditional_manufacturing_resources',
    '化肥': 'traditional_manufacturing_resources',
    '煤炭': 'traditional_manufacturing_resources',
    '石油': 'traditional_manufacturing_resources',
    '天然气': 'traditional_manufacturing_resources',
    '矿业': 'traditional_manufacturing_resources',
    '金属': 'traditional_manufacturing_resources',
    '材料': 'traditional_manufacturing_resources',
    '工业金属': 'traditional_manufacturing_resources',
    '贵金属': 'traditional_manufacturing_resources',
    '小金属': 'traditional_manufacturing_resources',
    '冶炼': 'traditional_manufacturing_resources',
    '包装印刷': 'traditional_manufacturing_resources',
    '家居用品': 'traditional_manufacturing_resources',
    '家用轻工': 'traditional_manufacturing_resources',
    '石油贸易': 'traditional_manufacturing_resources',
    '焦炭加工': 'traditional_manufacturing_resources',
    '综合': 'traditional_manufacturing_resources',
}

def classify_industry(industry_name):
    return CATEGORY_MAP.get(industry_name, None)

def fetch_company_details(ts_code):
    try:
        df = tushare_query('stock_company', {'ts_code': ts_code}, 'ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
        if len(df) > 0:
            row = df.iloc[0]
            return {
                'main_business': row.get('main_business', '') or '',
                'business_scope': row.get('business_scope', '') or '',
                'employees': row.get('employees', '') or '',
                'province': row.get('province', '') or '',
                'city': row.get('city', '') or '',
                'reg_capital': row.get('reg_capital', '') or '',
                'setup_date': row.get('setup_date', '') or '',
            }
    except Exception as e:
        print(f'  Error fetching details for {ts_code}: {e}')
    return {}

def save_batch(batch, batch_num):
    filepath = os.path.join(OUTPUT_DIR, f'batch_{batch_num:03d}.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
    print(f'  -> Saved {filepath} ({len(batch)} companies)')

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Fetch all stocks
    print('Fetching all A-share stocks from Tushare...')
    df = tushare_query('stock_basic', {'list_status': 'L'}, 'ts_code,symbol,name,area,industry,list_date,fullname,market,exchange')
    print(f'Total stocks fetched: {len(df)}')
    
    # Classify each stock
    df['broad_category'] = df['industry'].apply(classify_industry)
    
    # Filter to our 4 categories
    filtered = df[df['broad_category'].notna()].copy()
    print(f'Stocks in 4 target categories: {len(filtered)}')
    
    for cat in ['new_energy_ev', 'semiconductor_electronics', 'consumer_medicine', 'traditional_manufacturing_resources']:
        count = len(filtered[filtered['broad_category'] == cat])
        print(f'  {cat}: {count}')
    
    # Fetch company details and save incrementally into batches of 10
    batch_size = 10
    current_batch = []
    batch_num = 1
    total_processed = 0
    
    print('\nFetching company details and saving batches...')
    
    for idx, row in filtered.iterrows():
        ts_code = row['ts_code']
        total_processed += 1
        print(f'[{total_processed}/{len(filtered)}] {ts_code} - {row["name"]}')
        
        details = fetch_company_details(ts_code)
        
        record = {
            'ts_code': str(ts_code) if ts_code is not None else '',
            'symbol': str(row['symbol']) if row['symbol'] is not None else '',
            'name': str(row['name']) if row['name'] is not None else '',
            'fullname': str(row['fullname']) if row['fullname'] is not None else '',
            'area': str(row['area']) if row['area'] is not None else '',
            'industry': str(row['industry']) if row['industry'] is not None else '',
            'broad_category': str(row['broad_category']) if row['broad_category'] is not None else '',
            'market': str(row['market']) if row['market'] is not None else '',
            'exchange': str(row['exchange']) if row['exchange'] is not None else '',
            'list_date': str(row['list_date']) if row['list_date'] is not None else '',
            'main_business': str(details.get('main_business', '')),
            'business_scope': str(details.get('business_scope', '')),
            'employees': str(details.get('employees', '')),
            'province': str(details.get('province', '')),
            'city': str(details.get('city', '')),
            'reg_capital': str(details.get('reg_capital', '')),
            'setup_date': str(details.get('setup_date', '')),
        }
        current_batch.append(record)
        
        # Save batch when it reaches batch_size
        if len(current_batch) >= batch_size:
            save_batch(current_batch, batch_num)
            current_batch = []
            batch_num += 1
        
        # Rate limiting
        time.sleep(0.15)
    
    # Save remaining records
    if current_batch:
        save_batch(current_batch, batch_num)
        batch_num += 1
    
    total_batches = batch_num - 1
    
    # Save summary
    summary = {
        'total_stocks': int(len(df)),
        'filtered_stocks': int(len(filtered)),
        'total_batches': total_batches,
        'batch_size': batch_size,
        'categories': {}
    }
    for cat in ['new_energy_ev', 'semiconductor_electronics', 'consumer_medicine', 'traditional_manufacturing_resources']:
        summary['categories'][cat] = int(len(filtered[filtered['broad_category'] == cat]))
    
    with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print('\nDone!')
    print(f'Output directory: {OUTPUT_DIR}')
    print(f'Total batches: {total_batches}')

if __name__ == '__main__':
    main()
