# UAS-AIOS L1-L3 企业级 Agent 生态体系

> 从企业主权数据平面到经营数字岗位体系：以 UAS-AIOS 的世界模型、ASUI、双轨 AGI 与治理演化闭环，构建可审计、可回滚、可演化的企业级数字人生态。
> 具体产品方案、功能清单、工程架构与模块设计见 [UAS-AIOS 企业级产品蓝图](./UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md)。
> 全链路图形化表达见 [UAS-AIOS 企业级可视化蓝图](./UAS_AIOS_ENTERPRISE_VISUAL_BLUEPRINT.md)。

---

## 0. 定义边界与当前实现状态

本文的 **L1-L3** 指企业级数字人生态的产品层级：

| 层级 | 企业语义 | UAS 轨道 | 核心对象 |
|------|----------|----------|----------|
| **L1 个人数字分身** | 员工的企业版第二大脑与任务代理 | selfpaw / UAS-U | 员工、岗位、个人授权、证据与意图 |
| **L2 职能数字人** | 组织内部跨部门职能岗位 | Πpaw / UAS-S | HR、财务、法务、合规、调度、运营 |
| **L3 经营数字人** | 面向客户、渠道、市场与交付的经营岗位 | Πpaw / UAS-S | 销售顾问、客服、投标、渠道伙伴、客户成功 |

这与 `docs/认知超智能.md` 中的认知演进 L1-L4 不是同一套命名。本文采用企业产品层定义，并与 UAS-AIOS 的双轨 AGI 对齐：

- **User AGI = selfpaw (UAS-U)**：个人侧世界模型 + 个人 Agent / 蜂群。
- **Business AGI = Πpaw (UAS-S)**：组织侧世界模型 + 多专业 Agent 编排。
- **当前实现边界**：Πpaw/UAS-S 以 UAS-AIOS 本仓库为主；**SelfPaw/UAS-U 主实现**在 `aipos/copaw-src`（本机 `C:\Users\ranwu\XiaomiCloud\aipos\copaw-src`），见 [SELFPaw_REFERENCE_IMPLEMENTATION.md](../../SELFPaw_REFERENCE_IMPLEMENTATION.md)。本仓库 `projects/selfpaw-enterprise` 为企业租户与升级 ΠPaw 契约层。

---

## 1. 第一性判断：企业要的不是 Agent，而是组织能力的可执行化

企业级数字人生态的本质不是“让模型替人聊天”，而是把组织能力变成可授权、可调度、可审计、可演化的执行网络。

### 1.1 组织内在逻辑

企业不是 API 集合，而是由以下结构共同构成的价值机器：

| 组织结构 | 数字化表达 | UAS 承载层 |
|----------|------------|------------|
| 目标与经营指标 | OKR、KPI、SLA、现金流、毛利、风险阈值 | I / E |
| 岗位与责任 | 角色、权限、RACI、审批矩阵 | G / A |
| 业务对象 | 客户、线索、商机、合同、工单、发票、项目、库存 | K / S |
| 流程与制度 | BPM、表单、审批、合规规则、法则包 | K / R / G |
| 系统与数据 | CRM、ERP、BPM、财务、数据仓库、文档库 | S / Π |
| 反馈与收益 | 事件流、审计链、复盘、收益归因、ChangeSet | E |

所以企业级 Agent 的第一性原则是：

1. **模型负责理解与生成，平台负责执行与合规**。Agent 可以规划，但确定性引擎、权限系统、审批策略和审计链必须执行最终动作。
2. **Agent 不直连业务系统**。Agent 只调用语义能力服务 `cs.*`，由平台完成权限、字段映射、重试、幂等、审计和回滚。
3. **数据平面先于智能体平面**。没有租户、主数据、事件流和审计链，Agent 只能做对话，无法承担组织责任。
4. **岗位先于人格**。企业数字人不是“像人”，而是先有岗位职责、授权范围、绩效指标和红线，再在交互层表现出类人能力。
5. **经营闭环先于自动化片段**。单点自动化不能成为生态；必须围绕获客、转化、服务、续约、履约、回款和复盘形成价值闭环。

