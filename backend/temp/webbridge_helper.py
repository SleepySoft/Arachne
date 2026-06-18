import json
import sys
import urllib.request

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


if __name__ == "__main__":
    action = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = send(action, args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
