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


class OpsHttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    def test_frontline_ops_forbidden(self) -> None:
        res = self.client.get(
            "/hub/v1/ops/profile/matrix",
            headers={**HDR, "X-Ops-Role": "frontline"},
        )
        self.assertEqual(res.status_code, 403)
        err = res.json()["error"]
        self.assertEqual(err["code"], "SCOPE_DENIED")
        self.assertIn("看不到 /console", err["detail"])

    def test_missing_ops_role_blocked(self) -> None:
        hdr = {k: v for k, v in HDR.items() if k != "X-Ops-Role"}
        res = self.client.get("/hub/v1/ops/profile/matrix", headers=hdr)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "GATE_BLOCKED")

    def test_schema_drift_healthy(self) -> None:
        res = self.client.get("/hub/v1/ops/schema/drift", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["status"], "healthy")
        self.assertEqual(body["count"], 0)

    def test_tenant_get(self) -> None:
        res = self.client.get("/hub/v1/ops/tenant/get", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["tenant_id"], "t-hengchuan")
        self.assertEqual(res.json()["graph_id"], "ag-hengchuan-ltc")

    def test_policy_simulate_scene_write_forbidden(self) -> None:
        res = self.client.post(
            "/hub/v1/ops/policy/simulate",
            headers=HDR,
            json={"operation": "cs.visit.schedule", "profile": "scene"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertFalse(body["allowed"])
        self.assertEqual(body["code"], "PROFILE_FORBIDS_SIDE_EFFECT")
        self.assertEqual(body["profile"], "scene")

    def test_protocol_registry(self) -> None:
        res = self.client.get("/hub/v1/ops/protocol/registry", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        ids = [m["id"] for m in res.json()["modules"]]
        self.assertEqual(ids[0], "M1")
        self.assertEqual(len(ids), 24)

    def test_graph_get_cross_tenant(self) -> None:
        res = self.client.post(
            "/hub/v1/ops/graph/get",
            headers={**HDR, "X-Tenant-Id": "t-other"},
            json={"graph_id": "ag-hengchuan-ltc"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "TENANT_MISMATCH")

    def test_graph_validate_ok(self) -> None:
        res = self.client.post("/hub/v1/ops/graph/get", headers=HDR, json={})
        self.assertEqual(res.status_code, 200, res.text)
        val = self.client.post(
            "/hub/v1/ops/graph/validate",
            headers=HDR,
            json={"graph_id": "ag-hengchuan-ltc"},
        )
        self.assertEqual(val.status_code, 200, val.text)
        self.assertTrue(val.json()["ok"])

    def test_graph_publish_incomplete_rejected(self) -> None:
        bad = {
            "graph_id": "ag-bad",
            "tenant_id": "t-hengchuan",
            "pack": "cm",
            "nodes": [
                {
                    "node_id": "an-x",
                    "org": {"position_id": "pos-cm"},
                    "goal": {},
                    "kpi": {},
                    "process": {},
                    "wm": {},
                }
            ],
        }
        self.client.app.state.ch.core.graphs._by_id["ag-bad"] = bad
        pub = self.client.post(
            "/hub/v1/ops/graph/publish",
            headers=HDR,
            json={"graph_id": "ag-bad"},
        )
        self.assertEqual(pub.status_code, 422)
        self.assertEqual(pub.json()["error"]["code"], "INVARIANT_FAILED")

    def test_changeset_submit_decide(self) -> None:
        sub = self.client.post(
            "/hub/v1/ops/changeset/submit",
            headers=HDR,
            json={"kind": "manual", "summary": "test"},
        )
        self.assertEqual(sub.status_code, 200, sub.text)
        body = sub.json()
        self.assertEqual(body["status"], "pending")
        self.assertIs(body["auto_apply"], False)
        cid = body["changeset_id"]
        dec = self.client.post(
            "/hub/v1/ops/changeset/decide",
            headers=HDR,
            json={"changeset_id": cid, "approved": True},
        )
        self.assertEqual(dec.status_code, 200, dec.text)
        self.assertEqual(dec.json()["status"], "applied")
        self.assertIs(dec.json()["auto_apply"], False)
        listed = self.client.get("/hub/v1/ops/changeset/list", headers=HDR)
        row = next(x for x in listed.json()["items"] if x["changeset_id"] == cid)
        self.assertEqual(row["status"], "applied")

    def test_selfpaw_cannot_submit(self) -> None:
        res = self.client.post(
            "/hub/v1/ops/changeset/submit",
            headers={**HDR, "X-Track": "selfpaw"},
            json={"kind": "manual"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "TRACK_ESCALATION_REQUIRED")

    def test_law_compile_unapproved(self) -> None:
        res = self.client.post(
            "/hub/v1/law/compile",
            headers=HDR,
            json={"pack_id": "pack-visit", "changeset_approved": False},
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["error"]["code"], "INVARIANT_FAILED")

    def test_mcp_preview_hides_scene_write(self) -> None:
        res = self.client.get("/hub/v1/ops/mcp/preview?profile=scene", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        names = [t["name"] for t in res.json()["tools"]]
        self.assertNotIn("cs.visit.schedule", names)
        self.assertIn("cs.visit.list", names)

    def test_registry_patch_is_pending(self) -> None:
        res = self.client.post(
            "/hub/v1/ops/registry/patch",
            headers=HDR,
            json={"operation": "cs.visit.list", "enabled": False},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["status"], "pending")
        listed = self.client.get("/hub/v1/ops/registry/list", headers=HDR)
        self.assertIn("cs.visit.schedule", listed.json()["operations"])

    def test_skill_list_explore_not_executable(self) -> None:
        res = self.client.get("/hub/v1/ops/skill/list", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        row = res.json()["skills"][0]
        self.assertIn("executable", row)
        self.assertFalse(row["executable"])

    def test_connector_list_no_secret(self) -> None:
        res = self.client.get("/hub/v1/ops/connector/list", headers=HDR)
        blob = res.text.lower()
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("vault://", blob)
        self.assertNotIn("password", blob)
        self.assertNotIn("api_key", blob)

    def test_connector_rotate_pending_vault_only(self) -> None:
        before = self.client.get("/hub/v1/ops/connector/list", headers=HDR).json()["connectors"][0]
        res = self.client.post(
            "/hub/v1/ops/connector/rotate",
            headers=HDR,
            json={"connector_id": "connector.crm.sandbox"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["status"], "pending")
        self.assertIs(body["auto_apply"], False)
        self.assertTrue(str(body.get("secret_ref") or "").startswith("vault://"))
        blob = res.text.lower()
        self.assertNotIn("password", blob)
        self.assertNotIn("api_key", blob)
        after = self.client.get("/hub/v1/ops/connector/list", headers=HDR).json()["connectors"][0]
        self.assertEqual(after.get("secret_ref"), before.get("secret_ref"))

    def test_connector_rotate_frontline_403(self) -> None:
        res = self.client.post(
            "/hub/v1/ops/connector/rotate",
            headers={**HDR, "X-Ops-Role": "frontline"},
            json={"connector_id": "connector.crm.sandbox"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "SCOPE_DENIED")

    def test_audit_export_self_audits(self) -> None:
        self.client.get("/hub/v1/ops/audit/search", headers=HDR)
        exp = self.client.get("/hub/v1/ops/audit/export", headers=HDR)
        self.assertEqual(exp.status_code, 200, exp.text)
        nxt = self.client.get("/hub/v1/ops/audit/search?q=audit.export", headers=HDR)
        self.assertTrue(nxt.json()["records"])

    def test_iam_bindings_list(self) -> None:
        res = self.client.get("/hub/v1/ops/iam/bindings", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        people = {(b["actor_id"], b["position_id"]) for b in res.json()["bindings"]}
        self.assertIn(("cowen.hua", "pos-cm"), people)

    def test_audit_search_cross_tenant(self) -> None:
        self.client.app.state.ch.core.audit.append(
            {
                "operation": "hub.ops.audit.seed",
                "tenant_id": "t-hengchuan",
                "note": "hengchuan-only",
            }
        )
        res = self.client.get(
            "/hub/v1/ops/audit/search?q=hengchuan-only",
            headers={**HDR, "X-Tenant-Id": "t-other"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "TENANT_MISMATCH")

    def test_law_diff_no_compile(self) -> None:
        res = self.client.post("/hub/v1/ops/law/diff", headers=HDR, json={"pack_id": "pack-visit"})
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("current", res.json())
        self.assertIn("candidate", res.json())
        self.assertNotIn("compiled", res.json())

    def test_caliber_status_has_stale(self) -> None:
        res = self.client.get("/hub/v1/ops/caliber/status", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        items = res.json()["items"]
        self.assertTrue(items)
        self.assertIn("stale", items[0])
        self.assertIn("key", items[0])

    def test_kg_ingest_status(self) -> None:
        res = self.client.get("/hub/v1/ops/kg/ingest_status", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("lag_minutes", res.json())

    def test_kg_search_readonly(self) -> None:
        res = self.client.post(
            "/hub/v1/ops/kg/search",
            headers=HDR,
            json={"q": "visit"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("hits", res.json())
        self.assertNotIn("vault://", res.text.lower())

    def test_runtime_task_list(self) -> None:
        res = self.client.get("/hub/v1/ops/runtime/task", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("tasks", res.json())

    def test_runtime_retry_missing_task(self) -> None:
        res = self.client.post(
            "/hub/v1/ops/runtime/retry",
            headers=HDR,
            json={"task_id": "tsk-missing"},
        )
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json()["error"]["code"], "TASK_NOT_ISSUED")

    def test_artifact_list(self) -> None:
        res = self.client.get("/hub/v1/ops/artifact/list", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("items", res.json())

    def test_model_route(self) -> None:
        res = self.client.get("/hub/v1/ops/model/route", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("routes", res.json())

    def test_deferred_ops_frontline_still_403(self) -> None:
        res = self.client.get(
            "/hub/v1/ops/caliber/status",
            headers={**HDR, "X-Ops-Role": "frontline"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "SCOPE_DENIED")

    def test_memory_forget_receipt_roundtrip(self) -> None:
        mem = self.client.app.state.ch.core.memory.add("cowen.hua", "备忘-x")
        mid = mem["memory_id"]
        fr = self.client.post(
            "/hub/v1/ops/memory/forget",
            headers=HDR,
            json={"actor_id": "cowen.hua", "memory_id": mid},
        )
        self.assertEqual(fr.status_code, 200, fr.text)
        self.assertTrue(fr.json()["receipt_id"])
        listed = self.client.get(
            "/hub/v1/ops/memory/receipt?q=" + fr.json()["receipt_id"],
            headers=HDR,
        )
        self.assertEqual(listed.status_code, 200, listed.text)
        self.assertTrue(listed.json()["receipts"])

    def test_pipaw_memory_search_still_forbidden(self) -> None:
        res = self.client.post(
            "/hub/v1/memory/self/search",
            headers={**HDR, "X-Track": "pipaw"},
            json={"query": "x"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "MEMORY_TRACK_FORBIDDEN")

    def test_automation_run_pending_only(self) -> None:
        jobs = self.client.get("/hub/v1/ops/automation/jobs", headers=HDR)
        self.assertEqual(jobs.status_code, 200, jobs.text)
        self.assertTrue(jobs.json()["jobs"])
        run = self.client.post(
            "/hub/v1/ops/automation/run",
            headers=HDR,
            json={"job_id": "wm_drift_scan"},
        )
        self.assertEqual(run.status_code, 200, run.text)
        self.assertEqual(run.json().get("status"), "pending")
        self.assertIs(run.json().get("auto_apply"), False)

    def test_wm_list(self) -> None:
        self.client.post(
            "/hub/v1/wm/patch",
            headers=HDR,
            json={"world_model_id": "wm-demo", "lifetime": "draft", "body": {"x": 1}},
        )
        res = self.client.get("/hub/v1/ops/wm/list", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(any(i.get("world_model_id") == "wm-demo" for i in res.json()["items"]))


if __name__ == "__main__":
    unittest.main()
