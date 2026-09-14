# Requirement: REQ-UAS-M06 — M6 Capability Hub 控制面

## Status: completed

## 需求层级: 能力

## 优先级: P0

## 阶段: A（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：全部上游唯一门禁
- 遇到什么问题：多套注册中心/聊天壳各自连系统，剖面与审批被绕过。
- 为什么重要：控制面必须自有；别人的 OS 不当内核。

## 验证标准
- 成功：判定序不可颠倒；profile 入口强制；explain 人话 100%。
- 失败/放弃：Dify/Copilot Studio 当 Hub；第三套循环。

## Given / When / Then
- Given profile=scene 的令牌
- When invoke_cs 写操作
- Then 403 PROFILE_FORBIDS_SIDE_EFFECT 且 explain 给出签发下一步

## 场景穷举
- 正常：S-01 信封校验 · S-02 四剖面路由 · S-03 explain 试运行
- 异常：E-01 伪造 profile 作废 · E-02 缺 tenant 拒绝 · E-03 Thread 改剖面 409
- 边界：B-01 幂等键重放 · B-02 未知错误码仍有兜底人话

## Acceptance Criteria
- [x] PolicyChain 单测覆盖序 0-8
- [x] A2/A12
- [x] I-01 前台只走 hub.*

## 依赖与约束
- 前置：M7 · M8 · M11
- 技术：见模块设计 M6；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M6-1 FastAPI 骨架 · US-M6-2 PolicyChain · US-M6-3 explain · US-M6-4 Hub Console 试运行
- TDD 先写：test_profile_injected_not_from_body · test_policy_order · test_explain_covers_catalog
- 开发规划：US-M6-1 FastAPI 骨架已落地；US-M6-4 Hub Console 不在阶段 A
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/hub-api/ · projects/aios-workstudio/T1-CapabilityHub详细设计.md
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M6 节）

## 映射
UAS-AIOS M6 · 层 G/A/R
