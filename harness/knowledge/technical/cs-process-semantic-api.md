# cs.process 流程语义 API（REQ-EDH-PL-004）

> **status**: frozen-draft · Phase-0

## 操作契约

| 操作 | 用途 | 必填字段 |
|------|------|----------|
| `cs.process.start` | 启动流程实例 | `tenant_id`, `process_id`, `template_id`, `actor_id`, `payload` |
| `cs.process.advance` | 状态迁移 | `tenant_id`, `process_id`, `current_state`, `target_state`, `actor_id` |
| `cs.process.escalate` | 升级至 Human-in-the-loop | `tenant_id`, `process_id`, `escalation_reason`, `actor_id` |

Schema：`schemas/cs_process_operation.schema.json`

## BPM 适配器接口（草案）

```text
BpmAdapter.advance(process_id, from_state, to_state, context) -> AdvanceResult
BpmAdapter.escalate(process_id, reason, assignee_roles[]) -> EscalationTicket
```

Mock 实现：`asui-cli/src/asui/connectors/mock_bpm.py`

## Human-in-the-loop 事件

| 事件 | 触发 |
|------|------|
| `process.escalated` | `cs.process.escalate` 成功 |
| `process.awaiting_human` | G3/G4 审批 pending |
| `process.evidence_required` | `EVIDENCE_REQUIRED` |

## 流程模板（文档级）

| 模板 ID | 场景 | 路径 |
|---------|------|------|
| `sales_quote_approval` | B2B 线索→报价→审批 | `configs/process_templates/sales_quote_approval.json` |
| `cs_customer_service` | 客服工单→升级 | `configs/process_templates/cs_customer_service.json` |

验证：`python scripts/validate_cs_process.py validate`
