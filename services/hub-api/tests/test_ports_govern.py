from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB_ROOT))

from uas_hub.adapters.artifact import FixtureArtifact  # noqa: E402
from uas_hub.adapters.connector import FixtureConnector  # noqa: E402
from uas_hub.adapters.evolution import FixtureEvolution  # noqa: E402
from uas_hub.adapters.iam import FixtureIam  # noqa: E402
from uas_hub.adapters.law import FixtureLaw  # noqa: E402
from uas_hub.adapters.review import FixtureReview  # noqa: E402
from uas_hub.adapters.skill import FixtureSkill  # noqa: E402
from uas_hub.errors import HubError  # noqa: E402


class GovernPortTests(unittest.TestCase):
    def test_explore_cannot_execute_skill(self) -> None:
        skill = FixtureSkill()
        self.assertEqual(skill.state_of("skill.visit"), "discovered")
        with self.assertRaises(HubError) as ctx:
            skill.transition("skill.visit", "executed", "explore")
        self.assertEqual(ctx.exception.code, "SKILL_NOT_EXECUTABLE_IN_PROFILE")
        self.assertEqual(skill.state_of("skill.visit"), "discovered")
        with self.assertRaises(HubError) as ctx:
            skill.transition("skill.visit", "installed", "explore")
        self.assertEqual(ctx.exception.code, "SKILL_NOT_EXECUTABLE_IN_PROFILE")
        cited = skill.transition("skill.visit", "cited", "explore")
        self.assertEqual(cited["state"], "cited")
        with self.assertRaises(HubError) as ctx:
            skill.transition("skill.visit", "executed", "scene")
        self.assertEqual(ctx.exception.code, "SKILL_NOT_EXECUTABLE_IN_PROFILE")
        enabled = skill.transition("skill.visit", "enabled", "runtime")
        self.assertEqual(enabled["state"], "enabled")
        executed = skill.transition("skill.visit", "executed", "runtime")
        self.assertEqual(executed["state"], "executed")

    def test_unapproved_law_not_compiled(self) -> None:
        law = FixtureLaw()
        with self.assertRaises(HubError) as ctx:
            law.compile("pack-cm", False)
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")
        self.assertEqual(law._compiled, {})
        compiled = law.compile("pack-cm", True)
        self.assertTrue(compiled["compiled"])
        self.assertEqual(compiled["pack_id"], "pack-cm")
        self.assertTrue(compiled["laws"])
        self.assertEqual(compiled["laws"][0]["law_id"], "LAW-VISIT-SLA")

    def test_evolution_auto_apply_false(self) -> None:
        evo = FixtureEvolution()
        self.assertIs(evo.auto_apply, False)
        drafted = evo.draft({"kind": "timeout"})
        self.assertIs(drafted["auto_apply"], False)
        self.assertEqual(drafted["status"], "draft")
        denied = evo.apply(drafted["changeset_id"], False)
        self.assertIs(denied["applied"], False)
        self.assertIs(denied["auto_apply"], False)
        evo.auto_apply = True
        applied = evo.apply(drafted["changeset_id"], True)
        self.assertIs(applied["applied"], True)
        self.assertIs(applied["auto_apply"], False)
        self.assertIs(evo.auto_apply, False)
        self.assertIs(evo.wrote_compiled, False)

    def test_file_artifact_not_pack_state(self) -> None:
        store = FixtureArtifact()
        report = store.put("file", b"%PDF-report")
        self.assertIn("sha256", report)
        self.assertEqual(len(report["sha256"]), 64)
        self.assertFalse(store.usable_as_pack_state(report["artifact_id"]))
        theme = store.put("theme", {"name": "cm-pack"})
        self.assertTrue(store.usable_as_pack_state(theme["artifact_id"]))
        self.assertEqual(theme["kind"], "theme")

    def test_connector_idempotent_and_no_secrets(self) -> None:
        conn = FixtureConnector()
        self.assertEqual(conn.id, "connector.crm.mock")
        payload = {"account": "a1", "token": "leak", "password": "x", "api_key": "k"}
        first = conn.invoke("cs.visit.schedule", payload, {"tenant_id": "t-hengchuan"}, "idem-1")
        second = conn.invoke("cs.visit.schedule", payload, {"tenant_id": "t-hengchuan"}, "idem-1")
        self.assertEqual(first, second)
        self.assertEqual(conn.write_count, 1)
        self.assertEqual(conn.call_count, 2)
        blob = json.dumps(first).lower()
        for token in ("token", "password", "secret", "api_key"):
            self.assertNotIn(token, blob)
        health = conn.health()
        self.assertTrue(health["ok"])
        self.assertIs(health["secrets_exposed"], False)

    def test_iam_unbound_has_no_position(self) -> None:
        iam = FixtureIam()
        self.assertEqual(iam.position_of("cowen.hua", "t-hengchuan"), "pos-cm")
        self.assertIsNone(iam.position_of("nobody", "t-hengchuan"))
        bound = iam.bind("nobody", "t-hengchuan", "pos-bd")
        self.assertEqual(bound["position_id"], "pos-bd")
        self.assertEqual(iam.position_of("nobody", "t-hengchuan"), "pos-bd")

    def test_utopia_export_not_write_path(self) -> None:
        review = FixtureReview()
        exported = review.export_candidates("conflict")
        self.assertEqual(exported["candidates"], [])
        self.assertIs(exported["write_path"], False)
        forced = review.export_candidates("conflict", write=True)
        self.assertIs(forced["write_path"], False)
        self.assertFalse(hasattr(review, "invoke_cs"))
        self.assertFalse(callable(getattr(review, "invoke_cs", None)))


if __name__ == "__main__":
    unittest.main()
