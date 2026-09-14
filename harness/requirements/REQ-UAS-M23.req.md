# Requirement: REQ-UAS-M23 — M23 主数据 SoR

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: C（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：客户 IT
- 遇到什么问题：想自研轻量 CRM 当 P0。
- 为什么重要：不自研 MDM；只存 object_ref。

## 验证标准
- 成功：沙箱 Mock；生产映射客户 CRM。
- 失败/放弃：UAS 提供 CRM 产品。

## Given / When / Then
- Given object_ref=UEC-10293
- When cs.customer.get_profile
- Then 连接器回主数据，责任图只挂引用

## 场景穷举
- 正常：S-01 账户槽 · S-02 环境隔离
- 异常：E-01 SoR 未授权
- 边界：B-01 无 CRM 用 mock

## Acceptance Criteria
- [ ] 不复制主档
- [ ] Agentforce 只当 cs 后端

## 依赖与约束
- 前置：M14 · 客户 IT
- 技术：见模块设计 M23；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M23-1 账户运营页 · US-M23-2 衡川沙箱映射
- TDD 先写：test_object_ref_not_copied_as_mdm
- 估算：3 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/connectors/ · configs/connectors.json
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M23 节）

## 映射
UAS-AIOS M23 · 层 S 连接
