# AIOS 集群管理后台（Console · ops）实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `projects/aios-workstudio` 的模块脚手架真正跑起来——补齐从未存在的运行时契约骨架，新增 `capability_hub/ops/` 分平面子包与 33 个 `hub.ops.*` 端点，把 Console 从静态 mock 改成真调 `hub.ops.*` 的管理后台。

**Architecture:** Console（同源静态）→ `capability_hub/http_app.py`（ops 路由 + `X-Ops-Role` 入口门禁，强制 `profile=builder`，`frontline` 锁页）→ `capability_hub/ops/*`（8 平面只读视图 + 安全写，仅经既有门禁）→ `uas_hub.Hub` 核心与 15 个夹具。集成交互契约落在 `configs/protocol/registry.json` + `configs/protocol/KERNEL.yaml`（机器可读、`validate_registry` 强制）。

**Tech Stack:** Python 3.11+ / FastAPI / uvicorn / unittest；TypeScript（`ops.ts` 客户端契约）；原生 JS（Console 离线 shell）。

**依从规格：** [`docs/superpowers/specs/2026-09-11-aios-console-ops-design.md`](../specs/2026-09-11-aios-console-ops-design.md)

**硬约束（每个任务都必须满足）：**
- `ops/**` 禁词：不得出现 `invoke_cs`、`/hub/v1/kg/ingest`、`cubejs`、`graphiti`、`neo4j`、`langgraph`、`temporal`、`lethe`、`workflow_id`、`CubeQL`、`CollectionBlockModel`、`plugin-ai`、`mcp-server`。
- `ops/**` 不新建进程、不复用 SoR 密钥、不改 `hub.core` 既有行为。
- `auto_apply` 恒为 `false`。
- **不执行 git commit / 分支操作**（用户未要求）。每个任务以「回归验证」收尾，不写 commit 步骤。

---

## 文件结构（先定边界，再分解任务）

| 文件 | 职责 |
|------|------|
| `configs/metrics/osi/kpi-visit-dwell.yml` | 口径定义（`FixtureCube._load_osi` 唯一读入格式） |
| `configs/accountability_graph.sample.json` | 衡川 LTC 责任图（`Hub.from_repo` 唯一图源） |
| `configs/capability_registry.json` | 追加 `cs.visit.list` / `cs.visit.schedule` / `cs.metric.query` |
| `configs/gate_map.json` | L1–L3 → G1/G4/G6/G7 门禁映射（阶段 A 契约文件） |
| `configs/protocol/registry.json` | **M1–M24 集成交互契约**（权威声明） |
| `configs/protocol/KERNEL.yaml` | 三平面 / 八协议 / 不变量摘要 |
| `projects/aios-workstudio/demo/hub-pack-open.fixture.json` | 由脚本导出的场景夹具（测试要求存在） |
| `services/hub-api/uas_hub/adapters/{cube,evolution,artifact,iam,skill,connector,kg,memory,law}.py` | 追加只读方法（纯增量） |
| `projects/aios-workstudio/CapabilityHub/capability_hub/ops/__init__.py` | `OpsService` 组合根 + 角色门禁 |
| `.../ops/{overview,integrate,control,ontology,mesh,governance,runtime,publish}.py` | 8 平面（各 1 职责） |
| `.../capability_hub/http_app.py` | 追加 33 条 ops 路由 |
| `.../packages/hub-client/src/ops.ts` | 补 3 个新端点路径 |
| `projects/aios-workstudio/Console/demo/{api.js,app.js,data.js}` | 真调 `/hub/v1/ops/*` |
| `.../CapabilityHub/run.py` | 同源静态托管 Console + 首屏 seed |
| `.../CapabilityHub/tests/{test_ops_endpoints,test_protocol_registry}.py` | 新增契约测试 |
| `.../tests/test_scaffold.py` | 改断言：Console 调 ops + `ops/**` 禁词 |

---

# 阶段 1 · 运行时契约骨架（解锁 hub-api 测试）

**阶段目标：** `services/hub-api` 全绿（当前 61 tests / 46 errors，全部源于缺失的 configs 文件）。

### Task 1: 口径 OSI 定义

**Files:**
- Create: `configs/metrics/osi/kpi-visit-dwell.yml`

- [ ] **Step 1: 写文件**

`FixtureCube._load_osi` 只解析以 `id:` 与 `formula:` 开头的行（见 `services/hub-api/uas_hub/adapters/cube.py:16-31`）。

```yaml
id: kpi-visit-dwell
name: 阶段停留天数
unit: day
formula: now - stage_entered_at
source: crm.opportunity.stage_entered_at
grain: day
```

- [ ] **Step 2: 验证解析**

Run: `python -c "import sys; sys.path.insert(0,'services/hub-api'); from uas_hub.adapters.cube import _load_osi; from pathlib import Path; print(_load_osi(Path('configs/metrics/osi')))"`
Expected: `{'kpi-visit-dwell': 'now - stage_entered_at'}`

---

### Task 2: 衡川 LTC 责任图样例

**Files:**
- Create: `configs/accountability_graph.sample.json`
- Test: `services/hub-api/tests/test_phase_a.py`（既有，转绿）

- [ ] **Step 1: 写文件**

约束来自 `schemas/accountability_graph.schema.json`（节点 `additionalProperties:false`）与 `test_phase_a.py`、`test_hengchuan_trace.py`：
- `graph_id` 匹配 `^ag-[a-z0-9-]+$`；`pack` ∈ `ops|cm|pmo|invest`
- `an-stage-visit` 的 `org.position_id == "pos-cm"`；`kpi.status == "gate"`；`kpi.is == 28`、`kpi.ought == 14`；`kpi.kpi_id == "kpi-visit-dwell"`（`FixtureCube` 默认值 28，运行态写后变 10）
- `process.cs_write == ["cs.visit.schedule"]`（场景态禁写断言依赖它）
- `wm` 五维齐全（否则 `WM_INCOMPLETE`）；`kpi.caliber` 存在（否则 `CALIBER_MISSING`）
- `object_refs` 含 `"UEC-10293"`（`insight_drill` 据此从 KG 自动取证）

```json
{
  "graph_id": "ag-hengchuan-ltc",
  "tenant_id": "t-hengchuan",
  "pack": "cm",
  "world_model_id": "wm-hengchuan-ltc",
  "period": { "grain": "month", "from": "2026-08-01", "to": "2026-08-31" },
  "nodes": [
    {
      "node_id": "an-stage-visit",
      "parent_id": null,
      "goal": {
        "statement": "把衡川客户经理的阶段拜访停留压回 SLA 以内",
        "horizon": "2026-Q3",
        "success_criteria": "an-stage-visit 的 kpi.is <= 14"
      },
      "org": {
        "unit_id": "org.team-ltc",
        "position_id": "pos-cm",
        "owner_id": "cowen.hua",
        "raci": "A"
      },
      "kpi": {
        "kpi_id": "kpi-visit-dwell",
        "name": "阶段停留天数",
        "unit": "day",
        "caliber": "now - stage_entered_at",
        "ought": 14,
        "is": 28,
        "status": "gate"
      },
      "process": {
        "value_stream": "LTC 线索到回款",
        "stage": "qualify",
        "cs_read": ["cs.visit.list", "cs.metric.query"],
        "cs_write": ["cs.visit.schedule"],
        "system_of_record": "crm"
      },
      "wm": {
        "space": "cn.east.ltc",
        "time": "2026-08",
        "subject": "cowen.hua",
        "object": "UEC-10293",
        "feedback": "visit.scheduled -> kpi.is"
      },
      "object_refs": ["UEC-10293"]
    }
  ],
  "edges": []
}
```

- [ ] **Step 2: 跑契约测试**

Run: `python -m unittest discover -s services/hub-api/tests -p "test_phase_a.py" -v`
Expected: `test_pack_open_renders_gate_node`、`test_pack_open_slices_by_position`、`test_caliber_missing_cannot_issue` 等通过；仅剩 `cs.visit.list`/`cs.visit.schedule`/`cs.metric.query` 与 `gate_map.json`、demo fixture 相关失败（Task 3–5 解决）。

---

### Task 3: 能力注册表追加三项能力

**Files:**
- Modify: `configs/capability_registry.json`
- Test: `services/hub-api/tests/test_phase_a.py::test_write_ops_hidden_in_scene`

- [ ] **Step 1: 在 `services` 数组末尾追加三个服务**

`Registry.list_for_profile`（`registry.py:31-39`）对 `scene/explore/builder` 过滤掉**有 `side_effects`** 的 operation。因此 `cs.visit.list` 与 `cs.metric.query` 必须无 `side_effects`，`cs.visit.schedule` 必须有。

```json
{
  "id": "cs.visit",
  "domain": "visit",
  "description": "客户拜访列表与排期",
  "source_system": "crm",
  "connector_id": "connector.crm.sandbox",
  "uas_layer": "S",
  "enabled": true,
  "operations": [
    {
      "name": "list",
      "description": "列出待拜访与超期客户",
      "input": {
        "type": "object",
        "properties": {
          "owner_id": { "type": "string" },
          "overdue_only": { "type": "boolean" }
        }
      },
      "output": {
        "type": "object",
        "properties": { "items": { "type": "array" } }
      },
      "approval_level": "L1",
      "audit_required": true,
      "gates": ["G1"],
      "side_effects": [],
      "idempotent": true,
      "agent_visible": true
    },
    {
      "name": "schedule",
      "description": "为客户排期一次拜访（写 CRM）",
      "input": {
        "type": "object",
        "required": ["customer_id"],
        "properties": {
          "customer_id": { "type": "string" },
          "when": { "type": "string" }
        }
      },
      "output": {
        "type": "object",
        "properties": { "visit_id": { "type": "string" } }
      },
      "approval_level": "L2",
      "audit_required": true,
      "gates": ["G1", "G4", "G6"],
      "side_effects": ["event.visit.scheduled"],
      "idempotent": true,
      "agent_visible": true
    }
  ]
},
{
  "id": "cs.metric",
  "domain": "metric",
  "description": "经营指标口径查询",
  "source_system": "warehouse",
  "connector_id": "connector.crm.sandbox",
  "uas_layer": "K",
  "enabled": true,
  "operations": [
    {
      "name": "query",
      "description": "按口径查询 KPI 当前值（带 caliber_id / stale）",
      "input": {
        "type": "object",
        "required": ["kpi_id"],
        "properties": { "kpi_id": { "type": "string" } }
      },
      "output": {
        "type": "object",
        "properties": {
          "value": { "type": ["number", "null"] },
          "caliber_id": { "type": "string" },
          "stale": { "type": "boolean" }
        }
      },
      "approval_level": "L1",
      "audit_required": true,
      "gates": ["G1"],
      "side_effects": [],
      "idempotent": true,
      "agent_visible": true
    }
  ]
}
```

> 追加时注意 JSON 合法性：`cs.process` 之后补一个 `,`，三个对象之间用 `,` 分隔。

- [ ] **Step 2: 验证**

Run: `python -c "import sys,json; sys.path.insert(0,'services/hub-api'); from uas_hub.registry import Registry; r=Registry.from_file(__import__('pathlib').Path('configs/capability_registry.json')); print([n for n in r.list_for_profile('scene') if n.startswith('cs.visit') or n.startswith('cs.metric')])"`
Expected: `['cs.metric.query', 'cs.visit.list']`（**不含** `cs.visit.schedule`）

---

### Task 4: 门禁映射表

**Files:**
- Create: `configs/gate_map.json`
- Test: `services/hub-api/tests/test_phase_a.py::test_schema_files_exist`

- [ ] **Step 1: 写文件**

映射口径来自 `docs/strategic/design/UAS_AIOS_ARCHITECTURE_SPEC.md:514`（L1→G1/G4；L2→G1/G4/G6；L3→G6/G7）。

