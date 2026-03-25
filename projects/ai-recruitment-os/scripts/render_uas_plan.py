#!/usr/bin/env python3
"""渲染招聘智能OS sub uas app 方案。"""

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "ai-recruitment-os"


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
    return f"## {title}\n" + "\n".join(f"- {item}" for item in values) + "\n"


def main() -> int:
    payload = json.load(sys.stdin)
    topic = str(payload.get("topic", "ai-recruitment-os"))
    slug = slugify(topic)

    report_dir = Path("reports")
    data_dir = Path("database") / "plans"
    report_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    data_path = data_dir / f"{slug}.json"

    markdown = [
        f"# UAS 招聘 Sub App 方案：{topic}",
        "",
        section("意图模型", payload.get("intent_model")),
        section("知识资产", payload.get("knowledge_assets")),
        section("运行时拓扑", payload.get("runtime_topology")),
        section("Agent编织", payload.get("agent_fabric")),
        section("系统网格", payload.get("system_mesh")),
        section("治理控制", payload.get("governance_controls")),
        section("评估指标", payload.get("evaluation_metrics")),
        section("演化回路", payload.get("evolution_loop")),
        section("交付计划", payload.get("delivery_plan")),
    ]

    report_path.write_text("\n".join(markdown), encoding="utf-8")
    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"status": "written", "report_path": str(report_path), "data_path": str(data_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
