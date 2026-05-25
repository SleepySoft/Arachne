import requests, time

job_id = "company_view_compute_all_20260524082535315853"

for _ in range(30):
    time.sleep(2)
    job = requests.get(f'http://localhost:8000/api/v1/computation-jobs/{job_id}', timeout=30)
    j = job.json()
    print(f"Status: {j.get('status')} | processed: {j.get('processed_items')}/{j.get('total_items')}")
    if j.get('status') in ('completed', 'failed'):
        break

# Check versions
versions = requests.get('http://localhost:8000/api/v1/company-view/versions', timeout=30)
print('\nVersions:')
print(versions.json())
