"""
L3 销售顾问 Agent
经营向外：获 → 转 → 服 → 续
B2B 顾问式销售：资格判断 → 需求诊断 → 报价 → 审批 → 签单
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List
import uuid

from .business_agent import BusinessAgent, BusinessOpportunity


@dataclass
class SalesActivity:
    """销售活动记录"""
    activity_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    opp_id: str = ""
    type: str = ""      # call / meeting / email / demo / proposal
    summary: str = ""
    outcome: str = ""   # positive / neutral / negative
    next_action: str = ""
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SalesAgent(BusinessAgent):
    """
    销售顾问数字人（L3 经营 Agent）
    核心能力：
    - 线索资格判断（BANT + ICP）
    - 顾问式需求诊断
    - 报价生成 + 审批流转
    - 合规审查（G6）
    - 商机管道管理
    """

    STAGE_PROGRESSION = [
        "qualification", "needs_analysis", "proposal",
        "negotiation", "legal_review", "closed_won", "closed_lost",
    ]

    def __init__(self, tenant_id: str, cs_gateway=None, event_stream=None, sla_monitor=None):
        super().__init__(
            agent_id="l3_sales_agent",
            tenant_id=tenant_id,
            cs_gateway=cs_gateway,
            event_stream=event_stream,
            sla_monitor=sla_monitor,
        )
        perm = getattr(self._gateway, "_permission", None)
        if perm:
            perm.assign_roles(self.agent_id, ["l3_agent", "system_agent"])

    # ------------------------------------------------------------------
    # 官网留资 → 完整销售流程
    # ------------------------------------------------------------------
    def handle_inbound(self, source: str, data: Dict) -> Dict:
        """
        处理入站线索
        source: website / referral / outbound / channel
        """
        opp = BusinessOpportunity(
            customer_id=data.get("company", data.get("email", str(uuid.uuid4()))),
            stage="qualification",
            funnel_stage="acquire",
            owner_agent_id=self.agent_id,
        )

        # 步骤1：线索资格判断
        lead_data = {
            "lead_id": opp.opp_id,
            "budget_usd": data.get("budget_usd", 0),
            "decision_maker": data.get("is_decision_maker", False),
            "pain_score": data.get("pain_score", 0),
            "timeline_months": data.get("timeline_months", 12),
        }
        qualification = self.call_service("cs.customer", "qualify_lead", lead_data)
        opp.activities.append({"type": "qualification", "result": qualification})

        if not qualification.get("qualified", False):
            opp.stage = "disqualified"
            opp.funnel_stage = "acquire"
            self._opportunities[opp.opp_id] = opp
            return {
                "opp_id": opp.opp_id,
                "status": "disqualified",
                "score": qualification.get("score", 0),
                "reasons": qualification.get("disqualify_reasons", []),
                "next_action": qualification.get("next_action", "转入培育"),
            }

        # 资格通过 → 推进到需求诊断
        opp.stage = "needs_analysis"
        opp.funnel_stage = "convert"
        opp.amount = data.get("budget_usd", 0)
        opp.probability = qualification.get("score", 50)
        self._opportunities[opp.opp_id] = opp
        self.emit_pipeline_event("opportunity.qualified", opp, {"source": source})

        return {
            "opp_id": opp.opp_id,
            "status": "qualified",
            "stage": opp.stage,
            "score": qualification.get("score"),
            "next_action": "安排需求诊断会议",
        }

    def diagnose_needs(self, opp_id: str, meeting_notes: Dict) -> Dict:
        """需求诊断"""
        opp = self._get_opp(opp_id)
        diagnosis = {
            "pain_points": meeting_notes.get("pain_points", []),
            "desired_outcomes": meeting_notes.get("desired_outcomes", []),
            "technical_requirements": meeting_notes.get("tech_reqs", []),
            "decision_process": meeting_notes.get("decision_process", ""),
            "competition": meeting_notes.get("competition", []),
        }
        opp.activities.append({"type": "needs_diagnosis", "result": diagnosis})
        opp.stage = "proposal"
        opp.funnel_stage = "convert"
        self.emit_pipeline_event("opportunity.needs_analyzed", opp)
        return {"opp_id": opp_id, "stage": "proposal", "diagnosis": diagnosis}

    def create_quote(self, opp_id: str, line_items: List[Dict], discount_pct: float = 0) -> Dict:
        """创建报价单"""
        opp = self._get_opp(opp_id)

        # 合规检查（G6 审查）
        compliance = self.compliance_check("create_quote", {
            "discount_pct": discount_pct,
            "amount": sum(i.get("unit_price", 0) * i.get("quantity", 1) for i in line_items),
        })
        if not compliance["passed"]:
            return {
                "status": "compliance_blocked",
                "violations": compliance["violations"],
            }

        # 创建报价
        quote = self.call_service("cs.finance", "create_quote", {
            "customer_id": opp.customer_id,
            "opportunity_id": opp_id,
            "line_items": line_items,
            "discount_pct": discount_pct,
        })
        opp.activities.append({"type": "quote_created", "quote_id": quote.get("quote_id")})
        opp.amount = quote.get("net_amount", 0)

        # 提交审批
        approval = self.call_service("cs.approval", "create", {
            "type": "quote",
            "subject": f"报价单审批 - {opp.customer_id}",
            "requester_id": self.agent_id,
            "amount": opp.amount,
            "discount_pct": discount_pct,
        })
        self.emit_pipeline_event("opportunity.quote_created", opp, {
            "quote_id": quote.get("quote_id"),
            "approval_id": approval.get("task_id"),
        })

        return {
            "opp_id": opp_id,
            "quote_id": quote.get("quote_id"),
            "net_amount": quote.get("net_amount"),
            "approval_id": approval.get("task_id"),
            "approval_status": approval.get("status"),
            "stage": "proposal",
        }

    def advance_to_close(self, opp_id: str, approval_data: Dict) -> Dict:
        """推进到成交"""
        opp = self._get_opp(opp_id)
        if approval_data.get("status") == "approved":
            opp.stage = "negotiation"
            opp.funnel_stage = "convert"
            self.emit_pipeline_event("opportunity.approved", opp)
            return {"opp_id": opp_id, "stage": "negotiation", "next_action": "发送合同"}
        else:
            return {
                "opp_id": opp_id,
                "stage": "proposal",
                "next_action": "修改报价后重新提交",
                "rejection_reason": approval_data.get("reason", ""),
            }

    def close_won(self, opp_id: str, contract_data: Dict) -> Dict:
        """赢单"""
        opp = self._get_opp(opp_id)
        opp.stage = "closed_won"
        opp.funnel_stage = "serve"
        opp.probability = 100
        self.emit_pipeline_event("opportunity.closed_won", opp, {"contract": contract_data})

        # 触发履约流程
        bpm = self.call_service("cs.bpm", "start", {
            "process_key": "onboarding",
            "variables": {
                "customer_id": opp.customer_id,
                "contract_value": opp.amount,
                "opp_id": opp_id,
            },
        })

        return {
            "opp_id": opp_id,
            "status": "won",
            "amount": opp.amount,
            "onboarding_process_id": bpm.get("instance_id", ""),
            "next_action": "客户成功交接",
        }

    def _get_opp(self, opp_id: str) -> BusinessOpportunity:
        if opp_id not in self._opportunities:
            raise ValueError(f"商机不存在: {opp_id}")
        return self._opportunities[opp_id]
