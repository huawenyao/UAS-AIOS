# Intent 与 Evidence 标准（EPS-06）

> **版本** 1.0 | **父标准**：[ENTERPRISE_PLATFORM_STANDARD.md](./ENTERPRISE_PLATFORM_STANDARD.md)

---

## 1. 设计目标

1. **责任可追溯**：从 DH-L1 升级到 DH-L2/L3 时，组织接力的是「责任与证据」，不是聊天记录。  
2. **机器可校验**：升级前检查 `escalation_rules.require` 字段。  
3. **合规可出示**：G6 人工决策可关联完整 Evidence，但 LLM 附件不视为法律依据。

---

## 2. Intent 单

### 2.1 完整 Schema

见 `configs/schemas/enterprise_intent.schema.json`。

### 2.2 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `intent_id` | ✅ | UUID |
| `tenant_id` | ✅ | 租户 |
| `tier_source` | ✅ | DH-L1 \| DH-L2 \| DH-L3 \| external |
| `actor` | ✅ | 同 cs 调用 actor |
| `intent_type` | ✅ | 枚举或租户扩展，如 `escalate_quote` |
| `goal` | ✅ | 自然语言目标（≤2k） |
| `constraints` | | 法则/区域/客户约束引用 |
| `escalation_target` | 升级时 ✅ | 如 `DH-L3:pipaw_sales_advisor` |
| `status` | ✅ | open \| escalated \| resolved \| cancelled |
| `parent_intent_id` | | 拆分/合并时 |
| `created_at` / `updated_at` | ✅ | ISO8601 |
| `linked_evidence_ids` | | Evidence 外键列表 |
| `planned_capabilities` | | Agent 计划调用的 cs（未执行） |
| `executed_capabilities` | | 已执行 cs 的 request_id 列表 |

### 2.3 intent_type 推荐枚举（B2B 销售）

| intent_type | 默认 escalation_target |
|-------------|------------------------|
| `escalate_quote` | DH-L3:pipaw_sales_advisor |
| `escalate_contract` | G6_human |
| `escalate_refund` | DH-L2:pipaw_finance |
| `sla_breach` | DH-L2:pipaw_scheduler |
| `compliance_redline` | G6_human |
| `personal_task` | 无（DH-L1 内闭环） |

---

## 3. Evidence 包

### 3.1 完整 Schema

见 `configs/schemas/enterprise_evidence_bundle.schema.json`。

### 3.2 组成块（可组合）

| 块 | 字段 | 用途 |
|----|------|------|
| 主数据引用 | `mdm_refs[]` | `{type, id}` 无 PII 全文 |
| cs 轨迹 | `cs_trace[]` | `{capability, request_id, status, summary}` |
| 蜂群备忘录 | `swarm_memo` | SelfPaw 五视角 JSON/Markdown ref |
| 推理链 | `reasoning_chain` | LLM 步骤（附件级） |
| 待核实项 | `open_questions[]` | 认识论谦卑 |
| 附件 | `attachments[]` | `{uri, mime, hash}` |

### 3.3 升级最小集

按 `enterprise_digital_human_tiers.example.json` 的 `escalation_rules.require`：

| require 值 | 必须包含 |
|------------|----------|
| `intent_record` | 完整 Intent 单 |
| `evidence_bundle` | evidence_id 可解析 |
| `swarm_memo_optional` | 有则传，无则标注 skipped |
| `cs_call_trace` | cs_trace 非空 |
| `full_reasoning_chain` | reasoning_chain + audit_id |

---

## 4. 状态机

### 4.1 Intent

```
open → escalated → resolved
  │         │
  └→ cancelled
```

### 4.2 ΠPaw Task（与 Intent 关联）

```
pending → in_progress → completed
              ↓
           blocked → escalated (G6)
```

---

## 5. API

```
POST   /v1/tenants/{tid}/intents
GET    /v1/tenants/{tid}/intents/{intent_id}
POST   /v1/tenants/{tid}/intents/{intent_id}/escalate
POST   /v1/tenants/{tid}/intents/{intent_id}/evidence
GET    /v1/tenants/{tid}/tasks?status=pending&target=DH-L3:*
```

---

## 6. 存储约定（R0 文件型）

```
database/
  intents/{intent_id}.json
  evidence/{evidence_id}.json
  tasks/{task_id}.json
```

---

## 7. 隐私与留存

| 数据 | 默认留存 | 脱敏 |
|------|----------|------|
| Intent.goal | 365d | 导出时掩码客户名 |
| reasoning_chain | 90d | 可选不入库，仅 object store |
| cs_trace | 与 audit 一致 | 仅 summary |

---

*JSON Schema：`configs/schemas/enterprise_intent.schema.json`*
