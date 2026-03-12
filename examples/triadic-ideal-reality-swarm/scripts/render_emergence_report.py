#!/usr/bin/env python3
"""渲染三维理念现实涌现结果。"""

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "emergence"


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
    topic = str(payload.get("topic", "emergence"))
    synthesis = payload.get("emergence_synthesis", payload)
    debate = payload.get("ideal_reality_debate", {})

    slug = slugify(topic)
    report_dir = Path("reports")
    decision_dir = Path("database") / "emergence"
    report_dir.mkdir(parents=True, exist_ok=True)
    decision_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    decision_path = decision_dir / f"{slug}.json"

    markdown = [
        f"# 三维理念现实涌现方案：{topic}",
        "",
        section("基础目的与激活锚点", synthesis.get("purpose_anchor")),
        section("宏观生态机制", synthesis.get("macro_ecology")),
        section("中观价值回路", synthesis.get("meso_value_loops")),
        section("微观实体矩阵", synthesis.get("micro_object_matrix")),
        section("理念现实张力", synthesis.get("ideal_reality_tensions") or debate.get("tensions")),
        section("场景激活路径", synthesis.get("activation_plan")),
        section("涌现解决方案", synthesis.get("emergence_solution")),
        section("运行机制", synthesis.get("operating_mode")),
        section("关键实体", synthesis.get("key_entities")),
        section("场景指标", synthesis.get("scene_metrics")),
        section("复盘触发器", synthesis.get("retrospective_triggers")),
    ]

    report_path.write_text("\n".join(markdown), encoding="utf-8")

    stored_payload = {
        "topic": topic,
        "ideal_reality_debate": debate,
        "emergence_synthesis": synthesis,
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
