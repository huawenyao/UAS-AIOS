"""SystemConnector 适配器契约。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InvokeContext:
    tenant_id: str
    user_id: str = ""
    role_ids: list[str] = field(default_factory=list)
    product_track: str = "selfpaw"
    session_id: str = ""
    agent_id: str = ""


@dataclass
class InvokeResult:
    status: str  # ok | error
    output: dict[str, Any] = field(default_factory=dict)
    message: str = ""


class SystemConnector(ABC):
    """下游系统适配器：仅接收语义 operation，不暴露 REST 路径给 Agent。"""

    connector_id: str
    connector_type: str

    @abstractmethod
    def invoke(self, operation: str, payload: dict[str, Any], ctx: InvokeContext) -> InvokeResult:
        """operation 为 capability 操作名，如 qualify_lead、get_profile。"""
