# NocoBase Console 壳 + 三块 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用 NocoBase 做知识管理员可视化壳（本体 / 图谱 / 法则 / 口径），三个自定义块只调 `hub.ops.*`；拖改不落生产，发布只走 ChangeSet；图谱页无写 CRM。

**Architecture:** 真相仍在 Hub。NocoBase 只提供角色、侧栏、页面编排和表单底座；三块是 `BlockModel`（自拉 `hub-api`），**禁止** `CollectionBlockModel`。`/hub/v1/ops/*` 强制 `profile=builder`。NocoBase 主库不存 `ag_node` / episode / `kpi.is`。

**Tech Stack:** FastAPI Hub（已有）· NocoBase client-v2 Plugin + BlockModel · Cytoscape（责任图画布，模块设计已选）· unittest（与 `scripts/validate_uas_aios_phase_a.py` 同）+ 插件架构测试

**规格:** `docs/strategic/design/UAS_AIOS_PLATFORM_PRODUCT.md` §B2/B5/8.2 · 前序决策：NocoBase = Console 壳，不是数据核

---

## 现状（不要假设已有）

| 层 | 现状 |
|----|------|
| `hub.ops.*` | **未实现**。产品文档写了，`http_app.py` 只有 scene/explore/runtime |
| 责任图 / WM / KG | 内存夹具：`GraphStore`、`WmStore`、`FixtureKg` |
| ChangeSet | `FixtureEvolution.draft/apply`，无 ops 封装 |
| NocoBase | 本仓库 **无** 应用；compose 只有 Temporal |
| Console | REQ-UAS-AIOS-002 勾了定义，**工程未做** |

因此迭代顺序是：**先 Python `hub.ops`（curl 可测）→ 再 NocoBase 壳 → 再三块 → 最后发布纪律测试**。不要先搭 NocoBase 再倒逼 API。

---

## 文件地图

| 路径 | 职责 |
|------|------|
| `services/hub-api/uas_hub/ops.py` | 运营门面：graph/wm/law/kg/caliber/changeset；无 SoR 写 |
| `services/hub-api/uas_hub/http_app.py` | 挂 `/hub/v1/ops/*`，路径强制 `builder` |
| `services/hub-api/tests/test_ops_console.py` | ops 契约：缺维、禁 ingest、changeset、图谱无写 |
| `services/console-nocobase/README.md` | 本地启动：官方镜像 + 挂载插件 |
| `services/console-nocobase/packages/plugins/@uas/plugin-console/` | 唯一产品插件 |
| `.../src/server/plugin.ts` | 角色 `knowledge_admin`、插件黑名单、禁止经营 Collection |
| `.../src/server/deny.ts` | Workflow / AI / MCP 禁用清单 |
| `.../src/client-v2/plugin.tsx` | 侧栏四页 + 注册三块 |
| `.../src/client-v2/lib/hubOps.ts` | 唯一 fetch 客户端，信封 `profile=builder` |
| `.../src/client-v2/models/AccountabilityGraphBlock.tsx` | 块 1 |
| `.../src/client-v2/models/WmLifetimeBlock.tsx` | 块 2 |
| `.../src/client-v2/models/KgTimelineBlock.tsx` | 块 3 |
| `.../src/client-v2/models/ChangesetPublishAction.tsx` | 发布按钮，只调 submit |
| `services/console-nocobase/tests/architecture.test.ts` | 无 Collection 名、无 ingest、无 invoke_cs |
| `deploy/compose/docker-compose.yml` | 增加 `console-nocobase` 服务 |
| `configs/console/deny-plugins.json` | 黑名单权威（Hub 测试与插件共用语义） |

**明确不建：** NocoBase Collection `ag_nodes` / `episodes` / `kpis`；NocoBase Workflow；插件内 Graphiti/Cube SDK；`hub.ops.kg.ingest` 的 UI 入口。

---

## 迭代节奏（6 个切片，每片可单独验收）

```
W0  契约冻结     deny-plugins.json + ops 路径表 + 角色
W1  hub.ops 读   graph.get / wm.get / kg.search / caliber.status
W2  hub.ops 写草稿  graph.validate + changeset.submit（不 apply）
W3  NocoBase 壳   角色、侧栏、黑名单、空页
W4  块 1+2       责任图画布、WM 三寿命（可拖改，未发布）
W5  块 3+发布    时态浏览 + 发布按钮；图谱无 CRM
W6  门禁验收     架构测试 + 两周停用标准
```

