#!/usr/bin/env python3
"""三维理念现实涌现 SubApp 演化评估。"""

import json
import sys
from pathlib import Path


def main() -> int:
    manifest = json.loads((Path("configs") / "platform_manifest.json").read_text(encoding="utf-8"))
    payload = json.load(sys.stdin) if not sys.stdin.isatty() else {}
    risks = []
    if manifest["platform"]["technical_base"] != "ASUI":
        risks.append("技术底座不是 ASUI")
    if not payload.get("evolution_loop") and not payload.get("emergence_reports"):
        risks.append("缺少涌现报告或演化回路")
    status = "pass" if not risks else "needs_evolution"
    print(
        json.dumps(
            {"status": status, "risks": risks, "suggestions": ["补充交叉验证与复盘"] if risks else ["满足三维涌现标准"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
