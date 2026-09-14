"""M8 岗位绑定夹具。无岗位则切片拒绝。"""

from __future__ import annotations

from typing import Any


class FixtureIam:
    def __init__(self) -> None:
        self._bindings: dict[tuple[str, str], str] = {
            ("cowen.hua", "t-hengchuan"): "pos-cm",
        }

    def bind(self, actor_id: str, tenant_id: str, position_id: str) -> dict[str, Any]:
        self._bindings[(actor_id, tenant_id)] = position_id
        return {"actor_id": actor_id, "tenant_id": tenant_id, "position_id": position_id}

    def position_of(self, actor_id: str, tenant_id: str) -> str | None:
        return self._bindings.get((actor_id, tenant_id))
