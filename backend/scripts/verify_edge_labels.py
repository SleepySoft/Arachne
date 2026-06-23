import requests
import json

url = "http://localhost:16060/api/v1/edges?page=1&page_size=10"
resp = requests.get(url, timeout=5)
data = resp.json()
out_path = r"C:\D\Code\git\Arachne\data\backups\verify_edge_labels.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Wrote {out_path}")
