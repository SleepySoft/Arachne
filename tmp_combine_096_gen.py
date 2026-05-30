with open('tmp_generate_091_095.py', encoding='utf-8') as f:
    header = f.readlines()[:187]

with open('tmp_generate_096_100.py', encoding='utf-8') as f:
    lines = f.readlines()

# Find data start and end
for i, line in enumerate(lines):
    if '# ============ BATCH 096' in line:
        data_start = i
        break
for i in range(len(lines)-1, -1, -1):
    if 'def generate_batch' in lines[i]:
        data_end = i
        break

data = lines[data_start:data_end]

footer = '''

def generate_batch(batch_num, companies, nodes, edges):
    nodes_code = build_nodes_code(nodes)
    edges_code = build_edges_code(edges)
    companies_code = build_companies_code(companies, batch_num)

    content = TEMPLATE.format(
        batch_num=batch_num,
        nodes_code=nodes_code,
        edges_code=edges_code,
        companies_code=companies_code,
    )

    out_path = f"tmp_script/tmp_submit_batch_{batch_num:03d}.py"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")


def main():
    os.makedirs("tmp_script", exist_ok=True)
    generate_batch(96, batch_096_companies, batch_096_nodes, batch_096_edges)
    generate_batch(97, batch_097_companies, batch_097_nodes, batch_097_edges)
    generate_batch(98, batch_098_companies, batch_098_nodes, batch_098_edges)
    generate_batch(99, batch_099_companies, batch_099_nodes, batch_099_edges)
    generate_batch(100, batch_100_companies, batch_100_nodes, batch_100_edges)
    print("All 5 batch scripts generated.")


if __name__ == "__main__":
    main()
'''

with open('tmp_generate_096_100.py', 'w', encoding='utf-8') as f:
    f.writelines(header)
    f.writelines(data)
    f.write(footer)
print('Combined OK')
