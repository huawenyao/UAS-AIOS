# aios-workstudio 全模块详细设计与接口对齐

| 项 | 值 |
|----|-----|
| 状态 | 设计稿（战役总册 + 接口内核）。**不是**一份实现计划 |
| 日期 | 2026-09-12 |
| 交付目录 | `projects/aios-workstudio/`（三壳）+ `services/hub-api/`（契约与夹具） |
| 服从 | [`UAS_AIOS_TOGAF_ENTERPRISE_ARCHITECTURE.md`](../../strategic/design/UAS_AIOS_TOGAF_ENTERPRISE_ARCHITECTURE.md) · [`UAS_AIOS_ARCHITECTURE_SPEC.md`](../../strategic/design/UAS_AIOS_ARCHITECTURE_SPEC.md) · [`UAS_AIOS_INTEGRATION_DESIGN.md`](../../strategic/design/UAS_AIOS_INTEGRATION_DESIGN.md) · [`UAS_AIOS_CONSOLE_DEMO_DESIGN.md`](../../strategic/design/UAS_AIOS_CONSOLE_DEMO_DESIGN.md) · ADR-SEL-001/002/003 |

**一句话：** 30 个模块只通过信封 + `hub.*`/`hub.ops.*` + Port SPI 说话；本仓实现三个壳，零件在 `services/`；接口名先冻结，实现按 Spec-1…5 切片落地。

---

## 0. 本文地位与读法

| 问 | 答 |
|----|-----|
| 这是实现计划吗？ | **否。** 实现计划按 §3 拆成 Spec-1…5，禁止把 30 个模块塞进一份 plan |
| 模块内部方案权威？ | `UAS_AIOS_MODULE_DESIGN.md`。本文只锁**对外接口、提供/消费、错误码、否决、Demo 入口、归属 Spec** |
| 交互时序权威？ | `UAS_AIOS_INTEGRATION_DESIGN.md` 的 S-01…S-26。本文把每条场景映射到接口与模块 |
| 机器可读权威落点？ | 实现时写入 `configs/protocol/registry.json` + `KERNEL.yaml`（附录 A/B 为设计原文） |
| `modules/*/SPEC.md`？ | 由 `catalog.json` 生成的目录卡，**不是**本文；改契约先改 catalog 再 `gen_specs.py` |

---

## 1. 战役边界

`projects/aios-workstudio` 交付三个产品壳，并让 30 个模块在壳上可运营、可验收。M14–M24 零件内核仍在 `services/`，禁止平行重建。

| 壳 | 模块 | 权威 Demo | 本仓职责 |
|----|------|-----------|----------|
| 使用平面 | M1 + M5 UI + SSE | `http://127.0.0.1:18090/demo/index.html` | 自研：只走 `hub.scene.*` / SSE |
| 控制面门面 | M6 | 被两壳调用 | 自研：`CapabilityHub` 薄路由，剖面由入口强制 |
| 治理 / 运维壳 | B1/B2/B4 + nocobase-shell | `#/audit` · `#/automation` | 只走 `hub.ops.*`，写止于 ChangeSet |

**「完成所有模块」：**

- **设计** = 本文（每模块提供/消费/Port/错误/否决/Demo/Spec）。
- **开发** = `implement` 写代码；`compose/shell` 写 UI 调 Hub；`consume` 只调 `hub.*`；`platform/external` 只做管理入口与红线演示。

**明确不做：** 在 workstudio 复制零件 SDK；一线菜单出现零件名；`auto_apply`；NocoBase 当数据核；Spec-6（A2A 跨租户 / Utopia 写路径）默认不写。

---

## 2. 三平面 × 模块 × Demo

双向规则：新增按钮必须能填进下表一行；`kind=platform` 本仓不出现零件 SDK。

### 2.1 使用平面

| 模块 | Demo | 一线动作 | Spec |
|------|------|----------|------|
| M1 | `#/{pack}/loop\|optimize\|deposit` + 执行态 | `pack.open`、403 人话 | Spec-1 |
| M5 | 卡口作战 → 签发 | 未接地不得 issue；任务带 `source_node_id` | Spec-1 |
| SSE | 执行态进度 | 只见「待你确认」 | Spec-3 |

### 2.2 治理平面

| 模块 | 页 | AU | CR | Spec |
|------|----|----|----|------|
| M11 | `#/audit` | AU-01 | 检索/导出（导出自审） | Spec-2 |
| M8 | `#/dualtrack` | AU-02 | 岗位绑定 | Spec-1 骨架 / Spec-2 壳 |
| M17 | `#/memory` | AU-10 | 遗忘→回执 | Spec-4 |
| M12 | `#/evolution` | AU-08 | 草案评审 | Spec-2 |
| M4 | `#/govern` `#/evolution` | AU-08 | 条文草案 | Spec-2 |

### 2.3 运维 / 控制

| 模块 | 页 | AU/CR | Spec |
|------|----|-------|------|
| 作业中心 | `#/automation` | AU-01…12 只产建议 | Spec-4 |
| M2 | `#/ontology` | 五件套巡检 / 节点 ChangeSet | Spec-1 切片读 / Spec-2 publish 页 |
| M3 | `#/wm` | 漂移 / draft；live 不可改 | Spec-1 夹具 / Spec-4 运营页 |
| M6 | `#/control` `#/integrate` | dry-run 不落生产 | Spec-1 门禁 / Spec-2 页 |
| M7 / M13 / M9 | `#/mesh` | 目录、list≠call、货架 | Spec-1 目录与双检 / Spec-2 mesh 读路径 |
| M20 | `#/overview` / `#/integrate` | Schema 漂移灯（端点 Spec-2；契约文件 Spec-1） | Spec-1 契约 / Spec-2 端点 |
| M10 | `#/publish` 关联 | 报告不能当 pack 源 | Spec-3 |
| M14 / M23 | `#/mesh` | 槽位 / object_ref | Spec-5 |
| M15 | `#/caliber` | stale / 口径草稿 | Spec-3 |
| M16 | `#/run` | ingest lag / 白名单 | Spec-3 |
| M18 / M19 | `#/workflows` | 卡点催办；一线无内部编号 | Spec-3 |
| M24 | `#/run` | 配额 → ChangeSet | Spec-3 夹具 |
| M21 | 转派 | P0 `task.transfer` | Spec-6 默认不做 |
| M22 | 开关位 | 默认不部署 | Spec-6 |
| IdP | `#/dualtrack` | 只提供人 | Spec-1 |

