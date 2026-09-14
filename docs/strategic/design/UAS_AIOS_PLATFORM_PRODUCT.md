# UAS-AIOS 平台产品定义

| 项 | 值 |
|----|-----|
| 地位 | **平台级产品权威**。回答：这是什么产品、卖给谁、有哪些产品模块、用户故事、数据怎么流、运营怎么管、系统服务开哪些口。 |
| 方法 | 定位 → 用户/JTBD → 产品结构 → 模块 → 旅程 → 用户故事 → 对象与数据链路 → 运营面/服务面 → 度量 → 切片 |
| 服从 | [`AI_PRODUCT_CHARTER.md`](../../AI_PRODUCT_CHARTER.md) · 道-4 知识即配置 |
| 一线体验 | [`T0产品定义.md`](../../../projects/aios-workstudio/T0产品定义.md)（WorkStudio 子产品，服从本文） |
| 工程契约 | [`UAS_AIOS_ARCHITECTURE_SPEC.md`](./UAS_AIOS_ARCHITECTURE_SPEC.md) |
| 集群集成 | [`UAS_AIOS_CLUSTER_PRODUCTIZATION.md`](./UAS_AIOS_CLUSTER_PRODUCTIZATION.md) |
| 模块选型 | [`UAS_AIOS_MODULE_DESIGN.md`](./UAS_AIOS_MODULE_DESIGN.md) |
| 用户故事 | [`user-stories-uas-aios.md`](../../../harness/requirements/user-stories-uas-aios.md) |
| 可视化 | [`uas-aios-platform.html`](./uas-aios-platform.html) |
| 版本 | v1.0 · 2026-09-10 |

---

## 0. 产品一句话

**UAS-AIOS 是企业的经营操作系统平台**：把「组织目标」和「经营数据」收成同一棵责任图，让一线**看见并办成**，让平台侧**管得住谁能调什么**，让系统侧**只通过契约进出**。

它不是聊天机器人、不是 BI、不是 CRM、不是「再买一个 Agent 平台」。

| 对外说 | 对内是 |
|--------|--------|
| 经营操作系统 | 使用平面 + 控制平面 + 配置运维平面 |
| 三个可售套件 | WorkStudio · Platform Console · System Services |
| 工程模块 M1–M24 | 套件里的能力，不单独报价 |

---

## 1. 定位与边界

### 1.1 品类

企业级 **AGI 经营中枢平台**（Platform）：一套控制面，多岗位工作台，多系统接入。

### 1.2 要解决的平台问题

| # | 现状 | 平台承诺 |
|---|------|----------|
| 1 | 目标、组织、KPI、流程四套树对不齐 | 同一棵责任图，四种投影 |
| 2 | 报表能看不能派 | 指标下拆必须能签发任务 |
| 3 | 办完不回流 | 任务执行必须回写指标 |
| 4 | Agent 直连系统、密钥满天飞 | 只经 `cs.*` / Hub 门禁 |
| 5 | 规则改代码、权限改后台 JSON | 知识即配置 + ChangeSet |
| 6 | 运维靠零件原生 UI（Temporal/Cube/Neo4j） | 运营面用经营语言，零件 UI 只给 SRE 逃生 |

### 1.3 明确不做

- 不自研 CRM / ERP / 数仓 / 大模型  
- 不采购别人的 Ontology OS 当内核  
- 不把聊天、个人记忆、知识图谱当经营状态  
- 一线界面不出现连接器、工作流 ID、Cube 查询语言  
- 运营后台不能静默关审计、不能 `auto_apply` 生产法则  

### 1.4 北极星与护栏

| 北极星 | 定义 |
|--------|------|
| **看见并办成率** | 进入今日必办的 gate 节点中，7 日内完成签发且执行回流的比例 |

护栏：场景写生产次数 = 0；遗忘回执可检索率 = 100%；403 人话覆盖率 = 100%。

---

## 2. 用户与要完成的工作

平台有三类买家，不可混成「一个管理员」。

### 2.1 使用侧（业务用户）

