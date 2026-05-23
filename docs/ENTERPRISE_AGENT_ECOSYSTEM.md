# UAS-AIOS 企业级 Agent 生态体系

> **版本**：v1.0.0 | **路径**：`enterprise/` | **CLI 模板**：`asui init <name> -t enterprise`

---

## 一、第一性方法论：道德势术器映射

```
道（Tao）— 企业主权数据平面
  └── enterprise/platform/data_plane/
       ├── tenant_manager.py   # 租户隔离 + 岗位绑定
       ├── event_stream.py     # 领域事件流（不可变）
       └── audit_chain.py      # 不可篡改审计链

德（De）— 业务能力服务化 cs.*
  └── enterprise/platform/capability_services/
       ├── cs_gateway.py       # 语义网关（权限→执行→审计）
       ├── cs_customer.py      # 客户服务（资格判断/档案/健康分）
       ├── cs_approval.py      # 审批服务（矩阵路由/多级流转）
       ├── cs_invoice.py       # 开票服务（申请/开票/回款）
       ├── cs_finance.py       # 财务服务（报价/收入确认/KPI归因）
       └── cs_bpm.py           # 流程服务（BPM 语义封装）

势（Shi）— 双轨 AGI（SelfPaw × ΠPaw）差异对比
  ├── SelfPaw：员工数字分身（对内：写·查·办·汇）
  └── ΠPaw：经营数字岗位（对外：获·转·服·续）

术（Shu）— 三层数字人架构
  └── enterprise/agents/
       ├── l1_selfpaw/         # 个人数字分身（六大能力）
       ├── l2_pipaw/           # 职能数字人（HR/财务/合规）
       └── l3_pipaw/           # 经营数字人（销售/客服/投标）

器（Qi）— 产品化封装
  ├── enterprise/domain_packages/  # 行业 Domain 包
  ├── enterprise/workflow_templates/  # 流程模板包
  └── asui-cli 模板 enterprise     # CLI 脚手架
```

---

## 二、平台 + 模型分层

```
┌─────────────────────────────────────────────────────┐
│  模型层                                               │
│  通用 LLM + 领域模型 + 嵌入/OCR/语音                 │
└─────────────────────┬───────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  平台层（UAS）                                        │
│  ┌─────────────────────────────────────────────┐    │
│  │ Agent 平台                                   │    │
│  │ 世界模型 · cs.* AEE · 编排 · 治理 · 演化     │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │ 数字基础能力                                  │    │
│  │ 流程 · 表单 · 权限 · 数据                    │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │ 业务连接器 S-Grid                            │    │
│  │ CRM / BPM / 财务 / ERP                      │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  数据平面                                             │
│  租户 · 主数据 · 事件流 · 审计链                     │
└─────────────────────────────────────────────────────┘
```

**核心原则**：Agent 不直连 CRM/BPM，只调用语义能力服务 cs.*，由平台做权限、翻译、审计、重试。

---

## 三、三层数字人详解

### 3.1 L1 SelfPaw 企业版（个人数字分身）

**定位**：员工数字分身，第二大脑 + 任务代理 + 向上汇总

| # | 能力模块 | 实现 | 说明 |
|---|---------|------|------|
| 1 | 组织身份绑定 | `TenantManager` | SSO + 租户 + 岗位 + 数据 scope |
| 2 | Intent Hub | `IntentHub` | 意图识别；经营类一键升级 ΠPaw |
| 3 | 岗位 Domain 包 | `get_domain_ontology()` | 销售/HR/财务等 Ontology + cs.* 白名单 |
| 4 | 授权内执行 | `call_service()` / `draft_email()` | 填表/发起流程/代拟邮件 |
| 5 | 个人蜂群决策 | `SwarmDecisionEngine` | 五视角 → 可审计决策备忘录 |
| 6 | 向上汇总 | `generate_weekly_summary()` | 周报摘要 / SLA 异常 → ΠPaw Task |