### 1.2 UAS 八元组映射

`UAS-Platform = (I, K, R, A, S, G, E, Π)` 在企业生态中应落为：

| 元素 | 企业级含义 | 产品化形态 |
|------|------------|------------|
| **I Intent** | 员工意图、客户意图、经营目标、约束与成功标准 | Intent Hub、Outward Gateway、目标与 SLA 配置 |
| **K Knowledge** | 行业本体、岗位知识、流程、表单、合规、话术、法则包 | Domain Pack、Workflow Pack、Law Pack、Playbook |
| **R Runtime** | 状态隔离、任务编排、幂等执行、回滚、队列 | UAS Runtime Service、AEE、任务沙箱 |
| **A Agent Fabric** | L1/L2/L3 岗位 Agent 与跨部门编排 | SelfPaw Enterprise、ΠPaw Workbench、经营 Agent 编制 |
| **S System Mesh** | 企业系统与业务能力服务化层 | S-Grid / System Mesh、cs.* 语义能力服务、连接器包 |
| **G Governance** | 身份、授权、审批、审计、红线、解释链 | Policy Engine、Approval Gate、Audit Chain |
| **E Evolution** | 反馈、收益归因、策略复盘、ChangeSet 回写 | Evolution Center、KPI Attribution、知识热更新 |
| **Π Protocol** | UIP/A2A/MCP/ASUI 与企业语义协议 | 协议栈、能力合约、事件合约、Agent 包规范 |

---

## 2. 企业主权数据平面：生态的地基

企业级 Agent 生态必须先建立主权数据平面，再允许 Agent 参与经营与履约。

### 2.1 四个不可替代的底座

| 底座 | 作用 | 最小内容 |
|------|------|----------|
| **租户平面** | 隔离组织、业务线、区域、客户数据 | `tenant_id`、组织树、数据域、部署域 |
| **主数据平面** | 统一业务对象和身份 | 客户、联系人、员工、岗位、产品、价格、合同、发票 |
| **事件流平面** | 把业务变化转成可反馈的事实 | `lead_created`、`quote_approved`、`invoice_paid`、`sla_breached` |
| **审计链平面** | 记录谁基于何授权让系统做了什么 | intent、evidence、decision、tool_call、approval、result、rollback |

### 2.2 数据平面与世界模型

世界模型不是额外的“知识库”，而是对企业运行事实的结构化认知：

| 世界模型维度 | 企业表达 |
|--------------|----------|
| **空间** | 组织、区域、渠道、系统边界、数据域 |
| **时间** | SLA、账期、审批时限、销售周期、交付里程碑 |
| **主体** | 员工、客户、合作伙伴、审批人、Agent、组织单元 |
| **客体** | 线索、商机、报价、合同、工单、发票、项目、政策 |
| **感知-行动-反馈** | 事件采集、能力调用、审批结果、客户反馈、收入与风险指标 |

企业数据平面的最低目标不是“全量打通”，而是让关键业务对象进入可审计的反馈闭环。没有反馈，Agent 不会进化；没有审计，Agent 不能进入生产。

---

## 3. cs.* 语义能力服务：Agent 与系统之间的企业契约

Agent 不应直接调用 CRM、BPM、财务或 ERP。UAS 平台应把系统能力翻译为语义能力服务：

```text
Agent / Πpaw
  → cs.customer / cs.lead / cs.quote / cs.approval / cs.invoice / cs.ticket
  → Policy + Mapping + Retry + Audit + Rollback
  → CRM / BPM / ERP / Finance / Data Warehouse
```

### 3.1 能力服务的分层

