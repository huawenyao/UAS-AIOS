"""
cs.customer — 客户语义能力服务
覆盖：线索资格判断 / 客户档案 / 联系人管理 / 客户评分
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LeadQualification:
    lead_id: str
    qualified: bool
    score: int            # 0-100
    budget_fit: bool
    authority_fit: bool
    need_fit: bool
    timeline_fit: bool
    disqualify_reasons: List[str]
    next_action: str


@dataclass
class CustomerProfile:
    customer_id: str
    name: str
    industry: str
    size: str             # SMB / MID / ENT
    health_score: int     # 0-100
    lifecycle_stage: str  # lead / opportunity / customer / churned
    arr: float
    csm_owner: str
    tags: List[str]


class CustomerService:
    """
    cs.customer 语义能力服务实现
    方法命名语义化，屏蔽底层 CRM 字段差异
    """

    def __init__(self, crm_connector=None):
        self._crm = crm_connector
        self._store: Dict[str, Any] = {}  # 本地模拟存储

    # ------------------------------------------------------------------
    # 线索管理
    # ------------------------------------------------------------------
    def qualify_lead(self, lead_data: Dict) -> LeadQualification:
        """BANT + ICP 资格判断"""
        budget = lead_data.get("budget_usd", 0)
        authority = lead_data.get("decision_maker", False)
        need_score = lead_data.get("pain_score", 0)
        timeline_months = lead_data.get("timeline_months", 99)

        budget_fit = budget >= 10000
        authority_fit = bool(authority)
        need_fit = need_score >= 6
        timeline_fit = timeline_months <= 6

        reasons = []
        if not budget_fit:
            reasons.append(f"预算不足: {budget} < 10000 USD")
        if not authority_fit:
            reasons.append("缺乏决策人参与")
        if not need_fit:
            reasons.append(f"需求紧迫度不足: pain_score={need_score}")
        if not timeline_fit:
            reasons.append(f"购买周期过长: {timeline_months}个月")

        qualified = len(reasons) == 0
        score = sum([budget_fit * 25, authority_fit * 25, need_fit * 25, timeline_fit * 25])

        next_action = (
            "安排需求诊断会议" if qualified
            else ("转入培育序列" if score >= 50 else "暂缓跟进")
        )

        return LeadQualification(
            lead_id=lead_data.get("lead_id", ""),
            qualified=qualified,
            score=score,
            budget_fit=budget_fit,
            authority_fit=authority_fit,
            need_fit=need_fit,
            timeline_fit=timeline_fit,
            disqualify_reasons=reasons,
            next_action=next_action,
        )

    def get_customer_profile(self, customer_id: str) -> Optional[CustomerProfile]:
        """获取客户档案"""
        if self._crm:
            raw = self._crm.get_customer(customer_id)
            return self._map_crm_to_profile(raw)
        return self._store.get(customer_id)

    def update_lifecycle_stage(self, customer_id: str, stage: str) -> bool:
        """更新客户生命周期阶段"""
        if customer_id in self._store:
            self._store[customer_id].lifecycle_stage = stage
            return True
        return False

    def calculate_health_score(self, customer_id: str, signals: Dict) -> int:
        """计算客户健康分（续费/流失预测）"""
        usage_score = min(signals.get("dau_ratio", 0) * 30, 30)
        engagement_score = min(signals.get("nps", 0) / 10 * 20, 20)
        payment_score = 20 if signals.get("payment_current", True) else 0
        support_penalty = max(0, 20 - signals.get("open_tickets", 0) * 5)
        expansion_score = 10 if signals.get("upsell_signal", False) else 0
        return int(usage_score + engagement_score + payment_score + support_penalty + expansion_score)

    # ------------------------------------------------------------------
    # 适配器调用入口（供 cs_gateway 路由）
    # ------------------------------------------------------------------
    def __call__(self, action: str, payload: Dict, context=None) -> Any:
        handlers = {
            "qualify_lead": lambda p: self.qualify_lead(p),
            "get_profile": lambda p: self.get_customer_profile(p["customer_id"]),
            "update_stage": lambda p: self.update_lifecycle_stage(p["customer_id"], p["stage"]),
            "health_score": lambda p: self.calculate_health_score(p["customer_id"], p.get("signals", {})),
        }
        handler = handlers.get(action)
        if not handler:
            raise ValueError(f"cs.customer: 未知 action={action}")
        result = handler(payload)
        if hasattr(result, "__dict__"):
            return vars(result)
        return result

    def _map_crm_to_profile(self, raw: Dict) -> CustomerProfile:
        return CustomerProfile(
            customer_id=raw.get("id", ""),
            name=raw.get("name", ""),
            industry=raw.get("industry", ""),
            size=raw.get("company_size", "SMB"),
            health_score=raw.get("health_score", 50),
            lifecycle_stage=raw.get("stage", "lead"),
            arr=raw.get("arr", 0.0),
            csm_owner=raw.get("owner", ""),
            tags=raw.get("tags", []),
        )
