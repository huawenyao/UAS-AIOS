"""兼容包：历史导入路径 ``asui.runtime``。

新代码请使用 ``asui.engine``（R 层实现）与 ``asui.protocol``（Π 层契约）。
"""

from asui.engine import (
    CapabilityRegistry,
    CognitiveRouter,
    CognitiveStateStore,
    RuntimeManager,
    UASRuntimeService,
)

__all__ = [
    "RuntimeManager",
    "UASRuntimeService",
    "CognitiveStateStore",
    "CapabilityRegistry",
    "CognitiveRouter",
]
