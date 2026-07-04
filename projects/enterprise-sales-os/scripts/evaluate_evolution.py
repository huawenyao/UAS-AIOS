#!/usr/bin/env python3
"""Enterprise Sales OS 演化评估。"""

import json
import sys
from pathlib import Path


def main() -> int:
    manifest = json.loads((Path("configs") / "platform_manifest.json").read_text(encoding="utf-8"))
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    risks = []
    if not payload.get("governance_controls"):
        risks.append("缺少治理控制")
    sales_ok = payload.get("mvp_cases_passed") or payload.get("sales_result", {}).get("passed")
    if not sales_ok:
        risks.append("销售流水线未通过（mvp_cases_passed / sales_result.passed）")
    status = "pass" if not risks else "needs_evolution"
    print(
        json.dumps(
            {"status": status, "risks": risks, "suggestions": ["运行 evaluate_sales_mvp.py"] if risks else ["满足 v0.2 标准"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