| 层 | 示例 | 说明 |
|----|------|------|
| **对象能力** | `cs.customer.get_profile`、`cs.invoice.get_status` | 查询或更新标准业务对象 |
| **流程能力** | `cs.approval.start`、`cs.ticket.escalate` | 发起、推进或升级流程 |
| **决策能力** | `cs.pricing.calculate`、`cs.credit.check` | 执行确定性规则或授权模型 |
| **证据能力** | `cs.evidence.collect`、`cs.audit.append` | 归集证据、记录解释链 |
| **经营能力** | `cs.lead.qualify`、`cs.renewal.plan`、`cs.kpi.attribute` | 面向获转服续的业务闭环 |

### 3.2 能力服务合约

每个 `cs.*` 服务必须有稳定合约：

| 合约字段 | 要求 |
|----------|------|
| `intent` | 调用目的，关联原始意图或客户事件 |
| `actor` | 调用主体，含用户、岗位、Agent 与租户 |
| `scope` | 数据与动作边界 |
| `inputs` | 业务对象、字段、证据和上下文 |
| `policy` | 权限、审批、风险和红线 |
| `idempotency_key` | 防重复执行 |
| `audit_ref` | 审计链引用 |
| `result` | 标准化输出、失败原因、可回滚信息 |

这样平台可以做到：Agent 负责规划和解释，UAS 负责把规划约束在企业制度内执行。

---

## 4. L1：SelfPaw Enterprise，员工数字分身

L1 的目标不是替代员工，而是让员工拥有一个组织授权下的第二大脑和任务代理。

### 4.1 六大能力模块

| 模块 | 能力 | 与 L2/L3 的关系 |
|------|------|-----------------|
| **组织身份绑定** | SSO、租户、岗位、数据 scope、委托授权 | 决定能否升级给 Πpaw |
| **Intent Hub** | 识别写、查、办、汇、经营升级类意图 | 经营/跨部门事项转为 Πpaw Task |
| **岗位 Domain 包** | 销售、研发、HR、财务等岗位本体与可用 `cs.*` | 让个人能力受岗位知识约束 |
| **授权内执行** | 填表、查数、发起流程、代拟邮件、整理证据 | 调用低风险 `cs.*` 或生成审批草稿 |
| **个人蜂群决策** | 五视角讨论、风险对冲、决策备忘录 | 向上提交可审计 Evidence |
| **向上汇总** | 周报、异常、阻塞、SLA 风险、客户线索摘要 | 自动创建 L2/L3 任务或升级 |

### 4.2 L1 的产品边界

L1 不应拥有组织全局自由行动权。它的执行边界应满足：

- 只在员工授权、岗位 scope 与租户策略内行动。
- 经营类、跨部门、客户承诺、财务影响和合规敏感事项必须升级到 Πpaw。
- 输出必须携带 Evidence：来源、假设、引用、待确认事项、建议动作。
- 所有自动执行都需要 `audit_ref`，高风险动作需要人类确认或 L2 审批。

### 4.3 L1 到 L2/L3 的升级协议

```text
员工 SelfPaw
  → Intent + Evidence + Scope + Risk
  → Πpaw 职能/经营 Agent
  → cs.*
  → 企业系统与审计链
```

升级不是“转发聊天记录”，而是形成结构化意图单：

| 字段 | 内容 |
|------|------|
| `intent_type` | 查、写、办、汇、升级、异常、客户机会 |
| `business_object` | 客户、合同、发票、工单、候选人、项目等 |
| `evidence` | 文件、对话、系统记录、指标、引用 |
| `requested_outcome` | 希望达成的业务结果 |
| `risk_level` | 低、中、高、红线 |
| `recommended_agent` | L2 职能 Agent 或 L3 经营 Agent |

---

## 5. L2：ΠPaw 职能数字人，对内履约与跨部门协同

L2 是企业内部的数字岗位体系，重点处理跨部门协作、制度执行、资源调度和合规审查。

### 5.1 核心岗位编制