---

## 3. Spec 序列

```
Spec-0（本文）──批准──▶ Spec-1 TA-1 可经营（WP-01/02 + WP-03 骨架）
                         ├─ Spec-2 治理壳（WP-03）     可与 Spec-1 契约测试全绿后并行
                         └─ Spec-3 TA-2 可办成（WP-04/05）依赖签发落库，不依赖治理页
                              └─ Spec-4 TA-3 可运营（WP-06/07）
                                   └─ Spec-5 连接器（WP-08）
```

| Spec | 出站 | 不做 |
|------|------|------|
| 0 | 本文批准；附录 A 可生成 `registry.json` | 代码 |
| 1 | A1–A4、A12；I-02 / I-05 / I-10；Demo 见 `an-stage-visit` gate | Temporal/Cube/Graphiti 真进程；Console 真连；NocoBase |
| 2 | A7、A9、**A10**、A11；I-09；I-12 端点；D-02/D-04/D-07；frontline 锁页 | Lethe 真擦除；33 ops 一次做完；caliber/runtime/memory/rotate |
| 3 | A5、A6；I-03/I-04/I-06/I-07 | Celery；作战台 CubeQL |
| 4 | A8；I-08；D-01/D-03/D-05/D-06 | 静默生效 |
| 5 | Worker 无 SoR 明文；不复制主档 | 自研 CRM |
| 6 | 默认不写 | 跨租户 A2A；Utopia 写路径 |

**已有资产处置（禁止整份旧稿当 Spec-2 开干）：**

| 旧稿 `2026-09-11-aios-console-ops-design.md` | 划到 |
|-----------------------------------------------|------|
| G1–G3、G10：责任图样例、OSI、`cs.visit.*`、`gate_map.json`、附录 A/B 落盘 | **Spec-1** |
| G7：scene/exec 入口强制 profile（忽略 `X-Profile`） | **Spec-1** |
| G7：ops 入口强制 `profile=builder` + `X-Ops-Role` + frontline 锁页 | **Spec-2** |
| 治理页真连：`#/audit` `#/dualtrack` `#/evolution` `#/govern` `#/publish` + overview/control/integrate/ontology/mesh **读路径** | **Spec-2** |
| `GET ops/schema/drift`（overview / integrate 漂移灯） | **Spec-2** |
| `caliber.*` `kg.*` `model.route` `runtime.*` `artifact.*` | **Spec-3** |
| `memory.receipt`、`#/automation` `#/memory` `#/wm` | **Spec-4** |
| `connector.rotate` 及槽位生产语义 | **Spec-5** |
| 33 个 ops 端点「一次全部实现」 | **作废**；按上表切片，禁止 Spec-2 重做 Spec-1 或吞掉 3/4/5 |
| NocoBase W0–W12 | **Spec-4** |

---

## 4. 硬约束

AP-02 首页=`pack.open`。AP-03 控制面唯一。AP-04 只见 `cs.*`。AP-05 剖面入口强制、同 Thread 改剖面 409。AP-06 ΠPaw 读 Lethe 403。AP-07 写止于 ChangeSet，`auto_apply` 永关。AP-08 换零件不改 `hub.*` 与一线名词。AP-09 外环耐久。AP-10 list≠call。AP-11 审计追加写。AP-12 会话内不改生产知识。AP-13 一线无零件名。

**冲突裁决：** 德压过术（ADR-SEL-003）。

**本仓否决：** Next/Remix；Node 写门禁；聊天当状态；`ops/**` 出现 `invoke_cs`、`/hub/v1/kg/ingest`、零件名、`CollectionBlockModel`；未要求时 git commit。

**文档冲突：** 原则/WP → TOGAF；字段/A1–A12 → ARCHITECTURE_SPEC；序列 → INTEGRATION；Console 角色 → ADMIN_CONSOLE；Demo 行为 → CONSOLE_DEMO_DESIGN + 现网 demo；本仓角色 → `modules/catalog.json`；本战役切分 → **本文**。

---

## 5. 接口内核（模块间唯一对齐层）

### 5.1 三条流分名（R-1）

| 流 | 协议前缀 | 消费者 | 写规则 |
|----|----------|--------|--------|
| 控制流 | 信封 + PolicyChain | 全部入口 | profile 由路径强制，客户端 `X-Profile` **作废** |
| 数据流 | `hub.scene.*` / `hub.exec.*` / SSE | WorkStudio | 场景禁写 cs；签发不启工作流 |
| 管理流 | `hub.ops.*` | Console | 写 → ChangeSet；`X-Ops-Role`；frontline 403 |

跨流（例如 Console 调 `invoke_cs`）= 设计错误，测试拒绝。

### 5.2 公共信封

与 `uas_hub.errors.Envelope` + `module_protocol.schema.json` 对齐。HTTP 头映射：

| 字段 | 头 / 体 | 强制点 |
|------|---------|--------|
| `tenant_id` | `X-Tenant-Id` | 缺 → `TENANT_MISMATCH` |
| `actor_id` | `X-Actor-Id` | 缺 → `anonymous`，I-10 将失败 |
| `profile` | **忽略客户端**；由 `/scene`→scene、`/exec`→runtime、`/ops`→builder | 伪造作废 |
| `track` | `X-Track` 默认 `pipaw` | selfpaw 写经营 → `TRACK_ESCALATION_REQUIRED` |
| `correlation_id` | `X-Correlation-Id` | 贯穿审计；缺则服务端生成 |
| `idempotency_key` | `Idempotency-Key` | 写 cs / issue / ChangeSet 必填（读可空） |
| `thread_id` | `X-Thread-Id` | 同 Thread 改剖面 → 409 `THREAD_PROFILE_IMMUTABLE` |
| `source_node_id` | JSON 体 | issue/drill 必填 |
| `position_id` | JSON 体 `pack.open`；IAM 绑定权威 | 无绑定 → I-10 |

错误体（所有 `hub.*` 统一，UI 必须渲染 `message`）：

