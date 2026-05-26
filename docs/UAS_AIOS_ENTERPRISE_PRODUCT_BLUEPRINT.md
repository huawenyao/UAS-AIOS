# UAS-AIOS 企业级产品蓝图：产品方案、功能清单、工程架构与模块设计

> 本文将 [UAS-AIOS L1-L3 企业级 Agent 生态体系](./UAS_AIOS_ENTERPRISE_AGENT_ECOSYSTEM_L1_L3.md) 收敛为可落地的产品方案：明确产品边界、功能模块、技术工程架构、数据与能力合约、MVP 切入和验收标准。
> B2B 线索到报价审批 MVP 的开发规约见 [Enterprise Sales OS MVP 开发规约包](./enterprise-sales-os/README.md)。
> 图形化总览见 [UAS-AIOS 企业级可视化蓝图](./UAS_AIOS_ENTERPRISE_VISUAL_BLUEPRINT.md)。

---

## 0. 产品收敛原则

企业级 UAS-AIOS 不应以“聊天入口”作为产品中心，而应以 **组织任务闭环** 为中心：

```text
业务事件 / 员工意图 / 客户意图
  → Intent Hub
  → Evidence + Scope + Policy
  → Agent Workbench
  → cs.* Capability Service
  → System Mesh
  → Audit + KPI + ChangeSet
```

### 0.1 产品一句话

**UAS Enterprise 是一个把企业知识、流程、系统能力和数字岗位编制到同一治理闭环中的 Agent 操作系统。**

### 0.2 不做什么

| 非目标 | 原因 |
|--------|------|
| 不做通用大模型 | 模型层作为可替换能力，不是 UAS 的护城河 |
| 不做纯 Agent 编排框架 | 编排会被基础模型平台吸收，UAS 聚焦企业语义、治理和执行 |
| 不做单系统 Copilot | 企业价值来自跨系统、跨岗位、跨流程的闭环 |
| 不让 Agent 直连 CRM/ERP | 生产动作必须经过能力服务、权限、审计和回滚 |

---

## 1. 产品套件

### 1.1 产品线总览

| 产品 | 用户 | 解决的问题 | 交付形态 |
|------|------|------------|----------|
| **SelfPaw Enterprise** | 员工、经理、知识工作者 | 写、查、办、汇、个人证据整理与升级 | Web/桌面侧边栏、浏览器插件、企业 IM 入口 |
| **ΠPaw Workbench** | 职能部门、运营、管理者 | L2 职能任务台、跨部门调度、证据与审批 | Web 工作台、任务队列、审批台 |
| **ΠPaw Growth & Service** | 销售、客服、客户成功、渠道 | L3 获转服续、履约、续约、回款闭环 | 对外会话网关 + 经营工作台 |
| **UAS Data & Governance Plane** | CIO、IT、合规、数据团队 | 租户、权限、主数据、审计、策略、红线 | 管理后台、策略中心、审计中心 |
| **UAS Capability Hub** | IT、系统集成商、平台团队 | `cs.*` 语义能力服务、连接器、字段映射 | API 网关、连接器管理、能力目录 |
| **UAS Pack Studio** | 业务专家、实施顾问、生态伙伴 | Domain/Workflow/Law/Agent/Connector Pack 的配置与发布 | 低代码配置台、版本管理、发布审核 |

### 1.2 产品关系

```text
SelfPaw Enterprise
  └─ 提交 Intent + Evidence
      ↓
ΠPaw Workbench / ΠPaw Growth & Service
  └─ 编排岗位 Agent + 调用 cs.*
      ↓
UAS Capability Hub
  └─ 翻译到 CRM / BPM / ERP / Finance / Data Warehouse
      ↓
UAS Data & Governance Plane
  └─ 统一身份、权限、审计、事件、KPI、ChangeSet
      ↑
UAS Pack Studio
  └─ 将复盘沉淀为可复用 Pack
```

---

## 2. 核心用户与使用场景

