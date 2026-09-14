# UAS-AIOS 企业架构方案（TOGAF ADM 落地）

| 项 | 值 |
|----|-----|
| 地位 | **企业架构总册（TOGAF 框架视图）**。按 TOGAF ADM 全周期组织 UAS-AIOS 的架构资产：原则 → 愿景 → 业务架构 → 信息系统架构 → 技术架构（含选型决策矩阵）→ 机会与迁移 → 实施治理 → 变更管理。 |
| 与既有文档分工 | 本文是 **TOGAF 结构化的架构资产索引与决策总册**；字段级契约以 [`UAS_AIOS_ARCHITECTURE_SPEC.md`](./UAS_AIOS_ARCHITECTURE_SPEC.md) 为准；模块内部以 [`UAS_AIOS_MODULE_DESIGN.md`](./UAS_AIOS_MODULE_DESIGN.md) 为准；交互序列以 [`UAS_AIOS_INTEGRATION_DESIGN.md`](./UAS_AIOS_INTEGRATION_DESIGN.md) 为准；管理后台以 [`UAS_AIOS_ADMIN_CONSOLE_DESIGN.md`](./UAS_AIOS_ADMIN_CONSOLE_DESIGN.md) 为准。本文**不重复细节，只做框架化组织与缺口补齐**。 |
| 方法 | TOGAF Standard（ADM：预备 → A → B → C → D → E → F → G → H + 需求管理）；架构内容按内容元模型组织（目录/矩阵/图） |
| 业务输入 | [`ENTERPRISE_AGI_OPERATING_HUB.md`](./ENTERPRISE_AGI_OPERATING_HUB.md) · [`UAS_AIOS_PLATFORM_PRODUCT.md`](./UAS_AIOS_PLATFORM_PRODUCT.md) |
| 版本 | v1.0 · 2026-09-11 |
| 服从 | [`AI_PRODUCT_CHARTER.md`](../../AI_PRODUCT_CHARTER.md) · ADR-SEL-001/002/003 · ADR-EDH-001/002 |

---

## 0. 执行摘要

**架构愿景**：建成企业的**经营操作系统**——「组织目标 ≡ 经营数据」收进同一棵责任图，一线**看见并办成**，平台侧**管得住谁能调什么**，系统侧**只通过契约进出**。

**架构策略**（一句话）：自有经营本体 + 自有控制面；口径、时态、记忆、耐久、循环、协议全部采购**可替换零件**；AI 原生 = 委托驱动 + 剖面治理 + 知识即配置 + 受控演化。

**ADM 裁剪声明**：本项目为产品型架构（非传统企业 IT 架构），裁剪规则——① Phase B/C/D 不做全量现状盘点，Baseline 只记录与目标架构的差距项；② 架构契约以 `schemas/` + `configs/` + ADR 为载体，不另建文档型契约库；③ 实施治理由 harness invariants + ChangeSet 机制承载，Phase G 只定义治理组织与合规规则。

---

## 1. 预备阶段：架构原则（AI 原生 × TOGAF 原则格式）

> TOGAF 原则四要素：Name / Statement / Rationale / Implications。以下原则对全部架构决策有约束力；违反须走 ADR 变更。

