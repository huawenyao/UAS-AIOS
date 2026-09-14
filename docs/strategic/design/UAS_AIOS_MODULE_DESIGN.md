# UAS-AIOS 模块设计方案与技术选型

| 项 | 值 |
|----|-----|
| 地位 | **模块级设计权威**。每个模块的内部方案、技术栈、否决项以此为准。 |
| 服从 | ADR-SEL-001/002/003 · ADR-EDH-001/002 · 宪章道-4 |
| 契约 / 接口 | [`UAS_AIOS_ARCHITECTURE_SPEC.md`](./UAS_AIOS_ARCHITECTURE_SPEC.md) |
| 自研或集成决策 | [`UAS AIOS架构规划（自研OR集成）.md`](./UAS%20AIOS架构规划（自研OR集成）.md) |
| 产品平面 | [`UAS_AIOS_CLUSTER_PRODUCTIZATION.md`](./UAS_AIOS_CLUSTER_PRODUCTIZATION.md) |
| 平台产品 | [`UAS_AIOS_PLATFORM_PRODUCT.md`](./UAS_AIOS_PLATFORM_PRODUCT.md) |
| 市场对比 | [`SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md`](./SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md) |
| reqharness | [`REQ-UAS-AIOS-001.req.md`](../../../harness/requirements/REQ-UAS-AIOS-001.req.md) · [`uas-aios-module-delivery.md`](../../../harness/knowledge/technical/uas-aios-module-delivery.md) · [`sprint-uas-aios-001.md`](../../../harness/requirements/sprint-uas-aios-001.md) |
| 版本 | v1.0 · 2026-09-10 |
| 状态 | 冻结草案。换零件可以，换契约与判定序必须 ChangeSet / ADR。 |

**一句话**：控制面与经营本体自研、同栈；口径 / 时态 / 遗忘 / 耐久 / 循环采购开源零件；协议押 MCP + OSI + A2A；别人的 OS 不当内核。

---

## 0. 共用技术栈（Hub 家族默认）

先冻结「平台底盘」，各模块只写差异。P0 允许 `hub-api + mcp-gateway + temporal-worker` 同仓；**禁止** Lethe 与责任图同 schema。

| 层 | 首选 | 版本口径 | 备选 | 否决 |
|----|------|----------|------|------|
| 语言（云） | Python | 3.12 | 无（Hub 不双栈） | Node 写门禁；Go 重写控制面（P0） |
| API | FastAPI + Pydantic v2 | 0.115+ / 2.10+ | — | Django 全栈；把 Hub 做成 GraphQL 对外 |
| 迁移 | Alembic | 与 SQLAlchemy 2 同栈 | — | 手工 SQL 当唯一迁移 |
| 经营库 | PostgreSQL | 16 | 云 RDS/Azure PG | Mongo 当责任图；Neo4j 当 L0 |
| 缓存 / SSE 扇出 | Redis | 7 | P0 可进程内；P1 必上 | 用 Redis 存经营状态 |
| 对象存储 | MinIO（实验室）/ S3 | — | OSS / GCS | 制品只放本地磁盘 |
| 身份源 | Keycloak（实验室）/ 企业 Entra·Okta | OIDC | SAML 桥 | 自研登录；把 IdP 角色当经营承诺权 |
| 密钥 | HashiCorp Vault / 云 KMS | — | SOPS+git（仅实验室） | 密钥进仓库、进 tool description |
| 可观测 | OpenTelemetry + 结构化 JSON 日志 | — | — | 只靠 Temporal UI 当监控 |
| 测试 | pytest + `harness/invariants` | — | — | 用聊天手工点当作一验收 |
| 前端（使用平面） | Vite 6 + TypeScript 5 | P0 可沿用现有 HTML Demo | — | Next/Remix（无 SSR 需求）；Redux |
| 包管理（云） | uv | — | poetry | 多套 requirements 分叉 |
| 部署 P0 | Docker Compose | — | — | K8s 作为 P0 前置 |
| 部署 P1 | Kubernetes + Helm | — | Nomad | 把 Temporal / Cube / Neo4j 塞进 Hub 进程 |

**仓库落点（禁止平行建设）**

