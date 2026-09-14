# Spec-2 · 治理壳（WP-03）

| 项 | 值 |
|----|-----|
| 状态 | 已确认；实现计划见 `docs/superpowers/plans/2026-09-14-aios-workstudio-governance-shell.md` |
| 日期 | 2026-09-14 |
| 战役 | 方案 B（用户 2026-09-14 选定） |
| 服从 | [Spec-0](./2026-09-12-aios-workstudio-modules-design.md) · [ARCHITECTURE_SPEC](../../strategic/design/UAS_AIOS_ARCHITECTURE_SPEC.md) |
| 前置 | Spec-1 契约测试全绿（责任图 / OSI / `cs.visit.*` / 协议附录 / IAM `pack_open` / scene 忽略 `X-Profile`） |
| 交付目录 | `projects/aios-workstudio/` + `services/hub-api/` |

**一句话：** Console 只走 `hub.ops.*`，入口强制 `profile=builder` + `X-Ops-Role`；一线锁页在服务端；配置写止于 ChangeSet；只实现 Spec-0 §5.7 标成 Spec-2 的端点。

**禁止：** 整份采用 `2026-09-11-aios-console-ops-design.md`；一次做完 `ops.ts` 全部约 30 个端点；NocoBase；改 Console 皮肤；git commit（除非用户明确要求）。

---

## 1. 目标与非目标

### 1.1 出站（本战役必须可测）

| 码 | 判据 |
|----|------|
| A7 | `X-Track: selfpaw` 调变更类 ops（publish / patch / changeset submit|decide）→ `TRACK_ESCALATION_REQUIRED`（403） |
| A9 | explore 可 cite 不可 execute（既有 `test_explore_execute_skill_forbidden` 保持绿；`ops/skill/list` 标明不可执行） |
| A10 | 责任图节点缺五件套 / 缺口径 → `graph/validate` 失败；`graph/publish` 拒绝。未审批 ChangeSet → `law.compile` 仍 `INVARIANT_FAILED`（I-09） |
| A11 | 用 `t-other` 读 `ag-hengchuan-ltc` / 衡川审计 → `TENANT_MISMATCH`（403） |
| I-09 | `changeset_approved=false` 不能把 Law 写入 compiled |
| I-12 | `GET /hub/v1/ops/schema/drift`：对照 `configs/protocol/registry.json`、`KERNEL.yaml`、`schemas/protocol/module_protocol.schema.json`；无漂移 `status=healthy` |
| D-02 | `graph/publish`、`registry/patch`、`changeset/submit` 都不改 live；HTTP 状态一律 **`pending`**（见 §4.2）。`#/publish` 调 `changeset/decide` 后才变为 `applied` 或 `rejected` |
| D-04 | `X-Ops-Role: frontline` 任意 `/hub/v1/ops/*` → 403；live compiled 不可 ops 原地 PATCH |
| D-07 | `audit/export` 自身追加一条审计事件 |

frontline 锁页：HTTP 403 后人话含「看不到 /console」（可复用 Demo 文案）。Console 已有前端 overlay，本战役必须加上服务端拒绝。

### 1.2 明确不做

| 划走 | Spec |
|------|------|
| `caliber/status` `kg.*` `model.route` `runtime.*` `artifact/list` | 3 |
| `memory/receipt`、`#/automation` `#/memory` `#/wm` 真连 | 4 |
| `connector/rotate` | 5 |
| `exec.open` / SSE / Temporal | 3 |
| Lethe 真擦除、NocoBase、改 `console.css` 视觉语言 | — |
| Console 调 `invoke_cs` 或 `/hub/v1/kg/ingest` | 永久否决 |

`POST /hub/v1/ops/wm/get` 作为 **只读端点** 实现（§5.7「Spec-2/4」的读半边），**不**把 `#/wm` 从 `data.js` 换成真连。

---

## 2. 架构

