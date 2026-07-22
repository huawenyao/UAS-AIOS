# 生命回响 · MVP 验收用例

> v0.1 配置原型必须跑通的端到端用例。每条用例通过 JSON 输入触发脚本，输出 report、audit、state。

---

## 1. 统一验收输出

| 输出 | 要求 |
|------|------|
| `intent` | 含 `intent_id`、`actor`、`intent_type`、`risk_level` |
| `consent` | 含检查结果或错误码 |
| `audit` | 至少记录 intent、consent、capability、result |
| `report` | 含结论、灵感解析或失败下一步 |
| `world_model_view` | subjects / objects / drive / blockers / connectors |
| `state.final` | 符合用例期望 |
| `errors` | 失败用例必须有错误码 |

---

## 2. CASE-001：授权后惊喜盲盒成功交付

### 输入

```yaml
case_id: CASE-001
intent_type: surprise_delivery
person_id: person_ada
consent:
  scopes: [signals.low_sensitivity]
  status: granted
  purpose: create_for_user
signals:
  - kind: hum_melody
    value: motif_jazzy_03
  - kind: favorite_artist_style
    value: jazz_vocal
timing_window: boredom
```

### 期望

| 项 | 结果 |
|----|------|
| capability | `lw.surprise.compose` success |
| uniqueness_refs | 非空 |
| wow_score | ≥ 0.7 |
| 最终状态 | `delivered` 或 `closed` |

---

## 3. CASE-002：无同意拒绝惊喜

### 输入

```yaml
case_id: CASE-002
intent_type: surprise_delivery
person_id: person_ada
consent:
  scopes: []
  status: missing
```

### 期望

| 项 | 结果 |
|----|------|
| 错误码 | `CONSENT_REQUIRED` |
| 最终状态 | `consent_required` |
| 禁止 | 不得产生 surprise payload |

---

## 4. CASE-003：同意撤回中止创作

### 输入

```yaml
case_id: CASE-003
intent_type: surprise_delivery
person_id: person_ada
consent:
  scopes: [signals.low_sensitivity]
  status: revoked
  purpose: create_for_user
```

### 期望

| 项 | 结果 |
|----|------|
| 错误码 | `CONSENT_REVOKED` |
| 最终状态 | `consent_revoked` |

---

## 5. CASE-004：单人心跳音乐成功

### 输入

```yaml
case_id: CASE-004
intent_type: pulse_solo
person_id: person_ada
consent:
  scopes: [device.pulse]
  status: granted
device_linked: true
style: nature
```

### 期望

| 项 | 结果 |
|----|------|
| capability | `lw.pulse.compose` success |
| mode | `solo` |
| composition_ref | 非空 |
| 最终状态 | `delivered` 或 `closed` |

---

## 6. CASE-005：双人心跳共鸣成功

### 输入

```yaml
case_id: CASE-005
intent_type: pulse_duet
bond_id: bond_ada_lee
participants: [person_ada, person_lee]
consent_by_person:
  person_ada: {scopes: [device.pulse, share.partner], status: granted}
  person_lee: {scopes: [device.pulse, share.partner], status: granted}
bond_needs:
  person_ada: [connection, keepsake]
  person_lee: [connection, being_heard]
needs_met: [person_ada, person_lee]
style: classical
```

### 期望

| 项 | 结果 |
|----|------|
| capability | `lw.pulse.duet` success |
| bidirectional | true |
| sync_visual | 存在 |
| risk_level | G3 |
| 最终状态 | `delivered` 或 `closed` |

---

## 7. CASE-006：双人模式非双向需求被拦截

### 输入

```yaml
case_id: CASE-006
intent_type: pulse_duet
participants: [person_ada, person_lee]
consent_by_person:
  person_ada: {scopes: [device.pulse, share.partner], status: granted}
  person_lee: {scopes: [device.pulse, share.partner], status: granted}
needs_met: [person_ada]
```

### 期望

| 项 | 结果 |
|----|------|
| 错误码 | `BOND_ASYMMETRIC` |
| 最终状态 | `bond_blocked` |

---

## 8. CASE-007：生成器短暂不可用后恢复

### 输入

```yaml
case_id: CASE-007
intent_type: surprise_delivery
consent:
  scopes: [signals.low_sensitivity]
  status: granted
  purpose: create_for_user
signals:
  - kind: mood_hint
    value: lonely_curious
mock_failure:
  capability: lw.surprise.compose
  error: CONNECTOR_UNAVAILABLE
```

### 期望

| 项 | 结果 |
|----|------|
| connector.ok | true |
| retries | ≤ 3 |
| 最终状态 | `delivered` 或 `closed` |

---

## 9. CASE-008：低 wow 反馈生成 ChangeSet 草案

### 输入

```yaml
case_id: CASE-008
intent_type: feedback_review
feedback:
  feedback_type: wow_rating
  target_ref: sur_meh_001
  rating: 2
  wow_score: 0.42
  comment: "灵感任务太空泛，不够可执行"
  suggested_change:
    target_pack: surprise_policy
    summary: "灵感任务必须落到一句话可执行动作"
```

### 期望

| 项 | 结果 |
|----|------|
| changeset | 存在 |
| auto_apply | false |
| 最终状态 | `changeset_drafted` |