| 用户 | 典型任务 | 核心界面 | 成功标准 |
|------|----------|----------|----------|
| 员工 | 查客户、写邮件、发起流程、整理周报 | SelfPaw Inbox / Intent Hub | 少切系统、少重复写、证据可追溯 |
| 销售 | 线索诊断、方案报价、审批推进 | Growth Workspace | 转化率提升、报价合规、跟进不遗漏 |
| 客服 | 工单摘要、SLA 预警、升级协同 | Service Workspace | 首响更快、升级明确、客户体验可量化 |
| 职能专员 | 招聘、财务、合规、调度 | ΠPaw Task Board | 跨部门任务可追踪、审批可解释 |
| 经理 | 异常、瓶颈、KPI 归因、复盘 | Operating Console | 能看到原因、责任、建议和 ChangeSet |
| IT / 合规 | 权限、连接器、审计、红线 | Governance Console | 可控、可审计、可回滚、可停用 |
| 业务专家 | 维护领域规则、流程、话术、评估 | Pack Studio | 不改代码也能迭代业务能力 |

---

## 3. 功能清单

### 3.1 SelfPaw Enterprise

| 模块 | P0 | P1 | P2 |
|------|----|----|----|
| 组织身份绑定 | SSO、租户、岗位、scope 注入 | 委托授权、临时权限 | 跨组织身份与项目身份 |
| Intent Hub | 写/查/办/汇/升级分类 | 意图模板与收藏 | 主动意图建议 |
| Evidence Capture | 文件、网页、系统记录、对话摘录 | 证据可信度与引用规范 | 证据图谱 |
| 个人执行 | 草稿、摘要、表单预填、低风险流程发起 | 自动批处理 | 个性化任务策略 |
| 升级协议 | Intent 单、Evidence、Risk、推荐 Agent | 升级 SLA 与状态追踪 | 自动选择最优路径 |
| 个人蜂群决策 | 五视角决策备忘录 | 团队协作评审 | 与组织世界模型对齐 |

### 3.2 ΠPaw Workbench

| 模块 | P0 | P1 | P2 |
|------|----|----|----|
| Task Inbox | SelfPaw 升级、系统异常、外部事件接入 | 队列优先级与 SLA | 自动分派与负载均衡 |
| Evidence Board | 证据聚合、引用、规则匹配 | 证据冲突检测 | 主客体推演视图 |
| Agent Dispatch | 单 Agent 处理、人工接管 | 多 Agent 协同 | 跨部门资源博弈与调度 |
| Approval Gate | 审批矩阵、红线拦截 | 条件审批与豁免 | 策略仿真 |
| Report & Decision Memo | 结构化结论、风险、下一步 | 经理视图与复盘模板 | 自动生成 ChangeSet |
| KPI Attribution | 基础时效、成功/失败状态 | 归因树 | 收益反哺演化 |

### 3.3 ΠPaw Growth & Service

| 模块 | P0 | P1 | P2 |
|------|----|----|----|
| Outward Gateway | 官网表单、企业 IM、邮件入口 | 多渠道会话路由 | 渠道频控与客户画像 |
| Lead Qualification | 线索分层、资格判断 | 商机评分 | 增长实验 |
| Solution & Quote | 需求诊断、方案草案、报价草案 | 定价规则、折扣审批 | 多方案模拟 |
| Service & SLA | 工单摘要、SLA 监控、升级 | 履约协同 | 客户健康度预测 |
| Renewal & Upsell | 续约提醒、风险提示 | 续约计划与客户成功 playbook | 增购推荐 |
| Customer Audit Trail | 客户承诺、审批、交付记录 | 客户时间线 | 经营复盘 |

### 3.4 Data & Governance Plane

| 模块 | P0 | P1 | P2 |
|------|----|----|----|
| Tenant & Identity | 租户、组织、用户、岗位、角色 | 多业务线隔离 | 跨租户模板复用 |
| Scope & Policy | 数据 scope、动作 scope、G0-G6 风险分级 | 动态策略 | 策略仿真与回放 |
| Audit Chain | intent、evidence、decision、tool_call、approval、result | 可视化审计链 | 审计问答与异常检测 |
| Master Data | 客户、员工、产品、合同、发票最小模型 | 主数据同步与冲突处理 | 语义主数据 |
| Event Stream | 关键业务事件入库 | 事件订阅与规则触发 | 事件驱动演化 |
| ChangeSet Center | 演化建议、人工审核 | 回写 Pack | A/B 验证与回滚 |

### 3.5 Capability Hub

| 模块 | P0 | P1 | P2 |
|------|----|----|----|
| Capability Catalog | `cs.customer`、`cs.lead`、`cs.approval`、`cs.ticket`、`cs.invoice` | 能力版本与依赖 | 能力市场 |
| Connector Runtime | HTTP/script/MCP connector | 队列、重试、幂等 | 多环境发布 |
| Field Mapping | 标准对象到系统字段映射 | 映射测试 | 自动映射建议 |
| Policy Adapter | 调用前权限与风险检查 | 细粒度字段级控制 | 策略解释 |
| Tool Result Normalizer | 标准结果、错误、回滚信息 | 异常分类 | 自愈与降级 |

