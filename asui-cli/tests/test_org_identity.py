"""REQ-EDH-SP-001 / SP-002 原型测试。"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.domain_binding import DomainBindingLoader  # noqa: E402
from asui.org_identity import OrgIdentityResolver, OrgSessionRequest  # noqa: E402


def test_org_identity_resolves_sales_rep():
    r = OrgIdentityResolver(ROOT)
    ctx = r.resolve(
        OrgSessionRequest(
            tenant_id="t-acme-demo",
            user_id="u-employee-1001",
            position_id="pos-sales-rep",
        )
    )
    assert ctx.status == "ok"
    assert ctx.domain_id == "domain.sales"
    assert ctx.role_ids


def test_domain_binding_four_positions():
    loader = DomainBindingLoader(ROOT)
    for code in ("SALES_REP", "CS_AGENT", "HR_GENERALIST", "RD_ENGINEER"):
        frag = loader.bind_by_position_code(code)
        assert frag is not None
        assert frag.capability_whitelist
