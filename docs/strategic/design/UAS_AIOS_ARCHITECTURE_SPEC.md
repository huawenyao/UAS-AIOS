# UAS-AIOS 最终架构详细方案

| 项 | 值 |
|----|-----|
| 文档地位 | **工程实施权威**。模块边界、数据契约、接口、部署、验收以此为准。 |
| 版本 | v1.0 |
| 日期 | 2026-09-09 |
| 状态 | 冻结草案（Frozen Draft）。改内核须走 ChangeSet / ADR，禁止口头豁免。 |
| 受众 | 架构、Hub/Runtime 工程、实施、治理 |
| 服从 | [`AI_PRODUCT_CHARTER.md`](../../AI_PRODUCT_CHARTER.md) · ADR-EDH-001/002 |
| 业务语言 | [`ENTERPRISE_AGI_OPERATING_HUB.md`](./ENTERPRISE_AGI_OPERATING_HUB.md) |
| 选型论据 | [`SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md`](./SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md) |
| 模块总览 | [`UAS AIOS架构规划（自研OR集成）.md`](./UAS%20AIOS架构规划（自研OR集成）.md) |
| Hub 政策细节 | [`T1-CapabilityHub详细设计.md`](../../../projects/aios-workstudio/T1-CapabilityHub详细设计.md) |
| 作战台 UX | [`T1-场景态与执行态.md`](../../../projects/aios-workstudio/T1-场景态与执行态.md) |
| 集群产品化 | [`UAS_AIOS_CLUSTER_PRODUCTIZATION.md`](./UAS_AIOS_CLUSTER_PRODUCTIZATION.md) · [`uas-aios-cluster.html`](./uas-aios-cluster.html) |
| 模块设计与选型 | [`UAS_AIOS_MODULE_DESIGN.md`](./UAS_AIOS_MODULE_DESIGN.md) |
| 平台产品定义 | [`UAS_AIOS_PLATFORM_PRODUCT.md`](./UAS_AIOS_PLATFORM_PRODUCT.md) · [`uas-aios-platform.html`](./uas-aios-platform.html) |

**一句话**：自有经营本体与控制面；口径、时态知识、耐久执行、开放协议只作为可替换零件。前台只走 `hub.*`。场景禁写，Runtime 才写。

---

## 1. 问题、目标、非目标

### 1.1 要解决的断裂

传统 Dashboard 停在「人看完再切系统去办」。UAS-AIOS 要求：

1. **目标 ≡ 数据**：Goal / 组织 / KPI / 流程是同一棵责任图的投影，不是四套系统。  
2. **端 · 云 · 底**：作战台看见并决定；Hub 编译并执行；SoR 提供事实。  
3. **看见并办成**：指标下拆必须能签发任务；任务执行必须回写指标。

### 1.2 目标（本方案覆盖）

| ID | 目标 | 验收抓手 |
|----|------|----------|
| G-1 | 责任图为 L0 唯一经营写入 | schema + sample + invariant |
| G-2 | 四剖面同一 Hub，场景不能写生产 | `PROFILE_FORBIDS_SIDE_EFFECT` |
| G-3 | Agent 不直连系统 | 仅 MCP/`cs.*` 语义名 |
| G-4 | 任务必带 `source_node_id` | Task 契约拒绝空源 |
| G-5 | 内环一套、外环一套 | LangGraph + Temporal；禁第三套 |
| G-6 | 个人记忆 ≠ 经营承诺 | Lethe 分库；ΠPaw 403 |

### 1.3 非目标

- 不自研大模型、不自研 MDM/CRM、不自研 BPM 替代 Camunda 类 SoR。  
- 不采购 Palantir / Fabric IQ / Agentforce / Copilot Studio 当 OS。  
- 不用聊天历史、Lethe、Graphiti 充当经营状态。  
- 不在 P0 启用 A2A 跨租户（P1+）。Utopia 默认不进写路径。

---

## 2. 逻辑架构与部署拓扑

### 2.1 逻辑分层

