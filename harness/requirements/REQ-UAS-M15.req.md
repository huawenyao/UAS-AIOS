# Requirement: REQ-UAS-M15 — M15 口径 Cube + OSI

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: C（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：口径运营、作战台水合
- 遇到什么问题：口头口径；仓 Semantic View 当唯一真相。
- 为什么重要：kpi.is 必须可解释、带 as_of。

## 验证标准
- 成功：YAML 口径；失败 stale；Cube 不签发任务。
- 失败/放弃：LookML/Fabric 当内核。

## Given / When / Then
- Given Cube 宕机但有缓存
- When pack.open
- Then is 为缓存且 stale=true，页面可开

## 场景穷举
- 正常：S-01 OSI YAML · S-02 metric.query · S-03 指挥舱同口径切片
- 异常：E-01 无 caliber_id 422 · E-02 仓超时 stale
- 边界：B-01 维度空

## Acceptance Criteria
- [ ] I-03
- [ ] configs/metrics/osi/
- [ ] 模型不见 CubeQL

## 依赖与约束
- 前置：仓 · M7 cs.metric.query
- 技术：见模块设计 M15；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M15-1 样例 YAML · US-M15-2 Cube Compose · US-M15-3 Hub 适配
- TDD 先写：test_metric_query_as_of · test_cube_down_marks_stale · test_cube_cannot_issue_task
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- configs/metrics/osi/ · configs/cube/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M15 节）

## 映射
UAS-AIOS M15 · 层 K-L1
