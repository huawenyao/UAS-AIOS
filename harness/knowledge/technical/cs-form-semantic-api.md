# cs.form 动态表单语义 API（REQ-EDH-PL-005）

> **status**: frozen-draft · Phase-0

## 操作契约

| 操作 | 用途 | 必填 |
|------|------|------|
| `cs.form.render` | 按模板渲染字段 | `tenant_id`, `template_id`, `actor_id` |
| `cs.form.submit` | 提交并触发流程 | `tenant_id`, `form_id`, `fields` |
| `cs.form.validate` | 校验字段与策略 | `tenant_id`, `template_id`, `fields` |

Schema：`schemas/cs_form_operation.schema.json`

## 报销/审批场景样例

模板：`configs/form_templates/expense_reimbursement.sample.json`

| 字段 | 类型 | 审批关联 |
|------|------|----------|
| `amount` | number | >5000 → G3 财务 |
| `category` | enum | 差旅/招待/采购 |
| `receipt_ids` | array | 必填证据 |

## SelfPaw 填单代理验收（CASE-FORM-001）

```yaml
case_id: CASE-FORM-001
actor: selfpaw_fill_agent
template_id: expense_reimbursement
fields:
  amount: 3200
  category: travel
  receipt_ids: ["r1"]
expect:
  validate: pass
  process_template: cs_customer_service
```

验证：`python scripts/validate_cs_form.py validate`
