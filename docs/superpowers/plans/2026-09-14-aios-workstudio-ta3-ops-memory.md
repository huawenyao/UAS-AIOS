# Spec-4A TA-3 可运营（Hub 先）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Console memory/automation/wm 真连 ops；遗忘回执可测；自动化不静默生效；NocoBase 不做。

**Architecture:** OpsService 扩展 + http_app 路由；复用 FixtureMemory / WmStore；Demo hub-ops + app.js。

**Tech Stack:** Python / FastAPI / unittest / 原生 JS

**依从：** [`docs/superpowers/specs/2026-09-14-aios-workstudio-ta3-ops-memory-design.md`](../specs/2026-09-14-aios-workstudio-ta3-ops-memory-design.md)

**硬约束：** 不 commit；不改皮肤；frontline 403；无 ops ingest 写；rotate 仍 404。

---

### Task 1: memory receipt + forget

**Files:** `ops_service.py` `http_app.py` `test_ops_http.py`

- [x] **Step 1: 测试**

```python
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
        listed = self.client.get("/hub/v1/ops/memory/receipt?q=" + fr.json()["receipt_id"], headers=HDR)
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
```

原 `test_memory_receipt_still_404` 删除或改为 200 空列表。

- [x] **Step 3:** `_receipts` 列表；`memory_forget` / `memory_receipt`；路由改真实现。

---

### Task 2: automation jobs + run

- [x] **Step 1: 测试**

```python
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
```

- [x] **Step 3:** 夹具 jobs；run → `_put_pending`。

---

### Task 3: wm/list

```python
    def test_wm_list(self) -> None:
        self.client.post(
            "/hub/v1/wm/patch",
            headers=HDR,
            json={"world_model_id": "wm-demo", "lifetime": "draft", "body": {"x": 1}},
        )
        res = self.client.get("/hub/v1/ops/wm/list", headers=HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(any(i.get("world_model_id") == "wm-demo" for i in res.json()["items"]))
```

---

### Task 4: Demo 接线

- [x] `hub-ops.js`：memoryReceipt / memoryForget / automationJobs / automationRun / wmList  
- [x] `app.js`：离线芯片清空（无 automation/memory/wm）；boot 拉三路；render 适配  
- [x] scaffold 断言 path + 无三页离线常量

---

### Task 5: 回归

CapabilityHub + scaffold + hub-api memory 相关全绿；curl 冒烟。

---

## 不做

NocoBase、rotate、真 Lethe、git commit
