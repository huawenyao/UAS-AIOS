# LifeWake 功能规格

> 本文只定义模块、优先级、用户故事、前后条件、异常与验收，不重复产品定位。体验语义见 [PRODUCT_EXPERIENCE_DESIGN](./PRODUCT_EXPERIENCE_DESIGN.md)，能力 schema 见 [CAPABILITY_CONTRACTS](./CAPABILITY_CONTRACTS.md)。

## 1. 优先级与模块

| 模块 | 功能 ID | P0 | P1 | P2 |
|---|---|---|---|---|
| Privacy | F-CONSENT | scope/purpose/期限授权、暂停、撤回 | 分设备/供应商授权 | 个人数据仓/自管密钥 |
| Core | F-SIGNAL | 手动选择低敏感材料 | 多源材料组合 | 本地情境感知 |
| Core | F-TIMING | deliver/defer/cancel | 节奏偏好与安静期 | 本地时机推断 |
| Core | F-SURPRISE | song/artwork/task mock | 多模态编排 | 第三方受审模板 |
| Core | F-PULSE-SOLO | 会话级 pulse 作曲 | 真实设备适配 | 环境设备联动 |
| Bond | F-DUET | 双方 consent/needs、共同作品 | 异步共创 | 多方关系协议 |
| Core | F-RITUAL | `RitualEnvelope` 渲染、trace、反馈 | 改编、章节化 | 空间仪式 |
| Memory | F-KEEP | 保存、删除、导出 | 记忆时光机 | 开放迁移协议 |
| Bond/Memory | F-SHARE | 双方共享与任一方撤回 | 可过期外链 | 多方权利管理 |
| Studio | F-IMPACT | 用户反馈 + rubric 门禁 | 分层 rubric | 创作者质量治理 |
| Studio | F-EVOLVE | ChangeSet 草案/审批/回滚 | 实验回放 | 模板生态演化 |
| Privacy | F-SAFETY | 未成年人/高危/用途门禁 | 区域策略 | 独立透明度验证 |

## 2. 通用功能规则

### 2.1 前置不变量

- 所有创作先通过 `ConsentGrant`、purpose、age/safety policy。
- capability 只能读取信封声明的最小 scope。
- 所有交付先生成 `TimingDecision` 和 `EmotionImpact`。
- `EmotionImpact` 不是模型真理；模型辅助信号不能单独批准交付。
- 所有路径有 `trace_id`、幂等键、审计与补偿动作。

### 2.2 统一后置结果

功能必须返回以下之一：

1. 成功 `RitualEnvelope`；
2. 延期 `SLOW_INSPIRATION_DEFERRED` + `reconsider_after`；
3. 主权终止 `CONSENT_REVOKED` / `SHARE_REVOKED`；
4. 安全失败 + 用户可理解下一步；
5. 可重试技术失败 + 不重复处理证明。

## 3. F-CONSENT · 同意与撤回

**用户故事**：作为用户，我希望按数据、用途、受益者和期限授权，并能随时撤回，以便惊喜不以失控为代价。

| 项 | 规格 |
|---|---|
| 前置 | 已识别本人；展示必要/可选 scope 与处理者 |
| 触发 | grant、pause、resume、revoke |
| 输入 | person、scopes、purpose、beneficiaries、expiry |
| 处理 | 独立存证；禁止默认全选；purpose 仅 `create_for_user` |
| 后置 | 返回 consent receipt；revoke 取消队列和未交付资产 |
| 异常 | `CONSENT_REQUIRED`、`CONSENT_REVOKED`、`POLICY_DENIED` |
| 验收 | 撤回后非审计新处理为 0；授权与撤回入口同级 |
| 追溯 | 宪章“隐私领土”；F1/F6；CASE-002/003；M-07～M-09 |

## 4. F-SIGNAL · 授权材料选择与编织

**用户故事**：作为用户，我希望知道并选择哪些材料参与创作，以便作品独特但不过度窥探。

| 项 | 规格 |
|---|---|
| 前置 | 有效 `signals.low_sensitivity` consent |
| 输入 | 手动选择的哼唱动机、风格标签、粗粒度情境 |
| 处理 | 去除无关字段；生成 `SignalBundle` 与来源引用 |
| 后置 | 至少 1 个 `uniqueness_ref`；可排除任一来源 |
| 异常 | scope 不足、材料不足、敏感等级超限 |
| 验收 | 原始材料不进入遥测；trace 与 consent 可追溯 |
| 追溯 | 宪章“生命独奏”；F1；CASE-001；M-03/M-04 |

