# LifeWake MVP 验收用例

> CASE-001～014 验证产品价值、主权、安全、失败恢复与演化闭环。每例必须产出 state、audit、report，以及成功 `RitualEnvelope` 或明确错误/延期结果。

## 1. 统一输出契约

| 输出 | 必须字段 |
|---|---|
| `intent` | `intent_id`、`actor_ref`、`intent_type`、`risk_level` |
| `consent_decision` | 每位主体的 scope、purpose、status、decision |
| `timing_decision` | decision、reason、`reconsider_after?` |
| `capability_calls` | capability、idempotency_key、result/error |
| `ritual_envelope` | 成功交付时含 content、trace、consent、timing、actions |
| `emotion_impact` | user feedback、curation rubric、model auxiliary 分离存储 |
| `audit` | intent、policy、consent、capability、state、result |
| `state.final` | 与用例期望一致 |
| `next_action` | 失败、延期、撤回时必填 |

## 2. 用例总表

| CASE | 场景 | 期望终态/码 | 哲学原则 | KPI |
|---|---|---|---|---|
| 001 | 授权后单人惊喜 | `delivered/closed` | 生命独奏、解释主权 | MRCR、trace 覆盖率 |
| 002 | 无同意 | `CONSENT_REQUIRED` | 隐私领土 | 未授权处理数=0 |
| 003 | 创作中撤回 | `CONSENT_REVOKED` | 可撤回主权 | 撤回后新处理数=0 |
| 004 | solo pulse | `delivered/closed` | 生命值得倾听、不诊断 | Ritual 完成率 |
| 005 | duet 成功 | `delivered/closed` | 双向连接 | 双方同意完整率 |
| 006 | duet 非双向 | `BOND_ASYMMETRIC` | 关系不占有 | 单方共享数=0 |
| 007 | 生成器暂时失败 | 恢复后 `closed` | 安全失败 | 恢复率、重复交付数=0 |
| 008 | 低 wow/低冲击 | `EMOTION_IMPACT_FAILED` | 反馈裁决现实 | 低冲击拦截率 |
| 009 | 慢灵感延期 | `SLOW_INSPIRATION_DEFERRED` | 慢灵感 | defer 接受率、打扰率 |
| 010 | 共同共享撤回 | `SHARE_REVOKED` | 共同拥有、独立退出 | 撤回成功率/时延 |
| 011 | 未成年人 | 受限本地/`POLICY_DENIED` | 脆弱主体优先 | 未成年人外发违规=0 |
| 012 | 设备断连 | 恢复/降级/`aborted` | 不以完成压倒主权 | 安全恢复率 |
| 013 | 高危信号 | `SAFETY_HUMAN_REVIEW` | 敬畏人、拒绝娱乐化 | 娱乐化生成数=0 |
| 014 | 串联反馈→ChangeSet | `changeset_drafted` | 受控演化 | 证据完整率、auto_apply=0 |

## CASE-001 · 授权后惊喜成功交付

```yaml
case_id: CASE-001
intent_type: surprise_delivery
person_id: person_ada
consent: {scopes: [signals.low_sensitivity], status: granted, purpose: create_for_user}
signals:
  - {kind: hum_melody, value: motif_jazzy_03}
  - {kind: favorite_artist_style, value: jazz_vocal}
timing_context: {window: commute, quiet_hours: false}
curation_rubric: {source_fit: pass, specificity: pass, emotional_safety: pass}
```

**期望**

- `lw.surprise.compose` 成功，`uniqueness_refs` 非空。
- `TimingDecision.decision=DELIVER_NOW`。
- `RitualEnvelope` 含 trace、consent_ref、timing、delete/feedback 动作。
- `EmotionImpact` 明确 rubric 证据；不得只有模型分。
- 追溯：宪章“生命独奏/创造共谋者” → F1/F3 → Core；KPI：MRCR、M-04。

## CASE-002 · 无同意拒绝惊喜

```yaml
case_id: CASE-002
intent_type: surprise_delivery
person_id: person_ada
consent: {scopes: [], status: missing}
```

**期望**

- `CONSENT_REQUIRED`，终态 `consent_required`。
- 无 signal read、compose、notification 或 artifact。
- report 指向 Consent Center，不使用诱导文案。
- 追溯：宪章“隐私领土” → F1/F6 → Privacy；KPI：M-07、未授权处理数=0。

## CASE-003 · 创作中同意撤回

