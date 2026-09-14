# UAS-AIOS 集群产品化规划：模块集成 · 管理能力 · 协议机制

| 项 | 值 |
|----|-----|
| 地位 | **产品化权威**。回答：集群怎么卖、模块怎么接、每块怎么管、协议怎么验。 |
| 工程规格 | [`UAS_AIOS_ARCHITECTURE_SPEC.md`](./UAS_AIOS_ARCHITECTURE_SPEC.md) |
| 模块选型 | [`UAS AIOS架构规划（自研OR集成）.md`](./UAS%20AIOS架构规划（自研OR集成）.md) |
| 模块设计 | [`UAS_AIOS_MODULE_DESIGN.md`](./UAS_AIOS_MODULE_DESIGN.md) |
| 平台产品 | [`UAS_AIOS_PLATFORM_PRODUCT.md`](./UAS_AIOS_PLATFORM_PRODUCT.md) · [`uas-aios-platform.html`](./uas-aios-platform.html) |
| 可视化 | [`uas-aios-cluster.html`](./uas-aios-cluster.html) |
| 版本 | v1.0 · 2026-09-09 |
| 服从 | 宪章道-4 知识即配置 · ADR-EDH-001/002 · ADR-SEL-001/002/003 |

---

## 0. 产品化一句话

UAS-AIOS 集群不是「一堆可运行进程」，而是 **三张可交付产品平面** 编在同一控制面上：

| 平面 | 卖给谁 | 价值 |
|------|--------|------|
| **使用平面** | 一线岗位、指挥席 | 看见并办成 |
| **控制平面** | 平台 / IT / 合规 | 谁能调什么、审批、审计、剖面 |
| **配置与运维平面** | 知识管理员、实施、SRE | 法则/口径/连接器/运行时健康 |

模块之间 **只通过协议说话**，不通过「进对方数据库」。管理能力必须落在产品界面上，不能只存在于配置文件和运维手册。

---

## 1. 集群产品地图（工程模块 → 可售产品）

工程模块 M1–M24 不直接对客户报价。对外是 **6 个产品对象**；对内才是模块。

```
┌──────────── 使用平面 ────────────┐
│  WorkStudio                      │  M1 + M5 的体验壳
│  今日必办 / 作战室 / 指挥舱        │
└──────────────┬───────────────────┘
               │ 北向 hub.*
┌──────────── 控制平面 ────────────┐
│  Capability Hub Console          │  M6 的管理壳
│  剖面 · 双轨 · 目录 · 门禁解释     │
│  Pack Studio                     │  M4/M9/M10 的配置壳
│  Governance Console              │  M8/M11/M12 的治理壳
└──────────────┬───────────────────┘
               │ 南向 MCP/cs.* · 东向 Temporal · 知识协议
┌──────────── 配置与运维平面 ──────┐
│  Ontology Desk   责任图+WM       │  M2/M3
│  Capability Mesh 目录+连接器     │  M7/M13/M14
│  Runtime Ops     内外环健康      │  M18/M19
│  Knowledge Ops   Cube/图/记忆    │  M15/M16/M17
└──────────────────────────────────┘
               │
           SoR / IdP / LLM         M23/M24
```

与历史蓝图对齐、不平行建设：WorkStudio = ΠPaw Growth 工作台的经营形态；Hub Console + Mesh = 原 Capability Hub 产品；Governance = Data & Governance Plane；Pack Studio 名称保留；SelfPaw 入口走同一 Hub，记忆走 Lethe 分库。

---

## 2. 三平面集成关系（控制流 / 数据流 / 管理流）

### 2.1 三条流必须分名

| 流 | 携带什么 | 禁止携带 |
|----|----------|----------|
| **控制流** | 剖面、track、审批、门禁结果、Thread | SoR 密钥、SQL |
| **数据流** | 责任图切片、kpi.is、证据指针、Task、live WM 补丁 | 聊天全文当状态 |
| **管理流** | Pack 版本、连接器启用、口径 YAML、ChangeSet | 绕过 Hub 的「后台改 JSON」 |

### 2.2 模块依赖（只列产品级边）

读法：`A → B` 表示 A **调用或依赖** B，B 故障则 A 降级而不是改协议。

