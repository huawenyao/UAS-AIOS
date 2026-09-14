# Requirement: REQ-UAS-M17 — M17 Lethe 个人记忆

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: C（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：SelfPaw 用户、合规
- 遇到什么问题：个人备忘与经营承诺共库，无法遗忘举证。
- 为什么重要：双轨物理隔离 + GDPR 回执。

## 验证标准
- 成功：仅 selfpaw+self；forget 回执进经营审计；无 FK。
- 失败/放弃：Mem0/聊天历史；同 schema。

## Given / When / Then
- Given pipaw 令牌
- When memory.self.search
- Then 403 MEMORY_TRACK_FORBIDDEN

## 场景穷举
- 正常：S-01 add/search · S-02 forget 回执 · S-03 离职清库作业
- 异常：E-01 跨人检索 · E-02 回执验签失败
- 边界：B-01 空记忆

## Acceptance Criteria
- [ ] A8
- [ ] I-08
- [ ] 独立 Postgres uas_lethe

## 依赖与约束
- 前置：独立库 · M8 track
- 技术：见模块设计 M17；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M17-1 分库 · US-M17-2 Hub 封装 · US-M17-3 回执台
- TDD 先写：test_pipaw_forbidden · test_forget_receipt_in_audit · test_no_fk_to_ag_node
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/lethe-api/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M17 节）

## 映射
UAS-AIOS M17 · 层 K-L3
