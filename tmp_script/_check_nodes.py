import requests
BASE = 'http://localhost:8000/api/v1'
keywords = ['石膏', '电池', '磁', '烟', '油', 'ndfeb', 'lithium', 'petrol', 'gasoline', '成品油']
for kw in keywords:
    r = requests.get(f'{BASE}/nodes?page=1&page_size=10', params={'search': kw})
    if r.status_code == 200:
        data = r.json()
        items = data.get('items', [])
        print(f'=== {kw} ({len(items)} results) ===')
        for item in items[:5]:
            print(f'  {item["node_id"]} | {item["canonical_name_zh"]}')