```
┌─ 端  WorkStudio（自研 SPA）
│     场景态 scene          执行态 explore | builder | runtime
│                    只调 hub.*
├─ 云  Capability Hub（自研控制面）
│     Policy · Registry · IAM · WM Store · Artifact · Audit · Evolution
│     MCP Gateway 壳
│     Harness Broker ── InnerLoop SPI ── LangGraph 1.0
│                    ── Temporal Worker ── RuntimeCycleWorkflow
│     零件：Cube · Graphiti · Lethe · LLM
├─ 底  System Connector → CRM / ERP / 仓 / 审批 / 日历
│     口径：仓 → Cube
│     时态：ETL/episode → Graphiti（Neo4j|FalkorDB）
└─ 身份源 企业 IdP（OIDC/SAML）；授权模型仍在 Hub
```

UAS 形式化映射：`I` 作战台与 Insight→Task；`K` L0 自研 + L1–L3 零件；`R` Broker+Temporal；`A` Skill+LangGraph；`S` cs.*+Connector；`G` IAM+G 层+审计；`E` ChangeSet；`Π` hub.*+MCP+OSI+A2A。

### 2.2 四剖面（同一进程，四套政策）

| `profile` | 调用方 | Skill | cs 读 | cs 写 | 网络检索 | 默认 track |
|-----------|--------|-------|-------|-------|----------|------------|
| `scene` | 作战台 | 已装 Pack 只读 | 聚合/脱敏 | **拒绝** | 关 | scene |
| `explore` | 研究 | 发现+引用 | mock/脱敏 | **拒绝** | 租户开关 | selfpaw |
| `builder` | 构建 | 蓝图集合 | mock+校验 | dry-run 例外 | 默认关 | shared |
| `runtime` | 运行 | 启用∩授权 | 真读+scope | L1/L2/L3+G* | 默认关 | 实例声明 |

中途改 `profile` **必须新开 Thread**（`THREAD_PROFILE_IMMUTABLE`）。

### 2.3 判定顺序（不可颠倒）

```
InvokeRequest
  0. 注入 profile + track + actor + tenant
  1. tenant_id 匹配
  2. Registry：operation 存在且租户启用
  3. RBAC：role × operation
  4. approval_level → L1 自动 / L2 确认 / L3 双控
  5. gates G* 自检
  6. scope_rules 注入连接器（禁止模型拼 SQL）
  7. 执行 Connector / Cube / Graphiti / InnerLoop
  8. 审计 + 可选 live WM patch + 可选 ChangeSet 信号
```

与 [`enterprise-rbac-abac-spec.md`](../../../harness/knowledge/technical/enterprise-rbac-abac-spec.md) 对齐，并在最前增加剖面注入。

### 2.4 建议进程拆分（P0 可合并，边界不变）

| 进程 | 职责 | 状态 |
|------|------|------|
| `workstudio-web` | 静态/SSR 作战台 | 无密钥 |
| `hub-api` | 全部 `hub.*` | 无 SoR 明文密钥（读 KMS 引用） |
| `mcp-gateway` | MCP stdio/HTTP；可与 hub-api 同进程 | 同门禁 |
| `temporal-worker` | Activity：InnerLoop / InvokeCs / RefreshKpi | 调 hub 内部门禁，不旁路 |
| `cube-api` | 口径服务 | 只读仓账号 |
| `graphiti-worker` | episode 摄入与检索 | 独立图库账号 |
| `lethe-api` | SelfPaw 记忆 | **独立数据库** |
| `connector-*` | SoR 适配 | 密钥只在此 |

P0 允许 `hub-api + mcp-gateway + worker` 同仓不同进程；禁止把 Lethe 与责任图放同一 schema。

---

## 3. 数据契约

权威 JSON Schema 已存在则以其为准；本方案给出运行时对象与缺口 schema（实施时补文件）。

### 3.1 责任图（已有）

- Schema：`schemas/accountability_graph.schema.json`  
- 样例：`configs/accountability_graph.sample.json`（衡川 LTC）

