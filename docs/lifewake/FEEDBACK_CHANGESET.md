# 生命回响 · 反馈与 ChangeSet

> 产品随用户成长而生长：反馈进入演化回路，但绝不自动剥夺用户对灵魂领土的控制。

---

## 1. 反馈类型

| 类型 | 来源 | 用途 |
|------|------|------|
| `wow_rating` | 用户对惊喜/心跳的 wow/meh | 调整炼金策略、时机窗口 |
| `bond_resonance` | 双人会话相关度与双方评价 | 优化混音与双向任务 |
| `consent_friction` | 授权/撤回行为 | 简化同意文案、收紧默认 scope |
| `run_review` | 内测策展人点评 | 情感冲击测试改进 |

---

## 2. ChangeSet 草案格式

```yaml
changeset_id: cs-draft-CASE-008
source: human_feedback
target_pack: surprise_policy | pulse_policy | consent_copy | agent
summary: "无聊窗口下灵感任务应更具体到可执行的一句话"
auto_apply: false
evidence:
  - feedback_id: fb_001
  - wow_score: 0.42
requires_approval: true
```

### 硬约束

- `auto_apply` 在 v0.1 **必须为 false**
- 不得通过 ChangeSet 扩大数据用途至 `create_for_user` 之外
- 涉及同意文案的变更必须可回滚

---

## 3. 受控回写流程

```text
feedback_captured
  → evolution_listener.draft_changeset
  → human_approval
  → apply_to_configs (manual / evolveApply)
  → audit.append
```

对应命令预留：仓库级 `/evolveApply`；LifeWake 子应用仅产出草案到 `database/feedback/`。

---

## 4. KPI（情感而非效率）

| 指标 | 说明 | v0.1 目标 |
|------|------|-----------|
| 首次 wow 通过率 | 首次核心体验 wow_score≥0.7 | ≥80% 内测样本 |
| 同意撤回后零泄漏 | 撤回后无新创作/推送 | 100% |
| 双人双向通过率 | duet 无 BOND_ASYMMETRIC | 内测可解释为 0 容忍 |
| 慢灵感合规 | 不超日推送阈值 | 100% |
