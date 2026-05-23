"""
L3 客服 / 履约 Agent
职责：共情 + SLA 管理 + 流程推进
经营向外：服 + 续
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid

from .business_agent import BusinessAgent, BusinessOpportunity


@dataclass
class ServiceTicket:
    """服务工单"""
    ticket_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str = ""
    type: str = ""        # complaint / question / bug / feature_request / churn_risk
    priority: str = "normal"   # urgent / high / normal / low
    title: str = ""
    description: str = ""
    sentiment: str = "neutral"  # frustrated / neutral / satisfied
    status: str = "open"
    assigned_to: str = ""
    sla_hours: int = 24
    resolution: Optional[str] = None
    escalation_path: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: Optional[str] = None


class CustomerServiceAgent(BusinessAgent):
    """
    客服 / 履约数字人（L3 经营 Agent）
    核心能力：
    - 共情式接待（情绪识别）
    - SLA 分级处理
    - 流程推进（入职/交付/续费）
    - 流失预警 → 升级
    """

    def __init__(self, tenant_id: str, cs_gateway=None, event_stream=None, sla_monitor=None):
        super().__init__(
            agent_id="l3_cs_agent",
            tenant_id=tenant_id,
            cs_gateway=cs_gateway,
            event_stream=event_stream,
            sla_monitor=sla_monitor,
        )
        self._tickets: Dict[str, ServiceTicket] = {}
        perm = getattr(self._gateway, "_permission", None)
        if perm:
            perm.assign_roles(self.agent_id, ["l3_agent", "system_agent"])

    def handle_inbound(self, source: str, data: Dict) -> Dict:
        """处理客户咨询/投诉"""
        sentiment = self._detect_sentiment(data.get("message", ""))
        ticket_type = self._classify_ticket(data.get("message", ""), data.get("type", ""))
        priority = self._determine_priority(sentiment, ticket_type, data)

        ticket = ServiceTicket(
            customer_id=data.get("customer_id", ""),
            type=ticket_type,
            priority=priority,
            title=data.get("subject", data.get("message", "")[:50]),
            description=data.get("message", ""),
            sentiment=sentiment,
            assigned_to=self.agent_id,
            sla_hours=self._get_sla(priority),
        )
        self._tickets[ticket.ticket_id] = ticket

        # 注册 SLA
        self._sla.register(ticket_type, self.agent_id, ticket.sla_hours)

        # 高优先级 / 负面情绪 → 立即升级
        if priority == "urgent" or sentiment == "frustrated":
            return self._handle_urgent(ticket, data)

        # 流失风险 → 特别处理
        if ticket_type == "churn_risk":
            return self._handle_churn_risk(ticket, data)

        return {
            "ticket_id": ticket.ticket_id,
            "status": "created",
            "priority": priority,
            "sla_hours": ticket.sla_hours,
            "auto_response": self._generate_empathy_response(sentiment, ticket_type),
        }

    def resolve_ticket(self, ticket_id: str, resolution: str) -> Dict:
        """解决工单"""
        ticket = self._get_ticket(ticket_id)
        ticket.status = "resolved"
        ticket.resolution = resolution
        ticket.resolved_at = datetime.now(timezone.utc).isoformat()

        # 更新客户健康分
        signals = {"open_tickets": len([t for t in self._tickets.values() if t.status == "open"])}
        try:
            self.call_service("cs.customer", "health_score", {
                "customer_id": ticket.customer_id,
                "signals": signals,
            })
        except Exception:
            pass

        return {"ticket_id": ticket_id, "status": "resolved", "resolution": resolution}

    def check_renewal_opportunity(self, customer_id: str) -> Dict:
        """检查续费机会"""
        try:
            profile = self.call_service("cs.customer", "get_profile", {"customer_id": customer_id})
            self.call_service("cs.invoice", "ar_summary", {"customer_id": customer_id})

            if profile:
                health = profile.get("health_score", 0) if isinstance(profile, dict) else 0
                renewal_risk = "high" if health < 40 else ("medium" if health < 70 else "low")

                # 健康分低 → 创建流失预警意图单
                opp = BusinessOpportunity(
                    customer_id=customer_id,
                    stage="renewal_review",
                    funnel_stage="retain",
                    amount=profile.get("arr", 0) if isinstance(profile, dict) else 0,
                    owner_agent_id=self.agent_id,
                )
                self._opportunities[opp.opp_id] = opp
                self.emit_pipeline_event("renewal.risk_assessed", opp, {"risk": renewal_risk})

                return {
                    "customer_id": customer_id,
                    "renewal_risk": renewal_risk,
                    "health_score": health,
                    "arr": opp.amount,
                    "next_action": "安排续费 QBR 会议" if renewal_risk != "high" else "紧急客户挽留干预",
                }
        except Exception:
            pass

        return {"customer_id": customer_id, "renewal_risk": "unknown", "next_action": "补充客户信息"}

    def _handle_urgent(self, ticket: ServiceTicket, data: Dict) -> Dict:
        """紧急处理"""
        ticket.escalation_path.append(self.agent_id)
        ticket.escalation_path.append("l2_ops_manager")
        return {
            "ticket_id": ticket.ticket_id,
            "status": "escalated",
            "priority": "urgent",
            "sla_hours": 1,
            "escalated_to": "l2_ops_manager",
            "auto_response": "您好！您的问题已被标记为紧急，我们的专属顾问将在1小时内联系您。",
        }

    def _handle_churn_risk(self, ticket: ServiceTicket, data: Dict) -> Dict:
        """流失风险处理"""
        return {
            "ticket_id": ticket.ticket_id,
            "status": "churn_risk_flagged",
            "actions": ["安排 CSM 紧急跟进", "准备挽留方案", "申请特殊优惠授权"],
        }

    def _detect_sentiment(self, message: str) -> str:
        negative_words = ["失望", "投诉", "差", "无法接受", "要退", "取消", "不行", "问题严重"]
        positive_words = ["满意", "很好", "感谢", "赞", "推荐"]
        if any(w in message for w in negative_words):
            return "frustrated"
        if any(w in message for w in positive_words):
            return "satisfied"
        return "neutral"

    def _classify_ticket(self, message: str, explicit_type: str) -> str:
        if explicit_type and explicit_type != "unknown":
            return explicit_type
        if any(w in message for w in ["退", "取消", "不续", "考虑离开"]):
            return "churn_risk"
        if any(w in message for w in ["错误", "故障", "不能用", "报错"]):
            return "bug"
        if any(w in message for w in ["投诉", "差评", "不满意"]):
            return "complaint"
        return "question"

    def _determine_priority(self, sentiment: str, ticket_type: str, data: Dict) -> str:
        if ticket_type in ("churn_risk", "complaint") and sentiment == "frustrated":
            return "urgent"
        if ticket_type in ("bug", "complaint"):
            return "high"
        return "normal"

    def _get_sla(self, priority: str) -> int:
        return {"urgent": 1, "high": 4, "normal": 24, "low": 72}.get(priority, 24)

    def _generate_empathy_response(self, sentiment: str, ticket_type: str) -> str:
        responses = {
            "frustrated": "非常抱歉给您带来了不便，我们高度重视您的问题，将优先为您处理。",
            "neutral": "感谢您联系我们，我们已收到您的请求，将尽快跟进处理。",
            "satisfied": "感谢您的反馈！我们很高兴为您服务，有任何需要请随时联系。",
        }
        return responses.get(sentiment, responses["neutral"])

    def _get_ticket(self, ticket_id: str) -> ServiceTicket:
        if ticket_id not in self._tickets:
            raise ValueError(f"工单不存在: {ticket_id}")
        return self._tickets[ticket_id]
