from __future__ import annotations

import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HUB_ROOT))

from uas_hub.cycle import STEPS, TASK_QUEUE, WORKFLOW_TYPE  # noqa: E402
from uas_hub.errors import Envelope  # noqa: E402
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


class HengchuanTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = Hub.from_repo(REPO)

    def test_drill_auto_grounds_from_kg(self) -> None:
        insight = self.hub.insight_drill(env(), "an-stage-visit")
        self.assertTrue(insight["grounded"])
        ids = [e["id"] for e in insight["evidence_refs"]]
        self.assertIn("ep-visit-20260715", ids)

    def test_exec_write_goes_through_connector_and_changes_kpi(self) -> None:
        before = self.hub.pack_open(env(), "pos-cm")
        visit = next(n for n in before["nodes"] if n["node_id"] == "an-stage-visit")
        self.assertEqual(visit["kpi"]["is"], 28)
        insight = self.hub.insight_drill(env(), "an-stage-visit")
        task = self.hub.task_issue(
            env(),
            {
                "source_node_id": "an-stage-visit",
                "insight_id": insight["insight_id"],
                "cs_write": ["cs.visit.schedule"],
            },
        )
        self.hub.exec_open(env(profile="runtime"), {"task_id": task["task_id"]})
        self.assertEqual(self.hub.connector.write_count, 0)
        self.hub.cycle_step(env(profile="runtime"), {"task_id": task["task_id"], "signal": "approved"})
        self.assertGreaterEqual(self.hub.connector.write_count, 1)
        after = self.hub.pack_open(env(), "pos-cm")
        visit2 = next(n for n in after["nodes"] if n["node_id"] == "an-stage-visit")
        self.assertEqual(visit2["kpi"]["is"], 10)
        self.assertFalse(visit2["kpi"]["stale"])


class TemporalContractTests(unittest.TestCase):
    def test_compose_and_workflow_exist(self) -> None:
        compose = REPO / "deploy" / "compose" / "docker-compose.yml"
        workflow = REPO / "services" / "temporal-worker" / "uas_runtime" / "workflow.py"
        activities = REPO / "services" / "temporal-worker" / "uas_runtime" / "activities.py"
        self.assertTrue(compose.is_file())
        yaml = compose.read_text(encoding="utf-8")
        self.assertIn("temporalio/auto-setup", yaml)
        self.assertIn("7233", yaml)
        self.assertIn("SRE", yaml)
        self.assertNotIn("\n  workstudio", yaml.lower())
        src = workflow.read_text(encoding="utf-8")
        self.assertEqual(WORKFLOW_TYPE, "RuntimeCycleWorkflow")
        self.assertEqual(TASK_QUEUE, "uas-runtime")
        self.assertIn("WaitForSignal", STEPS)
        lowered = src.lower()
        for banned in ("import openai", "import httpx", "import langchain", "crewai", "celery"):
            self.assertNotIn(banned, lowered)
        act = activities.read_text(encoding="utf-8").lower()
        self.assertIn("invoke_and_finish", act)
        self.assertNotIn("import httpx", act)
