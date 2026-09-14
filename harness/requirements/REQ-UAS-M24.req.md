# Requirement: REQ-UAS-M24 — M24 模型推理 Broker

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：SRE、平台
- 遇到什么问题：厂商 Assistants 会话当实例状态；绑死一家。
- 为什么重要：模型必须可换。

## 验证标准
- 成功：剖面→模型路由；会话不当 WM。
- 失败/放弃：一线菜单选模型当功能。

## Given / When / Then
- Given configs/model_routes.yml 切提供商
- When 同一 explore turn
- Then hub.* 契约不变，一线名词不变

## 场景穷举
- 正常：S-01 路由 · S-02 限流 · S-03 token 审计
- 异常：E-01 提供商 429 可重试 · E-02 密钥仅 Broker
- 边界：B-01 无模型时 explore 降级

## Acceptance Criteria
- [ ] 薄 Broker
- [ ] 换模型不改 hub.*

## 依赖与约束
- 前置：M19 · 模型路由配置
- 技术：见模块设计 M24；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M24-1 路由配置 · US-M24-2 OpenAI 兼容适配
- TDD 先写：test_provider_switch_keeps_hub_contract · test_chat_not_instance_state
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/hub-api/broker/ · configs/model_routes.yml
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M24 节）

## 映射
UAS-AIOS M24 · 层 A 连接
