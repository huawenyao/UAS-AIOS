# Requirement: REQ-UAS-M03 — M3 世界模型 Store

## Status: in_progress

## 需求层级: 能力

## 优先级: P0

## 阶段: A（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：Builder、Runtime、指挥席
- 遇到什么问题：法则、应当/事实、运行态混在聊天或一份 JSON 里，无法区分编译产物与现场。
- 为什么重要：熔炉必须过门禁；Runtime 不得改 compiled。

## 验证标准
- 成功：同一 world_model_id 三寿命；live PATCH 不碰 compiled。
- 失败/放弃：Lethe/Graphiti 充当 live。

## Given / When / Then
- Given compiled 版本 n 已 release
- When Runtime cycle_step 试图 PATCH compiled
- Then 拒绝；仅 live 增加补丁版本

## 场景穷举
- 正常：S-01 draft→compiled 晋升 · S-02 live 钩子补丁 · S-03 指挥席只读 live
- 异常：E-01 缺维不能 compiled · E-02 剖面错误写寿命
- 边界：B-01 多版本并存 · B-02 回滚到上一 compiled

## Acceptance Criteria
- [ ] 三寿命表 UNIQUE(id,lifetime,version)
- [ ] A10 invariant 失败不能 release

## 依赖与约束
- 前置：M2 · M4 · M6
- 技术：见模块设计 M3；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M3-1 寿命 API · US-M3-2 晋升门禁 · US-M3-3 对照板
- TDD 先写：test_runtime_cannot_patch_compiled · test_promote_requires_five_dims
- 估算：5 点
- 阶段 A：`test_runtime_cannot_patch_compiled` 已绿；三寿命表与 release invariant 未做
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- schemas/enterprise_world_model.schema.json · services/hub-api/wm/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M3 节）

## 映射
UAS-AIOS M3 · 层 K-L0
