# Enterprise Sales OS 反馈与 ChangeSet 闭环

> 本文定义 MVP 阶段的人机反馈、KPI 归因、ChangeSet 草案和受控回写流程。v0.2 只生成 ChangeSet 草案，不自动修改生产配置。

---

## 1. 闭环原则

1. 反馈必须结构化，不能只写在聊天记录里。
2. ChangeSet 必须指向具体 Pack 或配置文件。
3. 任何回写都必须经过人工审批。
4. MVP 只做到草案和 diff preview，不做自动 apply。

---

## 2. 反馈来源

| 来源 | 示例 | 进入路径 |
|------|------|----------|
| 人工审批意见 | “折扣理由不足” | Approval decision |
| 人工运行反馈 | “评分过高，应要求预算证据” | `database/feedback/*.json` |
| KPI 偏差 | 审批周期过长、证据不足率高 | KPIEvent |
| 能力失败 | connector 不可用、schema 错误 | CapabilityCall |
| 策略拦截 | 信用 blocked、超折扣 | Policy check |

---

## 3. 反馈 schema

```yaml
feedback_id: fb_001
trace_id: trace_001
intent_ref: int_001
submitted_by: sales_manager_001
feedback_type: approval_comment | run_review | correction | risk_note
target_ref: quote_001
rating: 1-5
comment: "折扣理由不足，缺少竞争对手证据"
suggested_change:
  target_pack: law
  summary: "G3 折扣审批必须要求 discount_reason evidence"
created_at: "2026-05-24T14:00:00Z"
```

---

## 4. KPI 归因

| 指标 | 计算 | 归因目标 |
|------|------|----------|
| `lead_qualified` | 资格判断成功次数 | Sales Advisor |
| `evidence_missing_rate` | 证据不足次数 / 总运行次数 | Domain Pack / Evidence rules |
| `quote_drafted` | 报价草案生成次数 | Quote capability |
| `approval_cycle_minutes` | 审批完成时间 - 审批创建时间 | Approval workflow |
| `policy_blocked` | 策略拦截次数 | Law Pack |
| `manual_takeover` | 人工接管次数 | Agent Pack / Connector Pack |

---

## 5. ChangeSet schema

```yaml
changeset_id: chg_001
source:
  type: feedback
  ref: fb_001
target:
  pack: law
  file: configs/governance_policy.json
proposal: "G3 折扣审批必须包含 discount_reason evidence"
reason:
  - "审批人反馈折扣理由不足"
  - "当前 evidence requirement 未显式要求 discount_reason"
diff_preview:
  add:
    quote_policy.sales_manager_approval.required_evidence:
      - discount_reason
risk_level: G2
approval:
  status: draft
  required_roles: ["sales_manager", "compliance_reviewer"]
rollback:
  previous_version: null
created_at: "2026-05-24T14:05:00Z"
```

---

## 6. ChangeSet 类型

| 类型 | 目标 | 示例 |
|------|------|------|
| Domain ChangeSet | `world_model.json` / domain pack | 新增客户等级解释 |
| Workflow ChangeSet | `workflow_config.json` | 增加补证据步骤 |
| Law ChangeSet | `governance_policy.json` | 调整折扣阈值 |
| Agent ChangeSet | `swarm_agents.json` / skills | 修改 Sales Advisor 输出要求 |
| Connector ChangeSet | `system_registry.json` / field mapping | 修正字段映射 |
| Evaluation ChangeSet | `evaluate_sales_loop.py` | 新增验收检查 |

---

## 7. 受控回写流程

```text
feedback / KPI / failed_case
  → generate_changeset_draft
  → human_review
  → approved?
      ├─ no: rejected + audit
      └─ yes: apply_to_non_prod_config
              → run acceptance cases
              → promote manually
```

v0.2 只实现到 `generate_changeset_draft`。

---

## 8. 草案生成规则

| 触发 | ChangeSet 建议 |
|------|----------------|
| `EVIDENCE_REQUIRED` 高频 | 增加 Evidence Capture 模板或必填证据说明 |
| `POLICY_DENIED` 高频 | 检查 scope 配置或角色授权 |
| 审批拒绝因为折扣理由不足 | Law Pack 增加 `discount_reason` 要求 |
| connector 重试失败 | Connector Pack 增加降级或错误提示 |
| 人工接管率高 | Agent Pack 增加输出 schema 或置信度阈值 |

---

## 9. 输出文件

| 文件 | 内容 |
|------|------|
| `database/feedback/<trace_id>.json` | 人工反馈 |
| `database/kpi/<trace_id>.json` | KPI 归因 |
| `database/changesets/<changeset_id>.json` | ChangeSet 草案 |
| `reports/<trace_id>_evolution.md` | 人类可读演化报告 |

---

## 10. 验收标准

1. 至少一条人工反馈能生成 ChangeSet 草案。
2. ChangeSet 必须指向明确 Pack 和文件。
3. ChangeSet 不得自动修改生产配置。
4. ChangeSet 必须写入 audit。
5. 被拒绝的 ChangeSet 也必须保留原因。