| # | 原则 | 声明 | 理由 | 影响（Implications） |
|---|------|------|------|----------------------|
| AP-01 | 目标即数据 | 目标、组织、KPI、流程是同一棵责任图的投影 | 四套树对不齐是经营数字化的根本断裂 | 禁止平行的目标树/组织树/KPI 树/流程树；节点缺五维不得签发任务 |
| AP-02 | 看见并办成 | 指标下拆必须能签发任务，任务执行必须回写指标 | Dashboard 停在「人看完再切系统去办」 | Insight→Task 编译器是唯一合法派活入口；RefreshKpi 合流是闭环验收 |
| AP-03 | 控制面唯一 | Capability Hub 是唯一控制面与门禁 | 多入口 = 权限穿透与审计断链 | 前台/Agent/Worker/Console 全部经 `hub.*` / `hub.ops.*`；禁第二套注册中心 |
| AP-04 | 语义名隔离 | 模型与前台只见 `cs.{domain}.{action}` 语义名 | 密钥/REST/SQL 暴露 = 安全与可替换性双输 | 密钥不出连接器进程；tool description 无 URL/Token/SQL |
| AP-05 | 剖面强制 | scene/explore/builder/runtime 四剖面由服务端入口强制 | 客户端声明不可信 | 伪造 profile 作废；同 Thread 改剖面恒 409；scene 禁写 |
| AP-06 | 双轨不混权 | SelfPaw（个人）与 ΠPaw（经营承诺）物理分库、升级带证据 | 个人记忆 ≠ 经营承诺（宪章） | Lethe 独立库；ΠPaw 读 Lethe 恒 403；升级必须带证据 |
| AP-07 | 知识即配置 | 法则/口径/能力目录是可版本化配置，变更走 ChangeSet | 改规则改代码 = 不可治理 | Law Pack/Registry/OSI YAML 进 git；`auto_apply` 永关；Hooks 100% 执行 |
| AP-08 | 零件可换、契约不换 | 集成件（Cube/Graphiti/Lethe/Temporal/LangGraph）经 SPI/协议接入 | 18 个月换皮风险；供应商锁定 | 每个集成件定义 SPI 或协议边界；换实现不改 `hub.*` 与一线名词 |
| AP-09 | 委托驱动、耐久执行 | 任务是带 DoD 的委托；长任务由外环耐久化，人审批可暂停续跑 | Agent 任务跨越审批与故障，会话态不可靠 | Temporal 外环 + LangGraph 内环 SPI；杀 Worker 不丢审批 |
| AP-10 | 发现不等于执行 | Skill/能力发现与执行分态（discover≠execute） | 能力暴露即风险暴露 | Skill 六态状态机；explore 最高 cited；MCP list 按剖面过滤 |
| AP-11 | 一切可审计 | 每次调用/变更/升级追加写审计链，可回放 | 治理与合规的物理基础 | 审计追加写 + hash 链；ops 事件与业务事件同链分型；导出动作自审 |
| AP-12 | 受控演化 | 演化信号 → 草案 → 人确认 → 回写，禁止会话内改生产知识 | 静默自改 = 不可治理的 AI | Evolution Engine `auto_apply=false` 无法开启；回归 CASE 绑定 |
| AP-13 | 一线语言纯净 | 一线界面不出现连接器/工作流 ID/CubeQL/零件名 | 运营复杂性不该下沉给业务用户 | 零件 UI 仅 SRE 逃生；换零件一线名词不变 |

**原则冲突裁决**：德压过术——G 层（治理）否决权高于效率与便利（宪章）。

---

## 2. Phase A · 架构愿景

### 2.1 利益相关者与关注点（Stakeholder Map）

| 利益相关者 | 关注点（Concerns） | 对应架构视图（本册章节） |
|------------|--------------------|--------------------------|
| 业务买家（销售 VP/经营负责人） | 看见并办成率、预警提前量、闭环回流 | §2.3 度量；§3 业务架构 |
| 一线用户（CM/BD） | 打开知道干什么、派活不绕路、403 听得懂 | §3.4 业务服务；ADMIN_CONSOLE |
| 平台管理员/IT | 谁能调什么、租户隔离、故障边界 | §4.2 应用交互；§5 技术架构 |
| 知识管理员 | 责任图/法则/口径正确性与可演进 | §4.1 数据治理；§8 实施治理 |
| 合规官 | 追得回、忘得掉、双轨不混 | AP-06/AP-11；§4.1 数据分类 |
| 实施顾问 | Pack 发布确定性、invariant 前置 | §6 过渡架构；§8 |
| 客户 IT（SoR 属主） | 不换 CRM、授权范围可控、密钥不出域 | §5.3 部署；S-21 |
| 架构委员会 | 决策可追溯、变更可回滚 | §8 Phase G；ADR 体系 |

### 2.2 架构愿景声明（Architecture Vision Statement）

> 到目标态，企业的每一个经营位置（责任图节点）都同时是可观察的（口径回填）、可分析的（时态接地）、可行动的（签发任务）、可问责的（审计链）；AI Agent 作为带权的数字岗位在**统一控制面**下执行，其能力、知识、权限、演化全部产品化可运营。平台对企业的承诺：**目标 ≡ 数据、看见并办成、管理即产品**。

### 2.3 价值与度量（对齐产品北极星）

| 度量 | 定义 | 目标方向 |
|------|------|----------|
| 看见并办成率（北极星） | gate 节点 7 日内完成签发且执行回流的比例 | 升 |
| 场景写生产次数 | scene 剖面写调用 | = 0 |
| 403 人话覆盖率 | 错误码 → explain 人话 | = 100% |
| 遗忘回执可检索率 | 合规护栏 | = 100% |
| 打开作战台时延 | pack.open | < 2s |
| 架构合规率 | invariants 通过 / 总数 | = 100%（CI 门禁） |

### 2.4 架构工作说明书摘要（SoW 摘要）

范围：企业营销经营域（LTC 为主价值链）+ 平台治理域 + 系统集成域。不含：CRM/ERP/数仓产品本体、大模型研发、MDM。约束：18 个月分四阶段；P0 不上 K8s/A2A 跨租户/Utopia。

---

## 3. Phase B · 业务架构

### 3.1 业务能力地图（Business Capability Map）