```
WorkStudio ──hub.*──► Hub
                         ├──► 责任图 Store          （切片）
                         ├──► WM Store              （三寿命）
                         ├──► Insight→Task          （签发）
                         ├──► Registry/cs.*         （语义动作）
                         ├──► IAM/Policy            （判定序）
                         ├──► Skill 状态机          （发现≠执行）
                         ├──► Artifact              （Task/Theme/Release）
                         ├──► Audit / Evolution
                         ├──► MCP Gateway ──► Connector ──► SoR
                         ├──► Cube（经 cs.metric）
                         ├──► Graphiti（经 hub.kg）
                         ├──► Lethe（仅 selfpaw）
                         ├──► InnerLoop SPI ──► LangGraph
                         └──► Temporal ──► 同一 Hub 门禁（禁止旁路）
```

**硬隔离**

- Lethe ↛ 责任图、↛ Graphiti、↛ Cube（无 FK，无共享 schema）  
- Graphiti mutation ↛ `cs.*` 写  
- Cube ↛ 签发 Task  
- Temporal ↛ 解释 Law Pack  
- WorkStudio ↛ 直连任何零件  

### 2.3 事件（管理流可见的集群心跳）

所有事件进审计，指挥舱只投影，不替代审计。

| 事件 | 发出 | 消费 | 产品含义 |
|------|------|------|----------|
| `pack.opened` | Hub | WorkStudio | 今日切片已加载 |
| `kpi.hydrated` / `kpi.stale` | Cube 适配 | 作战台 | 数是新的还是缓存 |
| `insight.grounded` / `ungrounded` | Hub | 签发器 | 能否派活 |
| `task.issued` | Hub | Temporal（尚未 start） | 单据存在 |
| `exec.opened` | Hub | Temporal | 长任务开始 |
| `cs.invoked` | Gateway | 审计 / 回流 | 是否写了生产 |
| `approval.wait` / `approved` | Temporal | 作战台 SSE | 人在回路 |
| `wm.live.patched` | Runtime 钩子 | 指挥席 | 世界已变 |
| `changeset.drafted` | Evolution | 治理台 | 待人确认 |
| `memory.forgotten` | Lethe | 合规 | 回执已归档 |

---

## 3. 交互协议机制（集群的「普通话」）

协议分 **北 / 南 / 东 / 西 / 知识 / 水平 / 身份 / 演化** 八条。产品上每条都要能：版本化、鉴权、审计、降级说明。

### 3.0 公共信封（所有平面强制）

```json
{
  "envelope": {
    "tenant_id": "t-hengchuan",
    "actor_id": "cowen.hua",
    "profile": "scene|explore|builder|runtime",
    "track": "selfpaw|pipaw|scene",
    "correlation_id": "corr-...",
    "idempotency_key": "idem-...",
    "source_node_id": "an-... | null"
  }
}
```

缺失 `tenant_id` / `profile` → 拒绝。客户端伪造的 `profile` **作废**，以入口强制值为准。

### 3.1 北向 · 使用平面 ↔ 控制平面 · `hub.*`

| 项 | 约定 |
|----|------|
| 传输 | HTTPS JSON · OIDC Bearer · `X-Tenant-Id` |
| 产品入口 | WorkStudio 只实现这一组，不实现零件 SDK |
| 版本 | `/hub/v1/...` ；破坏性变更走新主版本 |
| 错误 | 统一 `error.code` + `hub.policy.explain` 人话 |
| 流式 | Runtime 进度：SSE `/hub/v1/exec/{task_id}/events`（自有，不绑 AG-UI） |

| 动词 | 谁点 | 下游 | 产品结果 |
|------|------|------|----------|
| `hub.scene.pack.open` | 打开作战台 | 责任图 + Cube 水合 | 今日切片 |
| `hub.scene.insight.drill` | 下拆指标 | Graphiti + 短 explore | Insight（须接地） |
| `hub.scene.task.issue` | 派活 | Artifact；**不**启 Temporal | 任务单据 |
| `hub.scene.task.return` | 办完回写 | 回流 is + 审计 | 节点状态更新 |
| `hub.exec.open` | 进入运行 | Temporal Start | 长任务开始 |
| `hub.instance.cycle_step` | 确认/驳回/补上下文 | Temporal Signal | 人在回路 |
| `hub.instance.invoke_cs` | 仅 runtime | MCP → Connector | 写生产 |
| `hub.wm.get` / `patch` | 指挥席 / 循环 | WM Store | 三寿命 |
| `hub.kg.search` / `ingest_episode` | 作战台读 / ETL 写 | Graphiti | 何时为真 |
| `hub.metric.query` | 水合 | Cube | `kpi.is` |
| `hub.memory.self.*` | 仅 SelfPaw | Lethe | 可遗忘 |
| `hub.policy.explain` | 任何 403 | Policy | 人话下一步 |
| `hub.task.transfer` | 转派 | Artifact + IAM | P0 岗位交接 |

