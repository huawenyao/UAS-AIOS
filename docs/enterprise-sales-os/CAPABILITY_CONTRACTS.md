# Enterprise Sales OS 能力服务合约

> Agent 不直连 CRM/BPM/财务系统，只调用 `cs.*` 语义能力服务。本文定义 P0 能力的输入、输出、错误、权限、幂等与回滚要求。

---

## 1. 通用调用信封

所有 `cs.*` 能力必须使用同一调用信封：

```yaml
capability: cs.lead.qualify
version: v1
tenant_id: tenant_acme
trace_id: trace_001
intent_ref: int_001
actor:
  type: agent
  id: ppaw_sales_advisor
on_behalf_of: user_123
idempotency_key: int_001:lead_456:qualify
inputs: {}
policy:
  required_scope: []
  max_risk_level: G2
audit:
  audit_ref: audit_001
```

### 1.1 通用响应

```yaml
status: success | failed | needs_human_review
result: {}
error:
  code: null
  message: null
  retryable: false
rollback:
  rollback_supported: false
  rollback_ref: null
audit:
  audit_ref: audit_001
  output_hash: sha256:...
```

### 1.2 通用错误码

| 错误码 | 含义 | 可重试 | 下一步 |
|--------|------|--------|--------|
| `POLICY_DENIED` | 权限或风险策略拒绝 | 否 | 人工审批或修改 scope |
| `EVIDENCE_REQUIRED` | 证据不足 | 否 | 创建补证据任务 |
| `VALIDATION_ERROR` | 输入 schema 不合法 | 否 | 修正输入 |
| `CONNECTOR_UNAVAILABLE` | mock/connector 不可用 | 是 | 重试或人工接管 |
| `IDEMPOTENCY_CONFLICT` | 幂等键冲突且输入不一致 | 否 | 人工审计 |
| `BUSINESS_RULE_BLOCKED` | 业务规则拦截 | 否 | 查看规则原因 |
| `HUMAN_REVIEW_REQUIRED` | 必须人工确认 | 否 | 创建审批或接管任务 |

---

## 2. `cs.lead.qualify`

### 2.1 目的

对线索做资格判断，输出资格状态、评分、原因和下一步建议。

### 2.2 权限

| 项 | 要求 |
|----|------|
| 数据 scope | `crm.leads.assigned` 或 `crm.leads.team` |
| 动作 scope | `cs.lead.qualify` |
| 最大风险 | G2 |
| 审批 | 不需要 |

### 2.3 输入

```yaml
inputs:
  lead_id: lead_456
  account_snapshot:
    account_name: "Acme Ltd"
    industry: "manufacturing"
    company_size: mid_market
  lead_signals:
    pain_points: ["审批慢", "销售流程不可追溯"]
    budget_range: medium
    timeline: this_quarter
    contact_role: "VP Sales"
  evidence_refs:
    - ev_form_001
    - ev_call_note_001
```

### 2.4 输出

```yaml
result:
  qualification_status: qualified | disqualified | needs_evidence | needs_human_review
  score: 0-100
  reasons:
    - "预算和时间窗口明确"
  missing_evidence:
    - "缺少决策人确认"
  next_capabilities:
    - cs.quote.draft
```

### 2.5 规则

| 条件 | 结果 |
|------|------|
| `pain_points` 为空 | `needs_evidence` |
| `budget_range=unknown` 且 `timeline=unknown` | `needs_evidence` |
| `contact_role` 非决策/影响角色且无补充证据 | `needs_human_review` |
| `score >= 70` | `qualified` |
| `score < 40` | `disqualified` |

---

## 3. `cs.quote.draft`

### 3.1 目的

生成报价草案，不对外发送，不构成客户承诺。

### 3.2 权限

| 项 | 要求 |
|----|------|
| 数据 scope | `crm.leads.assigned`、`product.catalog.read` |
| 动作 scope | `cs.quote.draft` |
| 最大风险 | G2；若折扣或金额超阈值，升级为 G3/G4 |
| 审批 | 草案不需要；超阈值报价进入审批 |

### 3.3 输入

```yaml
inputs:
  lead_id: lead_456
  account_id: account_789
  products:
    - sku: uas_enterprise_base
      quantity: 100
  requested_discount_rate: 0.18
  payment_terms: net_30
  evidence_refs:
    - ev_requirements_001
```

### 3.4 输出

