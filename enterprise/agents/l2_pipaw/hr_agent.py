"""
L2 HR 数字人
职责：招聘流程 · 入职 · 绩效 · 组织调整
调用：cs.bpm.* / cs.approval.*
"""
from __future__ import annotations
from typing import Any, Dict

from .functional_agent import FunctionalAgent, AgentTask


class HRAgent(FunctionalAgent):
    """
    HR 数字人（招聘 + 入职 + 绩效）
    """

    def __init__(self, tenant_id: str, cs_gateway=None, event_stream=None, sla_monitor=None):
        super().__init__(
            agent_id="l2_hr_agent",
            tenant_id=tenant_id,
            cs_gateway=cs_gateway,
            event_stream=event_stream,
            sla_monitor=sla_monitor,
        )
        perm = getattr(self._gateway, "_permission", None)
        if perm:
            perm.assign_roles(self.agent_id, ["hr", "l2_user"])

    def _do_execute(self, task: AgentTask) -> Any:
        task_type = task.task_type or task.payload.get("task_type", "")
        dispatchers = {
            "start_recruitment": self._start_recruitment,
            "onboard_employee": self._onboard_employee,
            "initiate_performance_review": self._initiate_performance_review,
        }
        handler = dispatchers.get(task_type, self._default_handler)
        return handler(task)

    def _start_recruitment(self, task: AgentTask) -> Dict:
        """启动招聘流程"""
        payload = task.payload
        process = self.call_service("cs.bpm", "start", {
            "process_key": "lead_qualification",
            "variables": {
                "position": payload.get("position", ""),
                "department": payload.get("department", ""),
                "headcount": payload.get("headcount", 1),
                "requester_id": payload.get("requester_id", ""),
            },
        })
        self.add_step(task, "start_recruitment_process", process)

        # 创建审批（新增人员需批）
        approval = self.call_service("cs.approval", "create", {
            "type": "contract",
            "subject": f"招聘申请: {payload.get('position', '')}",
            "requester_id": payload.get("requester_id", ""),
            "amount": payload.get("budget", 0),
        })
        self.add_step(task, "create_approval", approval)

        return {
            "process_id": process.get("instance_id", ""),
            "approval_id": approval.get("task_id", ""),
            "status": "recruitment_started",
        }

    def _onboard_employee(self, task: AgentTask) -> Dict:
        """员工入职"""
        payload = task.payload
        process = self.call_service("cs.bpm", "start", {
            "process_key": "onboarding",
            "variables": {"employee_id": payload.get("employee_id", ""), "start_date": payload.get("start_date", "")},
        })
        self.add_step(task, "start_onboarding", process)
        return {"process_id": process.get("instance_id", ""), "status": "onboarding_started"}

    def _initiate_performance_review(self, task: AgentTask) -> Dict:
        """发起绩效评估"""
        payload = task.payload
        approval = self.call_service("cs.approval", "create", {
            "type": "contract",
            "subject": f"绩效评估: {payload.get('period', 'Q4')}",
            "requester_id": payload.get("requester_id", ""),
            "amount": 0,
        })
        return {"approval_id": approval.get("task_id", ""), "status": "review_initiated"}

    def _default_handler(self, task: AgentTask) -> Dict:
        return {"status": "acknowledged", "note": "HR 数字人已接收任务"}
