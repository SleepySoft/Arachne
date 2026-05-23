import json, os
os.chdir('C:/D/code/Arachne')
with open('tmp_script/tushare_005_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for k, v in data.items():
    fin = v.get('finance', [{}])[0] if v.get('finance') else {}
    print(k, '|', 'revenue=', fin.get('revenue'), '| profit_yoy=', fin.get('netprofit_yoy'))
