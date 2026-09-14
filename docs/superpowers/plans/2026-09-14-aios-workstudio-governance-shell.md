# Spec-2 治理壳 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Console 真连 Spec-2 子集的 `hub.ops.*`：一线 `X-Ops-Role: frontline` 服务端 403；写止于 `pending` ChangeSet；漂移灯与审计导出可测。

**Architecture:** `Console/demo` 原生 `hub-ops.js`（路径对齐 `ops.ts` Spec-2 子集）→ CapabilityHub `:18088` `/hub/v1/ops/*`（信封强制 `builder` + `X-Ops-Role`）→ `OpsService` 组合 `uas_hub.Hub` 既有 GraphStore / Registry / Evolution / Law / Iam / audit 列表。禁止 ops 路由调用 `invoke_cs`。Hub 不可达时保留 `data.js` 并显示降级条。

**Tech Stack:** Python 3.11+ / FastAPI / unittest；Demo 原生 JS + `fetch`；不引入 Next / NocoBase / 零件 SDK。

**依从规格：** [`docs/superpowers/specs/2026-09-14-aios-workstudio-governance-shell-design.md`](../specs/2026-09-14-aios-workstudio-governance-shell-design.md)

**硬约束：**
- **不要**实现 `connector/rotate`、`caliber.*`、`kg.*`、`runtime.*`、`memory/receipt`、`artifact/list`、`model/route`（404 或 `OPERATION_NOT_FOUND`）。
- **不要**把 `#/run` `#/wm` `#/memory` `#/automation` `#/caliber` `#/workflows` 改成真连。
- **不要**改 `console.css` 视觉语言。
- **不执行 git commit**（用户未要求）。
- 工作目录：仓库根 `UAS-AIOS`。Windows 用 `curl.exe` 或 Python，不要用 PowerShell 的 `curl`。

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `projects/aios-workstudio/CapabilityHub/capability_hub/ops_service.py` | 新建。治理读/写组合根；ChangeSet 对外 `pending/applied/rejected` |
| `projects/aios-workstudio/CapabilityHub/capability_hub/http_app.py` | `ops_envelope` + 全部 Spec-2 `/hub/v1/ops/*` 路由 |
| `projects/aios-workstudio/CapabilityHub/tests/test_ops_http.py` | 新建。A7/A10/A11/I-12/D-02/D-04/D-07 |
| `projects/aios-workstudio/CapabilityHub/tests/test_http.py` | `profile/matrix` 补 `X-Ops-Role: admin` |
| `projects/aios-workstudio/packages/hub-client/src/ops.ts` | 追加 `protocolRegistry` `protocolContracts` `policySimulate` |
| `projects/aios-workstudio/Console/demo/hub-ops.js` | 原生管理向客户端 |
| `projects/aios-workstudio/Console/demo/index.html` | `app.js` 前引入 `hub-ops.js` |
| `projects/aios-workstudio/Console/demo/app.js` | 启动拉数 / 降级条 / submit·decide 走 Hub；离线页芯片 |
| `projects/aios-workstudio/tests/test_scaffold.py` | 断言 `hub-ops.js` 只含 ops、无 `invoke_cs` |

`POST /hub/v1/iam/bindings`（绑定）保持不动，与 `GET /hub/v1/ops/iam/bindings`（列表）并存。

---

### Task 1: ops 信封 + matrix 补头

**Files:**
- Modify: `projects/aios-workstudio/CapabilityHub/capability_hub/http_app.py`
- Modify: `projects/aios-workstudio/CapabilityHub/tests/test_http.py`
- Create: `projects/aios-workstudio/CapabilityHub/tests/test_ops_http.py`

- [x] **Step 1: 写失败测试**

在 `test_http.py` 的 `HDR` 增加 `"X-Ops-Role": "admin"`（否则 Task 1 实现后 `test_health_and_matrix` 会 403）。

新建 `test_ops_http.py`：

```python
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
```

- [x] **Step 2: 跑确认失败**

```
python -m unittest discover -s projects/aios-workstudio/CapabilityHub/tests -p "test_ops_http.py" -v
```

Expected: `test_frontline_ops_forbidden` FAIL（现在 matrix 无角色检查，200）。

- [x] **Step 3: 实现 `ops_envelope`**

在 `http_app.py` 的 `_envelope` 之后追加（不要改 scene 的 `_envelope`）：

