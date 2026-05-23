# -*- coding: utf-8 -*-
"""
Resume fetching ALL A-share stocks from where it left off.
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

def fetch_company_details(ts_code):
    try:
        df = tushare_query('stock_company', {'ts_code': ts_code}, 'ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
        if len(df) > 0:
            row = df.iloc[0]
            return {
                'main_business': str(row.get('main_business', '') or ''),
                'business_scope': str(row.get('business_scope', '') or ''),
                'employees': str(row.get('employees', '') or ''),
                'province': str(row.get('province', '') or ''),
                'city': str(row.get('city', '') or ''),
                'reg_capital': str(row.get('reg_capital', '') or ''),
                'setup_date': str(row.get('setup_date', '') or ''),
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
    
    # Find where we left off
    existing_batches = sorted([f for f in os.listdir(OUTPUT_DIR) if f.startswith('batch_') and f.endswith('.json') and f != 'summary.json'])
    start_batch = len(existing_batches) + 1
    
    # Read the last batch to see how many records were in it
    processed_count = 0
    if existing_batches:
        for bfile in existing_batches:
            with open(os.path.join(OUTPUT_DIR, bfile), 'r', encoding='utf-8') as f:
                batch_data = json.load(f)
                processed_count += len(batch_data)
    
    print(f'Resuming from batch {start_batch}, already processed {processed_count} companies')
    
    # Fetch all stocks
    print('Fetching all A-share stocks from Tushare...')
    df = tushare_query('stock_basic', {'list_status': 'L'}, 'ts_code,symbol,name,area,industry,list_date,fullname,market,exchange')
    print(f'Total stocks: {len(df)}')
    
    # Skip already processed
    df = df.iloc[processed_count:].copy()
    print(f'Remaining to process: {len(df)}')
    
    batch_size = 10
    current_batch = []
    batch_num = start_batch
    total_processed = processed_count
    
    print('\nFetching company details and saving batches...')
    
    for idx, row in df.iterrows():
        ts_code = row['ts_code']
        total_processed += 1
        print(f'[{total_processed}/{len(df) + processed_count}] {ts_code} - {row["name"]}')
        
        details = fetch_company_details(ts_code)
        
        record = {
            'ts_code': str(ts_code) if ts_code is not None else '',
            'symbol': str(row['symbol']) if row['symbol'] is not None else '',
            'name': str(row['name']) if row['name'] is not None else '',
            'fullname': str(row['fullname']) if row['fullname'] is not None else '',
            'area': str(row['area']) if row['area'] is not None else '',
            'industry': str(row['industry']) if row['industry'] is not None else '',
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
        
        if len(current_batch) >= batch_size:
            save_batch(current_batch, batch_num)
            current_batch = []
            batch_num += 1
        
        time.sleep(0.15)
    
    if current_batch:
        save_batch(current_batch, batch_num)
        batch_num += 1
    
    total_batches = batch_num - 1
    
    summary = {
        'total_stocks': int(total_processed),
        'total_batches': total_batches,
        'batch_size': batch_size,
    }
    
    with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print('\nDone!')
    print(f'Total batches: {total_batches}')

if __name__ == '__main__':
    main()