产品化要求：**每个 403 在作战台能讲人话**，否则不算集成完成。

### 3.2 南向 · 控制平面 ↔ 系统 · MCP + `cs.*`

| 项 | 约定 |
|----|------|
| 对模型 | MCP `tools/list` `tools/call`；工具名 = `cs.{domain}.{action}` |
| 对连接器 | 内部 InvokeCs；密钥、URL、SQL 不出 tool description |
| 双检 | list 已过滤 **不能** 跳过 call 时的判定序 |
| 口径 | `cs.metric.query` 也是南向语义，背后才是 Cube |
| 幂等 | 写操作必须 `idempotency_key`；连接器实现补偿信号给 Temporal |

**产品化**：Capability Mesh 控制台展示「模型可见名 / 审批级 / 副作用 / 租户开关」，不展示 REST。

### 3.3 东向 · 耐久 · Temporal

| 项 | 约定 |
|----|------|
| Workflow | `RuntimeCycleWorkflow` · Task Queue `uas-runtime` |
| Signal | `approved` `rejected` `more_context` |
| Activity | 一律回调 Hub，**Worker 不持有 SoR 密钥** |
| 产品壳 | Runtime Ops 包装 Temporal UI：按 `task_id` / `source_node_id` 检索，不把工作流 ID 甩给业务用户 |

### 3.4 西向 · 内环 · InnerLoop SPI

```
start_thread / turn / interrupt / resume / compact
```

工具回调只能进 Hub。`INNERLOOP_BACKEND=langgraph|codex` 二选一。产品上：**循环内核是运维选项，不是业务功能开关。**

### 3.5 知识向 · Cube / Graphiti / Lethe

| 协议 | 封装 | 产品禁忌 |
|------|------|----------|
| Cube REST `/v1/load` 或 Cube MCP | `cs.metric.query` | 作战台不出现 Cube 查询语言 |
| Graphiti Python API | `hub.kg.search` / `ingest_episode` | ingest ≠ 写 CRM |
| Lethe add/search/forget | `hub.memory.self.*` | ΠPaw 默认 403 |

口径定义文件走 **OSI/MetricFlow YAML**（git 即配置），Cube 只是服务层。

### 3.6 水平 · A2A（P1+）

P0：`hub.task.transfer`（租户内改 assignee）。  
P1：岗位 Agent Card；对端仍进对方 Hub。A2A 载荷 **不是** 身份权威。ACP 忽略。

### 3.7 身份 · OIDC / SAML

IdP 只提供人。岗位、track、scope、经营承诺权在 Hub IAM。权限变更走 `permissionChangeSet`。

### 3.8 演化 · ChangeSet

`auto_apply=false`。目标：`law_pack | release | permission | caliber`。人确认后下次 compiled/live 生效。禁止会话内改生产知识。

---

## 4. 逐模块：集成关系 · 管理产品化 · 协议

下表「管理产品」= 必须有界面或明确的配置台，而不是「改仓库里的 JSON 就算发布」。

### 使用平面

| 模块 | 集成（上→下） | 管理产品化能力 | 协议 |
|------|---------------|----------------|------|
| **M1 WorkStudio** | 只依赖 Hub | **岗位工作台产品**：场景切换、今日必办、作战室、指挥舱、错误人话、SSE 进度。无密钥、无连接器页。 | 北向 `hub.*` + SSE |
| **M5 Insight→Task** | 读 M2/M3/M15/M16；写 M10 | **签发台**（嵌在作战台）：接地灯、源节点必填、驳回原因进演化。管理员看签发成功率 / 未接地率。 | `insight.drill` `task.issue` `task.return` |

### 控制平面（Hub 家族）

