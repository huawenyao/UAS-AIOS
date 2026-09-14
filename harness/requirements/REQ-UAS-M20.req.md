# Requirement: REQ-UAS-M20 — M20 工具契约 JSON Schema

## Status: in_progress

## 需求层级: 能力

## 优先级: P0

## 阶段: A（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：平台/CI
- 遇到什么问题：模型一份宽松 schema、连接器一份严格 schema。
- 为什么重要：一份权威三处生成。

## 验证标准
- 成功：codegen + CI 漂移红灯。
- 失败/放弃：三份手写长期分叉。

## Given / When / Then
- Given registry 增字段未生成
- When CI
- Then 失败禁止合并

## 场景穷举
- 正常：S-01 生成 Pydantic · S-02 MCP 同源 · S-03 前台 AJV 可选
- 异常：E-01 生成物被手改
- 边界：B-01 空 properties

## Acceptance Criteria
- [ ] I-12
- [ ] datamodel-code-generator 或等价

## 依赖与约束
- 前置：M7
- 技术：见模块设计 M20；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M20-1 流水线 · US-M20-2 缺口 insight/task schema
- TDD 先写：test_schema_drift_fails_ci · test_pydantic_matches_registry
- 估算：3 点
- 阶段 A：`insight.schema.json` / `operating_task.schema.json` / `gate_map.json` 已挂；codegen 漂移 CI 未做
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- schemas/ · services/hub-api/generated/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M20 节）

## 映射
UAS-AIOS M20 · 层 Π