W1–W2 不依赖 NocoBase，可在现有 unittest 完成。W3 起才碰 Node。

---

### Task 1: 冻结运营信封与禁令

**Files:**
- Create: `configs/console/deny-plugins.json`
- Create: `services/hub-api/tests/test_ops_console.py`（先写空类与常量）
- Modify: `services/hub-api/uas_hub/errors.py`（补 `OPS_ROLE_REQUIRED`）

- [ ] **Step 1: 写禁令配置**

```json
{
  "plugin_denylist": [
    "@nocobase/plugin-workflow",
    "@nocobase/plugin-workflow-request",
    "@nocobase/plugin-ai",
    "@nocobase/plugin-mcp-server",
    "@nocobase/plugin-ai-gigachat"
  ],
  "forbidden_collections": ["ag_node", "ag_graph", "episodes", "kpi_is"],
  "forbidden_client_paths": [
    "/hub/v1/instance/invoke_cs",
    "/hub/v1/scene/invoke_cs",
    "/hub/v1/kg/ingest"
  ]
}
```

- [ ] **Step 2: 错误码**

在 `ERROR_HTTP` / `EXPLAIN` 增加：

```python
"OPS_ROLE_REQUIRED": 403,  # http
# EXPLAIN
"OPS_ROLE_REQUIRED": {
    "message": "只有知识管理员能打开配置台。",
    "next": "用运营角色登录 /console",
},
```

- [ ] **Step 3: 提交**

```bash
git add configs/console/deny-plugins.json services/hub-api/uas_hub/errors.py
git commit -m "$(cat <<'EOF'
feat(console): freeze plugin denylist and ops error code

EOF
)"
```

---

### Task 2: `hub.ops` 读路径（W1）

**Files:**
- Create: `services/hub-api/uas_hub/ops.py`
- Modify: `services/hub-api/uas_hub/http_app.py`
- Modify: `services/hub-api/uas_hub/hub.py`（薄委托，不把逻辑堆进 http）
- Test: `services/hub-api/tests/test_ops_console.py`

Ops 强制 `profile=builder`，忽略客户端伪造的 `profile` 字段（与 scene 路由同一纪律）。

- [ ] **Step 1: 写失败测试**

```python
OPS_HDR = {
    "X-Tenant-Id": "t-hengchuan",
    "X-Actor-Id": "knowledge.admin",
    "X-Track": "pipaw",
    "X-Ops-Role": "knowledge_admin",
}

class OpsConsoleTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_app())

    def test_ops_graph_get_returns_five_tuple(self):
        res = self.client.get("/hub/v1/ops/graph", headers=OPS_HDR)
        self.assertEqual(res.status_code, 200, res.text)
        node = next(n for n in res.json()["nodes"] if n["node_id"] == "an-stage-visit")
        for key in ("goal", "org", "kpi", "process", "wm"):
            self.assertIn(key, node)
        self.assertEqual(res.json().get("profile"), "builder")

    def test_ops_ignores_claimed_runtime_profile(self):
        res = self.client.get(
            "/hub/v1/ops/graph",
            headers={**OPS_HDR, "X-Profile": "runtime"},
        )
        self.assertEqual(res.json().get("profile"), "builder")

    def test_ops_wm_get_three_lifetimes(self):
        res = self.client.get(
            "/hub/v1/ops/wm/wm-hengchuan-ltc", headers=OPS_HDR
        )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        for lt in ("draft", "compiled", "live"):
            self.assertIn(lt, body["lifetimes"])

    def test_ops_kg_search_readonly(self):
        res = self.client.post(
            "/hub/v1/ops/kg/search",
            headers=OPS_HDR,
            json={"object_ref": "UEC-10293"},
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertTrue(res.json()["episodes"])
        self.assertFalse(res.json().get("write_path"))

    def test_ops_kg_ingest_not_exposed(self):
        res = self.client.post(
            "/hub/v1/ops/kg/ingest",
            headers=OPS_HDR,
            json={"id": "ep-x", "object_ref": "UEC-10293"},
        )
        self.assertEqual(res.status_code, 404)

    def test_ops_caliber_status(self):
        res = self.client.get("/hub/v1/ops/caliber/status", headers=OPS_HDR)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIn("items", res.json())
```