**不变量**

- 节点必填 `goal, org, kpi, process, wm`；缺维不得签发。  
- 四种边 `org_cascade | kpi_split | stage_split | object_drill` 是同一棵树的投影。  
- `kpi.caliber` 引用口径 ID，禁止节点内口头公式副本长期漂移（P0 样例可暂存可读公式，P1 必须 `caliber_id`）。  
- `kpi.is` 运行时由 `cs.metric.query` 水合；库内快照仅作缓存，带 `as_of`。  
- `process.cs_write` 为场景可展示、Runtime 可调用的写操作白名单。

### 3.2 企业世界模型（已有）

- Schema：`schemas/enterprise_world_model.schema.json`  
- 寿命：`draft | compiled | live`，同一 `world_model_id`。  
- Runtime **不得** PATCH `compiled`。改法则 → ChangeSet → 新 Release → 新 compiled。

### 3.3 Insight（缺口 schema，P0 补 `schemas/insight.schema.json`）

```json
{
  "insight_id": "ins-an-stage-visit-20260822",
  "tenant_id": "t-hengchuan",
  "source_node_id": "an-stage-visit",
  "profile": "explore",
  "hypothesis": "拜访停留 28 天且决策链仅 BD，流失风险上升",
  "suggested_cs": ["cs.visit.schedule"],
  "evidence_refs": [
    { "kind": "kg", "id": "ep-visit-20260715" },
    { "kind": "metric", "id": "kpi-visit-dwell", "as_of": "2026-08-22T00:00:00Z" }
  ],
  "grounded": true,
  "wm_completeness": ["space", "time", "subject", "object", "feedback"]
}
```

`grounded=false` 或 `wm_completeness` 缺项 → 不得进入 `task.issue`。

### 3.4 Task（缺口 schema，P0 补 `schemas/operating_task.schema.json`）

```json
{
  "task_id": "tsk-20260822-001",
  "tenant_id": "t-hengchuan",
  "source_node_id": "an-stage-visit",
  "insight_id": "ins-an-stage-visit-20260822",
  "assignee": { "owner_id": "zhangsan", "position_id": "pos-bd" },
  "due": "2026-08-23",
  "cs_write": ["cs.visit.schedule"],
  "evidence_refs": ["ep-visit-20260715"],
  "status": "issued",
  "track": "pipaw",
  "workflow_id": null
}
```

拒绝条件：缺 `source_node_id`；`cs_write` ⊄ 节点 `process.cs_write`；`cs_write` 含写操作但签发剖面不是经 `task.issue` 这种「只建单不执行」路径。

状态机：`issued → opened → running → awaiting_approval → succeeded | failed | cancelled | returned`。

### 3.5 ChangeSet（与治理规格对齐）

最小字段：`changeset_id, tenant_id, actor, target (law_pack|release|permission), diff, evidence_refs, impact_scope, regression_cases, rollback_ref, auto_apply=false, status=draft`。

禁止 `auto_apply=true` 写生产法则。回写走既有 `evolveApply` / 治理台。

### 3.6 审计记录

每次 `cs.*` / `hub.instance.invoke_cs` / 升级 / 权限变更：

```
audit_id, tenant_id, actor_id, track, profile, operation,
approval_level, gates_passed[], scope, request_hash, result_code,
source_node_id?, task_id?, workflow_id?, ts
```

对齐 [`enterprise-audit-chain-spec.md`](../../../harness/knowledge/technical/enterprise-audit-chain-spec.md)。指挥舱 KPI 不是审计系统。

### 3.7 三类对象禁止互冒

| 对象 | 例子 | 不是 |
|------|------|------|
| 产物 | ThemePack、报告 PDF | 状态源 |
| 主数据 | CRM 客户行 | 世界模型 |
| 世界模型 | 五维 + laws + ought/is | 知识图谱 / 口径立方 |

Lethe 行、Graphiti 节点、责任图 `node_id` 三套 ID 永不混用。

---

