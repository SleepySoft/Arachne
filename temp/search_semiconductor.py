import json
import urllib.request
import time

BASE = "http://127.0.0.1:10086/command"
SESSION = "semiconductor-company-research"


def send(action: str, args: dict):
    payload = {
        "action": action,
        "args": args,
        "session": SESSION,
    }
    req = urllib.request.Request(
        BASE,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    # Navigate to Google search
    print("Navigating to Google search...")
    result = send("navigate", {
        "url": "https://www.google.com/search?q=A股半导体上市公司名单 东方财富",
        "newTab": True,
        "group_title": "半导体公司调研"
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    time.sleep(3)

    # Take snapshot
    print("\nTaking snapshot...")
    snapshot = send("snapshot", {})
    print(json.dumps(snapshot, ensure_ascii=False, indent=2)[:4000])


if __name__ == "__main__":
    main()
