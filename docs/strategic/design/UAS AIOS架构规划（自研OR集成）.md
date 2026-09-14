# UAS-AIOS 最终架构设计（自研 × 集成）

> 地位：工程落地的**模块级架构与选型冻结**。  
> **详细方案（契约 / 接口 / 部署 / 验收 / WBS）**：[`UAS_AIOS_ARCHITECTURE_SPEC.md`](./UAS_AIOS_ARCHITECTURE_SPEC.md) ← 实施以此为准。  
> **降维总图（HTML）**：[`uas-aios-architecture.html`](./uas-aios-architecture.html) · 端云底 + 一条路 + 四把锁。  
> **集群产品化**：[`UAS_AIOS_CLUSTER_PRODUCTIZATION.md`](./UAS_AIOS_CLUSTER_PRODUCTIZATION.md) · [`uas-aios-cluster.html`](./uas-aios-cluster.html) · 三平面集成、管理壳、协议机制。  
> **模块设计与选型**：[`UAS_AIOS_MODULE_DESIGN.md`](./UAS_AIOS_MODULE_DESIGN.md) · 每模块内部方案、技术栈、否决项。  
> 服从：[`AI_PRODUCT_CHARTER.md`](../../AI_PRODUCT_CHARTER.md)、[`ENTERPRISE_AGI_OPERATING_HUB.md`](./ENTERPRISE_AGI_OPERATING_HUB.md)、[`T1-CapabilityHub详细设计.md`](../../../projects/aios-workstudio/T1-CapabilityHub详细设计.md)。  
> 选型论据：[`SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md`](./SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md)。  
> 契约：`schemas/accountability_graph.schema.json` · `schemas/enterprise_world_model.schema.json` · `configs/capability_registry.json`。  
> 版本：v1.0 · 2026-09-09

---

## 0. 一句话

UAS-AIOS 不是「再做一个 Agent 框架」，也不是「再买一个语义层」。  
它是：**自有经营本体 + 自有控制面**，用开放协议把**口径、时态知识、耐久执行、系统动作**编进同一条「看见并办成」闭环。

```
端  WorkStudio（自研）         看见：今日必办 / 客户作战室 / 指挥舱
        │ hub.* 仅这一条入口
云  Capability Hub（自研）      编译：剖面 · 双轨 · G 层 · Skill 发现≠执行
        │ 内环 / 外环 / 工具 经 SPI 接入零件
底  SoR + 口径 + 时态图         事实：CRM/ERP/仓 经 cs.* ；数怎么算走 Cube ；何时为真走 Graphiti
```

**永不外包**：责任图、五维世界模型、Law Pack、Hub 控制面、`cs.*` 契约、Insight→Task。  
**只采购零件**：Cube、Graphiti、Lethe、Temporal、LangGraph、MCP/A2A/OSI。  
**别人的 OS 不当内核**：Palantir / Fabric IQ / Agentforce / Copilot Studio。

---

## 1. 逻辑总图

把 UAS 形式化 `(I,K,R,A,S,G,E,Π)` 落到模块，而不是落到口号。

```
┌──────────────────────────────────────────────────────────────────────────┐
│ I  意图面     WorkStudio 作战台 · Insight/Task（自研）                     │
├──────────────────────────────────────────────────────────────────────────┤
│ Π  协议面     hub.*（自研）  MCP Gateway（自研壳+开源协议）  A2A（P1+）      │
├──────────────────────────────────────────────────────────────────────────┤
│ G  治理面     Identity/Policy · G0–G6 · 审批 · 审计（自研）                 │
├──────────────────────────────────────────────────────────────────────────┤
│ A  编织面     Skill 状态机（自研） · 岗位 Agent Card · 内环 LangGraph      │
├──────────────────────────────────────────────────────────────────────────┤
│ R  运行面     Harness Broker（自研 SPI） · 外环 Temporal · live WM 钩子     │
├──────────────────────────────────────────────────────────────────────────┤
│ K  知识面     L0 责任图+WM+Law（自研）                                      │
│               L1 Cube+OSI（集成）  L2 Graphiti（集成）  L3 Lethe（集成）      │
├──────────────────────────────────────────────────────────────────────────┤
│ S  系统面     cs.* Registry（自研） · Connector（适配） · CRM/ERP/仓 SoR    │
├──────────────────────────────────────────────────────────────────────────┤
│ E  演化面     ChangeSet Engine（自研） · 人确认后回写 Law Pack / Release    │
└──────────────────────────────────────────────────────────────────────────┘
```