## 4. `hub.*` 接口规格

传输：HTTPS JSON（P0）。认证：OIDC Bearer + `X-Tenant-Id`。所有写接口幂等键 `Idempotency-Key`。

错误体统一：

```json
{
  "error": {
    "code": "PROFILE_FORBIDS_SIDE_EFFECT",
    "message": "现在是作战台，不能改 CRM。请签发任务后进入运行。",
    "explain_ref": "hub.policy.explain",
    "retryable": false
  }
}
```

UI 必须展示 `message`，禁止只展示 HTTP 500。

### 4.1 场景态

#### `hub.scene.pack.open`

```
POST /hub/v1/scene/pack/open
profile=scene（服务端强制，忽略客户端伪造）

req: { "position_id": "pos-cm", "period": { "grain": "month", "from": "2026-08-01", "to": "2026-08-31" } }
res: { "graph_id", "nodes": [ /* 水合后的节点：kpi.is, kpi.status */ ], "insights_open_count", "tasks_open_count" }
```

水合：对每个节点调用内部 `cs.metric.query`（或批量）。Cube 失败则 `kpi.is` 保持缓存并标 `stale=true`，不得假装实时。

#### `hub.scene.insight.drill`

```
POST /hub/v1/scene/insight/drill
可升级为 profile=explore 短 Thread（新 thread_id）

req: { "source_node_id": "an-stage-visit" }
res: Insight
```

内部：校验五维 → `hub.kg.search` → InnerLoop(`explore`) → 接地检查。

#### `hub.scene.task.issue`

```
POST /hub/v1/scene/task/issue
req: { "source_node_id", "insight_id", "assignee", "due", "cs_write", "evidence_refs" }
res: { "task_id", "status": "issued" }
```

本接口**不**启动 Temporal，**不**调写 cs。

#### `hub.scene.task.return`

驳回：写审计 + Evolution 信号（未接地率/驳回原因）。

### 4.2 执行态

#### `hub.exec.open`

```
POST /hub/v1/exec/open
req: { "task_id" }
res: { "task_id", "workflow_id", "status": "opened" }
```

副作用：`Temporal.Start(RuntimeCycleWorkflow)`。`task.workflow_id` 回写。

#### `hub.instance.cycle_step`

人工推进或信号：`approved | rejected | more_context`。映射 Temporal Signal。

#### `hub.instance.invoke_cs`

仅 `profile=runtime`。请求体即 `cs.{domain}.{action}` + input。必须重走 §2.3 全序。LangGraph 不得绕过本接口直打连接器。

### 4.3 知识与记忆

| 方法 | 剖面 | 下游 |
|------|------|------|
| `hub.wm.get` | 按寿命 | WM Store |
| `hub.wm.patch` | draft 可由 explore；live 仅 cycle_step | WM Store |
| `hub.kg.search` | scene 投影 / explore | Graphiti |
| `hub.kg.ingest_episode` | 受控 ETL 或 runtime 钩子 | Graphiti；**≠ cs 写** |
| `hub.metric.query` | 只读 | `cs.metric.query` → Cube |
| `hub.memory.self.add\|search\|forget` | 仅 `track=selfpaw` + `scope=self` | Lethe |

### 4.4 Skill / 治理

Skill 状态机：`discovered → previewed → cited → installed → enabled → executed`。Explore 最高 `cited`。

`hub.policy.explain`：输入失败码 + 当前 context，返回人话与「下一步」（签发任务 / 升级轨道 / 补五维）。

`hub.iam.*` / `hub.org.*`：复用企业 IAM；权限变更必须 `permissionChangeSet`。

升级：复用 [`intent-escalation-api.md`](../../../harness/knowledge/technical/intent-escalation-api.md)。经营写无证据不得 SelfPaw→ΠPaw。

### 4.5 错误码目录