```yaml
case_id: CASE-003
intent_type: surprise_delivery
person_id: person_ada
consent: {scopes: [signals.low_sensitivity], status: granted, purpose: create_for_user}
inject_event: {after_state: composing, event: consent.revoked}
```

**期望**

- 运行中止，终态 `consent_revoked`，错误 `CONSENT_REVOKED`。
- 队列取消，未交付 asset 清理；仅保留最小审计。
- revoke 后非审计处理事件为 0，重复撤回幂等。
- 追溯：宪章“可撤回灵魂领土” → F1/F6；KPI：M-08/M-09。

## CASE-004 · Solo Pulse 成功

```yaml
case_id: CASE-004
intent_type: pulse_solo
person_id: person_ada
consent: {scopes: [device.pulse], status: granted, purpose: create_for_user}
device: {ref: mock_band_ada, linked: true}
style: nature
accessibility: {audio: true, reduced_motion: true}
```

**期望**

- `lw.pulse.compose` 成功，mode=solo，有 composition 和无动态视觉变体。
- 无 health/anxiety/abnormal 标签；原始连续 pulse 不入 audit/telemetry。
- 生成可保存的 `RitualEnvelope`。
- 追溯：宪章“生命值得倾听/技术服务自我发现” → F7；KPI：完成率、非诊断违规=0。

## CASE-005 · Duet 双向成功

```yaml
case_id: CASE-005
intent_type: pulse_duet
bond_id: bond_ada_lee
participants: [person_ada, person_lee]
consent_by_person:
  person_ada: {scopes: [device.pulse, share.partner], status: granted}
  person_lee: {scopes: [device.pulse, share.partner], status: granted}
needs:
  person_ada: [connection, keepsake]
  person_lee: [connection, being_heard]
devices: {person_ada: linked, person_lee: linked}
```

**期望**

- Bond active、双向 needs 通过；`lw.pulse.duet` 成功。
- `RitualEnvelope.owners` 包含双方；生成两份独立 rights receipt。
- `sync_visual` 不展示心率排名或关系分。
- 追溯：宪章“真正连接/关系编织” → F2；KPI：M-10=100%、双方完成率。

## CASE-006 · Duet 非双向需求拦截

```yaml
case_id: CASE-006
intent_type: pulse_duet
participants: [person_ada, person_lee]
consent_by_person:
  person_ada: {scopes: [device.pulse, share.partner], status: granted}
  person_lee: {scopes: [device.pulse, share.partner], status: granted}
needs_met: [person_ada]
```

**期望**

- `BOND_ASYMMETRIC`，终态 `bond_blocked`，无 duet asset。
- 对双方只显示“共同条件尚未满足”，不暴露另一方需求或拒绝原因。
- 不自动重复邀请。
- 追溯：宪章“关系不占有” → F2；KPI：单方共享数=0。

## CASE-007 · 生成器短暂不可用后恢复

```yaml
case_id: CASE-007
intent_type: surprise_delivery
consent: {scopes: [signals.low_sensitivity], status: granted, purpose: create_for_user}
signals: [{kind: mood_hint, value: lonely_curious}]
mock_failure:
  capability: lw.surprise.compose
  error: CONNECTOR_UNAVAILABLE
  fail_attempts: 2
```

**期望**

- 同一 idempotency_key 最多重试 3 次，第 3 次恢复。
- 仅一个 artifact、一次交付；不扩大数据输入。
- audit 记录每次尝试和恢复点，终态 `closed`。
- 追溯：宪章“敬畏人/安全失败” → F7；KPI：恢复成功率、重复交付=0。

## CASE-008 · 低 wow/低冲击进入重炼或策展

```yaml
case_id: CASE-008
intent_type: surprise_delivery
candidate:
  uniqueness_refs: [mood_hint]
user_research_feedback: {signal: not_meaningful, reason_category: too_generic}
curation_rubric:
  source_fit: fail
  specificity: fail
  emotional_safety: pass
model_auxiliary: {novelty: 0.91, predicted_wow: 0.88}
```

**期望**

- 尽管模型辅助分高，结果仍为 `EMOTION_IMPACT_FAILED`。
- `EmotionImpact.decision=rework|curate`，记录用户反馈与 rubric。
- 不进入 Ritual Stream；可选择重炼、人工策展或删除。
- 追溯：宪章“情感重量/反馈裁决” → F3；KPI：M-05，模型越权裁决=0。

## CASE-009 · 慢灵感延期

```yaml
case_id: CASE-009
intent_type: surprise_delivery
candidate_ready: true
timing_context:
  quiet_hours: true
  deliveries_last_24h: 1
  max_surprises_per_day: 1
```

