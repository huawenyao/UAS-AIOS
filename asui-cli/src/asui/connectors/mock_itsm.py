"""ITSM mock：cs.ticket。"""

from __future__ import annotations

import uuid
from typing import Any

from .base import InvokeContext, InvokeResult, SystemConnector


class ItsmMockConnector(SystemConnector):
    connector_id = "connector.itsm.sandbox"
    connector_type = "itsm"

    def invoke(self, operation: str, payload: dict[str, Any], ctx: InvokeContext) -> InvokeResult:
        if operation == "create":
            tid = f"TKT-{uuid.uuid4().hex[:8]}"
            return InvokeResult(
                status="ok",
                output={"ticket_id": tid, "sla_due_at": "2026-05-24T18:00:00Z"},
            )
        if operation == "escalate":
            return InvokeResult(
                status="ok",
                output={
                    "escalation_id": f"ESC-{uuid.uuid4().hex[:8]}",
                    "assigned_to": "role.cs_lead",
                },
            )
        return InvokeResult(status="error", message=f"unsupported itsm operation: {operation}")
