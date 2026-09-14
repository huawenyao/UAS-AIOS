# ADR-SEL-002：Agent 双环

## Status
Accepted · 2026-09-09 · harness 回写 2026-09-10

## Context
T1 要求不自研第三套循环。2026 年循环框架换皮快，耐久执行与协议会留下。

## Decision
1. **控制面自有** Capability Hub  
2. **外环** Temporal：`RuntimeCycleWorkflow`，HITL、续跑、Saga  
3. **内环默认** LangGraph 1.0，经 InnerLoop SPI  
4. Codex/Pi 仅同一 SPI 备选；`INNERLOOP_BACKEND` 二选一；测试矩阵只跑一套  
5. 工具只经 MCP Gateway / `hub.instance.invoke_cs`  
6. 跨岗位 P0=`task.transfer`，P1+=A2A；忽略 ACP

## Consequences
- Worker 不持 SoR 密钥；Workflow 内禁止非确定性 LLM（必须 Activity）
- 禁止 CrewAI / AutoGen / Dify Agent / 厂商 Assistants 当 OS
- 落地：`UAS_AIOS_MODULE_DESIGN.md` M18/M19
