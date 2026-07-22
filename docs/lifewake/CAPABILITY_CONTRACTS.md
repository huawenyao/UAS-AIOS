# 生命回响 · 能力服务合约

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
| `EMOTION_IMPACT_FAILED` | wow_score 未过门禁 | 否 | 重炼或人工策展 |
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

## 6. `lw.ritual.render`

### 目的

将作品包装为自我确认仪式，并计算情感冲击分。

### 输入

```yaml
inputs:
  artifact_type: surprise
  artifact_ref: sur_001
  narrative_tone: gentle
```

### 输出

```yaml
result:
  ritual_id: ritual_001
  narrative: "这是你潜意识写给自己的回信。"
  inspiration_trace: []
  emotion_impact:
    wow_score: 0.86
    passed: true
    threshold: 0.7
```

---

## 7. `lw.audit.append`

追加审计事件；始终允许（G0），但 payload 不得包含原始连续生物流。

---

## 8. 预留能力

| 能力 | 状态 | 调用结果 |
|------|------|----------|
| `lw.memory.weave` | reserved | `FEATURE_RESERVED` |
| `lw.bond.visualize` | reserved | `FEATURE_RESERVED` |
| `lw.twin.draft` | reserved | `FEATURE_RESERVED` |
