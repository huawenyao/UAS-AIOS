"""REQ-EDH-PL-007 连接器 mock 测试。"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.connectors import CapabilityInvokeContext, CapabilityServiceRouter  # noqa: E402


def test_crm_qualify_lead():
    router = CapabilityServiceRouter(ROOT)
    ctx = CapabilityInvokeContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        role_ids=["role.sales_rep"],
        product_track="selfpaw",
    )
    resp = router.invoke("cs.lead.qualify_lead", {"lead_id": "L-1001"}, ctx)
    assert resp.status == "ok"
    assert resp.output.get("qualified") is True


def test_oa_approval_submit():
    router = CapabilityServiceRouter(ROOT)
    ctx = CapabilityInvokeContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        role_ids=["role.cs_agent"],
        product_track="pipaw",
    )
    resp = router.invoke(
        "cs.approval.submit",
        {"template_id": "t1", "payload": {}},
        ctx,
    )
    assert resp.status == "ok"
    assert "approval_id" in resp.output


def test_cross_tenant_denied():
    router = CapabilityServiceRouter(ROOT)
    ctx = CapabilityInvokeContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-other",
        role_ids=["role.sales_rep"],
        product_track="selfpaw",
    )
    resp = router.invoke("cs.lead.list", {}, ctx)
    assert resp.status == "denied"
    assert resp.deny_reason == "TENANT_ISOLATION_VIOLATION"
