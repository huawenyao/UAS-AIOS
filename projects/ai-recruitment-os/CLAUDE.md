# AI 全流程招聘智能 OS

## 系统概述

本项目是一个基于 `UAS-Platform = (I, K, R, A, S, G, E, Π)` 标准生成的 sub uas app。

默认平台约束：

- 技术底座默认采用 `ASUI`
- 运行架构默认采用 `autonomous_agent runtime`
- 所有业务实现都必须满足：目标驱动 + 知识驱动 + Agent 协作 + 系统执行 + 审计治理 + 演化闭环

## 核心命令

- `/intent [议题]` - 归一化招聘业务目标与场景
- `/design [议题ID]` - 生成招聘智能 OS 方案
- `/validate [议题ID]` - 进行偏差校验与评估
- `/evolve [议题ID]` - 生成下一轮进化建议

## 工作原则

1. 目的守恒：任何实现都不得偏离基础招聘目标
2. 三维一致：宏观战略、中观流程、微观对象必须相互闭环
3. 现实实体优先：所有抽象结论都必须映射为招聘中的真实对象、流程、接口与角色
4. 演化开发：先形成最小闭环，再基于验证结果迭代，而不是一次性静态设计
5. 平台一致：所有实现都必须满足 UAS 平台标准资产、标准阶段与标准治理能力

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/platform_manifest.json` | UAS 平台清单与标准约束 |
| `configs/runtime_config.json` | autonomous_agent runtime 配置 |
| `configs/governance_policy.json` | 审计治理与权限策略 |
| `configs/evolution_policy.json` | 目标守恒与偏差控制策略 |
| `configs/system_registry.json` | 招聘场景系统接入清单 |
| `configs/workflow_config.json` | 招聘 OS 标准工作流 |
| `configs/swarm_agents.json` | 招聘智能体群角色定义 |
| `.claude/skills/platform_protocol.md` | 平台标准协议 |
| `.claude/skills/output_contract.md` | 平台输出契约 |
| `.claude/skills/recruitment_os_protocol.md` | 招聘领域执行协议 |
| `.claude/skills/recruitment_output_contract.md` | 招聘领域输出契约 |

## 运行产物

- `reports/`：Markdown 方案与迭代建议
- `database/`：结构化 JSON 记录
- `database/audit/`：运行时审计日志