```json
{ "error": { "code": "PROFILE_FORBIDS_SIDE_EFFECT", "message": "…", "explain_ref": "hub.policy.explain", "next": "hub.scene.task.issue", "retryable": false, "detail": "" } }
```

零件缺失不 500：`{ "available": false, "reason": "…", "stale": true }` + 人话（I-01/I-03）。

### 5.3 判定序（不可颠倒）

`PolicyChain.ORDER` ≡ `registry.json.policy_order`：

`inject → tenant → registry → rbac → approval → gates → scope → execute → audit`

`ops/policy/simulate` **只跑到 execute 之前**，不调连接器。MCP `tools/call` 必须重走全序（list 已过滤不能跳过）。

### 5.4 八协议（北/南/东/西/知识/水平/身份/演化）

| 向 | 边 | 协议 | 禁止 |
|----|----|------|------|
| 北 | M1 → M6 | HTTPS JSON `hub.scene.*` + SSE | 零件 SDK |
| 南 | M6 → M14 → M23 | 内部 `ConnectorPort.invoke` | 密钥出进程；模型见 REST |
| 东 | M6 ↔ M18 | Workflow/Activity；一线不见 `workflow_id` | Celery 当寿命 |
| 西 | M6 → M19 | `InnerLoopPort`；工具只回调 Hub | 节点直打 CRM |
| 知识 | M6 → M15/M16/M17 | Port.query/search/self.* | 仓 View 当唯一真相；ΠPaw 读 Lethe |
| 水平 | M21 | P0 `hub.task.transfer` | P0 跨租户 |
| 身份 | IdP → M8 | OIDC；承诺权在 Hub | IdP 角色当经营权 |
| 演化 | 全模块 → M12 | ChangeSet；`auto_apply=false` | 会话内 PATCH 生产知识 |

### 5.5 Port SPI（零件可换、方法名不换）

权威代码：`services/hub-api/uas_hub/ports.py`。`protocol_catalog.REQUIRED_PORTS` 必须被本表覆盖。

| Port | 模块 | 方法 | 语义红线 |
|------|------|------|----------|
| `CubePort` | M15 | `query(...)` | 失败 `stale=True`，不得签发 |
| `KgPort` | M16 | `search` / `ingest_episode` | episode id 禁 `an-*`；ingest ≠ cs 写 |
| `MemoryPort` | M17 | `add/search/forget` | 分库；轨道禁令由 Hub 先判 |
| `InnerLoopPort` | M19 | `start_thread/turn/interrupt/resume/compact` | 无出站 SoR |
| `OuterLoopPort` | M18 | **现状缺口：ports.py 未声明** | HITL/续跑语义不可用 Celery 替代 |
| `ConnectorPort` | M14 | `invoke/health` | 返回与 description 无密钥 |
| `McpPort` | M13 | `list_tools/call_tool` | call 重走 PolicyChain |
| `SkillPort` | M9 | `transition/state_of` | explore 最高 cited |
| `LawPort` | M4 | `compile(pack_id, changeset_approved)` | 未审批不得 compiled |
| `ArtifactPort` | M10 | `put/get/usable_as_pack_state` | `kind=file` 不能驱动 pack.open |
| `BrokerPort` | M24 | `complete` | 换提供商不改 hub.* |
| `EvolutionPort` | M12 | `draft/apply`；`auto_apply: bool` | auto_apply 恒 false |
| `IamPort` | M8 | `bind/position_of` | 无岗位切片拒绝 |
| `ReviewPort` | M22 | `export_candidates` | 只读；默认不部署 |

**对齐动作（Spec-1 最小集）：** 在 `ports.py` 补 `OuterLoopPort`（与现有 `OuterLoopPort` 类型别名/`InMemoryOuterLoop` 对齐：`start(task)` / `signal`），使 `REQUIRED_PORTS` 可被 registry 引用。不在 Spec-1 接真 Temporal。

### 5.6 北向：`hub.scene.*` / `hub.exec.*`（WorkStudio 唯一入口）

与 `packages/hub-client/src/scene.ts` **方法名冻结**。路径由 `uas_hub/http_app.py` 提供。

| 客户端 | HTTP | 提供模块 | 消费 | 成功后状态 |
|--------|------|----------|------|------------|
| `packOpen` | `POST /hub/v1/scene/pack/open` | M6+M2+M8+M15 | M1 | 切片；kpi 可 stale |
| `packList` | `GET /hub/v1/scene/pack/list` | M6 | M1 | CapabilityHub 已有 |
| `insightDrill` | `POST /hub/v1/scene/insight/drill` | M5+M2+M16 | M1 | Insight；未接地 `grounded=false` |
| `insightList` | `GET /hub/v1/scene/insight/list` | M5 | M1 | CapabilityHub 已有 |
| `taskIssue` | `POST /hub/v1/scene/task/issue` | M5+M10 | M1 | Task=`issued`，`workflow_id=null` |
| `taskReturn` | `POST /hub/v1/scene/task/return` | M5+M12 | M1 | 驳回信号 |
| `explain` | `GET /hub/v1/policy/explain` | M6 | **仅 M1**（北向）。Console 必须走 `POST /hub/v1/ops/policy/explain`，禁止跨流 | 人话 |
| `execOpen` | `POST /hub/v1/exec/open` | M18 | M1 执行态 | Spec-3 |
| `cycleStep` | `POST /hub/v1/instance/cycle_step` | M18 | M1 | Spec-3 |
| `eventsUrl` | `GET /hub/v1/exec/{id}/events` | SSE | M1 | Spec-3 |
| （探针） | `POST /hub/v1/scene/invoke_cs` | M6 必 403 | 测试 A2 | 永不进一线菜单 |
| `task.transfer` | `POST /hub/v1/task/transfer` | M21 P0 | 指挥舱 | ID 链不断 |

一线 **禁止** 调用任何 `/hub/v1/ops/*`。

### 5.7 管理向：`hub.ops.*`（Console 唯一入口）

与 `packages/hub-client/src/ops.ts` **路径冻结**。写动作不得绕过 ChangeSet（除遗忘处置走 L3 合规语义，见 S-14）。