```
services/hub-api/          # M2–M12 同进程包
services/mcp-gateway/      # M13，可与 hub-api 同镜像不同入口
services/temporal-worker/  # M18 Activity；调 Hub 内部门禁
services/connectors/       # M14 每 SoR 一包
services/workstudio-web/   # M1；P0 可暂指向 projects/aios-workstudio/demo
configs/                   # Law Pack · Registry · OSI · gate_map · 责任图样例
schemas/                   # JSON Schema 权威
```

**公共信封**（所有 `hub.*`）：`tenant_id, actor_id, profile, track, correlation_id, idempotency_key, source_node_id?`。`profile` 由入口强制，忽略客户端伪造。

---

## 1. 使用平面

### M1 WorkStudio 作战台

| 项 | 内容 |
|----|------|
| 决策 | **自研** · 产品壳 · 进程 `workstudio-web` |
| 非职责 | 门禁、循环、口径计算、SoR 写、密钥 |

**设计方案**

1. 路由即场景，不是聊天室：`/today` 今日必办、`/room/:object_ref` 作战室、`/command` 指挥舱、`/exec/:task_id` 执行态。  
2. 启动动作 = `POST /hub/v1/scene/pack/open`，渲染水合后的责任图切片。  
3. 签发嵌在作战台（调用 M5 的 `hub.*`，无本地编译器）。  
4. 进度：`EventSource /hub/v1/exec/{task_id}/events`。403 必须渲染 `error.message` + `hub.policy.explain`。  
5. 状态：URL + 当前 `pack` 快照；刷新再 `pack.open`。禁止把聊天全文当实例状态。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| P0 壳 | 现有 `projects/aios-workstudio/demo` + `nexus-ui.css` | — | 另起一套工作台皮肤当「第二产品」 |
| 产品路径 | Vite 6 + TypeScript 5 + 原生 Custom Elements | Lit | Next.js、Remix、Ant Design Pro 后台壳 |
| 数据获取 | `fetch` + 信封头；OIDC PKCE（AppAuth） | — | 前端 SDK 直连 Cube / Graphiti / CRM |
| 实时 | 自有 SSE | 观察 AG-UI | Socket.IO 自成协议；把 AG-UI 当 P0 |
| 可视化 | 自绘责任图切片（SVG） | Cytoscape 仅指挥舱子树 | ECharts 当第二套 KPI 模型 |

**验收**：A1 打开即见 gate 节点；一线菜单无连接器 / workflow_id / Cube 查询语言。

---

### M5 Insight→Task 编译器

| 项 | 内容 |
|----|------|
| 决策 | **自研** · 无独立进程（`hub-api` 内包） |
| 非职责 | 启 Temporal、调写 cs、解释 Law Pack |

**设计方案**

```
pack 节点 (ought/is/status)
  → InsightCompiler.drill   五维齐？→ kg.search + metric.query → InnerLoop(explore)
  → grounded? 否：422 UNGROUNDED_INSIGHT，信号进 Evolution
  → 人确认
  → TaskIssuer.issue        source_node_id 必填；cs_write ⊆ 节点 process.cs_write
  → 停在 issued（不 StartWorkflow）
```

表：`insight`、`operating_task`（状态机见规格 §3.4）。签发与执行分事务：issue 成功 ≠ CRM 已写。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 实现 | Python 领域服务 + Pydantic 模型（由 M20 生成） | — | 让 LangGraph 自己「决定要不要派活」 |
| 契约 | `schemas/insight.schema.json` · `schemas/operating_task.schema.json`（P0 补） | — | 用聊天 JSON 当任务 |
| 接地 | 强制 `evidence_refs` 至少一条 `kg` 或 `metric` | — | RAG 相似度分数代替接地 |

**验收**：A3 无源节点 422；A4 未接地 422；签发后 Temporal 中无 workflow。

---

## 2. 控制平面（Hub 家族）

### M6 Capability Hub 控制面

| 项 | 内容 |
|----|------|
| 决策 | **自研** · 进程 `hub-api` |
| 非职责 | 实现循环内核、持有 SoR 密钥、当 BI |

**设计方案**

```
FastAPI
  EnvelopeMiddleware          租户 / 相关 ID
  ProfileInjector             按路由强制 scene|explore|builder|runtime
  PolicyChain（不可颠倒）
    1 tenant  2 registry  3 RBAC  4 approval  5 gates  6 scope  7 execute  8 audit
  Routers: scene / exec / wm / kg / metric / memory / iam / policy
  Broker: InnerLoop SPI · Temporal client · Cube/Graphiti/Lethe ports
```

