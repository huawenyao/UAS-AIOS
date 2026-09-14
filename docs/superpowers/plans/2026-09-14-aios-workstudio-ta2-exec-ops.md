# Spec-3 TA-2 可办成（A∥B）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 轨 A 接线 WorkStudio `exec.open`/`cycle_step`/events「待你确认」；轨 B 实现 Spec-2 延期 ops（caliber/kg/runtime/artifact/model）并真连 Console 三页。

**Architecture:** CapabilityHub `OpsService` 替换 404 薄路由；复用 `Hub`/`InMemoryOuterLoop`/`FixtureCube`/`FixtureKg`。WorkStudio `hub-scene.js` 对齐 `scene.ts`。Console `hub-ops.js`+`app.js` 去掉 run/caliber/workflows 离线芯片。不启真 Temporal；`connector/rotate` 仍 404。

**Tech Stack:** Python 3.11+ / FastAPI / unittest；原生 JS Demo；无 NocoBase。

**依从规格：** [`docs/superpowers/specs/2026-09-14-aios-workstudio-ta2-exec-ops-design.md`](../specs/2026-09-14-aios-workstudio-ta2-exec-ops-design.md)

**硬约束：** 不改皮肤；不 commit；禁词；一线 UI 不展示 `workflow_id`；无 ops ingest 写。

**工作目录：** 仓库根 `UAS-AIOS`。Windows 用 `curl.exe`。

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `projects/aios-workstudio/CapabilityHub/capability_hub/ops_service.py` | 轨 B 七方法 |
| `projects/aios-workstudio/CapabilityHub/capability_hub/http_app.py` | 路由改调 OpsService |
| `projects/aios-workstudio/CapabilityHub/tests/test_ops_http.py` | 轨 B 测试 |
| `projects/aios-workstudio/demo/hub-scene.js` | exec 客户端 |
| `projects/aios-workstudio/demo/workstudio.js` | 执行态最小接线 |
| `projects/aios-workstudio/Console/demo/hub-ops.js` | 轨 B 客户端（已有 path，确认可用） |
| `projects/aios-workstudio/Console/demo/app.js` | 芯片 + boot 拉数 + 三页 |
| `projects/aios-workstudio/tests/test_scaffold.py` | 断言 |

---

### Task 1: ops caliber/status（TDD）

**Files:** `ops_service.py` `http_app.py` `test_ops_http.py`

- [x] **Step 1: 失败测试**

```python
    def test_caliber_status_has_stale(self) -> None:
        res = self.client.get("/hub/v1/ops/caliber/status", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        items = res.json()["items"]
        self.assertTrue(items)
        self.assertIn("stale", items[0])
        self.assertIn("key", items[0])
```

将原 `test_deferred_ops_not_found_for_admin` 的 caliber 断言改为「admin 200」；frontline 仍对 caliber 403。保留 rotate 404。

- [x] **Step 2: 跑红**（若仍是 404）

- [x] **Step 3: 实现**

`OpsService.caliber_status`：若 `hub.cube` 有 OSI keys，逐个 `query`；否则返回固定样例含 `stale`。HTTP 路由改为 `return ops.caliber_status(ops_envelope(...))`。

- [x] **Step 4: 绿**

---

### Task 2: kg search + ingest_status

**Files:** 同上

- [x] **Step 1: 测试**

```python
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
```

- [x] **Step 2–4:** `kg_search` 调 `hub.kg.search`（无则 `{"hits":[]}`）；`ingest_status` 夹具。路由改真实现。无 ingest POST 路由。

---

### Task 3: runtime task/retry + artifact + model

**Files:** 同上

- [x] **Step 1: 测试**

```python
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

    def test_connector_rotate_still_404(self) -> None:
        res = self.client.post("/hub/v1/ops/connector/rotate", headers=HDR, json={})
        self.assertEqual(res.status_code, 404)
```

- [x] **Step 3:**  
  - `runtime_task`：扫 `hub.outer_loop.runs` → `[{task_id,status}]`  
  - `runtime_retry`：查 task/`runs`，无则 `TASK_NOT_ISSUED`；有则 `signal("approved")`  
  - `artifact_list`：`hub.artifact` 若有 list API 用它，否则 `[{"id":"art-demo","kind":"report"}]`  
  - `model_route`：`{"routes":[{"id":"route-default","provider":"fixture","rpm":60}]}`

