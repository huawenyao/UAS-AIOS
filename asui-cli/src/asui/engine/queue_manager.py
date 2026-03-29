"""Queue manager for shared UAS Runtime Service."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class QueueManager:
    """基于文件系统的最小任务队列。"""

    def __init__(self, projects_root: Path) -> None:
        self.queue_dir = projects_root / ".service_registry" / "queue"
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def enqueue(self, app_id: str, topic: str, payload: dict | None = None, evaluate: bool = False) -> Path:
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S%f")
        job_path = self.queue_dir / f"{timestamp}-{app_id}.json"
        job = {
            "job_id": job_path.stem,
            "app_id": app_id,
            "topic": topic,
            "payload": payload or {},
            "evaluate": evaluate,
            "status": "queued",
            "created_at": datetime.now(UTC).isoformat(),
        }
        job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
        return job_path

    def list_jobs(self) -> list[dict]:
        jobs = []
        for path in sorted(self.queue_dir.glob("*.json")):
            jobs.append(json.loads(path.read_text(encoding="utf-8")))
        return jobs

    def pop_next(self) -> tuple[dict, Path] | None:
        queue_files = sorted(self.queue_dir.glob("*.json"))
        if not queue_files:
            return None
        path = queue_files[0]
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload, path

    def complete(self, path: Path, result: dict) -> None:
        path.unlink(missing_ok=True)
        completed_dir = self.queue_dir / "completed"
        completed_dir.mkdir(parents=True, exist_ok=True)
        completed_path = completed_dir / path.name
        completed_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    def stats(self) -> dict:
        return {
            "queued_jobs": len(list(self.queue_dir.glob("*.json"))),
            "completed_jobs": len(list((self.queue_dir / "completed").glob("*.json"))) if (self.queue_dir / "completed").exists() else 0,
        }
