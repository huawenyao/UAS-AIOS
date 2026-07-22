# LifeWake 能力服务合约

> Agent 不直连设备厂商或多模态厂商 SDK，只调用 `lw.*` 语义能力。本文定义 P0 能力的输入、输出、错误、权限、幂等与回滚。

---

## 1. 通用调用信封

```yaml
capability: lw.surprise.compose
version: v1
tenant_id: personal_space
trace_id: trace_001
intent_ref: int_001
actor:
  type: agent
  id: surprise_alchemist
on_behalf_of: person_ada
idempotency_key: int_001:person_ada:surprise
inputs: {}
policy:
  required_scopes: ["signals.low_sensitivity"]
  max_risk_level: G2
  purpose: create_for_user
audit:
  audit_ref: audit_001
```

### 1.1 通用响应

```yaml
status: success | failed | needs_human_review
result: {}
error:
  code: null
  message: null
  retryable: false
rollback:
  rollback_supported: true
  rollback_ref: null
audit:
  audit_ref: audit_001
```

### 1.2 通用错误码

| 错误码 | 含义 | 可重试 | 下一步 |
|--------|------|--------|--------|
| `CONSENT_REQUIRED` | 缺少有效同意 | 否 | 引导授权 |
| `CONSENT_REVOKED` | 同意已撤回 | 否 | 停止创作并清理待推送 |
| `POLICY_DENIED` | 用途或风险策略拒绝 | 否 | 说明原因 |
| `BOND_ASYMMETRIC` | 双人模式仅满足单方需求 | 否 | Bond Guardian 补齐双方 |
| `DEVICE_NOT_LINKED` | 心跳设备未连接 | 否 | 连接设备 |
| `VALIDATION_ERROR` | 输入不合法 | 否 | 修正输入 |
| `CONNECTOR_UNAVAILABLE` | mock/生成器不可用 | 是 | 重试或人工接管 |
| `DEVICE_DISCONNECTED` | 会话中设备断连 | 是 | 重连、双方确认降级或结束 |
| `EMOTION_IMPACT_FAILED` | 用户反馈 + 策展 rubric 门禁未过 | 否 | 重炼、人工策展或删除 |
| `SLOW_INSPIRATION_DEFERRED` | 时机、频率或质量尚不适合交付 | 否 | 到期重评或用户取消 |
| `SHARE_REVOKED` | 任一权利人已撤回共同共享 | 否 | 禁止访问并展示权利说明 |
| `SAFETY_HUMAN_REVIEW` | 高危情境停止娱乐化生成 | 否 | 安全资源/人工路径/退出 |
| `FEATURE_RESERVED` | 扩展能力未启用 | 否 | 提示后续版本 |
| `IDEMPOTENCY_CONFLICT` | 幂等冲突 | 否 | 人工审计 |

---

## 2. `lw.consent.check`

### 目的

校验指定 scopes 是否处于 `granted`，且 purpose 仅为 `create_for_user`。

### 输入

```yaml
inputs:
  person_id: person_ada
  required_scopes: ["signals.low_sensitivity"]
  purpose: create_for_user
```

### 输出

```yaml
result:
  allowed: true
  consent_id: consent_001
  missing_scopes: []
```

---

## 3. `lw.surprise.compose`

### 目的

基于 SignalBundle 生成惊喜作品与灵感解析。

### 权限

| 项 | 要求 |
|----|------|
| scope | `signals.low_sensitivity` |
| 最大风险 | G2 |
| 审批 | 默认无；外部分享升 G3 |

### 输入

```yaml
inputs:
  person_id: person_ada
  signal_bundle_ref: bundle_001
  preferred_kinds: ["song", "artwork", "inspiration_task"]
  timing_window: boredom
```

### 输出

```yaml
result:
  surprise_id: sur_001
  kind: song
  payload:
    asset_ref: mock://audio/sur_001.wav
    title: "雨夜哼唱 · 爵士回响"
    summary: "以你的旋律动机融合爵士人声质感"
  inspiration_trace:
    - signal: hum_melody
      explanation: "你无意识哼唱的动机被保留为主题"
    - signal: favorite_artist_style
      explanation: "你反复回味的爵士风格成为编配底色"
  uniqueness_refs: ["hum_melody", "favorite_artist_style"]
```

### 回滚

支持撤销未送达惊喜；已送达仅可标记 `dismissed`，不删除审计。

---

## 4. `lw.pulse.compose`

### 目的

单人模式：将 PulseStream 映射为生物韵律音乐。

### 权限

| 项 | 要求 |
|----|------|
| scope | `device.pulse` |
| 最大风险 | G2 |

### 输入

```yaml
inputs:
  person_id: person_ada
  device_ref: mock_band_ada
  style: nature
  mix_ratio:
    heartbeat: 0.7
    ambience: 0.3
```

### 输出

```yaml
result:
  session_id: pulse_001
  mode: solo
  composition_ref: mock://audio/pulse_001.wav
  waveform_ref: mock://visual/pulse_001.json
  tempo_map:
    - t: 0
      bpm_from_hr: 72
    - t: 30
      bpm_from_hr: 88
```

---

## 5. `lw.pulse.duet`

### 目的

双人模式：混合双方心跳生成共鸣交响曲。

### 权限

