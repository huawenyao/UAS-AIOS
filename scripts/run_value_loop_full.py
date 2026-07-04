#!/usr/bin/env python3
"""价值闭环 7 步全量编排原型（B-05）。"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(
    cmd: list[str],
    cwd: Path | None = None,
    input_json: dict | None = None,
) -> dict:
    kwargs: dict = {
        "cwd": str(cwd or ROOT),
        "capture_output": True,
        "text": True,
        "timeout": 120,
        "encoding": "utf-8",
    }
    if input_json is not None:
        kwargs["input"] = json.dumps(input_json, ensure_ascii=False)
    r = subprocess.run(cmd, **kwargs)
    body = (r.stdout or r.stderr).strip()
    try:
        parsed = json.loads(body) if body.startswith("{") or body.startswith("[") else {"raw": body[:500]}
    except json.JSONDecodeError:
        parsed = {"raw": body[:500]}
    return {"exit_code": r.returncode, "output": parsed}


def main() -> int:
    steps: dict[str, str] = {}

    steps["1_input"] = "ok"
    steps["2_simulate"] = "pending"
    sim = _run(
        [
            sys.executable,
            str(ROOT / "projects" / "enterprise-sales-os" / "scripts" / "run_simulation_snapshot.py"),
        ],
        cwd=ROOT / "projects" / "enterprise-sales-os",
        input_json={"topic": "value-loop-prototype", "sales_result": {"passed": True}},
    )
    steps["2_simulate"] = "ok" if sim["exit_code"] == 0 else "failed"

    mvp = _run([sys.executable, str(ROOT / "projects" / "enterprise-sales-os" / "scripts" / "evaluate_sales_mvp.py")])
    steps["3_generate"] = "ok" if mvp["exit_code"] == 0 else "failed"

    dual = _run([sys.executable, str(ROOT / "scripts" / "run_edh_dual_track_loop.py")])
    steps["4_interact"] = "ok" if dual["exit_code"] == 0 else "failed"

    evo = _run(
        [
            sys.executable,
            str(ROOT / "scripts" / "evolve_apply.py"),
            "--status",
        ]
    )
    steps["5_evolve"] = "ok" if evo["exit_code"] == 0 else "failed"

    runtime = _run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_uas_runtime_service.py"),
            "run",
            "--app-id",
            "enterprise-sales-os",
            "--topic",
            "value-loop-prototype",
            "--payload-json",
            json.dumps({"sales_case_id": "CASE-001"}, ensure_ascii=False),
        ]
    )
    steps["6_output"] = "ok" if runtime["exit_code"] == 0 else "failed"

    metrics_path = ROOT / "configs" / "value_metrics.sample.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.is_file() else {}
    rev_payload = {"topic": "value-loop-prototype", "sales_result": mvp.get("output", {})}
    rev = _run(
        [sys.executable, str(ROOT / "scripts" / "value_loop_snapshot.py")],
        input_json=rev_payload,
    )
    steps["7_revenue"] = "ok" if rev["exit_code"] == 0 else "failed"

    completed = sum(1 for v in steps.values() if v == "ok")
    out = {
        "status": "completed" if completed >= 6 else "partial",
        "value_loop_steps": steps,
        "completed_count": completed,
        "total_steps": 7,
        "metrics_config": metrics.get("north_star", metrics),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if completed >= 6 else 1


if __name__ == "__main__":
    raise SystemExit(main())