```python
_OPS_ROLES = {"admin", "operator", "sre", "frontline"}
_OPS_WRITES = (
    "/hub/v1/ops/graph/publish",
    "/hub/v1/ops/registry/patch",
    "/hub/v1/ops/changeset/submit",
    "/hub/v1/ops/changeset/decide",
)


def ops_envelope(request: Request, hub: CapabilityHub) -> Envelope:
    tenant = request.headers.get("x-tenant-id") or ""
    if not tenant:
        raise HubError("TENANT_MISMATCH")
    role = (request.headers.get("x-ops-role") or "").strip().lower()
    if role not in _OPS_ROLES:
        raise HubError("GATE_BLOCKED", "X-Ops-Role required")
    if role == "frontline":
        raise HubError("SCOPE_DENIED", "一线账号看不到 /console")
    env = Envelope(
        tenant_id=tenant,
        actor_id=request.headers.get("x-actor-id") or "anonymous",
        profile="builder",
        track=request.headers.get("x-track") or "pipaw",
        correlation_id=request.headers.get("x-correlation-id") or "corr-ops",
        idempotency_key=request.headers.get("idempotency-key") or "",
        thread_id=None,
        position_id=None,
    )
    path = request.url.path
    if env.track == "selfpaw" and path in _OPS_WRITES:
        raise HubError("TRACK_ESCALATION_REQUIRED")
    _ = hub
    return env
```

把 `profile_matrix` 改成：

```python
    @app.get("/hub/v1/ops/profile/matrix")
    def profile_matrix(request: Request) -> dict[str, Any]:
        ops_envelope(request, ch)
        return ch.matrix()
```

- [x] **Step 4: 再跑**

`test_ops_http.py` 两例 PASS；`test_http.py` 全绿（HDR 已含 `X-Ops-Role`）。

---

### Task 2: OpsService + tenant / health / drift

**Files:**
- Create: `projects/aios-workstudio/CapabilityHub/capability_hub/ops_service.py`
- Modify: `http_app.py`
- Modify: `test_ops_http.py`

- [x] **Step 1: 失败测试**

```python
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
```

- [x] **Step 2: 跑确认 404/失败**

- [x] **Step 3: 写 `ops_service.py`**

```python
"""管理流组合根。禁止 invoke_cs。ChangeSet 对外 pending/applied/rejected。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from capability_hub.paths import REPO
from uas_hub.errors import Envelope, EXPLAIN, HubError
from uas_hub.graph_store import node_incomplete
from uas_hub.protocol_catalog import KERNEL_PATH, REGISTRY_PATH, SCHEMA_PATH, load_registry, validate_registry


class OpsService:
    def __init__(self, hub: Any) -> None:
        self.hub = hub
        self._cs: dict[str, dict[str, Any]] = {}
        self._seq = 0
        self._idem: dict[str, dict[str, Any]] = {}

    def tenant_get(self, env: Envelope) -> dict[str, Any]:
        graph = None
        for g in self.hub.graphs._by_id.values():
            if g.get("tenant_id") == env.tenant_id:
                graph = g
                break
        if graph is None:
            raise HubError("TENANT_MISMATCH")
        return {
            "tenant_id": env.tenant_id,
            "pack": graph.get("pack"),
            "graph_id": graph.get("graph_id"),
        }

    def health_summary(self, env: Envelope) -> dict[str, Any]:
        _ = env
        return {
            "open_ms": 142,
            "explain": 1.0,
            "approval_stuck": 0,
            "stale": 0,
            "ungrounded_rate": 0.0,
            "gate_p95_ms": 80,
        }

    def schema_drift(self, env: Envelope) -> dict[str, Any]:
        _ = env
        checks = [
            {"id": "registry.json", "ok": Path(REGISTRY_PATH).is_file()},
            {"id": "KERNEL.yaml", "ok": Path(KERNEL_PATH).is_file()},
            {"id": "module_protocol.schema.json", "ok": Path(SCHEMA_PATH).is_file()},
            {"id": "validate_registry", "ok": validate_registry() == []},
        ]
        bad = [c for c in checks if not c["ok"]]
        return {
            "status": "healthy" if not bad else "drift",
            "count": len(bad),
            "checks": checks,
        }
```

`create_app` 里 `ops = OpsService(ch.core)`，`app.state.ops = ops`。注册：

