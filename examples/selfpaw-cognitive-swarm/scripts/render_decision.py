#!/usr/bin/env python3
"""渲染 selfpaw 蜂群决策结果。"""

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "decision"


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def section(title: str, items) -> str:
    values = ensure_list(items)
    if not values:
        return f"## {title}\n- 暂无\n"
    bullet_lines = "\n".join(f"- {item}" for item in values)
    return f"## {title}\n{bullet_lines}\n"


def main() -> int:
    payload = json.load(sys.stdin)
    topic = str(payload.get("topic", "decision"))
    synthesis = payload.get("synthesis", payload)
    debate = payload.get("second_negation", {})

    slug = slugify(topic)
    report_dir = Path("reports")
    decision_dir = Path("database") / "decisions"
    report_dir.mkdir(parents=True, exist_ok=True)
    decision_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    decision_path = decision_dir / f"{slug}.json"

    markdown = [
      f"# 全维度辩证决策方案：{topic}",
      "",
      f"**最终结论**：{synthesis.get('final_decision', '待补充')}",
      "",
      section("蜂群共识", synthesis.get("consensus") or debate.get("consensus")),
      section("核心冲突", synthesis.get("open_conflicts") or debate.get("conflicts")),
      section("执行路径", synthesis.get("execution_path")),
      section("风险预案", synthesis.get("risk_preplan")),
      section("用户适配", synthesis.get("user_adaptation")),
      section("成本把控", synthesis.get("cost_controls")),
      section("博弈应对", synthesis.get("game_response")),
      section("复盘触发器", synthesis.get("retrospective_triggers")),
    ]

    report_path.write_text("\n".join(markdown), encoding="utf-8")

    stored_payload = {
        "topic": topic,
        "second_negation": debate,
        "synthesis": synthesis,
    }
    decision_path.write_text(
        json.dumps(stored_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "written",
                "report_path": str(report_path),
                "decision_path": str(decision_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
