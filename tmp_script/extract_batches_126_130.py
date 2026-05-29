#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, glob, os

out_path = 'tmp_script/batches_126_130_summary.txt'
with open(out_path, 'w', encoding='utf-8') as out:
    for path in sorted(glob.glob('data/stock_batches/batch_12[6-9].json') + glob.glob('data/stock_batches/batch_130.json')):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        batch = os.path.basename(path).replace('.json','')
        out.write(f"=== {batch} ===\n")
        for item in data:
            out.write(f"  {item['ts_code']}: {item['name']}\n")
            out.write(f"    main: {item.get('main_business','')}\n")
            out.write(f"    scope: {item.get('business_scope','')[:200]}...\n")
            out.write(f"    emp: {item.get('employees','')}, prov: {item.get('province','')}, city: {item.get('city','')}\n")
            out.write("\n")
        out.write("\n")
print(f"Summary written to {out_path}")
