# Spec-1 TA-1 可经营 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 WorkStudio Demo 真连 `hub.scene.*`：打开首页见到 `an-stage-visit` gate，scene 写 403+人话，签发停在 `issued`（不启工作流）。

**Architecture:** 浏览器 `:18090/demo` → 原生 `hub-scene.js`（路径与 `scene.ts` 冻结一致）→ CapabilityHub `:18088`（入口强制 `profile=scene`）→ `uas_hub.Hub`。Hub 从 `accountability_graph.sample.json` + Registry + `IamPort.position_of` 水合切片。Hub 不可达时保留现有 LTC 夹具并显示降级条。

**Tech Stack:** Python 3.11+ / FastAPI / unittest；Demo 原生 JS + `fetch`；不引入 Next/零件 SDK。

**依从规格：** [`docs/superpowers/specs/2026-09-12-aios-workstudio-modules-design.md`](../specs/2026-09-12-aios-workstudio-modules-design.md) §9 + 缺口 G1–G8、G10。

**硬约束：**
- 关闭 G1–G8、G10。**不要**实现 33 个 `hub.ops.*`、NocoBase、真 Temporal、Console 改皮肤。
- `ops/**` 本计划不新建。
- **不执行 git commit**（用户未要求）。每任务以回归验证收尾。
- 工作目录：仓库根 `UAS-AIOS`。Windows 用 PowerShell；命令里的路径用正斜杠。

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `configs/metrics/osi/kpi-visit-dwell.yml` | 口径定义，供 `FixtureCube._load_osi` |
| `configs/accountability_graph.sample.json` | `Hub.from_repo` 唯一图源，含 `an-stage-visit` |
| `configs/capability_registry.json` | 追加 `cs.visit.list/schedule`、`cs.metric.query` |
| `configs/gate_map.json` | L1–L3 → 门禁；`test_phase_a` 存在性断言 |
| `configs/protocol/registry.json` | 从规格附录 A **原样**落盘 |
| `configs/protocol/KERNEL.yaml` | 从规格附录 B **原样**落盘 |
| `services/hub-api/uas_hub/ports.py` | 再导出 `OuterLoopPort`（G8） |
| `services/hub-api/uas_hub/hub.py` | `pack_open` 调 `iam.position_of`（I-10） |
| `projects/aios-workstudio/CapabilityHub/capability_hub/http_app.py` | `_envelope` 忽略 `X-Profile` |
| `projects/aios-workstudio/demo/hub-pack-open.fixture.json` | `scripts/export_hub_pack_open.py` 产出 |
| `projects/aios-workstudio/demo/hub-scene.js` | 原生北向客户端，路径对齐 `scene.ts` |
| `projects/aios-workstudio/demo/workstudio.js` | 启动 `packOpen`；失败降级条 |
| `projects/aios-workstudio/demo/index.html` | 引入 `hub-scene.js` |
| `services/hub-api/tests/test_phase_a.py` | 追加 I-10 |
| `projects/aios-workstudio/CapabilityHub/tests/test_http.py` | 追加伪造 profile 被忽略 |
| `projects/aios-workstudio/tests/test_scaffold.py` | Demo 含 `/hub/v1/scene/pack/open` |

产品路径 `packages/workstudio-web` **已接** `scene.ts`，本计划不改 Vite 壳。P0 验收面是 `demo/index.html`。

---

### Task 1: 口径 OSI 定义

**Files:**
- Create: `configs/metrics/osi/kpi-visit-dwell.yml`

- [ ] **Step 1: 写文件**

`FixtureCube._load_osi` 只认以 `id:` / `formula:` 开头的行（`adapters/cube.py:16-31`）。

```yaml
id: kpi-visit-dwell
name: 阶段停留天数
unit: day
formula: now - stage_entered_at
source: crm.opportunity.stage_entered_at
grain: day
```

- [ ] **Step 2: 验证解析**

Run:

```
python -c "import sys; sys.path.insert(0,'services/hub-api'); from pathlib import Path; from uas_hub.adapters.cube import _load_osi; print(_load_osi(Path('configs/metrics/osi')))"
```

Expected: `{'kpi-visit-dwell': 'now - stage_entered_at'}`