| 角色 | JTBD | 主界面 | 从不进入 |
|------|------|--------|----------|
| 客户经理 / BD | 今天盯谁、派给谁、办完闭环 | WorkStudio | 连接器、口径公式 |
| 销售总监 / 指挥席 | 哪段漏斗堵了、调配谁 | 指挥舱 | compiled WM 编辑 |
| 市场 / 客成 | 线索与健康度（同一套图的投影） | 作战台切片 | 网关工具清单 |
| SelfPaw 个人 | 个人备忘可删除 | 工作台个人区 | 经营库、ΠPaw 记忆 |

### 2.2 运营侧（平台运营）

| 角色 | JTBD | 主界面 |
|------|------|--------|
| 平台管理员 | 谁能调什么、租户与剖面 | Control · 门禁 / 目录 / 租户 |
| 知识管理员 | 责任图、法则、口径、实体白名单正确 | Control · 本体 / 法则 / 口径 |
| 合规官 | 追得回、忘得掉、双轨不混 | Control · 治理 |
| 实施顾问 | Pack 能发布、invariant 过 | Control · 制品 / 发布 |
| 运营值班（SRE-lite） | 积压、stale、续跑、死信 | Control · 运行 / 连接 |

### 2.3 系统侧（集成与机器）

| 角色 | JTBD | 主接口 |
|------|------|--------|
| 岗位 Agent / 内环 | 调语义动作，不见 REST | MCP `cs.*` |
| 客户 IT / SoR | 授权环境槽，不换 CRM | 连接器账户（运营页）+ 厂商 API |
| ETL / 仓 | 口径数、时态事实进来 | `cs.metric.query` 上游；`hub.kg.ingest_episode` |
| 企业 IdP | 只提供「人」 | OIDC / SAML |
| 外部岗位（P1+） | 委托任务 | `hub.task.transfer` → A2A |

---

## 3. 产品结构（三个套件）

工程 24 模块不对外报价。平台产品只有 **三个套件、九个产品模块**。

```
UAS-AIOS Platform
├── 套件 A  WorkStudio          使用产品
│     A1 今日必办 / 作战室 / 指挥舱
│     A2 签发与执行确认（嵌在 A1）
├── 套件 B  Platform Console    运营管理产品
│     B1 控制中心（门禁 · 租户 · 剖面）
│     B2 本体工作室（责任图 · WM · 法则）
│     B3 能力网格（目录 · MCP · 连接器）
│     B4 治理中心（身份 · 审计 · 演化 · 遗忘）
│     B5 运行与知识运营（任务寿命 · 口径 · 时态 · 模型）
└── 套件 C  System Services     系统服务（接口为主，界面为辅）
      C1 应用北向 hub.scene / hub.exec / SSE
      C2 运营北向 hub.ops.*
      C3 南向 MCP / cs.*
      C4 进入向 Webhook / ETL
      C5 身份 OIDC
```

WorkStudio 可以单独卖给业务线；Console + Services 是平台底座，按租户开通。

---

## 4. 产品模块说明书

每个产品模块写清：**界面（人点哪里）** 和 **接口（系统调什么）**。工程模块号只作追溯。

### A1 经营工作台 · WorkStudio

| | |
|--|--|
| 工程 | M1 |
| 界面 | `/today` 今日必办 · `/room/:object_ref` 作战室 · `/command` 指挥舱 · 错误人话条 |
| 接口 | 只消费 C1：`hub.scene.pack.open` `insight.drill` `task.issue` `task.return` `task.transfer`；订阅 SSE |
| 不做 | 连接器页、Cube 查询、Temporal ID |

### A2 签发与确认

| | |
|--|--|
| 工程 | M5 + 执行确认 |
| 界面 | 作战台内：接地灯、派活抽屉、待你确认条 |
| 接口 | `hub.scene.task.*` · `hub.exec.open` · `hub.instance.cycle_step` |
| 不做 | 直接 `invoke_cs`；签发时启工作流 |

### B1 控制中心

