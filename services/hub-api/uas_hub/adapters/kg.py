"""M16 Graphiti 夹具。episode id 仅 ep-*，ingest 不是 cs 写。"""

from __future__ import annotations

import uuid
from typing import Any

from uas_hub.errors import HubError

_VISIT = {
    "id": "ep-visit-20260715",
    "object_ref": "UEC-10293",
    "kind": "Visit",
    "summary": "拜访 UEC-10293，阶段停留超过 SLA",
}


class FixtureKg:
    """内存时态知识。节点禁止 an-*；不调用 CRM。"""

    def __init__(self) -> None:
        self._episodes: dict[str, dict[str, Any]] = {
            _VISIT["id"]: dict(_VISIT),
        }

    def search(
        self,
        *,
        object_ref: str | None = None,
        query: str | None = None,
        valid_at: str | None = None,
        as_of: str | None = None,
    ) -> list[dict[str, Any]]:
        _ = (valid_at, as_of)
        hits: list[dict[str, Any]] = []
        needle = (query or "").strip().lower()
        for ep in self._episodes.values():
            if object_ref and object_ref not in str(ep.get("object_ref") or ""):
                continue
            if needle:
                blob = " ".join(
                    str(ep.get(k) or "") for k in ("id", "kind", "summary", "object_ref")
                ).lower()
                if needle not in blob:
                    continue
            hits.append(dict(ep))
        return hits

    def ingest_episode(self, episode: dict[str, Any]) -> dict[str, Any]:
        ep = dict(episode)
        eid = str(ep.get("id") or "")
        if eid.startswith("an-"):
            raise HubError("INVARIANT_FAILED", "kg episode id must not use an-*")
        if not eid:
            eid = f"ep-{uuid.uuid4().hex[:12]}"
            ep["id"] = eid
        ep.setdefault("object_ref", "")
        ep.setdefault("kind", "Interaction")
        ep.setdefault("summary", "")
        self._episodes[eid] = ep
        return dict(ep)
