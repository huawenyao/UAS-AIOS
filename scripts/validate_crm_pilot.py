#!/usr/bin/env python3
"""校验 C-05 CRM 试点契约原型。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate() -> dict:
    pilot = ROOT / "configs" / "crm_pilot.sample.json"
    connectors = ROOT / "configs" / "connectors.json"
    if not pilot.is_file() or not connectors.is_file():
        return {"status": "error", "missing": "crm_pilot or connectors"}
    data = json.loads(pilot.read_text(encoding="utf-8"))
    conn = json.loads(connectors.read_text(encoding="utf-8"))
    cid = data.get("connector_id")
    found = any(c.get("id") == cid for c in conn.get("connectors", []))
    if not found:
        return {"status": "error", "reason": "connector_not_in_registry"}
    return {
        "status": "ok",
        "pilot_id": data.get("pilot_id"),
        "connector_id": cid,
        "capabilities": data.get("capabilities", []),
    }


def main() -> int:
    out = validate()
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