| | |
|--|--|
| 工程 | M6 |
| 界面 | **Platform Console / 控制** |
| 页面 | 租户概览 · 剖面矩阵 · 「若现在点写会怎样」试运行 · 403 分类 · 门禁延迟 |
| 接口 | `hub.ops.tenant.get` · `hub.ops.policy.explain` · `hub.ops.profile.matrix` · `hub.ops.health.gate` |
| 禁 | 关审计按钮；客户端改 profile |

### B2 本体工作室

| | |
|--|--|
| 工程 | M2 M3 M4 |
| 界面 | **Console / 本体** |
| 页面 | 责任图编辑（五件套校验、四类边投影）· WM 寿命对照 · Law Pack 版本对比 |
| 接口 | `hub.ops.graph.*` · `hub.ops.wm.*` · `hub.ops.law.*` · 发布必须 `hub.ops.changeset.submit` |
| 禁 | 直接 UPDATE 生产 JSON；live 改 compiled |

### B3 能力网格

| | |
|--|--|
| 工程 | M7 M13 M14 M20 M23 |
| 界面 | **Console / 能力** |
| 页面 | 目录启用/审批级/副作用 · MCP 当前剖面工具预览 · 连接器槽（沙箱/生产）· 契约漂移灯 |
| 接口 | `hub.ops.registry.*` · `hub.ops.mcp.preview` · `hub.ops.connector.*` · `hub.ops.schema.drift` |
| 禁 | 密钥明文回显；模型可见 URL/SQL |

### B4 治理中心

| | |
|--|--|
| 工程 | M8 M9 M10 M11 M12 M17 M21 |
| 界面 | **Console / 治理** |
| 页面 | 岗位绑定 · 双轨抽查 · Skill 货架漏斗 · 制品晋升 · 审计检索/导出 · ChangeSet 评审 · 遗忘回执 · 转派记录 |
| 接口 | `hub.ops.iam.*` · `hub.ops.skill.*` · `hub.ops.artifact.*` · `hub.ops.audit.export` · `hub.ops.changeset.*` · `hub.ops.memory.receipt` · `hub.task.transfer` |
| 禁 | auto_apply；用报告回放经营 |

### B5 运行与知识运营

| | |
|--|--|
| 工程 | M15 M16 M18 M19 M24 |
| 界面 | **Console / 运行** |
| 页面 | 按 `task_id`/`source_node_id` 查长任务 · 审批滞留 SLA · 续跑 · 口径 stale · 时态摄入延迟 · 模型路由 |
| 接口 | `hub.ops.runtime.task` · `hub.ops.runtime.signal`（封装 Temporal） · `hub.ops.caliber.status` · `hub.ops.kg.ingest_status` · `hub.ops.model.route` |
| 禁 | 把 Temporal/Cube/Neo4j 原生 UI 链给业务或普通运营（SRE 逃生通道单独授权） |

### C 系统服务（见 §8 全表）

机器与集成的正式产品面。没有「进对方数据库」这种集成。

---

## 5. 关键旅程（产品方法：旅程完整性）

### J1 一线看见并办成

```
打开工作台 → pack.open 切片 → 今日必办
  → drill（接地）→ 确认签发 → 不写 CRM
  → 进入运行 exec.open → 待确认 / 写 SoR
  → RefreshKpi → 同一节点 is 合流
```

### J2 知识变更

```
本体/法则/口径编辑 → ChangeSet 草案 → 人确认
  → 编译新 compiled → 下次 pack.open 生效
  → 会话内不改生产
```

### J3 能力发布

```
改 registry/schema → CI 漂移检测 → changeset
  → 租户启用 → MCP list 变化 → 试运行 explain
```

### J4 合规遗忘

```
当事人申请删除 → hub.memory.self.forget
  → 回执进经营审计（指针）→ 责任图不变
```

### J5 系统接入

```
客户 IT 开 SoR 槽 → 映射 YAML → 沙箱测幂等
  → 生产槽切换 → 运营页只见状态，不见密钥明文
```

---

## 6. 用户故事索引

完整条目与验收：[`harness/requirements/user-stories-uas-aios.md`](../../../harness/requirements/user-stories-uas-aios.md)。

