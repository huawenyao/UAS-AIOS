# 企业审计链规格（Phase-0）

> Schema：`schemas/audit_record.schema.json` · 策略样例：`configs/audit_policy.sample.json`

## 原则

1. **100% 覆盖** `cs.*` invoke（成功与拒绝）。  
2. `tenant_id` 必填；按租户分表/分桶。  
3. 敏感 input 存 `input_hash`，不存明文 PII。  
4. SelfPaw / ΠPaw 分 `product_track` 字段，便于合规导出。

## 事件类型

| event_type | 触发点 |
|------------|--------|
| capability.invoke | POST /capability/invoke 完成 |
| capability.denied | 权限/租户/Gate 拒绝 |
| permission.changeset | RBAC 策略变更 |
| intent.escalate | SelfPaw → ΠPaw 升级 |
| agent.session | 会话起止（可选） |
| outward.message | Outward Gateway 对外消息 |

## 查询 API 草案

`GET /api/v1/audit?tenant_id=&from=&to=&event_type=&actor_user_id=`

## 与 capability invoke 联动

每次 invoke 响应中的 `audit_id` 对应一条 `audit_record`，`gates_evaluated` 来自 registry + rbac。

## Phase-0 出口

- [x] 记录 schema  
- [ ] 持久化实现（JSONL 按租户目录）  
- [ ] Console 审计页（ΠPaw Demo 扩展）
