# LifeWake 治理矩阵

> 隐私即灵魂领土。本文把同意、用途限制、双向关系、共享与未成年人规则落为可执行策略。

---

## 1. 风险等级

| 等级 | 含义 | 示例动作 | 默认控制 |
|------|------|----------|----------|
| **G0** | 只读 / 审计 | 查询同意状态、追加审计 | scope + audit |
| **G1** | 本地草稿仪式 | 预览惊喜文案、未推送构图 | 不出域 |
| **G2** | 授权内创作交付 | 惊喜推送、单人心跳作曲 | 自动执行 + 可撤回推送 |
| **G3** | 关系共享 | 双人共鸣共享、纪念物互见 | 双方同意 + Bond 校验 |
| **G4** | 外发/高敏 | 公开分享、导出原始信号、代发消息 | 人工确认；MVP 默认拒绝原始导出 |

MVP 不实现健康诊断、广告画像、监控类能力；疑似用途一律 `POLICY_DENIED`。

---

## 2. 角色与权限

| 角色 | 数据 scope | 动作 scope |
|------|------------|------------|
| `person_self` | 本人信号、作品、同意 | `lw.consent.check`、`lw.surprise.compose`、`lw.pulse.compose`、`lw.ritual.render` |
| `partner` | Bond 内共享作品 | 仅 `share.partner` 明示同意后的共创资产 |
| `privacy_steward` | 同意与审计元数据 | `lw.consent.check`、`lw.audit.append`、阻断违规用途 |
| `bond_guardian` | Bond.needs / 共享状态 | 校验双向需求、撤销共享 |
| `surprise_alchemist` | 授权 SignalBundle | `lw.surprise.compose` |
| `pulse_composer` | 授权 PulseStream 摘要 | `lw.pulse.compose`、`lw.pulse.duet` |

---

## 3. 同意与用途规则

| 规则 ID | 条件 | 结果 |
|---------|------|------|
| C-01 | `purpose != create_for_user` | `POLICY_DENIED` |
| C-02 | 缺少 required scope 或 status≠granted | `CONSENT_REQUIRED` |
| C-03 | 运行中检测到 revoked | `CONSENT_REVOKED`，中止并清理队列 |
| C-04 | 用户撤回后 | 停止新创作；已生成未推送删除；审计保留 |
| C-05 | 隐性信号仅 `low` 灵敏度 | 中高敏信号禁止入 Surprise 路径 |

---

## 4. 关系与共享规则

| 规则 ID | 条件 | 结果 |
|---------|------|------|
| B-01 | duet 缺少任一方 `device.pulse` | `CONSENT_REQUIRED` |
| B-02 | duet 缺少 `share.partner` | `CONSENT_REQUIRED` |
| B-03 | 仅满足单方情感需求 | `BOND_ASYMMETRIC` |
| B-04 | 任一方撤销共享 | `SHARE_REVOKED`；所有共享 surface 立即失效，各方私有材料按各自 consent 处理 |
| B-05 | 公开外发纪念物 | G4，MVP 返回 `POLICY_DENIED`（需人工通道，v0.1 不开放） |

---

## 5. 时机与慢灵感

| 规则 ID | 条件 | 结果 |
|---|---|---|
| T-01 | quiet hours、频率已满或用户设为安静 | `SLOW_INSPIRATION_DEFERRED`，不得通知 |
| T-02 | 内容尚未通过 impact gate | defer 或 rework，不得用“先交付再观察” |
| T-03 | 到达重评时间 | 只重新计算 `TimingDecision`，不保证交付 |
| T-04 | 用户取消 deferred item | `CANCELLED` 并清理未交付资产 |

---

## 6. 情感冲击可解释门禁

**情感冲击测试不是模型真理，而是用户反馈 + 策展 rubric 的可解释门禁。**

| 规则 ID | 条件 | 结果 |
|---------|------|------|
| E-01 | 用户反馈为 `not_meaningful/uncomfortable` | `EMOTION_IMPACT_FAILED`；重炼、策展或删除 |
| E-02 | 惊喜缺少 `uniqueness_refs` | `VALIDATION_ERROR` |
| E-03 | rubric 的 source_fit/safety 不通过 | `rework/reject`，不得交付 |
| E-04 | 只有模型辅助信号 | 不允许 `deliver`；进入 rubric/内测评审 |
| E-05 | 用户反馈与模型/rubric 冲突 | 用户反馈优先；`superseded_by_feedback=true` |

模型可输出新颖度、来源覆盖和潜在风险，但不得输出“用户必然感动”等真理性结论。

---

## 7. 未成年人与敏感场景

| 规则 ID | 条件 | 结果 |
|---------|------|------|
| M-01 | `age_gate == minor` | 禁用 duet 与外部共享；只允许受限本地体验 |
| M-02 | 信号暗示自伤等高危 | 停止娱乐化内容；`SAFETY_HUMAN_REVIEW`，提供非诊断支持选择 |
| M-03 | age unknown 且请求关系/外发 | 采用更保守 minor 路径 |

---

## 8. 数据、保留与供应商

| 规则 ID | 条件 | 结果 |
|---|---|---|
| D-01 | 原始连续 pulse | 仅会话内处理，默认不持久化、不入遥测 |
| D-02 | 自由文本反馈 | 加密内容引用；指标只用结构化枚举 |
| D-03 | 第三方生成 | 只传最小输入；要求保留期限、删除与再训练禁用承诺 |
| D-04 | 导出/删除请求 | 不设付费墙；提供状态 receipt |
| D-05 | 产品分析 | 可退出非必要分析；不得重建原始信号或伴侣拒绝原因 |

---

## 9. 演化治理

| 规则 ID | 条件 | 结果 |
|---|---|---|
| EV-01 | feedback→ChangeSet | 必须含 feedback、EmotionImpact、rubric、影响范围、回滚点 |
| EV-02 | `auto_apply=true` | `POLICY_DENIED` |
| EV-03 | ChangeSet 扩大 purpose/scope | `POLICY_DENIED` |
| EV-04 | 相关主权/安全护栏回归失败 | 禁止发布或自动回滚 |

---

## 10. 审计要求

每次 capability 调用必须记录：

- intent_ref、actor、on_behalf_of
- consent_id / missing scopes
- capability 名与结果摘要（不含原始 HR 连续值）
- `TimingDecision`、`EmotionImpact` 的证据类别与决策（不含私密正文）
- 错误码与下一步建议
- share revoke 的请求、生效时间与 surface

审计不得包含原始连续 pulse、自由文本反馈、伴侣拒绝理由、精确年龄或诊断推断。

任何可交付内容都必须封装为引用有效 `EmotionImpact` 与 `TimingDecision` 的 `RitualEnvelope`；缺任一引用即阻断。

## 11. 治理否决权

以下任一事件发生即停止相关能力并进入 L3/L4 回退：

1. 撤回后仍有非审计处理。
2. duet 缺任一方 consent 仍生成/共享。
3. minor 可外发或进入 duet。
4. 模型分覆盖用户 `uncomfortable` 反馈。
5. ChangeSet 自动应用或扩大 `create_for_user`。