---

### Task 2: 衡川 LTC 责任图样例

**Files:**
- Create: `configs/accountability_graph.sample.json`
- Test: `services/hub-api/tests/test_phase_a.py`（既有，依赖本文件）

约束（`test_phase_a.py` + schema）：`graph_id=ag-hengchuan-ltc`；`pack=cm`；`an-stage-visit` 的 `org.position_id=pos-cm`；`kpi.status=gate`；`kpi.is=28`、`ought=14`、`kpi_id=kpi-visit-dwell`；`process.cs_write=["cs.visit.schedule"]`；五维齐全；`kpi.caliber` 存在；`object_refs` 含 `UEC-10293`。

- [ ] **Step 1: 写文件**

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

- [ ] **Step 2: 确认 Hub 能加载**

Run:

```
python -c "import sys; sys.path.insert(0,'services/hub-api'); from uas_hub.hub import Hub; h=Hub.from_repo(); print(h.graphs.get('ag-hengchuan-ltc')['graph_id'])"
```

Expected: `ag-hengchuan-ltc`（若下一步 Registry 缺 `cs.visit`，本步只要不抛 `FileNotFoundError`）

---

### Task 3: 能力目录补 cs.visit / cs.metric

**Files:**
- Modify: `configs/capability_registry.json`（在 `cs.process` 对象后追加 `,` 再贴两个服务）
- Test: `services/hub-api/tests/test_phase_a.py::test_write_ops_hidden_in_scene`

`list_for_profile` 对 scene 会丢掉带 `side_effects` 的操作。因此 `list`/`query` 的 `side_effects` 必须 `[]`，`schedule` 必须非空。

- [ ] **Step 1: 在 `services` 数组末尾追加**

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
      "input": { "type": "object", "properties": { "owner_id": { "type": "string" }, "overdue_only": { "type": "boolean" } } },
      "output": { "type": "object", "properties": { "items": { "type": "array" } } },
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
      "input": { "type": "object", "required": ["customer_id"], "properties": { "customer_id": { "type": "string" }, "when": { "type": "string" } } },
      "output": { "type": "object", "properties": { "visit_id": { "type": "string" } } },
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
      "description": "按口径查询 KPI 当前值",
      "input": { "type": "object", "required": ["kpi_id"], "properties": { "kpi_id": { "type": "string" } } },
      "output": { "type": "object", "properties": { "value": { "type": ["number", "null"] }, "caliber_id": { "type": "string" }, "stale": { "type": "boolean" } } },
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

- [ ] **Step 2: 验证 scene 隐藏写工具**

Run:

```
python -c "import sys; sys.path.insert(0,'services/hub-api'); from pathlib import Path; from uas_hub.registry import Registry; r=Registry.from_file(Path('configs/capability_registry.json')); print([n for n in r.list_for_profile('scene') if n.startswith('cs.visit') or n.startswith('cs.metric')])"
```

Expected: `['cs.metric.query', 'cs.visit.list']`（不含 `cs.visit.schedule`）

---

### Task 4: gate_map.json

**Files:**
- Create: `configs/gate_map.json`
- Test: `services/hub-api/tests/test_phase_a.py::test_schema_files_exist`

口径：ARCHITECTURE_SPEC §10 附近 L1→G1/G4；L2→G1/G4/G6；L3→G6/G7。本任务只要求文件存在且三档齐全。

- [ ] **Step 1: 写文件**

```json
{
  "version": "1.0.0",
  "updated_at": "2026-09-12T00:00:00Z",
  "approval_gate_mapping": {
    "L1": { "description": "自动执行：只读与低风险写", "gates": ["G1", "G4"], "human_confirm": false },
    "L2": { "description": "需用户或主管确认后执行", "gates": ["G1", "G4", "G6"], "human_confirm": true },
    "L3": { "description": "禁止 Agent 自主执行或需双人审批", "gates": ["G6", "G7"], "human_confirm": true, "dual_control": true }
  },
  "charter_gates": [
    { "id": "G0", "name": "意图显式" },
    { "id": "G1", "name": "租户隔离" },
    { "id": "G4", "name": "剖面/能力可见" },
    { "id": "G6", "name": "审批与证据" },
    { "id": "G7", "name": "审计闭环" }
  ]
}
```