政策是内存 + 配置，不是「再买一个策略产品」。`hub.policy.explain` 把错误码映射成人话与下一步（签发 / 升级 / 补五维）。Thread：`profile` 不可变，改剖面必须新 `thread_id`。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 服务 | FastAPI + uvicorn | — | 用 Dify / Copilot Studio 当 Hub |
| 政策引擎 | 自研 Python 链（判定序可读、可单测） | P2 把 gates 抽到 Cedar / OPA，**外壳仍是本链** | 一上来 OPA 当 OS；Rego 散落连接器 |
| 任务队列客户端 | Temporal Python SDK | — | Celery 当 Runtime 寿命 |
| 组合根 | 显式 Port/Adapter（CubePort, KgPort, MemoryPort, InnerLoopPort） | — | 模块 import 零件 SDK 到 router |

**验收**：scene 调写 cs → 403 + 人话；同一 Thread 改 profile → 409。

---

### M7 Capability Registry `cs.*`

| 项 | 内容 |
|----|------|
| 决策 | **自研契约** · 配置权威 `configs/capability_registry.json` |
| 非职责 | 执行 HTTP；当「WorkStudio API」平行目录 |

**设计方案**

一条 operation = 输入/输出 JSON Schema + `approval_level` + `gates[]` + `side_effects[]` + `idempotent` + `agent_visible` + `connector_id`。运行时加载进内存索引 `(tenant, name)`；租户覆盖表只存启用/停用与审批升级，不改 schema。发布 = ChangeSet，CI 跑 `scripts/validate_capability_registry.py` + M20 漂移检测。

命名：`cs.{domain}.{action}`。口径也是 cs：`cs.metric.query`。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 权威 | JSON 文件（知识即配置）+ DB 租户覆盖 | — | 只存在于代码常量；OpenAPI 自动当语义目录 |
| 校验 | Draft 2020-12 + 现有 validate 脚本 | — | 模型自由发明工具名 |
| 同步 | 启动加载；热更新经 ChangeSet | — | 运行时模型 POST 新工具进生产 |

**验收**：I-12 Registry 名与 MCP `tools/list` 一致；未启用 operation 在步骤 2 拒绝。

---

### M8 Identity & Policy

| 项 | 内容 |
|----|------|
| 决策 | **授权模型自研**；身份源集成 IdP |
| 非职责 | 当 IdP；用 Entra 组替代责任图 `org.*` |

**设计方案**

| 对象 | 存储 | 权威 |
|------|------|------|
| 人 / 密码 / MFA | IdP | IdP |
| 租户、岗位、`position_id`↔`org.*` | Hub 表 `iam_binding` | Hub |
| track / scope | 实例与请求上下文 | Hub |
| 升级 SelfPaw→ΠPaw | `intent-escalation-api` | Hub + 证据 |

权限变更走 `permissionChangeSet`。scope 在步骤 6 **注入连接器**，禁止模型拼 SQL / 选客户范围。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 认证 | OIDC Authorization Code + PKCE | SAML 2.0 桥 | 自研账号库当企业身份 |
| 实验室 IdP | Keycloak 26 | Auth0 | — |
| 企业 IdP | Entra ID / Okta | 企业已有 CAS | 把 IdP 角色映射成 `cs.*` 写权且无 Hub 判定 |
| 授权 | 自研表 + 规格 `enterprise-rbac-abac-spec.md` | P2 Cedar | OPA 散落；Salesforce Profile 当经营承诺权 |
| 令牌 | 验证 JWT（JWKS）+ `X-Tenant-Id` 必须 ⊆ token | — | 前端传 tenant 即信 |

**验收**：无岗位绑定的人 `pack.open` 空切片或 403；A7/A8 双轨。

---

### M9 Skill 协议状态机

| 项 | 内容 |
|----|------|
| 决策 | **自研状态机** · 兼容 agentskills.io |
| 非职责 | 人设商城；把 `CLAUDE.md` 当 Skill |

**设计方案**

```
discovered → previewed → cited → installed → enabled → executed
explore 最高 cited；builder 才 install；runtime 才 enable+execute
```

