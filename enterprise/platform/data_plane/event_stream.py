"""
企业事件流
职责：领域事件发布 / 订阅 / 回放 / Agent 触发
模型负责理解与生成；平台负责执行与合规（Agent 规划，确定性引擎执行）
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional
import uuid


@dataclass
class DomainEvent:
    """领域事件（不可变）"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""            # lead.qualified / quote.approved / payment.received ...
    aggregate_id: str = ""          # 关联业务对象 ID
    aggregate_type: str = ""        # Customer / Quote / Invoice / ...
    tenant_id: str = ""
    actor_id: str = ""              # 触发者（用户/Agent）
    payload: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    sequence: int = 0

    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "aggregate_type": self.aggregate_type,
            "tenant_id": self.tenant_id,
            "actor_id": self.actor_id,
            "payload": self.payload,
            "metadata": self.metadata,
            "occurred_at": self.occurred_at,
            "sequence": self.sequence,
        }


class EventStream:
    """
    领域事件流（内存实现，可换 Kafka/Pulsar 后端）
    支持：发布 / 多订阅 / 按类型过滤 / 回放
    """

    def __init__(self):
        self._events: List[DomainEvent] = []
        self._subscribers: Dict[str, List[Callable]] = {}
        self._sequence = 0

    def publish(self, event: DomainEvent) -> DomainEvent:
        """发布领域事件"""
        self._sequence += 1
        event.sequence = self._sequence
        self._events.append(event)

        # 通知订阅者
        handlers = (
            self._subscribers.get(event.event_type, []) +
            self._subscribers.get("*", [])  # 通配符订阅
        )
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass  # 订阅者错误不影响主流程

        return event

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """订阅事件类型（支持 * 通配）"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def replay(
        self,
        event_type: Optional[str] = None,
        aggregate_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        from_sequence: int = 0,
    ) -> List[DomainEvent]:
        """事件回放"""
        results = [e for e in self._events if e.sequence >= from_sequence]
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if aggregate_id:
            results = [e for e in results if e.aggregate_id == aggregate_id]
        if tenant_id:
            results = [e for e in results if e.tenant_id == tenant_id]
        return sorted(results, key=lambda e: e.sequence)

    def get_aggregate_history(self, aggregate_id: str) -> List[DomainEvent]:
        """获取业务对象完整事件历史"""
        return self.replay(aggregate_id=aggregate_id)

    # ------------------------------------------------------------------
    # 标准领域事件工厂方法
    # ------------------------------------------------------------------
    def emit_lead_qualified(self, lead_id: str, tenant_id: str, actor_id: str, data: Dict) -> DomainEvent:
        return self.publish(DomainEvent(
            event_type="lead.qualified",
            aggregate_id=lead_id,
            aggregate_type="Lead",
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload=data,
        ))

    def emit_quote_approved(self, quote_id: str, tenant_id: str, actor_id: str, data: Dict) -> DomainEvent:
        return self.publish(DomainEvent(
            event_type="quote.approved",
            aggregate_id=quote_id,
            aggregate_type="Quote",
            tenant_id=tenant_id,
            actor_id=actor_id,
            payload=data,
        ))

    def emit_payment_received(self, invoice_id: str, tenant_id: str, amount: float) -> DomainEvent:
        return self.publish(DomainEvent(
            event_type="payment.received",
            aggregate_id=invoice_id,
            aggregate_type="Invoice",
            tenant_id=tenant_id,
            actor_id="system",
            payload={"amount": amount},
        ))
