"""M17 Lethe 夹具。独立存储，不与责任图同 key；轨道禁令由 Hub 先判。"""

from __future__ import annotations

import uuid
from typing import Any


class FixtureMemory:
    """个人记忆实验室实现。key 不含 ag_ / an- / graph。"""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def add(self, actor_id: str, text: str) -> dict[str, Any]:
        memory_id = f"mem-{uuid.uuid4().hex[:12]}"
        rec = {"memory_id": memory_id, "actor_id": actor_id, "text": text}
        self._store[memory_id] = rec
        return {"memory_id": memory_id, "actor_id": actor_id}

    def search(self, actor_id: str, query: str) -> list[dict[str, Any]]:
        needle = (query or "").strip().lower()
        hits: list[dict[str, Any]] = []
        for rec in self._store.values():
            if rec["actor_id"] != actor_id:
                continue
            if needle and needle not in str(rec.get("text") or "").lower():
                continue
            hits.append(dict(rec))
        return hits

    def forget(self, actor_id: str, memory_id: str) -> dict[str, Any]:
        rec = self._store.get(memory_id)
        if rec is not None and rec.get("actor_id") == actor_id:
            self._store.pop(memory_id, None)
        return {"receipt_id": f"rec-{uuid.uuid4().hex[:12]}", "forgotten": True}
