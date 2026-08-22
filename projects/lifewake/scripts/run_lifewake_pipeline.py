#!/usr/bin/env python3
"""Runtime 脚本步：执行 LifeWake CASE（默认 CASE-001，可由 payload.lifewake_case_id 覆盖）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from evaluate_lifewake_mvp import ALL_CASES, run_case  # noqa: E402


def main() -> int:
    payload = json.load(sys.stdin)
    root = _SCRIPT_DIR.parent
    governance = json.loads((root / "configs" / "governance_policy.json").read_text(encoding="utf-8")).get(
        "governance", {}
    )

    case_id = payload.get("lifewake_case_id", "CASE-001")
    case = next((c for c in ALL_CASES if c["case_id"] == case_id), ALL_CASES[0])
    result = run_case(case, governance)

    audit_path = root / "database" / "audit" / f"runtime_{case_id}.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(
        json.dumps({"audit": result.get("audit", []), "case": case_id}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    out = {
        "lifewake_case_id": case_id,
        "lifewake_result": result,
        "governance_controls": payload.get("governance_controls")
        or ["consent", "privacy_purpose", "bond_bidirectional", "audit"],
        "evolution_loop": payload.get("evolution_loop")
        or ["intent_activation", "governance_check", "lifewake_execute"],
        "mvp_cases_passed": result.get("passed", False),
        "intent_model": payload.get("intent_model") or [f"生命回响议题：{payload.get('topic', case_id)}"],
        "final_state": result.get("state", {}).get("final"),
        "audit_path": str(audit_path.relative_to(root)),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