| 页 | 已声明端点 | 提供 | 归属 |
|----|------------|------|------|
| overview | `tenant/get` `health/summary` | M6 | Spec-2 |
| control | `profile/matrix` `policy/explain` | M6 | Spec-1 matrix 已有；explain Spec-2 POST |
| integrate | `protocol/registry` `protocol/contracts` `policy/simulate` | M20/M6 | Spec-2 新增 3 个 |
| ontology | `graph/get` `graph/validate` `graph/publish` | M2+M12 | Spec-2 |
| wm | `wm/get` | M3 | Spec-2/4 |
| govern | `law/diff` | M4 | Spec-2 |
| mesh | `registry/list|patch` `mcp/preview` `connector/list|rotate` `skill/list` | M7/M13/M14/M9 | Spec-2 读 / Spec-5 rotate |
| audit | `audit/search` `audit/export` | M11 | Spec-2 |
| dualtrack | `iam/bindings` | M8 | Spec-2 |
| memory | `memory/receipt` | M17 | Spec-4 |
| evolution/publish | `changeset/list|submit|decide` | M12 | Spec-2 |
| caliber | `caliber/status` | M15 | Spec-3 |
| run | `kg/search` `kg/ingest_status` `model/route` | M16/M24 | Spec-3 |
| overview / integrate | `schema/drift` | M20 | Spec-2（契约文件仍 Spec-1 落盘） |
| workflows | `runtime/task` `runtime/retry` | M18 | Spec-3 |
| artifact | `artifact/list` | M10 | Spec-3 |

`graph/publish`、`registry/patch`、`connector/rotate`、`changeset/decide` = 草案或元数据，**不** `invoke_cs`。

### 5.8 ID 链与状态机（跨模块一致性）

```
node_id (M2) ─drill→ insight_id (M5/M10) ─issue→ task_id (M5) ─exec.open→ workflow_id (M18)
     ▲                                                                      │
     └──────── RefreshKpi (M15) 同一 node_id 合流 (I-11) ◄──────────────────┘
correlation_id 贯穿 M11 全部行
```

| Task | Temporal | 进入 |
|------|----------|------|
| issued | 无 | `task.issue`（Spec-1 停在这里） |
| running | Running | `exec.open`（Spec-3） |
| awaiting_approval | WaitForSignal | L2+ |
| succeeded / succeeded(degraded) | Completed | RefreshKpi 成功 / SoR 已写刷新失败 |
| failed / returned | Failed / Terminated | S-05 / 驳回 |

WM：`draft → compiled → live`。Runtime PATCH compiled 恒 422。

kpi：`ought` 在责任图；`is(fresh|stale)` 只从 Cube 投影。

### 5.9 现状对齐缺口（实现必须消掉）

| # | 缺口 | 后果 | 关闭于 |
|---|------|------|--------|
| G1 | `configs/accountability_graph.sample.json` 缺失 | `Hub.from_repo()` 炸；阶段 A 测试不能跑 | Spec-1 |
| G2 | `configs/protocol/registry.json` / `KERNEL.yaml` 缺失 | `validate_registry` 无法跑；模块间无机器契约 | Spec-1 写入附录 A/B |
| G3 | `cs.visit.list/schedule`、`cs.metric.query` 不在 capability_registry | A2/MCP/水合无目录项 | Spec-1 |
| G4 | `demo/workstudio.js` 零 `fetch`；`scene.ts` 未接线 | Demo 与 Hub 两张皮 | Spec-1 |
| G5 | `IamPort.position_of` 未接入 `pack_open` | I-10 未在打开切片时强制 | Spec-1 |
| G6 | HTTP envelope 未带 `position_id` | 切片只靠 body，IAM 对不上 | Spec-1 |
| G7 | CapabilityHub `_envelope` 允许客户端 `X-Profile` 覆盖 | 违反 AP-05 | Spec-1 scene/exec；Spec-2 ops |
| G8 | `OuterLoopPort` 在 REQUIRED_PORTS 但 `ports.py` 无此 Protocol | 接口层自相矛盾 | Spec-1 补 Protocol，实现仍用内存夹具 |
| G9 | `capability_hub/ops/` 不存在；ops.ts 已声明路径无服务端 | Console 只能离线 fixture | Spec-2 只实现 §5.7 标成 Spec-2 的端点，禁止按 30 个一次做完 |
| G10 | `gate_map.json` 测试要求存在 | `test_phase_a` 失败 | Spec-1 |

---

## 6. 模块详细设计（M1–M24）

每张卡格式：**提供**（谁调用）/ **消费**（它调谁）/ **Port** / **错误** / **否决** / **Demo** / **Spec**。字段级 schema 仍以 `schemas/` 为准。

### M1 WorkStudio · own-shell · 使用平面

岗位工作台。路由即场景，打开 = `pack.open`。

- **提供：** 一线 UI（loop/optimize/deposit + 执行态）。
- **消费：** 仅 §5.6 北向。Hub 宕 → 顶栏人话 + `ltc-workbench.js` 只读降级。
- **Port：** 无。
- **错误：** 渲染 `error.message`；调 `policy.explain`。
- **否决：** 零件 SDK；Next/Remix；聊天当状态；一线菜单连接器。
- **Demo：** `demo/index.html`。
- **Spec-1。**

### M2 责任图 · own · 不替换

同一类节点：Goal × org × KPI × process × 五维。禁止四套树。

- **提供：** `pack.open` 切片；`ops/graph/get|validate|publish`。
- **消费：** 发布走 M12 ChangeSet；水合调 M15（内部，不经模型）。
- **Port：** 无（L0 自研）。
- **错误：** 缺维节点标 `WM_INCOMPLETE` 不阻断整包；无切片 `SCOPE_DENIED`。
- **否决：** Graphiti 当 L0；NocoBase Collection 当 `ag_node`。
- **Demo：** WorkStudio 看板；`#/ontology`。
- **Spec-1 读 / Spec-2 publish。**

### M3 世界模型 Store · own · 三寿命

- **提供：** `hub.wm.get/patch`；`ops/wm/get`。
- **消费：** Law.compile 写入 compiled；Runtime 只 PATCH live。
- **错误：** PATCH compiled → 422。
- **否决：** WM 塞进 Graphiti；live 改 compiled。
- **Demo：** `#/wm`。
- **Spec-1 夹具 / Spec-4 运营页。**

### M4 Law Pack · own · LawPort

