# Requirement: REQ-UAS-M01 — M1 WorkStudio 作战台

## Status: completed

## 需求层级: 能力

## 优先级: P0

## 阶段: A（对齐规格 WBS）

## 提出日期: 2026-09-10

## Derived from
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md

## 问题描述（不是方案）
- 谁：一线 CM/BD、指挥席
- 遇到什么问题：打开系统面对空白对话或报表墙，不知道今天卡在哪个责任节点、下一步该派给谁。
- 为什么重要：看见并办成的端侧唯一入口；失败则 Hub 再强也无人使用。

## 验证标准
- 成功：打开作战台 <2s 见到本人切片；gate 节点进入今日必办；403 有人话。
- 失败/放弃：一线菜单出现连接器、workflow_id 或 Cube 查询。

## Given / When / Then
- Given 已登录且绑定 position_id=pos-cm，样例图 ag-hengchuan-ltc 已发布
- When 打开 /today 并调用 pack.open
- Then 渲染水合节点；an-stage-visit 若 status=gate 上浮；无聊天空白页

## 场景穷举
- 正常：S-01 打开今日必办见 gate 节点 · S-02 进入客户作战室只读 360 · S-03 指挥舱按 org_cascade 聚合
- 异常：E-01 pack.open 失败人话降级 · E-02 场景调写 cs→展示 PROFILE_FORBIDS_SIDE_EFFECT · E-03 SSE 中断可重连
- 边界：B-01 空切片（无岗位）403 · B-02 stale 口径打标不假装实时

## Acceptance Criteria
- [x] 零零件 SDK：网络面板无 Cube/Graphiti/CRM 主机
- [x] A1：CM 打开即见 an-stage-visit gate
- [x] A2：scene 写路径只展示不可调用，点写得人话
- [x] P0 可沿用 demo 壳，产品路径 Vite+TS 不引入 Next

## 依赖与约束
- 前置：M6 Hub · M2 责任图 · M5 签发
- 技术：见模块设计 M1；判定序/信封/场景禁写不可豁免
- 合规：双轨、审计、密钥不出模型

## 开发规划
- 故事：US-M1-1 pack.open 首页 · US-M1-2 作战室 · US-M1-3 指挥舱只读 · US-M1-4 错误人话
- TDD 先写：test_pack_open_renders_gate_node · test_scene_cannot_invoke_cs_write · test_sse_progress_reconnect
- 估算：8 点
- DoR：schema/样例或上游契约已挂；AC 三 Amigos 认可；不引入禁替代清单中的产品当内核
- DoD：上述 AC 勾选；对应 invariant 或契约测试绿；产出回写 harness

## Files Involved
- projects/aios-workstudio/demo/ · services/workstudio-web/（P1）
- `harness/knowledge/technical/uas-aios-module-delivery.md`（M1 节）

## 映射
UAS-AIOS M1 · 层 I / 使用平面
