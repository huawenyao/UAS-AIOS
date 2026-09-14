"""M9 Skill 状态机夹具。发现 ≠ 执行。"""

from __future__ import annotations

from typing import Any

from uas_hub.errors import HubError

STATES = ("discovered", "previewed", "cited", "installed", "enabled", "executed")
_EXEC_STATES = frozenset({"installed", "enabled", "executed"})


class FixtureSkill:
    def __init__(self) -> None:
        self._states: dict[str, str] = {}

    def state_of(self, skill_id: str) -> str:
        return self._states.get(skill_id, "discovered")

    def transition(self, skill_id: str, to_state: str, profile: str) -> dict[str, Any]:
        if to_state not in STATES:
            raise HubError("INVARIANT_FAILED", to_state)
        if profile == "explore" and to_state in _EXEC_STATES:
            raise HubError("SKILL_NOT_EXECUTABLE_IN_PROFILE", profile)
        if to_state == "executed" and profile != "runtime":
            raise HubError("SKILL_NOT_EXECUTABLE_IN_PROFILE", profile)
        current = self.state_of(skill_id)
        if STATES.index(to_state) < STATES.index(current):
            raise HubError("INVARIANT_FAILED", "skill state cannot regress")
        self._states[skill_id] = to_state
        return {"skill_id": skill_id, "state": to_state, "profile": profile}
