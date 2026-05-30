with open('tmp_generate_096_100.py', encoding='utf-8') as f:
    content = f.read()

# Fix TEMPLATE back to escaped braces for .format()
content = content.replace('BASE = "http://localhost:8005/api/v1"', 'BASE = "{{BASE}}"')
content = content.replace('BASE = "http://localhost:8005/api/v1"', 'BASE = "{{BASE}}"')

# Replace .format() call
old = '''    content = TEMPLATE
    content = content.replace("{batch_num:03d}", f"{batch_num:03d}")
    content = content.replace("{batch_num}", str(batch_num))
    content = content.replace("{nodes_code}", nodes_code)
    content = content.replace("{edges_code}", edges_code)
    content = content.replace("{companies_code}", companies_code)'''
new = '''    content = TEMPLATE.format(
        batch_num=batch_num,
        nodes_code=nodes_code,
        edges_code=edges_code,
        companies_code=companies_code,
    )'''
content = content.replace(old, new)

with open('tmp_generate_096_100.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed3')
