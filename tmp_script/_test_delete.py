import requests, time

# Create first version
r1 = requests.post('http://localhost:8000/api/v1/company-view/versions', timeout=30)
job1 = r1.json()['job_id']
print(f"Created job1: {job1}")

# Wait for job1
for _ in range(30):
    time.sleep(2)
    j = requests.get(f'http://localhost:8000/api/v1/computation-jobs/{job1}', timeout=30).json()
    if j['status'] in ('completed', 'failed'):
        print(f"job1 {j['status']}")
        break

# Create second version
r2 = requests.post('http://localhost:8000/api/v1/company-view/versions', timeout=30)
job2 = r2.json()['job_id']
print(f"Created job2: {job2}")

# Wait for job2
for _ in range(30):
    time.sleep(2)
    j = requests.get(f'http://localhost:8000/api/v1/computation-jobs/{job2}', timeout=30).json()
    if j['status'] in ('completed', 'failed'):
        print(f"job2 {j['status']}")
        break

# List versions
v = requests.get('http://localhost:8000/api/v1/company-view/versions', timeout=30)
versions = v.json()
print(f"\nBefore delete: {versions['total']} versions")
for item in versions['items']:
    print(f"  version_id={item['version_id']}")

# Delete the first version
if versions['items']:
    vid = versions['items'][0]['version_id']
    d = requests.delete(f'http://localhost:8000/api/v1/company-view/versions/{vid}', timeout=30)
    print(f"\nDelete version {vid}: {d.status_code}")

# List again
v2 = requests.get('http://localhost:8000/api/v1/company-view/versions', timeout=30)
versions2 = v2.json()
print(f"After delete: {versions2['total']} versions")
for item in versions2['items']:
    print(f"  version_id={item['version_id']}")
