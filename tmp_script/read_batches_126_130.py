#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, glob

for path in sorted(glob.glob('data/stock_batches/batch_12[6-9].json') + glob.glob('data/stock_batches/batch_130.json')):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"=== {path} ===")
    for item in data:
        mb = item.get('main_business', '')[:80]
        print(f"  {item['ts_code']}: {item['name']} - {mb}")
    print()