| 项 | 要求 |
|----|------|
| scopes | 双方 `device.pulse` + `share.partner` |
| Bond | 必须存在 active Bond，且双向 needs 通过 |
| 最大风险 | G3（共享纪念物） |

### 输入

```yaml
inputs:
  bond_id: bond_ada_lee
  participants: [person_ada, person_lee]
  style: classical
  share_keepsake: true
```

### 输出

```yaml
result:
  session_id: pulse_duet_001
  mode: duet
  composition_ref: mock://audio/pulse_duet_001.wav
  sync_visual:
    correlation: 0.82
    motif: "interwoven_waves"
  keepsake_ref: mock://keepsake/pulse_duet_001
  bond_check:
    bidirectional: true
    needs_met: [person_ada, person_lee]
```

### 错误特化

若仅一方 needs 满足 → `BOND_ASYMMETRIC`。

---

## 6. `lw.timing.decide`

### 目的

在内容质量、安静期、频率和用户节奏约束下决定交付或延期。

```yaml
inputs:
  person_id: person_ada
  candidate_ref: sur_001
  requested_window: commute
  quiet_hours: false
  deliveries_last_24h: 0
  quality_ready: true
result:
  timing_id: timing_001
  decision: DELIVER_NOW
  reason_codes: [user_allowed_window, quality_ready]
  reconsider_after: null
```

若延期，响应 status 仍为成功决策，业务结果码为 `SLOW_INSPIRATION_DEFERRED`；不得调用通知能力。

---

## 7. `lw.impact.evaluate`

### 目的

生成 `EmotionImpact`。情感冲击测试不是模型真理，而是**用户反馈 + 策展 rubric** 的可解释门禁；模型只提供辅助信号。

```yaml
inputs:
  artifact_ref: sur_001
  user_feedback:
    - signal: not_meaningful
      reason_category: too_generic
  curation_rubric:
    version: ritual_v1
    dimensions:
      source_fit: fail
      specificity: fail
      emotional_safety: pass
  model_auxiliary:
    predicted_wow: 0.88
    uncertainty: 0.21
result:
  impact_id: impact_001
  decision: rework
  rationale: [user_feedback_not_meaningful, source_fit_failed]
  superseded_by_feedback: true
```

硬约束：缺用户/同类反馈时可由 rubric 决定进入内测，但模型信号单独存在不能 `deliver`。

---

## 8. `lw.ritual.render`

### 目的

将已通过治理、时机和影响门禁的作品封装为 `RitualEnvelope`；不在渲染阶段伪造情感分。

### 输入

```yaml
inputs:
  artifact_type: surprise
  artifact_ref: sur_001
  narrative_tone: gentle
  timing_decision_ref: timing_001
  emotion_impact_ref: impact_001
```

### 输出

```yaml
result:
  envelope_id: renv_001
  ritual_id: ritual_001
  content_blocks:
    - {type: audio, asset_ref: "mock://audio/sur_001.wav", autoplay: false}
  inspiration_trace:
    - {source_category: hum_melody, explanation: "保留了四音动机"}
  consent_refs: [consent_001]
  timing_decision_ref: timing_001
  emotion_impact_ref: impact_001
  owners: [person_ada]
  actions: [reveal, save, feedback, delete]
```

---

## 9. `lw.share.revoke`

### 目的

任一共同权利人撤回后，使所有共享 surface 立即失效。

```yaml
inputs:
  keepsake_id: keep_duet_001
  requested_by: person_lee
  share_grant_refs: [share_ada, share_lee]
result:
  status: SHARE_REVOKED
  revoked_surfaces: [bond_space, expiring_link]
  enforced_at: 2026-07-22T03:00:01Z
  receipts: [receipt_ada, receipt_lee]
```

幂等键按 `keepsake_id:requested_by:revoke`；重复调用仍返回同一生效结果，不披露撤回理由。

---

## 10. `lw.feedback.capture` 与 `lw.changeset.draft`

`lw.feedback.capture` 只接收结构化枚举与可选加密正文引用；正文不得进入遥测。

`lw.changeset.draft` 必须输入 feedback、EmotionImpact、rubric 版本、目标 pack、假设、护栏、回归 CASE 和 rollback；输出 `auto_apply: false`。扩大 purpose/scope 返回 `POLICY_DENIED`。

---

## 11. `lw.audit.append`

追加审计事件；始终允许（G0），但 payload 不得包含原始连续生物流、自由文本反馈、伴侣拒绝理由或诊断推断。

---

## 12. 预留能力

| 能力 | 状态 | 调用结果 |
|------|------|----------|
| `lw.memory.weave` | reserved | `FEATURE_RESERVED` |
| `lw.bond.async_create` | reserved | `FEATURE_RESERVED` |
| `lw.twin.draft` | reserved | `FEATURE_RESERVED` |
| `lw.template.publish` | reserved | `FEATURE_RESERVED` |

## 13. 合约不变量

1. compose 能力不得直接通知；必须依次生成 `EmotionImpact`、`TimingDecision`、`RitualEnvelope`。
2. duet 输入必须含双方 consent refs 与 active Bond。
3. `EmotionImpact` 的三类证据分别存储，模型不得冒充 user feedback。
4. `SLOW_INSPIRATION_DEFERRED` 是有效业务结果，不进入重试队列。
5. `SHARE_REVOKED` 后任何 read/share 能力都必须拒绝。
6. 所有补偿动作保持审计，但清除未交付内容和超范围数据。