```
UAS-AIOS 支撑的企业能力
├── 经营管理能力（使用平面承载）
│   ├── 目标分解与责任落实      → 责任图（M2）
│   ├── 经营过程监控            → pack 水合 + 指挥舱（M1/M15）
│   ├── 洞察与决策              → Insight 编译（M5/M16/M19）
│   ├── 任务派遣与执行闭环       → Task/Temporal（M5/M18）
│   └── 绩效回流与复盘          → RefreshKpi 合流（M15/M2）
├── 平台治理能力（控制平面承载）
│   ├── 能力治理                → Registry/MCP（M7/M13/M20）
│   ├── 身份与授权治理          → IAM 双轨（M8）
│   ├── 知识与法则治理          → Law Pack/WM（M3/M4）
│   ├── 合规与审计治理          → Audit/遗忘（M11/M17）
│   └── 受控演化治理            → Evolution/ChangeSet（M12）
└── 系统运营能力（配置与运维平面承载）
    ├── 系统连接运营            → Connector 槽（M14/M23）
    ├── 口径运营                → Cube/OSI（M15）
    ├── 时态知识运营            → Graphiti（M16）
    ├── 运行时运营              → Temporal/InnerLoop（M18/M19）
    └── 模型运营                → Broker 路由（M24）
```

### 3.2 价值流（Value Streams，对齐产品旅程 J1-J5）

| 价值流 | 阶段 | 承载能力 | 价值产出 |
|--------|------|----------|----------|
| VS-1 看见并办成 | 打开→洞察→签发→执行→合流 | 经营管理全链 | 缺口关闭、指标回流 |
| VS-2 知识变更 | 编辑→校验→评审→编译→生效 | 知识治理 | 法则/图/口径版本化演进 |
| VS-3 能力上线 | 草案→CI→评审→热载→回归 | 能力治理 | 新语义动作可用且受控 |
| VS-4 合规保障 | 申请→处置→回执→归档 | 合规治理 | 遗忘权可证明 |
| VS-5 系统接入 | 开槽→映射→沙箱→生产 | 系统连接运营 | SoR 能力语义化入网 |

### 3.3 组织与角色（Actor-Role，对齐 ADMIN_CONSOLE §1）

业务侧：一线岗位（CM/BD）、指挥席、SelfPaw 个人。运营侧：平台管理员、知识管理员、合规官、实施顾问、值班运营。系统侧：岗位 Agent、客户 IT、ETL 服务账号、IdP。**角色与页面的映射以 ADMIN_CONSOLE §6.3 为权威**。

### 3.4 业务服务目录（Business Services）

| 业务服务 | 消费者 | 实现（应用服务） |
|----------|--------|------------------|
| 今日必办服务 | 一线 | `hub.scene.pack.open`（切片+水合） |
| 洞察下拆服务 | 一线 | `hub.scene.insight.drill` |
| 派活服务 | 一线 | `hub.scene.task.issue/return/transfer` |
| 执行与审批服务 | 一线 | `hub.exec.open` / `hub.instance.cycle_step` / SSE |
| 门禁解释服务 | 全部 | `hub.policy.explain` |
| 本体/法则/口径配置服务 | 知识管理员 | `hub.ops.graph/wm/law/caliber.*` |
| 能力治理服务 | 平台管理员 | `hub.ops.registry/mcp/connector.*` |
| 合规服务 | 合规官 | `hub.ops.audit/memory.receipt/iam.*` |
| 演化服务 | 全部运营 | `hub.ops.changeset.*` |
| 运行时运营服务 | 值班 | `hub.ops.runtime.*` |

**业务架构红线**：业务服务对一线只暴露经营语言（任务/审批/合流），系统概念（workflow、connector、caliber）止于运营角色界面。

---

## 4. Phase C · 信息系统架构

### 4.1 数据架构

#### 4.1.1 数据实体目录与权威源矩阵（Data Entity × System of Record）

| 数据实体 | 分类 | 权威源（SoR） | 存储 | 禁止冒充 |
|----------|------|---------------|------|----------|
| 责任节点/边 | 经营本体（L0） | 责任图（ChangeSet 发布） | Postgres `ag_*` | 图库节点、仓维度表 |
| 世界模型（三寿命） | 经营本体（L0） | WM Store | Postgres `wm_doc` | RAG 索引、聊天记录 |
| Law Pack 条文 | 法则配置 | git `configs/law_packs/` | git + 编译产物 | 数据库平行副本 |
| 口径定义 | 知识（L1） | git `configs/metrics/osi/` | OSI YAML → Cube | 节点内口头公式 |
| 口径值 kpi.is | 知识（L1） | Cube 查询结果 | 运行时水合缓存 | 责任图内长期快照 |
| 时态事实 episode | 知识（L2） | Graphiti | Neo4j/FalkorDB | 经营承诺、cs 写 |
| 个人记忆 | 知识（L3） | Lethe | Postgres `uas_lethe`（独立） | 经营状态 |
| Insight/Task | 制品 | Artifact Store | Postgres + 对象存储 | 工作流状态 |
| ThemePack/Blueprint/Release | 制品 | Artifact Store | 同上 | 生产配置权威 |
| 审计记录 | 治理 | 审计链 | Postgres 分区表 + hash 链 | Cube 报表 |
| ChangeSet | 治理 | Evolution 表 + git | Postgres | 会话内 PATCH |
| 能力目录 | 系统契约 | git `configs/capability_registry.json` + 租户覆盖 | git + DB 覆盖表 | 代码常量 |
| 连接器凭证 | 系统秘密 | KMS/Vault | KMS | 配置文件、界面回显 |
| 主数据（客户等） | 外部事实 | 客户 SoR（CRM/ERP） | 客户系统 | UAS 内复制主档 |