| 模块 | 集成 | 管理产品化能力 | 协议 |
|------|------|----------------|------|
| **M6 Hub 控制面** | 所有下游的唯一门禁 | **Hub Console**：剖面矩阵、判定序可视化、`policy.explain` 试运行、「若现在点写会怎样」。租户级开关。健康：门禁延迟、403 分类。 | 信封 + 判定序；对外仍是 `hub.*` |
| **M7 Registry cs.*** | 被 Gateway/Runtime 读 | **能力目录产品**：启用/停用 operation、审批级、gates、副作用标记、契约测试绿灯。发布 = ChangeSet。 | JSON Schema 权威；MCP 名同源 |
| **M8 IAM** | IdP 入；Policy 出 | **身份与授权产品**：岗位绑定责任图 `org.*`、双轨、scope 模拟器、升级工单。 | OIDC + `hub.iam.*` + Escalation API |
| **M9 Skill 状态机** | Pack Studio 写；Explore/Runtime 读 | **技能货架**：discover→cite→install→enable 漏斗。Explore 最高 cited 的合规报表。 | agentskills `SKILL.md` 头；Hub 状态枚举 |
| **M10 Artifact** | 全场景写读 | **制品库**：Task/Theme/Blueprint/Release/Instance 晋升条。不可把报告当状态源（UI 禁用「用报告回放经营」）。 | 对象存储契约 + 晋升 API |
| **M11 Audit** | 全写 | **审计台**：按 correlation / node / cs 检索。导出合规包。不是 KPI 墙。 | 追加写审计链 |
| **M12 Evolution** | 读驳回/超时/收益 | **演化台**：草案列表、diff、回归 CASE、一键回滚。`auto_apply` 永远关。 | ChangeSet schema |
| **M13 MCP Gateway** | Registry + Policy | **网关运营**：当前剖面工具清单预览、call QPS、被拒原因。 | MCP 2025+ · HTTP/stdio |
| **M4 Law Pack** | 编进 WM / Policy | **法则配置台**（Pack Studio 子页）：条文生效范围、冲突显式、版本对比。 | 知识即配置；编译进 `compiled` |

### 配置与运维平面

| 模块 | 集成 | 管理产品化能力 | 协议 |
|------|------|----------------|------|
| **M2 责任图** | 被 scene 读；口径回填 is | **经营本体编辑器**：节点五件套校验、四类边投影切换、`cs_write` 白名单绑定目录。发布走 ChangeSet。 | Graph JSON + `pack.open` |
| **M3 WM Store** | 三寿命 | **世界模型寿命板**：draft/compiled/live 对照、缺维清单、禁止 live 改 compiled 的按钮级防护。 | `hub.wm.get/patch` |
| **M14 Connector** | 南向执行器 | **连接器运营**：凭证轮换、字段映射、沙箱/生产槽、幂等与死信。密钥不出屏幕明文。 | 内部 Invoke；对模型不可见 |
| **M15 Cube** | 仓 → 口径 → Hub | **口径运营**：OSI YAML 仓库、Cube 服务状态、`stale` 告警、口径变更评审。 | OSI 文件 + `cs.metric.query` |
| **M16 Graphiti** | ETL/episode 入；Explore 出 | **时态知识运营**：实体白名单、摄入延迟、what-changed 抽样。禁止「在图上点一下改 CRM」。 | `hub.kg.*` |
| **M17 Lethe** | 仅 SelfPaw | **遗忘运营（合规）**：删除请求、回执检索、离职清库作业。与经营库隔离证明（架构测试）。 | `hub.memory.self.*` |
| **M18 Temporal** | Runtime 长任务 | **运行时运营**：按任务/节点查工作流、审批滞留 SLA、失败精确续跑。业务用户只见「待你确认」。 | Workflow/Signal/Query |
| **M19 LangGraph** | SPI | **内环运营**：后端开关、checkpoint 磁盘、interrupt 次数。不出现在一线菜单。 | InnerLoop SPI |
| **M20 Schema** | Registry 同源 | **契约治理**：一份 schema 生成 MCP / Pydantic / 文档；漂移检测失败则禁止发布。 | JSON Schema |
| **M21 A2A** | P1+ 岗位 | **岗位委托运营**：Agent Card 签发、对端 Hub 可达性。P0 用 transfer。 | A2A + `task.transfer` |
| **M22 Utopia** | 可选 | **知识审核 Spike**：只导出到 ChangeSet。无生产写按钮。 | 只读导出 |
| **M23 SoR** | 被连接 | **系统账户运营**（客户 IT）：授权范围、环境槽。UAS 不提供 CRM 产品。 | 厂商 API（仅连接器内） |
| **M24 LLM** | Broker | **模型路由运营**：按剖面限流、提供商切换、禁用某模型。会话不当实例状态。 | Provider SDK（仅 Broker 内） |

---

## 5. 管理产品化能力矩阵（谁 · 在哪 · 管什么）