- [ ] **Step 2: 跑测试确认失败**

```bash
cd services/hub-api
python -m unittest tests.test_ops_console
```

Expected: FAIL（404 / import ops）

- [ ] **Step 3: 实现 `ops.py` 最小读**

```python
# services/hub-api/uas_hub/ops.py
from __future__ import annotations
from typing import Any
from uas_hub.errors import Envelope, HubError

class OpsFacade:
    def __init__(self, hub: Any) -> None:
        self.hub = hub

    def _builder(self, env: Envelope, ops_role: str = "") -> Envelope:
        env.profile = "builder"
        if ops_role != "knowledge_admin":
            raise HubError("OPS_ROLE_REQUIRED")
        return env

    def graph_get(self, env: Envelope) -> dict[str, Any]:
        env = self._builder(env)
        graph = self.hub.graphs.get("ag-hengchuan-ltc")
        if not graph or graph.get("tenant_id") != env.tenant_id:
            raise HubError("TENANT_MISMATCH")
        from uas_hub.graph_store import node_incomplete
        nodes = []
        for node in graph["nodes"]:
            item = dict(node)
            item["_incomplete"] = node_incomplete(node)
            nodes.append(item)
        return {
            "graph_id": graph["graph_id"],
            "nodes": nodes,
            "edges": graph.get("edges") or [],
            "profile": "builder",
        }

    def wm_get(self, env: Envelope, world_model_id: str) -> dict[str, Any]:
        env = self._builder(env)
        lifetimes = {}
        for lt in ("draft", "compiled", "live"):
            try:
                lifetimes[lt] = self.hub.wm.get(world_model_id, lt)
            except HubError:
                lifetimes[lt] = None
        return {"world_model_id": world_model_id, "lifetimes": lifetimes, "profile": "builder"}

    def kg_search(self, env: Envelope, object_ref: str | None, query: str | None) -> dict[str, Any]:
        env = self._builder(env)
        found = self.hub.kg_search(env, object_ref, query)
        found["write_path"] = False
        found["profile"] = "builder"
        return found

    def caliber_status(self, env: Envelope) -> dict[str, Any]:
        env = self._builder(env)
        graph = self.graph_get(env)
        items = []
        for node in graph["nodes"]:
            kpi = node.get("kpi") or {}
            items.append({
                "kpi_id": kpi.get("kpi_id"),
                "caliber": kpi.get("caliber") or kpi.get("caliber_id"),
                "stale": bool((kpi.get("stale") if "stale" in kpi else False)),
            })
        return {"items": items, "profile": "builder"}
```

公开方法均增加 `ops_role: str`，内部调用 `_builder(env, ops_role)`。HTTP 层读 `X-Ops-Role`。

在 `create_app` 里：`ops = OpsFacade(hub)`。路由一律 `envelope(request, "builder")`，并把 `request.headers.get("x-ops-role")` 传入 `OpsFacade` 各方法。缺角色 → `OPS_ROLE_REQUIRED`。

不注册 `POST /hub/v1/ops/kg/ingest`。

- [ ] **Step 4: 跑测试通过**

```bash
python -m unittest tests.test_ops_console
```

Expected: PASS（本 Task 六个读用例）

- [ ] **Step 5: 提交**

```bash
git add services/hub-api/uas_hub/ops.py services/hub-api/uas_hub/http_app.py services/hub-api/tests/test_ops_console.py
git commit -m "$(cat <<'EOF'
feat(hub): add read-only hub.ops for console shell

EOF
)"
```

---

### Task 3: `hub.ops` 草稿与 ChangeSet（W2）

**Files:**
- Modify: `services/hub-api/uas_hub/ops.py`
- Modify: `services/hub-api/uas_hub/graph_store.py`（可选 `validate` 复用 `node_incomplete`）
- Modify: `services/hub-api/tests/test_ops_console.py`

写 = 把 patch 放进 changeset draft，**不**改 live 图、**不** `law.compile`、**不** `invoke_cs`。

- [ ] **Step 1: 写失败测试**

