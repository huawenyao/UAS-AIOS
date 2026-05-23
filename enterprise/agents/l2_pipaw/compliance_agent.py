"""
L2 合规数字人
职责：专业写作 · 红线拦截 · 合规审查 · 风险评估
"""
from __future__ import annotations
from typing import Any, Dict

from .functional_agent import FunctionalAgent, AgentTask
from ...platform.governance.compliance_rules import ComplianceEngine


class ComplianceAgent(FunctionalAgent):
    """
    合规数字人
    核心能力：红线拦截 / 合规审查 / 合同专业写作
    """

    def __init__(self, tenant_id: str, cs_gateway=None, event_stream=None, sla_monitor=None):
        super().__init__(
            agent_id="l2_compliance_agent",
            tenant_id=tenant_id,
            cs_gateway=cs_gateway,
            event_stream=event_stream,
            sla_monitor=sla_monitor,
        )
        self._compliance = ComplianceEngine()
        perm = getattr(self._gateway, "_permission", None)
        if perm:
            perm.assign_roles(self.agent_id, ["l2_user", "approver"])

    def _do_execute(self, task: AgentTask) -> Any:
        task_type = task.task_type or task.payload.get("task_type", "")
        dispatchers = {
            "compliance_check": self._compliance_check,
            "contract_review": self._contract_review,
            "risk_assessment": self._risk_assessment,
        }
        handler = dispatchers.get(task_type, self._default_handler)
        return handler(task)

    def _compliance_check(self, task: AgentTask) -> Dict:
        """合规红线检查"""
        payload = task.payload
        passed, violations = self._compliance.check(task.task_type, payload)
        self.add_step(task, "compliance_check", {
            "passed": passed,
            "violations": [vars(v) for v in violations],
        })
        return {
            "passed": passed,
            "violations": [{"rule_id": v.rule_id, "severity": v.severity, "description": v.description, "remedy": v.remedy} for v in violations],
            "recommendation": "通过合规检查" if passed else f"发现 {len(violations)} 项违规，请按建议修改",
        }

    def _contract_review(self, task: AgentTask) -> Dict:
        """合同合规审查"""
        payload = task.payload
        contract_value = payload.get("contract_value", 0)
        issues = []

        if contract_value >= 1000000 and not payload.get("legal_reviewed"):
            issues.append({"type": "LEGAL_REVIEW_REQUIRED", "desc": "超百万合同需法务审核"})
        if not payload.get("sla_defined"):
            issues.append({"type": "SLA_MISSING", "desc": "合同未定义 SLA 条款"})
        if not payload.get("termination_clause"):
            issues.append({"type": "TERMINATION_CLAUSE_MISSING", "desc": "缺少终止条款"})

        risk_level = "high" if any(i["type"] == "LEGAL_REVIEW_REQUIRED" for i in issues) else ("medium" if issues else "low")
        self.add_step(task, "contract_review", {"issues": issues, "risk_level": risk_level})

        return {
            "contract_value": contract_value,
            "issues": issues,
            "risk_level": risk_level,
            "approved": risk_level == "low",
            "review_notes": f"合同风险等级: {risk_level}，发现 {len(issues)} 项问题",
        }

    def _risk_assessment(self, task: AgentTask) -> Dict:
        """风险评估"""
        payload = task.payload
        risk_factors = []

        if payload.get("new_customer", True):
            risk_factors.append({"factor": "新客户风险", "weight": 0.3})
        if payload.get("cross_border", False):
            risk_factors.append({"factor": "跨境合规风险", "weight": 0.4})
        if payload.get("large_discount", False):
            risk_factors.append({"factor": "大折扣利润风险", "weight": 0.3})

        total_risk = sum(f["weight"] for f in risk_factors)
        level = "high" if total_risk > 0.6 else ("medium" if total_risk > 0.3 else "low")

        return {"risk_score": total_risk, "risk_level": level, "factors": risk_factors}

    def _default_handler(self, task: AgentTask) -> Dict:
        return {"status": "acknowledged", "note": "合规数字人已接收任务"}
