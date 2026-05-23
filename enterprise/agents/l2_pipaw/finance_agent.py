"""
L2 财务数字人
职责：精确计算 · 账期管理 · KPI 归因 · 经营分析
调用：cs.invoice.* / cs.finance.* / cs.approval.*
"""
from __future__ import annotations
from typing import Any, Dict

from .functional_agent import FunctionalAgent, AgentTask


class FinanceAgent(FunctionalAgent):
    """
    财务数字人
    核心能力：开票处理 / 回款跟进 / 经营分析 / KPI 归因
    """

    def __init__(self, tenant_id: str, cs_gateway=None, event_stream=None, sla_monitor=None):
        super().__init__(
            agent_id="l2_finance_agent",
            tenant_id=tenant_id,
            cs_gateway=cs_gateway,
            event_stream=event_stream,
            sla_monitor=sla_monitor,
        )
        # 注册权限
        perm = getattr(self._gateway, "_permission", None)
        if perm:
            perm.assign_roles(self.agent_id, ["finance", "l2_user", "system_agent"])

    def _do_execute(self, task: AgentTask) -> Any:
        task_type = task.task_type or task.payload.get("task_type", "")

        dispatchers = {
            "process_invoice": self._process_invoice,
            "collect_payment": self._collect_payment,
            "kpi_attribution": self._kpi_attribution,
            "business_analysis": self._business_analysis,
            "overdue_check": self._overdue_check,
        }

        handler = dispatchers.get(task_type, self._default_handler)
        return handler(task)

    def _process_invoice(self, task: AgentTask) -> Dict:
        """处理开票申请"""
        payload = task.payload
        # 步骤1：创建发票
        invoice = self.call_service("cs.invoice", "create", {
            "order_id": payload.get("order_id", ""),
            "customer_id": payload.get("customer_id", ""),
            "amount": payload.get("amount", 0),
            "invoice_type": payload.get("invoice_type", "vat_normal"),
            "items": payload.get("items", [{"description": "服务费", "unit_price": payload.get("amount", 0), "quantity": 1}]),
        })
        self.add_step(task, "create_invoice", invoice)

        # 步骤2：提交审核
        submitted = self.call_service("cs.invoice", "submit", {
            "invoice_id": invoice["invoice_id"],
        })
        self.add_step(task, "submit_invoice", submitted)

        return {"invoice_id": invoice["invoice_id"], "status": "submitted", "amount": invoice["total_amount"]}

    def _collect_payment(self, task: AgentTask) -> Dict:
        """登记回款"""
        payload = task.payload
        payment = self.call_service("cs.invoice", "record_payment", {
            "invoice_id": payload["invoice_id"],
            "amount": payload["amount"],
            "method": payload.get("method", "bank_transfer"),
            "bank_flow_id": payload.get("bank_flow_id", ""),
        })
        self.add_step(task, "record_payment", payment)

        # 确认收入
        if payload.get("recognize_revenue", True):
            kpi = self.call_service("cs.finance", "kpi_attribution", {
                "order_id": payload.get("order_id", ""),
                "amount": payload["amount"],
                "revenue_type": payload.get("revenue_type", "new"),
                "ae_id": payload.get("ae_id", ""),
                "csm_id": payload.get("csm_id", ""),
            })
            self.add_step(task, "kpi_attribution", kpi)
            return {"payment_id": payment["payment_id"], "kpi": kpi}

        return {"payment_id": payment["payment_id"]}

    def _kpi_attribution(self, task: AgentTask) -> Dict:
        """KPI 归因计算"""
        return self.call_service("cs.finance", "kpi_attribution", task.payload)

    def _business_analysis(self, task: AgentTask) -> Dict:
        """经营分析"""
        return self.call_service("cs.finance", "business_analysis", {
            "period": task.payload.get("period", "current"),
        })

    def _overdue_check(self, task: AgentTask) -> Dict:
        """逾期检查"""
        overdue = self.call_service("cs.invoice", "check_overdue", {})
        return {"overdue_count": len(overdue) if isinstance(overdue, list) else 0, "details": overdue}

    def _default_handler(self, task: AgentTask) -> Dict:
        return {"status": "acknowledged", "task_id": task.task_id, "note": "财务数字人已接收任务"}

    def _get_sla_hours(self, task: AgentTask) -> int:
        sla_map = {
            "process_invoice": 2,
            "collect_payment": 1,
            "business_analysis": 4,
        }
        return sla_map.get(task.task_type, 4)