| 岗位 Agent | 职能方向 | 类人能力 | 确定性能力 |
|------------|----------|----------|------------|
| **HR / 招聘 Agent** | 招聘、面试、候选人体验 | 候选人沟通、岗位理解、冲突平衡 | 流程推进、评分规则、合规记录 |
| **财务 Agent** | 报销、开票、回款、预算 | 解释口径、提醒风险 | 精确计算、账期、税务规则 |
| **合规 / 法务 Agent** | 合同、投标、红线 | 专业写作、风险解释 | 条款审查、审批矩阵、留痕 |
| **调度 Agent** | 资源、排期、项目协调 | 协商、优先级解释 | SLA、产能、依赖关系 |
| **经营分析 Agent** | 指标、归因、复盘 | 叙事、洞察生成 | KPI 口径、事件归因、异常检测 |

### 5.2 L2 的核心机制

L2 的产品形态应是 **ΠPaw Workbench**：

- **Task Inbox**：接收 SelfPaw 升级、Outward Gateway 事件和系统异常。
- **Evidence Board**：聚合证据、规则、历史案例、审计引用。
- **Policy Gate**：按角色、金额、客户等级、风险类型做审批与红线拦截。
- **Cross-Agent Dispatch**：跨 HR、财务、法务、交付、客服调度资源。
- **ChangeSet Output**：把复盘建议沉淀为流程、话术、规则、Agent 包或法则包更新。

### 5.3 L2 的组织价值

L2 解决的是企业内部“有人负责但难以协同”的问题：

| 痛点 | L2 响应 |
|------|---------|
| 事项跨部门流转慢 | 用结构化任务和 `cs.approval` 推进 |
| 规则靠人记忆 | 用 Law Pack、Policy Gate 和 Evidence Board 固化 |
| 审批难解释 | 用 audit chain 记录意图、证据、策略和责任 |
| 异常无人归因 | 用 KPI Attribution 和 event stream 做复盘 |

---

## 6. L3：ΠPaw 经营数字人，对外增长与客户闭环

L3 是企业级数字人生态的价值前台。它不只是客服或销售聊天机器人，而是围绕“获、转、服、续”承担经营动作的数字岗位体系。

### 6.1 经营向外的四类闭环

| 闭环 | 目标 | 典型 Agent | 关键 `cs.*` |
|------|------|------------|-------------|
| **获客** | 触达、识别、分层、培育 | 线索培育、渠道伙伴、内容顾问 | `cs.lead.capture`、`cs.lead.qualify` |
| **转化** | 诊断、方案、报价、审批 | 销售顾问、方案顾问、投标 Agent | `cs.customer.diagnose`、`cs.quote.create`、`cs.approval.start` |
| **服务** | 工单、履约、SLA、共情 | 客服、履约、项目协同 Agent | `cs.ticket.create`、`cs.sla.monitor`、`cs.delivery.update` |
| **续约** | 健康度、增购、流失预警 | 客户成功、经营分析 Agent | `cs.renewal.plan`、`cs.kpi.attribute` |

### 6.2 B2B 线索到回款闭环

```text
官网留资
  → cs.lead.qualify
  → 需求诊断
  → cs.quote.create
  → G6 合规审查
  → G3/G4 经营审批
  → 履约任务
  → cs.invoice.issue
  → 回款确认
  → KPI 归因
  → ChangeSet 演化
```

### 6.3 L3 的经营能力模型

经营向外 = **触达 × 履约 × 决策 × 调度**。

| 能力 | Agent 侧 | 平台侧 |
|------|----------|--------|
| 触达 | 话术生成、客户理解、异议处理 | 渠道权限、频控、合规模板 |
| 履约 | 客户共情、进度解释、异常协调 | 工单、SLA、项目、审批 |
| 决策 | 资格判断、报价建议、风险解释 | 定价、信用、审批矩阵 |
| 调度 | 跨岗位协作、资源博弈 | 任务队列、产能、优先级策略 |