元数据：`SKILL.md` YAML 头。表 `skill_record(tenant, skill_id, state, cited_in_artifact)`。Explore 引用写入 ThemePack 且 `installed=false`。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 格式 | agentskills `SKILL.md` | — | 把 Skill 做成 GPT Store 人格卡 |
| 发现 | 仓库 / 内网索引 + Hub API | — | 运行时从公网任意装并立刻 execute |
| 执行绑定 | 仅当 state=enabled 且剖面=runtime | — | LangGraph 节点名直接当 Skill |

**验收**：A9 cite 未装可引用不可 execute。

---

### M10 Artifact Store

| 项 | 内容 |
|----|------|
| 决策 | **类型自研**；存储引擎可换 |
| 非职责 | 主数据；用报告回放经营 |

**设计方案**

元数据在 Postgres（`artifact_id, kind, tenant, sha256, promotion, pointers`）；字节在对象存储。晋升：Insight/Task → ThemePack → Blueprint → Release → Instance 事件。报告 / PDF `kind=file` **禁止**被 `pack.open` 当状态源。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 元数据 | PostgreSQL | — | 只靠对象存储目录名 |
| 字节 | MinIO / S3 | OSS | Git LFS 当 Runtime 制品库 |
| 完整性 | sha256 内容寻址 | — | 无哈希覆盖写 |

**验收**：UI 禁用「用报告回放经营」；晋升失败不改 live WM。

---

### M11 Audit

| 项 | 内容 |
|----|------|
| 决策 | **自研追加写** · 对齐 `enterprise-audit-chain-spec.md` |
| 非职责 | KPI 墙；替代指挥舱 |

**设计方案**

每次 `cs.*` / `invoke_cs` / 升级 / 权限变更追加一行：规格 §3.6 字段 + `prev_hash` 链。只追加，更正用补偿事件。导出合规包 = 按 `correlation_id` / `source_node_id` / `cs` 过滤。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 存储 | PostgreSQL 分区表（按月） | P2 再镜像到不可变对象存储 | Elasticsearch 当唯一审计 |
| 哈希 | SHA-256 链 | — | 可 UPDATE 的「日志表」 |
| 查询 | Hub 审计台 SQL | — | 把 Cube 当审计 |

**验收**：A5 写 CRM 后审计链完整；指挥舱挂了审计仍在。

---

### M12 Evolution Engine

| 项 | 内容 |
|----|------|
| 决策 | **自研** · `auto_apply=false` 永不关 |
| 非职责 | 会话内改生产法则 |

**设计方案**

信号（驳回 / 超时 / 未接地率 / 收益）→ 归因 → `ChangeSet(draft)` → 人确认 → 回写 `law_pack | release | permission | caliber` → 下次 compiled。表 `changeset` 字段见规格 §3.5。回滚指针必填。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 草案 | Postgres + unified diff / JSON Patch | — | 模型直接 PATCH 配置文件 |
| 应用 | 复用 `scripts/evolve_apply.py` 语义 | — | CI 机器人 auto_apply |
| 回归 | `regression_cases[]` 绑定 harness | — | 「感觉没问题」发布 |

**验收**：未审批 ChangeSet 不进 compiled；I-09。

---

### M4 Law Pack

| 项 | 内容 |
|----|------|
| 决策 | **自研** · 知识即配置 |
| 非职责 | 咨询用 markdown 堆；模型可跳过 |

**设计方案**

条文文件：`configs/law_packs/{pack_id}.yml`（适用主体、客体、门、冲突策略）。编译器写入 WM `laws[]` 与 Policy `gates`。Hooks **100% 执行**。生产变更只经 M12。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 权威 | Git YAML + schema 校验 | — | 数据库里一份、仓库里一份长期漂移 |
| 执行 | Hub PolicyChain 硬钩子 | — | 只把条文塞进 system prompt |
| 咨询知识 | `CLAUDE.md` / Skill 正文 | — | 与 Law Pack 混成一个文件 |

**验收**：改 YAML 未经 ChangeSet 不能进生产 compiled。

---

### M13 MCP Gateway

| 项 | 内容 |
|----|------|
| 决策 | **自研壳** · 协议用 MCP · 进程可与 Hub 同镜像 |
| 非职责 | 自己做权限判定的「简化版」 |

**设计方案**

