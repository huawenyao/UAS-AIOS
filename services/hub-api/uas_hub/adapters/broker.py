"""M24 模型路由夹具：换提供商不改返回字段；不把 messages 当经营状态。"""

from __future__ import annotations

from typing import Any


class FixtureBroker:
    """实验室 BrokerPort。路由表可换；complete 不落会话全文。"""

    def __init__(self, routes: dict[str, str] | None = None) -> None:
        self.routes = dict(routes or {"explore": "fixture-a", "runtime": "fixture-b"})

    def complete(self, route_id: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(messages)
        provider = self.routes.get(route_id, "fixture-a")
        return {
            "text": "fixture-complete",
            "provider": provider,
            "tokens": max(1, n),
            "route_id": route_id,
        }
