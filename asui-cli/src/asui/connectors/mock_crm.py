"""CRM mock 连接器：cs.customer / cs.lead。"""

from __future__ import annotations

from typing import Any

from .base import InvokeContext, InvokeResult, SystemConnector

_MOCK_CUSTOMERS = {
    "C-1001": {"customer_id": "C-1001", "name": "华东制造有限公司", "segment": "enterprise"},
    "C-1002": {"customer_id": "C-1002", "name": "深圳创新科技", "segment": "growth"},
}

_MOCK_LEADS = {
    "L-1001": {"lead_id": "L-1001", "company": "华东制造有限公司", "score": 0.82},
    "L-1002": {"lead_id": "L-1002", "company": "未知科技", "score": 0.45},
}


class CrmMockConnector(SystemConnector):
    connector_id = "connector.crm.sandbox"
    connector_type = "crm"

    def invoke(self, operation: str, payload: dict[str, Any], ctx: InvokeContext) -> InvokeResult:
        if operation == "get_profile":
            cid = payload.get("customer_id", "")
            row = _MOCK_CUSTOMERS.get(cid)
            if not row:
                return InvokeResult(status="error", message=f"customer not found: {cid}")
            return InvokeResult(
                status="ok",
                output={**row, "evidence": [f"tenant:{ctx.tenant_id}", "source:mock_crm"]},
            )
        if operation == "query":
            items = list(_MOCK_CUSTOMERS.values())[: payload.get("limit", 10)]
            return InvokeResult(status="ok", output={"items": items, "total": len(items)})
        if operation == "qualify_lead":
            lid = payload.get("lead_id", "")
            base = _MOCK_LEADS.get(lid, {"lead_id": lid, "score": 0.5})
            qualified = base.get("score", 0) >= 0.6
            return InvokeResult(
                status="ok",
                output={
                    "qualified": qualified,
                    "score": base.get("score", 0.5),
                    "evidence": ["mock_criteria", f"lead:{lid}"],
                },
            )
        if operation == "list":
            return InvokeResult(
                status="ok",
                output={"items": list(_MOCK_LEADS.values())},
            )
        return InvokeResult(status="error", message=f"unsupported crm operation: {operation}")