#### 4.1.2 数据流（三条分名的链路，权威定义见 PLATFORM §7）

1. **经营数据流**：SoR→仓→Cube→`cs.metric.query`→节点 is；SoR 事件→Graphiti→Insight 证据；Task→invoke_cs→SoR 写→RefreshKpi 合流。
2. **运营管理流**：Console 编辑→ChangeSet→配置权威（git/DB 覆盖）→编译/热载→管理事件入审计。
3. **系统集成流**：IdP→OIDC→IAM 绑定；ETL→`hub.kg.ingest_episode`；Agent→MCP→判定序→Connector。

**数据一致性契约**：以 INTEGRATION_DESIGN §5 为权威（ID 链、kpi.is 三态、WM 三寿命、Task×Temporal 状态映射）。

#### 4.1.3 数据治理规则

| 规则 | 机制 |
|------|------|
| 每个数据实体有唯一权威源（§4.1.1 矩阵） | 架构 invariant 检查跨库 FK/同 schema |
| 写生产只经 runtime 剖面 + 判定序 | M6 PolicyChain；scene 写恒 403 |
| 遗忘权可证明 | Lethe 回执 + 审计指针；离职批量作业 |
| 审计不可改 | 追加写 + hash 链；导出动作自审 |
| 配置即数据（知识即配置） | Law/Registry/OSI 进 git，发布走 ChangeSet |

### 4.2 应用架构

#### 4.2.1 应用组件目录（Application Component Catalog，M1-M24 → 构建块）

| 组件 | 类型（ABB 分类） | 自研/集成 | 产品壳归属 |
|------|------------------|-----------|------------|
| WorkStudio（M1） | 渠道应用 | 自研 | 套件 A |
| Insight→Task 编译器（M5） | 业务服务 | 自研 | 套件 A（嵌入式） |
| Capability Hub（M6/M7/M8/M9/M10/M11/M12） | 控制面平台服务 | 自研 | 套件 C + B 管理壳 |
| MCP Gateway（M13） | 协议网关 | 自研壳 | 套件 C |
| Law Pack（M4）/责任图（M2）/WM（M3） | 经营本体服务 | 自研（永不外包） | 套件 B2 |
| Connector（M14） | 集成适配器 | 自研 SPI | 套件 B3 运营 |
| Cube（M15） | 语义/口径服务 | 集成（可换） | 套件 B5 运营 |
| Graphiti（M16） | 时态知识服务 | 集成（可换） | 套件 B5 运营 |
| Lethe（M17） | 记忆服务 | 集成（可换） | 套件 B4 运营 |
| Temporal（M18） | 耐久执行服务 | 集成（语义不可换） | 套件 B5 运营 |
| LangGraph（M19） | 内环循环 | 集成默认（SPI 可换） | 不可见（运维选项） |
| LLM Broker（M24） | 模型路由 | 连接 | 套件 B5 运营 |
| Platform Console（B1-B5） | 管理应用 | NocoBase 壳 + 自定义 Block | 套件 B |
| A2A（M21，P1+） | 跨域委托协议 | 集成 | 套件 C |

#### 4.2.2 应用交互矩阵（通信矩阵，摘录关键边）

| 源 → 目标 | 协议 | 性质 |
|-----------|------|------|
| WorkStudio → Hub | `hub.*` HTTPS JSON + SSE | 北向，唯一入口 |
| Console → Hub | `hub.ops.*` HTTPS（X-Ops-Role） | 管理流，写止于 ChangeSet |
| Hub → Connector → SoR | 内部 Invoke / 厂商 API | 南向，密钥不出进程 |
| 模型/内环 → MCP Gateway → Hub | MCP tools/list·call | 南向，list≠call 双检 |
| Hub → Temporal → Hub | Workflow/Activity 回调 | 东向，Worker 无密钥 |
| Hub → InnerLoop SPI → LangGraph | SPI 调用 | 西向，工具回调只进 Hub |
| Hub → Cube / Graphiti / Lethe | REST/Python API/分库 | 知识向，读写规则各异 |
| Hub ↔ IdP | OIDC | 身份向，IdP 只提供人 |
| Hub → Hub（跨租户，P1+） | A2A | 水平向，对端仍过门禁 |
| 全部 → 审计 | 追加写 | 治理向 |