- **提供：** `hub.law.compile`；`ops/law.diff`。
- **消费：** M12 审批位；编译进 M3 compiled。
- **错误：** 未审批 compile 拒绝（I-09）。
- **否决：** 会话内改生产知识；Temporal 解释 Law。
- **Demo：** `#/govern` `#/evolution`。
- **Spec-2。**

### M5 Insight→Task · own

- **提供：** `insight.drill` `task.issue/return/transfer(P0)`。
- **消费：** M2 节点；M16/M15 证据；M10 落制品；**不**调 M18。
- **错误：** `TASK_SOURCE_REQUIRED` `UNGROUNDED_INSIGHT` `WM_INCOMPLETE` `CALIBER_MISSING` `SCOPE_DENIED`。
- **否决：** 无源任务；未接地派活；签发即启工作流。
- **Demo：** 卡口作战签发。
- **Spec-1。**

### M6 Capability Hub · own · 永不外包

- **提供：** 全部 `/hub/v1/*`；判定序；`policy.explain`；审计追加。
- **消费：** 只经 Port / GraphStore / Registry；不持 SoR 密钥。
- **错误：** `uas_hub.errors.EXPLAIN` 全表（ARCHITECTURE_SPEC 字段为准）；未知码不得无 `message`。
- **否决：** Dify 当 Hub；Node 写门禁；第二套注册中心。
- **Demo：** 无独立页。
- **Spec-1 门禁 / Spec-2 ops 面。**

### M7 Registry · own-contract

- **提供：** 语义动作目录；`ops/registry/list|patch`；MCP 工具名同源。
- **消费：** git `configs/capability_registry.json`；patch → M12。
- **错误：** `OPERATION_NOT_FOUND`。
- **否决：** 两份手写 schema；模型可见 URL/SQL/密钥。
- **Demo：** `#/mesh`。
- **Spec-1 补 cs.visit.* / Spec-2 patch。**

### M8 IAM · own-contract · IamPort

- **提供：** `position_of` 给 pack.open；`ops/iam.bindings`。
- **消费：** IdP 只提供人；绑定变更 = permissionChangeSet。
- **错误：** 无岗位 → 切片拒绝（I-10）；selfpaw 写经营 → `TRACK_ESCALATION_REQUIRED`。
- **否决：** 自研登录；IdP 角色当承诺权。
- **Demo：** `#/dualtrack`。
- **Spec-1 接入 pack_open / Spec-2 页。**

### M9 Skill · own · SkillPort

- **提供：** `hub.skill.transition`；`ops/skill/list`。
- **消费：** 无循环内核。
- **错误：** `SKILL_NOT_EXECUTABLE_IN_PROFILE`（A9）。
- **否决：** explore 直接 execute。
- **Demo：** `#/mesh` 货架。
- **Spec-1 状态机已有 / Spec-2 列表。**

### M10 Artifact · own · ArtifactPort

- **提供：** Insight/Task/ThemePack 元数据；`ops/artifact/list`。
- **消费：** 对象存储可换。
- **否决：** file kind 驱动 pack.open；用报告回放经营。
- **Spec-3。**

### M11 Audit · own

- **提供：** 追加写链；`ops/audit/search|export`。
- **消费：** 所有模块经 M6 埋点；导出动作自审。
- **否决：** Cube 当审计；改删记录。
- **Demo：** `#/audit`。
- **Spec-1 内存追加 / Spec-2 检索导出。**

### M12 Evolution · own · EvolutionPort

- **提供：** `changeset.list/submit/decide`；`auto_apply` 恒 false。
- **消费：** 信号来自驳回/超时/漂移；回写 M4/M7/M2。
- **错误：** 回归未过禁发布；评审人=提交人拒绝。
- **否决：** 请求头打开 auto_apply。
- **Demo：** `#/evolution` `#/publish`。
- **Spec-2。**

### M13 MCP Gateway · own-shell · McpPort

- **提供：** `POST /hub/v1/mcp/tools/list|call`；`ops/mcp/preview`。
- **消费：** 同一 PolicyChain。
- **错误：** scene 写工具不可见；call 仍 403（I-05）。
- **否决：** 私有 WS 帧；密钥进 description。
- **Demo：** `#/mesh` `#/integrate`。
- **Spec-1 双检。**

### M14 Connector · own-contract · ConnectorPort

- **提供：** 内部 invoke；`ops/connector/list|rotate`。
- **消费：** KMS 引用；每 SoR 一进程（Spec-5）。
- **否决：** LangGraph 内 httpx CRM；凭证进 Demo。
- **Demo：** `#/mesh` `#/automation` AU-04。
- **Spec-5；Spec-1 可用 Mock。**

### M15 Cube+OSI · integrate · CubePort · 可替换

- **提供：** `cs.metric.query`；`ops/caliber/status`。
- **消费：** OSI YAML。失败标 stale。
- **错误：** `CALIBER_MISSING`；宕机不 500。
- **否决：** 作战台 CubeQL；LookML 当唯一真相。
- **Demo：** `#/caliber`。
- **Spec-1 水合夹具 / Spec-3 页。**

### M16 Graphiti · integrate · KgPort · 可替换

- **提供：** `hub.kg.search`；`ops/kg/search|ingest_status`。
- **消费：** ingest 仅服务账号，Console 无 ingest UI。
- **否决：** Dify 知识库当 L2；图谱页写 CRM。
- **Demo：** `#/run`。
- **Spec-3；Spec-1 drill 可用夹具 evidence。**

### M17 Lethe · integrate · MemoryPort · 可替换

- **提供：** `hub.memory.self.*`；`ops/memory/receipt`。
- **消费：** 独立库；无 FK 到责任图。
- **错误：** ΠPaw → `MEMORY_TRACK_FORBIDDEN`（A8/I-08）。
- **否决：** Mem0 默认；与 `ag_node` 同 schema。
- **Demo：** `#/memory`。
- **Spec-4。**

### M18 Temporal 外环 · integrate · OuterLoopPort

- **提供：** `exec.open` `cycle_step` SSE；`ops/runtime/task|retry`。
- **消费：** Activity 回调仍进 M6（I-06）。
- **否决：** Celery；一线 `workflow_id`。
- **Demo：** `#/workflows`；执行态「待你确认」。
- **Spec-3。**

