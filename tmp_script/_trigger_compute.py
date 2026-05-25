import requests, time

# Trigger compute
r = requests.post('http://localhost:8000/api/v1/company-view/compute', timeout=30)
data = r.json()
print('Job created:', data)
job_id = data['job_id']

# Poll for completion
for _ in range(30):
    time.sleep(2)
    status = requests.get(f'http://localhost:8000/api/v1/computation-jobs/{job_id}', timeout=30)
    s = status.json()
    print(f"Status: {s.get('status')} | processed: {s.get('processed_items')}/{s.get('total_items')}")
    if s.get('status') in ('completed', 'failed'):
        print('Final:', s)
        break