| 编号段 | 套件 | 数量级 |
|--------|------|--------|
| US-A-* | WorkStudio 使用 | 一线/指挥席 |
| US-B-* | Platform Console 运营 | 平台/知识/合规/实施/值班 |
| US-C-* | System Services | Agent/IT/ETL/IdP |

优先级：P0 覆盖 J1 + 场景禁写 + 审计追加；P1 覆盖 J2/J3；P2 覆盖 A2A/Utopia。

---

## 7. 经营对象与数据链路

### 7.1 对象分册（禁止互冒）

| 对象 | 例子 | 权威存处 | 不是 |
|------|------|----------|------|
| 责任节点 | `an-stage-visit` | 责任图 | 图库节点、记忆行 |
| 世界模型 | draft/compiled/live | WM Store | RAG、聊天 |
| 口径值 | `kpi.is` + `as_of` + `stale` | Cube 查询结果缓存 | 口头公式 |
| 时态事实 | 某日决策链是谁 | Graphiti | 经营承诺 |
| 任务 | `tsk-*` + `source_node_id` | Artifact/任务表 | 工作流 ID |
| 洞察 | 接地假设 | Insight 表 | 未接地建议 |
| 审计 | 调用链 | 审计链 | 指挥舱 KPI |
| 变更 | ChangeSet | 演化表 | 会话内 PATCH |
| 个人记忆 | 备忘 | Lethe 分库 | 经营状态 |
| 主数据 | 客户行 | 客户 SoR | 世界模型 |

### 7.2 主数据链路（看见并办成）

```
SoR 事实 ──ETL/仓──► Cube ──cs.metric.query──► 节点 kpi.is
SoR 事件 ──webhook──► Graphiti ──hub.kg.search──► Insight.evidence
责任图 ought + 岗位切片 ──pack.open──► 工作台
人确认 ──task.issue──► Task（issued）
exec.open ──Temporal──► invoke_cs ──Connector──► SoR 写
                    └──► Patch live WM
                    └──► RefreshKpi ──► 同一 node_id 合流
每次 cs / 升级 ──► 审计链
驳回/超时 ──► ChangeSet（不自动生效）
```

### 7.3 运营数据链路

```
人在 Console 改目录/法则/绑定
  → 只生成 ChangeSet
  → 确认后写配置权威（git/DB 租户覆盖）
  → 下次编译/加载生效
  → 审计一条管理事件（与业务 cs 分类型，同链）
```

### 7.4 系统数据链路

```
IdP 人 ──OIDC──► Hub IAM 绑定岗位/track
Agent ──MCP tools/call──► 重走门禁 ──► Connector
ETL ──hub.kg.ingest_episode──► 图（≠ cs 写）
仓 ──Cube──► 只读数
```

三条链路分名：**经营数据流 / 运营管理流 / 系统集成流**。禁止运营流直接 UPDATE 经营 `kpi.ought` 而不走 ChangeSet。

---

## 8. 运营管理：界面信息架构 + 运营 API

运营是**正式产品**，不是「给运维的后台」。统一入口：**Platform Console**（`/console`），与 WorkStudio（`/app`）分应用、分权限。

### 8.1 界面信息架构

```
Platform Console
├── 总览            租户健康：门禁延迟、stale、审批滞留、未接地率
├── 控制 B1
│     租户 / 剖面矩阵 / 试运行 explain / 403 分类
├── 本体 B2
│     责任图 / 世界模型寿命 / Law Pack
├── 能力 B3
│     目录 / MCP 预览 / 连接器槽 / 契约漂移
├── 治理 B4
│     岗位与双轨 / Skill / 制品 / 审计 / 演化 / 遗忘 / 转派
├── 运行 B5
│     任务检索 / 滞留 SLA / 续跑 / 口径 / 时态摄入 / 模型路由
└── 发布
      ChangeSet 待办（所有写配置的汇合点）
```

一线账号默认 **看不到** `/console`。SRE 另有「零件逃生」开关（Temporal UI 等），默认关，且全程审计。

### 8.2 运营 API：`hub.ops.*`

前缀 `/hub/v1/ops/...`。OIDC + 运营角色。全部写操作要 `Idempotency-Key`，变更类进 ChangeSet。

