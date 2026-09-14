from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
HUB_API = Path(__file__).resolve().parents[4] / "services" / "hub-api"
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(HUB_API))

from capability_hub.profiles import PROFILES, load_matrix, tools_for  # noqa: E402


class ProfileMatrixTests(unittest.TestCase):
    def test_four_profiles_are_one_config_not_three_services(self) -> None:
        matrix = load_matrix()
        self.assertEqual(set(matrix["profiles"]), {"scene", "explore", "builder", "runtime"})
        self.assertEqual(matrix["engine"], "single_hub")
        self.assertEqual(PROFILES, ("scene", "explore", "builder", "runtime"))

    def test_scene_forbids_cs_write_and_skill_execute(self) -> None:
        scene = load_matrix()["profiles"]["scene"]
        self.assertFalse(scene["cs_write"])
        self.assertEqual(scene["skill_max_state"], "previewed")
        self.assertFalse(scene["skill_execute"])
        self.assertEqual(scene["default_track"], "scene")

    def test_explore_max_cited_and_no_production_write(self) -> None:
        explore = load_matrix()["profiles"]["explore"]
        self.assertFalse(explore["cs_write"])
        self.assertEqual(explore["skill_max_state"], "cited")
        self.assertTrue(explore["network_search"])
        self.assertEqual(explore["default_track"], "selfpaw")

    def test_builder_dry_run_only(self) -> None:
        builder = load_matrix()["profiles"]["builder"]
        self.assertFalse(builder["cs_write"])
        self.assertTrue(builder["cs_write_dry_run"])
        self.assertEqual(builder["skill_max_state"], "installed")

    def test_runtime_allows_gated_write(self) -> None:
        runtime = load_matrix()["profiles"]["runtime"]
        self.assertTrue(runtime["cs_write"])
        self.assertEqual(runtime["skill_max_state"], "executed")
        self.assertIn(runtime["default_track"], ("selfpaw", "pipaw", "instance"))

    def test_matrix_file_is_the_authority(self) -> None:
        path = PKG / "configs" / "profile_matrix.json"
        disk = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(disk, load_matrix())

    def test_tools_for_scene_hides_side_effects(self) -> None:
        tools = tools_for("scene", ["cs.visit.list", "cs.visit.schedule"], {"cs.visit.schedule": True})
        self.assertIn("cs.visit.list", tools)
        self.assertNotIn("cs.visit.schedule", tools)


if __name__ == "__main__":
    unittest.main()
