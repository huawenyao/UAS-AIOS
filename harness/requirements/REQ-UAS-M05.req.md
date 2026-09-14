# Requirement: REQ-UAS-M05 — M5 Insight→Task 编译器

## Status: completed

## 需求层级: 能力

## 优先级: P0

## 阶段: A（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：一线确认派活
- 遇到什么问题：Dashboard 停在人看完再切系统；建议没有源节点和证据。
- 为什么重要：相对 BI 的分水岭；无源节点不是经营任务。

## 验证标准
- 成功：签发必带 source_node_id；未接地 422；签发不启 Temporal。
- 失败/放弃：LangGraph 自行决定写 CRM。

## Given / When / Then
- Given 节点五维齐，Insight grounded=true
- When POST task.issue
- Then status=issued，workflow_id=null，CRM 无写

## 场景穷举
- 正常：S-01 drill 出 Insight · S-02 确认签发 · S-03 驳回进演化
- 异常：E-01 无源节点 422 · E-02 未接地 422 · E-03 cs_write 超白名单 422
- 边界：B-01 空 evidence · B-02 并发重复签发幂等

## Acceptance Criteria
- [x] 补 insight/operating_task schema
- [x] A3/A4
- [x] 签发≠执行

## 依赖与约束
- 前置：M2 · M3 · M16 接地 · M10
- 技术：见模块设计 M5；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M5-1 schema · US-M5-2 drill · US-M5-3 issue/return
- TDD 先写：test_task_requires_source_node · test_ungrounded_cannot_issue · test_issue_does_not_start_temporal
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- schemas/insight.schema.json · schemas/operating_task.schema.json · services/hub-api/insight/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M5 节）

## 映射
UAS-AIOS M5 · 层 I
