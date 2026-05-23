"""
L3 投标 / 合规 Agent
职责：专业写作 · 红线拦截 · 投标管理
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List
import uuid

from .business_agent import BusinessAgent, BusinessOpportunity


@dataclass
class BidProject:
    """投标项目"""
    bid_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str = ""
    customer_id: str = ""
    bid_amount: float = 0.0
    deadline: str = ""
    status: str = "preparing"  # preparing / submitted / won / lost
    compliance_checked: bool = False
    documents: List[str] = field(default_factory=list)
    red_lines: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BiddingAgent(BusinessAgent):
    """
    投标 / 合规数字人（L3 经营 Agent）
    核心能力：专业写作 / 红线拦截 / 资质管理
    """

    def __init__(self, tenant_id: str, cs_gateway=None, event_stream=None, sla_monitor=None):
        super().__init__(
            agent_id="l3_bidding_agent",
            tenant_id=tenant_id,
            cs_gateway=cs_gateway,
            event_stream=event_stream,
            sla_monitor=sla_monitor,
        )
        self._bids: Dict[str, BidProject] = {}
        perm = getattr(self._gateway, "_permission", None)
        if perm:
            perm.assign_roles(self.agent_id, ["l3_agent"])

    def handle_inbound(self, source: str, data: Dict) -> Dict:
        """处理投标邀请"""
        bid = BidProject(
            project_name=data.get("project_name", ""),
            customer_id=data.get("customer_id", ""),
            bid_amount=data.get("estimated_value", 0),
            deadline=data.get("deadline", ""),
        )
        self._bids[bid.bid_id] = bid

        # 红线检查
        red_lines = self._check_red_lines(data)
        bid.red_lines = red_lines

        if red_lines:
            bid.status = "red_line_blocked"
            return {
                "bid_id": bid.bid_id,
                "status": "blocked",
                "red_lines": red_lines,
                "action": "需要法务确认后方可投标",
            }

        return {
            "bid_id": bid.bid_id,
            "status": "preparing",
            "project": data.get("project_name", ""),
            "next_steps": ["收集资质文件", "撰写技术方案", "财务报价"],
        }

    def write_technical_proposal(self, bid_id: str, requirements: Dict) -> Dict:
        """撰写技术方案（专业写作能力）"""
        bid = self._bids.get(bid_id)
        if not bid:
            raise ValueError(f"投标项目不存在: {bid_id}")

        sections = {
            "executive_summary": self._write_executive_summary(requirements),
            "technical_solution": self._write_technical_solution(requirements),
            "implementation_plan": self._write_implementation_plan(requirements),
            "team_qualifications": self._write_team_section(requirements),
            "pricing_strategy": self._write_pricing(requirements, bid.bid_amount),
        }
        bid.documents.append("technical_proposal")

        return {
            "bid_id": bid_id,
            "proposal": sections,
            "word_count": sum(len(v) for v in sections.values()),
        }

    def submit_bid(self, bid_id: str, submission_data: Dict) -> Dict:
        """提交投标"""
        bid = self._bids.get(bid_id)
        if not bid:
            raise ValueError(f"投标项目不存在: {bid_id}")

        # 最终合规检查
        compliance = self.compliance_check("submit_bid", submission_data)
        if not compliance["passed"]:
            return {"status": "compliance_blocked", "violations": compliance["violations"]}

        bid.compliance_checked = True
        bid.status = "submitted"

        opp = BusinessOpportunity(
            customer_id=bid.customer_id,
            stage="proposal",
            funnel_stage="convert",
            amount=bid.bid_amount,
            owner_agent_id=self.agent_id,
        )
        self._opportunities[opp.opp_id] = opp
        self.emit_pipeline_event("bid.submitted", opp, {"bid_id": bid_id})

        return {"bid_id": bid_id, "status": "submitted", "opp_id": opp.opp_id}

    def _check_red_lines(self, data: Dict) -> List[str]:
        red_lines = []
        if data.get("foreign_entity", False):
            red_lines.append("涉及境外主体，需合规审查")
        if data.get("state_secret_involved", False):
            red_lines.append("涉及国家秘密，禁止参与")
        if data.get("conflict_of_interest", False):
            red_lines.append("存在利益冲突，需申报")
        return red_lines

    def _write_executive_summary(self, req: Dict) -> str:
        return f"执行摘要：针对 {req.get('project_name', '本项目')} 的需求，我方提供全面的解决方案，以专业能力和成熟经验保障项目成功交付。"

    def _write_technical_solution(self, req: Dict) -> str:
        return f"技术方案：基于 {req.get('tech_stack', '云原生')} 架构，结合 AI 能力，设计高可用、可扩展的系统架构。"

    def _write_implementation_plan(self, req: Dict) -> str:
        return "实施计划：分三阶段推进。阶段一（1-2月）：需求确认与环境搭建；阶段二（3-4月）：核心功能开发；阶段三（5-6月）：测试验收与上线。"

    def _write_team_section(self, req: Dict) -> str:
        return "团队资质：项目团队由具备10年以上行业经验的资深专家组成，持有相关认证资质。"

    def _write_pricing(self, req: Dict, base_amount: float) -> str:
        return f"报价策略：总报价 {base_amount:,.0f} 元，包含实施费、授权费及首年维保，提供多种付款方式。"
