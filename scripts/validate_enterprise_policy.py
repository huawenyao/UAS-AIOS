#!/usr/bin/env python3
"""校验企业租户目录与 RBAC 模板；执行租户隔离策略用例。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TENANT_CATALOG = REPO_ROOT / "configs" / "tenant_catalog.sample.json"
RBAC_TEMPLATE = REPO_ROOT / "configs" / "enterprise_rbac_template.json"
CAPABILITY_REGISTRY = REPO_ROOT / "configs" / "capability_registry.json"
OP_REF_RE = re.compile(r"^cs\.[a-z][a-z0-9_.]+\.[a-z][a-z0-9_]*$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def registry_operations(registry: dict) -> set[str]:
    ops: set[str] = set()
    for svc in registry.get("services", []):
        sid = svc["id"]
        for op in svc.get("operations", []):
            ops.add(f"{sid}.{op['name']}")
    return ops


def validate_tenant_catalog(catalog: dict) -> list[str]:
    errors: list[str] = []
    tenants = catalog.get("tenants", [])
    if not tenants:
        errors.append("no tenants")
    for t in tenants:
        tid = t.get("tenant_id", "")
        if not tid.startswith("t-"):
            errors.append(f"invalid tenant_id: {tid}")
        if not t.get("org_units") or not t.get("positions"):
            errors.append(f"{tid}: org_units/positions required")
    return errors


def validate_rbac(rbac: dict, known_ops: set[str]) -> list[str]:
    errors: list[str] = []
    if not rbac.get("approval_gate_mapping", {}).get("L1"):
        errors.append("missing L1 mapping")
    for role in rbac.get("roles", []):
        for op in role.get("allowed_operations", []):
            if not OP_REF_RE.match(op):
                errors.append(f"{role['role_id']}: bad op ref {op}")
            elif op not in known_ops:
                errors.append(f"{role['role_id']}: unknown op {op} (not in capability_registry)")
    return errors


def check_tenant_isolation() -> list[str]:
    """跨租户与轨道越权用例（纯逻辑，无 HTTP）。"""
    errors: list[str] = []

    def authorize(
        *,
        ctx_tenant: str,
        request_tenant: str,
        product_track: str,
        role_id: str,
        operation_ref: str,
        rbac: dict,
    ) -> str | None:
        if ctx_tenant != request_tenant:
            return "TENANT_ISOLATION_VIOLATION"
        roles = {r["role_id"]: r for r in rbac.get("roles", [])}
        role = roles.get(role_id)
        if not role:
            return "ROLE_NOT_FOUND"
        if role.get("product_track") not in (product_track, "shared"):
            return "PRODUCT_TRACK_DENIED"
        if operation_ref not in role.get("allowed_operations", []):
            return "OPERATION_DENIED"
        if operation_ref in role.get("denied_operations", []):
            return "OPERATION_DENIED"
        return None

    rbac = load(RBAC_TEMPLATE)

    # 用例 1：跨租户
    if authorize(
        ctx_tenant="t-acme-demo",
        request_tenant="t-other-corp",
        product_track="selfpaw",
        role_id="role.sales_rep",
        operation_ref="cs.lead.list",
        rbac=rbac,
    ) != "TENANT_ISOLATION_VIOLATION":
        errors.append("case1: expected TENANT_ISOLATION_VIOLATION")

    # 用例 2：pipaw 角色用 selfpaw 轨道
    if authorize(
        ctx_tenant="t-acme-demo",
        request_tenant="t-acme-demo",
        product_track="selfpaw",
        role_id="role.cs_agent",
        operation_ref="cs.ticket.create",
        rbac=rbac,
    ) != "PRODUCT_TRACK_DENIED":
        errors.append("case2: expected PRODUCT_TRACK_DENIED")

    # 用例 3：合法调用
    if authorize(
        ctx_tenant="t-acme-demo",
        request_tenant="t-acme-demo",
        product_track="pipaw",
        role_id="role.cs_agent",
        operation_ref="cs.ticket.create",
        rbac=rbac,
    ) is not None:
        errors.append("case3: expected success")

    # 用例 4：员工不能 approve
    if authorize(
        ctx_tenant="t-acme-demo",
        request_tenant="t-acme-demo",
        product_track="selfpaw",
        role_id="role.employee",
        operation_ref="cs.approval.approve",
        rbac=rbac,
    ) != "OPERATION_DENIED":
        errors.append("case4: expected OPERATION_DENIED")

    return errors


def cmd_validate() -> int:
    errors: list[str] = []
    if not TENANT_CATALOG.is_file():
        errors.append("missing tenant_catalog.sample.json")
    else:
        errors.extend(validate_tenant_catalog(load(TENANT_CATALOG)))
    if not RBAC_TEMPLATE.is_file():
        errors.append("missing enterprise_rbac_template.json")
    else:
        known = registry_operations(load(CAPABILITY_REGISTRY)) if CAPABILITY_REGISTRY.is_file() else set()
        errors.extend(validate_rbac(load(RBAC_TEMPLATE), known))
    errors.extend(check_tenant_isolation())
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print("OK: enterprise tenant + RBAC + isolation cases")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate"])
    args = parser.parse_args()
    if args.command == "validate":
        return cmd_validate()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