### 3.2 L2 ΠPaw 职能数字人（对内跨部门）

| Agent | 职责 | 核心 cs.* 调用 |
|-------|------|----------------|
| `HRAgent` | 招聘 · 入职 · 绩效 | cs.bpm.start, cs.approval.create |
| `FinanceAgent` | 开票 · 回款 · KPI 归因 | cs.invoice.*, cs.finance.* |
| `ComplianceAgent` | 红线拦截 · 合规审查 · 风险评估 | 本地规则引擎 |

### 3.3 L3 ΠPaw 经营数字人（对外）

| Agent | 方向 | 类人能力 |
|-------|------|---------|
| `SalesAgent` | 对外（获 + 转） | 顾问式销售 · BANT 资格判断 · 报价 |
| `CustomerServiceAgent` | 对外/内（服 + 续） | 共情 · SLA 分级 · 流失预警 |
| `BiddingAgent` | 对外/内 | 专业写作 · 红线拦截 · 投标管理 |

---

## 四、端到端 B2B 示例流程

```
官网留资（STEP 1）
  └─ SalesAgent.handle_inbound()
     └─ cs.customer.qualify_lead（BANT + ICP）

需求诊断（STEP 3）
  └─ SalesAgent.diagnose_needs()

报价 + G6 合规（STEP 4）
  └─ SalesAgent.create_quote()
     ├─ ComplianceEngine.check()（红线拦截）
     ├─ cs.finance.create_quote
     └─ cs.approval.create（路由到审批人）

SelfPaw 五视角决策（STEP 4b）
  └─ SelfPawEnterprise.make_decision()
     └─ SwarmDecisionEngine（五智能体辩证）

L3 审批（STEP 5）
  └─ cs.approval.approve

赢单 + 履约（STEP 6）
  └─ SalesAgent.close_won()
     └─ cs.bpm.start（onboarding）

开票（STEP 7）
  └─ FinanceAgent → cs.invoice.create + submit

回款 + KPI 归因（STEP 8）
  └─ FinanceAgent → cs.invoice.record_payment + cs.finance.kpi_attribution

ChangeSet 演化（STEP 11）
  └─ 业务经验 → 规则热更新 → 演化提议
```

---

## 五、产品化封装

### 5.1 行业 Domain 包

```
enterprise/domain_packages/b2b_saas/domain_config.json
  ├── ontology（实体 + 关系 + 漏斗阶段）
  ├── compliance_rules（热更新）
  ├── sales_playbook（话术 + 异议处理）
  ├── approval_matrix（报价/折扣多级）
  └── kpi_definitions（销售/CS/财务）
```

**切换行业** = 切换 `enabled_domain_packages`，无需代码变更。

### 5.2 流程模板包

| 模板 | 文件 | 适用 |
|------|------|------|
| 线索→签单 | `workflow_templates/lead_to_order.json` | B2B 销售 |
| 签单→回款 | `workflow_templates/order_to_revenue.json` | 财务运营 |

参数化 BPM + Agent 绑定 + SLA，**不改代码，改配置即生效**。

---

## 六、快速开始

```bash
# 方式1：CLI 脚手架
asui init my-enterprise-app -t enterprise
cd my-enterprise-app
python3 scripts/run_enterprise_platform.py

# 方式2：直接运行端到端演示
python3 enterprise/examples/b2b_lead_to_payment/scripts/b2b_pipeline.py

# 运行测试
cd asui-cli && python3 -m pytest tests/ -v
```

---

## 七、演化路线图

| 阶段 | 内容 |
|------|------|
| **现阶段（L1-L3 基础）** | cs.* 语义层 · 三层数字人 · 端到端 B2B 示例 |
| **下阶段（协议化）** | cs.* OpenAPI 规范 · 多租户 SaaS 化 · Webhook 事件推送 |
| **未来（智能化）** | 基于 LLM 的意图理解 · 自适应审批矩阵 · 实时 ChangeSet 演化 |