```
Console/demo
  hub-ops.js     原生 JS，路径字面量 = packages/hub-client/src/ops.ts 的 Spec-2 子集
  app.js         真连页 fetch；失败则沿用 data.js（只读降级条）
        │  只调 /hub/v1/ops/*   头：X-Tenant-Id, X-Actor-Id, X-Track, X-Ops-Role
        ▼
CapabilityHub/capability_hub/http_app.py
  /hub/v1/ops/*  统一 ops_envelope：信封 profile=builder，忽略 X-Profile；simulate 的 body.profile 仅作模拟参数
        ▼
uas_hub.Hub + 既有 Port 夹具（Evolution / Law / Iam / Registry / GraphStore / Audit 内存表）
```

- 一线 WorkStudio 继续只走 `hub.scene.*`；脚手架继续断言 `hub-scene.js` 不含 `/hub/v1/ops/`。
- 不新建第二套控制面。`capability_hub/ops/` 可以是薄函数模块，禁止在 ops 路由里 `invoke_cs`。
- 已有非 ops 路径保持：`GET /hub/v1/ops/profile/matrix` 纳入同一 envelope（今日无 `X-Ops-Role`，本战役补上）。
- 已有 `POST /hub/v1/iam/bindings`（绑定，要 ChangeSet）**不是** `GET /hub/v1/ops/iam/bindings`（列表）。两条并存，勿合并。

---

## 3. 管理流信封

所有 `/hub/v1/ops/*`：

1. **信封** `profile = "builder"`（路径强制；`X-Profile` 作废）。JSON 里的 `profile` **不得**改信封。唯一例外：`policy/simulate` 的 `body.profile` 是 **被模拟的剖面**（见 §4.3），不写进 `env.profile`。
2. 缺 `X-Tenant-Id` → `TENANT_MISMATCH`
3. 缺 `X-Ops-Role` 或值不在 `{admin, operator, sre, frontline}` → `GATE_BLOCKED`
4. `X-Ops-Role: frontline` → `SCOPE_DENIED`（403，人话含「看不到 /console」）。不读业务体。
5. `admin` / `operator` / `sre` 本战役权限相同（细角色拆分 YAGNI）
6. `X-Track: selfpaw` 且动词为写（见 §4.2）→ `TRACK_ESCALATION_REQUIRED`
7. 写动词（§4.2）若带 `Idempotency-Key`，相同键返回同一 ChangeSet；读路径不要求。
8. 判定序仍是 `inject → tenant → registry → rbac → approval → gates → scope → execute → audit`；ops 读路径可在 execute 返回夹具数据，但仍走 tenant/scope/audit

Console 角色下拉把 `state.role` 写入 `X-Ops-Role`。`cowen.hua` 在 IAM 夹具上是一线岗位，但 Console 角色与岗位绑定正交：打开 Console 看的是 `X-Ops-Role`，不是 `pos-cm`。

---

## 4. 端点（与 `ops.ts` 字面量一致）

### 4.1 本战役实现

