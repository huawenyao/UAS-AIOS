# LifeWake 正式项目开发计划

> 本文件把 `docs/lifewake/` 商业与产品设计规约映射为可落地的工程实现计划，并标注当前完成度。
> 现状基线：`scripts/lifewake_policy.py`（450 行真实治理引擎）+ 14 CASE 验收（全通过）已存在；
> 本计划在其之上补齐**正式项目架构**，而非重写治理核心。

## 一、定位

| 维度 | Demo（`prototype/`） | 正式项目（本计划） |
|------|----------------------|--------------------|
| 形态 | 静态三件套前端 | 类型化 Python 包 + 能力契约 + 状态机 + 存储 + CLI |
| 输入 | 仅 sessionStorage | 真实 Intent 输入边界（CLI/JSON） |
| 校验 | 结构 smoke test | jsonschema 实体 + RitualEnvelope 校验 |
| 编排 | 隐式 run_case | 显式状态机 + 顺序不变量 + 幂等 |
| 持久化 | 无 | 仓储模式（audit/runs/feedback/cognitive_state） |
| 指标 | 无 | M-01~M-18 + MRCR 北极星 |

## 二、架构（UAS 八元组映射）

```
Intent(I) → Consent(K/G) → Signal/Device(R/S) → Compose(A/S) →
Impact(E) → Timing(R) → Ritual(Π) → Deliver → Feedback(E) → ChangeSet(E)
                                                              ↓ auto_apply=false
```

正式包 `projects/lifewake/lifewake/`：

| 模块 | 职责 | 规约来源 |
|------|------|----------|
| `domain.py` | 15 个类型化实体 + 6 不变量 | DOMAIN_MODEL.md |
| `schemas.py` | jsonschema 校验（entity + ritual_envelope） | CAPABILITY_CONTRACTS / DOMAIN_MODEL |
| `capabilities.py` | `lw.*` 注册表 + 通用调用/响应信封 + 幂等 + 审计 | CAPABILITY_CONTRACTS.md |
| `orchestrator.py` | 状态机 intent_created→closed + 顺序不变量 | WORKFLOW_STATE_MACHINE.md |
| `store.py` | 仓储模式持久化 | DOMAIN_MODEL / README |
| `metrics.py` | M-01~M-18 + MRCR + 护栏否决 | METRICS_GROWTH_AND_BUSINESS.md |
| `cli.py` | 真实输入边界（非仅 CASE 夹具） | FUNCTIONAL_DESIGN.md |
| `governance.py` | 复用 `scripts/lifewake_policy.py` | GOVERNANCE_MATRIX.md |

## 三、`lw.*` 能力清单（P0 必实现）

| 能力 | 代理 | 治理 | CASE | 现状 |
|------|------|------|------|------|
| `lw.consent.check` | Privacy Steward | C-01~C-05 | 002 | 复用 check_consent |
| `lw.consent.revoke` | Privacy Steward | C-03, C-04 | 003 | 新增 |
| `lw.policy.check` | Privacy Steward | M-01~M-03 | 011,013 | 复用 check_safety_signal |
| `lw.surprise.compose` | Surprise Alchemist | C-01, E-02 | 001,007,008 | 复用 compose_surprise |
| `lw.pulse.compose` | Pulse Composer | D-01 | 004,012 | 复用 compose_pulse_solo |
| `lw.pulse.duet` | Pulse Composer + Bond Guardian | B-01~B-03 | 005,006 | 复用 compose_pulse_duet |
| `lw.timing.decide` | Timing Curator | T-01~T-04 | 009 | 复用 decide_timing |
| `lw.impact.evaluate` | Ritual Host | E-01~E-05 | 008 | 复用 assess_emotion_impact |
| `lw.ritual.render` | Ritual Host | A-01 | 001,004 | 复用 render_ritual |
| `lw.share.revoke` | Bond Guardian | B-04 | 010 | 复用 revoke_share |
| `lw.feedback.capture` | Evolution Listener | D-02 | 014 | 新增（结构化枚举） |
| `lw.changeset.draft` | Evolution Listener | EV-01~EV-04 | 014 | 复用 draft_changeset |
| `lw.audit.append` | Privacy Steward | G0 | all | 新增 |
| `lw.keepsake.save` | Ritual Host | D-04 | 001,004,010 | 新增 |

P1 时空记忆匣：`lw.memory.weave` / `shuttle` / `capture` / `fuse` / `lw.palace.snapshot` 已启用。
P2 保留：`lw.bond.async_create` / `lw.twin.draft` / `lw.template.publish` → `FEATURE_RESERVED`

## 四、状态机（编排器实现）

主路径（顺序不变量：impact → timing → ritual）：
```
intent_created → consent_checking → signal_weaving|device_linking
  → composing → impact_checking → timing_deciding → ritual_rendering
  → delivered → [changeset_drafted] → closed
```

