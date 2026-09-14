"""Skill 协议：discover ≠ execute。Explore 最高 cited。"""

from __future__ import annotations

from typing import Any

from capability_hub.profiles import skill_max_state
from uas_hub.adapters.skill import STATES
from uas_hub.errors import HubError

CATALOG = (
    {
        "skill_id": "skill.visit",
        "name": "拜访破局",
        "summary": "C-level 拜访议程与决策链补齐",
        "installed": False,
    },
    {
        "skill_id": "skill.quote",
        "name": "报价口径",
        "summary": "报价模板与审批清单",
        "installed": False,
    },
)


def assert_transition_allowed(profile: str, to_state: str) -> None:
    max_state = skill_max_state(profile)
    if STATES.index(to_state) > STATES.index(max_state):
        raise HubError("SKILL_NOT_EXECUTABLE_IN_PROFILE", profile)
