#!/usr/bin/env python3
"""
AI 招聘实体与事件运行时 — 与 UAS-ASUI autonomous_agent runtime 叠合

- 关键实体：Job, Candidate, Task（task 级状态隔离、可审计）
- 事件驱动：Task 完成 → 发布 Event → 触发 Notification / Evaluation
- 业务流程闭环：岗位→候选人→任务(初筛/AI面试)→完成状态→事件→通知与评价
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parent.parent
CONFIGS = ROOT / "configs"
DATABASE = ROOT / "database"
AUDIT_DIR = DATABASE / "audit"

SCHEMAS_FILE = CONFIGS / "entity_schemas.json"
EVENT_POLICY_FILE = CONFIGS / "event_policy.json"


def _load_json(path: Path, default=None):
    if default is None:
        default = []
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: Path, data, entity_name: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if AUDIT_DIR.exists() or os.environ.get("AUDIT_ENABLED", "true").lower() == "true":
        _audit("write", entity_name or path.stem, path, data)


def _audit(action: str, entity: str, path: Path, data):
    """与 runtime_config.audit_enabled 对齐：审计写操作"""
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    record = {
        "action": action,
        "entity": entity,
        "path": str(path),
        "at": datetime.now().isoformat(),
    }
    if isinstance(data, list) and len(data) > 0:
        record["count"] = len(data)
    elif isinstance(data, dict):
        record["id"] = data.get("task_id") or data.get("event_id") or data.get("candidate_id") or data.get("job_id")
    audit_file = AUDIT_DIR / f"audit_{entity}_{ts}.json"
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def create_task(
    task_type: str,
    job_id: str,
    candidate_id: str,
    payload: dict = None,
) -> dict:
    """创建任务（与 state_isolation: task_level 对应）。"""
    tasks_path = DATABASE / "tasks.json"
    tasks = _load_json(tasks_path, [])
    task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
    now = datetime.now().isoformat()
    task = {
        "task_id": task_id,
        "type": task_type,
        "status": "pending",
        "job_id": job_id,
        "candidate_id": candidate_id,
        "payload": payload or {},
        "result": None,
        "started_at": None,
        "completed_at": None,
        "created_at": now,
        "updated_at": now,
    }
    tasks.append(task)
    _save_json(tasks_path, tasks, "tasks")
    return task


def complete_task(task_id: str, result: dict) -> dict:
    """
    将任务标记为完成，发布事件，并执行 event_policy 中的 triggers：
    - create_evaluation → 写入 evaluations.json
    - notify_* → 写入 notifications.json
    """
    tasks_path = DATABASE / "tasks.json"
    tasks = _load_json(tasks_path, [])
    task = None
    for t in tasks:
        if t.get("task_id") == task_id:
            task = t
            break
    if not task:
        raise ValueError(f"Task not found: {task_id}")

    now = datetime.now().isoformat()
    task["status"] = "completed"
    task["result"] = result
    task["completed_at"] = now
    task["updated_at"] = now
    _save_json(tasks_path, tasks, "tasks")

    policy = _load_json(EVENT_POLICY_FILE, {})
    event_type_map = {e["id"]: e for e in policy.get("event_types", []) if isinstance(e, dict)}
    # 根据任务类型选择事件类型
    event_type = "ai_interview_completed" if task.get("type") == "ai_interview" else "human_interview_completed"
    if task.get("type") == "screening":
        event_type = "screening_completed"
    event_spec = event_type_map.get(event_type, {})

    # 发布事件
    events_path = DATABASE / "events.json"
    events = _load_json(events_path, [])
    event_id = f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
    event = {
        "event_id": event_id,
        "event_type": event_type,
        "task_id": task_id,
        "job_id": task.get("job_id"),
        "candidate_id": task.get("candidate_id"),
        "payload": {"result_summary": list(result.keys()) if isinstance(result, dict) else str(result)},
        "occurred_at": now,
    }
    events.append(event)
    _save_json(events_path, events, "events")

    triggers = event_spec.get("triggers", [])
    if "create_evaluation" in triggers:
        eval_id = f"eval_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
        evals_path = DATABASE / "evaluations.json"
        evals = _load_json(evals_path, [])
        evals.append({
            "evaluation_id": eval_id,
            "task_id": task_id,
            "candidate_id": task.get("candidate_id"),
            "job_id": task.get("job_id"),
            "scope": "ai_interview" if task.get("type") == "ai_interview" else "human_interview",
            "dimensions": result.get("dimensions", result) if isinstance(result, dict) else {},
            "summary": result.get("summary", str(result)) if isinstance(result, dict) else str(result),
            "created_at": now,
        })
        _save_json(evals_path, evals, "evaluations")

    if any(t.startswith("notify_") for t in triggers):
        notif_path = DATABASE / "notifications.json"
        notifs = _load_json(notif_path, [])
        notif_id = f"notif_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
        notifs.append({
            "notification_id": notif_id,
            "event_id": event_id,
            "channel": "in_app",
            "recipient_role": "hr_recruiter",
            "title": f"任务完成：{event_type}",
            "body": f"候选人 {task.get('candidate_id')} 的 {task.get('type')} 已完成，请查看评价。",
            "status": "pending",
            "created_at": now,
        })
        _save_json(notif_path, notifs, "notifications")

    return {"task": task, "event_id": event_id, "event_type": event_type}


def emit_event(event_type: str, job_id: str = None, candidate_id: str = None, task_id: str = None, payload: dict = None) -> dict:
    """直接发布业务事件（不经过 Task 完成）。"""
    events_path = DATABASE / "events.json"
    events = _load_json(events_path, [])
    event_id = f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:8]}"
    now = datetime.now().isoformat()
    event = {
        "event_id": event_id,
        "event_type": event_type,
        "task_id": task_id,
        "job_id": job_id,
        "candidate_id": candidate_id,
        "payload": payload or {},
        "occurred_at": now,
    }
    events.append(event)
    _save_json(events_path, events, "events")
    return event


def update_candidate_status(candidate_id: str, status: str) -> bool:
    """更新候选人状态（screened | shortlisted | interview_completed 等）。"""
    path = DATABASE / "candidates.json"
    candidates = _load_json(path, [])
    for c in candidates:
        if c.get("candidate_id") == candidate_id:
            c["status"] = status
            c["updated_at"] = datetime.now().isoformat()
            _save_json(path, candidates, "candidates")
            return True
    return False


# CLI
def main():
    import argparse
    p = argparse.ArgumentParser(description="实体运行时：创建/完成任务、发布事件")
    p.add_argument("action", choices=["create_task", "complete_task", "emit_event"], help="动作")
    p.add_argument("--type", default="ai_interview", help="任务类型: screening | ai_interview | human_interview")
    p.add_argument("--task-id", help="完成任务时必填")
    p.add_argument("--job-id", default="")
    p.add_argument("--candidate-id", default="")
    p.add_argument("--event-type", default="ai_interview_completed")
    p.add_argument("--result", default="{}", help="JSON 对象，complete_task 时使用")
    args = p.parse_args()

    if args.action == "create_task":
        t = create_task(args.type, args.job_id, args.candidate_id, {})
        print(json.dumps(t, ensure_ascii=False, indent=2))
    elif args.action == "complete_task":
        if not args.task_id:
            print("error: --task-id required", file=sys.stderr)
            sys.exit(1)
        result = json.loads(args.result) if args.result else {}
        out = complete_task(args.task_id, result)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.action == "emit_event":
        e = emit_event(args.event_type, args.job_id, args.candidate_id, None, {})
        print(json.dumps(e, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
