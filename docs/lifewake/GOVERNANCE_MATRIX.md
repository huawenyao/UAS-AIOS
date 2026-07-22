# 生命回响 · 治理矩阵

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
| B-04 | 任一方撤销共享 | keepsake 外链失效；各方本地副本保留 |
| B-05 | 公开外发纪念物 | G4，MVP 返回 `POLICY_DENIED`（需人工通道，v0.1 不开放） |

---

## 5. 情感冲击门禁

| 规则 ID | 条件 | 结果 |
|---------|------|------|
| E-01 | `wow_score < 0.7` 且场景为首次核心体验 | `EMOTION_IMPACT_FAILED`，不得标记为可上线交付 |
| E-02 | 惊喜缺少 `uniqueness_refs` | `VALIDATION_ERROR` |
| E-03 | 24h 内对同一用户惊喜推送 > 阈值阈值 | 延后推送（慢灵感） |

默认频率阈值：`max_surprises_per_day = 2`。

---

## 6. 未成年人与敏感场景

| 规则 ID | 条件 | 结果 |
|---------|------|------|
| M-01 | `age_gate == minor` | 禁用 duet 共享与代发；惊喜仅本地 |
| M-02 | 信号暗示自伤等高危 | 不生成娱乐化内容；升级 `needs_human_review`（关怀路径占位） |

---

## 7. 审计要求

每次 capability 调用必须记录：

- intent_ref、actor、on_behalf_of
- consent_id / missing scopes
- capability 名与结果摘要（不含原始 HR 连续值）
- wow_score（如有）
- 错误码与下一步建议