| 页（真连） | 方法 | 路径 | 行为 |
|------------|------|------|------|
| overview | GET | `/hub/v1/ops/tenant/get` | `{ tenant_id, pack, graph_id }` 来自责任图样例 |
| overview | GET | `/hub/v1/ops/health/summary` | 夹具健康：含 `open_ms` 等键；`ungrounded_rate` 可来自洞察服务计数 |
| overview / integrate | GET | `/hub/v1/ops/schema/drift` | 见 §5 |
| control | GET | `/hub/v1/ops/profile/matrix` | **已有**，套上 ops envelope |
| control | POST | `/hub/v1/ops/policy/explain` | body `{ code }` → 与 `Hub.explain` 同构；**禁止** Console 用北向 `GET /hub/v1/policy/explain` |
| integrate | GET | `/hub/v1/ops/protocol/registry` | `load_registry()` |
| integrate | GET | `/hub/v1/ops/protocol/contracts` | 每模块 `protocol_id` + `port` + `hub_methods` |
| integrate | POST | `/hub/v1/ops/policy/simulate` | 见 §4.3 |
| ontology | POST | `/hub/v1/ops/graph/get` | body `{ graph_id? }`；租户必须匹配 |
| ontology | POST | `/hub/v1/ops/graph/validate` | 每节点 `node_incomplete`；缺维 → `ok:false` + `WM_INCOMPLETE` |
| ontology | POST | `/hub/v1/ops/graph/publish` | validate 不过则 `INVARIANT_FAILED`；过则新建 **pending** ChangeSet |
| govern | POST | `/hub/v1/ops/law/diff` | 夹具现行 SLA vs 候选；不 compile |
| mesh | GET | `/hub/v1/ops/registry/list` | `capability_registry.json` 操作名 |
| mesh | POST | `/hub/v1/ops/registry/patch` | 新建 **pending** ChangeSet，不写 `capability_registry.json` |
| mesh | GET | `/hub/v1/ops/mcp/preview?profile=` | 按剖面过滤工具；scene 不含 `cs.visit.schedule` |
| mesh | GET | `/hub/v1/ops/connector/list` | 夹具槽位；**无密钥明文** |
| mesh | GET | `/hub/v1/ops/skill/list` | 状态机列表；explore 行 `executable:false` |
| audit | GET | `/hub/v1/ops/audit/search?q=` | 过滤 `Hub.audit` |
| audit | GET | `/hub/v1/ops/audit/export?q=` | 同检索结果 + 追加 export 审计行 |
| dualtrack | GET | `/hub/v1/ops/iam/bindings` | 列出夹具绑定（含 `cowen.hua` / `pos-cm`） |
| evolution / publish | GET | `/hub/v1/ops/changeset/list` | `pending` / `applied` / `rejected` |
| evolution / publish | POST | `/hub/v1/ops/changeset/submit` | body `{ kind, summary? }`；新建 **pending**；`auto_apply` 恒 false |
| evolution / publish | POST | `/hub/v1/ops/changeset/decide` | body `{ changeset_id, approved }`；仅 `pending` 可决定；`true`→`applied`，`false`→`rejected`；`auto_apply` 仍 false |
| （只读、页不真连） | POST | `/hub/v1/ops/wm/get` | 读 `WmStore`；缺文档 403 `SCOPE_DENIED` |

`ops.ts` 已声明但本战役 **404 或显式 `OPERATION_NOT_FOUND` 即可**（不要实现）：`connector/rotate`、`artifact/list`、`caliber/status`、`kg/search`、`kg/ingest_status`、`memory/receipt`、`runtime/task`、`runtime/retry`、`model/route`。

`protocol/registry`、`protocol/contracts`、`policy/simulate` 不在当前 `ops.ts` 中。本战役 **必须追加** 这三个方法，字面量与上表路径一致。既有 `profile/matrix` 测试要补 `X-Ops-Role: admin`，否则套 envelope 后会红。

### 4.2 写动词与 ChangeSet 状态（A7 / D-02）

写动词：`graph/publish`、`registry/patch`、`changeset/submit`、`changeset/decide`。  
其余均为读。`policy/simulate` 与 `mcp/preview` 不落生产。

HTTP 状态机（冻结，不要再出现第三种「draft」对外状态）：

```
publish | patch | submit  →  pending
pending + decide(true)    →  applied
pending + decide(false)   →  rejected
applied / rejected        →  再 decide → INVARIANT_FAILED
```

`FixtureEvolution.draft` 今日返回 `status=draft`：ops 层必须映射为 **`pending`**，或改夹具与 HTTP 一致。Console `#/publish` 只展示 `pending`。

`decide(approved=true)` **不**自动 `law.compile`。compile 仍要显式 `changeset_approved=true` 走既有 `Hub.law_compile`（I-09）。A10 的「不能 release」= validate/publish 失败，不是静默 compile。

### 4.3 `policy/simulate`（信封 ≠ 模拟剖面）

- 信封恒 `env.profile = "builder"`（管理流）。
- body：`{ "operation": "cs.visit.schedule", "profile": "scene" }`。`body.profile` 只用于构造 **一次性模拟信封** 交给 `PolicyChain`，不得 `bind_thread`、不得改当前请求 `env`。
- **禁止** `invoke_cs`。返回 `{ "allowed": false, "code": "PROFILE_FORBIDS_SIDE_EFFECT", "message": "…" }` 之类。
- 缺 `body.profile` → 模拟剖面默认 `scene`（一线最常见误用），不要默认 builder（否则写操作模拟几乎无意义）。

---

## 5. I-12 漂移灯

`GET /hub/v1/ops/schema/drift` 返回：

