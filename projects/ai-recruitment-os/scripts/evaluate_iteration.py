#!/usr/bin/env python3
"""根据目标守恒策略评估招聘OS方案并生成进化建议。"""

import json
import sys
from pathlib import Path


def load_policy() -> dict:
    policy_path = Path("configs") / "evolution_policy.json"
    return json.loads(policy_path.read_text(encoding="utf-8"))


def main() -> int:
    policy = load_policy()
    payload = json.load(sys.stdin)

    purpose_anchor = " ".join(payload.get("purpose_anchor", []))
    metrics = payload.get("metrics", {})

    missing_keywords = [
        keyword
        for keyword in policy["goal_guard"]["required_purpose_keywords"]
        if keyword not in purpose_anchor
    ]

    risks = []
    suggestions = []

    if len(policy["goal_guard"]["required_purpose_keywords"]) - len(missing_keywords) < policy["goal_guard"]["minimum_keyword_hits"]:
        risks.append("基础目的覆盖不足，存在目标漂移风险")
        suggestions.append("回到目的激活阶段，重新校准匹配/效率/公平/体验/成本的优先级")

    for metric_name, threshold in policy["evaluation_thresholds"].items():
        value = float(metrics.get(metric_name, 0.0))
        if value < threshold:
            risks.append(f"{metric_name} 低于阈值 {threshold}")
            suggestions.append(f"围绕 {metric_name} 对应层进行重构与进化")

    status = "pass" if not risks else "needs_evolution"
    result = {
        "status": status,
        "missing_purpose_keywords": missing_keywords,
        "risks": risks,
        "suggestions": suggestions or ["当前方案可继续进入实现阶段"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
