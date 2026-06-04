# Requirement: REQ-EDH-BASE-001 - 数字人生态 reqharness 项目基线

## Status: completed

## 需求层级: 基线

## 优先级: P0

## 问题描述

- **Who**: UAS-AIOS 数字人生态项目组
- **When/Where**: Phase-0 启动前
- **What Problem**: 缺少 harness 世界模型，需求/实体/知识/验证无法闭环
- **Why**: reqharness 要求知识驱动 + 目标驱动 + Invariant 验证

## Acceptance Criteria

- [x] `harness/state.json` 定义项目、模块、sprint、指标
- [x] `harness/entity-map.json` 定义核心实体与依赖规则
- [x] `harness/knowledge/index.yaml` 与 product/technical/domain/constraints 知识源
- [x] Phase-0 需求 REQ-EDH-PL/SP/PP/K 已登记
- [x] `harness/invariants/run-all.py` 可执行且基线 Invariant 通过
- [x] 战略文档在 state.project.strategic_docs 中可追溯

## Derived from

`/reqharness 创建数字人生态项目基线`