四剖面同一 Hub，禁止复制四套注册中心：

| profile | 谁用 | 读 | 写生产 |
|---------|------|----|--------|
| `scene` | 作战台 | 责任图 + Cube `kpi.is` + 脱敏 cs 读 | **拒绝** |
| `explore` | 研究 | Graphiti 时间线 + 可发现 Skill | **拒绝** |
| `builder` | 构建 | mock cs + 工作区文件 | dry-run 例外 |
| `runtime` | 运行 | 真读 + scope | `cs.*` 写，经 L1/L2/L3 + G* |

---

## 2. 模块总表（冻结）

| # | 模块 | 层 | 决策 | 产品/实现 | 可替换？ |
|---|------|----|------|-----------|----------|
| M1 | WorkStudio 作战台 | I / UI | **自研** | 场景态 + 执行态前台 | 否（产品壳） |
| M2 | 责任图 Accountability Graph | K-L0 | **自研** | `accountability_graph.schema.json` | 否 |
| M3 | 世界模型 Store | K-L0 | **自研** | 五维 · draft/compiled/live | 否 |
| M4 | Law Pack | K-L0 / 德 | **自研** | 法则条文 · 知识即配置 | 否 |
| M5 | Insight→Task 编译器 | I | **自研** | 节点签发任务，必带 `source_node_id` | 否 |
| M6 | Capability Hub 控制面 | G/A/R | **自研** | 剖面注入 · 门禁 · 钩子 | 否 |
| M7 | Capability Registry `cs.*` | S/Π | **自研契约** | `cs.{domain}.{action}` + JSON Schema | 否（名与契约） |
| M8 | Identity & Policy | G | **自研** | 租户/岗位/双轨/scope | 身份源可接 IdP |
| M9 | Skill 协议状态机 | A | **自研** | discover≠execute | 否 |
| M10 | Artifact Store | R | **自研** | Theme/Blueprint/Release/Task | 存储引擎可换 |
| M11 | Audit & ChangeSet | G/E | **自研** | 调用链 + 演化草案 | 否 |
| M12 | Evolution Engine | E | **自研** | 信号→草案→人确认→回写 | 否 |
| M13 | MCP Gateway | Π | **自研壳** | 按剖面过滤工具；协议用 MCP | 协议不换，实现可换 |
| M14 | System Connector | S | **自研适配器** | 密钥不出模型 | 连接器实现按 SoR |
| M15 | 口径服务 | K-L1 | **集成** | Cube Core + OSI YAML | 是（换服务，不换 YAML） |
| M16 | 时态知识 | K-L2 | **集成** | Graphiti + Neo4j/FalkorDB | 是（换图运行时） |
| M17 | 个人记忆 | K-L3 | **集成** | Lethe / pylethe | 是（须保留遗忘回执） |
| M18 | 外环运行时 | R | **集成** | Temporal | 是（须保留 HITL/续跑语义） |
| M19 | 内环 Agent 图 | A/R | **集成** | **LangGraph 1.0（默认）** | 是（同一 SPI；禁止第三套） |
| M20 | 工具类型 | Π | **集成** | Pydantic / JSON Schema | 否（与 cs.* 同一份） |
| M21 | 跨岗位委托 | A/Π | **集成** | A2A Agent Card（P1+） | 是（不用自研总线） |
| M22 | 知识工作台 | K 工程 | **可选集成** | Utopia Spike | 默认不进写路径 |
| M23 | 主数据 SoR | S | **连接** | CRM/ERP/数仓/审批/日历 | 不自研 MDM |
| M24 | 模型推理 | A | **连接** | 任意 LLM，经 Broker | 必须可换模型 |

内环冻结说明（相对选型文的收口）：**默认 LangGraph 1.0**。Python 与 Hub 同栈、checkpoint / interrupt 成熟、可被 Temporal Activity 包裹。若仓库已有 Codex/Pi harness 且不愿迁移，通过同一 `InnerLoop SPI` 接入，**不得并行第三套循环**。

---

## 3. 自研模块：定义与核心逻辑

### M1 WorkStudio 作战台

**定义**：端侧唯一经营界面。场景态回答「今天干什么」；执行态回答「这个任务怎么研究 / 固化 / 执行」。不是聊天壳，不是 BI 墙。

**核心逻辑**

