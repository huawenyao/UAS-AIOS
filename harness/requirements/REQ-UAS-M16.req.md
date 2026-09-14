# Requirement: REQ-UAS-M16 — M16 时态知识 Graphiti

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：Explore、作战室时间线
- 遇到什么问题：文档 RAG 被当成「何时为真」；图 mutation 当写 CRM。
- 为什么重要：Insight 必须接地。

## 验证标准
- 成功：search 带 valid_from/to；ingest≠cs 写；未接地不能签发。
- 失败/放弃：Dify 知识库当 L2。

## Given / When / Then
- Given 无 evidence 的 Insight
- When task.issue
- Then UNGROUNDED_INSIGHT

## 场景穷举
- 正常：S-01 episode 摄入 · S-02 object_ref 检索 · S-03 what-changed
- 异常：E-01 实体名不在白名单 · E-02 图库宕机 Insight 不可 grounded
- 边界：B-01 as_of 历史时点

## Acceptance Criteria
- [ ] I-04
- [ ] Pydantic 实体白名单
- [ ] 图 ID≠an-*

## 依赖与约束
- 前置：Neo4j · M5 接地
- 技术：见模块设计 M16；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M16-1 Compose Neo4j · US-M16-2 hub.kg.* · US-M16-3 摄入 ETL
- TDD 先写：test_ungrounded_blocked · test_ingest_not_cs_write · test_entity_whitelist
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/graphiti-worker/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M16 节）

## 映射
UAS-AIOS M16 · 层 K-L2
