#!/usr/bin/env python3
"""将审计事件追加到 database/audit/（MVP 占位实现）。"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {"events": []}
    root = Path(__file__).resolve().parents[1]
    audit_dir = root / "database" / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "events": payload.get("events", payload if isinstance(payload, list) else []),
    }
    out = audit_dir / f"audit_{record['recorded_at'].replace(':', '-')}.json"
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ok", "path": str(out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
