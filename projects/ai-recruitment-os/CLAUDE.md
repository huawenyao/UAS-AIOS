# AI 全流程招聘智能 OS

## 系统概述

本项目采用“蜂群智能体 + 三维理念现实 + 演化守恒”范式，目标是构建一个可运转、可评估、可迭代、可进化的招聘智能操作系统。

## 核心命令

- `/recruit-os [议题]` - 发起招聘智能 OS 方案生成
- `/instantiate [议题ID]` - 把方案映射成真实招聘实体与工作对象
- `/validate [议题ID]` - 执行交叉验证、偏差校验与指标评估
- `/evolve [议题ID]` - 基于验证反馈重构方案与智能体协作

## 工作原则

1. 目的守恒：任何实现都不得偏离基础招聘目标
2. 三维一致：宏观战略、中观流程、微观对象必须相互闭环
3. 现实实体优先：所有抽象结论都必须映射为招聘中的真实对象、流程、接口与角色
4. 演化开发：先形成最小闭环，再基于验证结果迭代，而不是一次性静态设计

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/workflow_config.json` | 招聘 OS 工作流定义 |
| `configs/swarm_agents.json` | 招聘智能体群角色定义 |
| `configs/evolution_policy.json` | 目标守恒与偏差控制策略 |
| `.claude/skills/recruitment_os_protocol.md` | 执行协议 |
| `.claude/skills/recruitment_output_contract.md` | 输出契约 |
| `docs/RECRUITMENT_OS_BLUEPRINT.md` | 产品与架构蓝图 |

## 运行产物

- `reports/`：Markdown 方案与迭代建议
- `database/`：结构化 JSON 记录
