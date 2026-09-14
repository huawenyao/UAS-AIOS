# Requirement: REQ-UAS-M11 — M11 Audit 审计链

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：合规
- 遇到什么问题：指挥舱 KPI 被当成审计；日志可改。
- 为什么重要：可审计的过去。

## 验证标准
- 成功：每次 cs/升级追加哈希链；可按 correlation 导出。
- 失败/放弃：ES 当唯一审计；可 UPDATE 行。

## Given / When / Then
- Given 一次 invoke_cs 成功
- When 查 audit 链
- Then 含 actor/profile/operation/source_node_id，prev_hash 连续

## 场景穷举
- 正常：S-01 追加写 · S-02 检索 · S-03 合规包导出
- 异常：E-01 写失败补偿事件 · E-02 时钟回拨仍可排序
- 边界：B-01 空租户导出空包

## Acceptance Criteria
- [ ] 对齐 enterprise-audit-chain-spec
- [ ] A5 链完整

## 依赖与约束
- 前置：既有 audit schema · M6
- 技术：见模块设计 M11；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M11-1 分区表 · US-M11-2 审计台
- TDD 先写：test_audit_append_only · test_hash_chain · test_command_deck_not_audit
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- schemas/audit_record.schema.json · services/hub-api/audit/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M11 节）

## 映射
UAS-AIOS M11 · 层 G