- [ ] **Step 2: 验证**

Run: `python -c "import json; print(list(json.load(open('configs/gate_map.json',encoding='utf-8'))['approval_gate_mapping']))"`

Expected: `['L1', 'L2', 'L3']`

---

### Task 5: 协议注册表 + KERNEL（G2）

**Files:**
- Create: `configs/protocol/registry.json`
- Create: `configs/protocol/KERNEL.yaml`
- Test: `services/hub-api/tests/test_protocol_registry.py`

- [ ] **Step 1: 原样复制规格附录**

从 `docs/superpowers/specs/2026-09-12-aios-workstudio-modules-design.md`：
- 附录 A 的 JSON（**无注释**）→ `configs/protocol/registry.json`
- 附录 B 的 YAML → `configs/protocol/KERNEL.yaml`

不要手改 `policy_order`。M2–M6 必须 `decision=own` 且 `replaceable=false`。

- [ ] **Step 2: 跑协议测试（预期先红若文件缺失，复制后应绿）**

Run: `python -m unittest services.hub-api.tests.test_protocol_registry -v`

若导入失败，改用：

```
python -m unittest discover -s services/hub-api/tests -p "test_protocol_registry.py" -v
```

Expected: `test_validate_clean` PASS（`validate_registry()==[]`）；`test_twenty_four_modules` PASS；`test_l0_not_replaceable` PASS；`test_policy_order_matches_chain` PASS。

---

### Task 6: OuterLoopPort 再导出（G8）

**Files:**
- Modify: `services/hub-api/uas_hub/ports.py`
- Test: 新建断言放在 `services/hub-api/tests/test_protocol_registry.py` 末尾

`OuterLoopPort` **已存在**于 `uas_hub/outer_loop.py`。不要复制一份 Protocol。本任务只让 `ports.py` 再导出，关闭规格 G8。

- [ ] **Step 1: 写失败测试**

在 `test_protocol_registry.py` 增加：

```python
    def test_outer_loop_port_exported(self) -> None:
        from uas_hub.ports import OuterLoopPort  # noqa: F401
        from uas_hub.protocol_catalog import REQUIRED_PORTS
        self.assertIn("OuterLoopPort", REQUIRED_PORTS)
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m unittest discover -s services/hub-api/tests -p "test_protocol_registry.py" -v`

Expected: FAIL `ImportError: cannot import name 'OuterLoopPort'`（在 Step 1 文件已保存且 ports 未改时）

- [ ] **Step 3: 最小实现**

在 `ports.py` 文件底部追加：

```python
from uas_hub.outer_loop import OuterLoopPort as OuterLoopPort
```

- [ ] **Step 4: 再跑测试**

Expected: `test_outer_loop_port_exported` PASS。

---

### Task 7: IAM 接入 pack_open（I-10 / G5）

**Files:**
- Modify: `services/hub-api/uas_hub/hub.py` `pack_open`（约 71–92 行）
- Test: `services/hub-api/tests/test_phase_a.py`

`FixtureIam` 已有 `("cowen.hua","t-hengchuan") → "pos-cm"`。`pack_open` 目前只看 `position_id` 参数，不看绑定。

- [ ] **Step 1: 写失败测试**

在 `test_phase_a.py` 的 `test_pack_open_slices_by_position` 之后追加：

```python
    def test_unbound_actor_cannot_open_pack(self) -> None:
        with self.assertRaises(HubError) as ctx:
            self.hub.pack_open(env(actor_id="nobody"), "pos-cm")
        self.assertEqual(ctx.exception.code, "SCOPE_DENIED")
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m unittest services.hub-api.tests.test_phase_a.PhaseATests.test_unbound_actor_cannot_open_pack -v`

若模块路径在 Windows 下失败，用：

```
python -m unittest discover -s services/hub-api/tests -p "test_phase_a.py" -v
```

Expected: 该例 FAIL（当前 `nobody` 仍能打开切片）或整文件因缺配置已绿/红混杂。Task 1–4 完成后本例必须 FAIL 于「未抛 SCOPE_DENIED」。

