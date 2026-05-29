import json
import sys

def read_batch(n):
    with open(f'data/stock_batches/batch_{n}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    data = read_batch(n)
    print(f"=== Batch {n}: {len(data)} companies ===")
    for i, c in enumerate(data):
        print(f"\n--- Company {i+1} ---")
        for k, v in c.items():
            print(f"{k}: {v}")
