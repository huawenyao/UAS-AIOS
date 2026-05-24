# 企业语义能力服务协议（cs.* Capability Service）

> **版本** 1.0  
> **父文档**：[ENTERPRISE_DIGITAL_HUMAN_L1_L3_ECOSYSTEM.md](./ENTERPRISE_DIGITAL_HUMAN_L1_L3_ECOSYSTEM.md)

---

## 一、设计原则

1. **Agent 只见语义，不见系统**：禁止在 Agent 工具列表中出现 `salesforce.createLead` 等厂商 API；统一为 `cs.lead.create`。  
2. **平台统一横切**：每次调用必经权限（scope）、审计（audit_id）、幂等（idempotency_key）、重试与死信。  
3. **确定性终裁**：涉及资金、合同、权限的 `cs.*` 必须声明 `execution_mode: deterministic`，LLM 输出不得作为唯一输入。  
4. **可演化**：能力版本 `capability_version` 与法则包 `policy_bundle_id` 绑定，支持回放与 ChangeSet。

---

## 二、命名规范

```
cs.<domain>.<verb>
```

| 域（domain） | 示例动词 | 说明 |
|--------------|----------|------|
| `lead` | capture, qualify, assign | 线索 |
| `customer` | get, upsert, search | 客户主数据 |
| `quote` | create, revise, submit | 报价 |
| `approval` | submit, signal, withdraw | 审批（常桥接 BPM） |
| `invoice` | issue, cancel, reconcile | 发票 |
| `case` | open, update, close | 工单/客服 |
| `workflow` | start, signal, status | 流程引擎 |
| `form` | render, submit | 表单 |
| `compliance` | review, attest | 合规 |
| `analytics` | attribute, query_kpi | 经营分析 |
| `mdm` | resolve, link | 主数据 |

---

## 三、调用契约（OpenAPI 风格摘要）

### 3.1 请求信封

```json
{
  "capability": "cs.quote.create",
  "capability_version": "2026-05-1",
  "tenant_id": "t_acme",
  "actor": {
    "user_id": "u_001",
    "roles": ["sales_rep"],
    "tier": "DH-L1",
    "delegation_from": null
  },
  "idempotency_key": "uuid",
  "policy_bundle_id": "credit_policy_v3",
  "payload": { },
  "evidence_refs": ["intent_id", "memo_id"]
}
```

### 3.2 响应信封

```json
{
  "request_id": "uuid",
  "status": "ok",
  "data": { },
  "audit_id": "audit_uuid",
  "side_effects": ["cs.approval.submit"],
  "escalation": null
}
```

失败时：

```json
{
  "request_id": "uuid",
  "status": "error",
  "code": "POLICY_DENIED",
  "message": "信用额度不足",
  "audit_id": "audit_uuid",
  "escalation": { "target": "DH-L2:finance", "reason": "credit_override" }
}
```

---

## 四、与 S-Grid（System Mesh）的映射

```
Agent 调用 cs.quote.create
    → UAS ToolGateway / CsRouter
        → 查 enterprise_cs_capability_registry
        → G: scope + 白名单校验
        → 适配器: projects/<tenant>/adapters/salesforce_quote.py
        → 写 audit + 事件流
        → 返回响应信封
```

`system_registry.json` 中 **systems** 条目仅作为 **cs 实现后端**，字段建议：

```json
{
  "id": "backend_salesforce",
  "implements": ["cs.lead.capture", "cs.customer.upsert"],
  "type": "crm",
  "mode": "adapter",
  "never_expose_to_agent": true
}
```

---

## 五、执行模式

| execution_mode | 含义 | 典型 capability |
|----------------|------|-----------------|
| `deterministic` | 规则/引擎终裁，LLM 仅辅助 | approval, invoice, compliance.review |
| `assisted` | LLM 生成草案，平台校验后写入 | quote.create（草稿）, case.update |
| `generative` | LLM 主导，无资金副作用 | 话术建议、邮件代拟 |

---

## 六、Agent 工具白名单

岗位 Agent 包中声明：

```json
{
  "agent_id": "pipaw_sales_advisor",
  "allowed_capabilities": [
    "cs.lead.qualify",
    "cs.quote.create",
    "cs.customer.search"
  ],
  "denied_capabilities": ["cs.invoice.issue"]
}
```

Runtime 在 `ToolGateway.execute` 前校验；违反则 `POLICY_DENIED` 并写审计。

---

## 七、实现状态

| 项 | 状态 |
|----|------|
| 协议文档 | ✅ 本文 |
| 示例注册表 | ✅ `configs/enterprise_cs_capability_registry.example.json` |
| CsRouter / 统一网关 | ❌ 规划（当前为 per-subapp script 网关） |
| 跨 subapp 租户审计 | ❌ 规划 |

---

*能力卡片与目录生命周期见 [ENTERPRISE_CS_CAPABILITY_CATALOG_STANDARD.md](./ENTERPRISE_CS_CAPABILITY_CATALOG_STANDARD.md)。扩展 cs 域时，先更新注册表与法则包，再发布 `capability_version` 变更说明。*
