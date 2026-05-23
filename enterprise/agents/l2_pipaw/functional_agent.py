"""
L2 职能 Agent 基类
职能数字人共同特征：
- 接收来自 L1 SelfPaw 的意图单
- 调用 cs.* 执行跨部门协作
- 编排多步骤业务流程
- 上报 KPI 与例外
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from ...platform.capability_services.cs_gateway import CapabilityServiceGateway, CSRequest
from ...platform.data_plane.event_stream import EventStream, DomainEvent
from ...platform.governance.sla_monitor import SLAMonitor


@dataclass
class AgentTask:
    """职能 Agent 工作任务"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""          # l1_selfpaw / l3_pipaw / manual
    originator_id: str = ""
    task_type: str = ""
    payload: Dict = field(default_factory=dict)
    status: str = "pending"   # pending / in_progress / completed / failed / escalated
    result: Any = None
    error: Optional[str] = None
    steps: List[Dict] = field(default_factory=list)
    sla_task_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


class FunctionalAgent(ABC):
    """
    L2 职能 Agent 抽象基类
    ΠPaw 工作台的核心执行单元
    """

    def __init__(
        self,
        agent_id: str,
        tenant_id: str,
        cs_gateway: Optional[CapabilityServiceGateway] = None,
        event_stream: Optional[EventStream] = None,
        sla_monitor: Optional[SLAMonitor] = None,
    ):
        self.agent_id = agent_id
        self.tenant_id = tenant_id
        self._gateway = cs_gateway or CapabilityServiceGateway()
        self._event_stream = event_stream or EventStream()
        self._sla = sla_monitor or SLAMonitor()
        self._tasks: Dict[str, AgentTask] = {}

    def receive_intent_unit(self, intent_unit: Dict) -> AgentTask:
        """接收来自 L1 SelfPaw 的意图单"""
        task = AgentTask(
            source="l1_selfpaw",
            originator_id=intent_unit.get("originator_id", ""),
            task_type=intent_unit.get("intent_classification", {}).get("intent_category", ""),
            payload=intent_unit,
        )
        self._tasks[task.task_id] = task
        return self.execute_task(task)

    def execute_task(self, task: AgentTask) -> AgentTask:
        """执行任务（模板方法模式）"""
        task.status = "in_progress"
        sla_task = self._sla.register(task.task_type, self.agent_id, self._get_sla_hours(task))
        task.sla_task_id = sla_task.task_id

        try:
            task.result = self._do_execute(task)
            task.status = "completed"
            task.completed_at = datetime.now(timezone.utc).isoformat()
            self._sla.complete(sla_task.task_id)
            self._emit_completed_event(task)
        except Exception as exc:
            task.status = "failed"
            task.error = str(exc)
            self._emit_failed_event(task)

        return task

    @abstractmethod
    def _do_execute(self, task: AgentTask) -> Any:
        """子类实现具体执行逻辑"""
        raise NotImplementedError

    def call_service(self, service: str, action: str, payload: Dict) -> Any:
        """调用 cs.* 服务"""
        req = CSRequest(
            service=service,
            action=action,
            payload=payload,
            caller_id=self.agent_id,
            tenant_id=self.tenant_id,
        )
        resp = self._gateway.invoke(req)
        if resp.status != "success":
            raise RuntimeError(f"{service}.{action} 失败: {resp.error}")
        return resp.result

    def add_step(self, task: AgentTask, step_name: str, result: Any) -> None:
        task.steps.append({
            "step": step_name,
            "result": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def get_pending_tasks(self) -> List[AgentTask]:
        return [t for t in self._tasks.values() if t.status == "pending"]

    def get_task_summary(self) -> Dict:
        statuses = {}
        for t in self._tasks.values():
            statuses[t.status] = statuses.get(t.status, 0) + 1
        return {"agent_id": self.agent_id, "total": len(self._tasks), **statuses}

    def _get_sla_hours(self, task: AgentTask) -> int:
        return 4

    def _emit_completed_event(self, task: AgentTask):
        self._event_stream.publish(DomainEvent(
            event_type=f"task.completed.{self.agent_id}",
            aggregate_id=task.task_id,
            aggregate_type="AgentTask",
            tenant_id=self.tenant_id,
            actor_id=self.agent_id,
            payload={"task_type": task.task_type, "source": task.source},
        ))

    def _emit_failed_event(self, task: AgentTask):
        self._event_stream.publish(DomainEvent(
            event_type=f"task.failed.{self.agent_id}",
            aggregate_id=task.task_id,
            aggregate_type="AgentTask",
            tenant_id=self.tenant_id,
            actor_id=self.agent_id,
            payload={"error": task.error},
        ))
