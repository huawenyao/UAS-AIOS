# AIOS 集群管理后台：集成交互设计与产品化 demo

| 项 | 值 |
|----|-----|
| 状态 | 已确认（设计冻结），待实现 |
| 日期 | 2026-09-11 |
| 交付目录 | `projects/aios-workstudio/`（AIOS 默认开发目录） |
| 服从 | [`UAS_AIOS_ARCHITECTURE_SPEC.md`](../../../strategic/design/UAS_AIOS_ARCHITECTURE_SPEC.md) · [`UAS_AIOS_CLUSTER_PRODUCTIZATION.md`](../../../strategic/design/UAS_AIOS_CLUSTER_PRODUCTIZATION.md) · [`uas-aios-cluster.html`](../../../strategic/design/uas-aios-cluster.html) · [`UAS AIOS架构规划（自研OR集成）.md`](../../../strategic/design/UAS%20AIOS架构规划（自研OR集成）.md) |

**一句话**：让 `projects/aios-workstudio` 的模块脚手架**真正跑起来**——补齐从未存在的运行时契约骨架，把 Console 从静态 mock 改成**真调 `hub.ops.*`** 的管理后台，并让「模块间集成交互设计」以机器可读契约落地。

---

## 0. 背景：探索结论

### 0.1 已存在（非空仓）

| 层 | 现状 | 证据 |
|----|------|------|
| 模块脚手架 | `modules/catalog.json` + 30 个 `SPEC.md`（use/control/ops/console 四层），`gen_specs.py` 生成 | `projects/aios-workstudio/modules/` |
| 脚手架测试 | 6 项全绿 | `python -m unittest discover -s projects/aios-workstudio/tests` |
| 内核代码 | `uas_hub.Hub` / `PolicyChain` / `Registry` / `GraphStore` / `WmStore` / `InsightTaskService` / `OuterLoop` + 15 个 adapter | `services/hub-api/uas_hub/` |
| 门面 | `CapabilityHub` facade（`__getattr__` 委托 `hub.core`）+ http_app | `CapabilityHub/capability_hub/` |
| Console demo | 静态 HTML，8 页 IA，数据硬编码在 `data.js` | `Console/demo/` |
| ops 客户端契约 | **30 个端点**（18 GET + 12 POST）已声明 | `packages/hub-client/src/ops.ts` |
| 查询器 | `load_registry` / `validate_registry` / `integrated_modules` | `uas_hub/protocol_catalog.py` |
| 协议 schema | 24 模块契约定义 | `schemas/protocol/module_protocol.schema.json` |

### 0.2 缺口（**git 中从未存在**，非本次误删）

| 缺失 | 依赖方 | 后果 |
|------|--------|------|
| `configs/accountability_graph.sample.json` | `hub.py:55`、`CapabilityHub/tests/test_t1_accept.py`、`test_http.py` | `Hub.from_repo()` 抛 `FileNotFoundError`；CapabilityHub 测试**无法收集** |
| `configs/protocol/registry.json` | `protocol_catalog.py` | 集成契约缺失 |
| `configs/protocol/KERNEL.yaml` | `CLAUDE.md` 索引 | 文档指向空 |
| `configs/metrics/osi/*.yml` | `FixtureCube._load_osi` | 口径无定义 |
| `cs.visit.list/schedule`、`cs.metric.query` | 测试、MCP 预览 | 注册表缺项 |
| `hub.ops.*` 读端点（`profile/matrix` 除外） | `ops.ts` | Console 无法真连 |
| 夹具 list 能力 | ops 只读视图 | `FixtureEvolution/Artifact/Iam/Skill/Connector/Cube` 无 list |

### 0.3 工作区删除处置（已确认）

工作区有 112 个未提交删除，**用户确认系有意清理，但 `configs/` 为误删**。据此仅恢复必需项：

```
git restore configs/ \
            "projects/aios-workstudio/demo/" \
            "projects/aios-workstudio/T1-WorkStudio详细设计.md"
```

`asui-cli/`（74）、`docs/`（5）、`database/` 等其余删除**保持不动**。

---

## 1. 目标与验收

| 验收 | 判据 |
|------|------|
| V1 | `Hub.from_repo()` 无异常；`CapabilityHub` 3 个测试文件全绿 |
| V2 | `protocol_catalog.validate_registry()` 返回空错列表 |
| V3 | Console 8 页全部经 `fetch` 真调 `/hub/v1/ops/*`，无硬编码数据 |
| V4 | I-01…I-12 中可离线验证的条目有契约测试 |
| V5 | 一线角色（`frontline`）打开 Console 得锁页 |

---

## 2. 架构与模块边界