| 角色 | 主产品 | 可管对象 | 不可管 |
|------|--------|----------|--------|
| 一线 CM/BD | WorkStudio | 确认 Insight、签发/转派 Task、催审批 | 连接器、口径公式、Law 条文、Gateway 工具清单 |
| 指挥席 | WorkStudio 指挥舱 | 子树、调配、看合流 | 改 compiled WM |
| 知识管理员 | Ontology Desk + Pack Studio | 责任图、Law Pack、实体白名单、口径 YAML | 生产写路径、SoR 密钥 |
| 平台管理员 | Hub Console + Mesh | 目录启用、剖面、租户、连接器槽 | 静默关审计、auto_apply |
| 合规 | Governance + Lethe 运营 | 审计导出、遗忘回执、双轨抽查 | 业务派活 |
| SRE | Runtime / Knowledge Ops | 健康、积压、stale、续跑 | 改经营 ought |
| 实施顾问 | Pack Studio | Blueprint / Release / 模板 | 跳过 invariant 发布 |

**产品原则**：一线菜单里出现「连接器 / 工作流 ID / Cube 查询」即不合格。那是运维平面的对象。

---

## 6. 集成协议的产品验收（模块间「接上了」的定义）

下列每条都必须有自动化或契约测试，否则只能叫进程堆叠，不能叫集群产品。

| ID | 集成对 | 通过标准 |
|----|--------|----------|
| I-01 | WorkStudio ↔ Hub | 作战台零零件 SDK；断网零件时有人话降级 |
| I-02 | Hub ↔ 责任图 | `pack.open` 缺维 → 不能签发 |
| I-03 | Hub ↔ Cube | is 带 `as_of`；失败标 `stale`，不假装实时 |
| I-04 | Hub ↔ Graphiti | 未接地 Insight 不能 `task.issue` |
| I-05 | Hub ↔ Registry/MCP | scene 调写 cs → 403 且 explain 可用 |
| I-06 | Hub ↔ Temporal | Worker 调 cs 仍走门禁；杀 Worker 后续跑不丢审批 |
| I-07 | InnerLoop ↔ Hub | LangGraph 无出站 HTTP 到 CRM（静态/运行时双检） |
| I-08 | Hub ↔ Lethe | pipaw 调 memory → 403；forget 有回执审计 |
| I-09 | Evolution ↔ Law | 未审批 ChangeSet 不进 compiled |
| I-10 | IAM ↔ IdP | 无岗位绑定的人打不开责任图切片 |
| I-11 | 事件 ↔ 指挥舱 | 写成功后同一 `node_id` 的 is 变化（合流） |
| I-12 | Schema ↔ MCP | Registry 与 tools/list 名/字段一致 |

---

## 7. 集群健康（产品化的可运营性）

对外 SLO 按平面，不按开源零件名。

| 平面 | 用户可感知指标 | 内部拆解 |
|------|----------------|----------|
| 使用 | 打开作战台 < 2s；签发到可见进度 < 3s | Hub p95、责任图读、Cube 水合 |
| 控制 | explain 可用率 100%（有码就有人话） | 错误码目录覆盖 |
| 运行 | 审批等待不丢；失败从断点续 | Temporal |
| 口径 | stale 可见 | Cube / 仓 |
| 合规 | 遗忘回执 100% 可检索 | Lethe + 审计 |

零件可换的前提：上述 SLO **不改名**。换 Graphiti 实现不能让一线菜单冒出新名词。

---

## 8. 产品化实施顺序（在工程 WBS 之上）

相对规格 18 个月节奏，增加 **管理壳** 交付，避免「协议有了、没人管」。

| 阶段 | 使用平面 | 控制平面 | 运维平面 |
|------|----------|----------|----------|
| A · 6 周 | 作战台接 `pack.open` + 签发 | 剖面 403 + explain | 责任图编辑最小集 |
| B · Q1 | SSE 进度、待确认 | Hub 试运行门禁 | Temporal 按 task 检索；Graphiti 摄入监视 |
| C · Q2 | 指挥舱合流 | 目录发布 ChangeSet | Cube OSI 进 git；Lethe 回执台 |
| D · Q3–4 | 岗位委托（transfer→A2A） | Pack Studio 全量 | Utopia 只读审核（可选） |

---

## 9. 与已有文档

| 文档 | 回答 |
|------|------|
| **本文件** | 集群怎么产品化：集成边、管理壳、协议平面 |
| `UAS_AIOS_MODULE_DESIGN.md` | 每模块内部方案与技术栈 |
| `UAS_AIOS_ARCHITECTURE_SPEC.md` | 契约与接口字段 |
| `UAS AIOS架构规划（自研OR集成）.md` | 自研/集成决策 |
| `uas-aios-architecture.html` | 逻辑分层可视化 |
| `uas-aios-cluster.html` | 本文件的集成与协议可视化 |
| `UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md` | 历史产品套件；冲突时以本文件 + 经营中枢为准 |

争议时：德压过术；G 层否决「为了管方便把密钥和写路径暴露给一线」。
