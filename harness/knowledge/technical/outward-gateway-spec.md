# Outward Gateway 规格（REQ-EDH-PP-002）

> **status**: draft · Phase-0 · ADR-EDH-001：仅 ΠPaw 可注册对外通道

## 统一入口

- **Webhook**：`POST /v1/outward/webhook/{channel_id}`
- **会话绑定**：Header `X-Tenant-Id` + Body `session_id` → 租户上下文

## 路由表（草案）

| channel_id | 类型 | 默认岗位 Agent |
|------------|------|----------------|
| `feishu_im` | IM | `ppaw_cs_agent` |
| `wecom_im` | IM | `ppaw_cs_agent` |
| `email_inbound` | email | `ppaw_sales_advisor` |

配置样例：`configs/outward_gateway_routes.sample.json`（待 Phase-1 实现 HTTP 服务）

## 审计与 PII

- 全量会话写入 `audit_record`（见 `enterprise-audit-chain-spec.md`）
- PII 字段：`contact_phone`, `contact_email`, `id_card` → 存储前 `mask(pii_policy)`

## 验收

- 文档级 AC 满足 Phase-0
- HTTP 服务归属 Phase-1（`capability-service-registry-api.md` 下半程）