```
Console/demo (index.html + console.css + app.js + ops-client)
   │  只调 /hub/v1/ops/*  ｜  头：X-Tenant-Id, X-Actor-Id, X-Ops-Role
   ▼
CapabilityHub/capability_hub/http_app.py   ← 薄路由，入口强制 profile=builder
   │
   ▼
capability_hub/ops/                        ← 本次新增
   ├── __init__.py    OpsService 组合根（持有 hub.core 引用）
   ├── overview.py    总览：三平面 SLO 聚合
   ├── integrate.py   集成：读 configs/protocol/registry.json
   ├── control.py     控制：剖面矩阵 · explain · 判定序试运行
   ├── ontology.py    本体：责任图 · WM 三寿命 · Law Pack
   ├── mesh.py        能力：Registry cs.* · MCP tools · Connector
   ├── governance.py  治理：IAM · Audit · Skill · Artifact
   ├── runtime.py     运行：任务寿命 · 口径 · 时态 · 记忆 · 模型路由
   └── publish.py     发布：ChangeSet 草案/审批
   │  仅读夹具状态 + 仅经既有门禁写
   ▼
hub.core (uas_hub.Hub)  graphs · wm · audit · registry · iam · artifact
                        · evolution · skill · connector · kg · memory · cube · insights · broker
```

### 2.1 硬约束（写进测试断言）

- **自动断言范围 = `ops/**`**（§8）：**禁止**出现 `invoke_cs` 调用、**摄入动作路由 `/hub/v1/kg/ingest`**、零件名（`cubejs` / `graphiti` / `neo4j` / `langgraph` / `temporal` / `lethe`）、`workflow_id`、`CubeQL`、`CollectionBlockModel`、`plugin-ai`、`mcp-server`
  - 禁词断言必须锚定**完整路径** `/hub/v1/kg/ingest`，而非子串 `kg/ingest`——否则会误伤必需端点 `GET kg/ingest_status`
  - `ops.ts` 不在该断言范围内：其首行注释已含 `invoke_cs` 一词；对 `ops.ts` 的约束只针对**端点路径字符串**（不得出现 `/invoke_cs`、`/kg/ingest`）
- `ops/` **不**新建进程、**不**复用 SoR 密钥、**不**改 `hub.core` 既有行为
- 一线角色打开 Console → 锁页（`看不到 /console`）

### 2.2 夹具只读缺口处理

`FixtureEvolution` / `Artifact` / `Iam` / `Skill` / `Connector` / `Cube` 目前只有写/查询方法，**无 list**。为 ops 只读视图，给每个夹具**追加只读方法**（`list()` / `status()`），签名与既有方法互不干扰，行为纯增量。

---

## 3. 集成交互设计的机器可读载体

### 3.1 `configs/protocol/registry.json`（新建）

契约已由 `schemas/protocol/module_protocol.schema.json` 定义，加载器 `protocol_catalog.py` 已就绪。

```jsonc
{
  "version": "1.0.0",
  "envelope": ["tenant_id","actor_id","profile","track","correlation_id","idempotency_key","source_node_id","position_id"],
  "policy_order": ["inject","tenant","registry","rbac","approval","gates","scope","execute","audit"],
  "front_forbidden_nouns": ["cubejs","graphiti","neo4j","langgraph","temporal","lethe","workflow_id","CubeQL"],
  "modules": [ /* 24 条，M1..M24 */ ]
}
```

每模块一条，示例：

```jsonc
{
  "id": "M15", "name": "口径服务 Cube+OSI", "layer": "K-L1",
  "decision": "integrate", "replaceable": true,      // integrate ⇒ 必须声明 port
  "protocol_id": "cs.metric.query", "port": "CubePort",
  "hub_methods": ["hub.metric.query", "hub.ops.caliber.status"],
  "verbs": ["query"], "errors": ["CALIBER_MISSING"],
  "forbidden": ["签发任务", "当责任图"], "part": "Cube Core", "fixture": "FixtureCube"
}
```

**这就是「模块间只通过协议说话」的权威声明**：`decision=integrate` ⇒ 必须声明 `port` 且 `replaceable=true`（`validate_registry` 已强制校验）。`policy_order` 必须逐字等于 `PolicyChain.ORDER`。

> ⚠️ 上方代码块用 `//` 注释仅为文档可读。**落盘文件必须是无注释的纯 JSON**——`protocol_catalog.load_registry()` 走 `json.loads`，带注释会直接解析失败。

### 3.2 `configs/protocol/KERNEL.yaml`（新建）

声明三平面、八协议（北/南/东/西/知识/水平/身份/演化）、不变量摘要，作为 `CLAUDE.md` 索引的真实落点。

---

## 4. ops 端点契约

**30 个端点已在 `packages/hub-client/src/ops.ts` 声明**（18 GET + 12 POST），**本次全部实现，不改命名**。另有 **3 个端点本次新增**（同时补进 `ops.ts`），共 **33**。

