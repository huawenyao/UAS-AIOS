"""反思模块 - Reflection (L6)：结果评估与策略微调（占位实现）。"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class ReflectionModule:
    """根据执行结果与认知状态给出元认知信号。"""

    def __init__(self, app_root: Path | str | None = None) -> None:
        self._app_root = Path(app_root).resolve() if app_root else None

    def process(self, execution_result: dict, cognitive_state: dict) -> dict[str, Any]:
        level = cognitive_state.get("level", 1)
        requires_upgrade = execution_result.get("status") != "simulated_ok"
        return {
            "quality": "adequate" if not requires_upgrade else "needs_review",
            "requires_higher_level_reasoning": bool(requires_upgrade and level < 6),
            "reasoning_gap": "执行状态未达预期，可提高推理层级" if requires_upgrade else "",
            "needs_retry": False,
            "retry_reason": "",
            "app_root_bound": self._app_root is not None,
        }