```python
    def test_graph_validate_flags_missing_wm(self):
        res = self.client.post(
            "/hub/v1/ops/graph/validate",
            headers=OPS_HDR,
            json={"nodes": [{"node_id": "an-x", "goal": {}, "org": {}, "kpi": {}, "process": {}, "wm": {}}]},
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["incomplete"])

    def test_changeset_submit_does_not_apply(self):
        res = self.client.post(
            "/hub/v1/ops/changeset/submit",
            headers={**OPS_HDR, "Idempotency-Key": "ops-1"},
            json={"kind": "graph", "patch": {"nodes": []}},
        )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["status"], "draft")
        self.assertFalse(body["auto_apply"])
        self.assertFalse(body["applied"])

    def test_graph_publish_is_alias_of_submit(self):
        res = self.client.post(
            "/hub/v1/ops/graph/publish",
            headers={**OPS_HDR, "Idempotency-Key": "ops-2"},
            json={"nodes": []},
        )
        self.assertEqual(res.json()["status"], "draft")

    def test_ops_cannot_invoke_cs(self):
        res = self.client.post(
            "/hub/v1/ops/invoke_cs",
            headers=OPS_HDR,
            json={"operation": "cs.visit.schedule"},
        )
        self.assertIn(res.status_code, (404, 405))
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m unittest tests.test_ops_console.OpsConsoleTests.test_changeset_submit_does_not_apply
```

- [ ] **Step 3: 实现 submit → `evolution.draft`，publish 同路径**

`graph/validate` 对每个 node 调 `node_incomplete`，返回 `incomplete: [{node_id, missing}]`。

`changeset/submit`：

```python
def changeset_submit(self, env: Envelope, kind: str, patch: dict) -> dict:
    env = self._builder(env)
    drafted = self.hub.evolution_draft(env, {"kind": kind, "patch": patch, "actor_id": env.actor_id})
    drafted["applied"] = False
    drafted["auto_apply"] = False
    return drafted
```

不调用 `evolution_apply`。`decide` 留到 W5（发布页确认）。

- [ ] **Step 4: 全绿后提交**

```bash
python -m unittest tests.test_ops_console
git add services/hub-api/uas_hub/ops.py services/hub-api/tests/test_ops_console.py
git commit -m "$(cat <<'EOF'
feat(hub): console edits submit changeset drafts only

EOF
)"
```

---

### Task 4: NocoBase 插件壳（W3）

**Files:**
- Create: `services/console-nocobase/README.md`
- Create: `services/console-nocobase/packages/plugins/@uas/plugin-console/package.json`
- Create: `.../src/server/deny.ts`
- Create: `.../src/server/plugin.ts`
- Create: `.../src/client-v2/plugin.tsx`
- Create: `.../src/client-v2/lib/hubOps.ts`
- Create: `.../src/client-v2/pages/{OntologyPage,GraphPage,LawPage,CaliberPage}.tsx`（先空壳）
- Create: `services/console-nocobase/tests/architecture.test.ts`
- Modify: `deploy/compose/docker-compose.yml`

NocoBase 用官方镜像，**不要** fork 内核。插件名 `@uas/plugin-console`。

- [ ] **Step 1: `hubOps.ts` — 唯一出口**

```ts
const HUB = (globalThis as { UAS_HUB_BASE?: string }).UAS_HUB_BASE || "http://127.0.0.1:18088";

export async function hubOps<T>(path: string, init: RequestInit = {}): Promise<T> {
  if (path.includes("invoke_cs") || path.includes("kg/ingest")) {
    throw new Error("console forbids write-path");
  }
  const res = await fetch(`${HUB}/hub/v1/ops${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      "X-Tenant-Id": sessionStorage.getItem("tenant_id") || "",
      "X-Actor-Id": sessionStorage.getItem("actor_id") || "",
      "X-Track": "pipaw",
      "X-Ops-Role": "knowledge_admin",
      ...(init.headers || {}),
    },
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
```

- [ ] **Step 2: 服务端黑名单**

```ts
// src/server/deny.ts
import denylist from "../../../../../configs/console/deny-plugins.json";

export function assertNoForbiddenPlugins(pm: { get: (n: string) => { enabled?: boolean } | undefined }) {
  for (const name of denylist.plugin_denylist) {
    const p = pm.get(name);
    if (p?.enabled) throw new Error(`forbidden plugin enabled: ${name}`);
  }
}

