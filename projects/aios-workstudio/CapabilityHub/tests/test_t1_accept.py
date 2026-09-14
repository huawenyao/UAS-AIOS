from __future__ import annotations

import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
HUB_API = Path(__file__).resolve().parents[4] / "services" / "hub-api"
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(HUB_API))

from capability_hub.facade import CapabilityHub  # noqa: E402
from uas_hub.errors import Envelope, HubError  # noqa: E402


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


class T1AcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = CapabilityHub.from_repo(REPO)

    def test_explore_can_cite_uninstalled_skill_but_not_execute(self) -> None:
        found = self.hub.skill_discover(env(profile="explore"))
        skill_id = found["skills"][0]["skill_id"]
        cited = self.hub.skill_cite(env(profile="explore"), skill_id, theme_id=None)
        self.assertEqual(cited["state"], "cited")
        self.assertFalse(cited["installed"])
        theme = self.hub.theme_create(
            env(profile="explore"),
            {"title": "visit-breakout", "knowledge_used": [{"skill_id": skill_id, "installed": False}]},
        )
        used = theme["knowledge_used"][0]
        self.assertIn("installed", used)
        self.assertFalse(used["installed"])
        with self.assertRaises(HubError) as ctx:
            self.hub.skill_execute(env(profile="explore"), skill_id)
        self.assertEqual(ctx.exception.code, "SKILL_NOT_EXECUTABLE_IN_PROFILE")

    def test_cite_without_installed_field_is_contract_failure(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.theme_create(
                env(profile="explore"),
                {"title": "bad", "knowledge_used": [{"skill_id": "skill.visit"}]},
            )
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")

    def test_builder_validate_fail_cannot_release(self) -> None:
        theme = self.hub.theme_create(
            env(profile="explore"),
            {"title": "ltc", "knowledge_used": [{"skill_id": "skill.visit", "installed": False}]},
        )
        promoted = self.hub.theme_promote(env(profile="explore"), theme["theme_id"])
        app = self.hub.app_normalize(env(profile="builder"), {"theme_id": promoted["theme_id"]})
        self.hub.app_analyze_wm(env(profile="builder"), app["app_id"])
        self.hub.app_select_template(env(profile="builder"), app["app_id"])
        self.hub.app_design(env(profile="builder"), app["app_id"])
        self.hub.app_generate(env(profile="builder"), app["app_id"])
        failed = self.hub.app_validate(env(profile="builder"), app["app_id"], pass_invariants=False)
        self.assertFalse(failed["ok"])
        with self.assertRaises(HubError) as ctx:
            self.hub.app_release(env(profile="builder"), app["app_id"])
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")

    def test_runtime_cross_tenant_rejected(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.pack_open(env(tenant_id="t-other"), "pos-cm")
        self.assertEqual(ctx.exception.code, "TENANT_MISMATCH")

    def test_workstudio_walks_problem_to_instance_via_section11(self) -> None:
        packs = self.hub.pack_list(env())
        self.assertTrue(packs["packs"])
        opened = self.hub.pack_open(env(), "pos-cm")
        self.assertTrue(opened["nodes"])
        insight = self.hub.insight_drill(
            env(),
            "an-stage-visit",
            evidence_refs=[{"kind": "kg", "id": "ep-visit-20260715"}],
        )
        listed = self.hub.insight_list(env())
        self.assertTrue(any(i["insight_id"] == insight["insight_id"] for i in listed["insights"]))
        task = self.hub.task_issue(
            env(),
            {
                "source_node_id": "an-stage-visit",
                "insight_id": insight["insight_id"],
                "cs_write": ["cs.visit.schedule"],
            },
        )
        theme = self.hub.theme_create(
            env(profile="explore"),
            {"title": "from-task", "task_id": task["task_id"], "knowledge_used": [{"skill_id": "skill.visit", "installed": False}]},
        )
        self.hub.theme_promote(env(profile="explore"), theme["theme_id"])
        app = self.hub.app_normalize(env(profile="builder"), {"theme_id": theme["theme_id"]})
        self.hub.app_analyze_wm(env(profile="builder"), app["app_id"])
        self.hub.app_select_template(env(profile="builder"), app["app_id"])
        self.hub.app_design(env(profile="builder"), app["app_id"])
        self.hub.app_generate(env(profile="builder"), app["app_id"])
        self.hub.app_validate(env(profile="builder"), app["app_id"], pass_invariants=True)
        release = self.hub.app_release(env(profile="builder"), app["app_id"])
        inst = self.hub.instance_deploy(env(profile="runtime"), {"release_id": release["release_id"], "task_id": task["task_id"]})
        self.assertEqual(inst["status"], "deployed")
        arts = self.hub.instance_list_artifacts(env(profile="runtime"), inst["instance_id"])
        self.assertTrue(arts["artifacts"])

    def test_task_return_writes_evolution_signal(self) -> None:
        insight = self.hub.insight_drill(
            env(),
            "an-stage-visit",
            evidence_refs=[{"kind": "kg", "id": "ep-1"}],
        )
        task = self.hub.task_issue(
            env(),
            {"source_node_id": "an-stage-visit", "insight_id": insight["insight_id"], "cs_write": ["cs.visit.schedule"]},
        )
        out = self.hub.task_return(env(), {"task_id": task["task_id"], "reason": "rejected", "note": "no slot"})
        self.assertEqual(out["status"], "returned")
        self.assertTrue(out["changeset_id"])
        self.assertFalse(out.get("auto_apply", True))

    def test_thread_profile_immutable(self) -> None:
        started = self.hub.thread_start(env(profile="explore"), {})
        with self.assertRaises(HubError) as ctx:
            self.hub.thread_start(env(profile="runtime", thread_id=started["thread_id"]), {})
        self.assertEqual(ctx.exception.code, "THREAD_PROFILE_IMMUTABLE")

    def test_runtime_cannot_patch_compiled_wm(self) -> None:
        self.hub.wm_patch(env(profile="builder"), "wm-cm", "compiled", {"space": "cn"})
        with self.assertRaises(HubError) as ctx:
            self.hub.wm_patch(env(profile="runtime"), "wm-cm", "compiled", {"space": "hack"})
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")

    def test_live_wm_patch_only_via_cycle_step(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.wm_patch(env(profile="runtime"), "wm-cm", "live", {"is": 1})
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")

    def test_iam_binding_requires_permission_changeset(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.iam_bind(env(profile="builder"), {"actor_id": "lisi", "position_id": "pos-bd"})
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")
        cs = self.hub.permission_changeset(
            env(profile="builder"),
            {"actor_id": "lisi", "position_id": "pos-bd"},
        )
        bound = self.hub.iam_bind(
            env(profile="builder"),
            {"actor_id": "lisi", "position_id": "pos-bd", "changeset_id": cs["changeset_id"]},
        )
        self.assertEqual(bound["position_id"], "pos-bd")

    def test_selfpaw_write_needs_escalation_evidence(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.instance_escalate(env(profile="runtime", track="selfpaw"), {"evidence_refs": []})
        self.assertEqual(ctx.exception.code, "TRACK_ESCALATION_REQUIRED")
        ok = self.hub.instance_escalate(
            env(profile="runtime", track="selfpaw"),
            {"evidence_refs": [{"kind": "kg", "id": "ep-1"}]},
        )
        self.assertEqual(ok["track"], "pipaw")

    def test_hooks_cannot_be_skipped(self) -> None:
        log = self.hub.hooks.fired
        theme = self.hub.theme_create(
            env(profile="explore"),
            {"title": "h", "knowledge_used": [{"skill_id": "skill.visit", "installed": False}]},
        )
        self.hub.theme_promote(env(profile="explore"), theme["theme_id"])
        self.assertIn("PrePromote", log)
        app = self.hub.app_normalize(env(profile="builder"), {"theme_id": theme["theme_id"]})
        self.hub.app_analyze_wm(env(profile="builder"), app["app_id"])
        self.hub.app_select_template(env(profile="builder"), app["app_id"])
        self.hub.app_design(env(profile="builder"), app["app_id"])
        self.hub.app_generate(env(profile="builder"), app["app_id"])
        self.assertIn("PreGenerateAssets", log)
        self.hub.app_validate(env(profile="builder"), app["app_id"], pass_invariants=True)
        self.hub.app_release(env(profile="builder"), app["app_id"])
        self.assertIn("PreRelease", log)


if __name__ == "__main__":
    unittest.main()
