#!/usr/bin/env python3
"""校验连接器配置并执行 CRM/OA mock 冒烟用例。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ASUI_SRC = REPO_ROOT / "asui-cli" / "src"
sys.path.insert(0, str(ASUI_SRC))

from asui.connectors import CapabilityInvokeContext, CapabilityServiceRouter  # noqa: E402

CONNECTORS_PATH = REPO_ROOT / "configs" / "connectors.json"
CRM_OPS = {"cs.customer.get_profile", "cs.customer.query", "cs.lead.qualify_lead", "cs.lead.list"}
OA_OPS = {"cs.approval.submit", "cs.notify.send_im"}


def validate_config() -> list[str]:
    errors: list[str] = []
    if not CONNECTORS_PATH.is_file():
        return ["missing configs/connectors.json"]
    cfg = json.loads(CONNECTORS_PATH.read_text(encoding="utf-8"))
    connectors = cfg.get("connectors", [])
    types = {c.get("type") for c in connectors}
    if "crm" not in types or "oa" not in types:
        errors.append("need crm and oa connector types")
    for c in connectors:
        if not c.get("secret_ref", "").startswith(("env:", "file:")):
            errors.append(f"{c.get('id')}: secret_ref must use env: or file: prefix")
    return errors


def smoke_invoke() -> list[str]:
    errors: list[str] = []
    router = CapabilityServiceRouter(REPO_ROOT)
    ctx = CapabilityInvokeContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        user_id="u-1001",
        role_ids=["role.sales_rep"],
        product_track="selfpaw",
    )

    r1 = router.invoke("cs.customer.get_profile", {"customer_id": "C-1001"}, ctx)
    if r1.status != "ok":
        errors.append(f"crm get_profile: {r1.deny_reason or r1.status}")

    r2 = router.invoke("cs.lead.qualify_lead", {"lead_id": "L-1001"}, ctx)
    if r2.status != "ok" or not r2.output.get("qualified"):
        errors.append(f"crm qualify_lead: {r2}")

    ctx_oa = CapabilityInvokeContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        user_id="u-cs",
        role_ids=["role.cs_agent"],
        product_track="pipaw",
    )
    r3 = router.invoke(
        "cs.approval.submit",
        {"template_id": "expense", "payload": {"amount": 100}},
        ctx_oa,
    )
    if r3.status != "ok":
        errors.append(f"oa submit: {r3}")

    r4 = router.invoke(
        "cs.notify.send_im",
        {"recipient_id": "u-1001", "body": "hello", "channel": "feishu"},
        ctx_oa,
    )
    if r4.status != "ok":
        errors.append(f"oa send_im: {r4}")

    return errors


def cmd_matrix() -> int:
    router = CapabilityServiceRouter(REPO_ROOT)
    registry = json.loads((REPO_ROOT / "configs" / "capability_registry.json").read_text(encoding="utf-8"))
    for svc in registry.get("services", []):
        cid = svc.get("connector_id", "")
        for op in svc.get("operations", []):
            print(f"{svc['id']}.{op['name']} -> {cid}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate", "matrix"])
    args = parser.parse_args()
    if args.command == "matrix":
        return cmd_matrix()
    errors = validate_config() + smoke_invoke()
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print("OK: connectors config + CRM/OA mock smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
