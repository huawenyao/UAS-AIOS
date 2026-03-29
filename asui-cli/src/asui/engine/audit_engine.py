"""审计引擎。"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class AuditEngine:
    """将运行事件写入审计日志。"""

    def __init__(self, app_root: Path) -> None:
        self.log_path = app_root / "database" / "audit" / "execution_log.jsonl"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event: dict) -> None:
        event_with_time = {
            "timestamp": datetime.now(UTC).isoformat(),
            **event,
        }
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event_with_time, ensure_ascii=False) + "\n")
