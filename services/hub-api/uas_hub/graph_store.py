from __future__ import annotations

from typing import Any

from uas_hub.errors import HubError, WM_DIMS


def node_incomplete(node: dict[str, Any]) -> str | None:
    for key in ("goal", "org", "kpi", "process", "wm"):
        if not node.get(key):
            return key
    wm = node.get("wm") or {}
    missing = [d for d in WM_DIMS if not wm.get(d)]
    if missing:
        return "wm." + ",".join(missing)
    kpi = node.get("kpi") or {}
    if not kpi.get("caliber") and not kpi.get("caliber_id"):
        return "caliber"
    return None


class GraphStore:
    def __init__(self, graphs: list[dict[str, Any]]) -> None:
        self._by_id = {g["graph_id"]: g for g in graphs}

    def get(self, graph_id: str) -> dict[str, Any] | None:
        return self._by_id.get(graph_id)

    def pack_open(
        self,
        tenant_id: str,
        position_id: str,
        graph_id: str | None = None,
        cube_ok: bool = True,
    ) -> dict[str, Any]:
        graph = None
        if graph_id:
            graph = self._by_id.get(graph_id)
        else:
            for g in self._by_id.values():
                if g.get("tenant_id") == tenant_id:
                    graph = g
                    break
        if graph is None:
            raise HubError("TENANT_MISMATCH", "no graph")
        if graph.get("tenant_id") != tenant_id:
            raise HubError("TENANT_MISMATCH")
        nodes = []
        for node in graph.get("nodes", []):
            org = node.get("org") or {}
            if org.get("position_id") and org.get("position_id") != position_id:
                continue
            item = dict(node)
            kpi = dict(item.get("kpi") or {})
            kpi["as_of"] = graph.get("period", {}).get("to")
            kpi["stale"] = not cube_ok
            item["kpi"] = kpi
            item["_incomplete"] = node_incomplete(node)
            nodes.append(item)
        if not nodes:
            raise HubError("SCOPE_DENIED", "empty slice")
        return {
            "graph_id": graph["graph_id"],
            "tenant_id": tenant_id,
            "nodes": nodes,
            "insights_open_count": 0,
            "tasks_open_count": 0,
        }

    def node(self, tenant_id: str, node_id: str) -> dict[str, Any]:
        for g in self._by_id.values():
            if g.get("tenant_id") != tenant_id:
                continue
            for n in g.get("nodes", []):
                if n.get("node_id") == node_id:
                    return n
        raise HubError("SCOPE_DENIED", node_id)