- [x] **Step 4: 绿**；frontline 对上述 GET 仍 403

---

### Task 4: hub-scene.js exec 方法

**Files:** `demo/hub-scene.js` `tests/test_scaffold.py`

- [x] **Step 1: 脚手架失败测试**

```python
    def test_workstudio_hub_scene_has_exec(self) -> None:
        blob = (ROOT / "demo" / "hub-scene.js").read_text(encoding="utf-8")
        self.assertIn("/hub/v1/exec/open", blob)
        self.assertIn("/hub/v1/instance/cycle_step", blob)
        self.assertIn("/hub/v1/exec/", blob)
```

- [x] **Step 3: 追加**

```javascript
    execOpen: (task_id) => req("POST", "/hub/v1/exec/open", { task_id }),
    cycleStep: (task_id, signal) =>
      req("POST", "/hub/v1/instance/cycle_step", { task_id, signal }),
    eventsPoll: (task_id) => req("GET", "/hub/v1/exec/" + encodeURIComponent(task_id) + "/events"),
```

- [x] **Step 4: 绿**

---

### Task 5: workstudio.js 执行态最小接线

**Files:** `demo/workstudio.js`

- [x] **Step 1:** 定位现有 `HubScene.taskIssue` / 「进入执行态」按钮绑定处。

- [x] **Step 2:** 签发成功后若有 `task_id`，点「进入执行」调 `HubScene.execOpen`；若返回 `awaiting_approval`，UI 显示「待你确认」+ 确认/驳回按钮（文案禁止 `workflow_id`）。

- [x] **Step 3:** 确认 → `cycleStep(id,"approved")`；驳回 → `rejected`。catch → toast 降级。

- [x] **Step 4:** scaffold 断言 `workstudio.js` 含 `execOpen` 与 `待你确认`，不含展示用 `workflow_id` 字符串（若必须解析 JSON 字段，用变量名 `wid` 且不写入 `textContent`）。

---

### Task 6: Console hub-ops + app.js 三页

**Files:** `Console/demo/hub-ops.js` `app.js` `test_scaffold.py`

- [x] **Step 1:** 确认 `hub-ops.js` 已有 caliber/kg/runtime/artifact/model path（Spec-2 客户端已声明）；缺则补。

- [x] **Step 2:** `pageHead` 离线列表改为仅 `automation|memory|wm`。

- [x] **Step 3:** `bootHubOps` 追加：

```javascript
window.HubOps.caliberStatus(),
window.HubOps.kgIngestStatus(),
window.HubOps.runtimeTask(),
window.HubOps.artifactList(),
window.HubOps.modelRoute(),
```

写入 `state.calibers` / `state.kg_*` / `state.runtime_tasks` / 等（字段适配现有 render，缺啥用空数组）。

- [x] **Step 4:** scaffold：`app.js` 含 `caliberStatus`；`本战役离线` 仍在；assert `#/caliber` 路径页不再与 run 一起无条件离线——可用注释或 `OFFLINE_PAGES` 常量断言不含 `caliber`。

---

### Task 7: 端到端回归

- [x] **Step 1:**

```
python -m unittest discover -s services/hub-api/tests -v
python -m unittest discover -s projects/aios-workstudio/CapabilityHub/tests -v
python -m unittest discover -s projects/aios-workstudio/tests -v
```

- [x] **Step 2:** 启 `:18088` + `:18090`

- [x] **Step 3:** curl exec 链 + ops caliber + frontline 403 + rotate 404

- [x] **Step 4:** 浏览器 WorkStudio 待确认 + Console 三页

- [x] **Step 5:** 停服

---

## 本计划明确不做

- NocoBase、memory/automation/wm 真连、connector.rotate、真 Temporal、git commit

## 出站对照

| 码 | 证明 |
|----|------|
| A5/A6 | test_exec + Demo |
| I-03 | caliber stale |
| S-12/S-13 | caliber + kg 只读 |
| D-04 | frontline 403 |
| Spec-5 边界 | rotate 404 |
