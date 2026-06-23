import requests

url = "http://localhost:16060/api/v1/edges?page=1&page_size=2"
resp = requests.get(url, timeout=5)
content = resp.content
# manually decode as utf-8
text = content.decode('utf-8')
print(text[:500])