`tools/list` = Registry ⋈ profile ⋈ role ⋈ track ⋈ `agent_visible`。`tools/call` **重新**走 PolicyChain，禁止 list 缓存直通。工具名 = `cs.{domain}.{action}`。scene/explore 剥离 `side_effects` 非空。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 协议 | Linux Foundation MCP 2025+（Streamable HTTP + 实验室 stdio） | — | 自研「内部 function call」平行协议 |
| SDK | 官方 MCP Python SDK | — | 手写 JSON-RPC 永久分叉 |
| 传输 | HTTP（企业网关） | stdio 仅本地 Agent | 把 WebSocket 私有帧当标准 |

**验收**：I-05 scene 写工具不可见且 call 仍 403；description 无 URL/Token/SQL。

---

## 3. 经营本体（L0，永不外包）

### M2 责任图 Accountability Graph

| 项 | 内容 |
|----|------|
| 决策 | **自研** · schema 已冻结 |
| 非职责 | 时态事实；口径公式引擎 |

**设计方案**

存储拆成可索引的关系，而不是「一个大 JSON 文件」：

```
ag_graph(graph_id, tenant_id, pack, period, world_model_id)
ag_node(node_id, graph_id, parent_id, goal jsonb, org jsonb, kpi jsonb,
        process jsonb, wm jsonb)
ag_edge(from_id, to_id, kind)  -- org_cascade|kpi_split|stage_split|object_drill
```

`pack.open`：按 `position_id × period` 切片 → 批量 `cs.metric.query` 水合 `kpi.is`（失败标 `stale`）。发布走 ChangeSet。编辑器（Ontology Desk）用同一 schema 校验五件套。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 存储 | PostgreSQL 16 + JSONB + GIN(`org`,`kpi`) | P2 Apache AGE 仅当遍历爆炸 | Neo4j/Graphiti 当 L0；四套树四套表 |
| 契约 | `schemas/accountability_graph.schema.json` | — | ORM 模型偏离 schema |
| 样例 | `configs/accountability_graph.sample.json` | — | — |
| 编辑 UI | JSON Schema 表单 + 投影切换 | — | 在 Neo4j Browser 里改经营 |

**验收**：缺维节点不可签发；I-02。

---

### M3 世界模型 Store

| 项 | 内容 |
|----|------|
| 决策 | **自研** · 三寿命 |
| 非职责 | 预测器；RAG 索引；聊天 checkpoint |

**设计方案**

```
wm_doc(world_model_id, lifetime draft|compiled|live, version, body jsonb, created_by)
UNIQUE(world_model_id, lifetime, version)
```

Runtime 只 `PATCH live`（经 cycle_step）。改法则 → ChangeSet → 新 Release → 新 `compiled`。节点 `wm.*` 是投影指针，不复制企业 WM 全文。压缩策略由 Hub 按剖面注入，框架不得丢五维。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 存储 | 与责任图同一 Postgres，**不同表** | — | 把 WM 塞进 Graphiti；用 Lethe 存 live |
| 契约 | `schemas/enterprise_world_model.schema.json` | — | — |
| API | `hub.wm.get` / `hub.wm.patch` | — | 前台直接 SQL |

**验收**：Runtime PATCH compiled → 拒绝；A10 invariant 失败不能 release。

---

## 4. 系统面

### M14 System Connector

| 项 | 内容 |
|----|------|
| 决策 | **自研适配器 SPI** · 每 SoR 一实现 · 进程 `connector-*` |
| 非职责 | 自研 CRM/ERP；对模型暴露 REST |

**设计方案**

```
class Connector(Protocol):
    id: str
    async def invoke(op, input, scope, idempotency_key) -> ConnectorResult
    async def health() -> Health
```

密钥只在本进程读 KMS 引用。字段映射 YAML：`configs/connectors/{id}.map.yml`。写操作必须幂等键；补偿信号返回给 Temporal（不在此解释 Law）。厂商错误映射为结构化 `result_code`，禁止 HTML 错误页进模型上下文。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| HTTP | httpx + 有限重试（幂等才重试） | — | 在 LangGraph 节点里 httpx CRM |
| Salesforce | 官方 REST 仅此进程 | simple-salesforce | Agentforce 当 OS |
| 审批 / BPM | 调客户 Camunda/OA 的 API | — | 自研 BPM 替代 SoR |
| 沙箱 | 每连接器 `slot=sandbox|prod` | — | 生产凭证写进 Demo |

**验收**：Worker 与模型进程环境变量中无 SoR 明文；幂等重放不双写。

