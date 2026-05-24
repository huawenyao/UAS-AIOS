# Enterprise Sales OS 工作流状态机

> 本文定义 B2B 线索到报价审批 MVP 的任务、审批、补证据、能力失败、人工接管和回滚路径。开发时所有状态迁移必须写入 `AuditEvent`。

---

## 1. 总体状态机

```text
INTENT_CREATED
  → EVIDENCE_CHECKING
  → LEAD_QUALIFYING
  → QUOTE_DRAFTING
  → POLICY_CHECKING
  → APPROVAL_PENDING
  → APPROVED
  → REPORT_RENDERED
  → CHANGESET_DRAFTED

任意执行态
  → EVIDENCE_REQUIRED
  → HUMAN_TAKEOVER
  → FAILED_RETRYABLE
  → FAILED_FINAL
  → CANCELLED
```

---

## 2. Intent 状态

| 状态 | 含义 | 允许迁移 |
|------|------|----------|
| `intent_created` | 意图已生成 | `evidence_checking`、`cancelled` |
| `evidence_checking` | 校验证据是否满足动作要求 | `lead_qualifying`、`evidence_required`、`failed_final` |
| `lead_qualifying` | 执行线索资格判断 | `quote_drafting`、`evidence_required`、`human_takeover`、`failed_retryable`、`failed_final` |
| `quote_drafting` | 生成报价草案 | `policy_checking`、`business_blocked`、`failed_retryable`、`failed_final` |
| `policy_checking` | 执行治理矩阵 | `approval_pending`、`approved`、`business_blocked`、`evidence_required` |
| `approval_pending` | 等待人工审批 | `approved`、`rejected`、`evidence_required`、`cancelled` |
| `approved` | 内部审批通过 | `report_rendered` |
| `rejected` | 审批拒绝 | `report_rendered`、`quote_drafting` |
| `report_rendered` | 输出报告 | `changeset_drafted`、`closed` |
| `changeset_drafted` | 已生成演化建议 | `closed` |
| `closed` | 闭环结束 | 无 |

---

## 3. Task 状态

| 状态 | 含义 | 进入条件 | 退出条件 |
|------|------|----------|----------|
| `queued` | 已入队 | 创建任务 | 被 runtime 处理 |
| `running` | 执行中 | runtime 获取任务 | 成功、失败、阻塞 |
| `blocked` | 阻塞 | 缺证据、缺权限、等待审批 | 补齐条件 |
| `needs_human` | 需要人工 | 策略要求、低置信度、异常 | 人工提交决定 |
| `succeeded` | 成功 | 步骤输出有效 | 进入下一步 |
| `failed_retryable` | 可重试失败 | connector 不可用等 | 重试或人工接管 |
| `failed_final` | 不可重试失败 | schema、规则、权限失败 | 输出失败报告 |
| `cancelled` | 取消 | 用户或策略取消 | 结束 |

### 3.1 重试规则

| 错误 | 最大重试 | 间隔 | 失败后 |
|------|----------|------|--------|
| `CONNECTOR_UNAVAILABLE` | 3 | 指数退避 | `needs_human` |
| `VALIDATION_ERROR` | 0 | - | `failed_final` |
| `POLICY_DENIED` | 0 | - | `failed_final` |
| `EVIDENCE_REQUIRED` | 0 | - | `blocked` |
| `IDEMPOTENCY_CONFLICT` | 0 | - | `needs_human` |

---

## 4. Approval 状态

```text
not_required
  → approved

pending
  → approved
  → rejected
  → needs_evidence
  → cancelled
```

| 状态 | 含义 |
|------|------|
| `not_required` | 治理矩阵判定无需审批 |
| `pending` | 等待审批角色处理 |
| `approved` | 审批通过 |
| `rejected` | 审批拒绝 |
| `needs_evidence` | 审批人要求补证据 |
| `cancelled` | 申请取消 |

### 4.1 审批拒绝后的路径

| 拒绝原因 | 下一步 |
|----------|--------|
| 折扣过高 | 回到 `quote_drafting`，生成较低折扣草案 |
| 证据不足 | 进入 `evidence_required` |
| 信用风险 | `business_blocked` |
| 合规风险 | `failed_final` + 合规报告 |

---

## 5. Evidence 状态

| 状态 | 含义 |
|------|------|
| `missing` | 缺必需证据 |
| `submitted` | 已提交 |
| `verified` | 可用于决策 |
| `conflicted` | 证据互相冲突 |
| `rejected` | 证据无效 |

证据冲突时不得自动继续报价，必须进入 `needs_human`。

---

## 6. Rollback 状态

MVP 只支持草案级回滚，不支持真实外部系统回滚。

| 对象 | 支持回滚 | 回滚动作 |
|------|----------|----------|
| Quote draft | 是 | `quote_status=cancelled` |
| Approval task | 是 | `approval_status=cancelled` |
| Audit event | 否 | 追加 `rollback_requested` 与 `rollback_completed` |
| KPI event | 否 | 追加修正事件 |

---

## 7. 运行时步骤映射

| UAS workflow step | MVP 状态 |
|-------------------|----------|
| `intent_activation` | `intent_created` |
| `knowledge_binding` | `evidence_checking` |
| `agent_planning` | `lead_qualifying` / `quote_drafting` |
| `runtime_topology` | `queued` / `running` |
| `system_mapping` | `capability_called` |
| `governance_check` | `policy_checking` / `approval_pending` |
| `evolution_plan` | `changeset_drafted` |
| `render_report` | `report_rendered` |

---

## 8. 必须覆盖的异常路径

1. 缺需求证据：`evidence_required` → `blocked` → 补证据 → 继续。
2. connector 失败：`failed_retryable` → 重试 → `needs_human`。
3. 折扣超阈值：`policy_checking` → `approval_pending`。
4. 审批拒绝：`rejected` → 降低折扣或关闭。
5. 信用 blocked：`business_blocked` → 失败报告。
6. 幂等冲突：`needs_human` → 审计确认。
