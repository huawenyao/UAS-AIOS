# ADR-EDH-002：先能力服务化，再挂 Agent 岗位

## Status

Accepted · 2026-05-23

## Context

个人/公网 Agent 可直接调工具；企业场景需租户隔离、审批分级、主数据一致性与可审计性。直接让 LLM 调 CRM REST 将导致权限失控与不可追溯。

## Decision

1. Phase-0 **必须先** 交付：租户/权限/审计 + `cs.*` 注册中心 + ≥2 系统连接器。  
2. Agent（SelfPaw/ΠPaw）**仅允许** 调用 `CapabilityService` 语义操作，禁止生产库 Shell/裸 API。  
3. 岗位 Agent 编制（PP-01）在 CS-01..05 可用后方可上线标杆。  
4. 模型层与平台层分离：模型提议，平台执行（ASUI 原则）。

## Consequences

- 新增 `schemas/capability_service.schema.json` 为 P0 工件  
- SelfPaw Skills 重构为 cs 客户端  
- Invariant：`agent_no_raw_crm` 纳入 CI（后续）