### 3.6 Pack Studio

| Pack | P0 | P1 | P2 |
|------|----|----|----|
| Domain Pack | 本体、术语、角色、对象生命周期 | 行业包模板 | 生态认证 |
| Workflow Pack | 流程、表单、SLA、Agent 绑定 | 流程版本化 | 流程仿真 |
| Law Pack | 审批矩阵、红线、定价/信用规则 | 热更新与回滚 | 策略评估 |
| Agent Pack | prompt、工具白名单、KPI、输出 schema | Agent 测试集 | Agent 发布市场 |
| Connector Pack | endpoint、mapping、retry policy | 多环境配置 | SI 伙伴包 |
| Evaluation Pack | 验收脚本、指标、rubric | 场景基准集 | 持续评估 |

---

## 4. 技术工程架构

### 4.1 分层架构

```text
┌──────────────────────────────────────────────────────────────┐
│ Experience Layer                                             │
│ SelfPaw UI / ΠPaw Workbench / Growth & Service / Admin       │
├──────────────────────────────────────────────────────────────┤
│ Agent Application Layer                                      │
│ Intent Hub / Task Board / Evidence Board / Agent Dispatch    │
├──────────────────────────────────────────────────────────────┤
│ UAS Core Runtime                                             │
│ Context Injector / Orchestrator / State Store / Queue / AEE   │
├──────────────────────────────────────────────────────────────┤
│ Governance & Evolution Plane                                 │
│ Policy Engine / Audit Chain / Approval Gate / ChangeSet       │
├──────────────────────────────────────────────────────────────┤
│ Capability Service Layer                                     │
│ cs.* API / Connector Runtime / Field Mapping / Result Normal  │
├──────────────────────────────────────────────────────────────┤
│ Sovereign Data Plane                                         │
│ Tenant / Identity / Master Data / Event Stream / KPI Store    │
├──────────────────────────────────────────────────────────────┤
│ Enterprise Systems                                           │
│ CRM / BPM / ERP / Finance / Data Warehouse / Document System  │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 运行时主路径

```text
1. Capture
   用户/客户/系统事件进入 Intent Hub 或 Outward Gateway
2. Normalize
   标准化 intent、actor、tenant、business_object、evidence
3. Govern
   Policy Engine 判断 scope、risk、approval requirement
4. Plan
   Orchestrator 选择 Agent、Pack、workflow 与 cs.* 能力
5. Execute
   Capability Hub 执行确定性动作，写入 audit chain
6. Observe
   Event Stream 与 KPI Store 记录结果和反馈
7. Evolve
   ChangeSet Center 生成、审批、回写 Pack
