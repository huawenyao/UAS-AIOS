# PRD：UAS-AIOS 集群（方案研究）

> reqharness 产品角色产出。实现细节见模块设计与技术方案。  
> 日期：2026-09-10 · 状态：评审通过（对齐冻结架构）

## 1. 背景与目标

### 1.1 业务背景
一线靠报表+聊天+CRM 三套界面拼经营。指标下拆不能签发任务，任务办完不回写指标。市场上把 Cube/Dify/Copilot Studio 误当成经营 OS。

### 1.2 产品目标
- 目标：作战台打开即见责任图切片；gate 可派活；Runtime 写 SoR 后同一节点 `kpi.is` 合流
- 非目标：聊天壳、BI 墙、别人的 Ontology OS、第三套 Agent 循环
- 成功：规格验收 A1–A12；集群集成 I-01–I-12
- 失败：场景能写生产；个人记忆当经营状态；零件名出现在一线菜单

## 2. 用户与场景

| 角色 | 主产品 | 频率 | 核心场景 |
|------|--------|------|----------|
| CM/BD | WorkStudio | 每日 | 今日必办、作战室、签发、待确认 |
| 指挥席 | 指挥舱 | 每日 | 子树、调配、合流 |
| 知识管理员 | Ontology / Pack Studio | 每周 | 责任图、Law、口径 YAML |
| 平台管理员 | Hub Console / Mesh | 每周 | 剖面、目录、连接器槽 |
| 合规 | Governance / Lethe | 按需 | 审计包、遗忘回执 |
| SRE | Runtime / Knowledge Ops | 每日 | 续跑、stale、健康 |

主路径（衡川 LTC）：打开 → 见拜访停留 gate → drill 接地 → 签发 BD → exec.open → 写拜访 → 回流 is。

异常：场景点写 → 人话引导签发；未接地 → 不能派活；L2 未批 → 暂停不丢。

## 3. 功能范围
- 本期程序（规划）：M1–M24 全覆盖规格与开发计划
- 本期实现（代码）：无（下一迭代阶段 A）
- 明确不做：Utopia 默认部署、跨租户 A2A、AG-UI P0、K8s 作为 P0 前置

## 4. 非功能
- 打开作战台 <2s；签发到可见进度 <3s
- 403 必须有 `error.message` + explain
- 租户隔离；密钥不出模型；Lethe 分库

## 5. 埋点（产品语言）
`pack.opened` `insight.grounded|ungrounded` `task.issued` `exec.opened` `cs.invoked` `approval.wait` `wm.live.patched` `changeset.drafted` `memory.forgotten`

## 6. 依赖与风险
- 依赖：既有 cs.* registry、租户/审计契约、WorkStudio Demo
- 风险：Graphiti/Temporal 运维；内环与 Codex 分叉诱惑 → ADR-SEL-002 关闭
- 回滚：零件可换，契约不换

## 7. 排期
见 `sprint-uas-aios-001.md` 与规格 §9 阶段 A–D。

平台级产品定义（套件 / 用户故事 / 数据链路 / 运营与系统界面）：[`UAS_AIOS_PLATFORM_PRODUCT.md`](../../../docs/strategic/design/UAS_AIOS_PLATFORM_PRODUCT.md)。
