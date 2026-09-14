from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Registry:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self._ops: dict[str, dict[str, Any]] = {}
        for svc in data.get("services", []):
            if not svc.get("enabled", True):
                continue
            sid = svc["id"]
            for op in svc.get("operations", []):
                name = f"{sid}.{op['name']}"
                rec = dict(op)
                rec["enabled"] = True
                rec["service_id"] = sid
                rec["side_effects"] = op.get("side_effects") or []
                self._ops[name] = rec

    @classmethod
    def from_file(cls, path: Path) -> "Registry":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def get(self, operation: str) -> dict[str, Any] | None:
        return self._ops.get(operation)

    def list_for_profile(self, profile: str) -> list[str]:
        names = []
        for name, op in self._ops.items():
            if not op.get("agent_visible", True):
                continue
            if profile in ("scene", "explore", "builder") and op.get("side_effects"):
                continue
            names.append(name)
        return sorted(names)