- [ ] **Step 3: 最小实现**

**必须先**走现有 `if not env.tenant_id` 与 `self.graphs.pack_open(...)`（未知租户继续 `TENANT_MISMATCH`，保住 `test_cross_tenant_forbidden`），**再**对成功切片做岗位绑定。

`pack_open` 改成：

```python
    def pack_open(self, env: Envelope, position_id: str, cube_ok: bool = True) -> dict[str, Any]:
        env.profile = "scene"
        if not env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        if not position_id:
            raise HubError("SCOPE_DENIED")
        env.position_id = position_id
        pack = self.graphs.pack_open(env.tenant_id, position_id, cube_ok=cube_ok)
        if self.iam is not None:
            bound = self.iam.position_of(env.actor_id, env.tenant_id)
            if not bound or bound != position_id:
                raise HubError("SCOPE_DENIED", "no position")
        if self.cube:
            for node in pack["nodes"]:
                kpi = dict(node.get("kpi") or {})
                kpi_id = kpi.get("kpi_id")
                if not kpi_id:
                    continue
                result = self.cube.query(str(kpi_id), available=cube_ok)
                kpi["is"] = result.get("value", kpi.get("is"))
                kpi["stale"] = bool(result.get("stale", not cube_ok))
                if result.get("caliber_id"):
                    kpi["caliber_id"] = result["caliber_id"]
                if result.get("as_of"):
                    kpi["as_of"] = result["as_of"]
                node["kpi"] = kpi
        return pack
```

`iam is None`（手工构造 Hub）时不挡切片。`nobody` + 已知租户：图能切开，随后因无绑定 `SCOPE_DENIED`。`cowen.hua` + `t-other`：仍在 `graphs.pack_open` 抛 `TENANT_MISMATCH`。`env.position_id = position_id` 同时关闭规格 G6（信封带岗位）。

不要把 IAM 插在 `graphs.pack_open` **之前**。

- [ ] **Step 4: 跑阶段 A**

Run: `python -m unittest discover -s services/hub-api/tests -p "test_phase_a.py" -v`

Expected: 全 PASS。`test_pack_open_renders_gate_node` 仍见 `an-stage-visit` + `kpi.status==gate`。`test_unbound_actor_cannot_open_pack` PASS。

---

### Task 8: CapabilityHub 忽略客户端 X-Profile（G7）

**Files:**
- Modify: `projects/aios-workstudio/CapabilityHub/capability_hub/http_app.py` `_envelope`（14–31 行）
- Test: `projects/aios-workstudio/CapabilityHub/tests/test_http.py`

`uas_hub/http_app.py` 的 `envelope()` **已经**用路径参数 `profile=`，忽略头。CapabilityHub 额外路由（`pack/list` 等）仍 `profile = header_profile or profile`。

- [ ] **Step 1: 写失败测试**

在 `CapabilityHub/tests/test_http.py` 追加：

```python
    def test_client_profile_header_ignored_on_pack_list(self) -> None:
        res = self.client.get(
            "/hub/v1/scene/pack/list",
            headers={**HDR, "X-Profile": "runtime"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(res.json()["packs"])
```

并追加 scene 写即使用户声称 runtime（走 **核心** 路由，确认仍 403）：

```python
    def test_scene_invoke_ignores_claimed_runtime_profile(self) -> None:
        res = self.client.post(
            "/hub/v1/scene/invoke_cs",
            headers={**HDR, "X-Profile": "runtime"},
            json={"operation": "cs.visit.schedule", "input": {"customer_id": "UEC-10293"}, "profile": "runtime"},
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()["error"]["code"], "PROFILE_FORBIDS_SIDE_EFFECT")
```

- [ ] **Step 2: 跑测试**

Run:

```
python -m unittest discover -s projects/aios-workstudio/CapabilityHub/tests -p "test_http.py" -v
```

Expected: `test_scene_invoke_ignores_claimed_runtime_profile` 应已 PASS（核心 `http_app` 路径强制）。`test_client_profile_header_ignored_on_pack_list` 在未改 `_envelope` 时仍可能 PASS（list 不校验 profile）。**真正要改的是 `_envelope` 不再读取 `x-profile`**，避免后续 Thread 绑定把客户端剖面写进去。

