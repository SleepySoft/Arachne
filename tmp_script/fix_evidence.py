import json, re

with open('tmp_script/tmp_submit_batch_116.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"source":', '"source_title":')
content = content.replace('"url":', '"source_url":')

def fix_evidence(m):
    s = m.group(0)
    s = s.replace('}', ', "quote": ""}')
    return s

content = re.sub(r'\{"source_title": "[^"]+", "source_url": "[^"]*", "timestamp": "[^"]+"\}', fix_evidence, content)

with open('tmp_script/tmp_submit_batch_116.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