export function assertNoForbiddenCollections(db: { getCollection: (n: string) => unknown }) {
  for (const name of denylist.forbidden_collections) {
    if (db.getCollection(name)) throw new Error(`forbidden collection: ${name}`);
  }
}
```

`plugin.ts` 的 `load()`：`assertNoForbiddenPlugins`；注册角色 `knowledge_admin`；`acl.allow` 仅插件设置页，**不允许** collection CRUD。

- [ ] **Step 3: 侧栏四页**

在 `plugin.tsx`：

```ts
this.pluginSettingsManager.addMenuItem({ key: "uas-ontology", title: "本体", icon: "ApartmentOutlined" });
this.pluginSettingsManager.addMenuItem({ key: "uas-kg", title: "图谱", icon: "ShareAltOutlined" });
this.pluginSettingsManager.addMenuItem({ key: "uas-law", title: "法则", icon: "AuditOutlined" });
this.pluginSettingsManager.addMenuItem({ key: "uas-caliber", title: "口径", icon: "FundOutlined" });
```

四页先渲染标题 +「块将在此插入」。**不要** `addCollection`。

- [ ] **Step 4: 架构测试（Node）**

```ts
import denylist from "../../../configs/console/deny-plugins.json";
import fs from "fs";
import path from "path";

const src = fs.readFileSync(
  path.join(__dirname, "../packages/plugins/@uas/plugin-console/src/client-v2/lib/hubOps.ts"),
  "utf8",
);

test("hubOps forbids ingest and invoke_cs", () => {
  expect(src).toContain("kg/ingest");
  expect(src).toContain("console forbids write-path");
});

test("client models are BlockModel not CollectionBlockModel", () => {
  const modelsDir = path.join(__dirname, "../packages/plugins/@uas/plugin-console/src/client-v2/models");
  if (!fs.existsSync(modelsDir)) return;
  for (const f of fs.readdirSync(modelsDir)) {
    const t = fs.readFileSync(path.join(modelsDir, f), "utf8");
    expect(t).not.toMatch(/CollectionBlockModel/);
    expect(t).not.toMatch(/invoke_cs/);
  }
});
```

W3 时 models 目录可先空，测试 skip；W4 起强制。

- [ ] **Step 5: compose 服务（实验室）**

```yaml
  console-nocobase:
    image: nocobase/nocobase:latest
    environment:
      APP_KEY: lab
      DB_DIALECT: sqlite
      UAS_HUB_BASE: http://host.docker.internal:18088
    volumes:
      - ../../services/console-nocobase/packages/plugins/@uas/plugin-console:/app/storage/plugins/@uas/plugin-console
    ports:
      - "13000:80"
    profiles: ["console"]
```

用 `profiles: ["console"]`，默认 `compose up` **不**启动 NocoBase（避免拖进阶段 A）。启动：

```bash
docker compose -f deploy/compose/docker-compose.yml --profile console up -d
```

- [ ] **Step 6: 提交**

```bash
git add services/console-nocobase deploy/compose/docker-compose.yml
git commit -m "$(cat <<'EOF'
feat(console): scaffold NocoBase plugin shell with denylist

EOF
)"
```

---

### Task 5: 块 1 责任图投影画布（W4a）

**Files:**
- Create: `.../models/AccountabilityGraphBlock.tsx`
- Modify: `.../pages/OntologyPage.tsx`（默认放入该块）
- Modify: `services/console-nocobase/tests/architecture.test.ts`

- [ ] **Step 1: 块必须是 `BlockModel`，自拉 `hubOps("/graph")`**

画布：

- 节点 = 责任节点；边按 `kind` 过滤：`org_cascade | kpi_split | stage_split | object_drill`
- 缺维（沿用服务端 `_incomplete` 或再调 `/graph/validate`）红灯
- 选中节点：右侧 Formily 表单绑五件套（JSON Schema 用 `schemas/accountability_graph.schema.json` 的 `$defs.accountabilityNode`）
- 拖拽改 `parent_id` / 边 **只改本地 React state**
- 底栏：「提交变更」→ `POST /changeset/submit` `{kind:"graph", patch}`，按钮文案禁止「发布到生产」「写 CRM」

Cytoscape 仅在此块；不要引 ECharts 当第二套 KPI 模型（模块设计否决项）。

- [ ] **Step 2: 架构测试补断言**

```ts
test("graph block has no CRM write copy", () => {
  const t = fs.readFileSync(".../AccountabilityGraphBlock.tsx", "utf8");
  expect(t).not.toMatch(/写回 CRM|invoke_cs|cs\.visit/);
  expect(t).toMatch(/changeset\/submit/);
});
```

- [ ] **Step 3: 手工验收（无浏览器工具时 curl + 单测）**

```bash
curl -s -H "X-Tenant-Id: t-hengchuan" -H "X-Ops-Role: knowledge_admin" \
  http://127.0.0.1:18088/hub/v1/ops/graph | jq '.nodes|length'