### 4.1 已有（`ops.ts` 已声明，本次实现/接线）

| Console 页 | 端点（← 数据源） |
|---|---|
| 总览 | `GET tenant/get` ← `tenant_catalog.sample.json` ｜ `GET health/summary` ← 三平面聚合 |
| 控制 B1 | `GET profile/matrix` ✅已有 ｜ `POST policy/explain` ← `core.explain` |
| 本体 B2 | `POST graph/get`、`POST graph/validate` ← `graphs` + `node_incomplete` ｜ `POST wm/get` ← `wm` ｜ `POST law/diff` ← `FixtureLaw` |
| 能力 B3 | `GET registry/list` ← `registry` ｜ `POST registry/patch` ← ★写，见 §5 ｜ `GET mcp/preview?profile=` ← `FixtureMcp.list_tools` ｜ `GET connector/list` ← `FixtureConnector` ｜ `POST connector/rotate` ← ★写，见 §5 ｜ `GET schema/drift` ← `protocol_catalog.validate_registry` |
| 治理 B4 | `GET iam/bindings` ｜ `GET audit/search`、`GET audit/export` ← `core.audit` ｜ `GET skill/list` ← `FixtureSkill`+`CATALOG` ｜ `GET artifact/list` ← `FixtureArtifact` |
| 运行 B5 | `GET runtime/task` ← `insights.tasks` ｜ `POST runtime/retry` ← ★写，见 §5 ｜ `GET caliber/status` ← `FixtureCube` ｜ `GET kg/ingest_status`、`POST kg/search` ← `FixtureKg` ｜ `GET memory/receipt` ← `FixtureMemory` ｜ `GET model/route` ← `FixtureBroker` |
| 发布 | `GET changeset/list`、`POST changeset/submit`、`POST changeset/decide` ← `FixtureEvolution` ｜ `POST graph/publish` ← ★写，见 §5 |

### 4.2 本次新增（3 个，需同步补进 `ops.ts`）

| 端点 | 用途 | 数据源 |
|------|------|--------|
| `GET ops/protocol/registry` | 集成页：24 模块协议契约 | `configs/protocol/registry.json` |
| `GET ops/protocol/contracts` | 集成页：I-01…I-12 集成验收矩阵 + 八协议信封 | `protocol_catalog` + §3 |
| `POST ops/policy/simulate` | 控制页：「若现在点写会怎样」判定序干跑（**不执行**） | `PolicyChain` 逐步 trace，不调 `execute_fn` |

### 4.3 profile 强制（**新增行为，非沿用**）

`http_app.py` 现有 `_envelope` 是 `profile = header_profile or profile`——**客户端 `x-profile` 头优先级更高**。这**不是**可直接沿用的模式。

V5（一线锁页）要求的是**入口强制**：ops 路由必须忽略 `x-profile`，改由 `X-Ops-Role` 映射固定 `profile=builder`，并对 `frontline` 角色直接返回锁页/403。这是本次**新增的门禁**，需新写，不能假设已存在。

**遗留项**：是否同时把 `_envelope` 既有行为改为服务端强制（影响 scene/exec 路由），列为开放问题，默认**不动**（避免改 `hub.core` 既有行为）。

---

## 5. 写动作与门禁（读 + 安全写）

所有写**只走两条路**：既有治理门禁，或 ChangeSet 草案。**`auto_apply` 恒为 `false`**。

| 写动作 | 路径 | 门禁 |
|---|---|---|
| Skill 漏斗 cite/install/enable | 既有 `/hub/v1/skill/*` | `assert_transition_allowed(profile, state)` |
| WM draft 补丁 | 既有 `/hub/v1/wm/patch` | `WmStore.patch`（live/compiled 拒 runtime） |
| IAM 岗位绑定 | 既有 `/hub/v1/iam/*` | 强制 `permissionChangeSet` |
| 责任图 / Registry 发布 | `POST ops/graph/publish`、`ops/registry/patch`（`registry/patch` 已在 `ops.ts`） | → `evolution.draft()` 出草案，**不直接生效** |
| 连接器槽位轮换 | `POST ops/connector/rotate`（已在 `ops.ts`） | 仅改槽位**元数据**（sandbox/prod 槽、轮换时间）；**不落密钥明文**，`FixtureConnector._reject_secrets` 兜底 |
| ChangeSet 提交/审批 | `POST ops/changeset/{submit,decide}`（已在 `ops.ts`） | `evolution.apply(approved)`，`auto_apply=false` |
| 任务续跑 | `POST ops/runtime/retry`（已在 `ops.ts`） | `outer_loop.signal`（非 `invoke_cs`） |

---

## 6. 运行时数据骨架（"模块初始化"的实质）

