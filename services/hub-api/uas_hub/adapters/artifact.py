"""M10 Artifact 夹具。kind=file 不能作为 pack.open 状态源。"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from uas_hub.errors import HubError

_PACK_STATE_KINDS = frozenset({"theme", "blueprint", "release"})


class FixtureArtifact:
    def __init__(self) -> None:
        self._items: dict[str, dict[str, Any]] = {}

    def put(self, kind: str, body: bytes | dict[str, Any]) -> dict[str, Any]:
        raw = _as_bytes(body)
        digest = hashlib.sha256(raw).hexdigest()
        artifact_id = f"art-{digest[:16]}"
        rec = {"artifact_id": artifact_id, "kind": kind, "sha256": digest, "body": body}
        self._items[artifact_id] = rec
        return {"artifact_id": artifact_id, "kind": kind, "sha256": digest}

    def get(self, artifact_id: str) -> dict[str, Any]:
        rec = self._items.get(artifact_id)
        if rec is None:
            raise HubError("INVARIANT_FAILED", artifact_id)
        return dict(rec)

    def usable_as_pack_state(self, artifact_id: str) -> bool:
        rec = self._items.get(artifact_id)
        if rec is None:
            return False
        return rec["kind"] in _PACK_STATE_KINDS


def _as_bytes(body: bytes | dict[str, Any]) -> bytes:
    if isinstance(body, bytes):
        return body
    return json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")
