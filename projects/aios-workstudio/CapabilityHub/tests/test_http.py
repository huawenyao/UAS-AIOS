from __future__ import annotations

import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
HUB_API = Path(__file__).resolve().parents[4] / "services" / "hub-api"
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(HUB_API))

from fastapi.testclient import TestClient  # noqa: E402

from capability_hub.http_app import create_app  # noqa: E402

HDR = {
    "X-Tenant-Id": "t-hengchuan",
    "X-Actor-Id": "cowen.hua",
    "X-Track": "pipaw",
    "X-Ops-Role": "admin",
    "Authorization": "Bearer lab",
}


class CapabilityHubHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    def test_health_and_matrix(self) -> None:
        self.assertEqual(self.client.get("/health").status_code, 200)
        res = self.client.get("/hub/v1/ops/profile/matrix", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(set(res.json()["profiles"]), {"scene", "explore", "builder", "runtime"})
        paths = {getattr(r, "path", "") for r in self.client.app.routes}
        skip = ("/docs", "/openapi.json", "/redoc")
        http_paths = [p for p in paths if p.startswith("/") and not any(p == s or p.startswith(s) for s in skip)]
        for path in http_paths:
            self.assertTrue(path.startswith("/hub/v1") or path == "/health", path)

    def test_scene_pack_list_and_open(self) -> None:
        listed = self.client.get("/hub/v1/scene/pack/list", headers=HDR)
        self.assertEqual(listed.status_code, 200, listed.text)
        self.assertTrue(listed.json()["packs"])
        opened = self.client.post("/hub/v1/scene/pack/open", headers=HDR, json={"position_id": "pos-cm"})
        self.assertEqual(opened.status_code, 200, opened.text)

    def test_scene_write_still_403_with_explain(self) -> None:
        res = self.client.post(
            "/hub/v1/scene/invoke_cs",
            headers=HDR,
            json={"operation": "cs.visit.schedule", "input": {"customer_id": "UEC-10293"}},
        )
        self.assertEqual(res.status_code, 403)
        err = res.json()["error"]
        self.assertEqual(err["code"], "PROFILE_FORBIDS_SIDE_EFFECT")
        explain = self.client.get("/hub/v1/policy/explain", params={"code": err["code"]})
        self.assertIn("签发", explain.json()["message"])

    def test_explore_execute_skill_forbidden(self) -> None:
        discover = self.client.post("/hub/v1/skill/discover", headers={**HDR, "X-Profile": "explore"}, json={})
        self.assertEqual(discover.status_code, 200, discover.text)
        skill_id = discover.json()["skills"][0]["skill_id"]
        cite = self.client.post(
            "/hub/v1/skill/cite",
            headers=HDR,
            json={"skill_id": skill_id, "profile": "explore"},
        )
        self.assertEqual(cite.status_code, 200, cite.text)
        exe = self.client.post(
            "/hub/v1/skill/execute",
            headers=HDR,
            json={"skill_id": skill_id, "profile": "explore"},
        )
        self.assertEqual(exe.status_code, 403)
        self.assertEqual(exe.json()["error"]["code"], "SKILL_NOT_EXECUTABLE_IN_PROFILE")

    def test_wm_get_http(self) -> None:
        patched = self.client.post(
            "/hub/v1/wm/patch",
            headers=HDR,
            json={"world_model_id": "wm-cm", "lifetime": "draft", "body": {"space": "cn"}, "profile": "explore"},
        )
        self.assertEqual(patched.status_code, 200, patched.text)
        got = self.client.post(
            "/hub/v1/wm/get",
            headers=HDR,
            json={"world_model_id": "wm-cm", "lifetime": "draft"},
        )
        self.assertEqual(got.status_code, 200, got.text)
        self.assertEqual(got.json()["space"], "cn")

    def test_client_profile_header_ignored_on_pack_list(self) -> None:
        res = self.client.get(
            "/hub/v1/scene/pack/list",
            headers={**HDR, "X-Profile": "runtime"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(res.json()["packs"])

    def test_scene_invoke_ignores_claimed_runtime_profile(self) -> None:
        res = self.client.post(
            "/hub/v1/scene/invoke_cs",
            headers={**HDR, "X-Profile": "runtime"},
            json={"operation": "cs.visit.schedule", "input": {"customer_id": "UEC-10293"}, "profile": "runtime"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "PROFILE_FORBIDS_SIDE_EFFECT")

    def test_extra_scene_route_does_not_bind_client_profile(self) -> None:
        hdr = {**HDR, "X-Thread-Id": "th-ch-1", "X-Profile": "runtime"}
        listed = self.client.get("/hub/v1/scene/pack/list", headers=hdr)
        self.assertEqual(listed.status_code, 200, listed.text)
        opened = self.client.post(
            "/hub/v1/scene/pack/open",
            headers=hdr,
            json={"position_id": "pos-cm"},
        )
        self.assertEqual(opened.status_code, 200, opened.text)


if __name__ == "__main__":
    unittest.main()
