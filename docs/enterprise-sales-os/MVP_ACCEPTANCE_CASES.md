# Enterprise Sales OS MVP 验收用例

> 本文定义 v0.2 配置原型必须跑通的端到端用例。每个用例都应能通过 JSON 输入触发 runtime 或脚本，输出 report、audit、state 和必要的 ChangeSet 草案。

---

## 1. 统一验收输出

每条用例必须产生：

| 输出 | 要求 |
|------|------|
| `intent` | 有 `intent_id`、`actor`、`business_object`、`risk_level` |
| `audit` | 至少记录 intent、policy、capability、result |
| `report` | 有结论、证据、风险、下一步 |
| `world_model_view` | 有 subjects、objects、drive、blockers、connectors |
| `state` | 最终状态符合用例期望 |
| `errors` | 失败用例必须有错误码和下一步建议 |

---

## 2. CASE-001：标准线索自动生成报价草案

### 输入

```yaml
case_id: CASE-001
actor_role: sales_rep
lead:
  pain_points: ["审批流程慢", "客户跟进不可追溯"]
  budget_range: medium
  timeline: this_quarter
  contact_role: "VP Sales"
quote:
  net_amount: 80000
  discount_rate: 0.08
account:
  tier: mid_market
  credit_level: A
evidence:
  - customer_need
  - product_items
```

### 期望

| 项 | 结果 |
|----|------|
| 资格判断 | `qualified` |
| 风险 | G2 |
| 审批 | `not_required` |
| 最终状态 | `report_rendered` 或 `closed` |
| 禁止 | 不得对外发送报价 |

---

## 3. CASE-002：折扣超阈值进入销售经理审批

### 输入

```yaml
case_id: CASE-002
actor_role: sales_rep
lead:
  pain_points: ["销售流程不可追溯"]
  budget_range: high
  timeline: this_month
  contact_role: "CRO"
quote:
  net_amount: 80000
  discount_rate: 0.18
account:
  tier: enterprise
  credit_level: A
evidence:
  - customer_need
  - product_items
  - discount_reason
```

### 期望

| 项 | 结果 |
|----|------|
| 资格判断 | `qualified` |
| 风险 | G3 |
| 审批 | `pending` |
| required_roles | `sales_manager` |
| 最终状态 | `approval_pending` |

---

## 4. CASE-003：大金额报价进入财务审批

### 输入

```yaml
case_id: CASE-003
actor_role: sales_rep
lead:
  pain_points: ["跨部门销售运营效率低"]
  budget_range: high
  timeline: this_quarter
  contact_role: "COO"
quote:
  net_amount: 600000
  discount_rate: 0.12
account:
  tier: strategic
  credit_level: B
evidence:
  - customer_need
  - product_items
  - discount_reason
  - payment_terms
```

### 期望

| 项 | 结果 |
|----|------|
| 风险 | G4 |
| 审批 | `pending` |
| required_roles | `sales_manager`、`finance_reviewer` |
| 审计 | 记录 G4 原因 |
| 最终状态 | `approval_pending` |

---

## 5. CASE-004：证据不足进入补证据

### 输入

```yaml
case_id: CASE-004
actor_role: sales_rep
lead:
  pain_points: []
  budget_range: unknown
  timeline: unknown
  contact_role: "Unknown"
quote:
  net_amount: 50000
  discount_rate: 0.05
account:
  tier: smb
  credit_level: A
evidence: []
```

### 期望

| 项 | 结果 |
|----|------|
| 错误码 | `EVIDENCE_REQUIRED` |
| 任务 | 创建 `collect_evidence` |
| 最终状态 | `evidence_required` 或 `blocked` |
| 禁止 | 不得生成报价草案 |

---

## 6. CASE-005：信用 blocked 拦截

### 输入

```yaml
case_id: CASE-005
actor_role: sales_rep
lead:
  pain_points: ["需要报价"]
  budget_range: medium
  timeline: this_month
  contact_role: "Procurement"
quote:
  net_amount: 70000
  discount_rate: 0.05
account:
  tier: mid_market
  credit_level: blocked
evidence:
  - customer_need
  - product_items
```

### 期望

| 项 | 结果 |
|----|------|
| 错误码 | `BUSINESS_RULE_BLOCKED` |
| 最终状态 | `business_blocked` 或 `failed_final` |
| 审计 | 记录信用 blocked |
| 禁止 | 不得生成可审批报价 |

---

## 7. CASE-006：connector 可重试失败

### 输入

```yaml
case_id: CASE-006
actor_role: sales_rep
mock_failure:
  capability: cs.quote.draft
  error: CONNECTOR_UNAVAILABLE
lead:
  pain_points: ["报价流程慢"]
  budget_range: medium
  timeline: this_quarter
  contact_role: "VP Sales"
quote:
  net_amount: 80000
  discount_rate: 0.08
account:
  tier: mid_market
  credit_level: A
evidence:
  - customer_need
  - product_items
```

### 期望

| 项 | 结果 |
|----|------|
| 错误码 | `CONNECTOR_UNAVAILABLE` |
| 重试 | 最多 3 次 |
| 最终状态 | 重试成功则继续；失败则 `needs_human` |
| 审计 | 记录每次失败和最终处理 |

---

## 8. CASE-007：审批拒绝后生成降折扣建议

### 输入

```yaml
case_id: CASE-007
actor_role: sales_rep
quote:
  net_amount: 90000
  discount_rate: 0.22
approval_decision:
  status: rejected
  reason: "折扣理由不足"
evidence:
  - customer_need
  - product_items
```

### 期望

| 项 | 结果 |
|----|------|
| 审批 | `rejected` |
| 下一步 | 回到 `quote_drafting` 或输出较低折扣建议 |
| ChangeSet | 草案建议 G3 审批必须要求 `discount_reason` |
| 审计 | 记录拒绝原因 |

---

## 9. CASE-008：人工反馈生成 ChangeSet 草案

### 输入

```yaml
case_id: CASE-008
feedback:
  feedback_type: run_review
  target_ref: quote_001
  rating: 2
  comment: "Sales Advisor 线索评分过高，预算未知时不应 qualified"
  suggested_change:
    target_pack: agent
    summary: "预算未知且时间未知时必须 needs_evidence"
```

### 期望

| 项 | 结果 |
|----|------|
| ChangeSet | 创建草案 |
| target_pack | `agent` 或 `law` |
| 自动回写 | 不允许 |
| 审计 | 记录反馈和 ChangeSet |

---

## 10. 通过标准

| 标准 | 要求 |
|------|------|
| 通过率 | CASE-001 到 CASE-008 均有确定输出 |
| 审计完整性 | 每个 case 都有 audit trace |
| 治理正确性 | CASE-002、003、005 必须命中治理 |
| 异常闭环 | CASE-004、006、007 必须有下一步 |
| 演化闭环 | CASE-007、008 必须生成 ChangeSet 草案 |
| 禁止越权 | 任意 case 都不得自动对外发送报价 |