```

### 4.3 逻辑服务划分

| 服务 | 职责 | 对应现有资产 |
|------|------|--------------|
| `intent-service` | 意图分类、结构化意图单、升级路由 | workflow 的 intent_activation |
| `evidence-service` | 证据采集、引用、可信度、证据包 | docs/skills + audit 扩展 |
| `agent-orchestrator` | Agent 选择、计划、步骤执行、结果合成 | autonomous_agent runtime |
| `task-service` | L2/L3 任务、队列、SLA、状态机 | UAS Runtime Service queue |
| `policy-service` | scope、G0-G6、审批矩阵、红线 | governance_policy |
| `approval-service` | 人工审批、豁免、会签、审批结果 | governance_check |
| `capability-service` | `cs.*` 合约、调用、幂等、重试、回滚 | system_registry + ToolGateway |
| `connector-service` | CRM/BPM/ERP/Finance 连接器 | MCP/script gateway |
| `audit-service` | 审计事件、解释链、回放 | AuditEngine |
| `event-service` | 业务事件流、订阅、触发 | 待扩展 |
| `kpi-service` | 指标、归因、收益反馈 | evolution_policy 扩展 |
| `changeset-service` | 演化建议、审批、Pack 回写 | EvolutionEngine 扩展 |
| `pack-registry` | Domain/Workflow/Law/Agent/Connector/Evaluation Pack | ASUI configs/skills |

### 4.4 部署形态

| 形态 | 适用 | 特点 |
|------|------|------|
| 单租户私有化 | 合规敏感企业 | 数据不出域，连接企业内网系统 |
| 混合部署 | 多数中大型企业 | 控制面托管，数据面和连接器私有 |
| 托管 SaaS | 中小团队和试点 | 快速试用，连接云端 SaaS |
| SI 交付包 | 行业伙伴 | Pack + Connector + Runtime 的项目化交付 |

---

## 5. 核心数据模型

### 5.1 关键实体

| 实体 | 关键字段 | 说明 |
|------|----------|------|
| `Tenant` | `tenant_id`、`region`、`deployment_mode` | 租户与数据域 |
| `Actor` | `actor_id`、`type`、`roles`、`delegations` | 人、Agent、系统主体 |
| `Scope` | `data_scope`、`action_scope`、`expiry` | 授权边界 |
| `Intent` | `intent_id`、`type`、`goal`、`success_criteria` | 意图单 |
| `BusinessObject` | `object_type`、`object_id`、`lifecycle_state` | 客户、线索、合同等 |
| `Evidence` | `evidence_id`、`source`、`hash`、`confidence` | 证据与引用 |
| `Task` | `task_id`、`owner_agent`、`sla`、`status` | L2/L3 任务 |
| `Decision` | `decision_id`、`rationale`、`risk_level` | 决策备忘录 |
| `CapabilityCall` | `capability`、`inputs`、`result`、`rollback_ref` | `cs.*` 调用 |
| `AuditEvent` | `event_type`、`actor`、`target`、`timestamp` | 审计链 |
| `KPIEvent` | `metric`、`value`、`attribution_ref` | 收益与风险归因 |
| `ChangeSet` | `target_pack`、`diff`、`approval_status` | 演化回写 |

### 5.2 标准意图单

```yaml
intent_id: int_20260524_001
tenant_id: tenant_acme
actor:
  actor_id: user_123
  roles: [sales_manager]
intent_type: customer_followup
business_object:
  type: lead
  id: lead_456
goal: "判断是否应进入报价流程"
success_criteria:
  - "线索资格判断有证据"
  - "若进入报价，生成审批草案"
scope:
  data_scope: ["crm.leads.assigned", "crm.accounts.read"]
  action_scope: ["cs.lead.qualify", "cs.quote.draft"]
evidence_refs:
  - ev_call_summary_001
  - ev_form_submission_002
risk_level: G2
requested_agent: ppaw_sales_advisor
```

### 5.3 `cs.*` 能力调用合约

```yaml
capability: cs.lead.qualify
version: v1
tenant_id: tenant_acme
actor:
  type: agent
  id: ppaw_sales_advisor
on_behalf_of: user_123
intent_ref: int_20260524_001
idempotency_key: int_20260524_001:lead_456:qualify
inputs:
  lead_id: lead_456
  evidence_refs: [ev_call_summary_001, ev_form_submission_002]
policy:
  required_scope: ["crm.leads.assigned"]
  max_risk_level: G2
audit:
  audit_ref: audit_789
result_contract:
  status: qualified | disqualified | needs_human_review
  score: number
  reasons: string[]
  next_capabilities: string[]
  rollback_ref: string | null