| 接口 | 方法 | 页面 | 说明 |
|------|------|------|------|
| `hub.ops.tenant.get` | GET | 总览/租户 | 租户与开通套件 |
| `hub.ops.health.summary` | GET | 总览 | 平面 SLO，不暴露零件名给非 SRE |
| `hub.ops.policy.explain` | POST | 试运行 | 输入拟调用 + 剖面，返回人话 |
| `hub.ops.profile.matrix` | GET | 剖面 | 四剖面 × 读写矩阵 |
| `hub.ops.graph.get/validate/publish` | * | 责任图 | publish→changeset |
| `hub.ops.wm.get` | GET | 寿命板 | 三寿命对照 |
| `hub.ops.law.diff` | GET | 法则 | 版本对比 |
| `hub.ops.registry.list/patch` | * | 目录 | patch 为覆盖启用/审批级 |
| `hub.ops.mcp.preview` | GET | MCP | 指定剖面的 tools/list 预览 |
| `hub.ops.connector.list/rotate/slot` | * | 连接器 | 轮换不回显明文 |
| `hub.ops.schema.drift` | GET | 契约 | 与 CI 同逻辑 |
| `hub.ops.iam.bindings` | * | 岗位 | 人↔岗位↔org.* |
| `hub.ops.audit.search/export` | GET | 审计 | 合规包 |
| `hub.ops.changeset.list/submit/decide` | * | 发布 | decide=confirm\|reject；无 auto |
| `hub.ops.memory.receipt.get` | GET | 遗忘 | 只读回执 |
| `hub.ops.runtime.task.get` | GET | 运行 | 按 task/node 查，映射工作流 |
| `hub.ops.runtime.retry` | POST | 运行 | 精确续跑，不回滚合法 SoR 写 |
| `hub.ops.caliber.status` | GET | 口径 | stale 告警 |
| `hub.ops.kg.ingest_status` | GET | 时态 | 延迟/失败 |
| `hub.ops.model.route` | GET/PATCH | 模型 | 剖面→模型；PATCH→changeset |

**运营 API 不做**：签发经营任务、写 SoR、解释 Law 的替代路径（仍走同一 PolicyChain）。

### 8.3 运营事件（管理流）

`ops.changeset.submitted` `ops.connector.rotated` `ops.registry.enabled` `ops.runtime.retried`  
进入审计，类型与 `cs.invoked` 区分。

---

## 9. 系统服务：接口与（最少）界面

系统服务是套件 C 的产品形态：**契约稳定、可版本、可鉴权、可审计**。

### 9.1 应用北向（给 WorkStudio / 合法客户端）

| 接口 | 调用方 | 界面落点 |
|------|--------|----------|
| `POST /hub/v1/scene/pack/open` | 工作台 | 打开即见切片 |
| `POST /hub/v1/scene/insight/drill` | 下拆 | 洞察卡 |
| `POST /hub/v1/scene/task/issue` | 派活 | 签发抽屉 |
| `POST /hub/v1/scene/task/return` | 驳回 | 演化信号 |
| `POST /hub/v1/exec/open` | 进入运行 | 进度条 |
| `POST /hub/v1/instance/cycle_step` | 确认/驳回/补上下文 | 待你确认 |
| `GET /hub/v1/exec/{task_id}/events` | SSE | 进度，不绑 AG-UI |
| `POST /hub/v1/task/transfer` | 转派 | 指挥舱 |
| `GET/PATCH /hub/v1/wm/*` | 指挥席只读 live | 不出现「改 compiled」 |
| `POST /hub/v1/kg/search` | 作战室时间线 | 只读投影 |
| `POST /hub/v1/metric/query` | 内部水合也可对外只读 | 工作台不露查询语言 |
| `POST /hub/v1/memory/self/*` | 仅 SelfPaw | 个人区 |
| `POST /hub/v1/policy/explain` | 任何 403 | 人话条（使用侧也可调） |

信封强制：`tenant_id, actor_id, profile, track, correlation_id`。`profile` 由入口决定。

### 9.2 南向（给模型 / 内环）

