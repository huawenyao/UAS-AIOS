#!/usr/bin/env python3
"""价值闭环：模拟快照 + 收益指标草案（步骤 2 / 7）。"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def snapshot(payload: dict) -> dict:
    sales = payload.get("sales_result", {})
    approval = sales.get("approval") or payload.get("approval")
    metrics = {
        "cycle_time_minutes": payload.get("cycle_time_minutes", 0),
        "approval_pass_rate": 1.0 if approval in ("not_required", "approved") else 0.0,
        "evidence_block_rate": 1.0 if sales.get("business_code") == "EVIDENCE_REQUIRED" else 0.0,
        "mvp_passed": bool(sales.get("passed")),
    }
    revenue = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "topic": payload.get("topic", ""),
        "metrics": metrics,
        "revenue_feedback_ready": True,
        "note": "收益反哺 evolution 可读 value_metrics.sample.json",
    }
    return {
        "simulation_status": "completed",
        "value_loop_steps": {"simulate": "completed", "revenue": "snapshot"},
        "metrics": metrics,
        "revenue_feedback": revenue,
    }


def main() -> int:
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    out = snapshot(payload)
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