```json
{
  "version": "1.0.0",
  "updated_at": "2026-09-11T00:00:00Z",
  "approval_gate_mapping": {
    "L1": { "description": "自动执行：只读与低风险写", "gates": ["G1", "G4"], "human_confirm": false },
    "L2": { "description": "需用户或主管确认后执行", "gates": ["G1", "G4", "G6"], "human_confirm": true },
    "L3": { "description": "禁止 Agent 自主执行或需双人审批", "gates": ["G6", "G7"], "human_confirm": true, "dual_control": true }
  },
  "charter_gates": [
    { "id": "G0", "name": "意图显式", "note": "无意图不执行" },
    { "id": "G1", "name": "租户隔离", "note": "跨租户拒绝" },
    { "id": "G4", "name": "剖面/能力可见", "note": "不在 Registry 或剖面不可见则拒" },
    { "id": "G6", "name": "审批与证据", "note": "L2 需确认，L3 需双人" },
    { "id": "G7", "name": "审计闭环", "note": "写动作必须留审计" }
  ]
}
```

- [ ] **Step 2: 验证**

Run: `python -c "import json; d=json.load(open('configs/gate_map.json',encoding='utf-8')); print(list(d['approval_gate_mapping']))"`
Expected: `['L1', 'L2', 'L3']`

---

### Task 5: 导出场景夹具（demo）

**Files:**
- Create: `projects/aios-workstudio/demo/hub-pack-open.fixture.json`（脚本产出）
- Create: `projects/aios-workstudio/demo/hub-pack-open.fixture.js`（脚本产出）
- Script: `scripts/export_hub_pack_open.py`（既有，勿改）

- [ ] **Step 1: 运行脚本**

Run: `python scripts/export_hub_pack_open.py`
Expected: 打印 `.../projects/aios-workstudio/demo/hub-pack-open.fixture.json`

- [ ] **Step 2: 验证内容**

Run: `python -c "import json; d=json.load(open('projects/aios-workstudio/demo/hub-pack-open.fixture.json',encoding='utf-8')); print(d['pack']['graph_id'], d['write_blocked']['error']['code'], d['issued_task']['workflow_id'])"`
Expected: `ag-hengchuan-ltc PROFILE_FORBIDS_SIDE_EFFECT None`

---

### Task 6: 24 模块集成交互契约 `registry.json`

**Files:**
- Create: `configs/protocol/registry.json`
- Test: `services/hub-api/tests/test_protocol_registry.py`（既有，转绿）

- [ ] **Step 1: 写文件（**无注释的纯 JSON**，`load_registry` 走 `json.loads`）**

约束：`validate_registry`（`protocol_catalog.py:36-80`）+ `schemas/protocol/module_protocol.schema.json`：
- `modules` 恰好 24 条且 `id` 顺序为 `M1..M24`
- 每条含 `id,name,layer,decision,replaceable,protocol_id,hub_methods(list),port(string|null),verbs(非空 list),errors(list),forbidden(list)`
- `decision=="integrate"` ⇒ `port` 非空 **且** `replaceable==true`
- `M2–M6` 必须 `decision=="own"` 且 `replaceable==false`
- `policy_order` 逐字等于 `PolicyChain.ORDER`
- `envelope` 含 `tenant_id,actor_id,profile,track,correlation_id`
- `front_forbidden_nouns` 含 `workflow_id`、`CubeQL`

```json
{
  "version": "1.0.0",
  "envelope": [
    "tenant_id",
    "actor_id",
    "profile",
    "track",
    "correlation_id",
    "idempotency_key",
    "source_node_id",
    "position_id"
  ],
  "policy_order": [
    "inject",
    "tenant",
    "registry",
    "rbac",
    "approval",
    "gates",
    "scope",
    "execute",
    "audit"
  ],
  "front_forbidden_nouns": [
    "cubejs",
    "graphiti",
    "neo4j",
    "langgraph",
    "temporal",
    "lethe",
    "workflow_id",
    "CubeQL"
  ],
  "modules": [
    {
      "id": "M1",
      "name": "WorkStudio 作战台",
      "layer": "A",
      "decision": "own-shell",
      "replaceable": false,
      "protocol_id": "hub.scene",
      "hub_methods": ["hub.scene.pack.open", "hub.scene.insight.drill", "hub.scene.task.issue", "hub.scene.task.return"],
      "port": null,
      "verbs": ["render", "open", "issue", "return"],
      "errors": ["SCOPE_DENIED", "WM_INCOMPLETE"],
      "forbidden": ["当责任图", "持 SoR 密钥", "口径计算"],
      "part": "WorkStudio Web",
      "fixture": null
    },
    {
      "id": "M2",
      "name": "责任图",
      "layer": "K-L0",
      "decision": "own",
      "replaceable": false,
      "protocol_id": "hub.graph",
      "hub_methods": ["hub.graph.get", "hub.graph.validate"],
      "port": null,
      "verbs": ["get", "validate", "split"],
      "errors": ["TENANT_MISMATCH", "SCOPE_DENIED"],
      "forbidden": ["存时态事实", "当口径引擎"],
      "part": "Accountability Graph",
      "fixture": "FixtureGraph"
    },
    {
      "id": "M3",
      "name": "世界模型 Store",
      "layer": "K-L0",
      "decision": "own",
      "replaceable": false,
      "protocol_id": "hub.wm",
      "hub_methods": ["hub.wm.get", "hub.wm.patch"],
      "port": null,
      "verbs": ["get", "patch"],
      "errors": ["INVARIANT_FAILED", "WM_INCOMPLETE"],
      "forbidden": ["塞进时态图", "存个人记忆"],
      "part": "World Model Store",
      "fixture": "FixtureWm"
    },
    {
      "id": "M4",
      "name": "Law Pack",
      "layer": "K-L0",
      "decision": "own",
      "replaceable": false,
      "protocol_id": "hub.law",
      "hub_methods": ["hub.law.compile", "hub.law.diff"],
      "port": null,
      "verbs": ["compile", "diff"],
      "errors": ["INVARIANT_FAILED"],
      "forbidden": ["未批先编", "口头法典"],
      "part": "Law Pack",
      "fixture": "FixtureLaw"
    },
    {
      "id": "M5",
      "name": "Insight→Task 编译器",
      "layer": "K-L0",
      "decision": "own",
      "replaceable": false,
      "protocol_id": "hub.scene.insight",
      "hub_methods": ["hub.scene.insight.drill", "hub.scene.task.issue"],
      "port": null,
      "verbs": ["drill", "issue"],
      "errors": ["UNGROUNDED_INSIGHT", "TASK_SOURCE_REQUIRED"],
      "forbidden": ["无证据派活", "绕过责任图"],
      "part": "Insight Compiler",
      "fixture": "FixtureInsight"
    },
    {
      "id": "M6",
      "name": "Capability Hub 控制面",
      "layer": "K-L0",
      "decision": "own",
      "replaceable": false,
      "protocol_id": "hub.ops",
      "hub_methods": ["hub.ops.overview", "hub.ops.control", "hub.ops.publish"],
      "port": null,
      "verbs": ["read", "govern", "publish"],
      "errors": ["SCOPE_DENIED"],
      "forbidden": ["平行门禁", "第二套 API 进程"],
      "part": "Capability Hub",
      "fixture": null
    },
    {
      "id": "M7",
      "name": "Capability Registry cs.*",
      "layer": "K-L1",
      "decision": "own-contract",
      "replaceable": false,
      "protocol_id": "hub.registry",
      "hub_methods": ["hub.registry.list", "hub.registry.patch"],
      "port": null,
      "verbs": ["list", "patch"],
      "errors": ["OPERATION_NOT_FOUND"],
      "forbidden": ["硬编码能力", "场景态放写能力"],
      "part": "Capability Registry",
      "fixture": "FixtureRegistry"
    },
    {
      "id": "M8",
      "name": "Identity & Policy",
      "layer": "G",
      "decision": "own",
      "replaceable": false,
      "protocol_id": "hub.iam",
      "hub_methods": ["hub.iam.bind", "hub.iam.bindings"],
      "port": null,
      "verbs": ["bind", "list"],
      "errors": ["INVARIANT_FAILED", "TENANT_MISMATCH"],
      "forbidden": ["当 IdP", "跳过审批票据"],
      "part": "Identity & Policy",
      "fixture": "FixtureIam"
    },
    {
      "id": "M9",
      "name": "Skill 协议状态机",
      "layer": "A",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.skill",
      "hub_methods": ["hub.skill.transition", "hub.skill.list"],
      "port": "SkillPort",
      "verbs": ["discover", "preview", "cite", "install", "enable", "execute", "list"],
      "errors": ["INVARIANT_FAILED", "SKILL_NOT_EXECUTABLE_IN_PROFILE"],
      "forbidden": ["发现即执行", "跨剖面执行"],
      "part": "Skill State Machine",
      "fixture": "FixtureSkill"
    },
    {
      "id": "M10",
      "name": "Artifact Store",
      "layer": "S",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.artifact",
      "hub_methods": ["hub.artifact.put", "hub.artifact.list"],
      "port": "ArtifactPort",
      "verbs": ["put", "get", "list"],
      "errors": ["INVARIANT_FAILED"],
      "forbidden": ["file 当 pack 状态源"],
      "part": "Artifact Store",
      "fixture": "FixtureArtifact"
    },
    {
      "id": "M11",
      "name": "Audit",
      "layer": "G",
      "decision": "own",
      "replaceable": true,
      "protocol_id": "hub.audit",
      "hub_methods": ["hub.audit.search", "hub.audit.export"],
      "port": null,
      "verbs": ["search", "export"],
      "errors": ["SCOPE_DENIED"],
      "forbidden": ["关闭审计", "静默写"],
      "part": "Audit Log",
      "fixture": "FixtureAudit"
    },
    {
      "id": "M12",
      "name": "Evolution Engine",
      "layer": "E",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.evolution",
      "hub_methods": ["hub.evolution.draft", "hub.evolution.apply", "hub.evolution.list"],
      "port": "EvolutionPort",
      "verbs": ["draft", "apply", "list"],
      "errors": ["INVARIANT_FAILED"],
      "forbidden": ["auto_apply 为真", "未批即生效"],
      "part": "Evolution Engine",
      "fixture": "FixtureEvolution"
    },
    {
      "id": "M13",
      "name": "MCP Gateway",
      "layer": "S",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.mcp",
      "hub_methods": ["hub.mcp.list", "hub.mcp.call"],
      "port": "McpPort",
      "verbs": ["list", "call"],
      "errors": ["SCOPE_DENIED"],
      "forbidden": ["跳过判定序", "暴露密钥"],
      "part": "MCP Gateway",
      "fixture": "FixtureMcp"
    },
    {
      "id": "M14",
      "name": "System Connector",
      "layer": "S",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.connector",
      "hub_methods": ["hub.connector.invoke", "hub.connector.list"],
      "port": "ConnectorPort",
      "verbs": ["invoke", "list", "rotate"],
      "errors": ["TENANT_MISMATCH"],
      "forbidden": ["明文密钥", "非幂等写"],
      "part": "System Connector",
      "fixture": "FixtureConnector"
    },
    {
      "id": "M15",
      "name": "口径服务 Cube+OSI",
      "layer": "K-L1",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "cs.metric.query",
      "hub_methods": ["hub.metric.query", "hub.ops.caliber.status"],
      "port": "CubePort",
      "verbs": ["query", "status"],
      "errors": ["CALIBER_MISSING"],
      "forbidden": ["签发任务", "当责任图"],
      "part": "Cube Core + OSI",
      "fixture": "FixtureCube"
    },
    {
      "id": "M16",
      "name": "时态知识",
      "layer": "K-L1",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.kg",
      "hub_methods": ["hub.kg.search", "hub.kg.ingest"],
      "port": "KgPort",
      "verbs": ["search", "ingest"],
      "errors": ["INVARIANT_FAILED"],
      "forbidden": ["an-* 当节点", "当 cs 写"],
      "part": "Temporal KG",
      "fixture": "FixtureKg"
    },
    {
      "id": "M17",
      "name": "个人记忆",
      "layer": "K-L1",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.memory",
      "hub_methods": ["hub.memory.add", "hub.memory.search", "hub.memory.forget"],
      "port": "MemoryPort",
      "verbs": ["add", "search", "forget"],
      "errors": ["MEMORY_TRACK_FORBIDDEN"],
      "forbidden": ["与责任图同表", "经营轨道读取"],
      "part": "Personal Memory",
      "fixture": "FixtureMemory"
    },
    {
      "id": "M18",
      "name": "外环",
      "layer": "R",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.runtime.outer",
      "hub_methods": ["hub.exec.open", "hub.instance.cycle_step"],
      "port": "OuterLoopPort",
      "verbs": ["open", "signal", "events"],
      "errors": ["TASK_NOT_ISSUED"],
      "forbidden": ["持 SoR 密钥", "内联出站调用"],
      "part": "Outer Loop",
      "fixture": "InMemoryOuterLoop"
    },
    {
      "id": "M19",
      "name": "内环",
      "layer": "R",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.runtime.inner",
      "hub_methods": ["hub.thread.start", "hub.mcp.call"],
      "port": "InnerLoopPort",
      "verbs": ["start", "turn", "interrupt", "resume", "compact"],
      "errors": ["THREAD_PROFILE_IMMUTABLE"],
      "forbidden": ["出站 SoR", "跳过 Hub 回调"],
      "part": "Inner Loop",
      "fixture": "FixtureInnerLoop"
    },
    {
      "id": "M20",
      "name": "工具类型",
      "layer": "K",
      "decision": "own-contract",
      "replaceable": false,
      "protocol_id": "hub.schema",
      "hub_methods": ["hub.schema.validate"],
      "port": null,
      "verbs": ["validate"],
      "errors": ["INVARIANT_FAILED"],
      "forbidden": ["第二套类型定义"],
      "part": "JSON Schema / Pydantic",
      "fixture": null
    },
    {
      "id": "M21",
      "name": "跨岗位委托",
      "layer": "A",
      "decision": "optional",
      "replaceable": true,
      "protocol_id": "hub.a2a",
      "hub_methods": ["hub.a2a.delegate"],
      "port": null,
      "verbs": ["delegate"],
      "errors": ["SCOPE_DENIED"],
      "forbidden": ["P0 伪装完成"],
      "part": "A2A",
      "fixture": null
    },
    {
      "id": "M22",
      "name": "回顾 Spike",
      "layer": "E",
      "decision": "optional",
      "replaceable": false,
      "protocol_id": "hub.review",
      "hub_methods": ["hub.review.export"],
      "port": null,
      "verbs": ["export"],
      "errors": ["SCOPE_DENIED"],
      "forbidden": ["任何写路径"],
      "part": "Review Spike",
      "fixture": "FixtureReview"
    },
    {
      "id": "M23",
      "name": "主数据 SoR",
      "layer": "S",
      "decision": "connect",
      "replaceable": false,
      "protocol_id": "cs.customer.get_profile",
      "hub_methods": ["hub.connector.invoke"],
      "port": null,
      "verbs": ["read", "write"],
      "errors": ["TENANT_MISMATCH"],
      "forbidden": ["绕过连接器", "内联密钥"],
      "part": "Master Data SoR",
      "fixture": null
    },
    {
      "id": "M24",
      "name": "模型推理 Broker",
      "layer": "S",
      "decision": "integrate",
      "replaceable": true,
      "protocol_id": "hub.broker",
      "hub_methods": ["hub.broker.complete"],
      "port": "BrokerPort",
      "verbs": ["complete"],
      "errors": ["OPERATION_NOT_FOUND"],
      "forbidden": ["改 hub.* 签名", "落会话全文"],
      "part": "Inference Broker",
      "fixture": "FixtureBroker"
    }
  ]
}
```

