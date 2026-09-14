# Requirement: REQ-UAS-M13 — M13 MCP Gateway

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：内环模型、平台运营
- 遇到什么问题：list 出的工具被直打连接器；密钥进 description。
- 为什么重要：对模型只暴露语义名。

## 验证标准
- 成功：call 重走判定序；scene 无写工具。
- 失败/放弃：自研平行 function-call 协议。

## Given / When / Then
- Given scene 会话
- When tools/list 与伪造 call 写工具
- Then list 不含写工具；call 403

## 场景穷举
- 正常：S-01 按剖面过滤 list · S-02 call 双检 · S-03 网关 QPS/拒因
- 异常：E-01 description 含 URL 发布失败 · E-02 MCP 协议版本不匹配
- 边界：B-01 空 allowlist

## Acceptance Criteria
- [ ] 官方 MCP Python SDK
- [ ] I-05
- [ ] 密钥不出 description

## 依赖与约束
- 前置：M7 · M6
- 技术：见模块设计 M13；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M13-1 HTTP MCP · US-M13-2 与 Hub 同门禁
- TDD 先写：test_list_filters_side_effects · test_call_reruns_policy · test_no_secrets_in_schema
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/mcp-gateway/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M13 节）

## 映射
UAS-AIOS M13 · 层 Π