| code | HTTP | 含义 |
|------|------|------|
| `WM_INCOMPLETE` | 422 | 五维或反馈通道缺失 |
| `PROFILE_FORBIDS_SIDE_EFFECT` | 403 | 当前剖面禁止写 |
| `INVARIANT_FAILED` | 422 | Builder PreRelease / harness 失败 |
| `GATE_BLOCKED` | 403 | G 层否决 |
| `TRACK_ESCALATION_REQUIRED` | 403 | 需证据升级 ΠPaw |
| `SKILL_NOT_EXECUTABLE_IN_PROFILE` | 403 | 发现≠执行 |
| `SCOPE_DENIED` | 403 | scope 不足 |
| `MEMORY_TRACK_FORBIDDEN` | 403 | ΠPaw 读个人记忆 |
| `THREAD_PROFILE_IMMUTABLE` | 409 | 试图在同一 Thread 改剖面 |
| `TASK_SOURCE_REQUIRED` | 422 | 无 `source_node_id` |
| `CALIBER_MISSING` | 422 | 无口径 ID / Cube 未注册 |
| `UNGROUNDED_INSIGHT` | 422 | 建议未接地 |

---

## 5. 集成零件：配置、场景、接口映射

### 5.1 Cube Core + OSI YAML（M15）

**决策**：口径服务层自持 Cube（Apache-2.0，原生 MCP）。定义用 OSI/MetricFlow 可互换 YAML，不绑 dbt Cloud，不以仓 Semantic View 为唯一真相。

**配置（建议）**

```
configs/metrics/osi/
  kpi-spend.yml
  kpi-visit-dwell.yml
configs/cube/cube.js          # 指向仓
```

**映射**

```
cs.metric.query
  in:  { "kpi_id", "grain", "from", "to", "dimensions": { "customer_id"? }, "scope" }
  out: { "value", "caliber_id", "as_of", "stale" }

Hub → Cube POST /v1/load  （或 Cube MCP）
模型只见 cs.metric.query
```

**场景**：作战台水合 `kpi.is`；指挥舱按 `org_cascade` 切片；Runtime 后刷新。

### 5.2 Graphiti + Neo4j/FalkorDB（M16）

**决策**：增量双时态 Context Graph。不是责任图，不签发任务，mutation 不是 `cs.*` 写。

**实体白名单（Pydantic，禁止模型自由起名）**：`Customer` `Opportunity` `Visit` `Approval` `Interaction`。必须能关联 `object_ref`（如 `UEC-10293`）。

```
hub.kg.search
  in:  { "object_ref"|"query", "valid_at"?, "as_of"? }
  out: { "facts": [{ "text", "valid_from", "valid_to", "source_ids" }] }
```

摄入：CRM webhook / ETL → `hub.kg.ingest_episode`（服务账号，非作战台用户）。

### 5.3 Lethe（M17）

独立 Postgres/专用库。仅 `hub.memory.self.*`。`forget` 产出签名回执写入审计，**不**改责任图。离职流程：forget 全量 + 回执归档。

### 5.4 Temporal（M18）

**Workflow 名**：`RuntimeCycleWorkflow`  
**Task Queue**：`uas-runtime`

**Args**

```json
{
  "tenant_id": "t-hengchuan",
  "instance_id": "inst-cm-001",
  "task_id": "tsk-20260822-001",
  "source_node_id": "an-stage-visit",
  "profile": "runtime",
  "track": "pipaw"
}
```

**确定性步骤**

1. `LoadTaskAndCompiledWm`  
2. `RunInnerLoop`（Activity，超时短、重试有限；长思考也须有上限）  
3. 对每个拟调用的 cs：`InvokeCs` Activity（内部调 hub 门禁）  
4. `approval_level ≥ L2`：`WaitForSignal("approved"|"rejected")`；超时 → `DraftChangeSet(timeout)`  
5. `PatchLiveWm`  
6. `RefreshKpi`（`cs.metric.query`）  
7. `WriteAudit`  

补偿：SoR 写成功、指标刷新失败 → 重试 RefreshKpi，不回滚已合法的 SoR 写（除非 operation 声明补偿 cs）。  
Temporal **不**存责任图、不解释 Law Pack。

