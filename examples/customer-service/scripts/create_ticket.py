#!/usr/bin/env python3
"""工单创建脚本 - ASUI 智能客服验证"""
import json
import sys
from pathlib import Path
from datetime import datetime

DB_DIR = Path(__file__).parent.parent / "database"
TICKETS_FILE = DB_DIR / "tickets.json"


def main():
    data = json.load(sys.stdin)
    DB_DIR.mkdir(exist_ok=True)

    tickets = []
    if TICKETS_FILE.exists():
        tickets = json.loads(TICKETS_FILE.read_text(encoding="utf-8"))

    ticket_id = f"T{len(tickets) + 1:04d}"
    ticket = {
        "ticket_id": ticket_id,
        "user_input": data.get("user_input", ""),
        "intent": data.get("intent", "unknown"),
        "assigned_to": _get_assigned_group(data.get("intent")),
        "priority": _get_priority(data.get("intent")),
        "created_at": datetime.now().isoformat(),
        "status": "created",
    }
    tickets.append(ticket)
    TICKETS_FILE.write_text(json.dumps(tickets, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"ticket_id": ticket_id, "status": "created"}))


def _get_assigned_group(intent: str) -> str:
    mapping = {"technical": "技术组", "refund": "客服主管", "complaint": "升级处理"}
    return mapping.get(intent, "客服组")


def _get_priority(intent: str) -> str:
    mapping = {"refund": "P0", "complaint": "P0", "technical": "P1"}
    return mapping.get(intent, "P2")


if __name__ == "__main__":
    main()
