#!/usr/bin/env python3
"""记录 evolution 建议已应用（Wave 2：审计落盘，不自动改 configs）。"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "cognitive-state"


def main() -> int:
    parser = argparse.ArgumentParser(description="记录 evolution apply 审计")
    parser.add_argument("topic", help="业务议题")
    parser.add_argument("--app-id", default="ai-recruitment-os")
    parser.add_argument("--app-root", help="subapp 根目录")
    parser.add_argument("--note", default="", help="应用说明")
    args = parser.parse_args()

    workspace = Path(__file__).resolve().parents[1]
    app_root = Path(args.app_root) if args.app_root else workspace / "projects" / args.app_id
    if not app_root.is_dir():
        print(json.dumps({"error": "app_root not found"}, ensure_ascii=False))
        return 1

    slug = slugify(args.topic)
    state_path = app_root / "database" / "cognitive_state" / f"{slug}.json"
    if not state_path.exists():
        print(json.dumps({"error": "state not found", "path": str(state_path)}, ensure_ascii=False))
        return 1

    state = json.loads(state_path.read_text(encoding="utf-8"))
    evolution = state.setdefault("evolution", {})
    suggestions = evolution.get("suggestions", [])
    if isinstance(suggestions, str):
        suggestions = [suggestions]

    applied_at = datetime.now(timezone.utc).isoformat()
    backup_dir = app_root / "database" / "evolution_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"{slug}_{applied_at.replace(':', '-')}.json"
    backup_path.write_text(state_path.read_text(encoding="utf-8"), encoding="utf-8")

    evolution["last_applied_at"] = applied_at
    evolution["applied_suggestions"] = suggestions
    evolution["apply_note"] = args.note or "recorded via record_evolution_apply.py"
    if "purpose_drift" in str(evolution.get("drift_triggered", "")):
        evolution["purpose_anchor"] = [
            "匹配",
            "效率",
            "公平",
            "体验",
            "成本",
            "让组织在可控成本下以更高确定性获得匹配人才",
        ]
    state["evolution"] = evolution
    state.setdefault("timeline", []).append(
        {
            "timestamp": applied_at,
            "event": "evolution_applied",
            "payload": {"suggestions": suggestions, "backup": str(backup_path.relative_to(app_root))},
        }
    )
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    log_path = app_root / "database" / "evolution_apply_log.json"
    log: list = []
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
    log.append({"topic_slug": slug, "applied_at": applied_at, "suggestions": suggestions})
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {"status": "ok", "topic_slug": slug, "last_applied_at": applied_at, "backup": str(backup_path)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