### M19 InnerLoop · integrate · InnerLoopPort

- **提供：** turn；工具回调 Hub。
- **消费：** 只见 MCP/cs 白名单。
- **否决：** CrewAI；第三套循环；直打 CRM（I-07）。
- **Demo：** `#/workflows` 内环面板。
- **Spec-3。**

### M20 Schema · own-contract

- **提供：** `ops/schema/drift`；CI 三处同源（I-12）。
- **消费：** `schemas/*.json` + registry 生成 Pydantic/MCP。
- **否决：** 只写 Pydantic 再反推；任意 dict 进连接器。
- **Demo：** `#/overview` / `#/integrate` 漂移灯（不在 `#/run`）。
- **Spec-1 落盘附录 A 使 `validate_registry()=[]`；Spec-2 实现 `GET ops/schema/drift`。**

### M21 转派 / A2A · own-contract（P0）

- **提供：** `hub.task.transfer`。P1+ Agent Card 默认不做。
- **消费：** M8/M10；对端仍进 Hub。
- **否决：** Card 签名替代门禁；P0 跨租户。
- **Spec-6 默认跳过；P0 方法已存在可被 Spec-1 测试引用。**

### M22 Utopia · optional · ReviewPort

- **提供：** `export_candidates` 只读。
- **否决：** 当 L2；生产写。默认不部署。
- **Spec-6。**

### M23 SoR · connect · port=null

- **提供：** 客户系统 API（仅连接器内）。
- **消费：** UAS 只存 `object_ref`。
- **否决：** 自研轻量 CRM；主档进 NocoBase。
- **Spec-5。**

### M24 Broker · connect · BrokerPort · 可替换

- **提供：** `complete`；`ops/model/route`。
- **否决：** 聊天历史当状态。
- **Demo：** `#/run`。
- **Spec-3 夹具。**

---

## 7. 壳与外部（catalog 非 M1–M24）

| ID | 设计 | 接口 | Spec |
|----|------|------|------|
| SSE | Hub 扇出；指挥舱只投影 | `GET /hub/v1/exec/{task_id}/events` | Spec-3 |
| nocobase-shell | 壳非核；禁 Collection/workflow/ai/mcp-server | 只调 hub.ops | Spec-4 |
| B1 Hub Console | 剖面矩阵、dry-run | `profile/matrix` `policy/simulate` | Spec-2 |
| B2 Pack Studio | 法则/技能/制品表单 | changeset + law/skill/artifact | Spec-2/4 |
| B4 Governance | 合规不派活 | iam/audit/memory | Spec-2/4 |
| IdP | OIDC 只提供人 | 实验室 Keycloak；承诺权在 M8 | Spec-1 夹具账号即可 |

---

## 8. 场景 → 接口对齐（S-xx）

| 场景 | 模块序 | 冻结接口 | 归属 |
|------|--------|----------|------|
| S-01 看见 | M1→M6→M2→M15→M8 | `pack.open` | Spec-1 |
| S-02 洞察 | M1→M5→M2→M16 | `insight.drill` | Spec-1（证据可夹具） |
| S-03 办成 | M1→M5→M18→M19→M13→M14→M15→M2→M11 | `task.issue` 然后 `exec.open` | issue=Spec-1；其后 Spec-3 |
| S-04 审批 | M18→M1→M6 | `cycle_step`；SSE「待你确认」 | Spec-3 |
| S-05 补偿 | M14/M18 | 幂等键；degraded+stale | Spec-3/5 |
| S-06 演化信号 | M5→M12 | `task.return` → draft | Spec-2 |
| S-07 指挥舱 | M1→M2→M15 | 同口径子树；事件投影 | Spec-1 只读切片 / Spec-3 合流 |
| S-10 图发布 | Console→M2→M12 | `graph/validate|publish` | Spec-2 |
| S-11 Law | Console→M4→M12→M3 | `law.diff` + compile | Spec-2 |
| S-12 口径 | git OSI→M15 | `caliber.status` | Spec-3 |
| S-13 ingest | 服务账号→M16 | **无** Console ingest；无 ops ingest 写路由 | Spec-3 |
| S-14 遗忘 | M17→M11 | `memory.self.forget` + receipt | Spec-4 |
| S-20 能力发布 | M7→M20→M12→M13 | `registry.patch` + drift | Spec-2 |
| S-21 连接器 | M14+KMS | `connector.rotate` | Spec-5 |
| S-22 岗位 | IdP→M8→M2 | `iam.bindings` | Spec-1/2 |
| S-23 双轨 | M6→M8 | `TRACK_ESCALATION_REQUIRED` | Spec-2 |
| S-24 审计导出 | M11 | `audit.search/export` 自审 | Spec-2 |
| S-25 转派 | M1→M21 | `task.transfer` | P0 可用；跨租户 Spec-6 |
| S-26 评审汇合 | M12 | `changeset.decide` | Spec-2 |

---

## 9. Spec-1 实现边界（本文批准后的下一份 plan）

**目标：** WorkStudio 真连 `hub.scene.*`；打开见 `an-stage-visit` gate。

```
demo/index.html ──scene.ts──▶ CapabilityHub :18088 ──▶ Hub
                                  profile 强制 scene
Hub ← accountability_graph.sample.json + Registry + IamPort.position_of
```

**做：** G1–G8、G10；IAM 接入 pack_open；scene 写 403+人话；issue 停在 `issued`。  
**不做：** exec.open 真工作流；ops 33 端点；NocoBase；Console 改离线 Demo 皮肤。

测试：`Hub.from_repo()`；`test_phase_a` A1；HTTP A2/A3/A4/A12；I-10；脚手架无零件名词；浏览器 `18090/demo` + `18088`。

---

## 10. 验收总表（跨 Spec）

