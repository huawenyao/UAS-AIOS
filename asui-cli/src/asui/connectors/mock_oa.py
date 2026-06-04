"""OA mock 连接器：cs.approval / cs.notify。"""

from __future__ import annotations

import uuid
from typing import Any

from .base import InvokeContext, InvokeResult, SystemConnector


class OaMockConnector(SystemConnector):
    connector_id = "connector.oa.sandbox"
    connector_type = "oa"

    def invoke(self, operation: str, payload: dict[str, Any], ctx: InvokeContext) -> InvokeResult:
        if operation == "submit":
            aid = f"APR-{uuid.uuid4().hex[:8]}"
            return InvokeResult(
                status="ok",
                output={"approval_id": aid, "status": "pending"},
            )
        if operation == "approve":
            return InvokeResult(
                status="ok",
                output={"status": "approved"},
            )
        if operation == "send_im":
            return InvokeResult(
                status="ok",
                output={"message_id": f"IM-{uuid.uuid4().hex[:8]}"},
            )
        if operation == "send_email":
            return InvokeResult(
                status="ok",
                output={"message_id": f"EM-{uuid.uuid4().hex[:8]}"},
            )
        return InvokeResult(status="error", message=f"unsupported oa operation: {operation}")
