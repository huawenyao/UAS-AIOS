# Requirement: REQ-EDH-K-001 - UAS Runtime 与 subapp 健康基线

## Status: completed

## 需求层级: 内核

## 优先级: P0

## Acceptance Criteria

- [x] `run_uas_runtime_service.py list` 可发现 ai-recruitment-os
- [x] health/validate 通过
- [x] 数字人生态 subapp 模板（招聘外）脚手架 1 个：`projects/enterprise-sales-os/`
- [x] subapp manifest 声明 cs.* 依赖占位（`capability_dependencies`）

## Files Involved

- `scripts/run_uas_runtime_service.py`
- `projects/ai-recruitment-os/`