完整交互序列（17 场景）以 INTEGRATION_DESIGN 为权威。

---

## 5. Phase D · 技术架构

### 5.1 技术标准目录（Technology Standards Catalog）

| 域 | 标准 | 版本口径 | 约束 |
|----|------|----------|------|
| Agent↔工具 | MCP（Linux Foundation） | 2025+ Streamable HTTP | 工具名 = `cs.*`；description 无密钥 |
| 口径定义互换 | OSI / MetricFlow YAML | 冻结子集 | 不绑 dbt Cloud / 仓 Semantic View |
| Agent↔Agent | A2A（P1+） | v1 | 载荷不含身份权威 |
| 技能资产 | agentskills `SKILL.md` | YAML 头规范 | 渐进披露；六态状态机约束 |
| 契约 | JSON Schema | 2020-12 | 一份权威三处生成（M20） |
| 身份 | OIDC（Auth Code + PKCE）/ SAML 桥 | — | IdP 只提供人 |
| 云语言 | Python 3.12 / FastAPI / Pydantic v2 | Hub 不双栈 | 禁 Node 写门禁 |
| 前端 | Vite 6 + TypeScript 5 + 原生 CE | P0 可 demo 壳 | 禁 Next/Remix |
| 数据 | PostgreSQL 16（经营/审计/Lethe 分库）· Neo4j 5 或 FalkorDB · 对象存储 | — | 禁 Lethe 与责任图同 schema |
| 部署 | P0 Docker Compose；P1 K8s+Helm | — | 零件不塞进 Hub 进程 |

### 5.2 技术组合（平台服务清单 → 进程）

`hub-api`（M2-M12 同进程包）· `mcp-gateway`（可同镜像）· `temporal-worker` + Temporal Server · `connector-*`（每 SoR 一进程）· `cube-api` · `graphiti-worker` + 图库 · `lethe-api`（独立库）· `workstudio-web` · `console-nocobase`（官方镜像 + `@uas/plugin-console`）· Keycloak · Vault/KMS · Redis（P1）· MinIO。拓扑与 P0 实验室 Compose 以 MODULE_DESIGN §8/§9 为权威。

### 5.3 架构选型决策矩阵（SBB 评估）

评估准则与权重：**A 架构契合**（控制面主权/契约稳定/判定序兼容）30% · **B AI 原生适配**（协议生态/语义层/Agent 友好）20% · **C 工程成熟度**（生产实证/社区）20% · **D 可自持与许可** 15% · **E 替换成本**（分高=易替换）15%。5 分制。

#### SD-01 口径服务（K-L1）

| 候选 | A | B | C | D | E | 加权 | 结论 |
|------|---|---|---|---|---|------|------|
| **Cube Core + OSI YAML** | 5 | 4（原生 MCP） | 4 | 5（Apache-2.0） | 4 | **4.45** | **选定** |
| dbt MetricFlow（开源引擎） | 4 | 3 | 4 | 4 | 4 | 3.85 | 备选（定义层可互换） |
| LookML / Fabric 语义模型 | 2 | 3 | 4 | 2 | 1 | 2.40 | 否决（绑厂商） |
| 仓 Semantic View 当唯一真相 | 2 | 2 | 4 | 3 | 2 | 2.55 | 否决（契约入仓） |

理由：口径**定义**必须留在可互换 YAML（OSI），服务可换；Cube 原生 MCP 与嵌入分析成熟。ADR-SEL-001。

#### SD-02 时态知识（K-L2）

| 候选 | A | B | C | D | E | 加权 | 结论 |
|------|---|---|---|---|---|------|------|
| **Graphiti + Neo4j/FalkorDB** | 5 | 4（双时态/Pydantic） | 4 | 5 | 4 | **4.45** | **选定** |
| Zep Cloud | 4 | 4 | 4 | 2 | 3 | 3.55 | 备选（不想运图库时） |
| GraphRAG（批处理） | 2 | 3 | 3 | 4 | 3 | 2.85 | 否决（非高频主干） |
| Stardog | 3 | 2 | 4 | 2 | 2 | 2.75 | 仅法规强制 RDF 时 |
| Utopia | 2 | 3 | 1 | 4 | 3 | 2.50 | 仅可选 Spike，不进写路径 |

#### SD-03 个人记忆（K-L3）

| 候选 | A | B | C | D | E | 加权 | 结论 |
|------|---|---|---|---|---|------|------|
| **Lethe / pylethe** | 5（遗忘轴+回执） | 4 | 3 | 4 | 4 | **4.15** | **选定** |
| Mem0 | 3（召回强遗忘弱） | 4 | 4 | 4 | 3 | 3.55 | 否决（遗忘回执不达标） |
| Letta | 2（Agent 自管记忆冲突 Hub） | 4 | 3 | 4 | 3 | 3.05 | 否决 |