- [ ] **Step 2: 跑契约测试**

Run: `python -m unittest services.hub_api_tests.test_protocol_registry -v` → 若因包路径失败，改用：
`cd services/hub-api && python -m unittest tests.test_protocol_registry -v`
Expected: 8 tests PASS（`test_twenty_four_modules`、`test_validate_clean`、`test_schema_validates`、`test_integrated_have_ports`、`test_l0_not_replaceable`、`test_front_forbidden_nouns` 等）

---

### Task 7: 内核声明 `KERNEL.yaml`

**Files:**
- Create: `configs/protocol/KERNEL.yaml`
- Test: `services/hub-api/tests/test_protocol_registry.py::test_kernel_and_schema_exist`

- [ ] **Step 1: 写文件**

```yaml
version: 1.0.0
kernel: uas-aios
planes:
  usage: { name: 使用平面, front: [M1, M5], shell: [M9, M13] }
  control: { name: 控制平面, owns: [M2, M3, M4, M6, M7, M8, M11, M12] }
  config_ops: { name: 配置与运维平面, owns: [M10, M14, M15, M16, M17, M18, M19, M20, M24] }
protocols:
  north: hub.*
  south: connector.*
  east: a2a.*
  west: mcp.*
  knowledge: kg.*
  horizontal: metric.*
  identity: iam.*
  evolution: evolution.*
profiles: [scene, explore, builder, runtime]
invariants:
  policy_order: [inject, tenant, registry, rbac, approval, gates, scope, execute, audit]
  scene_forbids_write: true
  auto_apply: false
  accountability_five_tuple: [goal, org, kpi, process, wm]
  front_forbidden_nouns: [cubejs, graphiti, neo4j, langgraph, temporal, lethe, workflow_id, CubeQL]
registry: ./registry.json
```

- [ ] **Step 2: 验证**

Run: `python -c "from pathlib import Path; print((Path('configs/protocol')/'KERNEL.yaml').is_file(), (Path('configs/protocol')/'registry.json').is_file())"`
Expected: `True True`

---

### Task 8: 阶段 1 回归

- [ ] **Step 1: hub-api 全绿**

Run: `python scripts/validate_uas_aios_phase_a.py`
Expected: `OK`（0 failures / 0 errors；此前为 46 errors）

- [ ] **Step 2: CapabilityHub T1 + HTTP 全绿**

Run: `cd projects/aios-workstudio/CapabilityHub && python -m unittest discover -s tests -v`
Expected: `test_t1_accept`（10 例）、`test_http`（5 例）、`test_profile_matrix` 全 PASS（此前 13 errors）

---

# 阶段 2 · 夹具只读方法（纯增量）

**阶段目标：** 为 ops 只读视图补 `list()` / `status()`；不改任何既有方法签名与行为。

### Task 9: 九个夹具追加只读方法

**Files:**
- Modify: `services/hub-api/uas_hub/adapters/cube.py`、`evolution.py`、`artifact.py`、`iam.py`、`skill.py`、`connector.py`、`kg.py`、`memory.py`、`law.py`
- Test: Create `services/hub-api/tests/test_fixture_readonly.py`

- [ ] **Step 1: 写失败测试**

```python
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HUB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HUB_ROOT))

from uas_hub.hub import Hub  # noqa: E402

REPO = Path(__file__).resolve().parents[3]


class FixtureReadonlyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = Hub.from_repo(REPO)

    def test_evolution_list(self) -> None:
        self.assertEqual(self.hub.evolution.list(), [])
        self.hub.evolution.draft({"kind": "x"})
        rows = self.hub.evolution.list()
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]["auto_apply"])

    def test_artifact_list(self) -> None:
        self.hub.artifact.put("theme", {"a": 1})
        rows = self.hub.artifact.list()
        self.assertEqual(rows[0]["kind"], "theme")
        self.assertIn("sha256", rows[0])

    def test_iam_list(self) -> None:
        rows = self.hub.iam.list()
        self.assertTrue(any(r["position_id"] == "pos-cm" for r in rows))

    def test_skill_list(self) -> None:
        self.hub.skill.transition("skill.visit", "cited", "explore")
        rows = self.hub.skill.list()
        self.assertEqual(rows[0], {"skill_id": "skill.visit", "state": "cited"})

    def test_connector_status_and_list(self) -> None:
        st = self.hub.connector.status()
        self.assertFalse(st["secrets_exposed"])
        self.assertEqual(self.hub.connector.list()[0]["id"], "connector.crm.mock")

    def test_cube_status(self) -> None:
        st = self.hub.cube.status()
        self.assertIn("kpi-visit-dwell", st["kpi_ids"])
        self.assertFalse(st["stale"])

    def test_kg_status(self) -> None:
        st = self.hub.kg.status()
        self.assertIn("ep-visit-20260715", st["episode_ids"])

    def test_memory_receipts(self) -> None:
        added = self.hub.memory.add("cowen.hua", "hello")
        self.hub.memory.forget("cowen.hua", added["memory_id"])
        rows = self.hub.memory.receipts("cowen.hua")
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["forgotten"])

    def test_law_diff(self) -> None:
        diff = self.hub.law.diff("lp-current", "lp-next")
        self.assertTrue(diff["changes"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行确认失败**

Run: `cd services/hub-api && python -m unittest tests.test_fixture_readonly -v`
Expected: FAIL（`AttributeError: 'FixtureEvolution' object has no attribute 'list'` 等 9 处）

- [ ] **Step 3: 追加方法（每处只新增，不改既有）**

`adapters/evolution.py` 类内追加：

```python
    def list(self) -> list[dict[str, Any]]:
        return [
            {"changeset_id": r["changeset_id"], "status": r["status"],
             "auto_apply": False, "applied": bool(r.get("applied"))}
            for r in self._drafts.values()
        ]
```

`adapters/artifact.py` 类内追加：

```python
    def list(self) -> list[dict[str, Any]]:
        return [
            {"artifact_id": r["artifact_id"], "kind": r["kind"], "sha256": r["sha256"]}
            for r in self._items.values()
        ]
```

`adapters/iam.py` 类内追加：

```python
    def list(self) -> list[dict[str, Any]]:
        return [
            {"actor_id": a, "tenant_id": t, "position_id": p}
            for (a, t), p in self._bindings.items()
        ]
```

`adapters/skill.py` 类内追加：

```python
    def list(self) -> list[dict[str, Any]]:
        return [{"skill_id": s, "state": st} for s, st in self._states.items()]
```

`adapters/connector.py` 类内追加：

```python
    def status(self) -> dict[str, Any]:
        return {
            "ok": True,
            "secrets_exposed": False,
            "call_count": self.call_count,
            "write_count": self.write_count,
        }

    def list(self) -> list[dict[str, Any]]:
        return [{"id": self.id, "status": "connected"}]
```

`adapters/cube.py` 类内追加：

```python
    def status(self) -> dict[str, Any]:
        return {
            "kpi_ids": sorted(set(_DEFAULTS) | set(self._osi)),
            "writes": self._writes,
            "stale": False,
        }
```

`adapters/kg.py` 类内追加：

```python
    def status(self) -> dict[str, Any]:
        return {"episodes": len(self._episodes), "episode_ids": sorted(self._episodes)}
```

`adapters/memory.py`：`__init__` 追加 `self._receipts: list[dict[str, Any]] = []`，`forget` 追加一行归档，再加 `receipts`：

```python
    def forget(self, actor_id: str, memory_id: str) -> dict[str, Any]:
        rec = self._store.get(memory_id)
        if rec is not None and rec.get("actor_id") == actor_id:
            self._store.pop(memory_id, None)
        receipt = {"receipt_id": f"rec-{uuid.uuid4().hex[:12]}", "forgotten": True, "actor_id": actor_id}
        self._receipts.append(receipt)
        return {"receipt_id": receipt["receipt_id"], "forgotten": True}

    def receipts(self, actor_id: str) -> list[dict[str, Any]]:
        return [dict(r) for r in self._receipts if r["actor_id"] == actor_id]
```

`adapters/law.py` 类内追加：

```python
    def diff(self, current_pack: str, next_pack: str) -> dict[str, Any]:
        candidate = dict(VISIT_SLA)
        candidate["rule"] = "stay_days <= 10"
        candidate["ought"] = 10
        return {
            "current_pack": current_pack,
            "next_pack": next_pack,
            "changes": [
                {"law_id": VISIT_SLA["law_id"], "field": "ought",
                 "current": VISIT_SLA["ought"], "next": candidate["ought"]}
            ],
        }
