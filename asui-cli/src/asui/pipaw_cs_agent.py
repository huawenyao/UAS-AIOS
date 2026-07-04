"""ΠPaw 客服标杆 Agent：按 Roster 绑定能力执行当前 Task Panel 步骤。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .connectors.router import CapabilityInvokeContext, CapabilityServiceRouter
from .pipaw_task_panel import PipawTaskPanel


@dataclass
class AgentStepResult:
    status: str
    operation_ref: str
    output: dict[str, Any] = field(default_factory=dict)
    deny_reason: str = ""


class PipawCsAgentRuntime:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root.resolve()
        self.panel = PipawTaskPanel(workspace_root)
        self.router = CapabilityServiceRouter(workspace_root)

    def _agent(self) -> dict:
        agent = self.panel.get_cs_agent()
        if not agent:
            raise ValueError("no cs agent in roster")
        return agent

    def run_current_step(self, *, tenant_id: str = "t-acme-demo") -> AgentStepResult:
        agent = self._agent()
        view = self.panel.build_view(
            tenant_id=tenant_id,
            assignee_role_id=agent["role_id"],
        )
        current = view.get("current")
        if not current:
            return AgentStepResult(status="idle", operation_ref="", deny_reason="NO_CURRENT_TASK")

        step = next((s for s in current["steps"] if s.get("current")), None)
        if not step or not step.get("operation_ref"):
            return AgentStepResult(status="done", operation_ref="")

        op_ref = step["operation_ref"]
        if op_ref not in agent.get("bound_operations", []):
            return AgentStepResult(
                status="denied",
                operation_ref=op_ref,
                deny_reason="OP_NOT_IN_ROSTER",
            )

        ctx = CapabilityInvokeContext(
            tenant_id=tenant_id,
            request_tenant_id=tenant_id,
            role_ids=[agent["role_id"]],
            product_track="pipaw",
        )
        payload = self._payload_for_step(step, current)
        resp = self.router.invoke(op_ref, payload, ctx)
        if resp.status == "ok":
            self.panel.advance_current_step()
        return AgentStepResult(
            status=resp.status,
            operation_ref=op_ref,
            output=resp.output,
            deny_reason=resp.deny_reason,
        )

    def _payload_for_step(self, step: dict, current: dict) -> dict[str, Any]:
        biz = current.get("business_context") or {}
        op = step.get("operation_ref", "")
        if op == "cs.customer.get_profile":
            return {"customer_id": biz.get("customer_id", "C-1001")}
        if op == "cs.ticket.create":
            return {
                "subject": "VIP 客诉：交付延期跟进",
                "customer_id": biz.get("customer_id", "C-1001"),
                "priority": current.get("priority", "high"),
            }
        if op == "cs.ticket.escalate":
            return {
                "ticket_id": biz.get("ticket_id", "TKT-mock-001"),
                "reason": "SLA at risk",
            }
        return {}
