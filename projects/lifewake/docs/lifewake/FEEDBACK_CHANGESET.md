# LifeWake 反馈与 ChangeSet

> 产品随用户成长而生长：反馈进入演化回路，但绝不自动剥夺用户对灵魂领土的控制。

---

## 1. 反馈类型

| 类型 | 来源 | 用途 |
|------|------|------|
| `meaning_feedback` | 用户选择 meaningful / not_meaningful / uncomfortable | 现实裁决；调整创作与门禁 |
| `bond_resonance` | 双人会话相关度与双方评价 | 优化混音与双向任务 |
| `consent_friction` | 授权/撤回行为 | 简化同意文案、收紧默认 scope |
| `run_review` | 内测策展人点评 | 情感冲击测试改进 |
| `timing_feedback` | 打扰、时机正好、希望更慢 | 调整 `TimingDecision` 策略 |
| `share_revoke` | 任一共同权利人撤回 | 验证 `SHARE_REVOKED` 与权利设计 |
| `device_recovery` | 断连后的重连/降级/结束 | 改进 Pulse 恢复流程 |

情感冲击测试不是模型真理。反馈进入 `EmotionImpact` 时必须分离：

1. `user_feedback`：用户的现实裁决，优先级最高；
2. `curation_rubric`：来源贴合、具体性、情绪安全、节奏、可访问性的可解释评审；
3. `model_auxiliary`：新颖度、覆盖率、风险提示等辅助信号。

反馈上下文必须引用交付时的 `RitualEnvelope` 与 `TimingDecision`；`SLOW_INSPIRATION_DEFERRED` 也可产生 timing feedback，但不能伪装为已交付 Ritual。

---

## 2. ChangeSet 草案格式

```yaml
changeset_id: cs-draft-CASE-014
source: human_feedback
target_pack: surprise_policy | pulse_policy | consent_copy | agent
summary: "无聊窗口下灵感任务应更具体到可执行的一句话"
auto_apply: false
evidence:
  - feedback_id: fb_001
  - emotion_impact_ref: impact_001
  - rubric_version: ritual_v1
hypothesis: "加入一个具体地点或动作约束可提升意义"
impact_scope: [inspiration_task]
guardrails: [consent_zero_leak, interruption_rate]
regression_cases: [CASE-001, CASE-008, CASE-009]
requires_approval: true
rollback_ref: surprise_policy_v1
```

### 硬约束

- `auto_apply` 在 v0.1 **必须为 false**
- 不得通过 ChangeSet 扩大数据用途至 `create_for_user` 之外
- 涉及同意文案的变更必须可回滚
- 必须有 feedback + EmotionImpact + rubric/事实证据，不能只引用模型分
- 必须声明影响范围、护栏、回归 CASE 与 rollback

---

## 3. 受控回写流程

```text
feedback_captured
  → emotion_impact_evaluated
  → attribution_reviewed
  → evolution_listener.draft_changeset
  → human_approval
  → limited_experiment
  → guardrail_review
  → apply_to_configs (manual / evolveApply) | rollback
  → audit.append
```

对应命令预留：仓库级 `/evolveApply`；LifeWake 子应用仅产出草案到 `database/feedback/`。

---

## 4. 归因与回退

| 反馈 | 首要归因层 | ChangeSet 目标 | 回退层 |
|---|---|---|---|
| 太通用/不像我 | 内容策略 | template/surprise policy | L2 策略 |
| 时机打扰 | timing 策略 | timing policy | L1 交付/L2 策略 |
| 被监控感 | 信号/解释/同意 | signal scope/consent copy | L3 治理 |
| duet 压力或不对称 | 邀请/Bond 协议 | bond policy | L3 流程治理 |
| 撤回后仍可访问 | share 执行 | capability/policy | L3，立即冻结 |
| 持续无意义 | 产品假设 | 主 BP/目标人群 | L4 产品 |

不得把所有低反馈都归因为模型参数；先检查现实实体、触点、时机、同意与关系结构。

---

## 5. KPI（意义与信任）

| 指标 | 说明 | v0.1 目标 |
|------|------|-----------|
| MRCR | 合格揭晓中用户显式确认有意义且护栏通过 | 方向性改善；阈值由内测预注册 |
| ChangeSet 证据完整率 | feedback+impact+rubric+scope+CASE+rollback 完整 | 100% |
| 同意撤回后零新处理 | revoke 后非审计处理事件 | 0 |
| 共享撤回成功率 | 所有 surface 按时 `SHARE_REVOKED` | 100% |
| 自动应用数 | 未审批 ChangeSet 自动生效 | 0 |

完整公式与采集点见 [METRICS_GROWTH_AND_BUSINESS](./METRICS_GROWTH_AND_BUSINESS.md)。

## 6. ChangeSet 验收

1. CASE-014 可从 feedback 顺序追到 EmotionImpact、ChangeSet 与 audit。
2. 用户负反馈能推翻历史模型高分。
3. ChangeSet 不包含原始 pulse、自由文本正文或伴侣拒绝理由。
4. 相关 CASE 回归或护栏失败时不发布/自动回滚。
5. 任何扩大 purpose/scope 的建议直接 `POLICY_DENIED`，不进入审批。