## 5. F-TIMING · 慢灵感时机决策

**用户故事**：作为用户，我希望作品在合适时刻出现，也允许暂时不出现，以免惊喜变成打扰。

| 项 | 规格 |
|---|---|
| 前置 | 候选作品、用户节奏偏好、频率与安静期策略 |
| 输入 | requested window、last delivery、quality readiness、quiet hours |
| 处理 | 输出 `DELIVER_NOW`、`SLOW_INSPIRATION_DEFERRED` 或 `CANCELLED` |
| 后置 | defer 带 reason、`reconsider_after`、取消入口 |
| 异常 | 缺少时区/策略时默认 defer，不猜测 |
| 验收 | defer 不通知轰炸；到点只重评，不保证交付 |
| 追溯 | 宪章“慢灵感”；F4/F5；CASE-009；M-12/M-13 |

## 6. F-SURPRISE · 单人惊喜创作

**用户故事**：作为用户，我希望收到由我选择的材料转化而来的独特作品，并看懂它为什么属于我。

| 项 | 规格 |
|---|---|
| 前置 | consent 通过；`SignalBundle` 非空；age/safety 通过 |
| 输入 | bundle、允许模态、风格、timing window |
| 处理 | 生成 song/artwork/task；保留来源变化说明 |
| 后置 | 候选 artifact + trace，尚不得直接推送 |
| 异常 | `CONNECTOR_UNAVAILABLE`、`VALIDATION_ERROR`、`CONSENT_REVOKED` |
| 验收 | 非模板唯一引用≥1；经 timing 与 impact 后才交付 |
| 追溯 | 宪章“创造共谋者”；F1/F3；CASE-001/007/008 |

## 7. F-PULSE-SOLO · 单人生命韵律

**用户故事**：作为用户，我希望把本次心跳转为音乐/视觉，而不被诊断或长期监控。

| 项 | 规格 |
|---|---|
| 前置 | `device.pulse` 会话 consent；设备已连接 |
| 输入 | 会话 pulse 摘要、style、mix、无障碍偏好 |
| 处理 | 映射 tempo/dynamics；不生成健康标签 |
| 后置 | composition + waveform；原始连续流按策略销毁 |
| 异常 | `DEVICE_NOT_LINKED`、`DEVICE_DISCONNECTED`、connector failure |
| 验收 | 可重连/无设备降级/结束；所有文案非诊断 |
| 追溯 | 宪章“生命值得倾听”；F7；CASE-004/012；M-14 |

## 8. F-DUET · 双人共同仪式

**用户故事**：作为关系双方，我们希望在各自愿意的前提下共同创作，并保持独立退出权。

| 项 | 规格 |
|---|---|
| 前置 | active Bond；双方 `device.pulse` + `share.partner`；双方 needs 可满足 |
| 输入 | two participants、two grants、devices、style |
| 处理 | Bond Guardian 先校验；生成共同作品，不做心率/关系比较 |
| 后置 | 共同 `RitualEnvelope` + 两份权利 receipt |
| 异常 | `BOND_ASYMMETRIC`、`CONSENT_REQUIRED`、`DEVICE_DISCONNECTED` |
| 验收 | 缺任一方 consent 零生成；拒绝理由不向另一方泄露 |
| 追溯 | 宪章“真正连接”；F2；CASE-005/006/012；M-10 |

## 9. F-RITUAL · 仪式交付

**用户故事**：作为体验者，我希望作品、来源、时机与主权动作在一个清晰仪式中呈现。

| 项 | 规格 |
|---|---|
| 前置 | artifact、`TimingDecision=DELIVER_NOW`、impact gate 可交付 |
| 输入 | content blocks、trace、consent refs、actions、a11y |
| 处理 | 封装 `RitualEnvelope`，映射为 `RitualView` |
| 后置 | ready→revealed→saved/dismissed/deleted |
| 异常 | trace 缺失、a11y 变体缺失、consent 过期 |
| 验收 | 不自动播放；来源、反馈、删除和撤回可达 |
| 追溯 | 宪章“自我确认仪式”；F6；CASE-001/004；MRCR |

## 10. F-IMPACT · 情感冲击可解释门禁

**用户故事**：作为用户和策展人，我希望低质量或可能冒犯的作品在交付前被拦截，同时用户反馈始终高于模型判断。

