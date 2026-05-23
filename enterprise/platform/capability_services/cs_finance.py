"""
cs.finance — 财务语义能力服务
覆盖：报价生成 / 合同金额 / 收入确认 / KPI 归因 / 经营分析
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid


@dataclass
class Quote:
    quote_id: str
    customer_id: str
    opportunity_id: str
    line_items: List[Dict]
    subtotal: float
    discount_pct: float
    discount_amount: float
    net_amount: float
    valid_days: int
    status: str           # draft / pending_approval / approved / sent / accepted / rejected
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RevenueRecord:
    record_id: str
    customer_id: str
    order_id: str
    recognized_amount: float
    recognition_date: str
    revenue_type: str     # new / expansion / renewal
    kpi_attribution: Dict  # {ae_id, csm_id, channel, region}


class FinanceService:
    """
    cs.finance 财务语义服务
    精确计算、资源博弈、KPI 归因
    """

    def __init__(self):
        self._quotes: Dict[str, Quote] = {}
        self._revenue: Dict[str, RevenueRecord] = {}

    def create_quote(
        self,
        customer_id: str,
        opportunity_id: str,
        line_items: List[Dict],
        discount_pct: float = 0.0,
        valid_days: int = 30,
    ) -> Quote:
        """生成报价单"""
        subtotal = sum(item.get("unit_price", 0) * item.get("quantity", 1) for item in line_items)
        discount_amount = round(subtotal * discount_pct / 100, 2)
        net_amount = round(subtotal - discount_amount, 2)

        quote = Quote(
            quote_id=str(uuid.uuid4()),
            customer_id=customer_id,
            opportunity_id=opportunity_id,
            line_items=line_items,
            subtotal=subtotal,
            discount_pct=discount_pct,
            discount_amount=discount_amount,
            net_amount=net_amount,
            valid_days=valid_days,
            status="draft",
        )
        self._quotes[quote.quote_id] = quote
        return quote

    def approve_quote(self, quote_id: str, approval_id: str) -> Quote:
        """报价审批通过"""
        q = self._get_quote(quote_id)
        q.status = "approved"
        return q

    def recognize_revenue(
        self,
        order_id: str,
        customer_id: str,
        amount: float,
        revenue_type: str,
        attribution: Dict,
    ) -> RevenueRecord:
        """确认收入并归因"""
        record = RevenueRecord(
            record_id=str(uuid.uuid4()),
            customer_id=customer_id,
            order_id=order_id,
            recognized_amount=amount,
            recognition_date=datetime.now(timezone.utc).date().isoformat(),
            revenue_type=revenue_type,
            kpi_attribution=attribution,
        )
        self._revenue[record.record_id] = record
        return record

    def calculate_kpi_attribution(self, order_data: Dict) -> Dict:
        """
        KPI 归因计算
        规则：新签=AE 100%；扩展=CSM 70% + AE 30%；续费=CSM 100%
        """
        rev_type = order_data.get("revenue_type", "new")
        amount = order_data.get("amount", 0)
        ae_id = order_data.get("ae_id")
        csm_id = order_data.get("csm_id")

        if rev_type == "new":
            return {"ae_id": ae_id, "ae_amount": amount, "csm_id": csm_id, "csm_amount": 0}
        elif rev_type == "expansion":
            return {
                "ae_id": ae_id, "ae_amount": round(amount * 0.3, 2),
                "csm_id": csm_id, "csm_amount": round(amount * 0.7, 2),
            }
        else:  # renewal
            return {"ae_id": ae_id, "ae_amount": 0, "csm_id": csm_id, "csm_amount": amount}

    def business_analysis(self, period: str, filters: Dict = None) -> Dict:
        """经营分析：ARR / NRR / 管道健康"""
        revenue_records = list(self._revenue.values())
        total_arr = sum(r.recognized_amount for r in revenue_records if r.revenue_type == "renewal")
        new_arr = sum(r.recognized_amount for r in revenue_records if r.revenue_type == "new")
        expansion_arr = sum(r.recognized_amount for r in revenue_records if r.revenue_type == "expansion")
        return {
            "period": period,
            "total_arr": total_arr,
            "new_arr": new_arr,
            "expansion_arr": expansion_arr,
            "nrr": round((total_arr + expansion_arr) / max(total_arr, 1) * 100, 1),
            "records_count": len(revenue_records),
        }

    def __call__(self, action: str, payload: Dict, context=None) -> Any:
        handlers = {
            "create_quote": lambda p: vars(self.create_quote(
                p["customer_id"], p["opportunity_id"], p["line_items"],
                p.get("discount_pct", 0), p.get("valid_days", 30)
            )),
            "approve_quote": lambda p: vars(self.approve_quote(p["quote_id"], p["approval_id"])),
            "recognize_revenue": lambda p: vars(self.recognize_revenue(
                p["order_id"], p["customer_id"], p["amount"],
                p["revenue_type"], p.get("attribution", {})
            )),
            "kpi_attribution": lambda p: self.calculate_kpi_attribution(p),
            "business_analysis": lambda p: self.business_analysis(p.get("period", "current"), p.get("filters")),
        }
        handler = handlers.get(action)
        if not handler:
            raise ValueError(f"cs.finance: 未知 action={action}")
        return handler(payload)

    def _get_quote(self, quote_id: str) -> Quote:
        if quote_id not in self._quotes:
            raise ValueError(f"报价单不存在: {quote_id}")
        return self._quotes[quote_id]
