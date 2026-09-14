from __future__ import annotations

import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB_ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from uas_hub.errors import Envelope, HubError  # noqa: E402
from uas_hub.hub import Hub  # noqa: E402
from uas_hub.http_app import create_app  # noqa: E402
from uas_hub.outer_loop import InMemoryOuterLoop  # noqa: E402

REPO = Path(__file__).resolve().parents[3]


def env(**kwargs) -> Envelope:
    base = dict(
        tenant_id="t-hengchuan",
        actor_id="cowen.hua",
        profile="runtime",
        track="pipaw",
        position_id="pos-cm",
    )
    base.update(kwargs)
    return Envelope(**base)


SCENE_HDR = {
    "X-Tenant-Id": "t-hengchuan",
    "X-Actor-Id": "cowen.hua",
    "X-Track": "pipaw",
    "Authorization": "Bearer lab",
}


class ExecOpenTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = Hub.from_repo(REPO)
        self.scene = env(profile="scene")

    def _issue(self) -> dict:
        insight = self.hub.insight_drill(
            self.scene,
            "an-stage-visit",
            evidence_refs=[{"kind": "kg", "id": "ep-visit-20260715"}],
        )
        return self.hub.task_issue(
            self.scene,
            {
                "source_node_id": "an-stage-visit",
                "insight_id": insight["insight_id"],
                "cs_write": ["cs.visit.schedule"],
                "assignee": {"owner_id": "zhangsan", "position_id": "pos-bd"},
            },
        )

    def test_issue_still_does_not_start_outer_loop(self) -> None:
        self._issue()
        self.assertEqual(self.hub.insights.temporal_starts, 0)

    def test_exec_open_requires_issued_task(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.exec_open(env(), {"task_id": "tsk-missing"})
        self.assertEqual(ctx.exception.code, "TASK_NOT_ISSUED")

    def test_l2_waits_signal(self) -> None:
        task = self._issue()
        opened = self.hub.exec_open(env(), {"task_id": task["task_id"]})
        self.assertEqual(opened["status"], "awaiting_approval")
        self.assertEqual(opened["workflow_type"], "RuntimeCycleWorkflow")
        self.assertTrue(opened["workflow_id"])
        stored = self.hub.insights.tasks[task["task_id"]]
        self.assertEqual(stored["workflow_id"], opened["workflow_id"])
        self.assertEqual(self.hub.insights.temporal_starts, 1)
        self.assertFalse(any(a["operation"] == "cs.visit.schedule" for a in self.hub.audit))

    def test_invoke_cs_goes_through_hub(self) -> None:
        task = self._issue()
        opened = self.hub.exec_open(env(), {"task_id": task["task_id"]})
        stepped = self.hub.cycle_step(
            env(),
            {"task_id": task["task_id"], "signal": "approved"},
        )
        self.assertEqual(stepped["status"], "opened")
        writes = [a for a in self.hub.audit if a["operation"] == "cs.visit.schedule"]
        self.assertEqual(len(writes), 1)
        self.assertEqual(writes[0]["profile"], "runtime")
        self.assertIs(self.hub.outer_loop.hub, self.hub)

    def test_worker_killed_resumes(self) -> None:
        task = self._issue()
        opened = self.hub.exec_open(env(), {"task_id": task["task_id"]})
        snap = self.hub.outer_loop.snapshot()
        revived = InMemoryOuterLoop()
        revived.restore(snap)
        revived.bind_hub(self.hub)
        self.hub.outer_loop = revived
        stepped = self.hub.cycle_step(
            env(),
            {"task_id": task["task_id"], "signal": "approved"},
        )
        self.assertEqual(stepped["workflow_id"], opened["workflow_id"])
        self.assertEqual(stepped["status"], "opened")
        self.assertTrue(any(a["operation"] == "cs.visit.schedule" for a in self.hub.audit))

    def test_rejected_does_not_write(self) -> None:
        task = self._issue()
        self.hub.exec_open(env(), {"task_id": task["task_id"]})
        self.hub.cycle_step(env(), {"task_id": task["task_id"], "signal": "rejected"})
        self.assertFalse(any(a["operation"] == "cs.visit.schedule" for a in self.hub.audit))

    def test_exec_open_http(self) -> None:
        client = TestClient(create_app(self.hub))
        drill = client.post(
            "/hub/v1/scene/insight/drill",
            headers=SCENE_HDR,
            json={"source_node_id": "an-stage-visit", "evidence_refs": [{"kind": "kg", "id": "ep-1"}]},
        )
        issued = client.post(
            "/hub/v1/scene/task/issue",
            headers=SCENE_HDR,
            json={
                "source_node_id": "an-stage-visit",
                "insight_id": drill.json()["insight_id"],
                "cs_write": ["cs.visit.schedule"],
            },
        )
        opened = client.post(
            "/hub/v1/exec/open",
            headers=SCENE_HDR,
            json={"task_id": issued.json()["task_id"]},
        )
        self.assertEqual(opened.status_code, 200, opened.text)
        body = opened.json()
        self.assertEqual(body["status"], "awaiting_approval")
        public = {k: v for k, v in body.items() if k != "workflow_id"}
        self.assertIn("status", public)
        events = client.get(f"/hub/v1/exec/{issued.json()['task_id']}/events", headers=SCENE_HDR)
        self.assertEqual(events.status_code, 200)
        kinds = [e["type"] for e in events.json()["events"]]
        self.assertIn("awaiting_approval", kinds)


if __name__ == "__main__":
    unittest.main()