追加 Thread 用例（失败条件：改前会把 runtime 绑上 thread）：

```python
    def test_extra_scene_route_does_not_bind_client_profile(self) -> None:
        hdr = {**HDR, "X-Thread-Id": "th-ch-1", "X-Profile": "runtime"}
        listed = self.client.get("/hub/v1/scene/pack/list", headers=hdr)
        self.assertEqual(listed.status_code, 200, listed.text)
        opened = self.client.post(
            "/hub/v1/scene/pack/open",
            headers=hdr,
            json={"position_id": "pos-cm"},
        )
        self.assertEqual(opened.status_code, 200, opened.text)
```

改前：`pack/list` 经 CapabilityHub `_envelope` 把 thread 绑成 runtime，随后核心 `pack/open` 强制 scene → **409**。改后：两次都 200。

- [ ] **Step 3: 最小实现**

把 `_envelope` 改成：

```python
def _envelope(request: Request, hub: CapabilityHub, profile: str) -> Envelope:
    tenant = request.headers.get("x-tenant-id") or ""
    actor = request.headers.get("x-actor-id") or "anonymous"
    track = request.headers.get("x-track") or "pipaw"
    env = Envelope(
        tenant_id=tenant,
        actor_id=actor,
        profile=profile,
        track=track,
        correlation_id=request.headers.get("x-correlation-id") or "corr-http",
        idempotency_key=request.headers.get("idempotency-key") or "",
        thread_id=request.headers.get("x-thread-id"),
        position_id=None,
    )
    if env.thread_id:
        hub.core.bind_thread(env.thread_id, env.profile)
    return env
```

删除 `header_profile` 读取。不要改 `uas_hub/http_app.py` 的既有 `envelope()`（已经路径强制）。

- [ ] **Step 4: 再跑**

Expected: `test_http.py` 全 PASS；`test_extra_scene_route_does_not_bind_client_profile` 为 200 而非 409。

---

### Task 9: 导出场景夹具

**Files:**
- Generate: `projects/aios-workstudio/demo/hub-pack-open.fixture.json`
- Generate: `projects/aios-workstudio/demo/hub-pack-open.fixture.js`
- Test: `test_phase_a.py::test_scene_fixture_hides_write_and_keeps_gate`

脚本已存在：`scripts/export_hub_pack_open.py`。

- [ ] **Step 1: 运行导出**

Run: `python scripts/export_hub_pack_open.py`

Expected: 打印 `projects/aios-workstudio/demo/hub-pack-open.fixture.json`

- [ ] **Step 2: 跑阶段 A 夹具断言**

Run: `python -m unittest discover -s services/hub-api/tests -p "test_phase_a.py" -v`

Expected: `test_scene_fixture_hides_write_and_keeps_gate` PASS（`write_blocked.error.code=PROFILE_FORBIDS_SIDE_EFFECT`；`issued_task.workflow_id is None`）。

---

### Task 10: Demo 北向客户端（对齐 scene.ts）

**Files:**
- Create: `projects/aios-workstudio/demo/hub-scene.js`
- Modify: `projects/aios-workstudio/demo/index.html`（在 `workstudio.js` 前引入）
- Test: `projects/aios-workstudio/tests/test_scaffold.py`

Demo 是 `python -m http.server` 原生 JS，**不能** import `scene.ts`。客户端必须与 `packages/hub-client/src/scene.ts` 路径字面量一致。

- [ ] **Step 1: 写失败脚手架断言**

在 `test_scaffold.py` 的 `test_workstudio_client_has_no_part_sdk` 旁追加：

```python
    def test_workstudio_demo_calls_scene_pack_open(self) -> None:
        demo = ROOT / "demo"
        blob = (demo / "hub-scene.js").read_text(encoding="utf-8")
        html = (demo / "index.html").read_text(encoding="utf-8")
        self.assertIn("/hub/v1/scene/pack/open", blob)
        self.assertIn("/hub/v1/scene/insight/drill", blob)
        self.assertIn("/hub/v1/scene/task/issue", blob)
        self.assertIn("/hub/v1/policy/explain", blob)
        self.assertIn("hub-scene.js", html)
        self.assertNotIn("/hub/v1/ops/", blob)
        for noun in FORBIDDEN:
            self.assertNotIn(noun, blob, noun)
```

