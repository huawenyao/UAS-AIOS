"""M19 内环夹具：零零件 SDK，工具名只允许 cs.* / hub.kg.search / hub.metric.query。"""

from __future__ import annotations

from typing import Any

from uas_hub.errors import HubError

_ALLOWED_HUB = frozenset({"hub.kg.search", "hub.metric.query"})


class FixtureInnerLoop:
    """实验室 InnerLoopPort。业务真相是 live WM + Task + 审计指针，不是消息数组。"""

    def __init__(self) -> None:
        self._seq = 0
        self._threads: dict[str, dict[str, Any]] = {}

    def start_thread(self, profile: str, tool_allowlist: list[str], track: str) -> str:
        self._seq += 1
        thread_id = f"th-{self._seq}"
        self._threads[thread_id] = {
            "thread_id": thread_id,
            "profile": profile,
            "tool_allowlist": list(tool_allowlist),
            "track": track,
            "status": "running",
        }
        return thread_id

    def turn(self, thread_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        thread = self._require(thread_id)
        calls = self._requested_calls(payload)
        allow = set(thread["tool_allowlist"])
        for call in calls:
            name = call["name"]
            if name not in allow or not self._legal_tool_name(name):
                raise HubError("SCOPE_DENIED", name)
        return {
            "thread_id": thread_id,
            "output": {"text": "fixture-turn"},
            "tool_calls": calls,
            "status": thread["status"],
            "source_of_truth": "live_wm+task+audit",
        }

    def interrupt(self, thread_id: str) -> dict[str, Any]:
        thread = self._require(thread_id)
        thread["status"] = "interrupted"
        return {"thread_id": thread_id, "status": "interrupted"}

    def resume(self, thread_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        thread = self._require(thread_id)
        thread["status"] = "running"
        if payload:
            out = self.turn(thread_id, payload)
            out["status"] = "running"
            return out
        return {"thread_id": thread_id, "status": "running"}

    def compact(self, thread_id: str) -> dict[str, Any]:
        thread = self._require(thread_id)
        thread["compacted"] = True
        return {
            "thread_id": thread_id,
            "status": thread["status"],
            "compacted": True,
            "source_of_truth": "live_wm+task+audit",
        }

    def _require(self, thread_id: str) -> dict[str, Any]:
        thread = self._threads.get(thread_id)
        if not thread:
            raise HubError("OPERATION_NOT_FOUND", thread_id)
        return thread

    @staticmethod
    def _legal_tool_name(name: str) -> bool:
        if "://" in name or name.startswith("httpx"):
            return False
        if name.startswith("cs."):
            return True
        return name in _ALLOWED_HUB

    @staticmethod
    def _requested_calls(payload: dict[str, Any]) -> list[dict[str, Any]]:
        calls: list[dict[str, Any]] = []
        raw = payload.get("tool_calls")
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict) and item.get("name"):
                    calls.append(
                        {
                            "name": str(item["name"]),
                            "arguments": dict(item.get("arguments") or {}),
                        }
                    )
                elif isinstance(item, str):
                    calls.append({"name": item, "arguments": {}})
        name = payload.get("tool") or payload.get("name")
        if name and not any(c["name"] == name for c in calls):
            calls.append(
                {
                    "name": str(name),
                    "arguments": dict(payload.get("arguments") or {}),
                }
            )
        return calls
