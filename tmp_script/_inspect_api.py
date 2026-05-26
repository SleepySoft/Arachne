import urllib.request, json

# Check current nodes and edges
for endpoint in ['/api/v1/query/stats', '/api/v1/nodes?page=1&page_size=5', '/api/v1/edges?page=1&page_size=5']:
    try:
        resp = urllib.request.urlopen(f'http://localhost:8005{endpoint}', timeout=10)
        data = json.loads(resp.read().decode())
        print(f'=== {endpoint} ===')
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1500])
        print()
    except Exception as e:
        print(f'=== {endpoint} === ERROR: {e}')
        print()