事件：Workflow 事件 → Hub SSE `/hub/v1/exec/{task_id}/events`（自有，不绑 AG-UI）。

### 5.5 LangGraph 1.0 InnerLoop SPI（M19）

**冻结默认实现**：LangGraph 1.0。Codex/Pi 仅实现同一 SPI，配置 `INNERLOOP_BACKEND=langgraph|codex`，测试矩阵只跑一套。

```
inner.start_thread(StartThread):
  profile, instructions, tool_allowlist, checkpoint_id?, tenant_id, actor
  → thread_id

inner.turn(Turn):
  thread_id, user_item, wm_slice
  → { items[], tool_calls[], interrupt? }

inner.interrupt / resume / compact
```

工具回调伪代码：

```
on_tool_call(name, args):
  assert name in thread.tool_allowlist
  return hub.instance.invoke_cs  or  hub.kg.search  or  hub.metric.query
  # 禁止 httpx/SQL
```

Checkpoint：Postgres。业务状态 = live WM + Task + 审计指针，**不是**聊天全文。

压缩策略由 Hub 按剖面注入：scene 保留 Insight+五维；explore 保留不确定点与信源；runtime 保留 live WM 与审计指针。框架不得擅自丢五维。

### 5.6 MCP Gateway（M13）

- `tools/list` = Registry ⋈ profile ⋈ role ⋈ track ⋈ `agent_visible`  
- `tools/call` **重新**走 §2.3（禁止 list 缓存直通连接器）  
- tool name = `cs.{domain}.{action}`  
- scene/explore：过滤 `side_effects` 非空  

### 5.7 A2A（M21，P1+）

P0：`hub.task.transfer` 在租户内改 assignee。  
P1：岗位 Agent Card（`position_id, cs_allowlist, track=pipaw`）。对端仍进对方 Hub。身份权威不在 A2A 载荷。ACP 忽略。

### 5.8 Utopia（M22，可选）

只读导出 → 人审 ChangeSet → 写入 Law Pack / 实体白名单。禁止 Action 打 CRM。默认不部署。

### 5.9 SoR 与模型（M23/M24）

连接器实现 `connector_id`：凭证、字段映射、幂等键。Salesforce Agentforce 等只当 cs 后端。  
LLM 经 Broker 注入 instructions；禁止把厂商 Assistants 会话当实例状态。

---

## 6. 端到端主路径（衡川 LTC 样例）

数据见 `configs/accountability_graph.sample.json`：`an-stage-visit`，拜访停留 `ought=14 / is=28`，`cs_write=["cs.visit.schedule"]`。

```
1  用户打开作战台
   POST pack.open { position_id: pos-cm, period: 2026-08 }
   Hub 读 ag-hengchuan-ltc，Cube 水合 kpi.is
   今日必办上浮 status=gate 的 an-stage-visit

2  用户点「分析 / 一键派活」
   POST insight.drill { source_node_id: an-stage-visit }
   新 Thread profile=explore
   kg.search(object_ref=客户A) + metric.query(kpi-visit-dwell)
   InnerLoop 产出 Insight；grounded 必须为 true

3  用户确认
   POST task.issue { source_node_id, insight_id, assignee: BD张三,
                     cs_write: ["cs.visit.schedule"], due: 2026-08-23 }
   Task status=issued；仍不写 CRM

4  进入运行
   POST exec.open { task_id }
   Temporal RuntimeCycleWorkflow
   InnerLoop profile=runtime, tool_allowlist ⊆ cs_write
   invoke_cs cs.visit.schedule → Connector.CRM
   PatchLiveWm + RefreshKpi + Audit

5  再打开作战台
   同一 node_id，停留天数/任务状态已合流
```

失败映射见 §4.5。L2 操作停在 Temporal `awaiting_approval`，作战台展示「待你确认」。

---

## 7. 安全、双轨、密钥