#### SD-04 外环耐久执行（R）

| 候选 | A | B | C | D | E | 加权 | 结论 |
|------|---|---|---|---|---|------|------|
| **Temporal** | 5（HITL/续跑/补偿） | 4 | 5 | 4 | 3 | **4.35** | **选定** |
| Celery | 2（无 HITL 寿命） | 3 | 5 | 5 | 4 | 3.55 | 否决 |
| Camunda 类 BPM | 2 | 2 | 5 | 3 | 2 | 2.80 | 仅作 SoR 经 `cs.process.*` |
| 自研工作流引擎 | 3 | 3 | 1 | 5 | 2 | 2.95 | 否决（非核心） |

#### SD-05 内环 Agent 循环（A/R）

| 候选 | A | B | C | D | E | 加权 | 结论 |
|------|---|---|---|---|---|------|------|
| **LangGraph 1.0（同一 SPI）** | 5 | 4 | 4（checkpoint/interrupt） | 5 | 4 | **4.45** | **默认选定** |
| Codex/Pi harness（同 SPI） | 5 | 4 | 3 | 4 | 4 | 4.10 | 备选（配置二选一） |
| CrewAI / AutoGen | 2（人格/会话中心） | 3 | 3 | 4 | 3 | 2.85 | 否决 |
| 模型厂 Agents SDK 当 OS | 1 | 4 | 3 | 2 | 1 | 2.05 | 否决（18 个月换皮） |

#### SD-06 控制面（G/A/R 核心）

| 候选 | A | B | C | D | E | 加权 | 结论 |
|------|---|---|---|---|---|------|------|
| **自研 Capability Hub** | 5 | 4 | 3 | 5 | 5 | **4.40** | **选定（永不外包）** |
| Dify / Copilot Studio 当 Hub | 1 | 3 | 4 | 2 | 1 | 2.05 | 否决（别人的 OS） |
| OPA/Cedar 当 OS（P2 可抽 gates） | 3 | 3 | 4 | 4 | 3 | 3.35 | 部分采纳（P2 抽 gates，外壳仍自研链） |

#### SD-07 管理后台壳（套件 B）

| 候选 | A | B | C | D | E | 加权 | 结论 |
|------|---|---|---|---|---|------|------|
| **NocoBase + 自定义 BlockModel 插件** | 4 | 3 | 4 | 5（Apache 系/可自持） | 3 | **3.85** | **选定**（壳非核，真相在 Hub） |
| 自研后台 | 5 | 3 | 2 | 5 | 5 | 4.00 | 否决（研发挤占内核） |
| Retool 等低代码 SaaS | 2 | 3 | 4 | 1 | 2 | 2.40 | 否决（配置真相外流） |

约束：禁 plugin-workflow/ai/mcp-server；禁经营 Collection；发布只走 changeset.submit（ADMIN_CONSOLE §6）。

#### SD-08 其余冻结选型（简表）

| 决策点 | 选定 | 否决 | 依据 |
|--------|------|------|------|
| 协议族 | MCP + OSI + A2A + SKILL.md | 自研总线/ACP | AP-08；ADR-SEL |
| 身份源 | 企业 IdP（Keycloak 实验室） | 自研登录；IdP 角色当承诺权 | M8 |
| 前端 | Vite6+TS5+CE；Cytoscape 仅指挥舱/画布 | Next/Remix；AntD Pro 壳 | M1 |
| 迁移 | Alembic | 手工 SQL | MODULE §0 |
| 模型接入 | 自研薄 Broker（Provider SDK 仅 Broker 内） | 绑单一厂 Agents 云 | M24 |

### 5.4 选型红线（与 AP 映射）

1. 任何选型不得违反 AP-01~AP-13；冲突时原则胜（德压过术）。
2. 集成件更换（AP-08）：不改 `hub.*`/`hub.ops.*` 契约与一线名词，须附 SPI 兼容证明与回归报告，走 ADR。
3. 新增零件类别：须先证明生态无协议覆盖，再经架构委员会评审入册。

---

## 6. Phase E · 机会与解决方案

### 6.1 差距分析（Baseline → Target）