```python
    @app.get("/hub/v1/ops/tenant/get")
    def ops_tenant_get(request: Request) -> dict[str, Any]:
        return ops.tenant_get(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/health/summary")
    def ops_health(request: Request) -> dict[str, Any]:
        return ops.health_summary(ops_envelope(request, ch))

    @app.get("/hub/v1/ops/schema/drift")
    def ops_drift(request: Request) -> dict[str, Any]:
        return ops.schema_drift(ops_envelope(request, ch))
```

- [x] **Step 4: 测试 PASS**

---

### Task 3: explain / protocol / simulate + ops.ts

**Files:**
- Modify: `ops_service.py` `http_app.py` `test_ops_http.py`
- Modify: `projects/aios-workstudio/packages/hub-client/src/ops.ts`

- [x] **Step 1: 失败测试**

```python
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
```

- [x] **Step 2: 跑红**

- [x] **Step 3: 实现**

`policy_simulate`：**信封**已是 builder。用 **新的** `Envelope(..., profile=body.profile or "scene")` 调 `self.hub.chain.run_cs(..., execute_fn=lambda op, scoped: {"dry_run": True})`。捕获 `HubError` 成 `{allowed:false,...}`。禁止 `invoke_cs`。禁止 `bind_thread`。

`policy_explain(env, code)` → `self.hub.explain(code)`。

`protocol_registry` → `load_registry()`。

`protocol_contracts` → `[{"id", "protocol_id", "port", "hub_methods"} for m in load_registry()["modules"]]`。

`projects/aios-workstudio/packages/hub-client/src/ops.ts` 在 `matrix` 后追加：

```typescript
    protocolRegistry: () => hub.get("/hub/v1/ops/protocol/registry"),
    protocolContracts: () => hub.get("/hub/v1/ops/protocol/contracts"),
    policySimulate: (body: unknown) => hub.post("/hub/v1/ops/policy/simulate", body),
```

- [x] **Step 4: 测试 PASS**。`test_explore_execute_skill_forbidden` 仍绿。

---

### Task 4: graph get / validate / publish（A10 / A11）

**Files:** `ops_service.py` `http_app.py` `test_ops_http.py`

- [x] **Step 1: 失败测试**

```python
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
            "nodes": [{"node_id": "an-x", "org": {"position_id": "pos-cm"}, "goal": {}, "kpi": {}, "process": {}, "wm": {}}],
        }
        self.client.app.state.ch.core.graphs._by_id["ag-bad"] = bad
        pub = self.client.post(
            "/hub/v1/ops/graph/publish",
            headers=HDR,
            json={"graph_id": "ag-bad"},
        )
        self.assertEqual(pub.status_code, 422)
        self.assertEqual(pub.json()["error"]["code"], "INVARIANT_FAILED")
```

`graph/get` 无 `graph_id` 时取该租户样例图。跨租户必须在 **取到图之后** 比 `tenant_id`，未知图 / 租户不匹配都是 `TENANT_MISMATCH`（保住 A11，不要先变成 `SCOPE_DENIED`）。

- [x] **Step 2: 跑红**

- [x] **Step 3: 实现**

`validate`：对每个 node 调 `node_incomplete`；任一非空 → `{ok:false, code:"WM_INCOMPLETE", nodes:[...]}`（HTTP 200，由 publish 再升 422）。

`publish`：validate 不过 → `raise HubError("INVARIANT_FAILED")`；过则 `_put_pending(kind="graph.publish", ...)` 返回 pending ChangeSet（`auto_apply: false`）。不改 `graphs._by_id` live 内容。

- [x] **Step 4: PASS**。既有 `test_cross_tenant_forbidden`（scene pack_open）仍是 `TENANT_MISMATCH`。

---

### Task 5: ChangeSet pending 状态机（D-02）

**Files:** `ops_service.py` `http_app.py` `test_ops_http.py`

对外状态 **只有** `pending | applied | rejected`。`FixtureEvolution.draft` 的 `draft` 必须映射，不要把 `draft` 返回给 HTTP。

- [x] **Step 1: 失败测试**

```python
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
```

`/hub/v1/law/compile` 已存在；本例锁定 I-09。`decide` **不要**自动 compile。

- [x] **Step 2–4:** `_put_pending` 共享给 publish/patch/submit。`decide` 非 pending → `INVARIANT_FAILED`。`approved=false` → `rejected`。`Idempotency-Key` 非空时相同键返回同一 pending 记录。

---