```

---

## 6. 模块设计

### 6.1 Intent Hub

| 项 | 设计 |
|----|------|
| 输入 | 自然语言、表单、外部事件、系统异常 |
| 输出 | 标准意图单、风险等级、推荐 Agent、Evidence 要求 |
| 关键逻辑 | 意图分类、业务对象识别、scope 绑定、升级判断 |
| 依赖 | Identity、Domain Pack、Policy Engine |
| 验收 | 80% 常见员工意图能结构化为可路由任务 |

### 6.2 Evidence Board

| 项 | 设计 |
|----|------|
| 输入 | 文档、系统记录、对话、表单、审计事件 |
| 输出 | 证据包、引用列表、冲突提示、可信度 |
| 关键逻辑 | 来源标准化、hash、引用、证据与结论绑定 |
| 依赖 | Master Data、Audit Chain、Document Connector |
| 验收 | 任意决策都能回溯到证据与规则 |

### 6.3 Agent Orchestrator

| 项 | 设计 |
|----|------|
| 输入 | 意图单、Evidence、Policy、可用 Agent 与 Pack |
| 输出 | 执行计划、Agent 步骤、结果合成、下一步动作 |
| 关键逻辑 | Agent 选择、工具白名单、状态隔离、失败重试 |
| 依赖 | Runtime、Agent Pack、Capability Hub |
| 验收 | 每一步有状态、有审计、有可恢复点 |

### 6.4 Policy Engine

| 项 | 设计 |
|----|------|
| 输入 | actor、scope、intent、business_object、capability |
| 输出 | allow / deny / approval_required / redact |
| 关键逻辑 | G0-G6 风险分级、审批矩阵、字段级权限、红线 |
| 依赖 | Identity、Law Pack、Audit Chain |
| 验收 | 高风险动作不会绕开审批或审计 |

### 6.5 Capability Hub

| 项 | 设计 |
|----|------|
| 输入 | `cs.*` 标准合约 |
| 输出 | 标准化执行结果、错误、rollback_ref、audit_ref |
| 关键逻辑 | 字段映射、连接器调用、幂等、重试、结果归一化 |
| 依赖 | Connector Pack、System Mesh、Policy Engine |
| 验收 | Agent 不知道底层 CRM/ERP 字段也能完成业务动作 |

### 6.6 Task Board

| 项 | 设计 |
|----|------|
| 输入 | SelfPaw 升级、客户事件、系统异常、Agent 子任务 |
| 输出 | 任务状态、SLA、责任人、下一步、升级记录 |
| 关键逻辑 | 状态机、队列、SLA、人工接管、跨 Agent 协同 |
| 依赖 | Runtime Queue、Identity、Notification |
| 验收 | 跨部门任务不靠聊天流转，能追踪责任和状态 |

### 6.7 ChangeSet Center

| 项 | 设计 |
|----|------|
| 输入 | KPI 偏差、人工反馈、失败任务、审计异常 |
| 输出 | Pack diff、影响范围、审批请求、回滚点 |
| 关键逻辑 | 归因、建议生成、人工确认、版本化回写 |
| 依赖 | Evolution Engine、Pack Registry、Policy Engine |
| 验收 | 演化建议能进入受控发布，而不是停留在报告里 |

---

## 7. MVP 产品方案

### 7.1 首个闭环：B2B 线索到报价审批

选择该闭环作为 MVP，是因为它同时覆盖 L1、L2、L3、`cs.*`、治理、审计和经营指标。

```text
官网线索 / 销售录入
  → Outward Gateway
  → ΠPaw Sales Advisor
  → cs.lead.qualify
  → SelfPaw 销售经理补证据
  → cs.quote.draft
  → Policy Engine 判断 G3/G4
  → ΠPaw Compliance / Finance 审批
  → 报价草案 + 审计链 + KPI 记录