```

- [ ] **Step 4: 运行确认通过**

Run: `cd services/hub-api && python -m unittest tests.test_fixture_readonly -v`
Expected: 9 tests PASS

---

# 阶段 3 · `capability_hub/ops` 子包 + 路由 + 客户端契约

**阶段目标：** 33 个 `hub.ops.*` 端点可用，`ops/**` 无禁词，`X-Ops-Role` 入口门禁生效。

### Task 10: `OpsService` 组合根与角色门禁

**Files:**
- Create: `projects/aios-workstudio/CapabilityHub/capability_hub/ops/__init__.py`
- Test: Create `.../CapabilityHub/tests/test_ops_endpoints.py`（本任务先写门禁两例）

- [ ] **Step 1: 写失败测试**

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

HDR = {"X-Tenant-Id": "t-hengchuan", "X-Actor-Id": "cowen.hua", "X-Track": "pipaw"}


class OpsGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())

    def test_frontline_is_locked_403(self) -> None:
        res = self.client.get("/hub/v1/ops/tenant/get", headers={**HDR, "X-Ops-Role": "frontline"})
        self.assertEqual(res.status_code, 403, res.text)
        body = res.json()["error"]
        self.assertEqual(body["code"], "SCOPE_DENIED")
        self.assertIn("看不到 /console", body["detail"])

    def test_client_profile_header_cannot_escalate(self) -> None:
        res = self.client.get(
            "/hub/v1/ops/health/summary",
            headers={**HDR, "X-Ops-Role": "platform_admin", "X-Profile": "runtime"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["profile"], "builder")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行确认失败**

Run: `cd projects/aios-workstudio/CapabilityHub && python -m unittest tests.test_ops_endpoints -v`
Expected: FAIL（404 — 路由尚不存在）

- [ ] **Step 3: 写 `ops/__init__.py`**

```python
"""ops 平面组合根：只读夹具 + 仅经既有门禁的安全写。禁止平行门禁与零件名。"""

from __future__ import annotations

from pathlib import Path

from capability_hub.ops.control import ControlPlane
from capability_hub.ops.governance import GovernancePlane
from capability_hub.ops.integrate import IntegratePlane
from capability_hub.ops.mesh import MeshPlane
from capability_hub.ops.ontology import OntologyPlane
from capability_hub.ops.overview import OverviewPlane
from capability_hub.ops.publish import PublishPlane
from capability_hub.ops.runtime import RuntimePlane

from uas_hub.errors import HubError

OPS_ROLE_PROFILE = {
    "platform_admin": "builder",
    "knowledge_admin": "builder",
    "compliance": "builder",
    "operator": "builder",
    "sre": "builder",
}
LOCKED_ROLES = {"frontline"}
DEFAULT_OPS_ROLE = "platform_admin"


def resolve_ops_profile(role: str) -> str:
    """入口强制：忽略客户端 x-profile，按 X-Ops-Role 固定剖面；一线锁页。"""
    role = (role or DEFAULT_OPS_ROLE).strip()
    if role in LOCKED_ROLES:
        raise HubError("SCOPE_DENIED", "看不到 /console")
    profile = OPS_ROLE_PROFILE.get(role)
    if profile is None:
        raise HubError("SCOPE_DENIED", f"unknown ops role: {role}")
    return profile


class OpsService:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo
        self.overview = OverviewPlane(core, repo)
        self.integrate = IntegratePlane(core, repo)
        self.control = ControlPlane(core, repo)
        self.ontology = OntologyPlane(core, repo)
        self.mesh = MeshPlane(core, repo)
        self.governance = GovernancePlane(core, repo)
        self.runtime = RuntimePlane(core, repo)
        self.publish = PublishPlane(core, repo)
```

- [ ] **Step 4: 建 8 个平面空壳**（各文件先放最小可运行类，后续任务填充）

`ops/overview.py`：

```python
from __future__ import annotations

from pathlib import Path


class OverviewPlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo
```

其余 7 个平面同构（`IntegratePlane` / `ControlPlane` / `OntologyPlane` / `MeshPlane` / `GovernancePlane` / `RuntimePlane` / `PublishPlane`）。

- [ ] **Step 5: 运行确认失败原因下移**

Run: `cd projects/aios-workstudio/CapabilityHub && python -m unittest tests.test_ops_endpoints -v`
Expected: 仍 PASS 不了（路由未注册）。本任务只保证 import 不报错：
`python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.ops import OpsService, resolve_ops_profile; print(resolve_ops_profile('sre'))"`
Expected: `builder`

---

### Task 11: 总览平面（2 端点）

**Files:**
- Create: `.../ops/overview.py`（填充）

- [ ] **Step 1: 写实现**

```python
"""总览平面：租户与三平面健康聚合。只读，不触门禁。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from uas_hub.errors import HubError

CATALOG = "configs/tenant_catalog.sample.json"


class OverviewPlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo

    def tenant_get(self, tenant_id: str) -> dict[str, Any]:
        path = self.repo / CATALOG
        tenants: list[dict[str, Any]] = []
        if path.is_file():
            tenants = json.loads(path.read_text(encoding="utf-8")).get("tenants", [])
        found = next((t for t in tenants if t.get("tenant_id") == tenant_id), None)
        if found is None:
            found = {
                "tenant_id": tenant_id,
                "name": "衡川 LTC（实验租户）",
                "source": "fixture",
                "suites": ["workstudio", "platform_console", "system_services"],
            }
        return {"tenant": found}

    def health_summary(self, tenant_id: str) -> dict[str, Any]:
        if not tenant_id:
            raise HubError("TENANT_MISMATCH")
        audit = [r for r in self.core.audit if r.get("tenant_id") == tenant_id]
        cube = self.core.cube.status() if self.core.cube is not None else {"stale": True}
        kg = self.core.kg.status() if self.core.kg is not None else {"episodes": 0}
        return {
            "profile": "builder",
            "tenant_id": tenant_id,
            "planes": {
                "usage": {"insights": len(self.core.insights.insights), "tasks": len(self.core.insights.tasks)},
                "control": {"graphs": len(self.core.graphs._by_id), "audit_records": len(audit)},
                "config_ops": {"episodes": kg.get("episodes", 0), "caliber_stale": bool(cube.get("stale"))},
            },
            "open_tasks": len([t for t in self.core.insights.tasks.values() if t.get("status") == "issued"]),
        }
```

- [ ] **Step 2: 单元验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.facade import CapabilityHub; from capability_hub.ops.overview import OverviewPlane; ch=CapabilityHub.from_repo(); print(OverviewPlane(ch.core, __import__('pathlib').Path('../../')).tennant if 0 else OverviewPlane(ch.core, __import__('pathlib').Path('../../')).health_summary('t-hengchuan')['profile'])"`
Expected: `builder`

---

### Task 12: 集成平面（2 端点，含契约矩阵）

**Files:**
- Create: `.../ops/integrate.py`（填充）

- [ ] **Step 1: 写实现**

`I-01..I-12` 验收矩阵来自 `harness/traces/hengchuan-ltc/index.json`（本页只做只读展示）。

```python
"""集成平面：模块协议契约与集成验收矩阵。数据源 configs/protocol/registry.json。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from uas_hub.protocol_catalog import KERNEL_PATH, load_registry, validate_registry

INTEGRATION_MATRIX = [
    {"id": "I-01", "title": "断零件时有人话降级", "check": "零件缺失返回 available=false 而非 500"},
    {"id": "I-05", "title": "写能力只在运行态经连接器幂等落地", "check": "场景/探索/构建剖面禁写"},
    {"id": "I-07", "title": "口径缺失不得当经营事实", "check": "CALIBER_MISSING"},
    {"id": "I-09", "title": "配置变更必须出草案，auto_apply=false", "check": "ChangeSet 审批后生效"},
    {"id": "I-12", "title": "责任图五件套齐全才可签发", "check": "WM_INCOMPLETE"},
]

EIGHT_PROTOCOLS = [
    {"id": "north", "prefix": "hub.*"},
    {"id": "south", "prefix": "connector.*"},
    {"id": "east", "prefix": "a2a.*"},
    {"id": "west", "prefix": "mcp.*"},
    {"id": "knowledge", "prefix": "kg.*"},
    {"id": "horizontal", "prefix": "metric.*"},
    {"id": "identity", "prefix": "iam.*"},
    {"id": "evolution", "prefix": "evolution.*"},
]


class IntegratePlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo

    def registry(self) -> dict[str, Any]:
        data = load_registry(self.repo)
        return {
            "version": data.get("version"),
            "modules": data.get("modules", []),
            "errors": validate_registry(data),
        }

    def contracts(self) -> dict[str, Any]:
        data = load_registry(self.repo)
        return {
            "envelope": data.get("envelope", []),
            "policy_order": data.get("policy_order", []),
            "front_forbidden_nouns": data.get("front_forbidden_nouns", []),
            "protocols": EIGHT_PROTOCOLS,
            "matrix": INTEGRATION_MATRIX,
            "kernel_present": KERNEL_PATH.is_file(),
        }
```

- [ ] **Step 2: 验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from uas_hub.protocol_catalog import load_registry; d=load_registry(__import__('pathlib').Path('../..')); print(len(d['modules']))"`
Expected: `24`

---

### Task 13: 控制平面（3 端点，含判定序干跑）

**Files:**
- Create: `.../ops/control.py`（填充）

- [ ] **Step 1: 写实现**

`policy/simulate` 只走 `PolicyChain` 逐步 trace，**不调用** execute 回调，**不写** `core.audit`。

```python
"""控制平面：剖面矩阵 · explain · 判定序干跑（不执行）。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from capability_hub.profiles import load_matrix
from uas_hub.errors import Envelope, HubError
from uas_hub.policy import PolicyChain


class ControlPlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo

    def matrix(self) -> dict[str, Any]:
        return load_matrix()

    def explain(self, code: str) -> dict[str, Any]:
        return self.core.explain(code)

    def simulate(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        operation = str(payload.get("operation") or "")
        if not operation:
            raise HubError("OPERATION_NOT_FOUND", "operation required")
        audit_before = len(self.core.audit)
        trace = PolicyChain.TRACE if False else list(PolicyChain.ORDER)
        steps = []
        for name in PolicyChain.ORDER:
            if name == "registry" and self.core.registry.get(operation) is None:
                steps.append({"step": name, "ok": False, "code": "OPERATION_NOT_FOUND"})
                return {"operation": operation, "allowed": False, "steps": steps,
                        "auto_apply": False, "executed": False}
            if name == "approval":
                op = self.core.registry.get(operation) or {}
                steps.append({"step": name, "ok": True, "level": op.get("approval_level", "L1")})
                continue
            steps.append({"step": name, "ok": True})
        if len(self.core.audit) != audit_before:
            raise HubError("INVARIANT_FAILED", "simulate must not write audit")
        return {"operation": operation, "allowed": True, "steps": steps,
                "auto_apply": False, "executed": False}
```

- [ ] **Step 2: 单元验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.facade import CapabilityHub; from capability_hub.ops.control import ControlPlane; from uas_hub.errors import Envelope; ch=CapabilityHub.from_repo(); c=ControlPlane(ch.core, __import__('pathlib').Path('.')); env=Envelope('t-hengchuan','cowen.hua','builder','pipaw'); print(c.simulate(env, {'operation':'cs.visit.schedule'})['executed'], len(ch.core.audit))"`
Expected: `False 0`

---

### Task 14: 本体平面（4 端点）

**Files:**
- Create: `.../ops/ontology.py`（填充）

- [ ] **Step 1: 写实现**

```python
"""本体平面：责任图 · WM 寿命 · 法则包差异。只读 graph/wm/law。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from uas_hub.errors import HubError
from uas_hub.graph_store import node_incomplete

GRAPH_ID = "ag-hengchuan-ltc"


class OntologyPlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo

    def _graph(self, tenant_id: str, graph_id: str = "") -> dict[str, Any]:
        gid = graph_id or GRAPH_ID
        graph = self.core.graphs.get(gid)
        if graph is None:
            raise HubError("TENANT_MISMATCH", gid)
        if graph.get("tenant_id") != tenant_id:
            raise HubError("TENANT_MISMATCH")
        return graph

    def graph_get(self, tenant_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        graph = self._graph(tenant_id, str(payload.get("graph_id") or ""))
        return {"graph_id": graph["graph_id"], "nodes": graph.get("nodes", []),
                "edges": graph.get("edges", [])}

    def graph_validate(self, tenant_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        graph = self._graph(tenant_id, str(payload.get("graph_id") or ""))
        rows = []
        for node in graph.get("nodes", []):
            gap = node_incomplete(node)
            rows.append({"node_id": node.get("node_id"), "complete": gap is None, "gap": gap})
        return {"graph_id": graph["graph_id"], "ok": all(r["complete"] for r in rows), "nodes": rows}

    def wm_get(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.core.wm.get(
            str(payload.get("world_model_id") or ""),
            str(payload.get("lifetime") or "draft"),
            payload.get("version"),
        )

    def law_diff(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self.core.law is None:
            return {"available": False, "reason": "法则服务未挂载", "changes": []}
        return self.core.law.diff(
            str(payload.get("current_pack") or "lp-current"),
            str(payload.get("next_pack") or "lp-next"),
        )
```

- [ ] **Step 2: 验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.facade import CapabilityHub; from capability_hub.ops.ontology import OntologyPlane; ch=CapabilityHub.from_repo(); print(OntologyPlane(ch.core, __import__('pathlib').Path('.')).graph_validate('t-hengchuan', {})['ok'])"`
Expected: `True`

---

### Task 15: 网格平面（6 端点）

**Files:**
- Create: `.../ops/mesh.py`（填充）

- [ ] **Step 1: 写实现**

`connector/rotate` 仅改槽位元数据，**不落密钥**；`registry/patch` 只出 ChangeSet 草案。

```python
"""网格平面：能力 Registry · MCP 预览 · 连接器 · schema 漂移。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from uas_hub.errors import Envelope, HubError
from uas_hub.protocol_catalog import load_registry, validate_registry

CONNECTORS = "configs/connectors.json"


class MeshPlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo
        self._rotations: list[dict[str, Any]] = []

    def registry_list(self, tenant_id: str) -> dict[str, Any]:
        services = []
        for name, op in sorted(self.core.registry._ops.items()):
            services.append({
                "operation": name,
                "service_id": op.get("service_id"),
                "approval_level": op.get("approval_level", "L1"),
                "side_effects": op.get("side_effects") or [],
                "agent_visible": bool(op.get("agent_visible", True)),
            })
        return {"tenant_id": tenant_id, "operations": services}

    def registry_patch(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        drafted = self.core.evolution_draft(env, {"kind": "registry_patch", **payload})
        return {**drafted, "auto_apply": False}

    def mcp_preview(self, env: Envelope, profile: str) -> dict[str, Any]:
        probe = Envelope(env.tenant_id, env.actor_id, profile or "builder", env.track)
        return {"profile": probe.profile, "tools": self.core.mcp_list(probe)["tools"]}

    def connector_list(self, tenant_id: str) -> dict[str, Any]:
        rows: list[dict[str, Any]] = []
        path = self.repo / CONNECTORS
        if path.is_file():
            rows = json.loads(path.read_text(encoding="utf-8")).get("connectors", [])
        live = self.core.connector.list() if self.core.connector is not None else []
        return {"tenant_id": tenant_id, "connectors": rows, "runtime": live,
                "rotations": list(self._rotations)}

    def connector_rotate(self, payload: dict[str, Any]) -> dict[str, Any]:
        connector_id = str(payload.get("connector_id") or "")
        slot = str(payload.get("slot") or "sandbox")
        if not connector_id:
            raise HubError("OPERATION_NOT_FOUND", "connector_id required")
        if connector_id not in {"connector.crm", "connector.bpm", "connector.itsm", "connector.crm.mock"}:
            raise HubError("OPERATION_NOT_FOUND", connector_id)
        rec = {"connector_id": connector_id, "slot": slot, "rotated": True, "secret_written": False}
        self._rotations.append(rec)
        return rec

    def schema_drift(self) -> dict[str, Any]:
        errors = validate_registry(load_registry(self.repo))
        return {"status": "healthy" if not errors else "drift",
                "count": len(errors), "errors": errors}
```

- [ ] **Step 2: 验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.facade import CapabilityHub; from capability_hub.ops.mesh import MeshPlane; ch=CapabilityHub.from_repo(); print(MeshPlane(ch.core, __import__('pathlib').Path('../..')).schema_drift())"`
Expected: `{'status': 'healthy', 'count': 0, ...}`

---

### Task 16: 治理平面（5 端点）

**Files:**
- Create: `.../ops/governance.py`（填充）

- [ ] **Step 1: 写实现**

```python
"""治理平面：IAM 绑定 · 审计检索/导出 · Skill · Artifact。全只读。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from capability_hub.profiles import load_matrix
from capability_hub.skills import CATALOG


class GovernancePlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo

    def iam_bindings(self, tenant_id: str) -> dict[str, Any]:
        rows = [r for r in self.core.iam.list() if r["tenant_id"] == tenant_id] if self.core.iam else []
        return {"tenant_id": tenant_id, "bindings": rows}

    def audit_search(self, tenant_id: str, query: str = "") -> dict[str, Any]:
        rows = [r for r in self.core.audit if r.get("tenant_id") == tenant_id]
        if query:
            rows = [r for r in rows if query in str(r)]
        return {"tenant_id": tenant_id, "count": len(rows), "records": rows}

    def audit_export(self, tenant_id: str, query: str = "") -> dict[str, Any]:
        found = self.audit_search(tenant_id, query)
        return {"tenant_id": tenant_id, "format": "jsonl", "count": found["count"],
                "records": found["records"], "read_only": True}

    def skill_list(self, tenant_id: str) -> dict[str, Any]:
        states = {r["skill_id"]: r["state"] for r in self.core.skill.list()} if self.core.skill else {}
        rows = [
            {"skill_id": s["skill_id"], "state": states.get(s["skill_id"], "discovered"),
             "summary": s.get("summary", "")}
            for s in CATALOG
        ]
        matrix = load_matrix()["profiles"]
        return {"tenant_id": tenant_id, "skills": rows,
                "max_state": {p: matrix[p]["skill_max_state"] for p in matrix}}

    def artifact_list(self, tenant_id: str) -> dict[str, Any]:
        rows = self.core.artifact.list() if self.core.artifact is not None else []
        return {"tenant_id": tenant_id, "artifacts": rows}
```

- [ ] **Step 2: 验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.facade import CapabilityHub; from capability_hub.ops.governance import GovernancePlane; ch=CapabilityHub.from_repo(); print([r['skill_id'] for r in GovernancePlane(ch.core, __import__('pathlib').Path('.')).skill_list('t-hengchuan')['skills']])"`
Expected: 含 `skill.visit`、`skill.quote`

---

### Task 17: 运行平面（7 端点）

**Files:**
- Create: `.../ops/runtime.py`（填充）

- [ ] **Step 1: 写实现**

续跑经 `core.cycle_step`（内部 signal 外环），**不出现**任何禁词；任务视图白名单投影，不外泄运行引用。

```python
"""运行平面：任务 · 口径 · 时态知识 · 记忆回执 · 模型路由。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from uas_hub.errors import Envelope, HubError

VISIBLE_TASK_FIELDS = ("task_id", "tenant_id", "source_node_id", "status", "assignee", "cs_write", "track")


class RuntimePlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo

    def task_list(self, tenant_id: str, query: str = "") -> dict[str, Any]:
        rows = []
        for task in self.core.insights.tasks.values():
            if task.get("tenant_id") != tenant_id:
                continue
            row = {k: task.get(k) for k in VISIBLE_TASK_FIELDS}
            if query and query not in str(row):
                continue
            rows.append(row)
        return {"tenant_id": tenant_id, "tasks": rows}

    def retry(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        task_id = str(payload.get("task_id") or "")
        if not task_id:
            raise HubError("TASK_NOT_ISSUED")
        result = self.core.cycle_step(env, {"task_id": task_id, "signal": str(payload.get("signal") or "retry")})
        return {"task_id": task_id, "status": result.get("status"), "auto_apply": False}

    def caliber_status(self) -> dict[str, Any]:
        if self.core.cube is None:
            return {"available": False, "reason": "口径服务未挂载"}
        return {"available": True, **self.core.cube.status()}

    def kg_status(self) -> dict[str, Any]:
        if self.core.kg is None:
            return {"available": False, "reason": "知识服务未挂载", "episodes": 0}
        return {"available": True, **self.core.kg.status()}

    def kg_search(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self.core.kg is None:
            return {"available": False, "reason": "知识服务未挂载", "episodes": []}
        return {"episodes": self.core.kg.search(
            object_ref=payload.get("object_ref"), query=payload.get("query"))}

    def memory_receipt(self, actor_id: str, query: str = "") -> dict[str, Any]:
        if self.core.memory is None:
            return {"actor_id": actor_id, "receipts": []}
        rows = self.core.memory.receipts(actor_id)
        if query:
            rows = [r for r in rows if query in str(r)]
        return {"actor_id": actor_id, "receipts": rows}

    def model_route(self) -> dict[str, Any]:
        routes = getattr(self.core.broker, "routes", {}) if self.core.broker is not None else {}
        catalog = "configs/ecoystem"  # noqa: F841
        path = self.repo / "configs" / "ecosystem_scenario_catalog.json"
        declared: list[dict[str, Any]] = []
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            declared = data.get("models", []) if isinstance(data, dict) else []
        return {"routes": [{"route_id": k, "provider": v} for k, v in routes.items()],
                "declared": declared}
```

> 若 `configs/ecosystem_scenario_catalog.json` 结构不含 `models`，`declared` 保留为空数组即可；**不要**新增对该文件结构的强断言。

- [ ] **Step 2: 验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.facade import CapabilityHub; from capability_hub.ops.runtime import RuntimePlane; ch=CapabilityHub.from_repo(); print(RuntimePlane(ch.core, __import__('pathlib').Path('../..')).caliber_status()['available'], RuntimePlane(ch.core, __import__('pathlib').Path('../..')).model_route()['routes'])"`
Expected: `True [{'route_id': 'explore', ...}, {'route_id': 'runtime', ...}]`

---

### Task 18: 发布平面（4 端点）

**Files:**
- Create: `.../ops/publish.py`（填充）

- [ ] **Step 1: 写实现**

```python
"""发布平面：ChangeSet 队列与提交/裁决。全部出草案，auto_apply 恒 false。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from uas_hub.errors import Envelope, HubError


class PublishPlane:
    def __init__(self, core, repo: Path) -> None:
        self.core = core
        self.repo = repo

    def list(self, tenant_id: str) -> dict[str, Any]:
        rows = self.core.evolution.list() if self.core.evolution is not None else []
        return {"tenant_id": tenant_id, "changesets": rows, "auto_apply": False}

    def submit(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        drafted = self.core.evolution_draft(env, {"kind": "changeset_submit", **payload})
        return {**drafted, "auto_apply": False}

    def decide(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        changeset_id = str(payload.get("changeset_id") or "")
        if not changeset_id:
            raise HubError("INVARIANT_FAILED", "changeset_id required")
        approved = bool(payload.get("approved"))
        return self.core.evolution_apply(env, changeset_id, approved)

    def graph_publish(self, env: Envelope, payload: dict[str, Any]) -> dict[str, Any]:
        drafted = self.core.evolution_draft(env, {"kind": "graph_publish", **payload})
        return {**drafted, "auto_apply": False}
```

- [ ] **Step 2: 验证**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; from capability_hub.facade import CapabilityHub; from capability_hub.ops.publish import PublishPlane; ch=CapabilityHub.from_repo(); p=PublishPlane(ch.core, __import__('pathlib').Path('.')); print(p.list('t-hengchuan')['auto_apply'], p.submit(__import__('uas_hub.errors',fromlist=['Envelope']).Envelope('t-hengchuan','cowen.hua','builder','pipaw'), {'kind':'x'})['auto_apply'])"`
Expected: `False False`

---

### Task 19: 注册 33 条 ops 路由 + 入口门禁

**Files:**
- Modify: `projects/aios-workstudio/CapabilityHub/capability_hub/http_app.py`
- Test: `.../CapabilityHub/tests/test_ops_endpoints.py`

- [ ] **Step 1: 加 import 与 ops 信封工厂**

在 `http_app.py` 顶部 import 区追加：

```python
from capability_hub.ops import OpsService, resolve_ops_profile
```

在 `_envelope` 之后追加：

```python
def _ops_envelope(request: Request, ch: CapabilityHub, body: dict[str, Any] | None = None) -> Envelope:
    """ops 入口强制：x-profile 无效，X-Ops-Role 决定剖面；frontline 锁页。"""
    role = request.headers.get("x-ops-role") or ""
    profile = resolve_ops_profile(role)
    env = Envelope(
        tenant_id=request.headers.get("x-tenant-id") or "",
        actor_id=request.headers.get("x-actor-id") or "anonymous",
        profile=profile,
        track=request.headers.get("x-track") or "pipaw",
        correlation_id=request.headers.get("x-correlation-id") or "corr-ops",
        idempotency_key=request.headers.get("idempotency-key") or "",
        position_id=(body or {}).get("position_id"),
    )
    if not env.tenant_id:
        raise HubError("TENANT_MISMATCH")
    return env
```

- [ ] **Step 2: 在 `create_app` 内、既有 `profile_matrix` 之后追加路由块**

```python
    ops = OpsService(ch.core, REPO)

    @app.get("/hub/v1/ops/tenant/get")
    def ops_tenant_get(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.overview.tenant_get(env.tenant_id)

    @app.get("/hub/v1/ops/health/summary")
    def ops_health_summary(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.overview.health_summary(env.tenant_id)

    @app.get("/hub/v1/ops/protocol/registry")
    def ops_protocol_registry(request: Request) -> dict[str, Any]:
        _ops_envelope(request, ch)
        return ops.integrate.registry()

    @app.get("/hub/v1/ops/protocol/contracts")
    def ops_protocol_contracts(request: Request) -> dict[str, Any]:
        _ops_envelope(request, ch)
        return ops.integrate.contracts()

    @app.post("/hub/v1/ops/policy/explain")
    def ops_policy_explain(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ops_envelope(request, ch, body)
        return ops.control.explain(str((body or {}).get("code") or ""))

    @app.post("/hub/v1/ops/policy/simulate")
    def ops_policy_simulate(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.control.simulate(env, body or {})

    @app.post("/hub/v1/ops/graph/get")
    def ops_graph_get(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.ontology.graph_get(env.tenant_id, body or {})

    @app.post("/hub/v1/ops/graph/validate")
    def ops_graph_validate(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.ontology.graph_validate(env.tenant_id, body or {})

    @app.post("/hub/v1/ops/wm/get")
    def ops_wm_get(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ops_envelope(request, ch, body)
        return ops.ontology.wm_get(body or {})

    @app.post("/hub/v1/ops/law/diff")
    def ops_law_diff(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ops_envelope(request, ch, body)
        return ops.ontology.law_diff(body or {})

    @app.get("/hub/v1/ops/registry/list")
    def ops_registry_list(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.mesh.registry_list(env.tenant_id)

    @app.post("/hub/v1/ops/registry/patch")
    def ops_registry_patch(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.mesh.registry_patch(env, body or {})

    @app.get("/hub/v1/ops/mcp/preview")
    def ops_mcp_preview(request: Request, profile: str = "builder") -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.mesh.mcp_preview(env, profile)

    @app.get("/hub/v1/ops/connector/list")
    def ops_connector_list(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.mesh.connector_list(env.tenant_id)

    @app.post("/hub/v1/ops/connector/rotate")
    def ops_connector_rotate(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ops_envelope(request, ch, body)
        return ops.mesh.connector_rotate(body or {})

    @app.get("/hub/v1/ops/schema/drift")
    def ops_schema_drift(request: Request) -> dict[str, Any]:
        _ops_envelope(request, ch)
        return ops.mesh.schema_drift()

    @app.get("/hub/v1/ops/iam/bindings")
    def ops_iam_bindings(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.governance.iam_bindings(env.tenant_id)

    @app.get("/hub/v1/ops/audit/search")
    def ops_audit_search(request: Request, q: str = "") -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.governance.audit_search(env.tenant_id, q)

    @app.get("/hub/v1/ops/audit/export")
    def ops_audit_export(request: Request, q: str = "") -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.governance.audit_export(env.tenant_id, q)

    @app.get("/hub/v1/ops/skill/list")
    def ops_skill_list(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.governance.skill_list(env.tenant_id)

    @app.get("/hub/v1/ops/artifact/list")
    def ops_artifact_list(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.governance.artifact_list(env.tenant_id)

    @app.get("/hub/v1/ops/runtime/task")
    def ops_runtime_task(request: Request, q: str = "") -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.runtime.task_list(env.tenant_id, q)

    @app.post("/hub/v1/ops/runtime/retry")
    def ops_runtime_retry(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.runtime.retry(env, body or {})

    @app.get("/hub/v1/ops/caliber/status")
    def ops_caliber_status(request: Request) -> dict[str, Any]:
        _ops_envelope(request, ch)
        return ops.runtime.caliber_status()

    @app.get("/hub/v1/ops/kg/ingest_status")
    def ops_kg_ingest_status(request: Request) -> dict[str, Any]:
        _ops_envelope(request, ch)
        return ops.runtime.kg_status()

    @app.post("/hub/v1/ops/kg/search")
    def ops_kg_search(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        _ops_envelope(request, ch, body)
        return ops.runtime.kg_search(body or {})

    @app.get("/hub/v1/ops/memory/receipt")
    def ops_memory_receipt(request: Request, q: str = "") -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.runtime.memory_receipt(env.actor_id, q)

    @app.get("/hub/v1/ops/model/route")
    def ops_model_route(request: Request) -> dict[str, Any]:
        _ops_envelope(request, ch)
        return ops.runtime.model_route()

    @app.get("/hub/v1/ops/changeset/list")
    def ops_changeset_list(request: Request) -> dict[str, Any]:
        env = _ops_envelope(request, ch)
        return ops.publish.list(env.tenant_id)

    @app.post("/hub/v1/ops/changeset/submit")
    def ops_changeset_submit(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.publish.submit(env, body or {})

    @app.post("/hub/v1/ops/changeset/decide")
    def ops_changeset_decide(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.publish.decide(env, body or {})

    @app.post("/hub/v1/ops/graph/publish")
    def ops_graph_publish(request: Request, body: dict[str, Any] | None = None) -> dict[str, Any]:
        env = _ops_envelope(request, ch, body)
        return ops.publish.graph_publish(env, body or {})
```

> 计数：tenant/get, health/summary（2）· protocol/registry, protocol/contracts（2）· profile/matrix（1，既有）· policy/explain, policy/simulate（2）· graph/get, graph/validate, wm/get, law/diff（4）· registry/list, registry/patch, mcp/preview, connector/list, connector/rotate, schema/drift（6）· iam/bindings, audit/search, audit/export, skill/list, artifact/list（5）· runtime/task, runtime/retry, caliber/status, kg/ingest_status, kg/search, memory/receipt, model/route（7）· changeset/list, changeset/submit, changeset/decide, graph/publish（4）= **33**

- [ ] **Step 3: 跑门禁测试**

Run: `cd projects/aios-workstudio/CapabilityHub && python -m unittest tests.test_ops_endpoints -v`
Expected: 2 tests PASS（`frontline` → 403 + `detail` 含「看不到 /console」；x-profile 无法提权，返回 `profile==builder`）

- [ ] **Step 4: 补齐 33 端点冒烟断言**

在 `test_ops_endpoints.py` 的 `OpsGateTests` 后追加：

```python
class OpsEndpointSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())
        self.hdr = {**HDR, "X-Ops-Role": "platform_admin"}
        self.sec = {**HDR, "X-Ops-Role": "sre"}

    def test_all_get_endpoints_200(self) -> None:
        gets = [
            "/hub/v1/ops/tenant/get", "/hub/v1/ops/health/summary",
            "/hub/v1/ops/profile/matrix", "/hub/v1/ops/protocol/registry",
            "/hub/v1/ops/protocol/contracts", "/hub/v1/ops/registry/list",
            "/hub/v1/ops/mcp/preview?profile=builder", "/hub/v1/ops/connector/list",
            "/hub/v1/ops/schema/drift", "/hub/v1/ops/iam/bindings",
            "/hub/v1/ops/skill/list", "/hub/v1/ops/artifact/list",
            "/hub/v1/ops/caliber/status", "/hub/v1/ops/kg/ingest_status",
            "/hub/v1/ops/memory/receipt", "/hub/v1/ops/runtime/task",
            "/hub/v1/ops/model/route", "/hub/v1/ops/changeset/list",
        ]
        for path in gets:
            self.assertEqual(self.client.get(path, headers=self.hdr).status_code, 200, path)

    def test_all_post_endpoints_200(self) -> None:
        posts = [
            ("/hub/v1/ops/policy/explain", {"code": "SCOPE_DENIED"}),
            ("/hub/v1/ops/policy/simulate", {"operation": "cs.visit.schedule"}),
            ("/hub/v1/ops/graph/get", {}),
            ("/hub/v1/ops/graph/validate", {}),
            ("/hub/v1/ops/wm/get", {"world_model_id": "wm-cm", "lifetime": "draft"}),
            ("/hub/v1/ops/law/diff", {}),
            ("/hub/v1/ops/registry/patch", {"op": "cs.visit.list", "enabled": True}),
            ("/hub/v1/ops/connector/rotate", {"connector_id": "connector.crm", "slot": "prod"}),
            ("/hub/v1/ops/kg/search", {"query": "UEC-10293"}),
            ("/hub/v1/ops/changeset/submit", {"kind": "demo"}),
            ("/hub/v1/ops/changeset/decide", {"changeset_id": "cs-evo-0001", "approved": True}),
            ("/hub/v1/ops/graph/publish", {"graph_id": "ag-hengchuan-ltc"}),
        ]
        for path, payload in posts:
            self.assertEqual(self.client.post(path, headers=self.hdr, json=payload).status_code, 200, path)

    def test_schema_drift_is_healthy(self) -> None:
        body = self.client.get("/hub/v1/ops/schema/drift", headers=self.hdr).json()
        self.assertEqual(body["status"], "healthy")
        self.assertEqual(body["count"], 0)

    def test_audit_export_is_read_only(self) -> None:
        body = self.client.get("/hub/v1/ops/audit/export", headers=self.hdr).json()
        self.assertTrue(body["read_only"])

    def test_simulate_does_not_execute(self) -> None:
        body = self.client.post(
            "/hub/v1/ops/policy/simulate", headers=self.hdr, json={"operation": "cs.visit.schedule"}
        ).json()
        self.assertFalse(body["executed"])
        self.assertFalse(body["auto_apply"])
```

- [ ] **Step 5: 运行**

Run: `cd projects/aios-workstudio/CapabilityHub && python -m unittest tests.test_ops_endpoints -v`
Expected: 7 tests PASS

---

### Task 20: 客户端契约 `ops.ts` 补 3 个新端点

**Files:**
- Modify: `projects/aios-workstudio/packages/hub-client/src/ops.ts`
- Test: `projects/aios-workstudio/tests/test_scaffold.py::test_console_client_only_ops`

- [ ] **Step 1: 追加 3 条路径常量（沿用文件既有风格）**

```ts
export const OPS_PROTOCOL_REGISTRY = "/hub/v1/ops/protocol/registry";
export const OPS_PROTOCOL_CONTRACTS = "/hub/v1/ops/protocol/contracts";
export const OPS_POLICY_SIMULATE = "/hub/v1/ops/policy/simulate";
```

- [ ] **Step 2: 验证**

Run: `cd projects/aios-workstudio && python -m unittest tests.test_scaffold.ScaffoldTests.test_console_client_only_ops -v`
Expected: PASS（仍不得含 `/hub/v1/instance/invoke_cs`、`/hub/v1/kg/ingest`）

---

### Task 21: 协议契约测试（CapabilityHub 侧）

**Files:**
- Create: `projects/aios-workstudio/CapabilityHub/tests/test_protocol_registry.py`

- [ ] **Step 1: 写测试**

```python
from __future__ import annotations

import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "services" / "hub-api"))

from uas_hub.policy import PolicyChain  # noqa: E402
from uas_hub.protocol_catalog import load_registry, validate_registry  # noqa: E402


class WorkStudioProtocolRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load_registry(REPO)

    def test_validate_clean(self) -> None:
        self.assertEqual(validate_registry(self.data), [])

    def test_policy_order_matches(self) -> None:
        self.assertEqual(tuple(self.data["policy_order"]), PolicyChain.ORDER)

    def test_integrate_has_port_and_replaceable(self) -> None:
        for mod in self.data["modules"]:
            if mod["decision"] == "integrate":
                self.assertTrue(mod["port"], mod["id"])
                self.assertTrue(mod["replaceable"], mod["id"])

    def test_l0_owned(self) -> None:
        for mid in ("M2", "M3", "M4", "M5", "M6"):
            mod = next(m for m in self.data["modules"] if m["id"] == mid)
            self.assertEqual(mod["decision"], "own")
            self.assertFalse(mod["replaceable"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行**

Run: `cd projects/aios-workstudio/CapabilityHub && python -m unittest tests.test_protocol_registry -v`
Expected: 4 tests PASS

---

### Task 22: 阶段 3 回归 + 禁词自检

- [ ] **Step 1: ops 包禁词自查（先手动跑一次，Task 26 会固化成断言）**

Run:
```bash
cd projects/aios-workstudio && python - <<'PY'
from pathlib import Path
ops = Path("CapabilityHub/capability_hub/ops")
blob = "".join(p.read_text(encoding="utf-8") for p in ops.rglob("*.py"))
for noun in ("cubejs","graphiti","neo4j","langgraph","temporal","lethe","workflow_id","CubeQL",
             "invoke_cs","/hub/v1/kg/ingest","CollectionBlockModel","plugin-ai","mcp-server"):
    assert noun not in blob, noun
print("ops clean")
PY
```
Expected: `ops clean`

- [ ] **Step 2: 全量回归**

Run: `cd projects/aios-workstudio/CapabilityHub && python -m unittest discover -s tests -v`
Expected: 全 PASS（含新增 `test_ops_endpoints` 7 例、`test_protocol_registry` 4 例）

- [ ] **Step 3: hub-api 回归（确认阶段 2 增量未破坏）**

Run: `python scripts/validate_uas_aios_phase_a.py`
Expected: `OK`

---

# 阶段 4 · Console 真连 `hub.ops.*`

**阶段目标：** Console 8 页经 `fetch` 真调 `/hub/v1/ops/*`；`data.js` 收敛为 IA 常量；`run.py` 同源托管；`test_scaffold` 转绿并新增 `ops/**` 禁词断言。

### Task 23: Console API 客户端

**Files:**
- Create: `projects/aios-workstudio/Console/demo/api.js`

- [ ] **Step 1: 写文件**

```js
/* Platform Console ops 客户端：只调 /hub/v1/ops/*，剖面由 X-Ops-Role 决定。 */
(() => {
  "use strict";

  const OPS = {
    tenantGet: ["GET", "/hub/v1/ops/tenant/get"],
    healthSummary: ["GET", "/hub/v1/ops/health/summary"],
    profileMatrix: ["GET", "/hub/v1/ops/profile/matrix"],
    protocolRegistry: ["GET", "/hub/v1/ops/protocol/registry"],
    protocolContracts: ["GET", "/hub/v1/ops/protocol/contracts"],
    policyExplain: ["POST", "/hub/v1/ops/policy/explain"],
    policySimulate: ["POST", "/hub/v1/ops/policy/simulate"],
    graphGet: ["POST", "/hub/v1/ops/graph/get"],
    graphValidate: ["POST", "/hub/v1/ops/graph/validate"],
    wmGet: ["POST", "/hub/v1/ops/wm/get"],
    lawDiff: ["POST", "/hub/v1/ops/law/diff"],
    registryList: ["GET", "/hub/v1/ops/registry/list"],
    registryPatch: ["POST", "/hub/v1/ops/registry/patch"],
    mcpPreview: ["GET", "/hub/v1/ops/mcp/preview"],
    connectorList: ["GET", "/hub/v1/ops/connector/list"],
    connectorRotate: ["POST", "/hub/v1/ops/connector/rotate"],
    schemaDrift: ["GET", "/hub/v1/ops/schema/drift"],
    iamBindings: ["GET", "/hub/v1/ops/iam/bindings"],
    auditSearch: ["GET", "/hub/v1/ops/audit/search"],
    auditExport: ["GET", "/hub/v1/ops/audit/export"],
    skillList: ["GET", "/hub/v1/ops/skill/list"],
    artifactList: ["GET", "/hub/v1/ops/artifact/list"],
    runtimeTask: ["GET", "/hub/v1/ops/runtime/task"],
    runtimeRetry: ["POST", "/hub/v1/ops/runtime/retry"],
    caliberStatus: ["GET", "/hub/v1/ops/caliber/status"],
    kgIngestStatus: ["GET", "/hub/v1/ops/kg/ingest_status"],
    kgSearch: ["POST", "/hub/v1/ops/kg/search"],
    memoryReceipt: ["GET", "/hub/v1/ops/memory/receipt"],
    modelRoute: ["GET", "/hub/v1/ops/model/route"],
    changesetList: ["GET", "/hub/v1/ops/changeset/list"],
    changesetSubmit: ["POST", "/hub/v1/ops/changeset/submit"],
    changesetDecide: ["POST", "/hub/v1/ops/changeset/decide"],
    graphPublish: ["POST", "/hub/v1/ops/graph/publish"],
  };

  async function call(key, { query, body } = {}) {
    const [method, path] = OPS[key];
    const state = window.ConsoleState;
    const url = new URL(path, window.location.origin);
    Object.entries(query || {}).forEach(([k, v]) => v && url.searchParams.set(k, v));
    const res = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        "X-Tenant-Id": state.tenantId,
        "X-Actor-Id": state.actorId,
        "X-Track": state.track,
        "X-Ops-Role": state.role,
      },
      body: method === "POST" ? JSON.stringify(body || {}) : undefined,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const err = (data && data.error) || { code: "HTTP_" + res.status, message: "请求失败" };
      const e = new Error(err.message);
      e.code = err.code;
      e.payload = err;
      throw e;
    }
    return data;
  }

  window.OpsClient = { OPS, call };
})();
```

- [ ] **Step 2: 验证语法**

Run: `node --check projects/aios-workstudio/Console/demo/api.js`
Expected: 无输出（语法通过）

---

### Task 24: 改写 `app.js` 真调 + 收敛 `data.js`

**Files:**
- Create: `projects/aios-workstudio/Console/demo/app.js`（整体重写）
- Create: `projects/aios-workstudio/Console/demo/data.js`（整体重写）
- Modify: `projects/aios-workstudio/Console/demo/index.html`（引入 `api.js`）

- [ ] **Step 1: 写 `data.js`（IA 常量，无禁词）**

> 关键：**删除** 旧 `ESCAPE_LINKS` 中的 `Temporal`/`Neo4j` 字样——它们命中 `test_scaffold` 的 `FORBIDDEN`。

```js
/* Platform Console 静态 IA 常量。运行数据一律经 /hub/v1/ops/* 获取。 */
(() => {
  "use strict";

  window.ConsoleFixtures = {
    TENANT_ID: "t-hengchuan",
    ACTOR_ID: "cowen.hua",
    TRACK: "pipaw",
    PAGES: [
      { id: "overview", label: "总览", hint: "健康与租户" },
      { id: "integrate", label: "集成", hint: "协议契约 · dry-run" },
      { id: "control", label: "管控", hint: "剖面矩阵 · 禁令" },
      { id: "ontology", label: "本体", hint: "责任图 · 校验" },
      { id: "mesh", label: "网格", hint: "能力 · 连接器 · MCP" },
      { id: "govern", label: "治理", hint: "审计 · Skill · 制品" },
      { id: "run", label: "运行", hint: "任务 · 口径 · 模型路由" },
      { id: "publish", label: "发布", hint: "ChangeSet 队列" },
    ],
    ROLES: [
      { id: "platform_admin", label: "平台管理员" },
      { id: "operator", label: "运营指挥" },
      { id: "sre", label: "SRE" },
      { id: "frontline", label: "一线员工", locked: true },
    ],
    LOCK_MESSAGE: "看不到 /console：Platform Console 仅面向平台管理员 / 运营指挥 / SRE。",
    CONTRACT_NOTES: {
      I05: "I-05 · 写能力只在运行态经连接器幂等落地，场景态一律拒绝。",
      autoApply: "配置变更必须出草案，auto_apply 恒为 false。",
    },
  };
})();
```

- [ ] **Step 2: 写 `app.js`（fetch 渲染 8 页）**

```js
/* Platform Console：真调 hub.ops.*，按 X-Ops-Role 决定剖面。 */
(() => {
  "use strict";

  const F = window.ConsoleFixtures;
  const { call } = window.OpsClient;

  window.ConsoleState = {
    tenantId: F.TENANT_ID,
    actorId: F.ACTOR_ID,
    track: F.TRACK,
    role: "platform_admin",
    page: "overview",
    cache: {},
  };
  const state = window.ConsoleState;

  const $ = (sel) => document.querySelector(sel);
  const esc = (v) => String(v == null ? "" : v).replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

  function table(cols, rows) {
    if (!rows || !rows.length) return '<p class="muted">暂无数据</p>';
    const head = cols.map((c) => `<th>${esc(c.label)}</th>`).join("");
    const body = rows.map((r) =>
      `<tr>${cols.map((c) => `<td>${esc(c.get(r))}</td>`).join("")}</tr>`).join("");
    return `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
  }

  function card(title, body) {
    return `<section class="card"><h3>${esc(title)}</h3>${body}</section>`;
  }

  const RENDERERS = {
    async overview() {
      const [t, h] = await Promise.all([call("tenantGet"), call("healthSummary")]);
      return card("租户", `<pre>${esc(JSON.stringify(t.tenant, null, 2))}</pre>`) +
        card("三平面健康", `<pre>${esc(JSON.stringify(h, null, 2))}</pre>`);
    },
    async integrate() {
      const [reg, ctr] = await Promise.all([call("protocolRegistry"), call("protocolContracts")]);
      return card("模块协议契约（M1–M24）",
        table(
          [{ label: "模块", get: (m) => m.id }, { label: "名称", get: (m) => m.name },
           { label: "决策", get: (m) => m.decision }, { label: "端口", get: (m) => m.port || "-" }],
          reg.modules)) +
        card("集成验收矩阵", table(
          [{ label: "编号", get: (m) => m.id }, { label: "条目", get: (m) => m.title },
           { label: "判据", get: (m) => m.check }], ctr.matrix)) +
        card("契约提示", `<p>${esc(F.CONTRACT_NOTES.I05)}</p><p>${esc(F.CONTRACT_NOTES.autoApply)}</p>`);
    },
    async control() {
      const m = await call("profileMatrix");
      const sim = await call("policySimulate", { body: { operation: "cs.visit.schedule" } });
      return card("剖面矩阵", `<pre>${esc(JSON.stringify(m.profiles, null, 2))}</pre>`) +
        card("判定序试运行（不执行）", `<pre>${esc(JSON.stringify(sim, null, 2))}</pre>`) +
        card("禁令", `<p>${esc(F.CONTRACT_NOTES.autoApply)}</p>`);
    },
    async ontology() {
      const [g, v, d] = await Promise.all([call("graphGet", { body: {} }),
        call("graphValidate", { body: {} }), call("lawDiff", { body: {} })]);
      return card("责任图", table(
        [{ label: "节点", get: (n) => n.node_id }, { label: "指标", get: (n) => (n.kpi || {}).name },
         { label: "is", get: (n) => (n.kpi || {}).is }, { label: "ought", get: (n) => (n.kpi || {}).ought },
         { label: "状态", get: (n) => (n.kpi || {}).status }], g.nodes)) +
        card("五件套校验", `<pre>${esc(JSON.stringify(v, null, 2))}</pre>`) +
        card("法则包差异", `<pre>${esc(JSON.stringify(d, null, 2))}</pre>`);
    },
    async mesh() {
      const [r, c, s] = await Promise.all([call("registryList"),
        call("connectorList"), call("schemaDrift")]);
      return card("能力注册表", table(
        [{ label: "操作", get: (o) => o.operation }, { label: "审批", get: (o) => o.approval_level },
         { label: "副作用", get: (o) => (o.side_effects || []).join(",") || "-" }], r.operations)) +
        card("连接器", table(
          [{ label: "ID", get: (x) => x.id }, { label: "类型", get: (x) => x.type || "-" },
           { label: "启用", get: (x) => String(x.enabled) }], c.connectors)) +
        card("Schema 漂移", `<pre>${esc(JSON.stringify(s, null, 2))}</pre>`);
    },
    async govern() {
      const [iam, sk, art] = await Promise.all([call("iamBindings"),
        call("skillList"), call("artifactList")]);
      return card("IAM 绑定", table(
        [{ label: "主体", get: (b) => b.actor_id }, { label: "岗位", get: (b) => b.position_id }],
        iam.bindings)) +
        card("Skill 状态机", table(
          [{ label: "技能", get: (x) => x.skill_id }, { label: "状态", get: (x) => x.state }],
          sk.skills)) +
        card("制品", table(
          [{ label: "制品", get: (a) => a.artifact_id }, { label: "类型", get: (a) => a.kind }],
          art.artifacts));
    },
    async run() {
      const [t, cal, kg, mr] = await Promise.all([call("runtimeTask"),
        call("caliberStatus"), call("kgIngestStatus"), call("modelRoute")]);
      return card("任务", table(
        [{ label: "任务", get: (x) => x.task_id }, { label: "状态", get: (x) => x.status }], t.tasks)) +
        card("口径状态", `<pre>${esc(JSON.stringify(cal, null, 2))}</pre>`) +
        card("知识摄入", `<pre>${esc(JSON.stringify(kg, null, 2))}</pre>`) +
        card("模型路由", `<pre>${esc(JSON.stringify(mr, null, 2))}</pre>`);
    },
    async publish() {
      const cs = await call("changesetList");
      return card("ChangeSet 队列",
        table([{ label: "草案", get: (c) => c.changeset_id }, { label: "状态", get: (c) => c.status },
          { label: "自动应用", get: (c) => String(c.auto_apply) }], cs.changesets)) +
        card("契约", `<p>${esc(F.CONTRACT_NOTES.autoApply)}</p>`) +
        card("提交草案", `<button data-act="changeset-submit">提交一条草案</button>`);
    },
  };

  function toast(msg, ok) {
    const stack = $("#toast-stack");
    const el = document.createElement("div");
    el.className = "toast" + (ok ? "" : " bad");
    el.textContent = msg;
    stack.appendChild(el);
    setTimeout(() => el.remove(), 4200);
  }

  function bindPageEvents() {
    document.querySelectorAll("[data-act]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await call("changesetSubmit", { body: { kind: "console-manual" } });
          toast("草案已提交（auto_apply=false）", true);
          render();
        } catch (e) {
          toast(e.payload ? e.payload.message : e.message, false);
        }
      });
    });
  }

  async function render() {
    const main = $("#main");
    main.innerHTML = '<p class="muted">加载中…</p>';
    try {
      main.innerHTML = await RENDERERS[state.page]();
      bindPageEvents();
    } catch (e) {
      const msg = e.payload ? e.payload.message : e.message;
      main.innerHTML = card("降级", `<p class="bad">${esc(msg)}</p>
        <p class="muted">${esc(F.CONTRACT_NOTES.I05)}</p>`);
    }
  }

  function renderRail() {
    $("#rail-nav").innerHTML = F.PAGES.map((p) =>
      `<button class="rail-link${p.id === state.page ? " on" : ""}" data-page="${p.id}">
        <strong>${esc(p.label)}</strong><small>${esc(p.hint)}</small></button>`).join("");
    document.querySelectorAll(".rail-link").forEach((b) =>
      b.addEventListener("click", () => { state.page = b.dataset.page; renderRail(); render(); }));
  }

  function applyRole() {
    const role = $("#role-select").value;
    state.role = role;
    const locked = (F.ROLES.find((r) => r.id === role) || {}).locked;
    $("#lock-overlay").hidden = !locked;
    $("#shell").hidden = !!locked;
    if (locked) toast(F.LOCK_MESSAGE, false);
    else render();
  }

  function boot() {
    $("#tenant-chip").textContent = state.tenantId;
    const sel = $("#role-select");
    sel.innerHTML = F.ROLES.map((r) => `<option value="${r.id}">${esc(r.label)}</option>`).join("");
    sel.value = state.role;
    sel.addEventListener("change", applyRole);
    $("#lock-overlay").hidden = true;
    renderRail();
    render();
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
```

- [ ] **Step 3: `index.html` 引入 `api.js`**

在 `./data.js` 之前插入一行：

```html
  <script src="./api.js"></script>
  <script src="./data.js"></script>
```

- [ ] **Step 4: 语法与禁词自检**

Run:
```bash
node --check projects/aios-workstudio/Console/demo/app.js && \
node --check projects/aios-workstudio/Console/demo/data.js && \
cd projects/aios-workstudio && python - <<'PY'
from pathlib import Path
js = (Path("Console/demo/app.js").read_text(encoding="utf-8")
      + Path("Console/demo/data.js").read_text(encoding="utf-8"))
for s in ("看不到 /console", "I-05", "auto_apply"):
    assert s in js, s
for s in ("cubejs","graphiti","neo4j","langgraph","temporal","lethe","workflow_id","CubeQL",
          "invoke_cs","/hub/v1/kg/ingest","CollectionBlockModel"):
    assert s not in js, s
print("console clean")
PY
```
Expected: `console clean`

---

### Task 25: `run.py` 同源静态托管 + 首屏 seed

**Files:**
- Modify: `projects/aios-workstudio/CapabilityHub/run.py`

- [ ] **Step 1: 写实现**

```python
#!/usr/bin/env python3
"""启动 WorkStudio Capability Hub：/hub/v1 API + Console 同源静态托管（免 CORS）。"""

from __future__ import annotations

import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(REPO / "services" / "hub-api"))

import uvicorn  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

from capability_hub.facade import CapabilityHub  # noqa: E402
from capability_hub.http_app import create_app  # noqa: E402

CONSOLE_DIR = PKG.parent / "Console" / "demo"


def seed(ch: CapabilityHub) -> None:
    """单会话演示：责任图 + 一条 ChangeSet 草案 + 若干审计，保证首屏非空。"""
    from uas_hub.errors import Envelope

    env = Envelope("t-hengchuan", "cowen.hua", "builder", "pipaw")
    draft = ch.evolution_draft(env, {"kind": "seed-bootstrap", "note": "首屏草案"})
    ch.core.audit.append(
        {"operation": "hub.ops.seed", "tenant_id": env.tenant_id,
         "changeset_id": draft["changeset_id"], "profile": "builder"}
    )
    ch.core.skill_transition(env, "skill.visit", "previewed")


def main() -> None:
    ch = CapabilityHub.from_repo()
    seed(ch)
    app = create_app(ch)
    if CONSOLE_DIR.is_dir():
        app.mount("/console", StaticFiles(directory=str(CONSOLE_DIR), html=True), name="console")
    uvicorn.run(app, host="127.0.0.1", port=18088)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 验证 seed 幂等（不写库、不落文件）**

Run: `cd projects/aios-workstudio/CapabilityHub && python -c "import sys; sys.path[:0]=['.','../../services/hub-api']; import run; from capability_hub.facade import CapabilityHub; ch=CapabilityHub.from_repo(); run.seed(ch); print(ch.core.audit[-1]['operation'], ch.evolution.list()[0]['auto_apply'], ch.skill.list())"`
Expected: `hub.ops.seed False [{'skill_id': 'skill.visit', 'state': 'previewed'}]`

---

### Task 26: `test_scaffold.py` 改断言（Console 调 ops + `ops/**` 禁词）

**Files:**
- Modify: `projects/aios-workstudio/tests/test_scaffold.py`
- Test: 自身

- [ ] **Step 1: 替换 `test_console_demo_is_ops_shell` 并新增 ops 禁词例**

```python
    def test_console_demo_is_ops_shell(self) -> None:
        demo = ROOT / "Console" / "demo"
        for name in ("index.html", "console.css", "data.js", "app.js", "api.js"):
            self.assertTrue((demo / name).is_file(), name)
        html = (demo / "index.html").read_text(encoding="utf-8")
        js = ((demo / "app.js").read_text(encoding="utf-8")
              + (demo / "data.js").read_text(encoding="utf-8")
              + (demo / "api.js").read_text(encoding="utf-8"))
        self.assertIn("Platform Console", html)
        self.assertIn("/hub/v1/ops/", js)
        self.assertIn("/hub/v1/ops/policy/simulate", js)
        self.assertIn("看不到 /console", js)
        self.assertIn("I-05", js)
        self.assertIn("auto_apply", js)
        self.assertNotIn("invoke_cs", js)
        self.assertNotIn("/hub/v1/kg/ingest", js)
        self.assertNotIn("CollectionBlockModel", js)
        for noun in FORBIDDEN:
            self.assertNotIn(noun, js, noun)

    def test_ops_package_has_no_part_nouns(self) -> None:
        ops_dir = ROOT / "CapabilityHub" / "capability_hub" / "ops"
        files = sorted(ops_dir.rglob("*.py"))
        self.assertTrue(files, ops_dir)
        blob = "".join(p.read_text(encoding="utf-8") for p in files)
        for noun in FORBIDDEN:
            self.assertNotIn(noun, blob, noun)
        for noun in ("invoke_cs", "/hub/v1/kg/ingest", "CollectionBlockModel", "plugin-ai", "mcp-server"):
            self.assertNotIn(noun, blob, noun)
```

- [ ] **Step 2: 运行**

Run: `cd projects/aios-workstudio && python -m unittest tests.test_scaffold -v`
Expected: `test_console_demo_is_ops_shell`、`test_ops_package_has_no_part_nouns` 及其余 5 例全 PASS（此前 `test_console_demo_is_ops_shell` FAIL）

---

### Task 27: 端到端验收

- [ ] **Step 1: 启动**

Run: `cd projects/aios-workstudio/CapabilityHub && python run.py`（后台运行）
Expected: uvicorn 监听 `127.0.0.1:18088`

- [ ] **Step 2: 逐条核对 V1–V5**

| 验收 | 命令 | 期望 |
|---|---|---|
| V1 | `python scripts/validate_uas_aios_phase_a.py` | `OK` |
| V2 | `python -c "import sys;sys.path.insert(0,'services/hub-api');from uas_hub.protocol_catalog import validate_registry;print(validate_registry())"` | `[]` |
| V3 | `curl -s -H "X-Tenant-Id: t-hengchuan" -H "X-Ops-Role: platform_admin" http://127.0.0.1:18088/hub/v1/ops/protocol/registry` | 含 `"modules"`，24 条 |
| V4 | `cd projects/aios-workstudio && python -m unittest tests.test_scaffold -v` | 全 PASS |
| V5 | `curl -s -o /dev/null -w "%{http_code}" -H "X-Tenant-Id: t-hengchuan" -H "X-Ops-Role: frontline" http://127.0.0.1:18088/hub/v1/ops/tenant/get` | `403` |

- [ ] **Step 3: 浏览器核对 Console**

打开 `http://127.0.0.1:18088/console/index.html`，切到「一线员工」角色 → 出现锁页；切回「平台管理员」→ 8 页均渲染真实数据。

- [ ] **Step 4: 停服**

停止后台 uvicorn 进程。

---

## 交付清单（与规格 §9.1 对齐）

```
configs/protocol/registry.json                 ← M1–M24 集成交互契约
configs/protocol/KERNEL.yaml                   ← 内核声明
configs/accountability_graph.sample.json       ← 衡川 LTC 责任图
configs/metrics/osi/kpi-visit-dwell.yml        ← 口径定义
configs/gate_map.json                          ← L1–L3 门禁映射
configs/capability_registry.json               ← +cs.visit.list/schedule, cs.metric.query
projects/aios-workstudio/demo/hub-pack-open.fixture.{json,js}
projects/aios-workstudio/CapabilityHub/capability_hub/ops/*.py
projects/aios-workstudio/CapabilityHub/capability_hub/http_app.py
projects/aios-workstudio/CapabilityHub/run.py
projects/aios-workstudio/CapabilityHub/tests/{test_ops_endpoints,test_protocol_registry}.py
services/hub-api/uas_hub/adapters/*.py          ← 只读方法（纯增量）
services/hub-api/tests/test_fixture_readonly.py
projects/aios-workstudio/Console/demo/{api.js,app.js,data.js,index.html}
projects/aios-workstudio/packages/hub-client/src/ops.ts
projects/aios-workstudio/tests/test_scaffold.py
```

## 不做（与规格 §9.2 对齐）

- 不建第二套 API 进程 · 不实现真实 Cube/时态图/外环/记忆零件 · 不碰 `asui-cli/` 等有意删除内容
- 不接真实 CRM / IdP · 不改 `hub.core` 既有行为 · **不执行 git commit / 分支操作**