1. 打开首页 = 打开当前用户责任图切片（岗位 × 周期），不是空白对话。  
2. 今日必办 = 节点 `kpi.status ∈ {watch, gate}` ∪ 逾期流程挂钩，按紧急度排序。  
3. 客户作战室 = 单一 `object_ref` 上的责任节点 + 360 只读投影。  
4. 指挥舱 = 子树聚合（`org_cascade` / `kpi_split`），不是另一套报表模型。  
5. 用户动作只调 `hub.*`。前台不持有模型密钥、不直连 CRM、不自己算口径。

**非职责**：循环内核、权限判定、写生产、存聊天当状态。

---

### M2 责任图 Accountability Graph

**定义**：经营本体内核。每个可管理位置是同一类节点：

```
AccountabilityNode = Goal × Subject(org) × Object-scope × Metric × Process-hook
                   投影到 WM 五维 space/time/subject/object/feedback
```

**核心逻辑**

1. **目标 ≡ 数据**：禁止「目标树 / 组织树 / KPI 树 / 流程树」四套图。四种边只是投影：`org_cascade` `kpi_split` `stage_split` `object_drill`。  
2. 节点必填 `goal` `org` `kpi` `process` `wm`。缺维 → `WM_INCOMPLETE`，不得签发任务。  
3. `kpi.ought` 来自目标分解；`kpi.is` **只**从口径层（Cube，经 `cs.metric.query`）回填；禁止口头口径。  
4. `process.cs_read` / `cs_write` 声明本节点允许的语义动作。场景态可展示写动作，**不可调用**。  
5. 任务必须带 `source_node_id`。没有源节点的任务不是经营任务。  
6. 权限双轨（SelfPaw / ΠPaw）与经营双轨（指标轨 / 执行轨）**分名**：前者是谁能承诺，后者是看见 vs 办成。

存储：租户级图文档 + 节点索引。不是知识图谱，不存「某天某客户说了什么」——那是 Graphiti。

契约：`schemas/accountability_graph.schema.json`。

---

### M3 世界模型 Store

**定义**：法则编译器的持久化，不是预测器，不是 RAG 索引。三重身份：镜像（反映）→ 透镜（看本质）→ 熔炉（重塑时必须过门禁）。

**核心逻辑**

| 寿命 | 谁写 | 谁读 | 晋升 |
|------|------|------|------|
| `draft` | Explore | Builder 分析 | 五维齐全 + 反馈通道 |
| `compiled` | Builder 固化进 App | Runtime 启动加载 | invariant 通过 |
| `live` | Runtime 每步钩子 | 指挥席 / 演化 | 实例运行中 |

- 同一 `world_model_id` 多寿命。Runtime **不得**改 `compiled`；改法则走 ChangeSet → 新 Release。  
- 最小字段：`space` `time` `subjects` `objects` `feedback` `laws[]` `ought` `is` `gates[]`。  
- 责任图节点的 `wm.*` 是该节点在当前周期的五维投影；企业 WM 是租户/岗位级编译结果。二者引用，不互相冒充。

契约：`schemas/enterprise_world_model.schema.json`。

---

### M4 Law Pack

**定义**：可版本化的应当（ought）条文。知识即配置：改条文 → 下次 compiled/live 生效，不必改代码发版。

**核心逻辑**

1. 条文声明：适用主体、客体、门禁、冲突处理（应当 vs 事实显式，不静默覆盖）。  
2. 只被编译进 WM 与 Hub Policy；模型把条文当咨询，**Hooks 100% 执行、模型不可跳过**。  
3. 生产条文变更必须 ChangeSet：diff、影响范围、回归 CASE、`auto_apply=false`、可回滚。  
4. `CLAUDE.md` / Domain Pack / Skill 正文是咨询知识；Law Pack 是可执行约束。禁止混成一个 markdown 堆。

---

### M5 Insight→Task 编译器

**定义**：把「看见」（指标轨）编成「办成」（执行轨）的唯一合法入口。相对 Dashboard 的分水岭。

**核心逻辑**

```
node (ought/is/delta/status)
  → Insight（只读：原因假设 + 证据指针 + 建议 cs_write）
  → 人确认 / 调整 / 驳回
  → Task { source_node_id, assignee, due, cs_write[], evidence_refs[] }
  → hub.exec.open → Runtime
  → 执行回写 SoR + 刷新 kpi.is
  → 原节点下一次打开已合流
```

规则：

- 未接地证据不得进建议（S4）。  
- `profile=scene` 只产出 Insight 与 Task 记录，调用链在签发处停止。  
- 驳回 / 超时进入 Evolution Engine，不进入「模型下次换个说法再写」。

---

### M6 Capability Hub 控制面

