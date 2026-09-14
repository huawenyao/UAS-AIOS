"""T1 §4 策略剖面：同一 Hub，四套政策，禁止复制注册中心。"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from capability_hub.paths import MATRIX

PROFILES = ("scene", "explore", "builder", "runtime")


@lru_cache(maxsize=1)
def load_matrix() -> dict[str, Any]:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def profile_of(name: str) -> dict[str, Any]:
    matrix = load_matrix()
    rec = matrix["profiles"].get(name)
    if rec is None:
        raise KeyError(name)
    return rec


def allows_cs_write(profile: str, dry_run: bool = False) -> bool:
    rec = profile_of(profile)
    if rec["cs_write"]:
        return True
    return bool(dry_run and rec.get("cs_write_dry_run"))


def skill_max_state(profile: str) -> str:
    return str(profile_of(profile)["skill_max_state"])


def tools_for(profile: str, names: list[str], side_effects: dict[str, bool]) -> list[str]:
    write = allows_cs_write(profile)
    out = []
    for name in names:
        if side_effects.get(name) and not write:
            continue
        out.append(name)
    return out
