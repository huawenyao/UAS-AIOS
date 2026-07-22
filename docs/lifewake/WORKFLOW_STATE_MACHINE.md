# 生命回响 · 工作流状态机

> 定义同意门禁、惊喜交付、心跳会话、失败、撤回与人工接管路径。所有迁移必须写入 `AuditEvent`。

---

## 1. 总体状态机

```text
INTENT_CREATED
  → CONSENT_CHECKING
  → SIGNAL_WEAVING | DEVICE_LINKING
  → COMPOSING
  → RITUAL_RENDERING
  → IMPACT_CHECKING
  → DELIVERED
  → CHANGESET_DRAFTED?
  → CLOSED

任意执行态
  → CONSENT_REQUIRED
  → CONSENT_REVOKED
  → BOND_BLOCKED
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
| `composing` | 调用 lw.surprise / lw.pulse | `ritual_rendering`、`bond_blocked`、`failed_retryable`、`consent_revoked` |
| `ritual_rendering` | 生成仪式叙事 | `impact_checking` |
| `impact_checking` | wow_score 门禁 | `delivered`、`emotion_impact_failed` |
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
| `emotion_impact_failed` | 情感冲击不足 |
| `failed_retryable` | connector 可重试失败 |
| `failed_final` | 不可重试失败 |
| `cancelled` | 用户取消 |

---

## 3. PulseSession 状态

```text
linking → live → completed
                 ↘ aborted
```

| 状态 | 进入条件 | 退出 |
|------|----------|------|
| `linking` | 设备授权开始 | 双方/单方 link 成功或失败 |
| `live` | 作曲进行中 | 完成或中止 |
| `completed` | 作品生成成功 | 可进入 ritual |
| `aborted` | 撤回同意 / 断连 / 取消 | 报告失败原因 |

---

## 4. Surprise 推送状态

```text
queued → composing → composed → delivered → saved | dismissed
                              ↘ cancelled_by_revoke
```

撤回同意时：`queued/composing/composed(未送达)` → `cancelled_by_revoke`。

---

## 5. 重试规则

| 错误 | 最大重试 | 失败后 |
|------|----------|--------|
| `CONNECTOR_UNAVAILABLE` | 3 | `needs_human` / `failed_retryable` |
| `CONSENT_REQUIRED` | 0 | `consent_required` |
| `CONSENT_REVOKED` | 0 | `consent_revoked` |
| `BOND_ASYMMETRIC` | 0 | `bond_blocked` |
| `EMOTION_IMPACT_FAILED` | 0（可人工策展重炼） | `emotion_impact_failed` |
| `VALIDATION_ERROR` | 0 | `failed_final` |
| `FEATURE_RESERVED` | 0 | `failed_final` |

---

## 6. 人工接管触发

- 高危关怀路径（M-02）
- connector 重试耗尽
- G4 外发请求（v0.1 默认拒绝并提示）
- 幂等冲突