**定义**：唯一控制面。把知识、能力、循环、权限、产物编译成**按场景生效的策略剖面**。WorkStudio 拥有界面与当前对象；Hub 拥有 WM、Skill、cs.*、Harness、身份、制品、审计、演化。

**核心逻辑（判定顺序，不可颠倒）**

```
请求
 → 注入 profile + track + actor
 → Registry：operation 存在且租户启用
 → RBAC：role × operation
 → approval_level L1/L2/L3
 → gates G0–G6
 → scope_rules 注入连接器
 → 工具执行（MCP / Activity）
 → 审计 + 可选 live WM patch + 可选 ChangeSet 信号
```

剖面政策见 §1 表。中途改 profile **必须新开 Thread**（避免污染循环前缀）。

对外只暴露 `hub.*`（见 §5）。错误必须可解释：`hub.policy.explain` 返回人话（「现在是作战台，不能改 CRM」），禁止静默 500。

详细字段与场景政策：`T1-CapabilityHub详细设计.md`。本文件只冻结它与零件的边界。

---

### M7 Capability Registry `cs.*`

**定义**：系统网格的语义目录。模型与前台只看见 `cs.{domain}.{action}` 与 JSON Schema，**永远看不见** REST URL、SQL、Token。

**核心逻辑**

1. 一条 operation = 输入 schema + 输出 schema + `approval_level` + `gates[]` + `side_effects[]` + `idempotent` + `agent_visible`。  
2. 读与写分列。`side_effects` 非空 ⇒ 非 `runtime` 剖面直接 `403 PROFILE_FORBIDS_SIDE_EFFECT`。  
3. 责任图 `process.cs_write` ⊆ 该租户已启用写操作，否则任务不可签发。  
4. 连接器实现可换（Salesforce / 自建 CRM / 沙箱），**语义名不换**。  
5. 口径查询也是 cs：`cs.metric.query` 背后是 Cube，对模型仍是语义名。

落点：`configs/capability_registry.json`。禁止另起「WorkStudio API」平行目录。

---

### M8 Identity & Policy

**定义**：谁能看哪棵子树、谁能承诺对外动作。双轨不混权。

**核心逻辑**

| 概念 | 含义 |
|------|------|
| Tenant | 隔离边界 |
| Org unit / Position | 责任图 `org.*` 的权威来源 |
| Track | 实例级 `selfpaw` \| `pipaw` |
| Scope | self / dept / dept_tree / project / instance |
| Escalation | SelfPaw → ΠPaw 必须带证据，禁止静默 |

判定仍走 M6 顺序。权限变更走 `permissionChangeSet`，禁止后台改 JSON 当发布。

身份**源**可接企业 IdP（OIDC/SAML，集成）；**授权模型**自研，不把经营承诺权交给 Entra / Salesforce 角色当唯一真相。

---

### M9 Skill 协议状态机

**定义**：发现与执行分离。Explore 不限已装 Skill，但看见 ≠ 动手。

```
discovered → previewed → cited
                ↓
           installed → enabled → executed
```

- Explore 最高 `cited`（写入 ThemePack，`installed=false` 必填）。  
- Builder 才 `install`。Runtime 才 `enable+execute`。  
- 兼容 `SKILL.md` YAML 头渐进披露。`CLAUDE.md` / Law Pack 不是 Skill。

---

### M10 Artifact Store

**定义**：工作产物库。产物 ≠ 主数据 ≠ 世界模型。

| 制品 | 所有者 | 下游 |
|------|--------|------|
| Insight / Task | scene | 执行态注入 |
| ThemePack | explore | Builder |
| Blueprint / Release | builder | Runtime 部署 |
| AppInstance 事件 | runtime | live WM + 审计指针 |
| Report / File | 下载 | **不可当状态源** |

存储引擎（对象存储 / Postgres）可换；制品类型与晋升条件不可换。

---

### M11 / M12 Audit 与 Evolution Engine

**定义**：可审计的过去 + 受控的将来。演化禁止会话内静默改生产知识。

**核心逻辑**

```
Runtime 驳回 / 超时 / 未接地 / 收益
  → 归因
  → ChangeSet（draft, auto_apply=false, rollback_ref, regression_cases）
  → 人确认
  → 回写 Law Pack 或新 Release
  → 下次 compiled/live 生效
```

审计记录每次 `cs.*` 调用链、剖面、actor、track、证据指针。指挥舱不是审计系统；审计不可被 KPI 看板替代。

---

### M13 MCP Gateway（自研壳）

