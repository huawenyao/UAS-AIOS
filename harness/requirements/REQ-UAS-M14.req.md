# Requirement: REQ-UAS-M14 — M14 System Connector

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：实施、SRE、客户 IT
- 遇到什么问题：模型或 Worker 持有 SoR 密钥并直打 REST。
- 为什么重要：密钥不出模型；映射在适配器。

## 验证标准
- 成功：SPI invoke+幂等；厂商错误结构化。
- 失败/放弃：LangGraph 内 httpx CRM。

## Given / When / Then
- Given idempotency_key 相同的第二次 cs.visit.schedule
- When 连接器执行
- Then 不双写 CRM

## 场景穷举
- 正常：S-01 mock 槽 · S-02 沙箱/生产槽 · S-03 凭证轮换
- 异常：E-01 SoR 5xx 映射码 · E-02 超时补偿信号
- 边界：B-01 未知 operation

## Acceptance Criteria
- [ ] 对齐 system-connector-spec
- [ ] Worker 环境无明文密钥
- [ ] I-07

## 依赖与约束
- 前置：既有 mock · KMS · M18 幂等
- 技术：见模块设计 M14；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M14-1 Connector SPI · US-M14-2 mock 拜访 · US-M14-3 真 CRM 适配（阶段C）
- TDD 先写：test_idempotent_no_double_write · test_keys_not_in_worker_env · test_error_not_html
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/connectors/ · asui-cli/src/asui/connectors/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M14 节）

## 映射
UAS-AIOS M14 · 层 S
