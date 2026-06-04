# 能力服务注册中心 API 草案（Phase-0）

> 实现状态：契约已冻结（schema + registry）；HTTP 服务待 Phase-0 下半程。  
> 配置：`configs/capability_registry.json` · Schema：`schemas/capability_service.schema.json`

## 设计原则

1. Agent 工具层只暴露 **`{service_id}.{operation}`** 语义名（如 `cs.lead.qualify_lead`），禁止下游 URL。  
2. 每次 `invoke` 写入审计链（REQ-EDH-PL-006）。  
3. 调用前校验：租户启用、角色权限、L1/L2/L3、Gate 清单。

## 资源模型

| 资源 | 说明 |
|------|------|
| `CapabilityService` | `cs.{domain}` 服务定义 |
| `CapabilityOperation` | 服务下原子操作 |
| `InvokeRequest` | 一次调用上下文 |
| `AuditRecord` | 审计记录 |

## HTTP API（草案 v0）

Base: `/api/v1/capability`

### GET /services

列出已注册能力服务（可按 `enabled`、`domain` 过滤）。

**Response 200**

```json
{
  "registry_id": "edh-platform-default",
  "version": "1.0.0",
  "services": [
    {
      "id": "cs.lead",
      "domain": "lead",
      "operation_count": 2,
      "agent_visible_operations": ["qualify_lead", "list"]
    }
  ]
}
```

### GET /services/{service_id}/operations

返回某服务全部 operation 契约（供 Console / Agent 工具注册）。

### POST /invoke

执行能力调用（核心路径）。

**Request**

```json
{
  "operation_ref": "cs.lead.qualify_lead",
  "tenant_id": "t-001",
  "caller": {
    "type": "agent",
    "agent_id": "pipaw.cs.agent",
    "user_id": "u-42",
    "session_id": "s-abc"
  },
  "input": {
    "lead_id": "L-1001",
    "criteria_ref": "default_b2b"
  },
  "idempotency_key": "optional-uuid"
}
```

**Response 200**

```json
{
  "status": "ok",
  "output": {
    "qualified": true,
    "score": 0.82,
    "evidence": ["budget_confirmed", "decision_maker_identified"]
  },
  "audit_id": "aud-7f3a",
  "side_effects_emitted": ["event.lead.qualified"]
}
```

**Response 403** — 权限或 L3 拦截  
**Response 422** — Gate 或输入校验失败

### GET /audit

查询审计（`tenant_id`、`operation_ref`、`from`、`to`）。

## Agent 工具映射

| LLM Tool 名 | 映射 |
|-------------|------|
| `capability_invoke` | `POST /invoke`，参数仅 `operation_ref` + `input` |
| 禁止 | `crm_host`、`api_key`、`raw_path` 等连接器字段 |

SelfPaw Skills 实现模式：

```python
# 伪代码：工具描述从 registry 自动生成，不手写 URL
def tool_qualify_lead(lead_id: str, criteria_ref: str = "default"):
    return capability_client.invoke("cs.lead.qualify_lead", {...})
```

## CLI（已实现验证）

```bash
python scripts/validate_capability_registry.py list
python scripts/validate_capability_registry.py validate
```

## 与 UAS 八元组

| API | UAS |
|-----|-----|
| registry | S 层 System Grid |
| invoke 审计 | G 层 |
| 法则/审批 | G + Domain 认知包 |
| 事件 side_effects | E 层输入 |
