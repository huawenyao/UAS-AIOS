# Requirement: REQ-EDH-PL-007 - CRM/OA 系统连接器（Phase-0 ≥2）

## Status: completed

## 需求层级: 平台

## 优先级: P0

## Acceptance Criteria

- [x] SystemConnector 适配器接口 `invoke(operation, payload, ctx)` — `asui/connectors/base.py`
- [x] CRM 连接器 mock：`cs.customer` / `cs.lead` — `mock_crm.py`
- [x] OA 连接器 mock：`cs.approval` / `cs.notify` — `mock_oa.py`
- [x] 连接器配置与密钥分区文档 — `configs/connectors.json` + `system-connector-spec.md`
- [x] 端到端路由：`CapabilityServiceRouter` + RBAC + 冒烟/ pytest

## 映射能力

PL-07

## Files Involved

- `schemas/system_connector.schema.json`
- `configs/connectors.json`
- `asui-cli/src/asui/connectors/`
- `scripts/validate_connectors.py`
- `scripts/invoke_capability.py`
- `asui-cli/tests/test_edh_connectors.py`
- `harness/knowledge/technical/system-connector-spec.md`