- [ ] **Step 2: 运行确认失败**

Run: `python -m unittest projects.aios-workstudio.tests.test_scaffold.ScaffoldTests.test_workstudio_demo_calls_scene_pack_open -v`

Expected: FAIL 找不到 `hub-scene.js`

- [ ] **Step 3: 写 `hub-scene.js`**

```javascript
(() => {
  "use strict";
  const DEFAULT = "http://127.0.0.1:18088";
  function headers() {
    return {
      "Content-Type": "application/json",
      "X-Tenant-Id": "t-hengchuan",
      "X-Actor-Id": "cowen.hua",
      "X-Track": "pipaw",
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
  window.HubScene = {
    packOpen: (position_id) => req("POST", "/hub/v1/scene/pack/open", { position_id }),
    insightDrill: (source_node_id, evidence_refs) =>
      req("POST", "/hub/v1/scene/insight/drill", { source_node_id, evidence_refs }),
    taskIssue: (body) => req("POST", "/hub/v1/scene/task/issue", body),
    explain: (code) => req("GET", "/hub/v1/policy/explain?code=" + encodeURIComponent(code)),
    invokeCs: (operation, input) =>
      req("POST", "/hub/v1/scene/invoke_cs", { operation, input }),
  };
})();
```

`index.html` 在 `workstudio.js` 之前加：

```html
<script src="./hub-scene.js"></script>
```

- [ ] **Step 4: 再跑脚手架**

Expected: `test_workstudio_demo_calls_scene_pack_open` PASS。`test_workstudio_client_has_no_part_sdk` 仍 PASS。

---

### Task 11: workstudio.js 启动 pack.open + 降级条

**Files:**
- Modify: `projects/aios-workstudio/demo/workstudio.js`（文件末尾 `render(false)` 附近）
- Modify: `projects/aios-workstudio/demo/workstudio.css`（仅加 `.hub-banner` 如需要）
- Test: `test_scaffold.py` 断言降级文案存在

视觉权威不变。Hub 成功：顶栏或 toast 出现 `an-stage-visit` + gate。Hub 失败：人话条「经营服务暂不可用，只读降级」，继续用 `ltc-workbench.js`。

- [ ] **Step 1: 脚手架断言**

```python
    def test_workstudio_demo_degrades_without_hub(self) -> None:
        js = (ROOT / "demo" / "workstudio.js").read_text(encoding="utf-8")
        self.assertIn("HubScene", js)
        self.assertIn("packOpen", js)
        self.assertIn("只读降级", js)
        self.assertIn("an-stage-visit", js)
```

Run: 该例 FAIL（尚无 `HubScene` 调用）。

- [ ] **Step 2: 最小接线**

在 `workstudio.js` 末尾 `render(false);` **之后**追加：

```javascript
(function bootHub() {
  const scene = window.HubScene;
  if (!scene) return;
  const bar = document.createElement("div");
  bar.id = "hub-banner";
  bar.setAttribute("role", "status");
  document.body.insertBefore(bar, document.body.firstChild);
  scene
    .packOpen("pos-cm")
    .then((pack) => {
      const visit = (pack.nodes || []).find((n) => n.node_id === "an-stage-visit");
      const st = visit && visit.kpi && visit.kpi.status;
      bar.textContent =
        st === "gate"
          ? "今日卡口 · 阶段拜访停留超 SLA（an-stage-visit）"
          : "作战台已连接 · " + ((pack.nodes || []).map((n) => n.node_id).join("、") || "无节点");
      bar.dataset.hub = "ok";
    })
    .catch((err) => {
      const msg = (err && err.error && err.error.message) || "经营服务暂不可用，只读降级";
      bar.textContent = msg.indexOf("降级") >= 0 ? msg : "经营服务暂不可用，只读降级。" + msg;
      bar.dataset.hub = "degraded";
    });
})();
```