| 接口 | 界面（运营预览，非一线） |
|------|--------------------------|
| MCP `tools/list` `tools/call` | Console / MCP 预览 |
| 工具名 `cs.{domain}.{action}` | 目录页 |

list 过滤不能跳过 call 判定。description 无 URL/Token/SQL。

### 9.3 进入向（给客户系统）

| 接口 | 谁调 | 界面 |
|------|------|------|
| `POST /hub/v1/kg/ingest_episode` | ETL/Webhook 服务账号 | 时态摄入监视 |
| 仓 → Cube（厂商协议） | 仓任务 | 口径状态页 |
| SoR → Connector（厂商 API，仅连接器进程） | 连接器 | 槽状态，无 REST 目录给模型 |

### 9.4 身份

| 接口 | 界面 |
|------|------|
| OIDC 授权码 + PKCE / SAML 桥 | 登录无产品页；岗位在 Console / 岗位绑定 |

IdP 不管 `cs.*` 写权。

### 9.5 明确不开放为产品接口

Temporal gRPC、CubeQL、Neo4j Bolt、Vault、数据库、LangGraph 内部 HTTP。SRE 逃生需独立角色 + 审计。

### 9.6 系统服务的「界面」原则

系统套件以 **OpenAPI / MCP 清单 / 变更日志** 为界面；Console 只提供「契约浏览器 + 试运行」，不是第二套业务工作台。

---

## 10. 权限：哪个界面能调哪个口

| 角色 | `/app` | `/console` | C1 应用 API | C2 运营 API | MCP 写 |
|------|--------|------------|-------------|-------------|--------|
| 一线 | 是 | 否 | scene + 有限 exec | 否 | 否 |
| 指挥席 | 是 | 否 | scene + transfer | 否 | 否 |
| 平台管理员 | 否* | 是 | explain | 租户/目录/剖面 | 否 |
| 知识管理员 | 否 | 本体/法则/口径 | 否 | graph/law/caliber+changeset | 否 |
| 合规 | 否 | 治理 | 否 | audit/memory.receipt | 否 |
| 值班 | 否 | 运行 | 否 | runtime/caliber/kg status | 否 |
| 岗位 Agent | 否 | 否 | 否 | 否 | runtime 且过门禁 |
| 服务账号 ETL | 否 | 否 | ingest_episode | 否 | 否 |

\*平台管理员若需体验一线，走「模拟岗位」且全程审计，默认关。

---

## 11. 度量

| 套件 | 指标 | 目标（方向） |
|------|------|----------------|
| A | 看见并办成率、打开时长、403 人话率 | 升 / <2s / 100% |
| B | ChangeSet 平均确认时长、stale 可见率、审批滞留 | 可解释，不追求「自动通过」 |
| C | 契约漂移次数、MCP 与 Registry 一致率 | 漂移=发布失败 |

指挥舱 KPI **不是**平台健康的审计系统。

---

## 12. 版本切片（产品，不是工程 WBS 复述）

| 版本 | 使用套件 | 运营套件 | 系统套件 |
|------|----------|----------|----------|
| **P0 可经营** | 今日必办+签发+人话 | 试运行 explain + 目录启用 | pack.open / issue / 场景写 403 / 审计追加 |
| **P1 可办成** | 待确认+回流 | 运行检索+口径 stale | exec + MCP 只读 + ingest |
| **P2 可运营** | 指挥舱合流 | 本体/法则/演化/遗忘全页 | Cube OSI、Lethe、changeset API |
| **P3 可扩展** | 转派网络 | 模型路由、A2A Card | A2A；Utopia 仍可选 |

---

## 13. 与其它文档

| 文档 | 回答 |
|------|------|
| **本文** | 平台产品是什么、模块、故事、数据链路、运营/系统界面与接口 |
| T0 WorkStudio | 一线话术与页面，是套件 A 的详细 UX |
| 集群产品化 | 三平面集成与管理原则 |
| 模块设计 / 规格 | 怎么实现、字段、错误码 |
| 用户故事文件 | 可开发的故事清单与验收 |

争议：德压过术。运营方便不能把写路径和密钥暴露给一线。