**定义**：把 Registry 里 `agent_visible=true` 的 operation **按当前剖面**暴露为 MCP tools。协议是 Linux Foundation MCP；**门禁、过滤、审计是我们的**。

**核心逻辑**

1. `tools/list` = Registry ⋈ profile ⋈ role ⋈ track，不是「把公司所有 API 倒进模型」。  
2. `tools/call` 必须重走 M6 判定顺序，禁止「已经 list 出来就直接打连接器」。  
3. 工具名 = `cs.{domain}.{action}`。参数/返回 = 同一份 JSON Schema（M20）。  
4. scene/explore：**剥离**所有 `side_effects` 非空的 tool。  
5. 密钥、base URL、SQL 只存在 Connector 进程，不进 tool description。

---

### M14 System Connector

**定义**：S 层适配器。一个 `connector_id` 对应一个 SoR 凭证与字段映射。

**核心逻辑**：幂等键、重试、补偿信号交给 Temporal Activity；映射与密钥轮换在连接器。失败返回结构化错误（可审计），不把厂商错误页塞进模型上下文。

不自研：CRM/ERP/数仓产品本身。

---

## 4. 集成模块：决策逻辑 · 使用场景 · 接口

下列模块**禁止**拥有经营本体、签发任务、替代 Hub 门禁。它们是零件。

### M15 Cube Core + OSI YAML（口径）

**决策逻辑**

- 要的是「这个数怎么算、谁能看」，不是「谁对这个数负责」。后者在责任图。  
- Cube Core：Apache-2.0、嵌入分析成熟、**原生 MCP**，可自持。  
- 口径**定义**写成 OSI / MetricFlow 可互换 YAML，避免绑 dbt Cloud 或某一仓 Semantic View。  
- 仓内 Views 可作 Cube 的上游表，**不作**跨系统唯一真相。

**使用场景**

| 场景 | 剖面 | 行为 |
|------|------|------|
| 作战台刷新节点 `kpi.is` | scene | 只读 `cs.metric.query` |
| 指挥舱子树汇总 | scene | 同一口径，按 `org_cascade` 切片 |
| Explore 解释「缺口怎么来的」 | explore | 读口径 + 维度下钻，仍不写 |
| Runtime 任务完成后回流 | runtime | Connector 写 SoR → 仓/Cube 刷新 → 节点 `is` 更新 |

**接口交互**

```
Hub  cs.metric.query
  input:  { kpi_id, grain, from, to, dimensions[], scope }
  output: { value, caliber_id, as_of, evidence }

内部：Hub → Cube REST /v1/load 或 Cube MCP
      Cube → 仓/SQL
模型只见 cs.metric.query，不见 Cube 查询语言。

口径文件：configs/metrics/*.yml   # OSI 互换
责任图 kpi.caliber 引用 caliber_id，禁止节点内手写公式副本。
```

**禁**：用 Cube 当责任图；用 LookML/Fabric 语义模型当 AIOS 内核。

---

### M16 Graphiti（时态知识）

**决策逻辑**

- 责任图回答「谁负责」；Graphiti 回答「事实何时为真、关系怎么跳、证据在哪」。  
- 增量双时态、Pydantic 实体、Apache-2.0、可自持 Neo4j/FalkorDB。  
- Utopia 太早（v0.1）不当运行时；Stardog 过重，除非法规强制 RDF。  
- GraphRAG 批处理不作高频记忆主干。

**使用场景**

| 场景 | 剖面 | 行为 |
|------|------|------|
| 客户作战室时间线 / what-changed | explore / scene 只读投影 | `search` + 有效时间过滤 |
| Insight 接地 | explore | 证据指针写入 Task `evidence_refs` |
| 红队 / 冲突 | explore | 矛盾边显式，不覆盖责任图 ought |
| 岗位上下文 | runtime 读 | 建议前必接地；**仍不能直接写 CRM** |

**接口交互**

```
Hub  hub.kg.ingest_episode     # 仅 runtime 或受控 ETL，不经模型直连图库
     hub.kg.search             # explore/scene
  input:  { object_ref | query, valid_at?, as_of? }
  output: { facts[], valid_from, valid_to, source_ids[] }

内部：Graphiti Python API
  add_episode / search / get_nodes
存储：Neo4j 或 FalkorDB（基础设施，不是本体）

禁止：Graphiti mutation 当作 cs.customer.update
禁止：用图节点 ID 替代 accountability node_id
```

实体类型必须与责任图客体对齐（Customer / Opportunity / Approval…），用 Pydantic 约束，禁止模型自由起实体名污染图。

---