L3 的红线是：不得绕开企业授权承诺价格、交期、法律条款或财务动作；所有承诺必须映射到确定性能力服务和审计链。

---

## 7. 平台 + 模型分层：让智能进入生产

企业级数字人生态应采用“模型层 + UAS 平台层 + 数据平面”的清晰分工。

```text
模型层
  通用 LLM + 领域模型 + Embedding + OCR + 语音
        ↓
UAS 平台层
  Agent 平台：世界模型 / AEE / 编排 / 治理 / 演化
  数字基础能力：流程 / 表单 / 权限 / 数据 / 审计
  业务连接器：CRM / BPM / 财务 / ERP / 数据仓库
        ↓
企业主权数据平面
  租户 / 主数据 / 事件流 / 审计链
```

### 7.1 模型层职责

- 理解自然语言、文件、图像、语音和上下文。
- 生成摘要、方案、话术、代码、报告和候选动作。
- 基于领域模型提升特定行业的表达和判断质量。
- 不直接承担最终业务执行责任。

### 7.2 UAS 平台层职责

- 把模型输出转为可验证的 plan、Evidence 和 `cs.*` 调用。
- 执行权限、审批、风控、幂等、重试、审计与回滚。
- 维护世界模型、事件反馈和演化建议。
- 将变更固化为 Domain Pack、Workflow Pack、Law Pack、Connector Pack、Agent Pack。

---

## 8. 产品化封装：把企业差异变成可替换的包

企业落地的关键不是做一个“万能 Agent”，而是把差异封装为可替换、可热更新、可审计的包。

| 封装单元 | 适配方式 | 产出 |
|----------|----------|------|
| **行业 Domain 包** | 切换行业本体、角色、术语、对象生命周期 | `ontology.yaml`、术语表、场景模板 |
| **流程模板包** | 参数化 BPM、Agent 绑定、SLA 与审批 | `workflow_config.json`、表单 schema |
| **能力连接器包** | CRM/BPM/财务 endpoint 与字段映射 | `system_registry.json`、mapping、retry policy |
| **法则包** | 定价、信用、审批矩阵、合规红线热更新 | `governance_policy.json`、rules、thresholds |
| **岗位 Agent 包** | Prompt、工具白名单、KPI、Evidence 要求 | `swarm_agents.json`、skills、eval rubric |
| **经营剧本包** | 获转服续场景路径与复盘模板 | playbook、KPI tree、ChangeSet template |

### 8.1 从项目到生态的生产机制

```text
行业/客户问题
  → 世界模型分析：主体、客体、反馈、约束
  → 选择/生成 Domain Pack + Workflow Pack + Connector Pack
  → 编制 L1/L2/L3 Agent
  → 绑定 cs.* 与治理策略
  → 运行、审计、评估
  → ChangeSet 演化为新包
```

### 8.2 生态市场的最小对象

UAS-AIOS 的企业生态市场不应只卖 Agent，而应售卖可组合资产：

| 资产 | 买方价值 |
|------|----------|
| Domain Pack | 快速进入行业语义 |
| Connector Pack | 降低系统接入成本 |
| Law Pack | 合规与审批可复用 |
| Agent Pack | 快速编制数字岗位 |
| Workflow Pack | 让场景闭环可运行 |
| Evaluation Pack | 让交付可验收、可复盘 |

---

## 9. 治理与演化：企业可用性的分水岭

企业级 Agent 生态必须把治理和演化设计为一等公民，而不是上线后的附属能力。

### 9.1 治理分级

