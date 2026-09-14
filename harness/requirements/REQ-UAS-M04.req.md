# Requirement: REQ-UAS-M04 — M4 Law Pack

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: C（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：知识管理员、合规
- 遇到什么问题：应当条文写在 prompt 或 wiki，模型可跳过，发版才能改规则。
- 为什么重要：知识即配置；Hooks 100% 执行。

## 验证标准
- 成功：YAML 条文经 ChangeSet 进 compiled；未审批不生效。
- 失败/放弃：条文只进 system prompt；auto_apply。

## Given / When / Then
- Given draft ChangeSet 改一条门禁
- When 未确认即 pack.open
- Then 仍用旧 compiled laws

## 场景穷举
- 正常：S-01 YAML 校验 · S-02 编译进 WM.laws · S-03 版本对比
- 异常：E-01 冲突未声明拒绝编译 · E-02 绕过 ChangeSet 写库拒绝
- 边界：B-01 空 pack 仅默认 G 层

## Acceptance Criteria
- [ ] configs/law_packs/*.yml 为权威
- [ ] I-09 未审批不进 compiled

## 依赖与约束
- 前置：M12 · M3 · M6 Policy
- 技术：见模块设计 M4；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M4-1 schema+样例 · US-M4-2 编译器 · US-M4-3 Pack Studio 子页
- TDD 先写：test_unapproved_changeset_not_in_compiled · test_hooks_not_skippable_by_model
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- configs/law_packs/ · services/hub-api/law/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M4 节）

## 映射
UAS-AIOS M4 · 层 K-L0 / 德