| 域 | Baseline（现状） | Target | 差距动作 |
|----|------------------|--------|----------|
| 责任图 | schema + 样例冻结；内存夹具 GraphStore | Postgres ag_* + 水合 + 编辑器 | WP-01 |
| WM | schema + 夹具 WmStore | 三寿命 API + compiled 保护 | WP-01 |
| Hub 门禁 | scene/explore/runtime 已有；判定序部分 | 全序 + explain 100% + ops 面 | WP-02 |
| hub.ops.* | **未实现** | 27 接口全量（ADMIN_CONSOLE §5） | WP-03 |
| Insight/Task | 缺口 schema | P0 补 schema + 签发落库 | WP-02 |
| Cube/口径 | 无 | Cube + OSI YAML + stale 语义 | WP-05 |
| Graphiti | FixtureKg | worker + 实体白名单 + 摄入 | WP-04 |
| Lethe | 无 | 分库 + 回执 + 离职作业 | WP-06 |
| Temporal | compose 有服务 | RuntimeCycleWorkflow 全链 | WP-04 |
| LangGraph | 未接（T1 写 Codex/Pi） | SPI 默认实现落地 | WP-04 |
| MCP Gateway | 部分 | list≠call 双检 + 剖面过滤 | WP-02 |
| Console | 无（REQ-002 仅定义） | NocoBase 壳 W0-W12 | WP-07 |
| 审计/演化 | FixtureEvolution | hash 链 + 评审流 + 导出 | WP-03 |
| IAM | 规格已有 | 绑定表 + IdP 集成 + 双轨 | WP-02 |

### 6.2 工作包（Work Packages）

| WP | 内容 | 依赖 | 验收锚点 |
|----|------|------|----------|
| WP-01 经营本体落地 | ag_*/wm_doc 表 + pack.open 水合 + 校验 | — | I-02, A1 |
| WP-02 Hub 门禁完备 | 判定序全序 + explain + Insight/Task schema + MCP 双检 + IAM 绑定 | WP-01 | A2-A4, A7-A9, I-05, I-10 |
| WP-03 治理内核 | 审计 hash 链 + Evolution 评审 + ops 骨架 | WP-02 | I-09, C-5 |
| WP-04 双环运行 | Temporal WF + LangGraph SPI + RefreshKpi 合流 | WP-02 | A5/A6, I-06, I-07, I-11 |
| WP-05 口径链 | Cube + OSI + stale | WP-01 | I-03 |
| WP-06 记忆与合规 | Lethe 分库 + 回执 | WP-03 | A8, I-08, C-6 |
| WP-07 Console 壳 | NocoBase 插件 W0-W12 | WP-03 | C-1~C-10 |
| WP-08 连接器工业化 | 槽/轮换/幂等/死信 | WP-02 | S-21 用例 |
| WP-09 A2A（P1+） | 岗位 Card + 跨 Hub | WP-04 | S-25 |
| WP-10 Utopia Spike（可选） | 只读导出 | WP-07 | 默认不部署 |

### 6.3 过渡架构（Transition Architectures，对齐产品切片）

| 过渡态 | 架构内容 | 出站判据 |
|--------|----------|----------|
| **TA-1 可经营（P0/阶段 A，6 周）** | WP-01+02 核心：只读切片 + 签发 + 场景写 403 + 审计追加 | A1-A4 全绿 |
| **TA-2 可办成（P1/阶段 B，Q1）** | +WP-04/05：Temporal 合流、Graphiti 接地、MCP 只读包 | A5/A6, I-04/06/07/11 |
| **TA-3 可运营（P2/阶段 C，Q2）** | +WP-03/06/07：Console 全页、Lethe、ChangeSet 评审流 | C-1~C-10, I-08/09 |
| **TA-4 可扩展（P3/阶段 D，Q3-Q4）** | +WP-09/10：A2A 岗位网络、Utopia 可选 | S-25 用例 |

---

## 7. Phase F · 迁移规划

### 7.1 实施序列（对齐 SPEC §9 18 个月 + nocobase W0-W12）

```
阶段 A（周 1-6）  WP-01 → WP-02 → WP-03 骨架；Console W0-W2（ops 读/写草稿）
阶段 B（Q1）      WP-04 → WP-05；Console W3-W6（壳 + 三块）
阶段 C（Q2）      WP-06 → WP-07 完成（W7-W12）→ WP-08
阶段 D（Q3-Q4）   WP-09 →（可选 WP-10）；不迁 Palantir、不以仓 View 替 Cube
```

### 7.2 依赖与关键路径

关键路径：WP-01 → WP-02 → WP-04（合流闭环是价值证明点）→ WP-03/07（运营化）。Console 切片 W1-W2 不依赖 NocoBase，可与 WP-02 并行。

### 7.3 迁移风险登记册

| # | 风险 | 等级 | 缓解 |
|---|------|------|------|
| FR-1 | 零件接入挤压内核自研进度 | 高 | 阶段 A 只读替身（Cube 可用 YAML/SQL 替身），接口名先冻结 |
| FR-2 | NocoBase 壳越界成数据核 | 中 | 架构测试：无 Collection/无 ingest/无 invoke_cs（deny-plugins.json） |
| FR-3 | LangGraph/Codex 双实现漂移 | 中 | 同一 SPI + 测试矩阵只跑一套 + 配置开关 |
| FR-4 | 客户强推既有套件（Agentforce 等） | 中 | 套件只进 S 层连接器；ADR-SEL-003 不可谈判 |
| FR-5 | 管理流绕过 ChangeSet（后台改 JSON） | 高 | ops 无直写路由 + CI 漂移红灯 + 审计分型告警 |
| FR-6 | 口径口头公式漂移 | 中 | P1 强制 caliber_id；CALIBER_MISSING 显式报错 |

