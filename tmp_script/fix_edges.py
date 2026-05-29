import re

with open('tmp_script/tmp_submit_batch_116.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace variant_of with composition
content = content.replace('"edge_type": "variant_of"', '"edge_type": "composition"')

# Add evidence to edges that have "evidence": []
def add_evidence(m):
    return '"evidence": [{"source_title": "产业知识图谱", "source_url": None, "quote": "工业流程关系定义"}]'

content = re.sub(r'"evidence": \[\]', add_evidence, content)

with open('tmp_script/tmp_submit_batch_116.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