### M17 Lethe（个人可遗忘记忆）

**决策逻辑**

- 个人工作记忆 ≠ 经营承诺 ≠ 岗位时态图。分库是双轨不混权的物理保证。  
- Lethe 强项是遗忘轴与可验证回执（GDPR/员工离职）。Mem0 召回强遗忘弱；Letta 让 Agent 自管记忆，与 Hub 冲突。

**使用场景**

- SelfPaw：草稿偏好、个人备忘、可声明删除。  
- 员工行使删除权：lexical 清除 + 签名回执。  
- **永不**用于：KPI ought/is、任务状态、客户主数据、岗位时间线。

**接口交互**

```
Hub  hub.memory.self.add | search | forget
  仅 track=selfpaw 且 scope=self
  forget → receipt (Ed25519) 写入审计，不写入责任图

ΠPaw / runtime 默认 403 MEMORY_TRACK_FORBIDDEN
```

---

### M18 Temporal（外环）

**决策逻辑**

- Agent 图解决「这一步想什么」；企业解决「审批停三天、失败从哪续、Saga 怎么补」。后者是 Temporal 的本职。  
- 不自研工作流引擎。Camunda 等 BPM 是 SoR，经 `cs.process.*` 调用，不替代外环。

**使用场景**

- Runtime 长任务：拜访准备 → 等人确认 → 写 CRM → 等审批 → 回写指标。  
- HITL：`WaitForApproval` 信号；超时进 Evolution。  
- 补偿：写 SoR 成功但回写指标失败时的 Activity 重试 / 补偿。

**接口交互**

```
hub.instance.cycle_step / hub.exec.open
  → Temporal StartWorkflow  RuntimeCycleWorkflow
       args: { instance_id, task_id, source_node_id, profile=runtime, track }

Workflow（确定性）：
  1. Load compiled WM + Task
  2. Activity RunInnerLoop   # 见 M19，可重试但有上限
  3. Activity InvokeCs       # 每个 cs.* 一次 Activity，走 Hub 门禁
  4. if approval_level≥L2:   WaitForSignal("approved")
  5. Activity PatchLiveWm
  6. Activity RefreshKpi     # cs.metric.query → 更新节点 is
  7. Activity WriteAudit

WorkStudio 订阅 Workflow 事件流（自有 WS/SSE，不绑 AG-UI）。
```

Temporal **不**存储责任图，不解释 Law Pack。它只耐久化「已经过门禁的步骤」。

---

### M19 LangGraph 1.0（内环，默认）

**决策逻辑**

- 需要有状态图、checkpoint、interrupt，且与 Python Hub 同栈。  
- 外环已有 Temporal，内环不必再造寿命；LangGraph 跑在 Activity 内或短请求（explore/builder）内。  
- 模型厂 Agents SDK 跟模型走，只作可选模型适配，不作 OS。  
- CrewAI / AutoGen 人格或会话中心，否决。

**使用场景**

| 剖面 | 图目标 | 工具集 |
|------|--------|--------|
| explore | 加深、红队、引用 Skill | kg.search、metric.query、skill.preview |
| builder | 生成蓝图、跑 invariant | 工作区文件、mock cs |
| runtime | 单步或短链计划 | MCP 已授权写工具；长等待交回 Temporal |

**接口交互（InnerLoop SPI，换皮只改适配器）**

```
inner.start_thread({ profile, instructions, tool_allowlist, checkpoint_id? })
inner.turn({ thread_id, user_item, wm_slice })
inner.interrupt({ thread_id, reason })      # HITL
inner.resume({ thread_id, decision })
inner.compact({ thread_id })               # 压缩策略由 Hub 注入，不由框架擅自丢五维

工具回调：
  模型 tool_call → MCP Gateway → M6 门禁 → Connector
  禁止 LangGraph 节点内直接 httpx CRM
```

Checkpoint 存 Postgres（或 Temporal payload 指针）。**聊天全文不是 checkpoint 的业务状态**；业务状态是 live WM + Task + 审计指针。

若启用 Codex/Pi：实现同一 SPI，配置开关二选一，测试矩阵只跑一套。

---

### M20 JSON Schema / Pydantic（工具契约）

**决策逻辑**：一份 schema 同时服务 Registry、MCP、LangGraph 工具、API 校验。禁止「给模型一份宽松 schema、给连接器一份严格 schema」。

**使用场景**：所有 `cs.*` input/output；Insight/Task 体；ChangeSet diff 元数据。

