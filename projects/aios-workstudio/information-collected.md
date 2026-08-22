# 信息搜集 · WorkStudio / Capability Hub

> Phase 1 · 2026-08-22 · 置信度标注：高 = 仓库已落盘；中 = 公开产品对照；低 = 待验证假设

---

## 产品契约（高）

- T0：前台是工作台，后台是能力中枢；产品是法则编译器。`T0产品定义.md`
- 禁止聊天冒充工作台；首屏五维；先解释再动作；双轨不混权。宪章 6.3 / T0 §8
- 北极星：质量调整后的岗位闭环成功率，不是 Token 或专家数

## 已有工程基线（高）

| 工件 | 用途 | 路径 |
|------|------|------|
| ADR-EDH-001 | 双轨边界、升级须带证据 | `harness/knowledge/constraints/adr-edh-001-dual-track-boundary.md` |
| ADR-EDH-002 | 先 cs.* 再 Agent；禁裸 API | `harness/knowledge/constraints/adr-edh-002-capability-before-agent.md` |
| RBAC/ABAC | tenant → role → operation → gate → scope | `harness/knowledge/technical/enterprise-rbac-abac-spec.md` |
| cs.* 目录 | 语义能力，写操作走平台 | `harness/knowledge/technical/capability-service-catalog-baseline.md` |
| Subapp 生产协议 | 7 阶段生产 UAS 应用 | `.claude/skills/subapp_producer_protocol.md` |
| 方案输出契约 | intent/knowledge/agent/governance/evolution | `.claude/skills/subapp_output_contract.md` |
| reqharness | 七阶段交付 + invariant 门禁 | `harness/reqharness.yaml` · reqharness skill |
| 价值闭环协议 | 7 步 ↔ workflow | `.claude/skills/value_loop_protocol.md` |
| World Model Studio | 五维 + 7 步原型 | `examples/world-model-studio/` · REQ-EDH-PP-001 completed |
| domain_builder | 议题 → 领域分析 → subapp | `.claude/skills/domain_builder.md` |
| loop-thinking-enhanced | 探索研究的方法论运行时 | `.claude/skills/loop-thinking-enhanced/` |

## 行业对照（中）

- WorkBuddy 工作台按职能切：日常办公 / 代码 / 设计。专家 + Skill 是执行加速器。
- 千问办公：通用 / 设计 / 幻灯片 / 写作。研究链路更重。
- Codex：循环嵌入工作对象；应用拥有界面与审批。
- 本产品若再按「文档/PPT/代码」切工作台，会退回面积战。

## 关键缺口（高）

- 仓库有 Kernel 契约与 Studio 原型，**没有** WorkStudio 三场景产品壳。
- 有 subapp 生产协议，**没有** Builder 场景的人机界面与门禁 UX。
- 有 RBAC/审计规格，**没有** Runtime 场景把它们变成用户可感知的治理台。
- Explore 若做成「已安装 Skill 目录」，直接违反用户给定的场景 1。

## 假设（待用户否证）

- A1：Runtime 首个 App 仍是招聘短名单（T0 默认）。三场景设计不绑定该行业。
- A2：Explore 允许受控外网检索；企业可关，但不能把「无外网」做成产品默认无能。
- A3：Builder 产出物是 UAS subapp，不是任意低代码页面。
