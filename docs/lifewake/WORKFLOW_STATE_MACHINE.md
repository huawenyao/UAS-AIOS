# LifeWake 工作流状态机

> 定义同意门禁、惊喜交付、心跳会话、失败、撤回与人工接管路径。所有迁移必须写入 `AuditEvent`。

---

## 1. 总体状态机

```text
INTENT_CREATED
  → CONSENT_CHECKING
  → SIGNAL_WEAVING | DEVICE_LINKING
  → COMPOSING
  → IMPACT_CHECKING
  → TIMING_DECIDING
  → RITUAL_RENDERING
  → DELIVERED
  → CHANGESET_DRAFTED?
  → CLOSED

任意执行态
  → CONSENT_REQUIRED
  → CONSENT_REVOKED
  → SLOW_INSPIRATION_DEFERRED
  → BOND_BLOCKED
  → SHARE_REVOKED
  → DEVICE_PAUSED
  → SAFETY_HOLD
  → HUMAN_TAKEOVER
  → FAILED_RETRYABLE
  → FAILED_FINAL
  → CANCELLED
```

---

## 2. Intent 状态

| 状态 | 含义 | 允许迁移 |
|------|------|----------|
| `intent_created` | 意图已生成 | `consent_checking`、`cancelled` |
| `consent_checking` | 校验同意与用途 | `signal_weaving`、`device_linking`、`consent_required`、`policy_denied` |
| `signal_weaving` | 编织隐性信号 | `composing`、`failed_final` |
| `device_linking` | 连接心跳设备 | `composing`、`device_not_linked`、`failed_final` |
| `composing` | 调用 lw.surprise / lw.pulse | `impact_checking`、`bond_blocked`、`device_paused`、`failed_retryable`、`consent_revoked` |
| `impact_checking` | 用户反馈/同类反馈 + 策展 rubric 可解释门禁 | `timing_deciding`、`emotion_impact_failed`、`human_takeover` |
| `timing_deciding` | 计算 `TimingDecision` | `ritual_rendering`、`slow_inspiration_deferred`、`cancelled` |
| `slow_inspiration_deferred` | 时机/频率/质量未就绪 | `timing_deciding`、`cancelled`、`consent_revoked` |
| `ritual_rendering` | 生成 `RitualEnvelope` | `delivered`、`consent_revoked` |
| `delivered` | 已交付用户 | `changeset_drafted`、`closed` |
| `changeset_drafted` | 已生成演化建议 | `closed` |
| `closed` | 闭环结束 | 无 |

### 失败态

| 状态 | 含义 |
|------|------|
| `consent_required` | 需引导授权 |
| `consent_revoked` | 撤回后中止 |
| `bond_blocked` | 双向关系未通过 |
| `device_not_linked` | 设备未连接 |
| `device_paused` | 会话中设备断连，等待重连/降级/结束 |
| `emotion_impact_failed` | 用户反馈/rubric 门禁不足；不是模型真理 |
| `share_revoked` | 共同共享已撤回 |
| `safety_hold` | 高危路径停止娱乐化生成 |
| `failed_retryable` | connector 可重试失败 |
| `failed_final` | 不可重试失败 |
| `cancelled` | 用户取消 |

---

## 3. PulseSession 状态

```text
linking → live → completed
            ↓
          paused → live
            └────→ aborted
```

| 状态 | 进入条件 | 退出 |
|------|----------|------|
| `linking` | 设备授权开始 | 双方/单方 link 成功或失败 |
| `live` | 作曲进行中 | 完成或中止 |
| `paused` | 设备断连或任一方主动暂停 | 重连、双方确认降级或中止 |
| `completed` | 作品生成成功 | 可进入 ritual |
| `aborted` | 撤回同意 / 断连 / 取消 | 报告失败原因 |

---

## 4. Surprise 与慢灵感状态

```text
queued → composing → impact_checked → timing_decided
                                      ├→ deferred → timing_decided
                                      └→ ritual_ready → delivered → saved | dismissed
                              ↘ cancelled_by_revoke
```

撤回同意时：`queued/composing/composed(未送达)` → `cancelled_by_revoke`。

`deferred` 不进入技术重试；到 `reconsider_after` 后只重算 `TimingDecision`。

---

## 5. ShareGrant 状态

```text
draft → active → SHARE_REVOKED
               ↘ expired
```

- 任一共同权利人请求 revoke：所有 active surface 原子性转为 `SHARE_REVOKED`。
- 撤回后的 read 返回同名业务码；不能回退到 active，需双方重新创建新 grant。
- 外链缓存必须失效；审计只保留主体引用、生效时间与 surface。

---

## 6. 重试规则

| 错误 | 最大重试 | 失败后 |
|------|----------|--------|
| `CONNECTOR_UNAVAILABLE` | 3 | `needs_human` / `failed_retryable` |
| `DEVICE_DISCONNECTED` | 设备重连 3 次 | `device_paused`，用户决定降级/结束 |
| `CONSENT_REQUIRED` | 0 | `consent_required` |
| `CONSENT_REVOKED` | 0 | `consent_revoked` |
| `BOND_ASYMMETRIC` | 0 | `bond_blocked` |
| `EMOTION_IMPACT_FAILED` | 0（可新建重炼/策展任务） | `emotion_impact_failed` |
| `SLOW_INSPIRATION_DEFERRED` | 0 | 等待重评，不计失败 |
| `SHARE_REVOKED` | 0 | 保持 revoked |
| `SAFETY_HUMAN_REVIEW` | 0 | `safety_hold` |
| `VALIDATION_ERROR` | 0 | `failed_final` |
| `FEATURE_RESERVED` | 0 | `failed_final` |

---

## 7. 人工接管触发

- 高危关怀路径（M-02）
- connector 重试耗尽
- G4 外发请求（v0.1 默认拒绝并提示）
- 幂等冲突
- 用户反馈与策展 rubric 严重冲突且存在潜在伤害

## 8. 状态迁移不变量

1. consent 在任何执行态撤回，都优先于重试、defer 和交付。
2. `impact_checking` 先于 `timing_deciding`，两者都先于 `ritual_rendering`。
3. `EmotionImpact` 只有模型辅助信号时不能迁移到 `timing_deciding`。
4. `SLOW_INSPIRATION_DEFERRED` 不能产生 notification/delivery。
5. `SHARE_REVOKED` 是共享终态，所有读取 surface 必须拒绝。
6. duet 断连不能自动降级为单人作品；需双方明确确认或中止。