### Task 6: mesh 读路径 + registry.patch

**Files:** `ops_service.py` `http_app.py` `test_ops_http.py`

- [x] **Step 1: 测试**

```python
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
        self.assertNotIn("vault://", blob)
        self.assertNotIn("password", blob)
        self.assertNotIn("api_key", blob)
```

- [x] **Step 3:**
  - `registry/list`：`list(self.hub.registry._ops)` 或等价公开 API。
  - `registry/patch`：只 `_put_pending`，**不**改 `capability_registry.json`。
  - `mcp/preview`：`self.hub.registry.list_for_profile(profile)`，包装为 `{"tools": [{"name": n} for n in names]}`（`list_for_profile` 返回 `list[str]`）。
  - `skill/list`：`capability_hub.skills.CATALOG` 每项 `executable: False`（explore 不能 execute；A9）。
  - `connector/list`：`[{"id": "connector.crm.sandbox", "status": "connected"}]`，禁止 `secret_ref`。

`GET /hub/v1/ops/connector/rotate` 不要注册。若有人 POST rotate → 可故意不实现。

---

### Task 7: audit / iam / law.diff / wm.get

**Files:** `ops_service.py` `http_app.py` `test_ops_http.py`

- [x] **Step 1: 测试**

```python
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
```

`wm/get`：`POST /hub/v1/ops/wm/get` body `{world_model_id, lifetime}` 调 `hub.wm.get`；缺文档 `SCOPE_DENIED`。先 `POST /hub/v1/wm/patch`（非 ops）写入 draft 再 ops get 可 200。

IAM 列表：读 `FixtureIam._bindings` 转成 `[{actor_id, tenant_id, position_id}]`。不要改成调用 `iam_bind`。

`law/diff`：从 `uas_hub.adapters.law` **模块**导入 `VISIT_SLA`（不是 `FixtureLaw.VISIT_SLA`）。`current = dict(VISIT_SLA)`；`candidate` = 同结构加 `"source":"pending"`。不调用 `compile`。

`audit/search` 与 `audit/export`：**必须先**按 `env.tenant_id` 过滤 `hub.audit`；若请求租户下无任何行且 `env.tenant_id` 不是衡川样例租户、或显式查询衡川专属内容时，对未知租户一律 `TENANT_MISMATCH`（与 graph/get 同口径：无本租户图/审计域 → 403）。最小实现：每条审计行必须带 `tenant_id`；search/export 只返回 `tenant_id == env.tenant_id` 的行；当 `env.tenant_id` 在 `graphs._by_id` 中无对应图时直接 `TENANT_MISMATCH`（A11）。

`audit/export`：在租户过滤之后按 `q` 再过滤，再 `hub.audit.append({"operation":"hub.ops.audit.export", "tenant_id": env.tenant_id, ...})`，返回过滤结果（导出动作本身随后可被同租户 search 到）。

- [x] **Step 4: PASS**

---

### Task 8: 未实现 ops 显式 404

**Files:** `http_app.py` `test_ops_http.py`

- [x] **Step 1: 写测试**

```python
    def test_deferred_ops_not_found_for_admin(self) -> None:
        res = self.client.get("/hub/v1/ops/caliber/status", headers=HDR)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()["error"]["code"], "OPERATION_NOT_FOUND")

    def test_deferred_ops_frontline_still_403(self) -> None:
        res = self.client.get(
            "/hub/v1/ops/caliber/status",
            headers={**HDR, "X-Ops-Role": "frontline"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "SCOPE_DENIED")
```

- [x] **Step 2: 跑确认失败（路径未注册）**

- [x] **Step 3: 注册薄处理**

**先** `ops_envelope`（frontline 仍 403），再 `raise HubError("OPERATION_NOT_FOUND", request.url.path)`。

GET：`/hub/v1/ops/artifact/list`、`/hub/v1/ops/caliber/status`、`/hub/v1/ops/kg/ingest_status`、`/hub/v1/ops/memory/receipt`、`/hub/v1/ops/runtime/task`、`/hub/v1/ops/model/route`  
POST：`/hub/v1/ops/connector/rotate`、`/hub/v1/ops/kg/search`、`/hub/v1/ops/runtime/retry`

每个路径单独 `@app.get` / `@app.post`，不要混循环。

- [x] **Step 4: PASS**（frontline 先于 404）

---

### Task 9: Demo 客户端 `hub-ops.js`

