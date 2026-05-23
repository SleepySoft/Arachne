# -*- coding: utf-8 -*-
import os
import json
import urllib.request
import pandas as pd

TOKEN = os.environ['TUSHARE_TOKEN']
URL = 'http://api.tushare.pro'

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

# Fetch all stocks
print('Fetching all A stocks...')
df = tushare_query('stock_basic', {'list_status': 'L'}, 'ts_code,symbol,name,area,industry,list_date,fullname,market,exchange')
print(f'Total stocks: {len(df)}')

# Define industry mappings
# Note: These are Tushare's industry classifications (证监会行业/申万行业)
# We map them to our 4 broad categories

NEW_ENERGY_EV = [
    '电气设备', '电源设备', '电池', '光伏设备', '新能源', '新能源汽车',
    '电机', '电网设备', '风电设备', '储能', '锂电池', '太阳能电池',
    '充电桩', '电动车', '汽车整车', '汽车零部件', '汽车配件'
]

SEMICONDUCTOR_ELECTRONICS = [
    '半导体', '电子制造', '电子元件', '集成电路', '芯片', '分立器件',
    'LED', '光学光电子', '面板', '印制电路板', '被动元件', '消费电子',
    '通信设备', '计算机设备', 'IT设备', '软件服务', '通信服务',
    '元器件', '电子设备', '通信服务'
]

CONSUMER_MEDICINE = [
    '食品饮料', '白酒', '啤酒', '调味品', '乳制品', '食品',
    '医药制造', '生物制药', '医疗器械', '医疗服务', '中药',
    '化学制药', '医药商业', '医疗耗材', '保健品', '制药',
    '医药', '医疗', '药品', '酒类', '饮料', '休闲食品',
    '食品加工', '农产品加工', '养殖业', '种植业'
]

TRADITIONAL_MANUFACTURING_RESOURCES = [
    '钢铁', '煤炭开采', '有色金属', '化学制品', '化工新材料',
    '石油化工', '石油加工', '基础化学', '化学原料', '塑料',
    '橡胶', '造纸', '建材', '水泥', '玻璃', '陶瓷',
    '纺织', '服装', '化工', '化纤', '农药', '化肥',
    '煤炭', '石油', '天然气', '矿业', '金属', '材料',
    '工业金属', '贵金属', '小金属', '钢铁', '冶炼',
    '造纸', '包装印刷', '家居用品', '家用轻工'
]

# Print all unique industries for manual inspection
print('\n=== All Tushare Industries ===')
for ind in sorted(df['industry'].dropna().unique()):
    count = len(df[df['industry'] == ind])
    print(f'{ind}: {count}')

# Save all industries to a reference file
with open('all_industries.json', 'w', encoding='utf-8') as f:
    industries = []
    for ind in sorted(df['industry'].dropna().unique()):
        industries.append({'industry': ind, 'count': int(len(df[df['industry'] == ind]))})
    json.dump(industries, f, ensure_ascii=False, indent=2)
print('\nSaved all_industries.json')
