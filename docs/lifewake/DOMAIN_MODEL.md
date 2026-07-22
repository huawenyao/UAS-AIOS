# 生命回响 · 领域模型

> 定义 MVP 最小业务对象、字段、生命周期与事件。开发时先按本文建立 JSON 结构，再映射到 `projects/lifewake/database/` 与 `configs/`。

---

## 1. 对象关系

```text
Person
  ├─ Consent[]
  ├─ SignalBundle[]
  ├─ Surprise[]
  ├─ PulseSession[]
  └─ Bond[] ─── Person (partner)
        └─ SharedArtifact[]

Intent
  ├─ ConsentCheck
  ├─ CapabilityCall[]
  ├─ Ritual
  ├─ AuditEvent[]
  ├─ EmotionImpact
  └─ ChangeSet?
```

---

## 2. 核心实体

### 2.1 Person

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `person_id` | string | 是 | 用户唯一标识 |
| `display_name` | string | 是 | 展示名 |
| `persona_tags` | string[] | 否 | 自述标签（创作者/情侣等），非系统画像评分 |
| `style_prefs` | object | 否 | 音乐/视觉风格偏好 |
| `locale` | string | 否 | 语言区域 |

### 2.2 Consent

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `consent_id` | string | 是 | 同意记录 ID |
| `person_id` | string | 是 | 主体 |
| `scopes` | string[] | 是 | 如 `signals.low_sensitivity`、`device.pulse`、`share.partner` |
| `purpose` | enum | 是 | 仅允许 `create_for_user` |
| `status` | enum | 是 | `granted` / `revoked` / `expired` |
| `granted_at` | string | 是 | ISO 时间 |
| `revoked_at` | string | 否 | 撤回时间 |
| `withdrawable` | bool | 是 | 必须为 true |

**硬约束：** `purpose` 不得为 `profile_user` / `ads` / `score_user`。

### 2.3 SignalBundle

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bundle_id` | string | 是 | 信号包 ID |
| `person_id` | string | 是 | 主体 |
| `signals` | object[] | 是 | 低敏感信号项 |
| `sensitivity` | enum | 是 | MVP 仅 `low` |
| `consent_ref` | string | 是 | 关联同意 |
| `collected_at` | string | 是 | 采集时间 |

信号项示例：

```yaml
- kind: hum_melody
  value: "motif_jazzy_03"
- kind: favorite_artist_style
  value: "jazz_vocal"
- kind: late_night_search
  value: "雨夜散步"
- kind: geo_coarse
  value: "neighborhood_cafe_district"
- kind: mood_hint
  value: "lonely_curious"
```

### 2.4 Surprise

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `surprise_id` | string | 是 | 惊喜 ID |
| `person_id` | string | 是 | 接收者 |
| `kind` | enum | 是 | `song` / `artwork` / `inspiration_task` |
| `payload` | object | 是 | mock 资产引用与摘要 |
| `inspiration_trace` | object[] | 是 | 灵感来源解析 |
| `timing_window` | string | 是 | 如 `morning` / `commute` / `boredom` |
| `wow_score` | number | 否 | 情感冲击分 0-1 |
| `status` | enum | 是 | `composed` / `delivered` / `saved` / `dismissed` |

### 2.5 PulseSession

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `session_id` | string | 是 | 会话 ID |
| `mode` | enum | 是 | `solo` / `duet` |
| `participants` | string[] | 是 | person_id 列表 |
| `device_refs` | string[] | 是 | mock 设备引用 |
| `style` | enum | 是 | `classical` / `electronic` / `nature` |
| `mix_ratio` | object | 否 | `{heartbeat: 0.6, ambience: 0.4}` |
| `composition_ref` | string | 否 | 生成作品引用 |
| `sync_visual` | object | 否 | 双人同步可视化 |
| `status` | enum | 是 | `linking` / `live` / `completed` / `aborted` |

### 2.6 Bond

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bond_id` | string | 是 | 关系 ID |
| `members` | string[2] | 是 | 双方 person_id |
| `needs` | object | 是 | 各方情感需求声明 |
| `shared_artifacts` | string[] | 否 | 共创作品引用 |
| `status` | enum | 是 | `active` / `paused` / `dissolved` |

### 2.7 Ritual

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ritual_id` | string | 是 | 仪式 ID |
| `intent_ref` | string | 是 | 意图引用 |
| `artifact_ref` | string | 是 | Surprise 或 Pulse 作品 |
| `narrative` | string | 是 | 自我确认叙事文案 |
| `inspiration_trace` | object[] | 是 | 展示用解析 |
| `emotion_impact` | object | 是 | `{wow_score, passed}` |

### 2.8 Intent

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `intent_id` | string | 是 | 意图 ID |
| `intent_type` | enum | 是 | `surprise_delivery` / `pulse_solo` / `pulse_duet` / `feedback_review` |
| `goal` | string | 是 | 情感目标 |
| `actor_ref` | string | 是 | 发起人 |
| `risk_level` | enum | 是 | G0–G4（见治理矩阵） |
| `business_object_ref` | string | 是 | 关联对象 |

### 2.9 AuditEvent

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `audit_id` | string | 是 | 审计 ID |
| `event` | string | 是 | intent / consent / capability / ritual / result … |
| `trace_id` | string | 是 | 追踪 |
| `payload` | object | 是 | 事件内容（不含敏感原始生物流） |

---

## 3. 生命周期与事件

### 3.1 Consent

`draft → granted → revoked | expired`

事件：`consent.granted`、`consent.revoked`

### 3.2 Surprise

`queued → composing → composed → delivered → saved | dismissed`

事件：`surprise.composed`、`surprise.delivered`

### 3.3 PulseSession

`linking → live → completed | aborted`

事件：`pulse.linked`、`pulse.composed`、`pulse.shared`、`pulse.share_revoked`

---

## 4. 数据最小化

| 数据类型 | 允许用途 | 禁止用途 |
|----------|----------|----------|
| 低敏感浏览/哼唱/粗粒度位置 | 创作惊喜 | 用户评分、广告、保险定价 |
| 心跳流 | 当场作曲与纪念物 | 健康诊断、就业评估 |
| 关系互动 | 双向共创 | 监控伴侣、公开排行 |
