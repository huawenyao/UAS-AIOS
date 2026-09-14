from __future__ import annotations

from typing import Any

from uas_hub.errors import HubError


class WmStore:
    def __init__(self) -> None:
        self._docs: dict[tuple[str, str, int], dict[str, Any]] = {}

    def put(self, world_model_id: str, lifetime: str, version: int, body: dict[str, Any]) -> None:
        self._docs[(world_model_id, lifetime, version)] = dict(body)

    def get(self, world_model_id: str, lifetime: str, version: int | None = None) -> dict[str, Any]:
        if version is not None:
            doc = self._docs.get((world_model_id, lifetime, version))
            if not doc:
                raise HubError("SCOPE_DENIED", "wm missing")
            return doc
        versions = [v for (wid, lt, v) in self._docs if wid == world_model_id and lt == lifetime]
        if not versions:
            raise HubError("SCOPE_DENIED", "wm missing")
        latest = max(versions)
        return self._docs[(world_model_id, lifetime, latest)]

    def patch(self, world_model_id: str, lifetime: str, profile: str, body: dict[str, Any]) -> dict[str, Any]:
        if lifetime == "compiled" and profile == "runtime":
            raise HubError("INVARIANT_FAILED", "runtime cannot patch compiled")
        if lifetime == "compiled" and profile != "builder":
            raise HubError("INVARIANT_FAILED", "only builder promotes compiled")
        versions = [v for (wid, lt, v) in self._docs if wid == world_model_id and lt == lifetime]
        nxt = (max(versions) + 1) if versions else 1
        self.put(world_model_id, lifetime, nxt, body)
        return {"world_model_id": world_model_id, "lifetime": lifetime, "version": nxt}
