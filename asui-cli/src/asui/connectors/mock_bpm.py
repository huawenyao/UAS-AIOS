"""BPM mock：cs.process。"""

from __future__ import annotations

import uuid
from typing import Any

from .base import InvokeContext, InvokeResult, SystemConnector


class BpmMockConnector(SystemConnector):
    connector_id = "connector.bpm.sandbox"
    connector_type = "bpm"

    def invoke(self, operation: str, payload: dict[str, Any], ctx: InvokeContext) -> InvokeResult:
        if operation == "start":
            pid = f"PROC-{uuid.uuid4().hex[:8]}"
            return InvokeResult(status="ok", output={"process_instance_id": pid})
        if operation == "advance":
            return InvokeResult(
                status="ok",
                output={"current_node": "review", "status": "active"},
            )
        return InvokeResult(status="error", message=f"unsupported bpm operation: {operation}")