| 规则 | 实现 |
|------|------|
| 双轨不混权 | 实例 `track`；Lethe 仅 selfpaw；经营写需 pipaw 或 Escalation+证据 |
| 密钥不出模型 | 连接器/KMS；tool description 无 URL/Token/SQL |
| 剖面伪造 | 服务端按入口强制 profile，忽略 body.profile |
| 租户隔离 | invariant：`t-a` 调 `t-b` 拒绝 |
| 场景禁写 | Registry `side_effects` + profile 矩阵，双检 |
| 遗忘 | Lethe 回执；图库/责任图另走治理删除，不共用 forget API |

G 层沿用企业规格：L1→G1/G4；L2→G1/G4/G6；L3→G6/G7。Hub 文中 G0–G6 为产品语言，实施以 RBAC 规格门禁 ID 为准，映射表放 `configs/gate_map.json`（P0 补）。

---

## 8. 仓库落点（禁止平行建设）

| 模块 | 已有 | 本方案增量 |
|------|------|------------|
| 责任图 | `schemas/accountability_graph.schema.json` | 水合服务、节点索引 |
| WM | `schemas/enterprise_world_model.schema.json` · `examples/world-model-studio` | 三寿命 API |
| cs.* | `configs/capability_registry.json` · `scripts/validate_capability_registry.py` | `cs.metric.query`、`cs.visit.schedule`、profile 拒绝写 |
| IAM | `enterprise-rbac-abac-spec.md` | 剖面注入步骤 0 |
| 升级 | `intent-escalation-api.md` | Runtime 按钮接 `exec` |
| 审计 | `enterprise-audit-chain-spec.md` | Promote/InvokeCs 事件类型 |
| Invariants | `harness/invariants/run-all.py` | 新增：场景写拒绝、Task 源节点、Lethe 隔离 |
| 作战台 | `projects/aios-workstudio/demo` | 接 `hub.*`，脱开纯 mock |
| Hub | T1 设计 | `hub-api` 实现 |
| 口径 | 无 | `configs/metrics/osi/` + Cube |
| 时态图 | 无 | Graphiti worker |
| 外环 | 无 | Temporal namespace `uas` |
| 内环 | T1 写 Codex/Pi | **改默认 LangGraph SPI** |

禁止新建第二套「WorkStudio API」目录名。

---

## 9. 实施工作分解

### 阶段 A · 0–6 周（L0 可运行只读）

1. 责任图 CRUD + `pack.open` 水合（Cube 可用手工 YAML/SQL 替身，接口名冻结为 `cs.metric.query`）。  
2. Hub 剖面中间件：scene 写 cs → 403。  
3. Insight/Task schema + `task.issue` 落库，不接 Temporal。  
4. 作战台 Demo 改读 sample 图 + 签发 Task（仍 mock 执行）。  
5. Invariant：`PROFILE_FORBIDS_SIDE_EFFECT`、`TASK_SOURCE_REQUIRED`。

### 阶段 B · Q1（看见可解释、办成可暂停）

1. Graphiti 接客户时间线；`insight.drill` 接地。  
2. Temporal `RuntimeCycleWorkflow` + `exec.open`。  
3. InnerLoop LangGraph 落地 SPI；ADR-SEL-002 关闭 Codex 分叉。  
4. MCP Gateway 包只读 `cs.*`。

### 阶段 C · Q2（口径与记忆）

1. Cube Core + OSI 文件进 git。  
2. Lethe 分库 + forget 回执。  
3. A2A 仅岗位 Card 设计，实现可仍用 `task.transfer`。

### 阶段 D · Q3–Q4

1. Utopia 仅评估知识审核台。  
2. 外部 ontology action 只做 cs 前检查。  
3. 不迁 Palantir；不以仓 Semantic View 替换 Cube 契约。

---

## 10. 验收矩阵

