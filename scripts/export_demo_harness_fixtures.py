#!/usr/bin/env python3
"""导出 Harness 运行时 fixtures 供 ΠPaw Demo 静态加载（对齐 intent_hub + task_panel）。"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = REPO_ROOT / "docs" / "strategic" / "demo" / "fixtures"
sys.path.insert(0, str(REPO_ROOT / "asui-cli" / "src"))

from asui.intent_hub import EscalateContext, IntentEscalationHub  # noqa: E402
from asui.pipaw_task_panel import PipawTaskPanel  # noqa: E402


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def export_fixtures() -> dict:
    intent_path = REPO_ROOT / "configs" / "intent_samples" / "complaint_escalation.sample.json"
    intent = json.loads(intent_path.read_text(encoding="utf-8"))

    hub = IntentEscalationHub(REPO_ROOT)
    hub.reset_store()
    panel = PipawTaskPanel(REPO_ROOT)
    panel.reset_session()

    ctx = EscalateContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        user_id=intent["actor"]["user_id"],
        product_track="selfpaw",
    )
    esc = hub.escalate(intent, ctx)
    if esc.status != "ok" or not esc.working_task:
        raise SystemExit(f"escalate failed: {esc.deny_reason}")

    view = panel.build_view(tenant_id="t-acme-demo")
    panel.open_task(esc.working_task["task_id"])
    view_open = panel.build_view(tenant_id="t-acme-demo")

    roster = json.loads(
        (REPO_ROOT / "configs" / "pipaw_business_agent_roster.json").read_text(encoding="utf-8")
    )
    cs_playbook = json.loads(
        (REPO_ROOT / "configs" / "pipaw_cs_agent_playbook.json").read_text(encoding="utf-8")
    )
    sales_playbook = json.loads(
        (REPO_ROOT / "configs" / "pipaw_sales_agent_playbook.json").read_text(encoding="utf-8")
    )
    outward_routes = json.loads(
        (REPO_ROOT / "configs" / "outward_gateway_routes.sample.json").read_text(encoding="utf-8")
    )

    manifest = {
        "version": "1.0.0",
        "exported_at": _utc_now(),
        "source": "scripts/export_demo_harness_fixtures.py",
        "validate_cmd": "python scripts/validate_pipaw_cs_agent.py validate",
    }

    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "manifest.json": manifest,
        "intent_complaint.json": intent,
        "escalate_response.json": {
            "status": esc.status,
            "working_task": esc.working_task,
            "intent": esc.intent,
            "audit_id": esc.audit_id,
            "deny_reason": esc.deny_reason,
        },
        "task_panel_backlog.json": view,
        "task_panel_current.json": view_open,
        "roster.json": roster,
        "playbook_cs.json": cs_playbook,
        "playbook_sales.json": sales_playbook,
        "outward_routes.json": outward_routes,
    }
    for name, data in files.items():
        (FIXTURES_DIR / name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return {"fixtures_dir": str(FIXTURES_DIR), "files": list(files.keys()), "task_id": esc.working_task["task_id"]}


def main() -> int:
    info = export_fixtures()
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
