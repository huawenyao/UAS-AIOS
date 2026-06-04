# Requirement: REQ-EDH-PL-002 - RBAC/ABAC 与数据 Scope

## Status: completed

## 需求层级: 平台

## 优先级: P0

## Acceptance Criteria

- [x] 角色→能力服务 operation 权限矩阵模板：`configs/enterprise_rbac_template.json`
- [x] 数据 scope 与 cs.* 查询过滤规则：`scope_rules` + 规格文档
- [x] L1/L2/L3 与 Gate G6 映射表：`approval_gate_mapping`
- [x] 权限变更可审计（ChangeSet 模型于 `enterprise_permission.schema.json`）

## 映射能力

PL-02 · PP-07

## Files Involved

- `schemas/enterprise_permission.schema.json`
- `configs/enterprise_rbac_template.json`
- `harness/knowledge/technical/enterprise-rbac-abac-spec.md`
