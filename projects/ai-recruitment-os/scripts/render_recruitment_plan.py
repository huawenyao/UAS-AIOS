#!/usr/bin/env python3
"""渲染招聘智能OS方案。"""

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "recruitment-os"


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
    topic = str(payload.get("topic", "recruitment-os"))
    slug = slugify(topic)

    report_dir = Path("reports")
    data_dir = Path("database") / "plans"
    report_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    data_path = data_dir / f"{slug}.json"

    markdown = [
        f"# 招聘智能OS方案：{topic}",
        "",
        section("基础目的", payload.get("purpose_anchor")),
        section("宏观战略", payload.get("macro_strategy")),
        section("中观流程", payload.get("meso_workflows")),
        section("微观实体", payload.get("micro_entities")),
        section("智能体分工", payload.get("swarm_roles")),
        section("现实实例化对象", payload.get("instantiated_objects")),
        section("产品定义", payload.get("product_definition")),
        section("体验蓝图", payload.get("experience_blueprint")),
        section("技术架构", payload.get("technical_architecture")),
        section("MVP范围", payload.get("mvp_scope")),
        section("评估指标", payload.get("evaluation_metrics")),
        section("偏差风险", payload.get("deviation_risks")),
        section("迭代回路", payload.get("iteration_loop")),
        section("复盘触发器", payload.get("retrospective_triggers")),
    ]

    report_path.write_text("\n".join(markdown), encoding="utf-8")
    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"status": "written", "report_path": str(report_path), "data_path": str(data_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
