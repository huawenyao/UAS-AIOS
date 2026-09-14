# Spec-5 connector.rotate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `connector/rotate` 从 404 改为 pending ChangeSet + vault 指针；无明文；Demo 接线。

**Architecture:** OpsService.rotate → `_put_pending`；list 带 secret_ref；decide 后可选更新内存槽位指针。

**Tech Stack:** Python / FastAPI / unittest / 原生 JS

**依从：** [`docs/superpowers/specs/2026-09-14-aios-workstudio-connector-rotate-design.md`](../specs/2026-09-14-aios-workstudio-connector-rotate-design.md)

---

### Task 1: rotate HTTP TDD

- [x] **Step 1: 替换 `test_connector_rotate_still_404`**
- [x] **Step 3:** 实现 `connector_rotate`；改路由；`connector_list` 带 `secret_ref`；decide 批准后写 live 指针。

---

### Task 2: Demo

- [x] `hub-ops.js`：`connectorRotate`
- [x] `app.js`：rotate 调 Hub；scaffold 断言 path 存在

---

### Task 3: 回归全绿 + 勾计划

- [x] CapabilityHub ops HTTP + discover；scaffold

---

## 不做

真 KMS、NocoBase、git commit
