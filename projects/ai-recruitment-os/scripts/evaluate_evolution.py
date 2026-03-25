#!/usr/bin/env python3
"""评估招聘智能OS是否满足 UAS 平台与演化标准。"""

import json
import sys
from pathlib import Path


def load_manifest() -> dict:
    manifest_path = Path("configs") / "platform_manifest.json"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def main() -> int:
    manifest = load_manifest()
    payload = json.load(sys.stdin)

    risks = []
    suggestions = []

    if manifest["platform"]["technical_base"] != "ASUI":
        risks.append("技术底座不是ASUI")
        suggestions.append("回退到平台清单，统一技术底座为ASUI")

    if manifest["platform"]["runtime"] != "autonomous_agent":
        risks.append("运行架构不是autonomous_agent")
        suggestions.append("回退到runtime配置，统一运行时为autonomous_agent")

    if not payload.get("governance_controls"):
        risks.append("缺少治理控制设计")
        suggestions.append("补充公平、审计、权限、解释链和审批控制")

    if not payload.get("evolution_loop"):
        risks.append("缺少演化回路")
        suggestions.append("补充偏差检测、评估指标与迭代路径")

    status = "pass" if not risks else "needs_evolution"
    print(json.dumps({"status": status, "risks": risks, "suggestions": suggestions or ["当前方案满足平台标准"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
