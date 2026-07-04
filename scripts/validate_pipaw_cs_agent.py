#!/usr/bin/env python3
"""REQ-EDH-PP-001：客服岗位 Agent 标杆 — Roster、能力绑定、Task Panel、E2E。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROSTER = REPO_ROOT / "configs" / "pipaw_business_agent_roster.json"
PLAYBOOK = REPO_ROOT / "configs" / "pipaw_cs_agent_playbook.json"
REGISTRY = REPO_ROOT / "configs" / "capability_registry.json"
INTENT_SAMPLE = REPO_ROOT / "configs" / "intent_samples" / "complaint_escalation.sample.json"
DEMO_HTML = REPO_ROOT / "docs" / "strategic" / "demo" / "ΠPaw_Enterprise_Demo.html"

REQUIRED_OPS = frozenset(
    {
        "cs.customer.get_profile",
        "cs.ticket.create",
        "cs.ticket.escalate",
    }
)
NARRATIVE_ALIASES = {"cs.customer", "cs.ticket", "cs.escalate"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def registry_operations(registry: dict) -> set[str]:
    ops: set[str] = set()
    for svc in registry.get("services", []):
        sid = svc["id"]
        for op in svc.get("operations", []):
            ops.add(f"{sid}.{op['name']}")
    return ops


def validate_roster(roster: dict, known_ops: set[str]) -> list[str]:
    errors: list[str] = []
    agents = roster.get("agents", [])
    cs_agents = [a for a in agents if a.get("agent_id") == "agent.cs_specialist"]
    if len(cs_agents) != 1:
        errors.append(f"expected 1 agent.cs_specialist, got {len(cs_agents)}")
        return errors
    agent = cs_agents[0]
    bound = set(agent.get("bound_operations", []))
    if bound != REQUIRED_OPS:
        errors.append(f"bound_operations mismatch: {bound} vs {REQUIRED_OPS}")
    missing = bound - known_ops
    if missing:
        errors.append(f"unknown ops in roster: {missing}")
    aliases = agent.get("narrative_aliases") or {}
    if not NARRATIVE_ALIASES.issubset(set(aliases.keys())):
        errors.append(f"narrative_aliases missing keys: {NARRATIVE_ALIASES - set(aliases.keys())}")
    for key, ref in aliases.items():
        if ref not in known_ops:
            errors.append(f"alias {key} -> {ref} not in registry")
    if not agent.get("demo_reference") or "ΠPaw" not in agent.get("demo_reference", ""):
        errors.append("demo_reference must cite ΠPaw Enterprise Demo")
    return errors


def validate_panel_shape(view: dict) -> list[str]:
    errors: list[str] = []
    for key in ("summary", "backlog", "current"):
        if key not in view:
            errors.append(f"panel missing {key}")
    if "summary" in view and "backlog_count" not in view["summary"]:
        errors.append("panel summary missing backlog_count")
    items = list(view.get("backlog", []))
    if view.get("current"):
        items.append(view["current"])
    if not items:
        errors.append("panel has no task items")
    for item in items:
        for field in ("status", "display_phase", "title", "steps"):
            if field not in item:
                errors.append(f"panel item missing {field}")
        if "log" in json.dumps(item, ensure_ascii=False).lower() and "steps" not in item:
            errors.append("panel must use task state not raw logs")
        if not isinstance(item.get("steps"), list) or not item["steps"]:
            errors.append(f"item {item.get('item_id')} missing structured steps")
    return errors


def run_e2e() -> list[str]:
    errors: list[str] = []
    sys.path.insert(0, str(REPO_ROOT / "asui-cli" / "src"))
    from asui.intent_hub import EscalateContext, IntentEscalationHub
    from asui.pipaw_cs_agent import PipawCsAgentRuntime
    from asui.pipaw_task_panel import PipawTaskPanel

    hub = IntentEscalationHub(REPO_ROOT)
    hub.reset_store()
    panel = PipawTaskPanel(REPO_ROOT)
    panel.reset_session()

    intent = load(INTENT_SAMPLE)
    ctx = EscalateContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        user_id=intent["actor"]["user_id"],
        product_track="selfpaw",
    )
    esc = hub.escalate(intent, ctx)
    if esc.status != "ok" or not esc.working_task:
        return [f"intent escalate failed: {esc.deny_reason}"]

    view = panel.build_view(tenant_id="t-acme-demo")
    errors.extend(validate_panel_shape(view))
    if view["summary"]["backlog_count"] < 1:
        errors.append("backlog empty after escalation")

    task_id = esc.working_task["task_id"]
    panel.open_task(task_id)
    view2 = panel.build_view(tenant_id="t-acme-demo")
    if not view2.get("current"):
        errors.append("current task not set after open")
    elif view2["current"]["display_phase"] != "current":
        errors.append("current item wrong display_phase")
    elif view2["current"]["status"] != "in_progress":
        errors.append("current task status should be in_progress")

    runtime = PipawCsAgentRuntime(REPO_ROOT)
    runtime.panel.open_task(task_id)
    step1 = runtime.run_current_step()
    if step1.status != "ok" or step1.operation_ref != "cs.customer.get_profile":
        errors.append(f"step1 failed: {step1.status} {step1.deny_reason}")

    hub.reset_store()
    panel.reset_session()
    return errors


def cmd_validate() -> int:
    errs: list[str] = []
    if not DEMO_HTML.is_file():
        errs.append("missing ΠPaw_Enterprise_Demo.html")
    if not ROSTER.is_file():
        errs.append("missing pipaw_business_agent_roster.json")
    else:
        known = registry_operations(load(REGISTRY))
        errs.extend(validate_roster(load(ROSTER), known))
    if not PLAYBOOK.is_file():
        errs.append("missing pipaw_cs_agent_playbook.json")
    for name in ("business_agent_roster.schema.json", "task_panel_view.schema.json"):
        if not (REPO_ROOT / "schemas" / name).is_file():
            errs.append(f"missing schemas/{name}")
    errs.extend(run_e2e())
    if errs:
        for e in errs:
            print(f"ERROR: {e}")
        return 1
    print("OK: pipaw cs agent roster + task panel + E2E escalate→handle")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate"], nargs="?", default="validate")
    args = parser.parse_args()
    if args.command == "validate":
        return cmd_validate()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
