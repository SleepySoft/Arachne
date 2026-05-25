import requests, time

r = requests.post('http://localhost:8000/api/v1/company-view/versions', timeout=30)
print('Create:', r.status_code, r.json())
job_id = r.json()['job_id']

for _ in range(30):
    time.sleep(2)
    j = requests.get(f'http://localhost:8000/api/v1/computation-jobs/{job_id}', timeout=30).json()
    print(f"  {j['status']} {j.get('processed_items',0)}/{j.get('total_items',0)}")
    if j['status'] in ('completed','failed'):
        if j.get('error_message'):
            print('  ERROR:', j['error_message'])
        break

v = requests.get('http://localhost:8000/api/v1/company-view/versions', timeout=30)
print('\nVersions:', v.json())