**Files:**
- Create: `projects/aios-workstudio/Console/demo/hub-ops.js`
- Modify: `Console/demo/index.html`
- Modify: `tests/test_scaffold.py`

- [x] **Step 1: 脚手架失败测试**（放在 `test_console_demo_is_ops_shell` 旁）

```python
    def test_console_hub_ops_client(self) -> None:
        demo = ROOT / "Console" / "demo"
        blob = (demo / "hub-ops.js").read_text(encoding="utf-8")
        html = (demo / "index.html").read_text(encoding="utf-8")
        self.assertIn("/hub/v1/ops/changeset/submit", blob)
        self.assertIn("/hub/v1/ops/schema/drift", blob)
        self.assertIn("/hub/v1/ops/audit/search", blob)
        self.assertIn("hub-ops.js", html)
        self.assertNotIn("/hub/v1/scene/", blob)
        self.assertNotIn("invoke_cs", blob)
        self.assertNotIn("/hub/v1/ops/connector/rotate", blob)
        for noun in FORBIDDEN:
            self.assertNotIn(noun, blob, noun)
```

- [x] **Step 2: FAIL 缺文件**

- [x] **Step 3: 写 `hub-ops.js`**（对齐 `hub-scene.js` 风格）

```javascript
(() => {
  "use strict";
  const DEFAULT = "http://127.0.0.1:18088";
  function headers() {
    const role = (window.CONSOLE_OPS_ROLE || "admin");
    return {
      "Content-Type": "application/json",
      "X-Tenant-Id": "t-hengchuan",
      "X-Actor-Id": "cowen.hua",
      "X-Track": "pipaw",
      "X-Ops-Role": role,
    };
  }
  async function req(method, path, body) {
    const res = await fetch((window.HUB_BASE || DEFAULT) + path, {
      method,
      headers: headers(),
      body: body == null ? undefined : JSON.stringify(body),
    });
    const json = await res.json();
    if (!res.ok) throw json;
    return json;
  }
  window.HubOps = {
    tenantGet: () => req("GET", "/hub/v1/ops/tenant/get"),
    healthSummary: () => req("GET", "/hub/v1/ops/health/summary"),
    schemaDrift: () => req("GET", "/hub/v1/ops/schema/drift"),
    matrix: () => req("GET", "/hub/v1/ops/profile/matrix"),
    policyExplain: (code) => req("POST", "/hub/v1/ops/policy/explain", { code }),
    protocolRegistry: () => req("GET", "/hub/v1/ops/protocol/registry"),
    protocolContracts: () => req("GET", "/hub/v1/ops/protocol/contracts"),
    policySimulate: (body) => req("POST", "/hub/v1/ops/policy/simulate", body),
    graphGet: (body) => req("POST", "/hub/v1/ops/graph/get", body || {}),
    graphValidate: (body) => req("POST", "/hub/v1/ops/graph/validate", body || {}),
    graphPublish: (body) => req("POST", "/hub/v1/ops/graph/publish", body || {}),
    wmGet: (body) => req("POST", "/hub/v1/ops/wm/get", body),
    lawDiff: (body) => req("POST", "/hub/v1/ops/law/diff", body || {}),
    registryList: () => req("GET", "/hub/v1/ops/registry/list"),
    registryPatch: (body) => req("POST", "/hub/v1/ops/registry/patch", body),
    mcpPreview: (profile) => req("GET", "/hub/v1/ops/mcp/preview?profile=" + encodeURIComponent(profile || "scene")),
    connectorList: () => req("GET", "/hub/v1/ops/connector/list"),
    skillList: () => req("GET", "/hub/v1/ops/skill/list"),
    iamBindings: () => req("GET", "/hub/v1/ops/iam/bindings"),
    changesetList: () => req("GET", "/hub/v1/ops/changeset/list"),
    changesetSubmit: (body) => req("POST", "/hub/v1/ops/changeset/submit", body),
    changesetDecide: (body) => req("POST", "/hub/v1/ops/changeset/decide", body),
    auditSearch: (q) => req("GET", "/hub/v1/ops/audit/search?q=" + encodeURIComponent(q || "")),
    auditExport: (q) => req("GET", "/hub/v1/ops/audit/export?q=" + encodeURIComponent(q || "")),
  };
})();
```

`index.html` 在 `app.js` 前：`<script src="./hub-ops.js"></script>`。

