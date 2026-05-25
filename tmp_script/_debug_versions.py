import requests, time

# Wait for the compute job to finish
job_id = "company_view_compute_all_20260524083909191932"
for _ in range(30):
    time.sleep(2)
    j = requests.get(f'http://localhost:8000/api/v1/computation-jobs/{job_id}', timeout=30).json()
    print(f"Job status: {j['status']} processed={j.get('processed_items')}/{j.get('total_items')}")
    if j['status'] in ('completed', 'failed'):
        break

# Now check versions
r = requests.get('http://localhost:8000/api/v1/company-view/versions', timeout=30)
print('\nVersions after compute:')
print(r.json())
