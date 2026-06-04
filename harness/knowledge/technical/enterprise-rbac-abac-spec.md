# RBAC/ABAC 与数据 Scope 规格（Phase-0）

> Schema：`schemas/enterprise_permission.schema.json` · 模板：`configs/enterprise_rbac_template.json`

## 权限判定流程

```
InvokeRequest
  → 1. tenant_id 匹配（否则 403）
  → 2. role ∈ allowed_operations（否则 403）
  → 3. operation.approval_level → L1/L2/L3 策略
  → 4. gates 清单自检（G1/G4/G6/G7）
  → 5. scope_rules 注入查询 filter
  → 6. 写审计 + 可选 ChangeSet
```

## 角色→能力矩阵（ACME 样例）

| 角色 | 轨道 | 典型 cs.* |
|------|------|-----------|
| role.employee | selfpaw | customer 读、lead.list、approval.submit |
| role.sales_rep | selfpaw | + qualify_lead、send_email |
| role.cs_agent | pipaw | ticket.*、notify.send_im |
| role.cs_lead | pipaw | + customer.query、process.escalate |
| role.compliance | shared | customer.query、approval.approve |

完整列表见 `configs/enterprise_rbac_template.json`。

## L1 / L2 / L3 与 Gate 映射

| 级别 | 含义 | Gates | 人工 | 典型 operation |
|------|------|-------|------|----------------|
| **L1** | 自动 | G1, G4 | 否 | get_profile, list, query |
| **L2** | 确认后 | G1, G4, G6 | 是 | ticket.create, send_email, process.start |
| **L3** | 禁止或双控 | G6, G7 | 是（双控） | approval.approve |

与 `configs/capability_registry.json` 中每条 `approval_level` 一致。

## 数据 Scope 与 cs.* 过滤

| scope type | 含义 | 适用轨道 |
|------------|------|----------|
| self | 仅本人数据 | selfpaw |
| dept | 本部门 | selfpaw |
| dept_tree | 部门及下级 | selfpaw 销售 |
| tenant | 租户内（按策略细分） | pipaw |
| project | 绑定 Project 资源边界 | 双轨 |

`scope_rules` 在 invoke 前合并进连接器查询参数，**不**交给 LLM 拼接 SQL。

## 权限变更审计（ChangeSet）

权限策略变更必须使用 `permissionChangeSet`：

```json
{
  "changeset_id": "pcs-001",
  "tenant_id": "t-acme-demo",
  "actor": "u-admin",
  "changes": [{ "op": "add_role_operation", "role_id": "role.sales_rep", "operation_ref": "cs.process.start" }],
  "gates_passed": ["G1", "G7"]
}
```

回写路径：`scripts/evolve_apply.py` 扩展（Phase-1）或企业治理 Console。

## 跨租户拒绝（Invariant）

见 `harness/acceptance/test_tenant_isolation_policy.py`：

- 用户上下文 `t-a` 调用 `tenant_id=t-b` → 拒绝  
- Agent `product_track=pipaw` 调用仅 selfpaw 授权 operation → 拒绝