| 新建 / 扩展 | 内容 | 解锁 |
|---|---|---|
| 🆕 `configs/protocol/registry.json` | 24 模块协议契约 | `protocol_catalog`、集成页 |
| 🆕 `configs/protocol/KERNEL.yaml` | 内核声明 | 文档索引一致性 |
| 🆕 `configs/accountability_graph.sample.json` | 衡川 LTC，含 `an-stage-visit`（`ought=14/is=28`、`pos-cm`、`cs_write=["cs.visit.schedule"]`、五维齐全） | `hub.py:55`、2 个测试文件 |
| 🆕 `configs/metrics/osi/kpi-visit-dwell.yml` | 口径定义 | `FixtureCube._load_osi` |
| ✏️ `configs/capability_registry.json` | 追加 `cs.visit.list`、`cs.visit.schedule`、`cs.metric.query` | 测试、MCP 预览 |
| 🆕 `CapabilityHub/run.py` 增加静态托管 | Console 同源，免 CORS | V3 |

---

## 7. 错误处理与降级

- 统一错误体 `{error:{code,message,explain_ref,retryable}}`，UI **必须**渲染 `message`
- **零件缺失不 500**：返回 `{"available": false, "reason": "...", "explain": {...}}` + 人话（对应 I-01「断零件时有人话降级」）
- 未知 ops 路径 → 404 而非 500；`profile` 非法 → `SCOPE_DENIED`

---

## 8. 测试与验收

| 测试 | 覆盖 |
|---|---|
| 🆕 `CapabilityHub/ops/tests/test_ops_endpoints.py` | 30 个已有 + 3 个新增 ops 端点契约（状态码 + 关键字段） |
| 🆕 `CapabilityHub/tests/test_protocol_registry.py` | §3 契约：24 模块、`integrate⇒port+replaceable`、`policy_order` 对齐、信封齐全 |
| ✏️ `projects/aios-workstudio/tests/test_scaffold.py` | 改断言：Console 从"硬编码数据"改为"调 `/hub/v1/ops/*`"；新增 `ops/**` 禁词断言 |
| ✏️ `CapabilityHub/tests/test_http.py` | 补 ops 只读端点断言（不改既有用例） |
| ✅ 既有 `CapabilityHub/tests/test_t1_accept.py`（10 例） | **必须转绿**——模块初始化是否完成的总开关 |

---

## 9. 交付物与不做

### 9.1 交付物

```
configs/protocol/registry.json              ← 24 模块集成交互契约
configs/protocol/KERNEL.yaml                ← 内核声明
configs/accountability_graph.sample.json    ← 衡川 LTC 责任图
configs/metrics/osi/kpi-visit-dwell.yml     ← 口径定义
configs/capability_registry.json            ← 扩展 cs.visit.* / cs.metric.query
projects/aios-workstudio/CapabilityHub/
  capability_hub/ops/{__init__,overview,integrate,control,ontology,mesh,governance,runtime,publish}.py
  capability_hub/http_app.py                ← 补 ops 路由
  run.py                                    ← 静态托管 Console
  tests/test_protocol_registry.py / ops/tests/test_ops_endpoints.py
services/hub-api/uas_hub/adapters/*.py      ← 夹具只读方法（纯增量）
projects/aios-workstudio/Console/
  demo/{index.html,console.css,app.js}      ← 改为真调
  src/hubOps.ts / packages/hub-client/src/ops.ts  ← 补写方法 + 3 个新端点
projects/aios-workstudio/tests/test_scaffold.py  ← 改断言
```

### 9.2 不做

- 不建第二套 API 进程（违反「Console 只调 `hub.ops.*`」）
- 不实现真实 Cube / Graphiti / Temporal / Lethe（仍用 Fixture）
- 不碰 `asui-cli/` 等有意删除的内容
- 不接真实 CRM / IdP
- 不改 `hub.core` 既有行为
- **不执行 git commit / 分支操作**（用户未要求）

---

## 10. 风险

| 风险 | 缓解 |
|------|------|
| 30 个 SPEC.md 与 `configs/protocol/registry.json` 的 24 模块 M1–M24 映射不一致（脚手架用 `m1`/`nb`/`pack`/`sse` 等短 id） | 两套 id 并存：`catalog.json` 服务 SPEC 目录（含 Console 壳），`registry.json` 服务内核协议（严格 M1–M24）。集成页同时展示并显式标注映射关系 |
| 夹具内存态重启即失，Console 刷新看不到管理动作结果 | demo 定位为**单会话演示**；`run.py` 启动时 seed 一次（责任图 + 一条 ChangeSet 草案 + 若干审计），保证首屏非空 |
| `FixtureCube._load_osi` 的 YAML 格式未知 | 实现首步先读 `adapters/cube.py` 确定格式，再写 `kpi-visit-dwell.yml`（TDD：先写失败测试） |
