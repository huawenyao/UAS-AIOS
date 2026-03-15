#!/usr/bin/env python3
"""通过 Cases 静态资源 API 部署 website 到 /data/cases。"""
import json
import sys
from pathlib import Path

try:
    import urllib.request
    import urllib.error
except ImportError:
    import urllib2 as urllib  # type: ignore
    urllib.request = urllib
    urllib.error = urllib

REPO_ROOT = Path(__file__).resolve().parent.parent
WEBSITE_DIR = REPO_ROOT / "website"
BASE_URL = "http://cases.wumaitech.com:8081"
API_KEY = "249e29ee68730d28ed32d229c448f16c"

FILES = ["index.html", "styles.css"]


def write_file(path: str, content: str, overwrite: bool = True) -> dict:
    url = f"{BASE_URL}/api/write"
    data = json.dumps({"path": path, "content": content, "overwrite": overwrite}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return {"status": r.status, "body": r.read().decode()}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": e.read().decode() if e.fp else ""}
    except Exception as e:
        return {"status": -1, "body": str(e)}


def main():
    for name in FILES:
        path = WEBSITE_DIR / name
        if not path.is_file():
            print(f"Skip (not found): {name}")
            continue
        content = path.read_text(encoding="utf-8")
        print(f"Uploading {name} ...", end=" ")
        result = write_file(name, content)
        if 200 <= result["status"] < 300:
            print("OK")
        else:
            print(f"FAIL {result['status']}\n{result['body']}")
            sys.exit(1)
    print(f"Done. Visit: {BASE_URL}/")


if __name__ == "__main__":
    main()
