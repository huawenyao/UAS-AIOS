# Requirement: REQ-EDH-PL-003 - 能力服务注册中心

## Status: completed

## 需求层级: 平台

## 优先级: P0

## Acceptance Criteria

- [x] `schemas/capability_service.schema.json` 发布
- [x] `configs/capability_registry.json` 含 ≥5 条 cs.* 定义（当前 6 服务、14 operations）
- [x] 注册中心 API 草案：list / invoke / audit（见 `harness/knowledge/technical/capability-service-registry-api.md`）
- [x] Agent 工具层仅暴露 cs 语义名，不暴露下游 URL（API 草案 § Agent 工具映射）

## 映射能力

PL-03 · SP-04

## Files Involved

- `schemas/capability_service.schema.json`
- `configs/capability_registry.json`
- `scripts/validate_capability_registry.py`
- `harness/knowledge/technical/capability-service-catalog-baseline.md`
- `harness/knowledge/technical/capability-service-registry-api.md`

## Completed

2026-05-23 · reqharness continue sprint-edh-001
