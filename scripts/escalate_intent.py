#!/usr/bin/env python3
"""CLI：从样例或 JSON 文件升级 Intent 为 ΠPaw Working Task。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "asui-cli" / "src"))

from asui.intent_hub import EscalateContext, IntentEscalationHub


def main() -> int:
    parser = argparse.ArgumentParser(description="Intent Hub escalate (Phase-0)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="列出 ΠPaw Working Tasks")
    p_list.add_argument("--tenant-id", default="t-acme-demo")
    p_list.add_argument("--position-id", default=None)
    p_list.add_argument("--role-id", default=None)

    p_esc = sub.add_parser("escalate", help="升级 Intent")
    p_esc.add_argument(
        "--intent-file",
        default=str(REPO_ROOT / "configs" / "intent_samples" / "complaint_escalation.sample.json"),
    )
    p_esc.add_argument("--tenant-id", default="t-acme-demo")
    p_esc.add_argument("--user-id", default="u-employee-1001")

    args = parser.parse_args()
    hub = IntentEscalationHub(REPO_ROOT)

    if args.cmd == "list":
        tasks = hub.list_tasks(
            tenant_id=args.tenant_id,
            position_id=args.position_id,
            assignee_role_id=args.role_id,
        )
        print(json.dumps(tasks, ensure_ascii=False, indent=2))
        return 0

    intent = json.loads(Path(args.intent_file).read_text(encoding="utf-8"))
    ctx = EscalateContext(
        tenant_id=args.tenant_id,
        request_tenant_id=args.tenant_id,
        user_id=args.user_id,
        product_track="selfpaw",
    )
    resp = hub.escalate(intent, ctx)
    print(json.dumps({"status": resp.status, "working_task": resp.working_task, "deny_reason": resp.deny_reason}, ensure_ascii=False, indent=2))
    return 0 if resp.status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
