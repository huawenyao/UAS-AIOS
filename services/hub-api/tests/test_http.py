from __future__ import annotations

import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB_ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from uas_hub.http_app import create_app  # noqa: E402


SCENE_HDR = {
    "X-Tenant-Id": "t-hengchuan",
    "X-Actor-Id": "cowen.hua",
    "X-Track": "pipaw",
    "Authorization": "Bearer lab",
}


class HubHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    def test_pack_open_http_renders_gate(self) -> None:
        res = self.client.post(
            "/hub/v1/scene/pack/open",
            headers=SCENE_HDR,
            json={"position_id": "pos-cm", "profile": "runtime"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        ids = [n["node_id"] for n in body["nodes"]]
        self.assertIn("an-stage-visit", ids)

    def test_missing_tenant_forbidden(self) -> None:
        res = self.client.post(
            "/hub/v1/scene/pack/open",
            headers={"X-Actor-Id": "cowen.hua", "X-Track": "pipaw"},
            json={"position_id": "pos-cm"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "TENANT_MISMATCH")

    def test_scene_invoke_write_forbidden(self) -> None:
        res = self.client.post(
            "/hub/v1/scene/invoke_cs",
            headers=SCENE_HDR,
            json={"operation": "cs.visit.schedule", "input": {"customer_id": "UEC-10293"}, "profile": "runtime"},
        )
        self.assertEqual(res.status_code, 403)
        err = res.json()["error"]
        self.assertEqual(err["code"], "PROFILE_FORBIDS_SIDE_EFFECT")
        self.assertIn("签发", err["message"])
        self.assertEqual(err["next"], "hub.scene.task.issue")

    def test_runtime_invoke_write_ok(self) -> None:
        res = self.client.post(
            "/hub/v1/instance/invoke_cs",
            headers=SCENE_HDR,
            json={"operation": "cs.visit.schedule", "input": {"customer_id": "UEC-10293"}},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(res.json()["ok"])

    def test_task_issue_http(self) -> None:
        drill = self.client.post(
            "/hub/v1/scene/insight/drill",
            headers=SCENE_HDR,
            json={"source_node_id": "an-stage-visit", "evidence_refs": [{"kind": "kg", "id": "ep-1"}]},
        )
        self.assertEqual(drill.status_code, 200, drill.text)
        insight_id = drill.json()["insight_id"]
        issued = self.client.post(
            "/hub/v1/scene/task/issue",
            headers={**SCENE_HDR, "Idempotency-Key": "iss-1"},
            json={
                "source_node_id": "an-stage-visit",
                "insight_id": insight_id,
                "cs_write": ["cs.visit.schedule"],
                "assignee": {"owner_id": "zhangsan", "position_id": "pos-bd"},
            },
        )
        self.assertEqual(issued.status_code, 200, issued.text)
        body = issued.json()
        self.assertEqual(body["status"], "issued")
        self.assertIsNone(body["workflow_id"])
        replay = self.client.post(
            "/hub/v1/scene/task/issue",
            headers={**SCENE_HDR, "Idempotency-Key": "iss-1"},
            json={"source_node_id": "an-stage-visit", "insight_id": insight_id},
        )
        self.assertEqual(replay.json()["task_id"], body["task_id"])

    def test_explain_http(self) -> None:
        res = self.client.get("/hub/v1/policy/explain", params={"code": "PROFILE_FORBIDS_SIDE_EFFECT"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("签发", res.json()["message"])

    def test_routes_only_hub_v1(self) -> None:
        paths = {getattr(r, "path", "") for r in self.client.app.routes}
        skip = ("/docs", "/openapi.json", "/redoc")
        http_paths = [p for p in paths if p.startswith("/") and not any(p == s or p.startswith(s) for s in skip)]
        self.assertTrue(any(p.startswith("/hub/v1") for p in http_paths), paths)
        for path in http_paths:
            self.assertTrue(path.startswith("/hub/v1") or path == "/health", path)

    def test_thread_profile_immutable_http(self) -> None:
        hdr = {**SCENE_HDR, "X-Thread-Id": "th-http-1"}
        first = self.client.post("/hub/v1/scene/pack/open", headers=hdr, json={"position_id": "pos-cm"})
        self.assertEqual(first.status_code, 200, first.text)
        second = self.client.post(
            "/hub/v1/instance/invoke_cs",
            headers=hdr,
            json={"operation": "cs.visit.list", "input": {}},
        )
        self.assertEqual(second.status_code, 409)
        self.assertEqual(second.json()["error"]["code"], "THREAD_PROFILE_IMMUTABLE")


if __name__ == "__main__":
    unittest.main()
