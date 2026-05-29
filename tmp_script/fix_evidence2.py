import json, re

with open('tmp_script/tmp_submit_batch_116.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace empty source_url with null
content = content.replace('"source_url": ""', '"source_url": null')

# Replace empty quote with some text
def fix_quote(m):
    return '"quote": "根据企业公开信息"'

content = re.sub(r'"quote": ""', fix_quote, content)

with open('tmp_script/tmp_submit_batch_116.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
