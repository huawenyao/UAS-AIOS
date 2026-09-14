"""M13 MCP 壳夹具：list 跟 Hub 剖面过滤；call 必须重走 invoke_cs。"""

from __future__ import annotations

from typing import Any

_BAD_FRAGMENTS = ("http://", "https://", "token", "sql", "password")


class FixtureMcp:
    """实验室 McpPort。禁止 list 缓存直通写；description 不含密钥痕迹。"""

    def __init__(self, hub: Any) -> None:
        self.hub = hub

    def list_tools(self, env: Any) -> list[dict[str, Any]]:
        names = self.hub.list_tools(env)
        tools: list[dict[str, Any]] = []
        for name in names:
            op = self.hub.registry.get(name) or {}
            tools.append({"name": name, "description": self._safe_description(op.get("description"))})
        return tools

    def call_tool(self, env: Any, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.hub.invoke_cs(env, name, arguments or {})

    @staticmethod
    def _safe_description(raw: Any) -> str:
        text = str(raw or "").strip() or "能力"
        lowered = text.lower()
        if any(frag in lowered for frag in _BAD_FRAGMENTS):
            return "能力"
        return text