| 码 | 判据 | Spec |
|----|------|------|
| A1 | 打开见 `an-stage-visit` gate | 1 |
| A2 | scene 调 `cs.visit.schedule` → 403+人话 | 1 |
| A3 | issue 无 source_node → 422 | 1 |
| A4 | 无 evidence → 422 | 1 |
| A5/A6 | 合流 / L2 暂停 | 3 |
| A7 | SelfPaw 无证据写经营 | 2 |
| A8 | ΠPaw memory.search 403 | 4 |
| A9 | explore cite 不可 execute | 1/2 |
| A10 | Builder invariant 失败不能 release（挂 S-10/S-11） | 2 |
| A11 | 跨租户 403 | 2 |
| A12 | 同 Thread 改 profile 409 | 1 |
| I-02/I-05/I-10 | 缺维 / scene 写 / 无岗位 | 1 |
| I-09 | 未审批不进 compiled | 2 |
| I-03/I-04/I-06/I-07/I-11 | stale / 接地 / Worker 门禁 / 无出站 / 合流 | 3 |
| I-08 | pipaw 403 Lethe | 4 |
| I-12 | 三处同源 | 1 契约 + 2 drift 端点 |
| D-01…D-08 | Console Demo 铁律 | 2/4 |

---

## 11. 非目标

- 一份 plan 实现全部模块。
- 把离线 Console Demo 在 Spec-1 改成真连。
- 实现 NocoBase 插件、K8s、跨租户 A2A、Utopia 写。
- 改一线视觉语言（沿用现有 `workstudio.css` / `console.css`）。
- git commit（除非用户明确要求）。

---

## 附录 A · `configs/protocol/registry.json` 设计原文

实现时原样落盘（无 JSON 注释）。`policy_order` 必须逐字等于 `PolicyChain.ORDER`。`front_forbidden_nouns` 含 `workflow_id`、`CubeQL`。M2–M6：`decision=own` 且 `replaceable=false`。M23 `port=null`。

