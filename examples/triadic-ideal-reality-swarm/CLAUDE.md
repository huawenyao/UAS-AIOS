# 三维理念现实涌现智能体群（UAS SubApp）

## 系统概述

本项目是 **UAS 平台 SubApp**，技术底座为 **ASUI**，运行时为 **autonomous_agent**。当前实现“宏观 / 中观 / 微观”与“理念 / 现实”的涌现蜂群；按 [docs/UAS_SUBAPP_建设规划.md](docs/UAS_SUBAPP_建设规划.md)，将扩展为**智能全链路闭环**（渠道洞察→智能选品→内容生成→自动投放→效果优化→数据复盘）与智能驱动数据全流通。

## 核心命令

- `/emerge [议题]` - 发起完整的三维理念现实涌现分析
- `/instantiate [议题ID]` - 把理念结构映射成现实实体
- `/validate [议题ID]` - 执行交叉验证与评估
- `/evolve [议题ID]` - 基于反馈进化方案

## 工作流

1. **议题归一化** - 明确场景、边界、目标对象与期望涌现结果
2. **目的激活** - 提炼基础目的并识别场景激活条件
3. **三维拆解** - 六个智能体并行输出理念 / 现实报告
4. **理念现实对冲** - 三组维度完成内部校正与跨维度校正
5. **现实实例化** - 把抽象结构映射成具体的人、物、流程与接口
6. **交叉验证** - 检查三维一致性、可执行性、可评估性
7. **涌现进化** - 生成《三维理念现实涌现方案》
8. **结构化落盘** - 报告脚本写入 `database/emergence/` 与 `reports/`

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/platform_manifest.json` | UAS 平台清单（I,K,R,A,S,G,E,Π） |
| `configs/runtime_config.json` | 运行时、审计、回滚、人工检查点 |
| `configs/governance_policy.json` | 治理策略 |
| `configs/evolution_policy.json` | 演化策略与漂移规则 |
| `configs/system_registry.json` | 系统网格（渠道数据、广告平台、内容平台等） |
| `configs/workflow_config.json` | 三维涌现工作流定义（后续扩展六链路） |
| `configs/swarm_agents.json` | 智能体角色、维度、目的、实例化与验证对手盘 |
| `.claude/skills/triadic_protocol.md` | 三维理念现实执行协议 |
| `.claude/skills/emergence_output_contract.md` | 最终输出契约 |