| 项 | 规格 |
|---|---|
| 前置 | 候选 artifact + trace + rubric 版本 |
| 输入 | 用户/同类内测反馈、策展 rubric、模型辅助信号 |
| 处理 | 分别保存证据；输出 `deliver/rework/curate/defer` |
| 后置 | 生成 `EmotionImpact`；低冲击不进入 ready |
| 异常 | 只有模型信号、rubric 缺失、评审冲突 |
| 验收 | 模型不能单独 `deliver`；负反馈可推翻历史高分 |
| 追溯 | 宪章“情感重量”；F3；CASE-008；M-05/M-06 |

## 11. F-KEEP · 纪念物保留与迁移

**用户故事**：作为用户，我希望保存、理解、导出或删除纪念物，而不被平台锁定。

| 项 | 规格 |
|---|---|
| 前置 | 已揭晓 Ritual；所有权明确 |
| 输入 | artifact、trace、retention、ownership |
| 处理 | 加密保存；生成开放导出清单 |
| 后置 | `Keepsake` 可重访、导出、删除 |
| 异常 | 共同权利冲突、存储失败、保留策略不合法 |
| 验收 | 删除/导出不付费；共同资产按 ShareGrant 执行 |
| 追溯 | 宪章“铭记/主权”；F6；CASE-010；M-15 |

## 12. F-SHARE · 共享与撤回

**用户故事**：作为共同作品权利人，我希望共享需要双方许可，任一方撤回后所有共享面立即失效。

| 项 | 规格 |
|---|---|
| 前置 | 共同 Keepsake；所有权人列表完整 |
| 输入 | per-person grants、surface、expiry |
| 处理 | 创建 `ShareGrant`；每次访问校验状态 |
| 后置 | revoke 后状态 `SHARE_REVOKED`，外链和对方访问失效 |
| 异常 | grant 缺失、过期、公开分享 G4 |
| 验收 | 撤回幂等；不披露撤回方原因；审计保留最小元数据 |
| 追溯 | 宪章“关系编织”；F2/F6；CASE-010；M-09/M-11 |

## 13. F-EVOLVE · 反馈到 ChangeSet

**用户故事**：作为产品/策展团队，我希望从真实反馈提出可审查改进，而不是自动画像或无控学习。

| 项 | 规格 |
|---|---|
| 前置 | 去标识 feedback、`EmotionImpact`、rubric 版本 |
| 输入 | evidence refs、target pack、hypothesis、guardrails |
| 处理 | 归因；生成 diff、影响范围、测试 CASE、回滚点 |
| 后置 | `ChangeSet.status=draft`，`auto_apply=false` |
| 异常 | 证据不足、扩大 purpose、缺回滚点 |
| 验收 | 串联 feedback→impact→ChangeSet；未审批不应用 |
| 追溯 | 宪章“随用户成长”；F3；CASE-014；M-17 |

## 14. F-SAFETY · 特殊主体与高危路径

**用户故事**：作为脆弱主体，我希望系统在风险不确定时保护我，而不是完成一件看似美的作品。

| 项 | 规格 |
|---|---|
| 前置 | age gate、用途分类、风险检测 |
| 处理 | minor 限制本地；高危停止娱乐化生成并提供人工/资源选择 |
| 后置 | `PolicyDecision` 与最小审计 |
| 异常 | 年龄未知时按更保守路径；资源不可用时仍可安全退出 |
| 验收 | minor 无 duet 外发；高危无诊断、无娱乐化内容 |
| 追溯 | 宪章“敬畏人”；F1/F7；CASE-011/013；安全违规数=0 |

## 15. P1/P2 预留边界

| 能力 | 优先级 | 当前行为 | 开放前置 |
|---|---|---|---|
| `lw.memory.weave` | P1 | `FEATURE_RESERVED` | F-KEEP、来源与删除回归通过 |
| `lw.bond.async_create` | P1 | `FEATURE_RESERVED` | 异步逐方同意协议通过 |
| `lw.template.publish` | P2 | `FEATURE_RESERVED` | Studio 审核、供应商与创作者治理完成 |
| `lw.twin.draft` | P2 | `FEATURE_RESERVED` | 反冒充、逐次审核、永不自动发送 |

## 16. 功能完成定义

每个功能完成必须同时具备：

- 前后条件、状态迁移、能力合约、错误和补偿；
- UI 触点与无障碍变体；
- consent/policy/audit；
- 至少一个成功 CASE 和一个失败/撤回 CASE；
- 指标采集与护栏；
- 在 [推导与验证矩阵](./DERIVATION_AND_VALIDATION_MATRIX.md) 中有完整追溯。
