#!/usr/bin/env python3
"""Runtime simulation 步：委托平台 value_loop_snapshot。"""

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    payload = json.load(sys.stdin)
    root = Path(__file__).resolve().parents[3]
    script = root / "scripts" / "value_loop_snapshot.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        encoding="utf-8",
        capture_output=True,
        cwd=root,
        check=True,
    )
    print(result.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
