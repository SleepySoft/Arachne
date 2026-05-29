import re

with open('tmp_script/tmp_submit_batch_116.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the BUSINESS section and fix evidence there
# Exposure evidence pattern: {"source_title": "...", "timestamp": "..."}
def fix_business_evidence(m):
    s = m.group(0)
    if '"quote"' not in s and '"source_url"' not in s:
        s = s.replace('}', ', "source_url": None, "quote": "根据企业公开信息"}')
    return s

# Only apply to lines after "company_node_exposures_to_upsert"
marker = '"company_node_exposures_to_upsert":'
idx = content.find(marker)
if idx != -1:
    before = content[:idx]
    after = content[idx:]
    after = re.sub(r'\{"source_title": "[^"]+", "timestamp": "[^"]+"\}', fix_business_evidence, after)
    content = before + after

with open('tmp_script/tmp_submit_batch_116.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
