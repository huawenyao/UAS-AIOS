#!/usr/bin/env python3
"""校验 REQ-EDH-SP-001 组织身份绑定原型。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.org_identity import OrgIdentityResolver, OrgSessionRequest  # noqa: E402


def validate() -> dict:
    for name in (
        "configs/selfpaw_enterprise.feature_flags.json",
        "configs/tenant_catalog.sample.json",
        "configs/enterprise_rbac_template.json",
    ):
        if not (ROOT / name).is_file():
            return {"status": "error", "missing": name}

    resolver = OrgIdentityResolver(ROOT)
    ctx = resolver.resolve(
        OrgSessionRequest(
            tenant_id="t-acme-demo",
            user_id="u-employee-1001",
            position_id="pos-sales-rep",
        )
    )
    if ctx.status != "ok":
        return {"status": "error", "reason": ctx.deny_reason}
    if not ctx.domain_id or not ctx.role_ids:
        return {"status": "error", "reason": "incomplete_context"}
    return {
        "status": "ok",
        "tenant_id": ctx.tenant_id,
        "position_code": ctx.position_code,
        "domain_id": ctx.domain_id,
        "role_ids": ctx.role_ids,
    }


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        out = validate()
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if out.get("status") == "ok" else 1
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
