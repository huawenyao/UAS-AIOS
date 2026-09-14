# Requirement: REQ-UAS-M12 — M12 Evolution Engine

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: C（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：知识管理员
- 遇到什么问题：会话内模型改生产法则。
- 为什么重要：受控的将来；auto_apply=false。

## 验证标准
- 成功：驳回/超时→草案→人确认→下次 compiled。
- 失败/放弃：CI 机器人自动回写 Law Pack。

## Given / When / Then
- Given L2 审批超时
- When Workflow 发 DraftChangeSet
- Then status=draft，生产 laws 未变

## 场景穷举
- 正常：S-01 信号入队 · S-02 diff 评审 · S-03 回滚指针
- 异常：E-01 无回归 CASE 不能确认 · E-02 确认后编译失败可回滚
- 边界：B-01 空信号不产草案

## Acceptance Criteria
- [ ] ChangeSet schema
- [ ] I-09
- [ ] 复用 evolve_apply 语义

## 依赖与约束
- 前置：M4 · M11 · evolve_apply.py
- 技术：见模块设计 M12；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M12-1 草案表 · US-M12-2 治理台
- TDD 先写：test_auto_apply_always_false · test_unapproved_not_compiled
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- scripts/evolve_apply.py · services/hub-api/evolution/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M12 节）

## 映射
UAS-AIOS M12 · 层 E
