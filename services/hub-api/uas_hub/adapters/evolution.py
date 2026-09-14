"""M12 Evolution 夹具。auto_apply 永远为 false；禁止静默写 Law compiled。"""

from __future__ import annotations

from typing import Any


class FixtureEvolution:
    auto_apply: bool = False

    def __init__(self) -> None:
        self.auto_apply = False
        self.wrote_compiled = False
        self._drafts: dict[str, dict[str, Any]] = {}
        self._seq = 0

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "auto_apply":
            super().__setattr__(name, False)
            return
        super().__setattr__(name, value)

    def draft(self, signal: dict[str, Any]) -> dict[str, Any]:
        self.auto_apply = False
        self._seq += 1
        changeset_id = f"cs-evo-{self._seq:04d}"
        rec = {
            "changeset_id": changeset_id,
            "auto_apply": False,
            "status": "draft",
            "signal": dict(signal),
            "applied": False,
        }
        self._drafts[changeset_id] = rec
        return {"changeset_id": changeset_id, "auto_apply": False, "status": "draft"}

    def apply(self, changeset_id: str, approved: bool) -> dict[str, Any]:
        self.auto_apply = False
        rec = self._drafts.setdefault(
            changeset_id,
            {
                "changeset_id": changeset_id,
                "auto_apply": False,
                "status": "draft",
                "applied": False,
            },
        )
        rec["auto_apply"] = False
        if not approved:
            rec["applied"] = False
            return {
                "changeset_id": changeset_id,
                "applied": False,
                "auto_apply": False,
                "status": rec.get("status", "draft"),
            }
        rec["applied"] = True
        rec["status"] = "applied"
        rec["auto_apply"] = False
        return {
            "changeset_id": changeset_id,
            "applied": True,
            "auto_apply": False,
            "status": "applied",
        }
