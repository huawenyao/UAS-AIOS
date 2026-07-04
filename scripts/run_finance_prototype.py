#!/usr/bin/env python3
"""L3 财务开票审批原型：cs.approval.submit + cs.process.start。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.connectors.router import CapabilityInvokeContext, CapabilityServiceRouter  # noqa: E402


def main() -> int:
    router = CapabilityServiceRouter(ROOT)
    ctx = CapabilityInvokeContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        role_ids=["role.finance"],
        product_track="pipaw",
    )
    proc = router.invoke(
        "cs.process.start",
        {
            "template_id": "finance_invoice_approval",
            "business_key": "INV-2026-0604-001",
            "variables": {"amount": 12800, "vendor": "ACME Supplier"},
        },
        ctx,
    )
    appr = router.invoke(
        "cs.approval.submit",
        {
            "template_id": "expense_reimbursement",
            "payload": {"invoice_id": "INV-2026-0604-001", "amount": 12800},
        },
        ctx,
    )
    out = {
        "status": "completed" if proc.status == "ok" and appr.status == "ok" else "failed",
        "process": {"status": proc.status, "output": proc.output},
        "approval": {"status": appr.status, "output": appr.output},
        "business_closed_loop": proc.status == "ok" and appr.status == "ok",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["business_closed_loop"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