---

### M23 主数据 SoR

| 项 | 内容 |
|----|------|
| 决策 | **连接，不自研 MDM** |
| 产品 | 客户已有 CRM / ERP / 仓 / 审批 / 日历 |

**设计方案**：UAS 只存 `object_ref` 与映射，不复制客户主档。Agentforce / Joule / UiPath = `cs.*` 后端或 RPA 执行器。账户与环境槽由客户 IT 管，UAS 提供连接器运营页（凭证轮换，不明文回显）。

**选型**：按租户采购；默认沙箱可用 Mock Connector。否决：自研「轻量 CRM」当 P0。

---

## 5. 知识零件（L1–L3）

### M15 口径服务 · Cube Core + OSI

| 项 | 内容 |
|----|------|
| 决策 | **集成** · 进程 `cube-api` · 可替换服务，不换 YAML |
| 非职责 | 签发任务；当责任图 |

**设计方案**

```
configs/metrics/osi/*.yml  -- 口径定义（OSI/MetricFlow 互换）
     ↓ 编译（P0 可手工同步）
configs/cube/  cube.js + schema
     ↓
Cube Core  →  仓（只读账号）
Hub cs.metric.query → Cube /v1/load 或 Cube MCP
```

输出必须带 `caliber_id, as_of, stale`。指挥舱切片用同一口径 + `org_cascade` 维度，不另建语义模型。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 服务 | Cube Core（Apache-2.0，自持 Docker） | Cube Cloud（若不想运） | LookML / Fabric 语义模型 / 仓 Semantic View 当唯一真相 |
| 定义 | OSI / MetricFlow YAML | dbt MetricFlow 开源引擎（不绑 Cloud） | 节点内口头公式长期当权威（P1 禁） |
| 对模型 | 只经 `cs.metric.query` | Cube 原生 MCP 仅 Hub 调用 | 作战台写 CubeQL |

**验收**：I-03 失败标 stale；Cube 宕机作战台仍能打开并标明缓存。

---

### M16 时态知识 · Graphiti

| 项 | 内容 |
|----|------|
| 决策 | **集成** · 进程 `graphiti-worker` |
| 非职责 | 经营本体；cs 写；签发 |

**设计方案**

实体白名单（Pydantic）：`Customer Opportunity Visit Approval Interaction`，必须能挂 `object_ref`。摄入：ETL / CRM webhook → `hub.kg.ingest_episode`（服务账号）。检索：`hub.kg.search(object_ref|query, valid_at?, as_of?)`。mutation ≠ `cs.*`。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 运行时 | Graphiti（getzep，Apache-2.0） | Zep Cloud（不想运图库） | Dify/FastGPT 知识库当 L2；LlamaIndex GraphRAG 当主干 |
| 图库 P0 | Neo4j 5 Community | FalkorDB（要 Redis 运维形态时） | 用责任图 Postgres 假装双时态 |
| 工作台 | 无（P0） | Utopia 只读审核（M22） | Neo4j Browser 给一线 |
| 实体 | Pydantic 白名单 | — | 模型自由起实体类型 |

**验收**：I-04 未接地不得签发；图节点 ID ≠ `an-*`。

---

### M17 个人记忆 · Lethe

| 项 | 内容 |
|----|------|
| 决策 | **集成** · 进程 `lethe-api` · **独立数据库** |
| 非职责 | KPI、任务、客户主数据、岗位时间线 |

**设计方案**

仅 `hub.memory.self.*`，且 `track=selfpaw` + `scope=self`。`forget` → Ed25519 回执写入 **经营库审计**（指针），不改责任图。离职作业：全量 forget + 回执归档。架构测试：无 FK、无同 schema。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 引擎 | Lethe / pylethe | 自研「仅向量+删除日志」须保留回执语义 | Mem0 当默认；Letta 自管记忆；聊天历史 |
| 库 | 独立 Postgres `uas_lethe` | — | 与 `ag_node` 同库同 schema |
| 接口 | Hub 封装 | — | ΠPaw 直连 Lethe |

**验收**：A8 pipaw 403；forget 回执可检索；I-08。

---

## 6. 运行时零件（双环）

### M18 外环 · Temporal

| 项 | 内容 |
|----|------|
| 决策 | **集成** · 耐久语义不可换 · 实现可换 |
| 非职责 | 存责任图；解释 Law Pack；持 SoR 密钥 |