**接口**：`configs/capability_registry.json` 的 JSON Schema 为权威；Python 侧 Pydantic 由 schema 生成或对测，不手写第二份。

---

### M21 A2A（跨岗位委托，P1+）

**决策逻辑**

- MCP 解决 Agent→工具（垂直）。岗位之间（CM 委托法务催办）是 Agent→Agent（水平）。  
- A2A 已吸收 ACP，不自研消息总线。  
- P0 可先用 Hub 内 `hub.task.transfer`；跨租户/跨产品岗位再用 A2A Agent Card。

**使用场景**：指挥席调配、跨部门审批催办、外部伙伴岗位（未来）。

**接口交互**

```
岗位 Agent Card（我们签发）：
  agent_id, position_id, skill_allowlist, cs_allowlist, track=pipaw
A2A task send → 对端仍必须进对方 Hub 门禁
身份、审批、审计留在双方 Hub，不进 A2A 载荷当权威
```

---

### M22 Utopia（可选 Spike）

**决策逻辑**：知识工程工作台（本体编辑、冲突审核、Ontology2SQL）有价值，v0.1 不进内核、不接生产写。

**使用场景**：知识管理员审核「应当 vs 事实」冲突草稿；输出候选 Law Pack / 实体类型，**经 ChangeSet 人工入库**。

**接口**：只读导出 → 人审 → 写我们的 schema。禁止 Utopia Action 直接打 CRM。

---

### M23 主数据 SoR（连接，不自研）

CRM / ERP / 数仓 / 审批 / 邮件日历提供客体记录与确定性流程。UAS 不复制一套 MDM。字段映射在 Connector；经营语义在责任图。

Salesforce Agentforce / SAP Joule / UiPath 若客户已有，当作 **cs.* 后端** 或 RPA 执行器，不当 OS。

---

### M24 模型推理（连接）

任意 LLM。Broker 注入 instructions + 工具集。禁止把某一家 Assistants API 会话当实例状态。

---

## 5. 端到端交互：一键派活（主路径）

以「客户A 拜访停留 28 天」为例，标明模块边界。

```
[1] WorkStudio scene
    hub.scene.pack.open({ position_id, period })
    Hub 读责任图切片

[2] 水合指标
    对每个 node: cs.metric.query(kpi_id, scope=object_refs)
    Cube 返回 is → 填入节点（内存投影，权威口径在 Cube）

[3] 今日必办
    status=gate 的节点上浮
    可选 hub.kg.search(object_ref) 取「最近互动」只读摘要

[4] 用户点「一键派任务」
    hub.scene.insight.drill(node_id)     # explore 短循环可在此
    inner.turn(profile=explore)          # LangGraph：原因 + 建议动作
    接地：evidence 必须能指到 kg 或 cs 读
    返回 Insight（仍不写 CRM）

[5] 用户确认
    hub.scene.task.issue({
      source_node_id, assignee, due,
      cs_write: ["cs.activity.create"],
      evidence_refs: [...]
    })
    Artifact Store 落 Task
    场景态结束

[6] 进入执行 / 运行
    hub.exec.open(task_id)
    Temporal RuntimeCycleWorkflow 启动
    Activity: inner.turn(profile=runtime, tool_allowlist⊆cs_write)
    模型提议 cs.activity.create
    MCP Gateway → M6 全序门禁 → Connector.CRM
    PostToolUse: Audit + PatchLiveWm
    RefreshKpi: cs.metric.query → 节点 is 变

[7] 作战台再打开
    同一 node_id，缺口与任务状态已合流
```

失败：

- 缺五维 → `WM_INCOMPLETE`，停在 [4]。  
- scene 误发写 → `403 PROFILE_FORBIDS_SIDE_EFFECT`。  
- SelfPaw 写经营承诺 → `TRACK_ESCALATION_REQUIRED`。  
- 审批等待 → Temporal signal；超时 → ChangeSet 草案。

---

## 6. `hub.*` 接口目录（前台唯一入口）

前台与 Agent 运行时对系统只通过这一组语义。连接器、Cube、Graphiti、Lethe、Temporal 均在其后。