```yaml
result:
  quote_id: quote_001
  quote_status: draft
  list_amount: 120000
  discount_rate: 0.18
  net_amount: 98400
  currency: CNY
  approval_required: true
  approval_reasons:
    - "折扣超过销售自助阈值 15%"
  next_capabilities:
    - cs.approval.start
```

### 3.5 规则

| 条件 | 结果 |
|------|------|
| 产品不存在 | `VALIDATION_ERROR` |
| 客户信用为 `blocked` | `BUSINESS_RULE_BLOCKED` |
| 折扣 `<= 0.10` 且金额 `< 100000` | G2，可保留草案 |
| 折扣 `> 0.10` 或金额 `>= 100000` | G3，销售经理审批 |
| 折扣 `> 0.25` 或金额 `>= 500000` | G4，财务 + 合规审批 |

### 3.6 回滚

报价草案可取消，返回：

```yaml
rollback:
  rollback_supported: true
  rollback_ref: quote_001:cancel
```

---

## 4. `cs.approval.start`

### 4.1 目的

为报价、折扣、信用例外或合规事项创建审批任务。

### 4.2 权限

| 项 | 要求 |
|----|------|
| 数据 scope | 关联对象可读 |
| 动作 scope | `cs.approval.start` |
| 最大风险 | G4 |
| 审批 | 创建审批本身不需要；审批结果必须由人类角色确认 |

### 4.3 输入

```yaml
inputs:
  approval_type: quote_discount
  target_ref: quote_001
  risk_level: G3
  requested_decision: approve_quote
  reasons:
    - "折扣 18% 超过销售自助阈值"
  evidence_refs:
    - ev_requirements_001
    - ev_quote_001
```

### 4.4 输出

```yaml
result:
  approval_id: appr_001
  status: pending
  required_roles:
    - sales_manager
  sla_due_at: "2026-05-25T10:00:00Z"
  next_actions:
    - "wait_for_approval"
```

### 4.5 审批角色规则

| 风险 | 需要角色 |
|------|----------|
| G2 | 无或 owner 确认 |
| G3 | `sales_manager` |
| G4 金额/折扣 | `sales_manager` + `finance_reviewer` |
| G4 合同/红线 | `sales_manager` + `compliance_reviewer` |

---

## 5. `cs.audit.append`

### 5.1 目的

追加不可变审计事件，形成 intent、evidence、decision、capability、approval、result 的解释链。

### 5.2 权限

| 项 | 要求 |
|----|------|
| 数据 scope | 当前 trace |
| 动作 scope | `cs.audit.append` |
| 最大风险 | G0 |
| 审批 | 不需要 |

### 5.3 输入

```yaml
inputs:
  event_type: capability_called
  target_ref: quote_001
  actor_ref: ppaw_sales_advisor
  intent_ref: int_001
  payload_hash: sha256:...
  summary: "生成报价草案"
```

### 5.4 输出

```yaml
result:
  audit_id: audit_001
  trace_id: trace_001
  appended: true
```

### 5.5 规则

- 审计事件只能追加，不能修改。
- 任何 `cs.*` 成功或失败都必须调用或等价记录 `cs.audit.append`。
- 审计失败时，业务动作不得标记为成功。

---

## 6. 幂等策略

| 能力 | 幂等键 |
|------|--------|
| `cs.lead.qualify` | `{intent_id}:{lead_id}:qualify` |
| `cs.quote.draft` | `{intent_id}:{lead_id}:{product_hash}:quote_draft` |
| `cs.approval.start` | `{intent_id}:{target_ref}:{approval_type}` |
| `cs.audit.append` | `{trace_id}:{event_type}:{target_ref}:{payload_hash}` |

---

## 7. P0 mock 实现要求

开发 v0.2 时，每个能力先以 `scripts/cs_*.py` 实现：

| 脚本 | 输入 | 输出 |
|------|------|------|
| `cs_lead_qualify.py` | stdin JSON | 通用响应 JSON |
| `cs_quote_draft.py` | stdin JSON | 通用响应 JSON |
| `cs_approval_start.py` | stdin JSON | 通用响应 JSON |
| `cs_audit_append.py` | stdin JSON | 写入 `database/audit/execution_log.jsonl` 并输出 JSON |

所有脚本必须支持：

1. schema 校验失败返回 `VALIDATION_ERROR`。
2. 权限不足返回 `POLICY_DENIED`。
3. 业务拦截返回 `BUSINESS_RULE_BLOCKED`。
4. 成功和失败都输出 `audit_ref` 或明确说明审计失败。
