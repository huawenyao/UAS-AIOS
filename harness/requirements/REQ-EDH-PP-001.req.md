# Requirement: REQ-EDH-PP-001 - 客服岗位 Agent 标杆（P1）



## Status: completed



## 需求层级: 产品



## 优先级: P0



## Acceptance Criteria



- [x] BusinessAgentRoster 配置：客服 Agent 1 个

- [x] 绑定 cs.ticket + cs.customer + cs.escalate（`cs.ticket.escalate`）

- [x] Task Panel 展示任务态（非仅日志）

- [x] 对标 `docs/strategic/demo/ΠPaw_Enterprise_Demo.html` 能力叙事



## 映射能力



PP-01 · PP-03 · Phase-0 ΠPaw P1



## 交付物



| 类型 | 路径 |

|------|------|

| Schema | `schemas/business_agent_roster.schema.json`, `schemas/task_panel_view.schema.json` |

| 配置 | `configs/pipaw_business_agent_roster.json`, `configs/pipaw_cs_agent_playbook.json` |

| 运行时 | `asui-cli/src/asui/pipaw_task_panel.py`, `asui-cli/src/asui/pipaw_cs_agent.py` |

| 规格 | `harness/knowledge/technical/pipaw-cs-agent-benchmark.md` |

| 校验 | `scripts/validate_pipaw_cs_agent.py` |



## 验证



```bash

python scripts/validate_pipaw_cs_agent.py validate

python harness/invariants/run-all.py

```

