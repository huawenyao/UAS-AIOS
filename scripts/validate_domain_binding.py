#!/usr/bin/env python3
"""校验 REQ-EDH-SP-002 岗位 Domain 绑定原型。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.domain_binding import DomainBindingLoader  # noqa: E402

REQUIRED_CODES = ("SALES_REP", "CS_AGENT", "HR_GENERALIST", "RD_ENGINEER")


def validate() -> dict:
    path = ROOT / "configs" / "role_domain_bindings.json"
    if not path.is_file():
        return {"status": "error", "missing": str(path)}

    catalog = json.loads(path.read_text(encoding="utf-8"))
    bindings = catalog.get("bindings", [])
    codes = {b.get("position_code") for b in bindings}
    missing = [c for c in REQUIRED_CODES if c not in codes]
    if missing:
        return {"status": "error", "missing_positions": missing}

    loader = DomainBindingLoader(ROOT)
    samples = {}
    for code in REQUIRED_CODES:
        frag = loader.bind_by_position_code(code)
        if not frag or not frag.capability_whitelist:
            return {"status": "error", "reason": f"empty_binding:{code}"}
        samples[code] = {
            "domain_id": frag.domain_id,
            "ops_count": len(frag.capability_whitelist),
        }

    return {"status": "ok", "bindings": len(bindings), "samples": samples}


def main() -> int:
    out = validate()
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
