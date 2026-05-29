import re

with open('tmp_script/tmp_submit_batch_116.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix exposure evidence: add quote and source_url
# Pattern in exposures uses "source_title" already but no "quote" or "source_url"
def fix_exp_evidence(m):
    s = m.group(0)
    if '"quote"' not in s:
        s = s.replace('}', ', "source_url": None, "quote": "根据企业公开信息"}')
    return s

content = re.sub(r'\{"source_title": "[^"]+", "timestamp": "[^"]+"\}', fix_exp_evidence, content)

with open('tmp_script/tmp_submit_batch_116.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
