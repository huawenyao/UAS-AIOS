# Requirement: REQ-UAS-M09 — M9 Skill 协议状态机

## Status: pending

## 需求层级: 能力

## 优先级: P1

## 阶段: C（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：探索研究员、构建者
- 遇到什么问题：看见 Skill 就能执行，Explore 污染生产工具。
- 为什么重要：发现≠执行。

## 验证标准
- 成功：explore 最高 cited；runtime 才 execute。
- 失败/放弃：人设商城；CLAUDE.md 当 Skill。

## Given / When / Then
- Given Skill 仅 cited 未 installed
- When runtime execute
- Then SKILL_NOT_EXECUTABLE_IN_PROFILE

## 场景穷举
- 正常：S-01 发现预览 · S-02 cite 进 ThemePack · S-03 install/enable
- 异常：E-01 explore 执行写工具 403 · E-02 头 YAML 非法
- 边界：B-01 未发现列表为空

## Acceptance Criteria
- [ ] A9
- [ ] 状态枚举持久化

## 依赖与约束
- 前置：M6 · M10 ThemePack
- 技术：见模块设计 M9；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M9-1 状态机 · US-M9-2 货架 UI
- TDD 先写：test_explore_cannot_execute · test_cite_sets_installed_false
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/hub-api/skill/ · .claude/skills/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M9 节）

## 映射
UAS-AIOS M9 · 层 A
