# Requirement: REQ-UAS-M02 — M2 责任图 Accountability Graph

## Status: in_progress

## 需求层级: 能力

## 优先级: P0

## 阶段: A（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：知识管理员、Hub scene
- 遇到什么问题：目标树/组织树/KPI 树/流程树四套系统对不齐，指标无法签发到人。
- 为什么重要：目标≡数据的唯一经营写入；缺此无合法 source_node_id。

## 验证标准
- 成功：节点五件套校验失败不得签发；pack.open 按岗位切片。
- 失败/放弃：用 Neo4j/Graphiti 当 L0；口头口径当权威。

## Given / When / Then
- Given tenant 已有 sample 图
- When 校验节点缺 wm 或 kpi.caliber 并尝试 task.issue
- Then WM_INCOMPLETE 或 CALIBER_MISSING，任务不落库

## 场景穷举
- 正常：S-01 CRUD 图+边四类投影 · S-02 pack.open 切片 · S-03 发布走 ChangeSet
- 异常：E-01 缺维拒绝签发 · E-02 跨租户读 403 · E-03 Cube 失败标 stale
- 边界：B-01 空边图仍可打开 · B-02 parent 环检测拒绝

## Acceptance Criteria
- [x] schema+sample invariant
- [ ] Postgres JSONB 存图非 Neo4j
- [x] I-02 缺维不能签发

## 依赖与约束
- 前置：M15 口径水合（P0 可 YAML 替身） · M20 schema
- 技术：见模块设计 M2；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M2-1 落库+索引 · US-M2-2 切片 API · US-M2-3 编辑器最小集
- TDD 先写：test_node_requires_five_tuple · test_pack_open_slices_by_position · test_cross_tenant_forbidden
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- schemas/accountability_graph.schema.json · services/hub-api/graph/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M2 节）

## 映射
UAS-AIOS M2 · 层 K-L0
