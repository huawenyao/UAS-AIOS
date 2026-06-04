"""REQ-EDH-SP-003：Intent 升级 ΠPaw Working Task。"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.intent_hub import EscalateContext, IntentEscalationHub  # noqa: E402
SAMPLE = ROOT / "configs" / "intent_samples" / "complaint_escalation.sample.json"


@pytest.fixture
def hub():
    h = IntentEscalationHub(ROOT)
    h.reset_store()
    yield h
    h.reset_store()


def _load_intent():
    import json

    return json.loads(SAMPLE.read_text(encoding="utf-8"))


def test_business_outward_escalate_creates_cs_task(hub):
    intent = _load_intent()
    ctx = EscalateContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        user_id="u-employee-1001",
        product_track="selfpaw",
    )
    resp = hub.escalate(intent, ctx)
    assert resp.status == "ok"
    assert resp.working_task["position_id"] == "pos-cs-agent"
    visible = hub.list_tasks(
        tenant_id="t-acme-demo",
        position_id="pos-cs-agent",
        assignee_role_id="role.cs_agent",
    )
    assert len(visible) == 1


def test_escalate_without_evidence_denied(hub):
    intent = _load_intent()
    intent["evidence_refs"] = []
    ctx = EscalateContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        user_id="u-employee-1001",
        product_track="selfpaw",
    )
    resp = hub.escalate(intent, ctx)
    assert resp.status == "denied"
    assert resp.deny_reason == "EVIDENCE_REQUIRED"


def test_cross_tenant_denied(hub):
    intent = _load_intent()
    ctx = EscalateContext(
        tenant_id="t-other",
        request_tenant_id="t-other",
        user_id="u-employee-1001",
        product_track="selfpaw",
    )
    resp = hub.escalate(intent, ctx)
    assert resp.status == "denied"
    assert resp.deny_reason == "TENANT_ISOLATION_VIOLATION"
