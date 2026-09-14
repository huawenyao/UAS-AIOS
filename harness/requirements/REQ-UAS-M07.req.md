# Requirement: REQ-UAS-M07 — M7 Capability Registry cs.*

## Status: in_progress

## 需求层级: 能力

## 优先级: P0

## 阶段: A（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：平台管理员发布能力
- 遇到什么问题：模型看见 REST/SQL；目录与 MCP 名漂移。
- 为什么重要：Agent 不直连系统的契约源。

## 验证标准
- 成功：operation 含 side_effects/gates；租户未启用则步骤2拒绝。
- 失败/放弃：OpenAPI 自动当语义目录；运行时模型注册生产工具。

## Given / When / Then
- Given registry 已有 cs.visit.schedule side_effects 非空
- When scene tools/list
- Then 该工具不可见；call 仍 403

## 场景穷举
- 正常：S-01 加载 JSON · S-02 租户覆盖启用 · S-03 发布 ChangeSet
- 异常：E-01 schema 非法 CI 红 · E-02 名与 MCP 不一致红灯
- 边界：B-01 空 side_effects 只读可 list

## Acceptance Criteria
- [x] 扩展 cs.metric.query 与 cs.visit.schedule
- [ ] I-12
- [x] 沿用 validate_capability_registry.py

## 依赖与约束
- 前置：已有 registry · M20 · M13
- 技术：见模块设计 M7；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M7-1 写操作标记 · US-M7-2 租户开关 · US-M7-3 目录控制台
- TDD 先写：test_write_ops_hidden_in_scene · test_registry_mcp_name_parity
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- configs/capability_registry.json · scripts/validate_capability_registry.py
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M7 节）

## 映射
UAS-AIOS M7 · 层 S/Π
