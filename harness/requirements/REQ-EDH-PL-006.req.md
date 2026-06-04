# Requirement: REQ-EDH-PL-006 - 事件总线与审计链

## Status: completed

## 需求层级: 平台

## 优先级: P0

## Acceptance Criteria

- [x] 企业事件命名规范（见 audit_record.event_type 枚举）
- [x] 每次 cs.* 调用审计字段定义（audit_record.schema + capability API 草案）
- [x] 审计查询 API 草案（enterprise-audit-chain-spec.md）
- [x] 对外通道审计字段预留（event_type: outward.message）

## 映射能力

PL-06

## Files Involved

- `schemas/audit_record.schema.json`
- `configs/audit_policy.sample.json`
- `harness/knowledge/technical/enterprise-audit-chain-spec.md`
