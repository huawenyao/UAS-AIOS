"""M4 Law Pack 夹具。未审批 ChangeSet 不得进入 compiled。"""

from __future__ import annotations

from typing import Any

from uas_hub.errors import HubError

VISIT_SLA = {
    "law_id": "LAW-VISIT-SLA",
    "subject": "pos-cm",
    "object": "visit",
    "gate": "an-stage-visit",
    "rule": "stay_days <= 14",
    "ought": 14,
    "kind": "sla",
}


class FixtureLaw:
    def __init__(self) -> None:
        self._compiled: dict[str, dict[str, Any]] = {}

    def compile(self, pack_id: str, changeset_approved: bool) -> dict[str, Any]:
        if not changeset_approved:
            raise HubError("INVARIANT_FAILED", "unapproved changeset cannot compile")
        law = dict(VISIT_SLA)
        law["pack_id"] = pack_id
        out = {"pack_id": pack_id, "laws": [law], "compiled": True}
        self._compiled[pack_id] = out
        return out
