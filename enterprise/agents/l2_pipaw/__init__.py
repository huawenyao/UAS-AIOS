"""L2 职能数字人 — ΠPaw 内部跨部门"""
from .functional_agent import FunctionalAgent, AgentTask
from .hr_agent import HRAgent
from .finance_agent import FinanceAgent
from .compliance_agent import ComplianceAgent

__all__ = ["FunctionalAgent", "AgentTask", "HRAgent", "FinanceAgent", "ComplianceAgent"]
