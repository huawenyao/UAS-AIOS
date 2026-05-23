"""
SLA 监控引擎
职责：监控审批/流程/Agent 任务 SLA，超时自动升级
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
import uuid


@dataclass
class SLATask:
    task_id: str
    task_type: str
    owner_id: str
    sla_deadline: str
    status: str = "active"    # active / completed / breached / escalated
    escalation_target: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SLAMonitor:
    """SLA 监控 + 自动升级"""

    def __init__(self):
        self._tasks: Dict[str, SLATask] = {}

    def register(
        self,
        task_type: str,
        owner_id: str,
        sla_hours: int,
        escalation_target: str = None,
    ) -> SLATask:
        deadline = (datetime.now(timezone.utc) + timedelta(hours=sla_hours)).isoformat()
        task = SLATask(
            task_id=str(uuid.uuid4()),
            task_type=task_type,
            owner_id=owner_id,
            sla_deadline=deadline,
            escalation_target=escalation_target,
        )
        self._tasks[task.task_id] = task
        return task

    def complete(self, task_id: str) -> Optional[SLATask]:
        task = self._tasks.get(task_id)
        if task:
            task.status = "completed"
        return task

    def check_breaches(self) -> List[SLATask]:
        """检查 SLA 超时（通常由定时任务调用）"""
        now = datetime.now(timezone.utc).isoformat()
        breached = []
        for task in self._tasks.values():
            if task.status == "active" and task.sla_deadline < now:
                task.status = "breached"
                breached.append(task)
        return breached

    def escalate_breaches(self, event_stream=None) -> List[str]:
        """自动升级 SLA 超时任务"""
        breached = self.check_breaches()
        escalated = []
        for task in breached:
            task.status = "escalated"
            escalated.append(task.task_id)
            if event_stream:
                from ..data_plane.event_stream import DomainEvent
                event_stream.publish(DomainEvent(
                    event_type="sla.breached",
                    aggregate_id=task.task_id,
                    aggregate_type="SLATask",
                    payload={"task_type": task.task_type, "owner": task.owner_id},
                ))
        return escalated

    def get_summary(self) -> Dict:
        counts: Dict[str, int] = {}
        for t in self._tasks.values():
            counts[t.status] = counts.get(t.status, 0) + 1
        return {"total": len(self._tasks), **counts}
