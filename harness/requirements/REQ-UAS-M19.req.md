# Requirement: REQ-UAS-M19 — M19 LangGraph 内环

## Status: pending

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：Explore/Builder/Runtime 短循环
- 遇到什么问题：多套 Agent 框架并行；图节点直打 CRM。
- 为什么重要：一套 SPI；默认 LangGraph 1.0。

## 验证标准
- 成功：工具回调只进 Hub；checkpoint≠聊天全文。
- 失败/放弃：CrewAI/第三套；Codex 并行生产。

## Given / When / Then
- Given INNERLOOP_BACKEND=langgraph
- When 模型 tool_call cs.visit.schedule
- Then 只发生 hub.invoke_cs，无出站 CRM HTTP

## 场景穷举
- 正常：S-01 start/turn · S-02 interrupt/resume · S-03 compact 保五维
- 异常：E-01 工具不在 allowlist · E-02 checkpoint 损坏可从 Task 重建
- 边界：B-01 空 wm_slice 拒绝

## Acceptance Criteria
- [ ] I-07 静态+运行时
- [ ] SPI 测试矩阵只跑一套

## 依赖与约束
- 前置：M6 InnerLoop SPI · M24 · M13
- 技术：见模块设计 M19；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M19-1 SPI · US-M19-2 LangGraph 适配 · US-M19-3 checkpoint PG
- TDD 先写：test_no_outbound_http_to_crm · test_compact_keeps_five_dims · test_backend_switch_one_matrix
- 估算：13 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- services/hub-api/innerloop/
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M19 节）

## 映射
UAS-AIOS M19 · 层 A/R
