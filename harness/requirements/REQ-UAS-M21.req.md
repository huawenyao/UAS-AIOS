# Requirement: REQ-UAS-M21 — M21 跨岗位委托 A2A

## Status: pending

## 需求层级: 能力

## 优先级: P1

## 阶段: D（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：指挥席、跨岗位
- 遇到什么问题：跨岗位靠聊天或自研总线；身份放进载荷。
- 为什么重要：P0 transfer；P1 A2A；对端仍进 Hub。

## 验证标准
- 成功：P0 改 assignee 有审计；跨租户默认拒绝。
- 失败/放弃：ACP；Card 替代门禁。

## Given / When / Then
- Given 同租户任务
- When hub.task.transfer 给 pos-legal
- Then assignee 更新，源节点不变，审计一条

## 场景穷举
- 正常：S-01 transfer · S-02 P1 Agent Card · S-03 对端 Hub 门禁
- 异常：E-01 跨租户 403 · E-02 无权限转派
- 边界：B-01 转给自己

## Acceptance Criteria
- [ ] P0 API
- [ ] A2A 默认不部署

## 依赖与约束
- 前置：M5 · M8
- 技术：见模块设计 M21；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M21-1 transfer · US-M21-2 Card 设计（不实现网络）
- TDD 先写：test_transfer_same_tenant · test_cross_tenant_denied
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/hub-api/transfer/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M21 节）

## 映射
UAS-AIOS M21 · 层 A/Π
