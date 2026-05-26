# Enterprise Sales OS 领域模型

> 本文定义 B2B 线索到报价审批 MVP 的最小业务对象、字段、生命周期和事件。开发时应先按本文建立 JSON Schema 或等价数据结构，再映射到当前 UAS subapp 的 `database/` 与 `configs/`。

---

## 1. 对象关系

```text
Tenant
  └─ Actor
      └─ Intent
          ├─ Evidence[]
          ├─ BusinessObject: Lead / Account / Quote / Approval
          ├─ Task[]
          ├─ CapabilityCall[]
          ├─ AuditEvent[]
          ├─ KPIEvent[]
          └─ ChangeSet?
```

---

## 2. 核心实体

### 2.1 Tenant

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tenant_id` | string | 是 | 租户唯一标识 |
| `name` | string | 是 | 企业名称 |
| `deployment_mode` | enum | 是 | `local_mock`、`private`、`hybrid`、`saas` |
| `data_region` | string | 是 | 数据域 |
| `enabled_capabilities` | string[] | 是 | 可用 `cs.*` 能力 |

### 2.2 Actor

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `actor_id` | string | 是 | 用户、Agent 或系统 ID |
| `actor_type` | enum | 是 | `human`、`agent`、`system` |
| `roles` | string[] | 是 | 如 `sales_rep`、`sales_manager`、`finance_reviewer` |
| `department` | string | 否 | 部门 |
| `delegations` | object[] | 否 | 委托授权 |
| `data_scope` | string[] | 是 | 可读数据范围 |
| `action_scope` | string[] | 是 | 可执行动作范围 |

### 2.3 Intent

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `intent_id` | string | 是 | 意图单 ID |
| `tenant_id` | string | 是 | 租户 |
| `source` | enum | 是 | `outward_gateway`、`selfpaw_escalation`、`sales_manual_input`、`system_event` |
| `intent_type` | enum | 是 | `lead_qualification`、`quote_request`、`approval_request`、`evidence_request` |
| `goal` | string | 是 | 业务目标 |
| `success_criteria` | string[] | 是 | 成功标准 |
| `actor_ref` | string | 是 | 发起主体 |
| `business_object_ref` | string | 是 | 关联业务对象 |
| `risk_level` | enum | 是 | `G0`、`G1`、`G2`、`G3`、`G4` |
| `status` | enum | 是 | 见状态机 |

### 2.4 Lead

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `lead_id` | string | 是 | 线索 ID |
| `account_name` | string | 是 | 公司名 |
| `contact_name` | string | 是 | 联系人 |
| `contact_channel` | enum | 是 | `web_form`、`email`、`im`、`phone`、`manual` |
| `industry` | string | 否 | 行业 |
| `company_size` | enum | 否 | `smb`、`mid_market`、`enterprise` |
| `pain_points` | string[] | 是 | 需求/痛点 |
| `budget_range` | enum | 否 | `unknown`、`low`、`medium`、`high` |
| `timeline` | enum | 否 | `unknown`、`this_month`、`this_quarter`、`later` |
| `owner_actor_id` | string | 是 | 负责人 |
| `qualification_score` | number | 否 | 0-100 |
| `qualification_status` | enum | 是 | `new`、`qualified`、`disqualified`、`needs_evidence`、`needs_human_review` |

### 2.5 Account

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `account_id` | string | 是 | 客户 ID |
| `name` | string | 是 | 客户名称 |
| `tier` | enum | 是 | `smb`、`mid_market`、`enterprise`、`strategic` |
| `credit_level` | enum | 是 | `A`、`B`、`C`、`blocked` |
| `existing_customer` | boolean | 是 | 是否存量客户 |
| `risk_flags` | string[] | 否 | 黑名单、逾期、合规风险等 |

### 2.6 Quote

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `quote_id` | string | 是 | 报价 ID |
| `lead_id` | string | 是 | 来源线索 |
| `account_id` | string | 否 | 客户 |
| `items` | object[] | 是 | 报价明细 |
| `list_amount` | number | 是 | 标准价格 |
| `discount_rate` | number | 是 | 折扣率，0-1 |
| `net_amount` | number | 是 | 折后价 |
| `currency` | string | 是 | 币种 |
| `payment_terms` | string | 是 | 账期 |
| `valid_until` | string | 是 | 有效期 |
| `quote_status` | enum | 是 | `draft`、`pending_approval`、`approved`、`rejected`、`cancelled` |
| `approval_ref` | string | 否 | 审批单 |

### 2.7 Approval

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `approval_id` | string | 是 | 审批 ID |
| `approval_type` | enum | 是 | `quote_discount`、`quote_amount`、`credit_exception`、`legal_review` |
| `risk_level` | enum | 是 | `G2`、`G3`、`G4` |
| `required_roles` | string[] | 是 | 审批角色 |
| `status` | enum | 是 | `not_required`、`pending`、`approved`、`rejected`、`needs_evidence`、`cancelled` |
| `decision_reason` | string | 否 | 审批理由 |
| `approved_by` | string[] | 否 | 审批人 |

### 2.8 Evidence

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `evidence_id` | string | 是 | 证据 ID |
| `source_type` | enum | 是 | `form`、`email`、`call_note`、`crm_record`、`document`、`manual_note` |
| `source_ref` | string | 是 | 来源引用 |
| `summary` | string | 是 | 证据摘要 |
| `hash` | string | 否 | 文件或内容 hash |
| `confidence` | number | 是 | 0-1 |
| `created_by` | string | 是 | 创建主体 |
| `linked_object_refs` | string[] | 是 | 关联对象 |

### 2.9 Task

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | string | 是 | 任务 ID |
| `task_type` | enum | 是 | `qualify_lead`、`draft_quote`、`review_compliance`、`review_finance`、`collect_evidence` |
| `owner_agent` | string | 是 | 负责 Agent |
| `human_owner` | string | 否 | 人类负责人 |
| `status` | enum | 是 | 见状态机 |
| `sla_due_at` | string | 否 | SLA 截止 |
| `blocking_reason` | string | 否 | 阻塞原因 |

### 2.10 AuditEvent

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `audit_id` | string | 是 | 审计事件 ID |
| `event_type` | enum | 是 | `intent_created`、`policy_checked`、`capability_called`、`approval_decided`、`report_rendered`、`rollback_requested` |
| `actor_ref` | string | 是 | 操作主体 |
| `target_ref` | string | 是 | 作用对象 |
| `input_hash` | string | 否 | 输入摘要 |
| `output_hash` | string | 否 | 输出摘要 |
| `timestamp` | string | 是 | 时间戳 |
| `trace_id` | string | 是 | 一次运行的 trace |

### 2.11 KPIEvent

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `kpi_id` | string | 是 | 指标事件 ID |
| `metric` | enum | 是 | `lead_qualified`、`quote_drafted`、`approval_cycle_minutes`、`policy_blocked`、`manual_takeover` |
| `value` | number | 是 | 指标值 |
| `attribution_ref` | string | 是 | 归因对象 |
| `created_at` | string | 是 | 记录时间 |

### 2.12 ChangeSet

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `changeset_id` | string | 是 | 变更建议 ID |
| `source` | enum | 是 | `feedback`、`kpi_drift`、`failed_case`、`policy_block` |
| `target_pack` | enum | 是 | `domain`、`workflow`、`law`、`agent`、`connector`、`evaluation` |
| `proposal` | string | 是 | 建议内容 |
| `diff_preview` | object | 否 | 配置差异预览 |
| `approval_status` | enum | 是 | `draft`、`pending_review`、`approved`、`rejected`、`applied` |

---

## 3. 关键生命周期

### 3.1 Lead

```text
new
  → needs_evidence
  → qualified
  → quote_requested
  → closed_won / closed_lost

new
  → disqualified
```

### 3.2 Quote

```text
draft
  → pending_approval
  → approved
  → sent_manually

pending_approval
  → rejected
  → draft

draft
  → cancelled
```

### 3.3 ChangeSet

```text
draft
  → pending_review
  → approved
  → applied

pending_review
  → rejected
```

---

## 4. 最小事件

| 事件 | 触发 | 后续动作 |
|------|------|----------|
| `lead_created` | 官网表单或人工录入 | 创建 Intent + Task |
| `evidence_missing` | 资格判断证据不足 | 创建 `collect_evidence` 任务 |
| `lead_qualified` | `cs.lead.qualify` 成功 | 进入报价草案 |
| `quote_drafted` | `cs.quote.draft` 成功 | 进入 Policy Engine |
| `approval_required` | G3/G4 命中 | 创建审批任务 |
| `approval_rejected` | 审批拒绝 | 回到草稿或关闭 |
| `capability_failed` | `cs.*` 失败 | 记录错误并进入人工接管或重试 |
| `feedback_submitted` | 人工反馈 | 生成 ChangeSet 草案 |
