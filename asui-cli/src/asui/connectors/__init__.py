"""S-Grid 业务系统连接器（Phase-0 mock）。"""

from .router import CapabilityInvokeContext, CapabilityServiceRouter, InvokeResult
from .base import SystemConnector

__all__ = [
    "SystemConnector",
    "CapabilityInvokeContext",
    "CapabilityServiceRouter",
    "InvokeResult",
]