**期望**

- `TimingDecision.decision=SLOW_INSPIRATION_DEFERRED`。
- 含 reason=`quiet_hours|frequency_guardrail`、`reconsider_after` 和 cancel 动作。
- 无通知、红点、倒计时；到点只重评。
- 追溯：宪章“慢灵感” → F4/F5；KPI：M-12/M-13。

## CASE-010 · 共同纪念物共享撤回

```yaml
case_id: CASE-010
intent_type: share_revoke
keepsake_id: keep_duet_001
owners: [person_ada, person_lee]
requested_by: person_lee
active_surfaces: [bond_space, expiring_link]
```

**期望**

- `lw.share.revoke` 幂等成功；状态/结果码 `SHARE_REVOKED`。
- Bond Space 对方访问与外链立即失效；不披露撤回理由。
- 双方 receipt 保留最小元数据，各自私有材料按各自 consent 处理。
- 追溯：宪章“共同拥有、独立退出” → F2/F6；KPI：M-09/M-11。

## CASE-011 · 未成年人受限路径

```yaml
case_id: CASE-011
intent_type: pulse_duet
person_id: person_minor
age_gate: minor
requested_actions: [pulse_solo, pulse_duet, external_share]
```

**期望**

- 可选仅本地受限 solo preview；duet 与 external share 返回 `POLICY_DENIED`。
- 不采集关系 needs，不创建公开/可转发链接。
- 文案适龄、非诱导；audit 不记录精确年龄。
- 追溯：宪章“敬畏人/脆弱主体优先” → F1/F7；KPI：未成年人外发违规=0。

## CASE-012 · Pulse 设备断连

```yaml
case_id: CASE-012
intent_type: pulse_duet
participants: [person_ada, person_lee]
all_consents_valid: true
inject_event: {after_state: live, participant: person_lee, event: device.disconnected}
user_resolution: reconnect
```

**期望**

- 共同生成暂停、音频平滑淡出；返回 `DEVICE_DISCONNECTED`。
- 提供 reconnect、无设备降级（仅双方确认）、结束。
- 重连时复用同一 session/consent，不重复交付；失败则 `aborted`。
- 对方只看到连接断开，不看到健康推断。
- 追溯：宪章“技术不占有/安全失败” → F7；KPI：M-14、诊断文案违规=0。

## CASE-013 · 高危信号停止娱乐化生成

```yaml
case_id: CASE-013
intent_type: surprise_delivery
safety_signal: {category: possible_self_harm, confidence: uncertain}
```

**期望**

- 停止 surprise compose，结果 `SAFETY_HUMAN_REVIEW`，终态 `safety_hold`。
- 只展示直接、非诊断的支持选择与退出；不生成歌曲/任务。
- 原始文本不进入普通策展或增长分析。
- 追溯：宪章“敬畏人” → F1/F7；KPI：娱乐化生成=0、安全路由正确率。

## CASE-014 · 串联反馈生成受控 ChangeSet

```yaml
case_id: CASE-014
intent_type: surprise_delivery
consent:
  status: granted
  purpose: create_for_user
  scopes: [signals.low_sensitivity]
signals:
  - {kind: hum_melody, value: motif_jazzy_03}
  - {kind: favorite_artist_style, value: jazz_vocal}
curator_score: 0.9
post_delivery_feedback:
  feedback_id: fb_001
  # target_ref 由真实交付的 RitualEnvelope 生成，不作为输入
  signal: not_meaningful
  reason_category: too_generic
  rating: 2
  comment: "灵感任务太空泛，不够可执行"
```

**期望**

- 流程为 `ritual_delivered → feedback_captured → impact_evaluated → changeset_drafted`；feedback 的 `target_ref` 必须等于本次真实 `ritual_id`。
- ChangeSet 含 evidence、diff、影响范围、护栏、回归 CASE、审批与 rollback。
- `auto_apply=false`；不得新增 scope 或改变 purpose。
- 追溯：宪章“产品随用户成长” → F3；KPI：M-17、auto_apply 数=0。

## 3. 验收判定

- 任一主权、安全或关系护栏失败，整套 MVP 不通过。
- CASE 不能仅靠文档断言；L3 runnable subapp 应输出可比对的 state/audit/report。
- 模型辅助分不能替代 CASE-008 的用户反馈和 rubric 证据。
- CASE-014 只能证明受控学习链存在，不能自动发布策略。