**设计方案**

- Workflow：`RuntimeCycleWorkflow` · Queue：`uas-runtime` · Namespace：`uas`  
- 步骤：LoadTask → RunInnerLoop → InvokeCs（每次 cs 一个 Activity，回调 Hub）→ L2+ `WaitForSignal` → PatchLiveWm → RefreshKpi → WriteAudit  
- 补偿：SoR 已写、刷新失败 → 重试 RefreshKpi，不擅自回滚合法写  
- 产品壳按 `task_id` / `source_node_id` 检索，一线不见 workflow id

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 引擎 | Temporal Server 自持（Compose / K8s） | Temporal Cloud | Celery/Airflow 当 HITL 寿命；自研工作流引擎 |
| SDK | temporalio Python | — | 在 Workflow 里跑非确定性 LLM 调用（必须进 Activity） |
| BPM | Camunda 等经 `cs.process.*` | — | 用 Camunda 替代本外环 |
| UI | Temporal UI 仅 SRE | — | 把 Temporal UI 链给客户经理 |

**验收**：I-06 杀 Worker 后续跑；L2 未批不写或可解释等待（A6）。

---

### M19 内环 · LangGraph 1.0

| 项 | 内容 |
|----|------|
| 决策 | **集成，默认实现** · 经 InnerLoop SPI · **禁止第三套** |
| 非职责 | 出站打 CRM；当控制面 |

**设计方案**

SPI：`start_thread / turn / interrupt / resume / compact`。图按剖面加载不同节点，但**一套代码**。工具回调：

```
on_tool_call(name, args):
  assert name in thread.tool_allowlist
  return hub.invoke_cs | hub.kg.search | hub.metric.query
  # 禁止 httpx / SQL
```

Checkpoint 在 Postgres。业务状态 = live WM + Task + 审计指针，不是消息数组。`INNERLOOP_BACKEND=langgraph|codex` 二选一，测试矩阵只跑一套。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 图 | LangGraph 1.0 + `langgraph-checkpoint-postgres` | 同一 SPI 的 Codex/Pi harness | CrewAI、AutoGen 主干、第三套图 |
| 消息 | langchain-core 消息类型（可选） | 自有 item 结构 | 把 LangChain AgentExecutor 当 OS |
| TS 内环 | 不启用 | 前台纯 TS 再评 Mastra（仍须 SPI） | Hub 用 TypeScript 重写循环 |
| 模型厂 SDK | 只当 M24 适配 | OpenAI Agents / ADK | 用厂商会话当 instance 状态 |

**验收**：I-07 静态+运行时无出站 CRM；interrupt 可被 Temporal 信号恢复。

---

### M24 模型推理 Broker

| 项 | 内容 |
|----|------|
| 决策 | **连接，必须可换模型** |
| 非职责 | 会话当实例；厂商 Assistants 当 Runtime |

**设计方案**

Hub Broker 按剖面注入：instructions（含压缩策略）、tool_allowlist、限流、提供商。调用在 InnerLoop Activity 内。记录 token 与 `correlation_id`，不把全文当 WM。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 路由 | 自研薄 Broker（官方 SDK：OpenAI 兼容 / Anthropic / 本地 vLLM） | LiteLLM 作适配器（仍经 Broker） | 绑定单一厂 Agents 云 |
| 配置 | `configs/model_routes.yml`（剖面→模型） | — | 一线菜单选模型当功能 |
| 评测 | harness 回归集 | — | 线上 A/B 直接改 Law Pack |

**验收**：换模型不改 `hub.*` 与一线名词。

---

## 7. 协议与可选

### M20 工具类型 · JSON Schema / Pydantic

| 项 | 内容 |
|----|------|
| 决策 | **一份权威，三处生成** |
| 非职责 | 「给模型宽松、给连接器严格」双份 |

**设计方案**

```
schemas/*.json  +  registry.input/output
        ↓ datamodel-code-generator / 自有脚本
services/hub-api/generated/models.py
        ↓ 同一份
MCP tool schema  ·  FastAPI 校验  ·  连接器校验
CI: 漂移则红灯，禁止发布
```

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| 权威 | JSON Schema 2020-12 | — | 只写 Pydantic 再反推、两份手维护 |
| 生成 | datamodel-code-generator | 自研 codegen | TypeScript 再手写第三份（前台用 JSON Schema 校验即可） |
| 运行时 | Pydantic v2 | — | 任意 dict 进连接器 |

