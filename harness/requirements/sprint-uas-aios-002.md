# 迭代规划：sprint-uas-aios-002

| 属性 | 值 |
|------|-----|
| ID | sprint-uas-aios-002 |
| 名称 | 阶段 A 编码：契约 + 门禁 + 签发 |
| 周期 | 2026-09-10 ~ 2026-09-24 |
| 上一迭代 | sprint-uas-aios-001（规划完成） |

## 迭代目标
- 业务：场景不能写生产；打开切片能看到 gate 节点；签发必须带源节点且不启 Temporal
- 技术：`services/hub-api` 可单测运行；Demo 吃 pack.open 夹具

## 承诺（已实现）

| 故事 | 验收 | 状态 |
|------|------|------|
| M20 缺口 schema | insight / operating_task / gate_map | 完成（codegen CI 未做） |
| M7 cs.visit.schedule + cs.metric.query | scene list 隐藏写工具 | 完成 |
| M6 PolicyChain + HTTP | 序 0–8、伪造 profile 作废、`/hub/v1` | 完成（Console 未做） |
| M2 pack.open | 岗位切片、跨租户拒绝、stale、缺维拒签发 | 完成（Postgres 未做） |
| M5 issue | 无源节点 / 未接地 / workflow_id=null | 完成 |
| M3 compiled 只读 | runtime PATCH compiled 拒绝 | 最小完成 |
| M1 Demo | pack.open 渲染 an-stage-visit；点写得人话 | 完成（live hub.*，离线回退夹具） |

## 不在本期
| 项 | 原因 |
|----|------|
| Temporal / Graphiti / Cube 真零件 | 阶段 B；本期口径/接地用夹具 |
| Platform Console / hub.ops | 阶段 A 不做管理壳 |
| schema codegen 漂移 CI | M20 剩余；不阻塞签发 |

## DoD
- [x] `python scripts/validate_uas_aios_phase_a.py`
- [x] FastAPI `/hub/v1` 包同一 Hub（body.profile 作废）
- [x] `python scripts/export_hub_pack_open.py`
- [ ] `python harness/invariants/run-all.py`（含既有 selfpaw-enterprise 缺口）
- [x] 不引入第三套循环、不持有 SoR 密钥