| 接口 | 剖面 | 下游零件 | 写生产 |
|------|------|----------|--------|
| `hub.scene.pack.list \| open` | scene | 责任图 | 否 |
| `hub.scene.insight.list \| drill` | scene/explore | Cube + Graphiti + 内环 | 否 |
| `hub.scene.task.issue \| return` | scene | Artifact | 否（只建 Task） |
| `hub.exec.open` | runtime | Temporal | 转入写路径 |
| `hub.theme.*` / `hub.app.*` | explore/builder | Artifact + 内环 | 否 |
| `hub.instance.deploy \| cycle_step \| invoke_cs` | runtime | Temporal + MCP + cs.* | 是（门禁后） |
| `hub.skill.discover \| preview \| cite \| install \| enable` | 按状态机 | Skill Store | install 起才入库 |
| `hub.wm.get \| patch` | 按寿命 | WM Store | live 仅经 cycle_step |
| `hub.kg.search \| ingest_episode` | explore / 受控 ETL | Graphiti | ingest 不等于 cs 写 |
| `hub.memory.self.*` | selfpaw | Lethe | 仅个人库 |
| `hub.metric.query` | scene/explore/runtime | Cube（经 cs.metric） | 否 |
| `hub.policy.explain` | 全 | Policy | 否 |
| `hub.audit.query` | 授权角色 | Audit | 否 |
| `hub.org.*` / `hub.iam.*` | 治理 | IAM | 权限 ChangeSet |
| `hub.task.transfer` | runtime | 内部门禁；P1+ 可映射 A2A | 视 cs |

错误码（UI 必须展示人话）：  
`WM_INCOMPLETE` `PROFILE_FORBIDS_SIDE_EFFECT` `INVARIANT_FAILED` `GATE_BLOCKED` `TRACK_ESCALATION_REQUIRED` `SKILL_NOT_EXECUTABLE_IN_PROFILE` `SCOPE_DENIED` `MEMORY_TRACK_FORBIDDEN`。

---

## 7. 数据与信任边界

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Lethe       │     │ Graphiti     │     │ 责任图+WM   │
│ 个人可遗忘   │     │ 岗位时态事实  │     │ 应当+负责   │
│ SelfPaw 分库 │     │ 只读进建议   │     │ L0 唯一写入 │
└─────────────┘     └──────────────┘     └─────────────┘
        × 禁止互当权威                    ↑ ought 只来自这里
                                         ↓ is 只来自 Cube←仓←SoR

┌─────────────┐     ┌──────────────┐
│ Cube        │     │ CRM/ERP/仓   │
│ 口径服务     │ ←── │ 主数据 SoR    │
└─────────────┘     └──────────────┘
        写 SoR 只经 cs.* + runtime
```

三条不可互相冒充：

1. **产物**（报告、ThemePack）不是状态。  
2. **主数据**（客户记录）不是世界模型。  
3. **世界模型**不是知识图谱，也不是口径层。

---

## 8. 禁替代清单（架构红线）

| 禁止 | 原因 |
|------|------|
| Palantir / Fabric IQ / Agentforce / Copilot Studio 当内核 | 别人的 OS，UAS 变成实施商 |
| Cube / dbt / 仓 Semantic View 当责任图 | 无 Owner、无流程挂钩、不能合法签发任务 |
| Graphiti / Utopia 当责任图或写路径 | 时态事实 ≠ 过关动作 |
| Lethe / 聊天历史当经营状态 | 双轨混权；宪章禁止 |
| CrewAI / Dify / n8n 当中枢 | 人格或流水线工厂 |
| 模型厂 Agents SDK 当 OS | 18 个月换皮 |
| 第三套 Agent 循环 | 违反 Hub T1 |
| 自研 ACP 总线 | 已并入 A2A |
| Agent 直连 REST/SQL | ADR-002 |
| 场景态写生产 | 剖面政策 |

争议时：**德压过术**；G 层否决权高于「某零件 star 更多」或「客户已经买了某套件」。套件只进 S 层。

---

## 9. 与已有文档的关系

| 文档 | 回答 |
|------|------|
| 本文件 | 模块边界、自研定义、集成接口（一览） |
| `UAS_AIOS_ARCHITECTURE_SPEC.md` | **详细方案**：数据契约、hub.* 规格、零件映射、部署、验收、WBS |
| `SEMANTIC_AND_AGENT_PLATFORM_SELECTION.md` | 为什么选这些零件 |
| `ENTERPRISE_AGI_OPERATING_HUB.md` | 业务语言：看见并办成 |
| `T1-CapabilityHub详细设计.md` | Hub 内部政策与钩子 |
| `T1-场景态与执行态.md` | 作战台 UX |
| `AI_PRODUCT_CHARTER.md` | 道/德否决权 |

实施顺序仍服从选型文 18 个月节奏：先冻 L0 schema 与 `hub.*` 门禁，再接 Cube 只读，再 Graphiti Explore，再 Temporal Runtime，内环只落地 LangGraph 一套。
