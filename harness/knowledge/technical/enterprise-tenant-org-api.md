# 多租户与组织目录 API 草案（Phase-0）

> Schema：`schemas/enterprise_tenant.schema.json` · 样例：`configs/tenant_catalog.sample.json`

## 核心规则

1. **所有** API、cs.* invoke、审计记录必须携带 `tenant_id`。  
2. 跨租户 `tenant_id` 不匹配 → **403 TENANT_ISOLATION_VIOLATION**（见 acceptance 用例）。  
3. SSO 登录后构建 `EnterpriseUserContext` 注入 RuntimeContext（对齐 SelfPaw `aee/runtime_context.py`）。

## 组织目录同步

### POST /api/v1/tenants/{tenant_id}/directory/sync

从 IdP 增量同步（Phase-0 支持 **feishu mock**）。

**Request**

```json
{
  "provider": "feishu",
  "mode": "incremental",
  "since": "2026-05-22T00:00:00Z"
}
```

**Response**

```json
{
  "org_units_upserted": 12,
  "positions_upserted": 8,
  "users_upserted": 120
}
```

### GET /api/v1/tenants/{tenant_id}/directory/org-units

### GET /api/v1/tenants/{tenant_id}/directory/positions

## 用户上下文

### GET /api/v1/me/context

SSO 后返回企业用户上下文（写入 Runner）。

```json
{
  "tenant_id": "t-acme-demo",
  "user_id": "u-1001",
  "org_unit_id": "ou-sales",
  "position_id": "pos-sales-rep",
  "role_ids": ["role.sales_rep"],
  "product_track": "selfpaw",
  "data_scopes": [
    { "type": "self", "value": "u-1001" },
    { "type": "dept_tree", "value": "ou-sales" }
  ]
}
```

## RuntimeContext 扩展字段

| 字段 | 来源 |
|------|------|
| `tenant_id` | 租户 |
| `org_unit_id` | 组织目录 |
| `position_id` | 岗位 → `domain_id` |
| `role_ids` | RBAC |
| `product_track` | selfpaw \| pipaw |
| `data_scopes` | ABAC |

## 双轨对齐（ADR-EDH-001）

| product_track | 默认 data_scope | 对外通道 |
|---------------|-----------------|----------|
| selfpaw | self + dept / dept_tree | 否 |
| pipaw | tenant 或 role 限定 | 是（Outward Gateway） |
