#!/usr/bin/env python3
"""全场景产品原型验收：L1-L3 + 平台价值闭环。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str], *, cwd: Path | None = None, input_json: dict | None = None) -> dict:
    kwargs: dict = {
        "cwd": str(cwd or ROOT),
        "capture_output": True,
        "text": True,
        "timeout": 180,
    }
    if input_json is not None:
        kwargs["input"] = json.dumps(input_json, ensure_ascii=False)
    r = subprocess.run(cmd, **kwargs)
    body = (r.stdout or r.stderr).strip()
    try:
        parsed = json.loads(body.splitlines()[-1]) if body else {}
    except (json.JSONDecodeError, IndexError):
        parsed = {"raw": body[:400]}
    return {"passed": r.returncode == 0, "exit_code": r.returncode, "result": parsed}


def run_scenario(scenario: dict) -> dict:
    sid = scenario["id"]
    runner = scenario.get("runner", "")

    if runner == "selfpaw_session":
        return {
            "id": sid,
            **_run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_uas_runtime_service.py"),
                    "run",
                    "--app-id",
                    "selfpaw-enterprise",
                    "--topic",
                    "ecosystem-prototype-l1",
                    "--payload-json",
                    json.dumps({"tenant_id": "t-acme-demo", "user_id": "u-employee-1001"}, ensure_ascii=False),
                ]
            ),
        }
    if runner == "dual_track_cs":
        return {"id": sid, **_run([sys.executable, str(ROOT / "scripts" / "run_edh_dual_track_loop.py")])}
    if runner == "recruitment_entity":
        path = scenario.get("path", "examples/ai-recruitment/scripts/run_entity_closed_loop.py")
        return {
            "id": sid,
            **_run([sys.executable, str(ROOT / path)], cwd=ROOT / "examples" / "ai-recruitment"),
        }
    if runner == "sales_mvp":
        return {
            "id": sid,
            **_run([sys.executable, str(ROOT / "projects" / "enterprise-sales-os" / "scripts" / "evaluate_sales_mvp.py")]),
        }
    if runner == "pipaw_cs_agent":
        return {
            "id": sid,
            **_run([sys.executable, "-m", "pytest", "tests/test_pipaw_cs_agent.py", "-q"], cwd=ROOT / "asui-cli"),
        }
    if runner == "finance_prototype":
        return {"id": sid, **_run([sys.executable, str(ROOT / "scripts" / "run_finance_prototype.py")])}
    if runner == "outward_gateway":
        return {"id": sid, **_run([sys.executable, str(ROOT / "scripts" / "run_outward_gateway_mock.py")])}
    if runner == "value_loop_full":
        return {"id": sid, **_run([sys.executable, str(ROOT / "scripts" / "run_value_loop_full.py")])}

    return {"id": sid, "passed": False, "result": {"error": f"unknown_runner:{runner}"}}


def main() -> int:
    catalog = json.loads((ROOT / "configs" / "ecosystem_scenario_catalog.json").read_text(encoding="utf-8"))
    results = [run_scenario(s) for s in catalog.get("scenarios", [])]
    passed = sum(1 for r in results if r.get("passed"))
    total = len(results)
    out = {
        "status": "completed" if passed == total else "partial",
        "passed": passed,
        "total": total,
        "scenarios": results,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
