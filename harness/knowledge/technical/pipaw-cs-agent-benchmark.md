# ΠPaw 客服岗位 Agent 标杆（REQ-EDH-PP-001 / Phase-0 P1）

> Roster：`configs/pipaw_business_agent_roster.json`  
> SOP：`configs/pipaw_cs_agent_playbook.json`  
> Task Panel：`asui-cli/src/asui/pipaw_task_panel.py`  
> 运行时：`asui-cli/src/asui/pipaw_cs_agent.py`  
> 原型对标：`docs/strategic/demo/ΠPaw_Enterprise_Demo.html`

## 标杆 Agent

| 字段 | 值 |
|------|-----|
| agent_id | `agent.cs_specialist` |
| 岗位 | `pos-cs-agent` / `role.cs_agent` |
| 对外 | 是（Outward + IM，Phase-1 接 Gateway） |
| Domain | `domain.customer_service` |

## 能力绑定（叙事 → cs.*）

| 产品叙事 | operation_ref |
|----------|----------------|
| cs.customer | `cs.customer.get_profile` |
| cs.ticket | `cs.ticket.create` |
| cs.escalate | `cs.ticket.escalate` |

Agent **禁止**直连 CRM/ITSM（ADR-EDH-002），一律经 `CapabilityServiceRouter`。

## Task Panel 任务态（非日志）

对齐 Demo **待办任务** 与 **【当前任务】执行区**：

| 字段 | 用途 |
|------|------|
| `status` | open / in_progress / blocked / done |
| `display_phase` | backlog / current / completed |
| `steps[]` | SOP 步骤：done / current / operation_ref |
| `sla_label` | 如「剩余时间：今日内」 |
| `actions[]` | 处理 / 完成步骤 / 升级 |

## 端到端场景（验收）

```
SelfPaw 客诉 Intent (business_outward + Evidence)
  → POST /intent/escalate
  → Working Task (pipaw / pos-cs-agent)
  → Task Panel backlog
  → 客服 Agent open → current + in_progress
  → 步骤1 cs.customer.get_profile
  → 步骤2 cs.ticket.create
  → 可选 cs.ticket.escalate
```

## CLI

```bash
python scripts/validate_pipaw_cs_agent.py validate
python scripts/escalate_intent.py escalate
python scripts/pipaw_task_panel.py show --open-task <task_id>
```

## 与产品定义对齐

- `Enterprise_Digital_Human_Ecosystem_Product_Definition.md` §6.3 客服 Agent、§6.6 P1 单岗位标杆  
- Sprint `sprint-edh-001` 项 6 PP-001
