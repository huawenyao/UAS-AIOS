# Requirement: REQ-UAS-M10 — M10 Artifact Store

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：构建者、运行时
- 遇到什么问题：报告/PDF 被当成经营状态回放。
- 为什么重要：产物≠主数据≠世界模型。

## 验证标准
- 成功：Task/Theme/Release 晋升条；file 类不可 pack.open 回放。
- 失败/放弃：制品只放磁盘无哈希。

## Given / When / Then
- Given kind=file 的报告
- When 当作 pack 状态源读取
- Then API 拒绝 / UI 禁用

## 场景穷举
- 正常：S-01 上传哈希 · S-02 晋升 · S-03 按 task_id 取回
- 异常：E-01 sha 不匹配 · E-02 跨租户读
- 边界：B-01 空制品库

## Acceptance Criteria
- [ ] MinIO/S3 + artifact_meta
- [ ] 报告不可回放经营

## 依赖与约束
- 前置：M5 Task · 对象存储
- 技术：见模块设计 M10；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M10-1 元数据表 · US-M10-2 晋升 API
- TDD 先写：test_file_kind_not_state_source · test_sha256_addressing
- 估算：5 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/hub-api/artifact/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M10 节）

## 映射
UAS-AIOS M10 · 层 R
