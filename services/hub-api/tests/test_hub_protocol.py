from __future__ import annotations

import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HUB_ROOT))

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


class HubProtocolWireTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = Hub.from_repo(REPO)

    def test_ports_attached(self) -> None:
        for name in ("cube", "kg", "memory", "inner_loop", "mcp", "skill", "law", "evolution", "artifact", "broker", "connector"):
            self.assertIsNotNone(getattr(self.hub, name), name)

    def test_pack_open_hydrates_via_cube_port(self) -> None:
        opened = self.hub.pack_open(env(), "pos-cm")
        visit = next(n for n in opened["nodes"] if n["node_id"] == "an-stage-visit")
        self.assertEqual(visit["kpi"]["is"], 28)
        self.assertFalse(visit["kpi"]["stale"])
        self.assertTrue(visit["kpi"].get("caliber_id"))

    def test_task_transfer_keeps_source_node(self) -> None:
        insight = self.hub.insight_drill(
            env(),
            "an-stage-visit",
            evidence_refs=[{"kind": "kg", "id": "ep-visit-20260715"}],
        )
        task = self.hub.task_issue(
            env(),
            {
                "source_node_id": "an-stage-visit",
                "insight_id": insight["insight_id"],
                "cs_write": ["cs.visit.schedule"],
            },
        )
        moved = self.hub.task_transfer(
            env(profile="runtime"),
            {"task_id": task["task_id"], "assignee": {"owner_id": "lisi", "position_id": "pos-bd"}},
        )
        self.assertEqual(moved["source_node_id"], "an-stage-visit")
        self.assertEqual(moved["assignee"]["owner_id"], "lisi")

    def test_mcp_scene_call_still_gated(self) -> None:
        listed = self.hub.mcp_list(env(profile="scene"))
        names = [t["name"] for t in listed["tools"]]
        self.assertNotIn("cs.visit.schedule", names)
        with self.assertRaises(HubError) as ctx:
            self.hub.mcp_call(env(profile="scene"), "cs.visit.schedule", {})
        self.assertEqual(ctx.exception.code, "PROFILE_FORBIDS_SIDE_EFFECT")

    def test_review_not_write_path(self) -> None:
        out = self.hub.review_export(env(), "visit")
        self.assertFalse(out.get("write_path"))