| 级别 | 适用动作 | 控制方式 |
|------|----------|----------|
| **G0 只读** | 查询、摘要、检索 | scope + audit |
| **G1 草稿** | 邮件、报告、报价草案 | 人工确认 |
| **G2 低风险执行** | 填表、创建任务、发起流程 | 授权内自动执行 + 可回滚 |
| **G3 经营承诺** | 报价、交期、客户承诺 | 审批矩阵 + 证据链 |
| **G4 财务/法务影响** | 开票、合同、信用、付款 | 强审批 + 红线规则 |
| **G5 外部承诺自动化** | 对客户或伙伴的可执行承诺 | 双人审批或策略豁免 |
| **G6 禁止区** | 违法、越权、歧视、泄密 | 拦截 + 安全审计 |

### 9.2 演化闭环

企业级演化不是“让 Agent 自己改 prompt”，而是经过治理的 ChangeSet：

```text
业务事件 / 人工反馈 / KPI 偏差
  → 归因：数据、流程、话术、规则、Agent、连接器
  → 生成 ChangeSet
  → G 审批
  → 回写 Domain / Workflow / Law / Agent / Connector Pack
  → 下一轮运行验证
```

### 9.3 收益归因

每个 L2/L3 Agent 都应绑定收益或风险指标：

| 指标类型 | 示例 |
|----------|------|
| 收入 | 线索转化率、平均合同额、续约率、回款周期 |
| 成本 | 人工处理时长、重复沟通次数、跨部门等待时长 |
| 风险 | 合规拦截数、错误承诺数、审批超时、SLA 违约 |
| 体验 | 客户满意度、员工采纳率、候选人体验、客服一次解决率 |

没有收益归因，Evolution 只能优化局部体验，无法支撑商业闭环。

---

## 10. 商业落地闭环

### 10.1 产品线

| 产品 | 目标客户 | 核心交付 |
|------|----------|----------|
| **UAS Open Protocol** | 开发者、技术决策者、SI | ASUI/UIP/能力合约、参考实现、模板 |
| **SelfPaw Enterprise** | 组织内知识工作者 | L1 个人数字分身、Intent Hub、岗位 Domain 包 |
| **ΠPaw Workbench** | 职能部门与运营团队 | L2 职能数字人、任务台、证据板、审批与复盘 |
| **ΠPaw Growth & Service** | 销售、客服、客户成功、渠道 | L3 经营数字人、获转服续闭环 |
| **UAS Data & Governance Plane** | CIO、合规、IT、数据团队 | 主权数据平面、审计链、Policy Engine |
| **UAS Pack Marketplace** | 行业伙伴、SI、客户内部 CoE | Domain/Workflow/Law/Connector/Agent Pack |

### 10.2 落地路径

| 阶段 | 目标 | 验收标准 |
|------|------|----------|
| **P0 单场景闭环** | 选一个高频、高痛、高审计需求场景 | 从 intent 到 `cs.*` 到报告和审计链可跑通 |
| **P1 单部门数字岗位** | 编制 1-3 个 L2/L3 Agent | 有岗位 KPI、审批策略和事件反馈 |
| **P2 跨部门履约** | 打通 L1 SelfPaw 升级与 L2/L3 调度 | 意图单、Evidence、任务流和回滚可追踪 |
| **P3 经营闭环** | 覆盖获转服续或履约回款链路 | 有收益归因和 ChangeSet 演化 |
| **P4 生态复制** | 封装为行业包与连接器包 | 新客户通过包组合快速复用 |

### 10.3 标杆场景选择

优先选择满足以下条件的场景：

1. 有清晰业务对象：客户、线索、工单、合同、发票、候选人等。
2. 有高频流程和明确 SLA。
3. 有合规、审计或复盘刚需。
4. 有可量化收益指标。
5. 可以通过 `cs.*` 能力服务逐步替换人工系统操作。

建议优先级：

| 场景 | 原因 |
|------|------|
| B2B 线索到回款 | 经营价值链完整，适合 L3 验证 |
| 客服工单到续约 | 高频、可审计、客户体验可量化 |
| AI 招聘 OS | 已有项目基础，适合 L2 职能闭环 |
| 财务开票与回款 | 规则清晰、审计强、ROI 易度量 |

