# cs.* 能力服务目录基线（Phase-0）

> Agent **禁止**直连 CRM/BPM；一律调用语义能力服务。

## 命名规范

```
cs.{domain}.{action}
```

## Phase-0 最小目录（≥5）

| ID | 服务 | 操作示例 | 来源系统 | 优先级 |
|----|------|----------|----------|--------|
| CS-01 | cs.customer | query, get_profile | CRM | P0 |
| CS-02 | cs.lead | qualify_lead, list | CRM | P0 |
| CS-03 | cs.ticket | create, update_status, escalate | ITSM/客服 | P0 |
| CS-04 | cs.approval | submit, approve, reject | BPM/OA | P0 |
| CS-05 | cs.notify | send_im, send_email | OA/IM | P0 |
| CS-06 | cs.calendar | list_events, create_event | OA | P1 |
| CS-07 | cs.expense | submit_report | 财务 | P1 |
| CS-08 | cs.invoice | create, status | 财务 | P1 |
| CS-09 | cs.process | start, advance, escalate | BPM | P0 |
| CS-10 | cs.opportunity | create_quote | CRM | P1 |

## 契约字段（每条 operation）

```yaml
name: qualify_lead
input_schema: { lead_id, criteria_ref }
output_schema: { qualified, score, evidence[] }
gates: [G6, G4]
approval_level: L1 | L2 | L3
side_effects: [event.lead.qualified]
audit: required
```

## 注册中心职责

- 契约版本与兼容  
- 租户级启用/禁用  
- 角色→operation 权限映射  
- 调用审计与重试策略  

## 与 SelfPaw Tools 关系

Skills/Tools 封装为 **cs.* 客户端**，不暴露原始 REST 路径给 LLM。
