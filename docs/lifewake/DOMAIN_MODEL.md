# LifeWake 领域模型

> 定义 MVP 最小业务对象、字段、生命周期与事件。开发时先按本文建立 JSON 结构，再映射到 `projects/lifewake/database/` 与 `configs/`。

---

## 1. 对象关系

```text
Person
  ├─ ConsentGrant[]
  ├─ SignalBundle[]
  ├─ Surprise[]
  ├─ PulseSession[]
  └─ Bond[] ─── Person (partner)
        └─ SharedArtifact[]

Intent
  ├─ ConsentDecision
  ├─ TimingDecision
  ├─ CapabilityCall[]
  ├─ RitualEnvelope
  ├─ AuditEvent[]
  ├─ EmotionImpact
  ├─ ShareGrant?
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

### 2.2 ConsentGrant

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
| `beneficiaries` | string[] | 是 | 本人或明确的 Bond 双方 |
| `expires_at` | string | 是 | 不允许无期限隐性授权 |
| `processor_refs` | string[] | 否 | 实际处理供应商 |

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
| `impact_ref` | string | 否 | 指向 `EmotionImpact`；不得把模型分当用户感受 |
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

### 2.7 RitualEnvelope

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `envelope_id` | string | 是 | 交付信封 ID |
| `ritual_id` | string | 是 | 仪式 ID |
| `intent_ref` | string | 是 | 意图引用 |
| `artifact_ref` | string | 是 | Surprise 或 Pulse 作品 |
| `content_blocks` | object[] | 是 | audio/image/text/task/visual |
| `inspiration_trace` | object[] | 是 | 展示用解析 |
| `consent_refs` | string[] | 是 | 覆盖每位数据/权利主体 |
| `timing_decision_ref` | string | 是 | 交付时机依据 |
| `emotion_impact_ref` | string | 是 | 可解释门禁依据 |
| `owners` | string[] | 是 | 个人或共同权利人 |
| `actions` | string[] | 是 | save/feedback/delete/revoke_share 等 |
| `accessibility` | object | 是 | transcript、alt、reduced motion 等 |

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

### 2.10 EmotionImpact

`EmotionImpact` 是交付/重炼/策展的证据记录，**不是情感真理或人格评分**。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `impact_id` | string | 是 | 记录 ID |
| `artifact_ref` | string | 是 | 候选/已交付作品 |
| `user_feedback` | object[] | 否 | `meaningful/not_meaningful/uncomfortable` 等显式反馈 |
| `curation_rubric` | object | 是 | rubric 版本、维度、证据、评审人 |
| `model_auxiliary` | object | 否 | 新颖度/风险等辅助信号及不确定性 |
| `decision` | enum | 是 | `deliver/rework/curate/defer/reject` |
| `rationale` | string[] | 是 | 可解释理由 |
| `superseded_by_feedback` | bool | 是 | 用户反馈是否推翻既有辅助判断 |

硬约束：`model_auxiliary` 单独存在时不得得到 `deliver`。

### 2.11 TimingDecision

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `timing_id` | string | 是 | 决策 ID |
| `decision` | enum | 是 | `DELIVER_NOW` / `SLOW_INSPIRATION_DEFERRED` / `CANCELLED` |
| `reason_codes` | string[] | 是 | quiet_hours、frequency、quality_not_ready 等 |
| `reconsider_after` | string | 否 | defer 的最早重评时间 |
| `policy_version` | string | 是 | 时机策略版本 |
| `user_overridable` | bool | 是 | 用户是否可调整/取消 |

### 2.12 Keepsake 与 ShareGrant

| 实体 | 关键字段 | 约束 |
|---|---|---|
| `Keepsake` | `keepsake_id`、`envelope_ref`、`owners`、`retention`、`status` | 支持导出/删除；共同资产不能由平台单方改权 |
| `ShareGrant` | `share_id`、`keepsake_ref`、`grantor`、`surface`、`expires_at`、`status` | 每位共同权利人独立授权；任一方 revoke 触发 `SHARE_REVOKED` |

### 2.13 PolicyDecision 与 ChangeSet

| 实体 | 关键字段 | 约束 |
|---|---|---|
| `PolicyDecision` | `decision_id`、`risk_level`、`rules`、`result`、`next_action` | 年龄未知取更保守路径；不输出诊断 |
| `ChangeSet` | `changeset_id`、`evidence_refs`、`target_pack`、`diff`、`impact_scope`、`regression_cases`、`rollback_ref`、`auto_apply` | `auto_apply=false`；不得扩大 purpose |

---

## 3. 生命周期与事件

### 3.1 ConsentGrant

`draft → granted → revoked | expired`

事件：`consent.granted`、`consent.revoked`

### 3.2 Surprise

`queued → composing → composed → delivered → saved | dismissed`

事件：`surprise.composed`、`surprise.delivered`

### 3.3 PulseSession

`linking → live → completed | aborted`

事件：`pulse.linked`、`pulse.composed`、`pulse.shared`、`pulse.share_revoked`

### 3.4 TimingDecision

`evaluating → DELIVER_NOW | SLOW_INSPIRATION_DEFERRED | CANCELLED`

`SLOW_INSPIRATION_DEFERRED → evaluating` 只能由重评时间、用户调整或新上下文触发，不能用轮询制造触达。

### 3.5 ShareGrant

`draft → active → SHARE_REVOKED | expired`

事件：`share.granted`、`share.revoked`、`share.access_denied_after_revoke`。

### 3.6 RitualEnvelope

`draft → ready → revealed → saved | dismissed | deleted`

若 consent 在 `ready` 前撤回：`draft/ready → cancelled_by_revoke`。

---

## 4. 数据最小化

| 数据类型 | 允许用途 | 禁止用途 |
|----------|----------|----------|
| 低敏感浏览/哼唱/粗粒度位置 | 创作惊喜 | 用户评分、广告、保险定价 |
| 心跳流 | 当场作曲与纪念物 | 健康诊断、就业评估 |
| 关系互动 | 双向共创 | 监控伴侣、公开排行 |
| 产品遥测 | 去标识价值/可靠性评估 | 原始 pulse、自由文本、拒绝理由 |

## 5. 实体不变量

1. `RitualEnvelope.consent_refs` 必须覆盖所有数据主体和共同权利人。
2. duet 的 `owners` 恰为双方，不能以发起者作为唯一 owner。
3. `EmotionImpact` 分离用户反馈、策展 rubric 与模型辅助信号。
4. `TimingDecision=SLOW_INSPIRATION_DEFERRED` 时不得产生 delivery/notification。
5. `ShareGrant.status=SHARE_REVOKED` 时所有共享 surface 拒绝访问。
6. 原始连续 pulse 不进入 AuditEvent、KPIEvent 或 ChangeSet。
