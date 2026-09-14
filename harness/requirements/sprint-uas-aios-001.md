# 迭代规划：sprint-uas-aios-001

| 属性 | 值 |
|------|-----|
| ID | sprint-uas-aios-001 |
| 名称 | UAS-AIOS 模块 reqharness：方案研究→开发规划 |
| 周期 | 2026-09-10 ~ 2026-09-24（规划冻结） |
| 下一实现迭代 | sprint-uas-aios-002 = 规格阶段 A 编码 |

## 迭代目标
- 业务：把集群 24 模块从架构文档变成可跟踪需求、技术方案与阶段计划
- 技术：harness 回写完整；不写生产代码；invariants 仍全绿

## 容量
- 本迭代：研究/规格/规划（已执行）
- 预留 buffer：实现阶段见技术方案人天表（A≈31 人天含 buffer）

## 候选故事（规划已承诺，实现未开始）

| 故事 | 优先级 | 估算点 | 依赖 | 风险 |
|------|--------|--------|------|------|
| REQ-UAS-M20 缺口 schema+漂移 CI | P0 | 3 | — | 低 |
| REQ-UAS-M02 责任图落库 | P0 | 8 | M20 | 模型想用 Neo4j |
| REQ-UAS-M07 写操作标记 | P0 | 5 | 现有 registry | 低 |
| REQ-UAS-M06 PolicyChain | P0 | 13 | M7 | 想上 OPA |
| REQ-UAS-M05 签发 | P0 | 8 | M2 M6 | 接地依赖 M16，A 可用夹具 |
| REQ-UAS-M03 三寿命最小 | P0 | 5 | M2 | 低 |
| REQ-UAS-M01 Demo 接线 | P0 | 8 | M6 M5 | 平行第二套 UI |
| 其余 M8–M24 | 按阶段 B–D | 见交付方案 | Hub | 范围膨胀 |

## 迭代承诺（本 sprint）

| 产出 | Owner 角色 | 验收 | 状态 |
|------|------------|------|------|
| REQ-UAS-AIOS-001 + M01–M24 | 需求/产品 | 24 卡 + AC + TDD 名 | 完成 |
| PRD 集群 | 产品 | 用户/非目标/埋点 | 完成 |
| 技术方案 | 架构/开发 | 阶段人天、数据、测试 | 完成 |
| ADR-SEL-001/002/003 | 架构 | harness/constraints | 完成 |
| entity-map / state / glossary | 融合层 | invariant 绿 | 本迭代结束时 |

## 不在本期
| 项 | 原因 | 预计 |
|----|------|------|
| hub-api 代码 | 本 sprint 只到规划 | sprint-uas-aios-002 |
| Temporal/Graphiti Compose | 阶段 B | Q1 |
| Utopia / A2A 网络 | P2/P1 | 阶段 D |
| K8s | 非 P0 | P1 |

## DoD（本规划 sprint）
- [x] 需求写入 `requirements/*.req.md`
- [x] 技术方案写入 `knowledge/technical/`
- [x] ADR 写入 `knowledge/constraints/`
- [ ] `python harness/invariants/run-all.py` PASS（回写后执行）

## 三 Amigos 纪要（压缩）
- 产品：一线只走作战台；403 必须人话；签发≠写 CRM
- 开发：阶段 A 用口径/接地夹具，接口名冻结；禁止第三套循环
- 测试：先契约（场景写拒绝、源节点、租户），再 E2E 衡川样例