需要时可在 `workstudio.css` 加：

```css
#hub-banner { padding: 0.4rem 1rem; font-size: 0.85rem; background: #111; color: #eee; }
#hub-banner[data-hub="degraded"] { background: #5c3d00; }
```

不要在一线菜单写连接器/零件名。不要 `fetch` `/hub/v1/ops/`。**不要**加「试写 CRM」按钮、不要自动 `invoke_cs`（A2 由 HTTP 测试覆盖）。

- [ ] **Step 3: 跑脚手架**

Run: `python -m unittest discover -s projects/aios-workstudio/tests -p "test_scaffold.py" -v`

Expected: 全 PASS。

---

### Task 12: 端到端回归

- [ ] **Step 1: hub-api 测试**

Run: `python -m unittest discover -s services/hub-api/tests -v`

Expected: 全 PASS（含 `test_http.py` 的 A2 scene 写 403、A1 pack.open gate、A12 同 Thread 409、issue `workflow_id is None`）。

- [ ] **Step 2: CapabilityHub 测试**

Run: `python -m unittest discover -s projects/aios-workstudio/CapabilityHub/tests -v`

Expected: 全 PASS。

- [ ] **Step 3: 脚手架**

Run: `python -m unittest discover -s projects/aios-workstudio/tests -v`

Expected: 全 PASS。

- [ ] **Step 4: 启动 Hub**

Run: `python projects/aios-workstudio/CapabilityHub/run.py`

Expected: uvicorn `127.0.0.1:18088`

另开终端：`cd projects/aios-workstudio` → `python -m http.server 18090`

- [ ] **Step 5: 浏览器 / curl**

Windows 用 `curl.exe`（PowerShell 的 `curl` 是 `Invoke-WebRequest`）。

```
curl.exe -s -H "X-Tenant-Id: t-hengchuan" -H "X-Actor-Id: cowen.hua" -H "X-Track: pipaw" -H "Content-Type: application/json" --data-raw "{\"position_id\":\"pos-cm\"}" http://127.0.0.1:18088/hub/v1/scene/pack/open
```

Expected: JSON 含 `"node_id": "an-stage-visit"`。

```
curl.exe -s -o - -w "\n%{http_code}" -H "X-Tenant-Id: t-hengchuan" -H "X-Actor-Id: cowen.hua" -H "X-Track: pipaw" -H "Content-Type: application/json" -d "{\"operation\":\"cs.visit.schedule\",\"input\":{\"customer_id\":\"UEC-10293\"}}" http://127.0.0.1:18088/hub/v1/scene/invoke_cs
```

Expected: HTTP 403，body `PROFILE_FORBIDS_SIDE_EFFECT`，`message` 含「签发」。

打开 `http://127.0.0.1:18090/demo/index.html`：顶栏出现今日卡口 / `an-stage-visit`，**不是**空白对话。停掉 `:18088` 后刷新：出现「只读降级」，LTC 夹具仍可用。

- [ ] **Step 6: 停服**

停掉 uvicorn 与 http.server。

---

## 本计划明确不做

- `capability_hub/ops/` 与 33 个 ops 端点（Spec-2）
- `exec.open` / Temporal / SSE 真闭环（Spec-3）
- Console `#/audit` 真连（Spec-2）
- NocoBase、Lethe、连接器轮换
- git commit

---

## 出站清单（对应规格 A1–A4、A12、I-02/I-05/I-10）

| 码 | 证明 |
|----|------|
| A1 | pack.open 含 `an-stage-visit` gate；Demo 顶栏 |
| A2 | scene `cs.visit.schedule` 403 + 人话 |
| A3 | issue 无 `source_node_id` → 422（既有 `test_task_requires_source_node`） |
| A4 | 无 evidence → 422（既有 `test_ungrounded_cannot_issue`） |
| A12 | `test_thread_profile_immutable_http` |
| I-02 | `test_node_requires_five_tuple` |
| I-05 | scene 工具列表无 schedule；call 仍 403 |
| I-10 | `test_unbound_actor_cannot_open_pack` |
| G2 | `validate_registry()==[]` |
| G8 | `from uas_hub.ports import OuterLoopPort` |