```

### 7.2 MVP 功能范围

| 范围 | 必须包含 |
|------|----------|
| 入口 | 官网表单 mock、员工录入、SelfPaw 升级 |
| Agent | Sales Advisor、Compliance Reviewer、Finance Reviewer |
| 能力服务 | `cs.lead.qualify`、`cs.quote.draft`、`cs.approval.start`、`cs.audit.append` |
| 数据 | Tenant、Actor、Lead、Quote、Evidence、Task、AuditEvent |
| 治理 | G0-G4、报价金额阈值、折扣阈值、客户等级 |
| 输出 | 资格判断、报价草案、审批任务、审计报告、KPI 摘要 |
| 演化 | 失败原因和人工反馈生成 ChangeSet 草案 |

### 7.3 MVP 不包含

| 暂不包含 | 原因 |
|----------|------|
| 全量 CRM 双向同步 | 先用关键对象与 mock connector 验证闭环 |
| 自动发送客户报价 | 外部承诺需等治理与审批成熟 |
| 多行业 Pack 市场 | 先验证一个 B2B 销售场景 |
| 全自动演化回写 | MVP 阶段只生成 ChangeSet 草案 |

### 7.4 验收标准

| 指标 | 标准 |
|------|------|
| 业务闭环 | 从 lead 到 quote approval task 全链路跑通 |
| 审计 | 任意报价草案可追溯 intent、evidence、policy、capability call |
| 治理 | 超阈值报价必须进入审批，不得自动承诺客户 |
| 可配置 | 修改定价/审批规则无需改 Agent 代码 |
| 可演化 | 至少输出一条可审查的 ChangeSet 建议 |
| 可复用 | 新增另一个销售场景时复用 70% 以上模块与合约 |

开发前置规约已拆分为：[领域模型](./enterprise-sales-os/DOMAIN_MODEL.md)、[能力服务合约](./enterprise-sales-os/CAPABILITY_CONTRACTS.md)、[治理矩阵](./enterprise-sales-os/GOVERNANCE_MATRIX.md)、[状态机](./enterprise-sales-os/WORKFLOW_STATE_MACHINE.md)、[世界模型配置](./enterprise-sales-os/WORLD_MODEL_CONFIG.md)、[反馈与 ChangeSet](./enterprise-sales-os/FEEDBACK_CHANGESET.md)、[验收用例](./enterprise-sales-os/MVP_ACCEPTANCE_CASES.md)。

---

## 8. 工程目录建议

面向当前仓库，可先以文档、配置和参考实现推进，不必一次性拆成微服务。

```text
projects/enterprise-sales-os/
├── CLAUDE.md
├── .claude/
│   └── skills/
├── configs/
│   ├── platform_manifest.json
│   ├── workflow_config.json
│   ├── swarm_agents.json
│   ├── governance_policy.json
│   ├── evolution_policy.json
│   ├── system_registry.json
│   ├── world_model.json
│   ├── capability_catalog.json
│   └── field_mapping.json
├── database/
│   ├── audit/
│   ├── events/
│   ├── feedback/
│   └── state/
├── scripts/
│   ├── cs_lead_qualify.py
│   ├── cs_quote_draft.py
│   ├── cs_approval_start.py
│   └── evaluate_sales_loop.py
├── docs/
│   ├── PRODUCT_BLUEPRINT.md
│   ├── DOMAIN_MODEL.md
│   ├── CAPABILITY_CONTRACTS.md
│   ├── GOVERNANCE_MATRIX.md
│   ├── WORKFLOW_STATE_MACHINE.md
│   ├── WORLD_MODEL_CONFIG.md
│   ├── FEEDBACK_CHANGESET.md
│   ├── MVP_ACCEPTANCE_CASES.md
│   └── RUNBOOK.md
└── reports/
```

### 8.1 与现有 UAS Runtime 的对齐

| 现有标准资产 | 企业销售 OS 扩展 |
|--------------|------------------|
| `workflow_config.json` | 增加 lead qualification、quote draft、approval、audit report |
| `swarm_agents.json` | 定义 Sales Advisor、Compliance Reviewer、Finance Reviewer |
| `governance_policy.json` | 增加 G0-G4、金额/折扣/客户等级矩阵 |
| `system_registry.json` | 注册 `cs.*` 脚本或 connector |
| `evolution_policy.json` | 读取 KPI 与人工反馈，生成 ChangeSet 草案 |

---

## 9. 版本路线

| 版本 | 目标 | 关键产物 |
|------|------|----------|
| **v0.1 文档蓝图** | 产品、架构、合约、模块边界明确 | 本文 + 生态总纲 |
| **v0.2 配置原型** | enterprise-sales-os subapp 可被 runtime 发现 | 开发规约包 + configs + mock scripts |
| **v0.3 闭环 MVP** | lead→quote→approval→audit 可运行 | 运行报告 + 审计链 |
| **v0.4 治理增强** | G0-G4、字段级 scope、审批矩阵 | policy tests |
| **v0.5 Pack 化** | Domain/Workflow/Law/Agent/Connector Pack 可复用 | pack registry |
| **v1.0 企业试点** | 接入真实 CRM/BPM/财务系统的受控试点 | connector + runbook |

---

## 10. 与生态总纲的关系

| 生态总纲问题 | 本文落地答案 |
|--------------|--------------|
| L1-L3 是什么 | SelfPaw Enterprise、ΠPaw Workbench、ΠPaw Growth & Service |
| `cs.*` 如何产品化 | Capability Hub + Capability Catalog + Connector Runtime |
| 主权数据平面如何落地 | Tenant、Identity、Master Data、Event、Audit、KPI、ChangeSet |
| 治理如何成为生产能力 | Policy Engine、Approval Service、Audit Chain、G0-G6 |
| 演化如何不失控 | ChangeSet Center + Pack Registry + 人工审批回写 |
| MVP 从哪里切入 | B2B 线索到报价审批闭环 |

---

## 11. 一句话总括

企业级 UAS-AIOS 的具体产品方案是：以 SelfPaw Enterprise 做个人意图与证据入口，以 ΠPaw Workbench 和 Growth & Service 承接职能与经营数字岗位，以 Data & Governance Plane 保证主权数据和审计治理，以 Capability Hub 把企业系统封装为 `cs.*`，以 Pack Studio 和 ChangeSet Center 把每次业务运行沉淀为可复用、可演化的组织能力。
