# Requirement: REQ-EDH-SP-001 - SelfPaw 企业 SSO 与工作区

## Status: completed (prototype)

## 需求层级: 产品

## 优先级: P0

## Acceptance Criteria

- [x] 企业版与 C 端配置分离（Feature Flag）
- [x] 个人 Project 默认绑定租户与岗位 Domain
- [x] Console/API 租户上下文中间件草案
- [x] 满足 ADR-EDH-001 数据 scope

## 映射能力

SP-01

## 验证

`python scripts/validate_org_identity.py validate`
