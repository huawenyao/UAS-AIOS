# Spec-3 · TA-2 可办成（WP-04/05）· A∥B 并行

| 项 | 值 |
|----|-----|
| 状态 | 已确认（用户 2026-09-14「ok 继续」；切入 A∥B） |
| 日期 | 2026-09-14 |
| 服从 | [Spec-0](./2026-09-12-aios-workstudio-modules-design.md) · [ARCHITECTURE_SPEC](../../strategic/design/UAS_AIOS_ARCHITECTURE_SPEC.md) |
| 前置 | Spec-1 / Spec-2 契约与治理壳全绿 |
| 交付目录 | `projects/aios-workstudio/` + `services/hub-api/` |

**一句话：** 轨 A 把 WorkStudio 办成主链接上已有 `exec.open` / `cycle_step` / events；轨 B 把 Spec-2 延期为 404 的 ops（caliber/kg/runtime/artifact/model）真实现并接线 Console 三页。夹具级，不启真 Temporal/Cube/Graphiti。

**禁止：** Celery；作战台 CubeQL；NocoBase；`connector.rotate`（Spec-5）；`memory.*` / `#/automation` `#/memory` `#/wm` 真连（Spec-4）；改 Console/WorkStudio 皮肤；git commit（除非用户明确要求）；一线 UI 露出 `workflow_id`。

---

## 1. 目标与非目标

### 1.1 出站（本战役必须可测）

| 码 | 判据 |
|----|------|
| A5/A6 | issue → `exec.open` → events 含 `awaiting_approval`（L2）→ `cycle_step` `approved` 后写入夹具；`rejected` 不写 |
| I-03 | Cube 不可用 / 未知 KPI → `stale=true`（既有夹具保持；`ops/caliber/status` 暴露 stale） |
| I-04 | 未接地不得 issue（Spec-1 已有；本战役回归） |
| I-06 | Activity/retry 仍进 Hub 门禁，不直打 CRM |
| I-07 | 内环工具仅白名单；本战役不新建第三套循环 |
| S-12 | `GET ops/caliber/status` 可读 OSI 口径态 |
| S-13 | `ops/kg/search` + `ingest_status` **只读**；**无** Console / ops ingest **写**路由 |
| D-04 | frontline 任意 `/hub/v1/ops/*` 仍 403 |
| 禁词 | Demo JS 无 `workflow_id` / CubeQL / Celery / langgraph / temporal 产品名（测试断言） |

### 1.2 明确不做

| 划走 | Spec |
|------|------|
| `memory/receipt`、`#/automation` `#/memory` `#/wm` 真连 | 4 |
| `connector/rotate`、槽位生产语义 | 5 |
| 真 Temporal Worker、真 Cube 进程、真 Graphiti | — |
| NocoBase、改皮肤、git commit | — |

---

## 2. 双轨架构

```
轨 A WorkStudio
  hub-scene.js ──execOpen/cycleStep/eventsPoll──▶ :18088
       │                                              │
  workstudio.js「进入执行」/「待你确认」          Hub.exec_* + InMemoryOuterLoop

轨 B Console
  hub-ops.js ──caliber/kg/runtime/artifact/model──▶ OpsService（真实现，非 404）
  app.js #/caliber #/run #/workflows 去掉「本战役离线」芯片
```

两轨并行、同一 PR/工作树；共享 `ops_envelope`；禁止 Console 调 `invoke_cs` / `kg/ingest`。

---

## 3. 轨 A · 办成主链

### 3.1 后端（已有，本战役只接线 + 验收）

- `POST /hub/v1/exec/open` → `Hub.exec_open`（profile 强制 runtime）
- `POST /hub/v1/instance/cycle_step` → `Hub.cycle_step`
- `GET /hub/v1/exec/{task_id}/events` → `Hub.exec_events`
- L2：`cs.visit.schedule` 等 → `awaiting_approval`；一线文案「待你确认」，**响应可含** `workflow_id` 供客户端内部使用，**UI 不得渲染**该字段

### 3.2 客户端

`projects/aios-workstudio/demo/hub-scene.js` 追加（对标 `packages/hub-client/src/scene.ts`）：

