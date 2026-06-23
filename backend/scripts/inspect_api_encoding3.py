import requests
import sys

print("stdout encoding:", sys.stdout.encoding)
url = "http://localhost:16060/api/v1/edges?page=1&page_size=1"
resp = requests.get(url, timeout=5)
content = resp.content
text = content.decode('utf-8')
# find description substring
import json
data = json.loads(text)
desc = data['items'][0]['description']
print("repr:", repr(desc))
print("len:", len(desc))
print("bytes:", desc.encode('utf-8'))
