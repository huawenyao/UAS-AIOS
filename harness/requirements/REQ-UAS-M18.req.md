# Requirement: REQ-UAS-M18 — M18 Temporal 外环

## Status: in_progress

## 需求层级: 能力

## 优先级: P0

## 阶段: B（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：Runtime 长任务、SRE
- 遇到什么问题：审批停三天、失败重来、HITL 用线程睡眠或 Celery。
- 为什么重要：耐久寿命在 Temporal；门禁仍在 Hub。

## 验证标准
- 成功：RuntimeCycleWorkflow；Worker 回调 Hub；一线不见 workflow_id。
- 失败/放弃：Workflow 内直接调 LLM；Camunda 替代外环。

## Given / When / Then
- Given task issued
- When exec.open 后杀 Worker 再拉起
- Then 从断点续，审批信号不丢

## 场景穷举
- 正常：S-01 StartWorkflow · S-02 WaitForSignal L2 · S-03 RefreshKpi
- 异常：E-01 InvokeCs 403 不写 SoR · E-02 RefreshKpi 失败重试不回滚合法写
- 边界：B-01 超时 DraftChangeSet

## Acceptance Criteria
- [x] I-06 契约：Activity 共用 `cycle.py`；Compose + Workflow 无 LLM
- [x] A6 L2 未批不写（实验室外环）
- [ ] I-06 live：对运行中 Temporal 杀 Worker 续跑

## 依赖与约束
- 前置：M6 · M19 · M14
- 技术：见模块设计 M18；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M18-1 Compose Temporal · US-M18-2 Workflow · US-M18-3 SSE 桥
- TDD 先写：test_worker_killed_resumes · test_invoke_cs_goes_through_hub · test_l2_waits_signal
- 估算：13 点
- 阶段 B：`InMemoryOuterLoop` 与 Temporal Activity 共用 `uas_hub.cycle`；`deploy/compose/docker-compose.yml` 已落
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- `services/hub-api/uas_hub/cycle.py`
- `services/temporal-worker/`
- `deploy/compose/docker-compose.yml`

## 映射
UAS-AIOS M18 · 层 R
