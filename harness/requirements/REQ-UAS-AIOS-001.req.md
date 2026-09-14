# Requirement: REQ-UAS-AIOS-001 — UAS-AIOS 集群程序史诗

## Status: in_progress

## 需求层级: 战略

## 优先级: P0

## 提出日期: 2026-09-10

## Derived from
ENTERPRISE_AGI_OPERATING_HUB.md · UAS_AIOS_ARCHITECTURE_SPEC.md · UAS_AIOS_CLUSTER_PRODUCTIZATION.md · UAS_AIOS_MODULE_DESIGN.md · ADR-SEL-001/002/003 · ADR-EDH-001/002

## 问题描述（不是方案）
- 谁：营销一线、指挥席、平台/合规、知识管理员、实施与 SRE
- 场景：从线索到回款，指标能看见但不能派活、办完不回流
- 问题：Dashboard 停在「人看完再切系统」；市场上的语义层/Agent 平台被误当成 AIOS
- 为什么重要：组织目标必须 ≡ 经营数据；看见必须能办成

## 产品目标
- 量化：阶段 A 结束，衡川 LTC 样例可 `pack.open` + 签发 Task（不写 CRM）；场景写 cs 403+人话
- 非目标：自研大模型/MDM/CRM；采购 Palantir/Fabric IQ/Agentforce/Copilot Studio 当 OS；P0 跨租户 A2A；Utopia 进写路径
- 失败：一线菜单出现连接器/工作流 ID/Cube 查询；第三套循环；Lethe 与责任图同 schema

## 假设（已冻结，变更走 ADR）
- 经营本体与控制面自研；Cube/Graphiti/Lethe/Temporal/LangGraph 为可替换零件
- 内环默认 LangGraph；Codex 仅同一 SPI
- 本程序覆盖方案研究→规格→开发规划，**不含**本迭代 TDD 实现代码

## 下层功能需求
REQ-UAS-M01 … REQ-UAS-M24（每模块一卡，含场景、AC、TDD 先写用例、估算）

## Acceptance Criteria
- [x] 24 张模块需求卡落入 `harness/requirements/REQ-UAS-M*.req.md`
- [x] 技术方案 `harness/knowledge/technical/uas-aios-module-delivery.md`
- [x] ADR-SEL-001/002/003 回写 `harness/knowledge/constraints/`
- [x] 迭代规划 `harness/requirements/sprint-uas-aios-001.md`
- [x] entity-map / state / index / glossary 回写
- [ ] 阶段 A 代码与 invariant（后续 sprint，本 REQ 不包含实现）

## Files Involved
- `docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md`
- `harness/knowledge/technical/uas-aios-module-delivery.md`
- `harness/knowledge/product/uas-aios-cluster-prd.md`