- [x] **Step 4: 脚手架 PASS**。`test_workstudio_demo_calls_scene_pack_open` 仍断言 scene 无 ops。

---

### Task 10: `app.js` 接线（不改皮肤）

**Files:** `Console/demo/app.js`（及如需一行 CSS 可用既有 `ban-strip`，尽量不改 `console.css`）

**不要**重写八页布局。最小接线：

1. `window.CONSOLE_OPS_ROLE = state.role`，在 `renderRoleSelect` onchange 里同步。
2. 文件末尾 `render()` 之后追加 `bootHubOps()`：
   - 无 `HubOps` 则 return
   - `Promise.all`：`tenantGet` `healthSummary` `schemaDrift` `changesetList` `auditSearch` `iamBindings` `graphGet({})` `registryList` `skillList`
   - 成功：写入 `state.tenant_id`、`state.health`、`state.schema_drift`（把 Hub 的 `status:"drift"` 映射为现有灯逻辑能识别的失败态：改 `isDriftFail` 为 `status === "fail" || status === "drift"`，并扫 overview/publish 里写死 `"fail"` 的文案）、`state.changeSets`（把 `changeset_id` 映到现有 `id` 字段）、`state.audit_events`、`state.iam_bindings`（能显示即可，字段可适配）
   - 顶栏插 `div#ops-banner`：`dataset.hub=ok` 文案可用 graph_id；`catch` →「治理服务暂不可用，只读降级」
3. `submitChangeSet`：若 `HubOps`，先 `changesetSubmit({kind:type, summary})` 再用返回的 `changeset_id`；失败则 toast 人话并仍可本地 pending（降级）。
4. `#/publish` 确认按钮：若 Hub 在线则 `changesetDecide({changeset_id, approved:true})`。
5. `pageHead`：对 `run|caliber|workflows|automation|memory|wm` 增加芯片「本战役离线」。
6. **不要**接 `connector.rotate` / caliber / memory 到 Hub。
7. **不要** `fetch('/hub/v1/scene/` 或 `invoke_cs`。

脚手架追加：

```python
    def test_console_demo_degrades_without_hub(self) -> None:
        js = (ROOT / "Console" / "demo" / "app.js").read_text(encoding="utf-8")
        self.assertIn("HubOps", js)
        self.assertIn("只读降级", js)
        self.assertIn("本战役离线", js)
```

---

### Task 11: 端到端回归

- [x] **Step 1: 单元测试**

```
python -m unittest discover -s services/hub-api/tests -v
python -m unittest discover -s projects/aios-workstudio/CapabilityHub/tests -v
python -m unittest discover -s projects/aios-workstudio/tests -v
```

Expected: 全 PASS。点名：frontline 403、selfpaw submit 403、graph 跨租户、drift healthy、simulate scene 写 forbidden、export 自审、law compile 未审批、explore skill execute 仍 403。

- [x] **Step 2: 启动**

```
python projects/aios-workstudio/CapabilityHub/run.py
```

另开：`cd projects/aios-workstudio` → `python -m http.server 18090`

- [x] **Step 3: curl / Python**

`GET /hub/v1/ops/audit/search` 带头 `X-Ops-Role: admin` → 200。  
frontline matrix → 403 + detail 含「看不到 /console」。

- [x] **Step 4: 浏览器**

`http://127.0.0.1:18090/Console/demo/index.html#/audit`：有审计区，不是空白。  
`#/publish`：提交后可见 pending。  
角色切 frontline：锁页。  
停 `:18088` 刷新：降级条 + `data.js` 仍可点。

- [x] **Step 5: 停服**

---

## 本计划明确不做

- NocoBase、33 端点一次做完、Console 改皮肤
- `#/wm` `#/memory` `#/automation` 真连
- `auto_apply=true`、ops 内 `invoke_cs`
- git commit

## 出站对照

| 码 | 证明 |
|----|------|
| A7 | `test_selfpaw_cannot_submit` |
| A9 | 既有 execute 403 + `test_skill_list_explore_not_executable` |
| A10 | `test_graph_publish_incomplete_rejected` |
| A11 | `test_graph_get_cross_tenant` |
| I-09 | `test_law_compile_unapproved` |
| I-12 | `test_schema_drift_healthy` |
| D-02 | submit pending / decide applied |
| D-04 | `test_frontline_ops_forbidden` |
| D-07 | `test_audit_export_self_audits` |
