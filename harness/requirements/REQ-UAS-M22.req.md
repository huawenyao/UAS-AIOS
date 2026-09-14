# Requirement: REQ-UAS-M22 — M22 Utopia 知识工作台

## Status: pending

## 需求层级: 能力

## 优先级: P2

## 阶段: D（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：知识管理员 Spike
- 遇到什么问题：需要冲突审核台，但 v0.1 不能进写路径。
- 为什么重要：只读导出→ChangeSet。

## 验证标准
- 成功：默认 Compose 不含；无 CRM 按钮。
- 失败/放弃：当 L2 或 Dify 替代叙事。

## Given / When / Then
- Given 可选 profile 启动
- When 尝试 Action 打 CRM
- Then 无此按钮 / 403

## 场景穷举
- 正常：S-01 只读导出 · S-02 人审入库
- 异常：E-01 误配进生产写
- 边界：B-01 未部署则忽略

## Acceptance Criteria
- [ ] 默认不部署
- [ ] 导出不自动 apply

## 依赖与约束
- 前置：M12 · M4
- 技术：见模块设计 M22；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M22-1 评估备忘 · US-M22-2 导出适配器（可选）
- TDD 先写：test_default_compose_without_utopia
- 估算：3 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- docs/strategic/design/ （Spike 评估）
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M22 节）

## 映射
UAS-AIOS M22 · 层 K 工程