```

Expected: ≥ 2。块加载后可见 `an-stage-visit` gate。

- [ ] **Step 4: 提交**

```bash
git commit -m "$(cat <<'EOF'
feat(console): accountability graph projection block

EOF
)"
```

---

### Task 6: 块 2 WM 三寿命对照（W4b）

**Files:**
- Create: `.../models/WmLifetimeBlock.tsx`
- Modify: `.../pages/LawPage.tsx`（寿命板 + 法则 diff 可同页上下）

- [ ] **Step 1: `GET /wm/wm-hengchuan-ltc` 三列 draft | compiled | live**

- 缺维清单（五维空字段）
- compiled 列只读；「改 compiled」按钮不渲染（builder 调 `hub.wm.patch(..., compiled)` 已被 Hub 拒，UI 不得提供入口）
- draft 可编辑 → 「提交变更」走 `changeset/submit` `{kind:"wm"}`
- 若已有 `GET /ops/law/diff`，同页展示；没有则 W4 只做三寿命，diff 放 W5

- [ ] **Step 2: 补测试 `test_ops_console.py`**

```python
    def test_ops_wm_patch_compiled_still_denied(self):
        res = self.client.patch(
            "/hub/v1/ops/wm/wm-hengchuan-ltc/compiled",
            headers=OPS_HDR,
            json={"laws": ["x"]},
        )
        self.assertEqual(res.status_code, 422)
```

实现：ops 的 PATCH compiled 直接 `raise HubError("INVARIANT_FAILED")`，与 `WmStore.patch` 一致。draft PATCH 仍只进 changeset，不写 store。

- [ ] **Step 3: 提交**

```bash
git commit -m "$(cat <<'EOF'
feat(console): world-model three-lifetime board

EOF
)"
```

---

### Task 7: 块 3 Graphiti 时态浏览 + 发布（W5）

**Files:**
- Create: `.../models/KgTimelineBlock.tsx`
- Create: `.../models/ChangesetPublishAction.tsx`
- Modify: `.../pages/GraphPage.tsx`
- Modify: `uas_hub/ops.py`（`changeset/decide`）
- Modify: tests

- [ ] **Step 1: 图谱页只读**

```tsx
// KgTimelineBlock: hubOps("/kg/search", { method:"POST", body: JSON.stringify({ object_ref }) })
// 展示 episode id / kind / summary / object_ref
// 禁止：ingest 按钮、CRM 按钮、invoke_cs
// 页脚固定文案：「只读时间线 · 生产写走作战台签发」
```

- [ ] **Step 2: 发布动作只在本体/法则页，不在图谱页**

```tsx
export class ChangesetPublishAction extends ActionModel {
  async handler() {
    await hubOps("/changeset/decide", {
      method: "POST",
      headers: { "Idempotency-Key": crypto.randomUUID() },
      body: JSON.stringify({ changeset_id, decision: "confirm" }),
    });
  }
}
```

`GraphPage.tsx` **不得 import** `ChangesetPublishAction`。架构测试：

```ts
test("kg page does not import publish or ingest", () => {
  const t = fs.readFileSync(".../pages/GraphPage.tsx", "utf8");
  expect(t).not.toMatch(/ChangesetPublishAction|ingest|invoke_cs|写回/);
});
```

- [ ] **Step 3: `decide` 测试**

```python
    def test_changeset_decide_confirm_applies_once(self):
        sub = self.client.post("/hub/v1/ops/changeset/submit", headers={**OPS_HDR, "Idempotency-Key": "d1"},
                               json={"kind": "graph", "patch": {}})
        cid = sub.json()["changeset_id"]
        dec = self.client.post("/hub/v1/ops/changeset/decide", headers=OPS_HDR,
                               json={"changeset_id": cid, "decision": "confirm"})
        self.assertTrue(dec.json()["applied"])
        self.assertFalse(dec.json()["auto_apply"])

    def test_changeset_no_auto_header(self):
        res = self.client.post("/hub/v1/ops/changeset/decide", headers=OPS_HDR,
                               json={"changeset_id": "x", "decision": "confirm", "auto_apply": True})
        # 即使请求带 auto，响应必须 false
        if res.status_code == 200:
            self.assertFalse(res.json()["auto_apply"])
