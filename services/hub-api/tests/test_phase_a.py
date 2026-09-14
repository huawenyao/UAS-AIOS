from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HUB_ROOT))

from uas_hub.errors import Envelope, HubError  # noqa: E402
from uas_hub.hub import Hub  # noqa: E402
from uas_hub.policy import PolicyChain  # noqa: E402


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


class PhaseATests(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = Hub.from_repo(REPO)

    def test_schema_files_exist(self) -> None:
        for name in ("insight.schema.json", "operating_task.schema.json"):
            self.assertTrue((REPO / "schemas" / name).is_file(), name)
        self.assertTrue((REPO / "configs" / "gate_map.json").is_file())

    def test_insight_and_task_schema_validate_examples(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        insight_schema = json.loads((REPO / "schemas" / "insight.schema.json").read_text(encoding="utf-8"))
        task_schema = json.loads((REPO / "schemas" / "operating_task.schema.json").read_text(encoding="utf-8"))
        insight = {
            "insight_id": "ins-an-stage-visit-20260822",
            "tenant_id": "t-hengchuan",
            "source_node_id": "an-stage-visit",
            "profile": "explore",
            "hypothesis": "停留过长",
            "suggested_cs": ["cs.visit.schedule"],
            "evidence_refs": [{"kind": "kg", "id": "ep-1"}],
            "grounded": True,
            "wm_completeness": ["space", "time", "subject", "object", "feedback"],
        }
        task = {
            "task_id": "tsk-20260822-001",
            "tenant_id": "t-hengchuan",
            "source_node_id": "an-stage-visit",
            "insight_id": "ins-an-stage-visit-20260822",
            "assignee": {"owner_id": "zhangsan", "position_id": "pos-bd"},
            "cs_write": ["cs.visit.schedule"],
            "status": "issued",
            "track": "pipaw",
            "workflow_id": None,
        }
        jsonschema.Draft202012Validator(insight_schema).validate(insight)
        jsonschema.Draft202012Validator(task_schema).validate(task)

    def test_pack_open_renders_gate_node(self) -> None:
        opened = self.hub.pack_open(env(), "pos-cm")
        ids = [n["node_id"] for n in opened["nodes"]]
        self.assertIn("an-stage-visit", ids)
        visit = next(n for n in opened["nodes"] if n["node_id"] == "an-stage-visit")
        self.assertEqual(visit["kpi"]["status"], "gate")

    def test_pack_open_slices_by_position(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.pack_open(env(), "pos-unknown")
        self.assertEqual(ctx.exception.code, "SCOPE_DENIED")

    def test_unbound_actor_cannot_open_pack(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.pack_open(env(actor_id="nobody"), "pos-cm")
        self.assertEqual(ctx.exception.code, "SCOPE_DENIED")

    def test_cross_tenant_forbidden(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.pack_open(env(tenant_id="t-other"), "pos-cm")
        self.assertEqual(ctx.exception.code, "TENANT_MISMATCH")

    def test_write_ops_hidden_in_scene(self) -> None:
        tools = self.hub.list_tools(env(profile="scene"))
        self.assertNotIn("cs.visit.schedule", tools)
        self.assertIn("cs.visit.list", tools)
        self.assertIn("cs.metric.query", tools)

    def test_scene_cannot_invoke_cs_write(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.invoke_cs(env(profile="scene"), "cs.visit.schedule", {"customer_id": "UEC-10293"})
        self.assertEqual(ctx.exception.code, "PROFILE_FORBIDS_SIDE_EFFECT")
        body = ctx.exception.as_body()
        self.assertIn("签发", body["error"]["message"])

    def test_profile_injected_not_from_body(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.invoke_cs(
                env(profile="scene"),
                "cs.visit.schedule",
                {},
                claimed_profile="runtime",
            )
        self.assertEqual(ctx.exception.code, "PROFILE_FORBIDS_SIDE_EFFECT")

    def test_policy_order(self) -> None:
        result = self.hub.invoke_cs(env(profile="runtime"), "cs.visit.schedule", {"customer_id": "x"})
        self.assertEqual(result["_policy_trace"], list(PolicyChain.ORDER))

    def test_explain_covers_catalog(self) -> None:
        for code in (
            "PROFILE_FORBIDS_SIDE_EFFECT",
            "TASK_SOURCE_REQUIRED",
            "UNGROUNDED_INSIGHT",
            "WM_INCOMPLETE",
            "MEMORY_TRACK_FORBIDDEN",
        ):
            explained = self.hub.explain(code)
            self.assertTrue(explained["message"])
            self.assertTrue(explained["next"])

    def test_node_requires_five_tuple(self) -> None:
        graph = self.hub.graphs.get("ag-hengchuan-ltc")
        assert graph is not None
        graph["nodes"].append(
            {
                "node_id": "an-incomplete",
                "goal": {"statement": "缺维节点不得签发"},
                "org": {"position_id": "pos-cm", "owner_id": "cowen.hua"},
                "kpi": {"name": "x", "caliber": "y"},
                "process": {"cs_write": ["cs.visit.schedule"]},
                "wm": {"space": "only"},
            }
        )
        with self.assertRaises(HubError) as ctx:
            self.hub.task_issue(
                env(),
                {
                    "source_node_id": "an-incomplete",
                    "insight_id": "ins-x",
                    "cs_write": ["cs.visit.schedule"],
                },
            )
        self.assertEqual(ctx.exception.code, "WM_INCOMPLETE")

    def test_caliber_missing_cannot_issue(self) -> None:
        graph = self.hub.graphs.get("ag-hengchuan-ltc")
        assert graph is not None
        graph["nodes"].append(
            {
                "node_id": "an-nocaliber",
                "goal": {"statement": "无口径"},
                "org": {"position_id": "pos-cm", "owner_id": "cowen.hua"},
                "kpi": {"name": "x"},
                "process": {"cs_write": ["cs.visit.schedule"]},
                "wm": {
                    "space": "cm.ltc",
                    "time": "近30天",
                    "subject": "cowen.hua",
                    "object": "x",
                    "feedback": "none",
                },
            }
        )
        with self.assertRaises(HubError) as ctx:
            self.hub.task_issue(
                env(),
                {
                    "source_node_id": "an-nocaliber",
                    "insight_id": "ins-x",
                    "cs_write": ["cs.visit.schedule"],
                },
            )
        self.assertEqual(ctx.exception.code, "CALIBER_MISSING")

    def test_scene_fixture_hides_write_and_keeps_gate(self) -> None:
        fixture = self.hub.export_scene_fixture()
        ids = [n["node_id"] for n in fixture["pack"]["nodes"]]
        self.assertIn("an-stage-visit", ids)
        visit = next(n for n in fixture["pack"]["nodes"] if n["node_id"] == "an-stage-visit")
        self.assertEqual(visit["kpi"]["status"], "gate")
        self.assertNotIn("cs.visit.schedule", fixture["tools_scene"])
        self.assertIn("cs.visit.schedule", fixture["tools_runtime"])
        self.assertEqual(fixture["write_blocked"]["error"]["code"], "PROFILE_FORBIDS_SIDE_EFFECT")
        self.assertIsNone(fixture["issued_task"]["workflow_id"])
        path = REPO / "projects" / "aios-workstudio" / "demo" / "hub-pack-open.fixture.json"
        self.assertTrue(path.is_file(), "run scripts/export_hub_pack_open.py")
        disk = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(disk["pack"]["graph_id"], fixture["pack"]["graph_id"])

    def test_task_requires_source_node(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.task_issue(env(), {"insight_id": "ins-x"})
        self.assertEqual(ctx.exception.code, "TASK_SOURCE_REQUIRED")

    def test_ungrounded_cannot_issue(self) -> None:
        insight = self.hub.insight_drill(env(), "an-stage-visit", evidence_refs=[])
        self.assertFalse(insight["grounded"])
        with self.assertRaises(HubError) as ctx:
            self.hub.task_issue(
                env(),
                {
                    "source_node_id": "an-stage-visit",
                    "insight_id": insight["insight_id"],
                    "cs_write": ["cs.visit.schedule"],
                },
            )
        self.assertEqual(ctx.exception.code, "UNGROUNDED_INSIGHT")

    def test_issue_does_not_start_temporal(self) -> None:
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
                "assignee": {"owner_id": "zhangsan", "position_id": "pos-bd"},
            },
        )
        self.assertEqual(task["status"], "issued")
        self.assertIsNone(task["workflow_id"])
        self.assertEqual(self.hub.insights.temporal_starts, 0)

    def test_runtime_cannot_patch_compiled(self) -> None:
        self.hub.wm.put("wm-hengchuan-ltc", "compiled", 1, {"laws": []})
        with self.assertRaises(HubError) as ctx:
            self.hub.wm_patch(env(profile="runtime"), "wm-hengchuan-ltc", "compiled", {"laws": ["x"]})
        self.assertEqual(ctx.exception.code, "INVARIANT_FAILED")

    def test_pipaw_memory_forbidden(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.memory_self(env(track="pipaw"), "search")
        self.assertEqual(ctx.exception.code, "MEMORY_TRACK_FORBIDDEN")

    def test_selfpaw_write_requires_escalation(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.invoke_cs(env(profile="runtime", track="selfpaw"), "cs.visit.schedule", {})
        self.assertEqual(ctx.exception.code, "TRACK_ESCALATION_REQUIRED")

    def test_thread_profile_immutable(self) -> None:
        self.hub.bind_thread("th-1", "scene")
        with self.assertRaises(HubError) as ctx:
            self.hub.bind_thread("th-1", "runtime")
        self.assertEqual(ctx.exception.code, "THREAD_PROFILE_IMMUTABLE")

    def test_cube_down_marks_stale(self) -> None:
        opened = self.hub.pack_open(env(), "pos-cm", cube_ok=False)
        self.assertTrue(all(n["kpi"]["stale"] for n in opened["nodes"]))


if __name__ == "__main__":
    unittest.main()
