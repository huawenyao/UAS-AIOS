#!/usr/bin/env python3
"""准备 evolution 回写数据，供 Agent 执行 /evolveApply 时使用。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "cognitive-state"


def discover_apps(workspace: Path) -> list[Path]:
    roots: list[Path] = []
    for base in ("projects", "examples"):
        parent = workspace / base
        if not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            if child.is_dir() and (child / "configs").is_dir():
                roots.append(child)
    return roots


def scan_backlog(workspace: Path) -> list[dict]:
    items: list[dict] = []
    for app_root in discover_apps(workspace):
        state_dir = app_root / "database" / "cognitive_state"
        if not state_dir.is_dir():
            continue
        for state_file in state_dir.glob("*.json"):
            try:
                state = json.loads(state_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            evolution = state.get("evolution", {})
            suggestions = evolution.get("suggestions", [])
            if isinstance(suggestions, str):
                suggestions = [suggestions] if suggestions else []
            if not suggestions:
                continue
            applied = evolution.get("last_applied_at")
            items.append(
                {
                    "app_root": str(app_root.relative_to(workspace)),
                    "state_file": str(state_file.relative_to(workspace)),
                    "topic_slug": state_file.stem,
                    "suggestions_count": len(suggestions),
                    "last_applied_at": applied,
                    "status": "applied" if applied else "pending",
                }
            )
    return items


def law_pack_targets(app_root: Path) -> dict:
    """REQ-EDH-K-002：cs 法则包与治理模板回写目标路径（草案，不自动写入）。"""
    return {
        "governance_policy": str(app_root / "configs" / "governance_policy.json"),
        "evolution_policy": str(app_root / "configs" / "evolution_policy.json"),
        "cs_law_pack_example": str(
            app_root / "configs" / "cs_law_pack.sample.json"
        ),
        "changeset_audit_dir": str(app_root / "database" / "audit"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="准备 evolution 回写数据")
    parser.add_argument("topic", nargs="?", help="业务议题")
    parser.add_argument("--app-id", help="sub app ID")
    parser.add_argument("--app-root", help="sub app 根目录")
    parser.add_argument("--dry-run", action="store_true", help="仅输出待应用项")
    parser.add_argument("--status", action="store_true", help="扫描未 apply 的 evolution 积压")
    parser.add_argument("--law-pack", action="store_true", help="输出 cs 法则包回写目标路径")
    parser.add_argument(
        "--apply-safe-all",
        action="store_true",
        help="原型：将根目录 cs_law_pack 样例同步到各 subapp 并标记 evolution 已应用",
    )
    args = parser.parse_args()

    workspace = Path(__file__).resolve().parents[1]

    if args.status:
        backlog = scan_backlog(workspace)
        print(
            json.dumps(
                {"pending_count": sum(1 for x in backlog if x["status"] == "pending"), "items": backlog},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.apply_safe_all:
        from datetime import datetime, timezone

        law_src = workspace / "configs" / "cs_law_pack.sample.json"
        applied: list[dict] = []
        for app_root in discover_apps(workspace):
            dest = app_root / "configs" / "cs_law_pack.sample.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            if law_src.is_file():
                dest.write_text(law_src.read_text(encoding="utf-8"), encoding="utf-8")
            for state_file in (app_root / "database" / "cognitive_state").glob("*.json"):
                try:
                    state = json.loads(state_file.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    continue
                evo = state.setdefault("evolution", {})
                if not evo.get("suggestions") and evo.get("last_applied_at"):
                    continue
                evo["last_applied_at"] = datetime.now(timezone.utc).isoformat()
                evo["apply_note"] = "apply-safe-all prototype sync"
                state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            applied.append({"app_root": str(app_root.relative_to(workspace)), "law_pack": dest.is_file()})
        print(json.dumps({"status": "ok", "applied": applied}, ensure_ascii=False, indent=2))
        return 0

    if not args.topic:
        print(json.dumps({"error": "topic required unless --status"}, ensure_ascii=False))
        return 1

    app_root = Path(args.app_root) if args.app_root else workspace / "projects" / (args.app_id or ".")
    if not app_root.is_dir():
        app_root = workspace / "examples" / (args.app_id or ".")
    if not app_root.is_dir():
        print(json.dumps({"error": "app_root not found", "app_id": args.app_id}, ensure_ascii=False))
        return 1

    slug = slugify(args.topic)
    state_path = app_root / "database" / "cognitive_state" / f"{slug}.json"
    feedback_path = app_root / "database" / "feedback" / f"{slug}.json"
    evolution_policy_path = app_root / "configs" / "evolution_policy.json"

    state: dict = {}
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))

    feedback = None
    if feedback_path.exists():
        feedback = json.loads(feedback_path.read_text(encoding="utf-8"))

    evolution = state.get("evolution", {})
    suggestions = evolution.get("suggestions", [])
    if isinstance(suggestions, str):
        suggestions = [suggestions]

    human_feedback_path = "database/feedback/{topic_slug}.json"
    if evolution_policy_path.exists():
        policy = json.loads(evolution_policy_path.read_text(encoding="utf-8"))
        human_feedback_path = policy.get("human_feedback_path", human_feedback_path)

    output: dict = {
        "topic": args.topic,
        "topic_slug": slug,
        "app_root": str(app_root),
        "suggestions": suggestions,
        "feedback": feedback,
        "human_feedback_path": human_feedback_path.replace("{topic_slug}", slug),
        "evolution": evolution,
        "dry_run": args.dry_run,
        "apply_required": bool(suggestions) and not evolution.get("last_applied_at"),
    }
    if args.law_pack:
        output["law_pack_targets"] = law_pack_targets(app_root)

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
