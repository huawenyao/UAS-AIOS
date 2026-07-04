#!/usr/bin/env python3
"""校验企业世界模型五维与法则包（REQ-EDH-PP-003）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_DIMS = ("space", "time", "subject", "object", "feedback")
REQUIRED_IDENTITIES = ("mirror", "lens", "furnace")


def validate(workspace: Path) -> list[str]:
    errors: list[str] = []
    sample = workspace / "configs" / "enterprise_world_model.sample.json"
    sales_wm = workspace / "projects" / "enterprise-sales-os" / "configs" / "world_model.json"
    for path in (sample, sales_wm):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(workspace)}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        dims = data.get("dimensions", {})
        for d in REQUIRED_DIMS:
            if d not in dims:
                errors.append(f"{path.name}: missing dimension {d}")
        ids = data.get("identities", {})
        for i in REQUIRED_IDENTITIES:
            if i not in ids:
                errors.append(f"{path.name}: missing identity {i}")
        laws = data.get("law_pack") or []
        if path == sample and len(laws) < 3:
            errors.append("sample law_pack need >= 3 entries")
    law_pack = workspace / "projects" / "enterprise-sales-os" / "configs" / "cs_law_pack.sample.json"
    if not law_pack.is_file():
        errors.append("missing cs_law_pack.sample.json")
    return errors


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] != "validate":
        print("Usage: validate_enterprise_wm.py validate", file=sys.stderr)
        return 2
    workspace = Path(__file__).resolve().parents[1]
    errors = validate(workspace)
    if errors:
        print(json.dumps({"status": "fail", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "ok"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
