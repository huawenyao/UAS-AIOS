"""REQ-EDH-PP-001：ΠPaw 客服标杆 Agent 与 Task Panel。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "asui-cli" / "src"))

from asui.intent_hub import EscalateContext, IntentEscalationHub  # noqa: E402
from asui.pipaw_cs_agent import PipawCsAgentRuntime  # noqa: E402
from asui.pipaw_task_panel import PipawTaskPanel  # noqa: E402

SAMPLE = ROOT / "configs" / "intent_samples" / "complaint_escalation.sample.json"
ROSTER = ROOT / "configs" / "pipaw_business_agent_roster.json"


@pytest.fixture
def fresh_hub():
    hub = IntentEscalationHub(ROOT)
    hub.reset_store()
    yield hub
    hub.reset_store()


def test_roster_single_cs_agent():
    roster = json.loads(ROSTER.read_text(encoding="utf-8"))
    cs = [a for a in roster["agents"] if a["agent_id"] == "agent.cs_specialist"]
    assert len(cs) == 1
    ops = set(cs[0]["bound_operations"])
    assert "cs.ticket.escalate" in ops
    assert cs[0]["narrative_aliases"]["cs.escalate"] == "cs.ticket.escalate"


def test_panel_task_states_not_logs(fresh_hub):
    intent = json.loads(SAMPLE.read_text(encoding="utf-8"))
    fresh_hub.escalate(
        intent,
        EscalateContext(
            tenant_id="t-acme-demo",
            request_tenant_id="t-acme-demo",
            user_id="u-employee-1001",
            product_track="selfpaw",
        ),
    )
    panel = PipawTaskPanel(ROOT)
    view = panel.build_view(tenant_id="t-acme-demo")
    assert view["backlog"]
    item = view["backlog"][0]
    assert "status" in item and "steps" in item
    assert isinstance(item["steps"], list)


def test_open_current_and_run_profile_step(fresh_hub):
    intent = json.loads(SAMPLE.read_text(encoding="utf-8"))
    resp = fresh_hub.escalate(
        intent,
        EscalateContext(
            tenant_id="t-acme-demo",
            request_tenant_id="t-acme-demo",
            user_id="u-employee-1001",
            product_track="selfpaw",
        ),
    )
    panel = PipawTaskPanel(ROOT)
    panel.open_task(resp.working_task["task_id"])
    view = panel.build_view(tenant_id="t-acme-demo")
    assert view["current"]["display_phase"] == "current"

    runtime = PipawCsAgentRuntime(ROOT)
    runtime.panel.open_task(resp.working_task["task_id"])
    result = runtime.run_current_step()
    assert result.status == "ok"
    assert result.operation_ref == "cs.customer.get_profile"
