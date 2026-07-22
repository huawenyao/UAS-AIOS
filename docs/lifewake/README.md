# 生命回响（LifeWake）MVP 开发规约包

> 本目录将「生命回响」产品哲学宪章收敛为可开发工程规约。目标是让 [`projects/lifewake/`](../../projects/lifewake/) 以单个 UAS subapp 原型进入开发与验收，而不是提前拆成多端 App / 微服务平台。

---

## 1. v0.1 开发边界

| 项 | 决策 |
|----|------|
| 工程形态 | 单个 `projects/lifewake/` subapp |
| 运行方式 | 复用 `scripts/run_uas_runtime_service.py` 与 autonomous_agent runtime |
| 设备与生成模型 | 使用 mock connector；不接真实穿戴设备、不调用真实多模态生成 API |
| 数据与隐私 | 所有隐性数据仅用于「为用户创作」；默认拒绝画像用于广告/评分/定义用户 |
| UI | 暂不建设正式 UI；以 JSON 输入、reports 输出、audit/state 文件验证闭环 |
| 演化 | 生成 ChangeSet 草案，不自动写回生产配置 |
| 扩展功能 | 「记忆时光机 / 关系纽带 / 数字孪生对话」仅预留能力接口，不进入 v0.1 执行路径 |

---

## 2. MVP 闭环

```text
consent_granted / pulse_device_linked / boredom_signal
  → Intent Hub: 归一化情感意图（惊喜 / 心跳共鸣）
  → Consent Gate: 校验授权范围与可撤回状态
  → LifeWake Agents:
      · Signal Weaver（隐性信号编织）
      · Surprise Alchemist（惊喜炼金）
      · Pulse Composer（心跳作曲）
      · Bond Guardian（双向关系守卫）
      · Privacy Steward（隐私领土守卫）
  → lw.surprise.compose 或 lw.pulse.compose / lw.pulse.duet
  → Ritual Render: 灵感来源解析 + 情感冲击校验
  → audit_report + wow_score + ChangeSet draft（可选）
```

---

## 3. 规约文件

| 文件 | 解决的问题 |
|------|------------|
| [PRODUCT_CHARTER.md](./PRODUCT_CHARTER.md) | 产品哲学宪章与设计原则工程映射 |
| [FUNCTIONAL_DESIGN.md](./FUNCTIONAL_DESIGN.md) | MVP 功能设计、用户流程、扩展接口 |
| [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) | Person、Consent、Signal、Surprise、PulseSession、Bond、Ritual、Audit 等实体 |
| [CAPABILITY_CONTRACTS.md](./CAPABILITY_CONTRACTS.md) | `lw.*` 能力输入/输出/错误/幂等/回滚 |
| [GOVERNANCE_MATRIX.md](./GOVERNANCE_MATRIX.md) | 隐私、同意、双向关系、未成年人、外发共享治理 |
| [WORKFLOW_STATE_MACHINE.md](./WORKFLOW_STATE_MACHINE.md) | 同意门禁、惊喜推送、心跳会话、失败与撤回路径 |
| [WORLD_MODEL_CONFIG.md](./WORLD_MODEL_CONFIG.md) | 情感世界模型五维与镜像/透镜/熔炉 |
| [FEEDBACK_CHANGESET.md](./FEEDBACK_CHANGESET.md) | 情感冲击反馈 → ChangeSet 草案 |
| [MVP_ACCEPTANCE_CASES.md](./MVP_ACCEPTANCE_CASES.md) | CASE-001～008 端到端验收 |

---

## 4. 与 UAS 八元组映射

| 层 | LifeWake 落点 |
|----|---------------|
| **I** | 惊喜探索、心跳共鸣、关系共创意图 |
| **K** | 哲学宪章、同意策略、风格偏好、仪式模板 |
| **R** | autonomous_agent runtime + mock 生物/生成 connector |
| **A** | Signal Weaver / Surprise Alchemist / Pulse Composer / Bond Guardian / Privacy Steward |
| **S** | mock 穿戴设备、mock 多模态生成、本地 audit store |
| **G** | 同意撤回、隐私领土、双向关系门禁、人工审核共享 |
| **E** | wow_score / 共鸣反馈 → ChangeSet |
| **Π** | `lw.*` 能力契约与仪式输出协议 |

---

## 5. 开发完成定义

v0.1 配置原型完成时必须满足：

1. `lifewake` 能被 UAS Runtime Service 发现和 validate。
2. 至少 8 条验收用例可通过 `scripts/evaluate_lifewake_mvp.py` 执行。
3. 每次运行都生成 intent、consent_check、capability_call、ritual、audit、report。
4. 无有效同意时不得生成惊喜或心跳作品。
5. 双人模式必须同时满足双方同意与双向情感需求检查。
6. 失败用例必须产出明确错误码、审计记录和下一步建议。
7. 至少一条反馈能生成 ChangeSet 草案（`auto_apply: false`）。
