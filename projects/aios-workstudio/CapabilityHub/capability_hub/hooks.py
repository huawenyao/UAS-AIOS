"""确定性 Hooks。模型不可跳过。"""

from __future__ import annotations

from typing import Any, Callable

from uas_hub.errors import WM_DIMS, HubError


class HookBus:
    def __init__(self) -> None:
        self.fired: list[str] = []

    def run(self, name: str, check: Callable[[], None]) -> None:
        check()
        self.fired.append(name)

    def pre_promote(self, wm: dict[str, Any]) -> None:
        def check() -> None:
            missing = [d for d in WM_DIMS if not wm.get(d)]
            if missing:
                raise HubError("WM_INCOMPLETE", ",".join(missing))

        self.run("PrePromote", check)

    def pre_generate_assets(self, app: dict[str, Any]) -> None:
        def check() -> None:
            if not app.get("world_model_analysis"):
                raise HubError("INVARIANT_FAILED", "world_model_analysis required")

        self.run("PreGenerateAssets", check)

    def pre_release(self, app: dict[str, Any]) -> None:
        def check() -> None:
            if not app.get("validated"):
                raise HubError("INVARIANT_FAILED", "validate required")

        self.run("PreRelease", check)

    def pre_tool_use(self, profile: str, operation: str) -> None:
        def check() -> None:
            from capability_hub.profiles import allows_cs_write

            side_effect = operation.endswith(".schedule") or ".write" in operation
            if operation.startswith("cs.") and side_effect and not allows_cs_write(profile):
                raise HubError("PROFILE_FORBIDS_SIDE_EFFECT")

        self.run("PreToolUse", check)

    def post_tool_use(self, audit: list[dict[str, Any]], record: dict[str, Any]) -> None:
        def check() -> None:
            audit.append(record)

        self.run("PostToolUse", check)
