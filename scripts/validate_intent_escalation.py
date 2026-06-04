#!/usr/bin/env python3
"""校验 IntentObject / WorkingTask 契约；执行客诉升级 E2E 用例。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INTENT_SAMPLE = REPO_ROOT / "configs" / "intent_samples" / "complaint_escalation.sample.json"
POLICY = REPO_ROOT / "configs" / "intent_escalation_policy.sample.json"

INTENT_ID_RE = re.compile(r"^int-[a-z0-9-]+$")
TASK_ID_RE = re.compile(r"^wt-[a-z0-9-]+$")
INTENT_CLASSES = frozenset({"personal", "collaboration", "business_outward"})


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_intent_shape(intent: dict) -> list[str]:
    errors: list[str] = []
    for key in ("intent_id", "tenant_id", "intent_class", "goal", "actor", "status"):
        if key not in intent:
            errors.append(f"missing field: {key}")
    if intent.get("intent_id") and not INTENT_ID_RE.match(intent["intent_id"]):
        errors.append("bad intent_id pattern")
    ic = intent.get("intent_class")
    if ic not in INTENT_CLASSES:
        errors.append(f"bad intent_class: {ic}")
    if ic == "business_outward":
        if not intent.get("evidence_refs"):
            errors.append("business_outward requires evidence_refs")
        tgt = intent.get("escalation_target") or {}
        if tgt.get("product_track") != "pipaw":
            errors.append("business_outward escalation_target.product_track must be pipaw")
    actor = intent.get("actor") or {}
    if actor.get("product_track") != "selfpaw":
        errors.append("escalation actor must be selfpaw track")
    return errors


def validate_policy(policy: dict) -> list[str]:
    errors: list[str] = []
    classes = {r.get("intent_class") for r in policy.get("rules", [])}
    if classes != INTENT_CLASSES:
        errors.append(f"policy rules must cover {INTENT_CLASSES}, got {classes}")
    bo = next((r for r in policy.get("rules", []) if r.get("intent_class") == "business_outward"), None)
    if not bo or not bo.get("requires_evidence"):
        errors.append("business_outward rule must require evidence")
    return errors


def run_e2e_complaint() -> list[str]:
    """员工客诉 → ΠPaw 客服 Task 在 pos-cs-agent / role.cs_agent 可见。"""
    errors: list[str] = []
    sys.path.insert(0, str(REPO_ROOT / "asui-cli" / "src"))
    from asui.intent_hub import EscalateContext, IntentEscalationHub

    hub = IntentEscalationHub(REPO_ROOT)
    hub.reset_store()

    intent = load(INTENT_SAMPLE)
    shape_errs = validate_intent_shape(intent)
    if shape_errs:
        return shape_errs

    ctx = EscalateContext(
        tenant_id="t-acme-demo",
        request_tenant_id="t-acme-demo",
        user_id=intent["actor"]["user_id"],
        product_track="selfpaw",
        role_ids=["role.employee"],
    )
    resp = hub.escalate(intent, ctx)
    if resp.status != "ok" or not resp.working_task:
        errors.append(f"escalate failed: {resp.status} {resp.deny_reason}")
        return errors

    wt = resp.working_task
    if not TASK_ID_RE.match(wt.get("task_id", "")):
        errors.append("invalid working task_id")
    if wt.get("position_id") != "pos-cs-agent":
        errors.append(f"expected pos-cs-agent, got {wt.get('position_id')}")
    if wt.get("assignee_role_id") != "role.cs_agent":
        errors.append("expected role.cs_agent assignee")
    if wt.get("source") != "selfpaw_escalation":
        errors.append("bad task source")

    visible = hub.list_tasks(
        tenant_id="t-acme-demo",
        position_id="pos-cs-agent",
        assignee_role_id="role.cs_agent",
        status="open",
    )
    if not any(t["task_id"] == wt["task_id"] for t in visible):
        errors.append("ΠPaw CS task board: task not visible to cs_agent")

    hub.reset_store()
    return errors


def cmd_validate() -> int:
    errs: list[str] = []
    if not INTENT_SAMPLE.is_file():
        errs.append("missing intent sample")
    else:
        errs.extend(validate_intent_shape(load(INTENT_SAMPLE)))
    if POLICY.is_file():
        errs.extend(validate_policy(load(POLICY)))
    else:
        errs.append("missing intent_escalation_policy.sample.json")

    for name in ("intent_object.schema.json", "working_task.schema.json"):
        if not (REPO_ROOT / "schemas" / name).is_file():
            errs.append(f"missing schemas/{name}")

    errs.extend(run_e2e_complaint())

    if errs:
        for e in errs:
            print(f"ERROR: {e}")
        return 1
    print("OK: intent escalation contract + E2E complaint→cs_task")
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