**验收**：I-12；改 registry 字段未生成 → CI 失败。

---

### M21 跨岗位委托 · A2A

| 项 | 内容 |
|----|------|
| 决策 | **P0 自研 transfer；P1+ 集成 A2A** |
| 非职责 | 身份权威放进 A2A 载荷；自研总线；ACP |

**设计方案**

P0：`hub.task.transfer` 改 `assignee`，审计 + IAM。P1：签发岗位 Agent Card（`position_id, cs_allowlist, track=pipaw`）；对端 **仍进对方 Hub**。

**技术选型**

| 层 | 首选 | 备选 | 否决 |
|----|------|------|------|
| P0 | Hub 内部 API | — | 上线即跨租户 A2A |
| P1 | A2A v1（Linux Foundation 系） | — | ACP（已并入，忽略）；自研 NATS 业务总线 |
| 身份 | 双方 Hub OIDC | — | Card 签名替代门禁 |

**验收**：P0 转派后源节点与审计仍在；跨租户默认拒绝。

---

### M22 Utopia（可选 Spike）

| 项 | 内容 |
|----|------|
| 决策 | **默认不部署** · 只读导出 |
| 非职责 | 生产写；替代 Graphiti 运行时 |

**设计方案**：知识管理员在 Spike 里审冲突 → 导出候选条文/实体 → 人走 ChangeSet。无 CRM Action 按钮。Compose profile `optional`。

**选型**：Utopia v0.1 观察。否决：当 L2；当 Dify 替代叙事。

---

## 8. 模块 × 进程 × 库 一览

| 模块 | 进程 | 主存储 | 运行时依赖 |
|------|------|--------|------------|
| M1 | workstudio-web | 无 | 仅 Hub |
| M2 M3 M4 M5 M6 M7 M8 M9 M10 M11 M12 | hub-api | Postgres `uas_hub` | Redis（P1） |
| M13 | mcp-gateway | 无（读 Registry） | Hub Policy |
| M14 | connector-* | 密钥在 KMS | 各 SoR |
| M15 | cube-api | Cube 配置 + 仓 | 只读仓账号 |
| M16 | graphiti-worker | Neo4j **或** FalkorDB | 独立账号 |
| M17 | lethe-api | Postgres `uas_lethe` | 与 Hub 无 FK |
| M18 | temporal-server + temporal-worker | Temporal 自有店 | Worker 只调 Hub |
| M19 | 跑在 worker/hub 内 | checkpoint 在 `uas_hub` | 无出站 SoR |
| M20 | CI | git schemas | — |
| M21 | hub-api（P0） | 同 Hub | P1 A2A 运行时 |
| M22 | 可选 | 自有 | 无写路径 |
| M23 | 客户系统 | 客户 | 仅连接器 |
| M24 | 经 Broker | 无状态 | 提供商 API |

---

## 9. P0 实验室拓扑（Compose）

```
[浏览器] WorkStudio
    │ hub.* / SSE
[hub-api] ──┬── Postgres uas_hub
            ├── Redis（可关）
            ├── mcp-gateway（同镜像）
            ├── temporal-worker ── Temporal Server
            ├── cube-api ── 仓(Postgres 样例)
            ├── graphiti-worker ── Neo4j
            ├── lethe-api ── Postgres uas_lethe
            ├── connector-mock
            └── Keycloak
Vault / 环境变量只给 connector 与 cube 只读账号
```

P0 **不**包含 Utopia、A2A 网络、K8s、AG-UI。

---

## 10. 与已有文档的分工

| 文档 | 回答 |
|------|------|
| **本文件** | 每个模块怎么做、用什么、不用什么 |
| `UAS_AIOS_ARCHITECTURE_SPEC.md` | 字段、URL、错误码、WBS、验收用例 |
| `UAS AIOS架构规划（自研OR集成）.md` | 自研/集成一句话与核心逻辑 |
| `UAS_AIOS_CLUSTER_PRODUCTIZATION.md` | 谁在哪个产品壳里管 |
| `SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md` | 市场为什么这样选 |

争议：德压过术。零件可换，**判定序、信封、责任图五件套、场景禁写、双环 SPI** 不可口头豁免。