```json
{
  "version": "1.0.0",
  "envelope": ["tenant_id", "actor_id", "profile", "track", "correlation_id", "idempotency_key", "source_node_id", "position_id"],
  "policy_order": ["inject", "tenant", "registry", "rbac", "approval", "gates", "scope", "execute", "audit"],
  "front_forbidden_nouns": ["cubejs", "graphiti", "neo4j", "langgraph", "temporal", "lethe", "workflow_id", "CubeQL"],
  "modules": [
    {"id":"M1","name":"WorkStudio","layer":"use","decision":"own-shell","replaceable":false,"protocol_id":"hub.scene.pack.open","port":null,"hub_methods":["hub.scene.pack.open","hub.scene.insight.drill","hub.scene.task.issue","hub.policy.explain"],"verbs":["open","render"],"errors":["TENANT_MISMATCH","SCOPE_DENIED"],"forbidden":["零件SDK","聊天当状态"]},
    {"id":"M2","name":"责任图","layer":"K-L0","decision":"own","replaceable":false,"protocol_id":"hub.ops.graph","port":null,"hub_methods":["hub.scene.pack.open","hub.ops.graph.get","hub.ops.graph.validate","hub.ops.graph.publish"],"verbs":["slice","validate","publish"],"errors":["WM_INCOMPLETE","SCOPE_DENIED"],"forbidden":["Graphiti当L0"]},
    {"id":"M3","name":"世界模型Store","layer":"K-L0","decision":"own","replaceable":false,"protocol_id":"hub.wm","port":null,"hub_methods":["hub.wm.get","hub.wm.patch","hub.ops.wm.get"],"verbs":["get","patch"],"errors":["INVARIANT_FAILED"],"forbidden":["live改compiled"]},
    {"id":"M4","name":"Law Pack","layer":"K-L0","decision":"own","replaceable":false,"protocol_id":"hub.law.compile","port":"LawPort","hub_methods":["hub.law.compile","hub.ops.law.diff"],"verbs":["compile","diff"],"errors":["INVARIANT_FAILED"],"forbidden":["会话内改生产知识"]},
    {"id":"M5","name":"Insight→Task","layer":"use","decision":"own","replaceable":false,"protocol_id":"hub.scene.task.issue","port":null,"hub_methods":["hub.scene.insight.drill","hub.scene.task.issue","hub.scene.task.return"],"verbs":["drill","issue","return"],"errors":["TASK_SOURCE_REQUIRED","UNGROUNDED_INSIGHT","WM_INCOMPLETE"],"forbidden":["签发即启工作流"]},
    {"id":"M6","name":"Capability Hub","layer":"control","decision":"own","replaceable":false,"protocol_id":"hub.policy","port":null,"hub_methods":["hub.policy.explain","hub.scene.invoke_cs","hub.instance.invoke_cs"],"verbs":["enforce","explain"],"errors":["PROFILE_FORBIDS_SIDE_EFFECT","THREAD_PROFILE_IMMUTABLE"],"forbidden":["第二套控制面"]},
    {"id":"M7","name":"Registry","layer":"control","decision":"own-contract","replaceable":false,"protocol_id":"cs.*","port":null,"hub_methods":["hub.ops.registry.list","hub.ops.registry.patch"],"verbs":["list","patch"],"errors":["OPERATION_NOT_FOUND"],"forbidden":["双份schema"]},
    {"id":"M8","name":"IAM","layer":"govern","decision":"own-contract","replaceable":false,"protocol_id":"hub.ops.iam","port":"IamPort","hub_methods":["hub.ops.iam.bindings"],"verbs":["bind","resolve"],"errors":["TRACK_ESCALATION_REQUIRED","SCOPE_DENIED"],"forbidden":["IdP角色当承诺权"]},
    {"id":"M9","name":"Skill","layer":"weave","decision":"own","replaceable":false,"protocol_id":"hub.skill","port":"SkillPort","hub_methods":["hub.skill.transition","hub.ops.skill.list"],"verbs":["transition"],"errors":["SKILL_NOT_EXECUTABLE_IN_PROFILE"],"forbidden":["explore执行"]},
    {"id":"M10","name":"Artifact","layer":"runtime","decision":"own","replaceable":true,"protocol_id":"hub.ops.artifact","port":"ArtifactPort","hub_methods":["hub.ops.artifact.list"],"verbs":["put","get"],"errors":["INVARIANT_FAILED"],"forbidden":["file驱动pack.open"]},
    {"id":"M11","name":"Audit","layer":"govern","decision":"own","replaceable":false,"protocol_id":"hub.ops.audit","port":null,"hub_methods":["hub.ops.audit.search","hub.ops.audit.export"],"verbs":["append","search","export"],"errors":["SCOPE_DENIED"],"forbidden":["Cube当审计"]},
    {"id":"M12","name":"Evolution","layer":"evolve","decision":"own","replaceable":false,"protocol_id":"hub.ops.changeset","port":"EvolutionPort","hub_methods":["hub.ops.changeset.list","hub.ops.changeset.submit","hub.ops.changeset.decide"],"verbs":["draft","submit","decide"],"errors":["INVARIANT_FAILED"],"forbidden":["auto_apply"]},
    {"id":"M13","name":"MCP Gateway","layer":"protocol","decision":"own-shell","replaceable":false,"protocol_id":"hub.mcp.tools","port":"McpPort","hub_methods":["hub.mcp.tools.list","hub.mcp.tools.call","hub.ops.mcp.preview"],"verbs":["list","call"],"errors":["PROFILE_FORBIDS_SIDE_EFFECT"],"forbidden":["list跳过call判定"]},
    {"id":"M14","name":"Connector","layer":"system","decision":"own-contract","replaceable":true,"protocol_id":"connector.invoke","port":"ConnectorPort","hub_methods":["hub.ops.connector.list","hub.ops.connector.rotate"],"verbs":["invoke","rotate"],"errors":["GATE_BLOCKED"],"forbidden":["密钥出进程"]},
    {"id":"M15","name":"口径Cube+OSI","layer":"K-L1","decision":"integrate","replaceable":true,"protocol_id":"cs.metric.query","port":"CubePort","hub_methods":["hub.metric.query","hub.ops.caliber.status"],"verbs":["query"],"errors":["CALIBER_MISSING"],"forbidden":["签发任务"],"part":"Cube Core","fixture":"FixtureCube"},
    {"id":"M16","name":"时态知识","layer":"K-L2","decision":"integrate","replaceable":true,"protocol_id":"hub.kg.search","port":"KgPort","hub_methods":["hub.kg.search","hub.ops.kg.search","hub.ops.kg.ingest_status"],"verbs":["search","ingest"],"errors":["UNGROUNDED_INSIGHT"],"forbidden":["cs写"],"part":"Graphiti","fixture":"FixtureKg"},
    {"id":"M17","name":"Lethe","layer":"K-L3","decision":"integrate","replaceable":true,"protocol_id":"hub.memory.self","port":"MemoryPort","hub_methods":["hub.memory.self.search","hub.ops.memory.receipt"],"verbs":["add","search","forget"],"errors":["MEMORY_TRACK_FORBIDDEN"],"forbidden":["与责任图同库"],"part":"Lethe","fixture":"FixtureMemory"},
    {"id":"M18","name":"外环Temporal","layer":"runtime","decision":"integrate","replaceable":true,"protocol_id":"hub.exec.open","port":"OuterLoopPort","hub_methods":["hub.exec.open","hub.instance.cycle_step","hub.ops.runtime.task","hub.ops.runtime.retry"],"verbs":["open","signal"],"errors":["TASK_NOT_ISSUED"],"forbidden":["Celery当寿命"],"part":"Temporal","fixture":"InMemoryOuterLoop"},
    {"id":"M19","name":"内环LangGraph","layer":"weave","decision":"integrate","replaceable":true,"protocol_id":"innerloop.turn","port":"InnerLoopPort","hub_methods":["hub.instance.cycle_step"],"verbs":["turn","interrupt"],"errors":["SCOPE_DENIED"],"forbidden":["出站CRM"],"part":"LangGraph","fixture":"FixtureInnerLoop"},
    {"id":"M20","name":"JSON Schema","layer":"protocol","decision":"own-contract","replaceable":false,"protocol_id":"hub.ops.schema.drift","port":null,"hub_methods":["hub.ops.schema.drift"],"verbs":["drift"],"errors":["INVARIANT_FAILED"],"forbidden":["双份模型"]},
    {"id":"M21","name":"转派A2A","layer":"weave","decision":"own-contract","replaceable":false,"protocol_id":"hub.task.transfer","port":null,"hub_methods":["hub.task.transfer"],"verbs":["transfer"],"errors":["TENANT_MISMATCH"],"forbidden":["P0跨租户"]},
    {"id":"M22","name":"Utopia","layer":"knowledge","decision":"optional","replaceable":true,"protocol_id":"review.export","port":"ReviewPort","hub_methods":[],"verbs":["export"],"errors":[],"forbidden":["生产写"],"fixture":null},
    {"id":"M23","name":"主数据SoR","layer":"system","decision":"connect","replaceable":true,"protocol_id":"sor.object_ref","port":null,"hub_methods":[],"verbs":["ref"],"errors":[],"forbidden":["复制主档"]},
    {"id":"M24","name":"LLM Broker","layer":"weave","decision":"connect","replaceable":true,"protocol_id":"hub.ops.model.route","port":"BrokerPort","hub_methods":["hub.ops.model.route"],"verbs":["complete","route"],"errors":["SCOPE_DENIED"],"forbidden":["聊天当状态"],"part":"Provider SDK","fixture":"FixtureBroker"}
  ]
}
```

`validate_registry()` 必须返回 `[]`。`test_protocol_registry` 全绿是接口对齐的机器门禁。

---

## 附录 B · `configs/protocol/KERNEL.yaml` 设计原文

```yaml
version: "1.0.0"
planes:
  use: { entry: hub.scene.*, consumers: [M1, M5], demo: demo/index.html }
  control: { entry: hub.* PolicyChain, consumers: [M6] }
  ops: { entry: hub.ops.*, consumers: [Console], write: changeset }
protocols:
  north: hub.scene + SSE
  south: ConnectorPort.invoke
  east: OuterLoopPort
  west: InnerLoopPort
  knowledge: CubePort | KgPort | MemoryPort
  horizontal: hub.task.transfer  # P0
  identity: OIDC -> IamPort
  evolution: EvolutionPort auto_apply=false
policy_order: [inject, tenant, registry, rbac, approval, gates, scope, execute, audit]
invariants: [I-01, I-02, I-03, I-04, I-05, I-06, I-07, I-08, I-09, I-10, I-11, I-12]
```

---

*争议时：德压过术。本文变更走 ADR；字段变更走 ARCHITECTURE_SPEC / ChangeSet。实现从 Spec-1 开始，不从本文直接铺 30 个模块的代码。*
