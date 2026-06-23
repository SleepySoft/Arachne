import requests

url = "http://localhost:16060/api/v1/edges?page=1&page_size=2"
resp = requests.get(url, timeout=5)
print("status", resp.status_code)
print("encoding", resp.encoding)
print("content first 500 bytes", resp.content[:500])
print("text first 500 chars", resp.text[:500])