终态/错误：`consent_required` `consent_revoked` `bond_blocked` `device_paused`
`emotion_impact_failed` `slow_inspiration_deferred` `share_revoked`
`safety_hold` `failed_retryable` `failed_final` `cancelled` `human_takeover`

子状态机：PulseSession（linking→live⇄paused→completed|aborted）、
Surprise（queued→composing→…→delivered）、ShareGrant（draft→active→SHARE_REVOKED|expired）。

重试预算：`CONNECTOR_UNAVAILABLE` ×3、`DEVICE_DISCONNECTED` ×3 重连。

## 五、治理红线（代码强制，18 条）

1. 无有效 consent → 不收集/生成/通知/分享（`CONSENT_REQUIRED`）
2. `purpose` 必须 `create_for_user`，否则 `POLICY_DENIED`
3. 撤回后非审计处理 = 0
4. duet 需双方 `device.pulse`+`share.partner`+双向 needs，否则 `BOND_ASYMMETRIC`
5. 任一方撤回分享 → 立即 `SHARE_REVOKED` 全表面
6. MVP 阻断 G4 公开分享/原始信号导出
7. 原始连续 pulse 仅会话内，默认不持久化不入遥测
8. 未成年人：无 duet、无外部分享；年龄未知走保守路径
9. 高危：停止生成 → `SAFETY_HUMAN_REVIEW`，无娱乐/诊断
10. `EmotionImpact`：模型辅助不可单独 deliver；用户 `uncomfortable` 胜出
11. surprise 缺 `uniqueness_refs` → `VALIDATION_ERROR`
12. impact 门禁失败 → 不交付
13. `SLOW_INSPIRATION_DEFERRED` → 不通知
14. ChangeSet `auto_apply=false` 恒成立；扩 scope/purpose → `POLICY_DENIED`
15. `RitualEnvelope` 必须含 `timing_decision_ref` + `emotion_impact_ref`，否则阻断
16. 审计永不包含：原始 pulse、自由文本反馈、对方拒绝理由、精确年龄、诊断推断
17. duet 断连不可静默降级为 solo
18. 频率/静默时段护栏不可被实验绕过

## 六、指标（M-01~M-18 + MRCR）

北极星 **MRCR** = meaningful_rituals / eligible_revealed_rituals。
护栏否决（即使 MRCR↑也回滚）：M-08>0、未成年人/外分享违规、duet 缺双方 consent、
模型覆盖负反馈、侵入性阈值突破、商业侵蚀免费主权。

遥测事件（净化）：consent.viewed/granted/revoked、signal.selected、timing.decided、
ritual.ready/revealed、trace.viewed、ritual.feedback_submitted、keepsake.saved、
duet.invite_resolved、device.disconnected、share.revoked、impact.evaluated、changeset.drafted。

遥测禁含：原始 pulse、哼唱/照片内容、自由文本反馈体、对方拒绝理由、健康推断。

## 七、实施阶段与完成度

| 阶段 | 内容 | 状态 |
|------|------|------|
| P0 工程定义 | 治理 MVP + 14 CASE + RitualEnvelope + JSON 持久化 | ✅ 已存在 |
| F1 类型化领域 | `domain.py` 15 实体 + 不变量 | ⬜ 本计划 |
| F2 schema 校验 | `schemas.py` jsonschema | ⬜ 本计划 |
| F3 能力契约 | `capabilities.py` lw.* 注册表 + 信封 + 幂等 + 审计 | ⬜ 本计划 |
| F4 状态机编排 | `orchestrator.py` 顺序不变量 | ⬜ 本计划 |
| F5 结构化存储 | `store.py` 仓储模式 | ⬜ 本计划 |
| F6 指标层 | `metrics.py` MRCR + M-01~M-18 | ⬜ 本计划 |
| F7 真实输入边界 | `cli.py` 非 CASE 夹具 | ⬜ 本计划 |
| F8 测试 | 新层测试 + 14 CASE 回归 | ⬜ 本计划 |
| P1 体验深化 | 时机历史 DB、策展工作流、账号 | ⬜ 后续 |
| P2 连接器 | 真实穿戴/多模态/keepsake 存储 | ⬜ 后续 |
| P3 扩展能力 | memory.weave / bond.visualize / twin.draft | ⬜ 后续 |

## 八、验收

```bash
cd projects/lifewake
python3 -m pytest -q                          # 含新层 + 14 CASE 回归
python3 -m lifewake.cli --intent '{"...":...}' # 真实输入边界
python3 scripts/evaluate_lifewake_mvp.py       # 14 CASE 仍通过
```

## 九、非目标（v0.2 正式项目范围外）

- 真实设备 SDK / 真实多模态 API（规约允许 mock）
- 正式移动端 UI（prototype 已是高保真前端）
- LLM 调用（workflow LLM 步保持模板填充，规约 v0.2 允许）
- 自动应用 ChangeSet（恒 `auto_apply=false`）
