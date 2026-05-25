import requests, time

# Step 1: Create two versions
for i in range(2):
    r = requests.post('http://localhost:8000/api/v1/company-view/versions', timeout=30)
    job_id = r.json()['job_id']
    print(f"Created job {i+1}: {job_id}")
    
    # Wait for completion
    for _ in range(30):
        time.sleep(2)
        j = requests.get(f'http://localhost:8000/api/v1/computation-jobs/{job_id}', timeout=30).json()
        if j['status'] in ('completed', 'failed'):
            print(f"  Job {i+1} {j['status']}")
            break

# Step 2: List versions (simulate opening panel)
v1 = requests.get('http://localhost:8000/api/v1/company-view/versions', timeout=30)
print(f"\nPanel open - versions: {v1.json()['total']}")
for item in v1.json()['items']:
    print(f"  #{item['version_id']} status={item['status']}")

# Step 3: Delete first version
target_id = v1.json()['items'][0]['version_id']
print(f"\nDeleting version {target_id}...")
d = requests.delete(f'http://localhost:8000/api/v1/company-view/versions/{target_id}', timeout=30)
print(f"Delete status: {d.status_code}")

# Step 4: List again (simulate refresh after delete)
v2 = requests.get('http://localhost:8000/api/v1/company-view/versions', timeout=30)
print(f"\nAfter delete - versions: {v2.json()['total']}")
for item in v2.json()['items']:
    print(f"  #{item['version_id']} status={item['status']}")
