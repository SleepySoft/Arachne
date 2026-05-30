with open('tmp_generate_091_095.py', encoding='utf-8') as f:
    content = f.read()
content = content.replace('"source_id": "{sid}",', '"from_node": "{sid}",')
content = content.replace('"target_id": "{tid}",', '"to_node": "{tid}",')
with open('tmp_generate_091_095.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