---

## 8. Phase G · 实施治理

### 8.1 架构合规框架（Architecture Compliance）

| 机制 | 载体 | 强制点 |
|------|------|--------|
| 不变量测试 | `harness/invariants/` | CI 红灯禁发布（场景写拒绝/Task 源节点/Lethe 隔离/跨租户） |
| 契约测试 | `services/hub-api/tests/` + validate 脚本 | A/I/C 三层验收矩阵自动化 |
| Schema 漂移检测 | M20 CI | Registry ↔ MCP ↔ Pydantic 三处同源 |
| 运行时门禁 | M6 PolicyChain | 判定序不可颠倒；profile 强制 |
| 管理流合规 | ChangeSet + ops 审计分型 | 无 auto_apply；评审人≠提交人 |

### 8.2 架构治理组织

**架构委员会**（轻量）：架构负责人 + 治理（M11/M12 属主）+ 业务代表。职责：ADR 评审、原则变更、零件更换批准、禁替代清单守门。会议触发制（有 ADR/ChangeSet 升级即开），非例会制。

**ChangeSet 评审 = 产品化的架构合规**：任何配置/法则/口径/目录/权限变更在 `/releases` 页面完成合规检查（diff/影响范围/回归 CASE），与工程 CI 双闸。

### 8.3 ADR 管理

既有 ADR-EDH-001/002、ADR-SEL-001/002/003 继续有效。新 ADR 触发：原则例外申请、SPI 变更、新零件类别、契约破坏性变更。ADR 记录进 `docs/` 并关联 ChangeSet。

---

## 9. Phase H · 架构变更管理 + 需求管理

### 9.1 变更分级

| 级 | 例 | 路径 |
|----|-----|------|
| 配置变更 | 目录启用、口径调整、法则条文 | ChangeSet（无需 ADR） |
| 零件更换 | Graphiti→Zep、Neo4j→FalkorDB | ADR + SPI 兼容证明 + 回归 |
| 契约变更 | hub.* 破坏性变更、schema 字段移除 | ADR + 双版本并行一个灰度期 |
| 原则变更 | 修改 AP-xx、引入第三套循环 | 架构委员会 + 宪章对齐评审（默认拒绝） |

### 9.2 需求管理（贯穿）

需求追踪链：`harness/requirements/REQ-UAS-AIOS-*.req.md` → 用户故事（US-A/B/C-*）→ 场景（S-xx）→ 验收（A/I/C）→ invariants。新需求进 backlog 必须标注影响的 AP 原则与 WP；影响原则者先走 Phase H 评审再排期。

---

## 附录 A · TOGAF 交付物映射

| TOGAF 交付物 | 本文/仓库落点 |
|--------------|---------------|
| 架构原则 | §1（AP-01~13） |
| 架构愿景 / SoW | §2 |
| 业务架构（能力/价值流/角色/服务） | §3 |
| 数据架构（实体/流/治理/生命周期） | §4.1 + INTEGRATION §5 |
| 应用架构（组件/交互） | §4.2 + INTEGRATION §2-4 |
| 技术架构（标准/组合/选型） | §5 + MODULE_DESIGN |
| 差距分析 / 工作包 / 过渡架构 | §6 |
| 迁移计划 / 风险 | §7 |
| 实施治理 / 合规 | §8 + harness/invariants |
| 变更与需求管理 | §9 |
| 架构契约 | `schemas/` + `configs/` + ADR |

## 附录 B · 构建块映射（ABB → SBB）

架构构建块（ABB，契约与接口）→ 解决方案构建块（SBB，产品与实现）的映射权威表 = `UAS AIOS架构规划（自研OR集成）.md` §2 模块总表（M1-M24 的「决策/产品/可替换」三列）。更换 SBB 不动 ABB（AP-08）。

## 附录 C · 术语

**剖面（profile）**：场景/研究/构建/运行四套政策上下文。**双轨（track）**：SelfPaw 个人轨 / ΠPaw 经营承诺轨。**ChangeSet**：一切生产配置变更的唯一载体。**合流**：执行结果经 RefreshKpi 回填同一责任节点。**SBB/ABB**：解决方案/架构构建块（TOGAF 企业连续体）。

---

*争议时：德压过术。本册变更自身须走 ADR；引用文档的字段级细节变更走各自 ChangeSet/CI 流程。*
