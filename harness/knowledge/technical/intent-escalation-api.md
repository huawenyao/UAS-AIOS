# Intent Hub 与升级 ΠPaw API 草案（Phase-0）

> Schema：`schemas/intent_object.schema.json` · `schemas/working_task.schema.json`  
> 策略：`configs/intent_escalation_policy.sample.json`  
> 实现：`asui-cli/src/asui/intent_hub.py` · `scripts/escalate_intent.py`

## 核心规则（ADR-EDH-001）

1. **SelfPaw** 会话 `product_track=selfpaw` 方可发起升级。  
2. **business_outward** 必须携带 `evidence_refs[]`（≥1）与 `escalation_target`（`pipaw`）。  
3. 升级创建 **ΠPaw Working Task**，禁止静默越权直连对外通道。  
4. 审计：`audit_id` 写入 Working Task，与 PL-006 审计链对齐（Phase-1 落库）。

## 意图分类

| intent_class | 说明 | 默认升级 |
|--------------|------|----------|
| `personal` | 个人效率 | 不允许 |
| `collaboration` | 部门协同 | 可选 → cs_lead |
| `business_outward` | 经营/客诉/对外 | 必须 Evidence → cs_agent |

## POST /api/v1/intent/escalate

将 SelfPaw `IntentObject` 升级为 ΠPaw `WorkingTask`。

**Headers**

- `X-Tenant-Id`: 租户（须与 body 一致）
- `Authorization`: SSO（Phase-0 mock）

**Request**

```json
{
  "intent": {
    "intent_id": "int-complaint-demo-001",
    "tenant_id": "t-acme-demo",
    "source": "selfpaw_intent_hub",
    "intent_class": "business_outward",
    "goal": "处理 VIP 客户交付延期投诉",
    "actor": {
      "user_id": "u-employee-1001",
      "product_track": "selfpaw",
      "position_id": "pos-sales-rep"
    },
    "escalation_target": {
      "product_track": "pipaw",
      "position_id": "pos-cs-agent",
      "domain_id": "domain.customer_service",
      "role_id": "role.cs_agent"
    },
    "evidence_refs": [
      {
        "evidence_id": "ev-chat-001",
        "type": "chat_transcript",
        "summary": "客户 IM 投诉摘要"
      }
    ],
    "status": "active"
  }
}
```

**Response 200**

```json
{
  "status": "ok",
  "audit_id": "aud-abc123",
  "intent": { "status": "escalated" },
  "working_task": {
    "task_id": "wt-...",
    "source": "selfpaw_escalation",
    "product_track": "pipaw",
    "position_id": "pos-cs-agent",
    "assignee_role_id": "role.cs_agent",
    "status": "open"
  }
}
```

**Response 403**

| deny_reason | 说明 |
|-------------|------|
| `TENANT_ISOLATION_VIOLATION` | 租户不匹配 |
| `ESCALATION_REQUIRES_SELFPaw_SESSION` | 非 SelfPaw 会话发起 |
| `EVIDENCE_REQUIRED` | 经营类缺 Evidence |
| `ESCALATION_NOT_ALLOWED_FOR_CLASS` | personal 类不可升级 |

## GET /api/v1/pipaw/working-tasks

ΠPaw Task Board 查询（按岗位/角色过滤）。

**Query**

- `tenant_id`（必填）
- `position_id`（可选，如 `pos-cs-agent`）
- `assignee_role_id`（可选，如 `role.cs_agent`）
- `status`（可选，`open`）

## E2E 验收用例

**员工提交客诉 → ΠPaw 客服 Task 可见**

1. 加载 `configs/intent_samples/complaint_escalation.sample.json`  
2. `POST /intent/escalate`（或 `python scripts/escalate_intent.py escalate`）  
3. `GET working-tasks?position_id=pos-cs-agent` 含新 `task_id`  
4. 运行：`python scripts/validate_intent_escalation.py validate`

## 与实体图谱

`entity-map.json` → `SelfPawEnterprise_to_PiPaw` via `IntentHub`, contract `intent_escalation_with_evidence`.
