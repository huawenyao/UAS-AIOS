# Enterprise Sales OS 世界模型配置

> 本文为 v0.2 原型提供最小 `configs/world_model.json` 设计，解决世界模型未工程化的问题。它不是完整世界模型引擎，而是让主客体、反馈通道、约束和推动/阻碍/连接先进入配置与报告。

---

## 1. 世界模型目标

MVP 世界模型必须回答：

1. 当前业务闭环有哪些主体？
2. 被操作的业务客体是什么？
3. 哪些反馈能证明动作有效或失败？
4. 哪些约束会影响 Agent 决策？
5. 对每个任务，推动、阻碍、连接分别是什么？

---

## 2. 五维映射

| 维度 | MVP 表达 |
|------|----------|
| 空间 | 租户、部门、渠道、系统边界、数据 scope |
| 时间 | SLA、报价有效期、审批时限、销售周期 |
| 主体 | 员工、销售经理、财务、合规、客户联系人、Agent |
| 客体 | Lead、Account、Quote、Approval、Evidence、Task |
| 感知-行动-反馈 | 线索创建、能力调用、审批结果、KPI、人工反馈 |

---

## 3. 配置草案

```json
{
  "world_model_id": "enterprise_sales_os_mvp",
  "scope": {
    "tenant_id": "tenant_acme",
    "business_loop": "lead_to_quote_approval",
    "systems": ["mock_crm", "mock_approval", "local_audit"]
  },
  "subjects": [
    {
      "id": "sales_rep",
      "type": "human_role",
      "intent": "推进合格线索进入报价",
      "permissions": ["cs.lead.qualify", "cs.quote.draft"],
      "success_metrics": ["lead_qualified", "quote_drafted"]
    },
    {
      "id": "sales_manager",
      "type": "human_role",
      "intent": "控制折扣与销售承诺质量",
      "permissions": ["cs.approval.decide.sales"],
      "success_metrics": ["approval_cycle_minutes", "policy_blocked"]
    },
    {
      "id": "finance_reviewer",
      "type": "human_role",
      "intent": "控制金额、信用和账期风险",
      "permissions": ["cs.approval.decide.finance"],
      "success_metrics": ["finance_risk_blocked"]
    },
    {
      "id": "ppaw_sales_advisor",
      "type": "agent",
      "intent": "基于证据完成线索判断和报价草案",
      "permissions": ["cs.lead.qualify", "cs.quote.draft", "cs.audit.append"],
      "success_metrics": ["lead_qualified", "quote_drafted"]
    }
  ],
  "objects": [
    {
      "id": "lead",
      "lifecycle": ["new", "needs_evidence", "qualified", "disqualified", "quote_requested"],
      "required_evidence": ["customer_need"]
    },
    {
      "id": "quote",
      "lifecycle": ["draft", "pending_approval", "approved", "rejected", "cancelled"],
      "required_evidence": ["customer_need", "product_items", "discount_reason"]
    },
    {
      "id": "approval",
      "lifecycle": ["not_required", "pending", "approved", "rejected", "needs_evidence", "cancelled"]
    }
  ],
  "feedback_sources": [
    {
      "id": "approval_result",
      "type": "human_decision",
      "latency": "minutes_to_hours",
      "used_by": ["policy", "changeset"]
    },
    {
      "id": "capability_result",
      "type": "system_event",
      "latency": "seconds",
      "used_by": ["audit", "retry", "kpi"]
    },
    {
      "id": "manual_feedback",
      "type": "human_feedback",
      "latency": "after_run",
      "used_by": ["changeset"]
    }
  ],
  "constraints": {
    "time": {
      "approval_sla_hours": 24,
      "quote_valid_days": 15
    },
    "governance": {
      "max_auto_risk_level": "G2",
      "external_commitment_requires_human": true
    },
    "data": {
      "agent_must_use_capability_service": true,
      "audit_required_for_all_capability_calls": true
    }
  }
}
```

---

## 4. 推动 / 阻碍 / 连接输出要求

每次运行报告必须包含：

```yaml
world_model_view:
  subjects:
    - ppaw_sales_advisor
    - sales_manager
  objects:
    - lead_456
    - quote_001
  drive:
    - "客户预算和时间窗口明确"
  blockers:
    - "折扣 18% 超过销售自助阈值"
  connectors:
    - "cs.approval.start 将报价草案连接到销售经理审批"
  feedback_channels:
    - approval_result
    - capability_result
```

---

## 5. 与配置文件的关系

| 文件 | 关系 |
|------|------|
| `configs/world_model.json` | 本文配置落点 |
| `configs/governance_policy.json` | 使用 constraints.governance 与主体权限 |
| `configs/workflow_config.json` | 每步输出需引用主客体和反馈 |
| `configs/evolution_policy.json` | 使用 feedback_sources 和 KPI 触发 ChangeSet |
| `reports/*.md` | 输出 world_model_view |

---

## 6. 验收规则

| 检查 | 标准 |
|------|------|
| 主体 | 至少包含发起人、执行 Agent、审批人 |
| 客体 | 至少包含 Lead、Quote、Approval |
| 反馈 | 至少包含 capability_result、approval_result |
| 约束 | 必须有 max_auto_risk_level 与 audit_required |
| 报告 | 必须输出 drive/blockers/connectors |
