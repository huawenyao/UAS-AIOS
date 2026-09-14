# Requirement: REQ-UAS-M08 — M8 Identity & Policy

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：平台管理员、合规
- 遇到什么问题：IdP 组被当成经营承诺权；双轨混权。
- 为什么重要：人在 IdP，岗位与 track 在 Hub。

## 验证标准
- 成功：无岗位绑定打不开切片；pipaw 禁 Lethe；升级必须证据。
- 失败/放弃：Salesforce Profile 当写权权威。

## Given / When / Then
- Given 仅 selfpaw 令牌无 pipaw
- When 经营写 cs
- Then TRACK_ESCALATION_REQUIRED

## 场景穷举
- 正常：S-01 OIDC 登录 · S-02 岗位绑定 · S-03 升级工单
- 异常：E-01 跨租户 403 · E-02 令牌过期 · E-03 权限 JSON 后台改无效须 ChangeSet
- 边界：B-01 多岗位切换 · B-02 scope=self 注入连接器

## Acceptance Criteria
- [ ] 对齐 enterprise-rbac-abac-spec
- [ ] A7/A8/A11
- [ ] I-10

## 依赖与约束
- 前置：IdP · M2 org.* · 既有 RBAC 规格
- 技术：见模块设计 M8；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M8-1 OIDC · US-M8-2 binding 表 · US-M8-3 scope 注入
- TDD 先写：test_no_position_no_pack · test_pipaw_memory_forbidden · test_escalation_needs_evidence
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- harness/knowledge/technical/enterprise-rbac-abac-spec.md · services/hub-api/iam/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M8 节）

## 映射
UAS-AIOS M8 · 层 G
