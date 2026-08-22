#!/usr/bin/env python3
"""渲染 LifeWake 运行报告。"""

import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "lifewake-run"


def main() -> int:
    payload = json.load(sys.stdin)
    topic = str(payload.get("topic", "lifewake-run"))
    slug = slugify(topic)
    lw = payload.get("lifewake_result", {})

    report_dir = Path("reports")
    data_dir = Path("database") / "runs"
    report_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{slug}.md"
    data_path = data_dir / f"{slug}.json"

    lines = [
        f"# 生命回响运行报告：{topic}",
        "",
        f"- **CASE**: {payload.get('lifewake_case_id', 'CASE-001')}",
        f"- **最终状态**: {payload.get('final_state', 'unknown')}",
        f"- **通过**: {lw.get('passed', False)}",
        "",
        "## 审计",
        "",
    ]
    for item in lw.get("audit", []):
        lines.append(f"- `{json.dumps(item, ensure_ascii=False)}`")

    lines.extend(
        [
            "",
            "## 仪式 / 结论",
            "",
            f"- report: `{json.dumps(lw.get('report', {}), ensure_ascii=False)}`",
            f"- ritual: `{json.dumps(lw.get('ritual', {}), ensure_ascii=False)}`",
        ]
    )
    if lw.get("changeset"):
        lines.extend(["", "## ChangeSet 草案", "", f"- `{json.dumps(lw['changeset'], ensure_ascii=False)}`"])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {"status": "written", "report_path": str(report_path), "data_path": str(data_path)},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
