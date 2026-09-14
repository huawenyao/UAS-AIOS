from __future__ import annotations

from typing import Any

from uas_hub.errors import HubError, utc_now
from uas_hub.graph_store import node_incomplete


class InsightTaskService:
    def __init__(self) -> None:
        self.insights: dict[str, dict[str, Any]] = {}
        self.tasks: dict[str, dict[str, Any]] = {}
        self.temporal_starts = 0

    def drill(
        self,
        tenant_id: str,
        source_node_id: str,
        node: dict[str, Any],
        evidence_refs: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        miss = node_incomplete(node)
        if miss == "caliber":
            raise HubError("CALIBER_MISSING")
        if miss:
            raise HubError("WM_INCOMPLETE", miss)
        refs = evidence_refs or []
        grounded = bool(refs)
        insight_id = f"ins-{source_node_id}-drill"
        wm = node.get("wm") or {}
        insight = {
            "insight_id": insight_id,
            "tenant_id": tenant_id,
            "source_node_id": source_node_id,
            "profile": "explore",
            "hypothesis": f"{node.get('kpi', {}).get('name', 'kpi')} 偏离 ought",
            "suggested_cs": list((node.get("process") or {}).get("cs_write") or []),
            "evidence_refs": refs,
            "grounded": grounded,
            "wm_completeness": [k for k in ("space", "time", "subject", "object", "feedback") if wm.get(k)],
        }
        self.insights[insight_id] = insight
        return insight

    def issue(self, tenant_id: str, payload: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
        source = payload.get("source_node_id")
        if not source:
            raise HubError("TASK_SOURCE_REQUIRED")
        miss = node_incomplete(node)
        if miss == "caliber":
            raise HubError("CALIBER_MISSING")
        if miss:
            raise HubError("WM_INCOMPLETE", miss)
        insight_id = payload.get("insight_id")
        insight = self.insights.get(insight_id or "")
        if insight is None or not insight.get("grounded"):
            raise HubError("UNGROUNDED_INSIGHT")
        allowed = set((node.get("process") or {}).get("cs_write") or [])
        requested = list(payload.get("cs_write") or [])
        if requested and not set(requested).issubset(allowed):
            raise HubError("SCOPE_DENIED", "cs_write not on node")
        task_id = payload.get("task_id") or f"tsk-{source}-001"
        task = {
            "task_id": task_id,
            "tenant_id": tenant_id,
            "source_node_id": source,
            "insight_id": insight["insight_id"],
            "assignee": payload.get("assignee") or {"owner_id": "unknown", "position_id": "pos-bd"},
            "due": payload.get("due"),
            "cs_write": requested,
            "evidence_refs": [e.get("id") for e in insight.get("evidence_refs", []) if isinstance(e, dict)],
            "status": "issued",
            "track": payload.get("track") or "pipaw",
            "workflow_id": None,
            "issued_at": utc_now(),
        }
        self.tasks[task_id] = task
        return task
