#!/usr/bin/env python3
"""调用 cs.* 能力服务（经 mock 连接器）。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ASUI_SRC = REPO_ROOT / "asui-cli" / "src"
sys.path.insert(0, str(ASUI_SRC))

from asui.connectors import CapabilityInvokeContext, CapabilityServiceRouter  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="列出能力服务")
    p_list.set_defaults(func=lambda _a: _cmd_list())

    p_inv = sub.add_parser("invoke", help="调用能力")
    p_inv.add_argument("operation_ref", help="如 cs.lead.qualify_lead")
    p_inv.add_argument("--payload-json", default="{}")
    p_inv.add_argument("--tenant", default="t-acme-demo")
    p_inv.add_argument("--user", default="u-demo")
    p_inv.add_argument("--roles", default="role.sales_rep")
    p_inv.add_argument("--track", default="selfpaw", choices=["selfpaw", "pipaw"])
    p_inv.set_defaults(func=_cmd_invoke)

    args = parser.parse_args()
    return args.func(args)


def _cmd_list() -> int:
    router = CapabilityServiceRouter(REPO_ROOT)
    print(json.dumps(router.list_services(), ensure_ascii=False, indent=2))
    return 0


def _cmd_invoke(args: argparse.Namespace) -> int:
    router = CapabilityServiceRouter(REPO_ROOT)
    payload = json.loads(args.payload_json)
    ctx = CapabilityInvokeContext(
        tenant_id=args.tenant,
        request_tenant_id=args.tenant,
        user_id=args.user,
        role_ids=[r.strip() for r in args.roles.split(",") if r.strip()],
        product_track=args.track,
    )
    resp = router.invoke(args.operation_ref, payload, ctx)
    print(json.dumps(resp.__dict__, ensure_ascii=False, indent=2))
    return 0 if resp.status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
