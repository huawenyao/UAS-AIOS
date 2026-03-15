#!/usr/bin/env python3
"""准备 evolution 回写数据，供 Agent 执行 /evolveApply 时使用。"""

import argparse
import json
import sys
from pathlib import Path


def slugify(value: str) -> str:
    import re
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return normalized or "cognitive-state"


def main() -> int:
    parser = argparse.ArgumentParser(description="准备 evolution 回写数据")
    parser.add_argument("topic", help="业务议题")
    parser.add_argument("--app-id", help="sub app ID，默认从 projects/ 推断")
    parser.add_argument("--app-root", help="sub app 根目录")
    parser.add_argument("--dry-run", action="store_true", help="仅输出待应用项")
    args = parser.parse_args()

    workspace = Path(__file__).resolve().parents[1]
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

    state = {}
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

    output = {
        "topic": args.topic,
        "topic_slug": slug,
        "app_root": str(app_root),
        "suggestions": suggestions,
        "feedback": feedback,
        "human_feedback_path": human_feedback_path.replace("{topic_slug}", slug),
        "evolution": evolution,
        "dry_run": args.dry_run,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
