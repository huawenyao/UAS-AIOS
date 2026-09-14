from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HUB_ROOT))

from uas_hub.adapters.broker import FixtureBroker  # noqa: E402
from uas_hub.adapters.inner_loop import FixtureInnerLoop  # noqa: E402
from uas_hub.adapters.mcp import FixtureMcp  # noqa: E402
from uas_hub.errors import Envelope, HubError  # noqa: E402
from uas_hub.hub import Hub  # noqa: E402


def env(**kwargs) -> Envelope:
    base = dict(
        tenant_id="t-hengchuan",
        actor_id="cowen.hua",
        profile="scene",
        track="pipaw",
        position_id="pos-cm",
    )
    base.update(kwargs)
    return Envelope(**base)


class PortsRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = Hub.from_repo(REPO)
        self.loop = FixtureInnerLoop()

    def test_innerloop_rejects_tool_outside_allowlist(self) -> None:
        tid = self.loop.start_thread("explore", ["cs.visit.list", "hub.kg.search"], "pipaw")
        with self.assertRaises(HubError) as ctx:
            self.loop.turn(tid, {"tool": "cs.visit.schedule", "arguments": {"customer_id": "x"}})
        self.assertEqual(ctx.exception.code, "SCOPE_DENIED")

    def test_innerloop_tool_names_are_cs_or_hub(self) -> None:
        allow = ["cs.visit.list", "hub.kg.search", "hub.metric.query"]
        tid = self.loop.start_thread("explore", allow, "pipaw")
        out = self.loop.turn(
            tid,
            {
                "tool_calls": [
                    {"name": "cs.visit.list", "arguments": {}},
                    {"name": "hub.kg.search", "arguments": {"query": "visit"}},
                    {"name": "hub.metric.query", "arguments": {"kpi_id": "kpi-visit-dwell"}},
                ]
            },
        )
        self.assertEqual(out["thread_id"], tid)
        self.assertIn("output", out)
        self.assertIsInstance(out["tool_calls"], list)
        self.assertEqual(out.get("source_of_truth"), "live_wm+task+audit")
        for call in out["tool_calls"]:
            name = call["name"]
            self.assertTrue(
                name.startswith("cs.") or name in {"hub.kg.search", "hub.metric.query"},
                name,
            )
            self.assertNotIn("httpx", name)
            self.assertNotIn("://", name)

    def test_innerloop_no_third_framework_import(self) -> None:
        from uas_hub.adapters import inner_loop as inner_mod

        src = inspect.getsource(inner_mod).lower()
        for banned in ("crewai", "autogen", "langchain", "langgraph"):
            self.assertNotIn(banned, src)
            self.assertNotIn(banned, sys.modules)

    def test_innerloop_compact_keeps_allowlist_not_chat(self) -> None:
        tid = self.loop.start_thread("explore", ["cs.visit.list"], "pipaw")
        out = self.loop.compact(tid)
        self.assertTrue(out["compacted"])
        self.assertEqual(out["source_of_truth"], "live_wm+task+audit")
        self.assertEqual(self.loop._threads[tid]["tool_allowlist"], ["cs.visit.list"])

    def test_broker_swap_provider_same_shape(self) -> None:
        broker = FixtureBroker()
        messages = [{"role": "user", "content": "explore turn"}]
        first = broker.complete("explore", messages)
        self.assertEqual(set(first), {"text", "provider", "tokens", "route_id"})
        self.assertEqual(first["provider"], "fixture-a")
        self.assertEqual(first["route_id"], "explore")
        broker.routes = {"explore": "fixture-z", "runtime": "fixture-b"}
        second = broker.complete("explore", messages)
        self.assertEqual(set(second), set(first))
        self.assertEqual(second["provider"], "fixture-z")
        self.assertNotEqual(first["provider"], second["provider"])
        self.assertNotIn("messages", second)
        self.assertFalse(hasattr(broker, "messages"))

    def test_mcp_scene_list_hides_write(self) -> None:
        mcp = FixtureMcp(self.hub)
        tools = mcp.list_tools(env(profile="scene"))
        names = [t["name"] for t in tools]
        self.assertNotIn("cs.visit.schedule", names)
        self.assertTrue(all("name" in t and "description" in t for t in tools))

    def test_mcp_call_goes_through_hub(self) -> None:
        mcp = FixtureMcp(self.hub)
        with self.assertRaises(HubError) as ctx:
            mcp.call_tool(env(profile="scene"), "cs.visit.schedule", {"customer_id": "UEC-10293"})
        self.assertEqual(ctx.exception.code, "PROFILE_FORBIDS_SIDE_EFFECT")

    def test_mcp_description_has_no_secret_tokens(self) -> None:
        mcp = FixtureMcp(self.hub)
        for profile in ("scene", "runtime"):
            for tool in mcp.list_tools(env(profile=profile)):
                desc = str(tool.get("description") or "").lower()
                for frag in ("http://", "https://", "token", "sql", "password"):
                    self.assertNotIn(frag, desc, tool["name"])


if __name__ == "__main__":
    unittest.main()
