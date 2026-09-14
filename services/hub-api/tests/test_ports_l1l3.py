from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HUB_ROOT))

from uas_hub.adapters.cube import FixtureCube  # noqa: E402
from uas_hub.adapters.kg import FixtureKg  # noqa: E402
from uas_hub.adapters.memory import FixtureMemory  # noqa: E402
from uas_hub.errors import HubError  # noqa: E402


class PortsL1L3Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.cube = FixtureCube(osi_dir=REPO / "configs" / "metrics" / "osi")
        self.kg = FixtureKg()
        self.memory = FixtureMemory()

    def test_cube_query_has_caliber_and_as_of(self) -> None:
        visit = self.cube.query("kpi-visit-dwell")
        spend = self.cube.query("kpi-spend")
        for row in (visit, spend):
            self.assertIn("value", row)
            self.assertTrue(row["caliber_id"])
            self.assertTrue(row["as_of"])
            self.assertIn("stale", row)
            blob = json.dumps(row, ensure_ascii=False)
            self.assertNotIn("CubeQL", blob)
            self.assertNotIn("cubeql", blob.lower())
        self.assertEqual(visit["value"], 28)
        self.assertEqual(visit["caliber_id"], "now - stage_entered_at")
        self.assertFalse(visit["stale"])
        self.assertEqual(spend["value"], 4290000)
        unknown = self.cube.query("kpi-missing")
        self.assertTrue(unknown["stale"])
        self.assertIn(unknown["value"], (None, 0))

    def test_cube_down_marks_stale(self) -> None:
        down = self.cube.query("kpi-visit-dwell", available=False)
        self.assertTrue(down["stale"])
        self.assertEqual(down["value"], 28)
        self.assertTrue(down["caliber_id"])
        self.assertTrue(down["as_of"])

    def test_kg_ids_not_accountability_nodes(self) -> None:
        hits = self.kg.search()
        self.assertTrue(hits)
        for ep in hits:
            eid = ep["id"]
            self.assertTrue(eid.startswith("ep-"), eid)
            self.assertFalse(eid.startswith("an-"), eid)

    def test_kg_rejects_an_prefix_ingest(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.kg.ingest_episode({"id": "an-stage-visit", "kind": "Visit", "object_ref": "UEC-10293"})
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")

    def test_kg_search_grounds_visit(self) -> None:
        hits = self.kg.search(object_ref="UEC-10293")
        self.assertTrue(hits)
        visit = next(h for h in hits if h["id"] == "ep-visit-20260715")
        self.assertEqual(visit["kind"], "Visit")
        self.assertIn("UEC-10293", str(visit["object_ref"]))
        self.assertIn("summary", visit)

    def test_memory_forget_receipt(self) -> None:
        added = self.memory.add("cowen.hua", "拜访备忘")
        self.assertEqual(added["actor_id"], "cowen.hua")
        self.assertTrue(added["memory_id"])
        out = self.memory.forget("cowen.hua", added["memory_id"])
        self.assertTrue(out["forgotten"])
        self.assertTrue(out["receipt_id"].startswith("rec-"))
        self.assertEqual(self.memory.search("cowen.hua", "拜访备忘"), [])

    def test_memory_store_not_graph_keys(self) -> None:
        self.memory.add("cowen.hua", "独立备忘")
        self.assertTrue(self.memory._store)
        forbidden = ("ag_", "an-", "graph")
        for key in self.memory._store:
            lowered = key.lower()
            for token in forbidden:
                self.assertNotIn(token, lowered, key)


if __name__ == "__main__":
    unittest.main()