| # | 用例 | 期望 |
|---|------|------|
| A1 | 打开 CM 作战台 | 见 `an-stage-visit` gate，不等聊天 |
| A2 | scene 调 `cs.visit.schedule` | 403 + 人话 |
| A3 | `task.issue` 无 `source_node_id` | 422 `TASK_SOURCE_REQUIRED` |
| A4 | Insight 无 evidence | 422 `UNGROUNDED_INSIGHT` |
| A5 | exec.open 后 CRM 有拜访、节点 is 变化 | 审计链完整 |
| A6 | L2 未批准 | 工作流暂停，不写或写后可解释等待 |
| A7 | SelfPaw 无证据写经营 | `TRACK_ESCALATION_REQUIRED` |
| A8 | ΠPaw `memory.self.search` | 403 `MEMORY_TRACK_FORBIDDEN` |
| A9 | Explore cite 未装 Skill | 可 cite 不可 execute |
| A10 | Builder invariant 失败 | 不能 release |
| A11 | 跨租户 | 403（已有 invariant） |
| A12 | 同一 Thread 改 profile | 409 |

自动化：扩展 `harness/invariants`；A1/A5 可先契约测试后接沙箱 CRM。

---

## 11. ADR 冻结（本方案生效）

**ADR-SEL-001 语义分层**  
L0 自有（责任图 + 五维 + Law Pack）。L1 Cube+OSI。L2 Graphiti。L3 Lethe。Utopia 默认不进写路径。

**ADR-SEL-002 Agent 双环**  
控制面 Hub。外环 Temporal。内环默认 LangGraph 1.0（InnerLoop SPI）。Codex/Pi 仅备选同一 SPI。工具只经 MCP Gateway / `invoke_cs`。

**ADR-SEL-003 禁替代**  
禁止 Palantir/Fabric IQ/Agentforce/Copilot Studio 替换 L0 或 Hub。禁止口径层或知识图谱签发生产写。禁止第三套循环。禁止聊天历史当状态。

**ADR-EDH-001/002** 继续有效：双轨不混权；模型不见 REST。

---

## 12. 开放项（不阻塞 P0）

| ID | 项 | 默认 |
|----|-----|------|
| O-1 | `kpi.caliber` 从内联公式迁 `caliber_id` | P1 强制 |
| O-2 | Graph 存储 Neo4j vs FalkorDB | P0 任选其一，SPI 不变 |
| O-3 | Cube 自持 vs 托管 | P0 自持 |
| O-4 | 前台事件 AG-UI | 观察；P0 自有 SSE |
| O-5 | gate_map.json 与宪章 G0–G6 逐条对照表 | 阶段 A 补文件 |

争议时：**德压过术**；G 层否决权高于「客户已买某套件」。套件只进 S 层 Connector。

---

## 13. 文档地图

| 文档 | 用途 |
|------|------|
| **本文件** | 详细方案：契约、接口、部署、验收、WBS |
| `uas-aios-architecture.html` | **降维总图**：端云底 + 一条路 + 四把锁 |
| `UAS AIOS架构规划（自研OR集成）.md` | 模块定义与选型一览 |
| `SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md` | 市场对比与为什么选这些零件 |
| `ENTERPRISE_AGI_OPERATING_HUB.md` | 业务语言与成功标准 |
| `UAS_AIOS_CLUSTER_PRODUCTIZATION.md` | **产品化**：三平面、模块集成边、管理壳、八条协议 |
| `UAS_AIOS_MODULE_DESIGN.md` | **模块设计**：内部方案、技术栈、进程与存储、否决项 |
| `UAS_AIOS_PLATFORM_PRODUCT.md` | **平台产品**：套件、故事、数据链路、运营/系统界面与接口 |
| `harness/knowledge/technical/uas-aios-module-delivery.md` | **reqharness 开发规划**：阶段人天、TDD、发布 |
| `uas-aios-cluster.html` | 集群集成与协议可视化（非工作台皮肤） |
| `T1-CapabilityHub详细设计.md` | 剖面政策、钩子、制品寿命 |
| `T0产品定义.md` / `T1-场景态与执行态.md` | 产品与 UX |
| `UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md` | 产品套件与功能清单（历史蓝图，冲突时以本方案+宪章为准） |
