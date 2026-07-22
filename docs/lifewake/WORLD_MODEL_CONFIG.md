# LifeWake 世界模型配置

> 世界模型是法则编译器：把高维情感现实降维为可求解结构，再映射回可感知仪式。

---

## 1. 五维占位

| 维 | LifeWake 含义 | 配置要点 |
|----|---------------|----------|
| **空间** | 个人灵魂领土 / 关系共创空间 | `personal_space`、`bond_space`；数据不出用途边界 |
| **时间** | 慢灵感节奏、会话时刻、纪念日 | `TimingDecision`、安静期、频率阈值、重评时间 |
| **主体** | 自我、伴侣、隐形艺术家 Agent | Person + Agents；禁止「系统操控者」主体位 |
| **客体** | 信号、惊喜、心跳作品、仪式、共同纪念物 | Surprise / PulseSession / `RitualEnvelope` / Keepsake |
| **反馈** | 用户意义反馈、策展 rubric、撤回事件 | `EmotionImpact`、Consent/Share revoke、ChangeSet |

---

## 2. 镜像 · 透镜 · 熔炉

| 身份 | 落点 |
|------|------|
| 镜像 | audit + `RitualEnvelope` 反映来源和共同权利，不定义人格/关系质量 |
| 透镜 | Privacy Steward + Bond Guardian 揭示同意与双向需求本质 |
| 熔炉 | 惊喜/心跳作品重塑可分享的情感现实；ChangeSet 反哺策略 |

---

## 3. 推动 / 阻碍 / 连接

| 类型 | 示例 |
|------|------|
| 推动（Drive） | 无聊信号、思念、创作欲、纪念日 |
| 阻碍（Blocker） | 无同意、非双向、设备断连、时机不合、impact 门禁不足 |
| 连接（Connector） | `lw.surprise.compose`、`lw.pulse.duet`、`RitualEnvelope`、ShareGrant |

---

## 4. 与道德势术器映射

| 层次 | LifeWake |
|------|----------|
| 道 | 哲学宪章：敬畏生命独奏 |
| 德 | 隐私领土、不为定义用户、服务爱与自我发现 |
| 势 | 自我/伴侣/孤独-连接张力 |
| 术 | Agent 编织与时机策略 |
| 器 | mock 设备、生成器、仪式渲染 |

---

## 5. 宏观—中观—微观实例化

| 层 | 理念 | 现实 | 实体/动作 | 触点/承载 |
|---|---|---|---|---|
| 宏观 | 每个主体拥有解释与数据主权 | 设备、生成商、伴侣、平台存在权力不对称 | processor、rights owner、policy | Consent Center + supplier policy |
| 中观 | 生命材料经创作成为可撤回仪式 | 授权→创作→时机→仪式→反馈→演化 | Intent、Consent、Timing、Impact、ChangeSet | Core/Bond/Memory/Studio |
| 微观 | 每个决定可见、可操作、可补偿 | 用户点击授权/稍后/反馈/撤回；设备断连 | receipt、reason code、state、rollback | RitualView/Bond Space/Vault |

交叉验证见 [DERIVATION_AND_VALIDATION_MATRIX](./DERIVATION_AND_VALIDATION_MATRIX.md)。

---

## 6. 可证伪法则

| 法则 | 世界模型表达 | 反证 | 回退 |
|---|---|---|---|
| 解释增强被理解感 | trace→user meaning feedback | trace 引发被监控感 | 收紧来源或停止该信号 |
| 对称 consent 增强关系信任 | two grants→duet→two feedbacks | 强迫邀请/共享争议增加 | 限制提醒或停止 duet |
| 合适时机提升意义 | context→`TimingDecision`→feedback | defer 长期困惑/即时交付更佳 | 调整 timing policy |
| 用户反馈裁决情感现实 | feedback supersedes auxiliary score | 模型高分仍冒犯 | 回滚模型/rubric |

世界模型不能输出“爱/孤独/关系好坏”的事实判断；它只编译治理法则、当前上下文与可行动空间。

---

## 7. 运行时配置文件

工程落地见 [`projects/lifewake/configs/world_model.json`](../../projects/lifewake/configs/world_model.json)。

配置必须显式包含 `EmotionImpact`、`TimingDecision`、`RitualEnvelope`、`SLOW_INSPIRATION_DEFERRED`、`SHARE_REVOKED`，并保持本文语义。
