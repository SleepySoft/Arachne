import json, sys
sys.path.insert(0, 'backend')

# Load data from build script
with open('tmp_build_batch_002.py', 'r', encoding='utf-8') as f:
    code = f.read()
    idx = code.find('print(f"Companies:')
    if idx > 0:
        code = code[:idx]
    namespace = {}
    exec(code, namespace)
    
    data = {
        "NEW_NODES": namespace["NEW_NODES"],
        "EDGES": namespace["EDGES"],
        "COMPANIES": namespace["COMPANIES"],
        "EXPOSURES": namespace["EXPOSURES"]
    }
    with open('tmp_batch_002_data.json', 'w', encoding='utf-8') as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
    print("Saved to tmp_batch_002_data.json")
