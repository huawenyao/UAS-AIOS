"""
L3 经营 Agent 基类
经营向外 = 触达 × 履约 × 决策 × 调度
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from ...platform.capability_services.cs_gateway import CapabilityServiceGateway, CSRequest
from ...platform.data_plane.event_stream import EventStream, DomainEvent
from ...platform.governance.compliance_rules import ComplianceEngine
from ...platform.governance.sla_monitor import SLAMonitor


@dataclass
class BusinessOpportunity:
    """业务机会（贯穿 L3 生命周期）"""
    opp_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str = ""
    stage: str = "qualification"
    # 获客 → 转化 → 服务 → 续费
    funnel_stage: str = "acquire"  # acquire / convert / serve / retain
    amount: float = 0.0
    probability: int = 0
    owner_agent_id: str = ""
    activities: List[Dict] = field(default_factory=list)
    pipeline_events: List[Dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BusinessAgent(ABC):
    """
    L3 经营 Agent 抽象基类
    经营数字岗位：销售顾问 / 客服 / 投标 / 渠道
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
        self._compliance = ComplianceEngine()
        self._opportunities: Dict[str, BusinessOpportunity] = {}
        self._pipeline_events: List[DomainEvent] = []

    def call_service(self, service: str, action: str, payload: Dict) -> Any:
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

    def compliance_check(self, action: str, payload: Dict) -> Dict:
        """执行前合规检查"""
        passed, violations = self._compliance.check(action, payload)
        return {
            "passed": passed,
            "violations": [vars(v) for v in violations],
        }

    def emit_pipeline_event(self, event_type: str, opp: BusinessOpportunity, data: Dict = None):
        event = self._event_stream.publish(DomainEvent(
            event_type=event_type,
            aggregate_id=opp.opp_id,
            aggregate_type="Opportunity",
            tenant_id=self.tenant_id,
            actor_id=self.agent_id,
            payload={"stage": opp.stage, "amount": opp.amount, **(data or {})},
        ))
        self._pipeline_events.append(event)
        opp.updated_at = datetime.now(timezone.utc).isoformat()

    def get_pipeline_summary(self) -> Dict:
        """获取商机管道汇总"""
        opps = list(self._opportunities.values())
        return {
            "total_opportunities": len(opps),
            "total_value": sum(o.amount for o in opps),
            "by_stage": self._count_by_stage(opps),
            "by_funnel": self._count_by_funnel(opps),
        }

    def _count_by_stage(self, opps: List[BusinessOpportunity]) -> Dict:
        counts: Dict[str, int] = {}
        for o in opps:
            counts[o.stage] = counts.get(o.stage, 0) + 1
        return counts

    def _count_by_funnel(self, opps: List[BusinessOpportunity]) -> Dict:
        counts: Dict[str, int] = {}
        for o in opps:
            counts[o.funnel_stage] = counts.get(o.funnel_stage, 0) + 1
        return counts

    @abstractmethod
    def handle_inbound(self, source: str, data: Dict) -> Dict:
        """处理入站事件（官网留资/客服咨询/投标邀请）"""
        raise NotImplementedError
