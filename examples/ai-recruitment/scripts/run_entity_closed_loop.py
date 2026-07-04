#!/usr/bin/env python3
"""实体事件全流程闭环：初筛 → AI 面试任务 → 事件 → 评价 → 通知。"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if os.environ.get("AI_RECRUITMENT_ROOT"):
    ROOT = Path(os.environ["AI_RECRUITMENT_ROOT"]).resolve()

# 确保 entity_runtime 使用相同 ROOT
os.environ["AI_RECRUITMENT_ROOT"] = str(ROOT)
sys.path.insert(0, str(Path(__file__).parent))

from entity_runtime import complete_task, create_task, _load_json, _save_json  # noqa: E402
from recruitment_closed_loop import run_recruitment_closed_loop  # noqa: E402


def seed_if_needed() -> dict:
    db = ROOT / "database"
    db.mkdir(parents=True, exist_ok=True)
    jobs_path = db / "jobs.json"
    candidates_path = db / "candidates.json"

    if not jobs_path.exists():
        _save_json(
            jobs_path,
            [
                {
                    "job_id": "job-demo-001",
                    "title": "高级后端工程师",
                    "status": "open",
                    "created_at": datetime.now().isoformat(),
                }
            ],
            "jobs",
        )
    if not candidates_path.exists():
        _save_json(
            candidates_path,
            [
                {"candidate_id": "c1", "name": "候选人A", "status": "new", "job_id": "job-demo-001"},
                {"candidate_id": "c2", "name": "候选人B", "status": "new", "job_id": "job-demo-001"},
            ],
            "candidates",
        )

    for name in ("tasks.json", "events.json", "evaluations.json", "notifications.json"):
        path = db / name
        if not path.exists():
            _save_json(path, [], name)

    return {"job_id": "job-demo-001", "database": str(db)}


def run_loop() -> dict:
    seed_if_needed()
    loop = run_recruitment_closed_loop(
        [
            {"candidate_id": "c1", "total_score": 8.5},
            {"candidate_id": "c2", "total_score": 6.0},
        ]
    )
    tasks_created = []
    for item in loop["interview"]["scheduled"]:
        task = create_task("ai_interview", "job-demo-001", item, {"source": "closed_loop_runner"})
        out = complete_task(
            task["task_id"],
            {
                "dimensions": {"technical": 8, "communication": 7},
                "summary": f"AI 面试完成：{item}",
            },
        )
        tasks_created.append({"task_id": task["task_id"], "event_id": out.get("event_id")})

    events = _load_json(ROOT / "database" / "events.json", [])
    evals = _load_json(ROOT / "database" / "evaluations.json", [])
    notifs = _load_json(ROOT / "database" / "notifications.json", [])

    ok = (
        len(events) >= 1
        and len(evals) >= 1
        and len(notifs) >= 1
        and "screening_completed" in loop["events"]
        and "ai_interview_completed" in loop["events"]
    )
    return {
        "status": "completed" if ok else "incomplete",
        "closed_loop": loop,
        "tasks": tasks_created,
        "counts": {"events": len(events), "evaluations": len(evals), "notifications": len(notifs)},
        "passed": ok,
    }


def main() -> int:
    result = run_loop()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
