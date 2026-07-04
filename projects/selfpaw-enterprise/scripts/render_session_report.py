#!/usr/bin/env python3
"""写入 SelfPaw 会话 Markdown 报告。"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    payload = json.load(sys.stdin)
    prev = payload.get("step_outputs", {}).get("intent_activation", {})
    topic = payload.get("topic", "session")
    slug = topic.replace(" ", "-")[:40]
    reports = APP_ROOT / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    path = reports / f"{slug}.md"
    lines = [
        f"# SelfPaw 会话报告 · {topic}",
        "",
        f"- 时间：{datetime.now(timezone.utc).isoformat()}",
        f"- 租户：{prev.get('session', {}).get('tenant_id', '')}",
        f"- 岗位：{prev.get('session', {}).get('position_code', '')}",
        f"- Domain：{prev.get('domain_binding', {}).get('domain_id', '')}",
        "",
        "## 意图模型",
        "",
    ]
    for item in prev.get("intent_model", []):
        lines.append(f"- {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"report_path": str(path.relative_to(APP_ROOT))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