---

## 11. 实施状态矩阵

| 能力 | 目标态 | 当前仓库状态 | 推进方式 |
|------|--------|--------------|----------|
| ASUI 知识底座 | 企业知识、流程、规则可配置 | 已有 ASUI 文档、模板与示例 | 继续标准化 pack 结构 |
| Πpaw / UAS-S | 多岗位 Agent 编排与业务运行时 | 部分实现，`projects/*` 与运行时可用 | 先做 L2/L3 场景闭环 |
| selfpaw / UAS-U | 企业版个人数字分身 | 模板/示例级，平台 U 层未实现 | 先定义 Intent Hub 与升级协议 |
| 主权数据平面 | 租户、主数据、事件流、审计链 | 审计与状态有雏形，主数据/事件流不足 | 从关键业务对象开始 |
| cs.* 能力服务 | Agent 与系统的语义契约 | 当前多为系统 registry / script gateway | 增加能力合约与映射层 |
| 治理分级 | G0-G6 风险控制 | governance_policy 有基础 | 补审批矩阵和红线策略 |
| 演化回写 | ChangeSet 经治理回写 pack | 演化建议有，自动/半自动回写不足 | 引入 ChangeSet 协议 |
| 收益归因 | KPI 反馈驱动演化 | 文档与路线图为主 | 在标杆场景绑定指标 |

---

## 12. 与现有文档的关系

| 文档 | 本文关系 |
|------|----------|
| [THEORY_SYSTEM.md](./THEORY_SYSTEM.md) | 方法论总纲：道德势术器、价值闭环、世界模型、双轨 AGI |
| [AGI_WORLD_MODEL_UAS.md](./AGI_WORLD_MODEL_UAS.md) | 双轨 AGI 与世界模型的形式化来源 |
| [UAS_PLATFORM_STANDARD.md](./UAS_PLATFORM_STANDARD.md) | UAS 八元组、平台标准与运行时入口 |
| [ASUI_ARCHITECTURE.md](./ASUI_ARCHITECTURE.md) | 知识即配置、构建即运行、增量演化的技术底座 |
| [ASUI_AUTONOMOUS_AGENT_STANDARD.md](./ASUI_AUTONOMOUS_AGENT_STANDARD.md) | sub uas app 的工作流与强制约定 |
| [UAS_ASUI_PROTOCOL_GAPS_AND_ROADMAP.md](./UAS_ASUI_PROTOCOL_GAPS_AND_ROADMAP.md) | 协议化、智能化推演和演化回写的差距与路线 |
| [THEORY_ARCHITECTURE_CONSISTENCY_AUDIT.md](./THEORY_ARCHITECTURE_CONSISTENCY_AUDIT.md) | 区分已实现、部分实现和规划态能力 |
| [UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md](./UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md) | 产品方案、功能清单、工程架构、模块设计与 MVP |
| [UAS_AIOS_ENTERPRISE_VISUAL_BLUEPRINT.md](./UAS_AIOS_ENTERPRISE_VISUAL_BLUEPRINT.md) | 架构理念、产品定义、功能设计与 MVP 的图形化总览 |
| [enterprise-sales-os/README.md](./enterprise-sales-os/README.md) | B2B 线索到报价审批 MVP 的开发规约包 |
| [商业经营/COMPANY_OPERATING_STRATEGY.md](./商业经营/COMPANY_OPERATING_STRATEGY.md) | 商业定位、客户场景与开源-商业双轨 |

---

## 13. 一句话总括

企业级数字人生态的本质是：以企业主权数据平面为地基，以 `cs.*` 语义能力服务为执行契约，以 selfpaw 承接个人授权与证据，以 Πpaw 编制职能与经营数字岗位，最终在获、转、服、续、履约、回款、复盘中形成可审计、可回滚、可演化的组织智能闭环。