```json
{
  "status": "healthy",
  "count": 0,
  "checks": [
    {"id": "registry.json", "ok": true},
    {"id": "KERNEL.yaml", "ok": true},
    {"id": "module_protocol.schema.json", "ok": true},
    {"id": "validate_registry", "ok": true}
  ]
}
```

`validate_registry() != []` 或三文件缺一 → `status=drift`，`count=问题数`。不在本战役发明第二份模块清单。

---

## 6. Console 接线

**真连页：** `#/overview` `#/control` `#/integrate` `#/ontology` `#/mesh` `#/govern` `#/audit` `#/dualtrack` `#/evolution` `#/publish`

**保持 `data.js` 并在页头标明「本战役离线」：** `#/run` `#/caliber` `#/workflows` `#/artifact`（若有）`#/automation` `#/memory` `#/wm`

实现要点：

- 新增 `Console/demo/hub-ops.js`（与 WorkStudio `hub-scene.js` 同模式）。只含 §4.1 路径。禁止 `/hub/v1/scene/`、`invoke_cs`、零件名词（`cubejs` `graphiti` `neo4j` `langgraph` `temporal` `lethe` `workflow_id` `CubeQL`）。
- `index.html` 在 `app.js` 前引入。
- Hub 可达：真连页用返回 JSON 渲染；overview 漂移灯读 `schema/drift`。
- Hub 不可达：顶栏「治理服务暂不可用，只读降级」，继续 `data.js`（对标 Spec-1 作战台降级）。
- 角色切到 frontline：请求应 403；继续走已有 `#lock-overlay`。
- 不改布局/配色；不把 33 端点 mock 进 `hub-ops.js`。

---

## 7. 测试与浏览器验收

### 7.1 自动化

- 新文件建议：`services/hub-api/tests/test_ops_governance.py` 或 `CapabilityHub/tests/test_ops_http.py`
- 每条 §4.1 路径至少 1 个 HTTP 用例（200 或约定错误）
- frontline → 全部抽样 403
- `t-other` + `graph/get` → `TENANT_MISMATCH`
- selfpaw + `changeset/submit` → `TRACK_ESCALATION_REQUIRED`
- `graph/validate` 对缺维节点 `ok:false`
- 未审批 `law_compile` 仍失败
- `audit/export` 后再 `search` 能看到 export 行
- `auto_apply` 在 submit/decide 响应中为 false
- 脚手架：`hub-ops.js` 含 `/hub/v1/ops/changeset/submit`、不含 `invoke_cs`；`hub-scene.js` 仍不含 ops

### 7.2 浏览器（实现计划 Task 末项）

1. Hub `:18088` + `python -m http.server 18090` cwd=`projects/aios-workstudio`
2. 打开 `http://127.0.0.1:18090/Console/demo/index.html#/audit`：审计来自 Hub，不是空白
3. `#/publish` 可见 pending；decide 后列表变化
4. 角色 frontline：锁页
5. 停 Hub 刷新：降级条 + 离线夹具仍可点

Windows 用 `curl.exe` 或 Python `urllib`，不要用 PowerShell 的 `curl`。

---

## 8. 文件预期（计划阶段再拆任务）

| 动作 | 路径 |
|------|------|
| 改 | `CapabilityHub/capability_hub/http_app.py` ops 路由 + 统一 envelope |
| 可新建 | `CapabilityHub/capability_hub/ops_service.py`（或 `uas_hub/ops_facade.py`）组合读路径 |
| 改 | `uas_hub/hub.py` / `graph_store.py` / adapters：仅当缺 list/validate/diff |
| 新建 | `Console/demo/hub-ops.js` |
| 改 | `Console/demo/index.html` `app.js`（接线，不改皮肤） |
| 改 | `packages/hub-client/src/ops.ts` 追加 `protocol/registry` `protocol/contracts` `policy/simulate` |
| 改 | `tests/test_scaffold.py` 断言 ops 客户端 |
| 测 | CapabilityHub + hub-api 新测 |

内核 Port 已存在则只再导出/列表，禁止复制第二份 Protocol。

---

## 9. 与旧稿对照

`2026-09-11-aios-console-ops` 的 V3「八页全部去硬编码」作废。本文件是 Spec-0 治理壳切片的实现规格，不是那份 33 端点计划的续篇。
