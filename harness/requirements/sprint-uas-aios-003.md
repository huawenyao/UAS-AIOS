# 迭代规划：sprint-uas-aios-003

| 属性 | 值 |
|------|-----|
| ID | sprint-uas-aios-003 |
| 名称 | 阶段 B 起步：exec.open 外环端口 |
| 周期 | 2026-09-10 ~ 2026-09-24 |
| 上一迭代 | sprint-uas-aios-002 |

## 迭代目标
- 签发之后才能进入运行；L2 先等待确认再写 cs
- 外环接口名冻结为 `RuntimeCycleWorkflow`；实验室内存实现可被 Temporal 替换
- 一线不展示 workflow_id

## 承诺

| 故事 | 验收 | 状态 |
|------|------|------|
| M18 exec.open | 未签发拒绝；L2 等待；确认后走 hub.invoke_cs | 实验室完成 |
| Worker 快照续跑 | `test_worker_killed_resumes` | 内存端口完成 |
| SSE 事件列表 | `GET /hub/v1/exec/{task_id}/events` | JSON 列表，非 AG-UI |

## 不在本期
| 项 | 原因 |
|----|------|
| Temporal 集群 live I-06 | 需本机 Compose + TEMPORAL_ADDRESS |
| LangGraph InnerLoop | M19 |
| Platform Console | 阶段 A/B 均不做管理壳 |

## DoD
- [x] `python scripts/validate_uas_aios_phase_a.py`（含 test_exec）
- [x] 不引入 Celery / 第三套循环
- [x] Compose 文件 + Workflow 定义无 LLM（实验室 I-06 契约）
- [ ] 对运行中 Temporal 杀 Worker 续跑（需 TEMPORAL_ADDRESS）