- `execOpen(task_id)`
- `cycleStep(task_id, signal)` — signal ∈ `approved` \| `rejected` \| `more_context`
- `eventsPoll(task_id)` — `GET` events（轮询即可，不强制 EventSource）

`workstudio.js`：在已有签发成功路径后提供「进入执行」；若 status=`awaiting_approval` 展示确认/驳回；Hub 不可达时保留 Spec-1 降级条，不假造成功。

### 3.3 测试

- 既有 `services/hub-api/tests/test_exec.py` 全绿
- scaffold：`hub-scene.js` 含 `/hub/v1/exec/open` 与 `/hub/v1/exec/` events；**不含**字面量 `workflow_id` 作为展示文案（允许注释外的代码键名仅在 JSON 解析侧；脚手架断言 Demo 渲染串无 `workflow_id`）

---

## 4. 轨 B · ops 真实现

### 4.1 端点（替换 Spec-2 的 OPERATION_NOT_FOUND）

| 方法 | 路径 | 行为 |
|------|------|------|
| GET | `/hub/v1/ops/caliber/status` | 聚合 OSI + Cube 样例；每项含 `key`/`stale`/`caliber_id`/`as_of` |
| GET | `/hub/v1/ops/kg/ingest_status` | `{lag_minutes, status, last_episode, failures:[]}` 夹具 |
| POST | `/hub/v1/ops/kg/search` | `hub.kg.search`；无 kg → 空 hits；**禁止** ingest 写 |
| GET | `/hub/v1/ops/runtime/task` | 列 `outer_loop.runs` 摘要（`task_id`/`status`/`updated`）；**不**把 `workflow_id` 作为一线字段强制返回到 Console 展示（API 可返回，Demo 不显示） |
| POST | `/hub/v1/ops/runtime/retry` | body `{task_id}` → 对已有 run `signal("approved")` 或等价再入；须经 `ops_envelope`；无 run → `TASK_NOT_ISSUED` |
| GET | `/hub/v1/ops/artifact/list` | `hub.artifact` 夹具列表或静态安全列表；报告不可当 pack 源 |
| GET | `/hub/v1/ops/model/route` | Broker 路由只读夹具 `{routes:[{id,provider,rpm}]}` |

`POST /hub/v1/ops/connector/rotate` **保持** 404 `OPERATION_NOT_FOUND`。

### 4.2 Demo

- `hub-ops.js`：上述方法从「不存在」变为真实 path（已有 stub 则改为可用）
- `app.js`：`pageHead` 离线芯片仅保留 `#/automation` `#/memory` `#/wm`（去掉 run/caliber/workflows）
- `bootHubOps`：追加拉 `caliberStatus` / `kgIngestStatus` / `runtimeTask` / `artifactList` / `modelRoute`，写入 `state` 供三页渲染；失败不炸，页内提示降级

### 4.3 测试

`test_ops_http.py`：七路径 admin 200；frontline 403；rotate 仍 404；kg search 响应无 secret；caliber 含 stale 字段。

---

## 5. 文件地图

| 文件 | 职责 |
|------|------|
| `capability_hub/ops_service.py` | 实现 §4.1 方法 |
| `capability_hub/http_app.py` | 404 薄路由改为调用 OpsService |
| `tests/test_ops_http.py` | 轨 B HTTP |
| `demo/hub-scene.js` | exec 三方法 |
| `demo/workstudio.js` | 执行态确认 UI 最小接线 |
| `Console/demo/hub-ops.js` | 轨 B 客户端 |
| `Console/demo/app.js` | 三页接线 + 芯片 |
| `tests/test_scaffold.py` | 禁词与 path 断言 |

---

## 6. 验收清单

1. `unittest`：hub-api + CapabilityHub + workstudio scaffold 全绿  
2. curl：issue→exec→events→cycle_step；ops caliber/runtime 200；frontline ops 403；rotate 404  
3. 浏览器：WorkStudio 待确认；Console `#/caliber` `#/run` `#/workflows` 有 Hub 数据或明确降级；停 Hub 双端降级  

---

## 7. 后续

- Spec-4：memory / automation / wm 运营 + NocoBase 壳  
- Spec-5：`connector.rotate` + 槽位生产语义  
