import json
import sys

def dump_batch(n):
    with open(f'data/stock_batches/batch_{n}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    out_path = f'tmp_script/_batch_{n}_dump.txt'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"=== Batch {n}: {len(data)} companies ===\n\n")
        for i, c in enumerate(data):
            f.write(f"--- Company {i+1} ---\n")
            for k, v in c.items():
                f.write(f"{k}: {v}\n")
            f.write("\n")
    print(f"Dumped to {out_path}")

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    dump_batch(n)