```

实现：`decide` 调 `evolution_apply`；忽略请求体 `auto_apply`。

- [ ] **Step 4: 口径页只读 `GET /caliber/status`**

表格：kpi_id / caliber / stale。无编辑公式入口（公式改 OSI 文件走 git；P1 再做 YAML 编辑器）。

- [ ] **Step 5: 提交**

```bash
git commit -m "$(cat <<'EOF'
feat(console): kg readonly timeline and changeset decide

EOF
)"
```

---

### Task 8: 门禁验收与两周停用标准（W6）

**Files:**
- Modify: `services/console-nocobase/tests/architecture.test.ts`
- Create: `services/hub-api/tests/test_ops_invariants.py`（或并入 test_ops_console）
- Modify: `harness/requirements/REQ-UAS-AIOS-002.req.md`（勾工程实现的 P0 子集）

- [ ] **Step 1: 不变量清单（全必须绿）**

| ID | 断言 |
|----|------|
| C-01 | 无 `/hub/v1/ops/kg/ingest` |
| C-02 | 无 `/hub/v1/ops/invoke_cs` |
| C-03 | ops 路由 `profile==builder` |
| C-04 | submit 后 `applied==false` |
| C-05 | plugin denylist 与 json 一致 |
| C-06 | 无 forbidden collections |
| C-07 | 三块均非 CollectionBlockModel |
| C-08 | GraphPage 无 publish/ingest |
| C-09 | compiled PATCH 422 |

```bash
python scripts/validate_uas_aios_phase_a.py
# 在 console-nocobase 目录
npx vitest run tests/architecture.test.ts
```

- [ ] **Step 2: 两周 Spike 停用标准（写进 README，不写代码）**

停用 NocoBase、把块搬进 Hub Console 的条件（满足任一）：

1. 三块自定义代码行数 > 插件壳（server+IA）的 3 倍，且仍缺投影/时态浏览。
2. 一线账号能打开 `/console`（菜单泄漏）。
3. 有人启用 Workflow / AI / MCP 才能「演示成功」。
4. 出现 `ag_node` Collection 或 episode 进主库。

- [ ] **Step 3: 提交验收记录**

```bash
git commit -m "$(cat <<'EOF'
test(console): architecture invariants for shell-and-blocks

EOF
)"
```

---

## 依赖与并行

```
Task1 → Task2 → Task3 ─┬→ Task5 → Task6 ─┐
                       └→ Task4 ─────────┴→ Task7 → Task8
```

Task4（壳）可在 Task2 完成后与 Task3 并行。Task5 需要 Task2 的 GET graph。Task7 需要 Task3 的 submit。

不要开第四块「连接器 / Temporal」。那是 B3/B5 运行面，不在本次 Spike。

---

## 本地最小验证（W5 结束时）

1. `python scripts/run_hub_api.py`（监听 `127.0.0.1:18088`，与现网 Demo 一致）
2. `curl -s -H "X-Tenant-Id: t-hengchuan" -H "X-Ops-Role: knowledge_admin" http://127.0.0.1:18088/hub/v1/ops/graph` 看到五件套
3. `--profile console` 起 NocoBase，知识管理员只见四菜单
4. 本体页拖节点 → 提交变更 → changeset `draft`
5. 图谱页搜 `UEC-10293` → 有 episode，无写按钮
6. 法则页点发布 → `decide=confirm`；图谱页找不到该按钮

---

## 非目标（本次不做）

- 责任图落 Postgres 表（仍用 JSON 夹具；落库是数据底座另一条计划）
- 真 Graphiti/Neo4j、真 Cube
- OSI YAML 编辑器
- NocoBase 外部 PG 商业插件
- Utopia
- 一线 WorkStudio 嵌入这些块
