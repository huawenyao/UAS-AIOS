#!/usr/bin/env python3
"""PP-002 经营向外 Gateway 原型：路由 + cs.notify.send_im。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.connectors.router import CapabilityInvokeContext, CapabilityServiceRouter  # noqa: E402


def main() -> int:
    routes_path = ROOT / "configs" / "outward_gateway_routes.sample.json"
    routes = json.loads(routes_path.read_text(encoding="utf-8")) if routes_path.is_file() else {}
    channel = "im"
    route = next(
        (r for r in routes.get("routes", []) if r.get("channel") == channel),
        {"channel": channel, "handler": "cs.notify.send_im"},
    )

    router = CapabilityServiceRouter(ROOT)
    ctx = CapabilityInvokeContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        role_ids=["role.cs_agent"],
        product_track="pipaw",
    )
    resp = router.invoke(
        route.get("handler", "cs.notify.send_im"),
        {
            "recipient_id": "u-customer-9001",
            "body": "【ACME】您的客诉已受理，工单处理中。",
            "channel": "feishu",
        },
        ctx,
    )
    out = {
        "status": "completed" if resp.status == "ok" else "failed",
        "route": route,
        "notify": {"status": resp.status, "output": resp.output},
        "audit_required": True,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
