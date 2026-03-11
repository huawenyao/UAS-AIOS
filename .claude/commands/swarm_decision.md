# /swarmDecision 命令

## 功能

启动 SelfPaw 蜂群认知智能体工作流，基于否定之否定辩证升维方法论，对用户决策议题进行全维度洞察。

## 用法

```
/swarmDecision [决策议题]
```

或带上下文：

```
/swarmDecision [决策议题] | 背景：[背景信息]
```

## 示例

```
/swarmDecision 是否接受某创业公司的技术总监 offer
```

```
/swarmDecision 是否在Q2投入资源做新产品线 | 背景：当前团队10人，已有3条产品线在维护
```

## 执行流程

1. **第一阶段（初次否定）**：并行调用五智能体
   - 用户视角智能体 → 用户真实需求报告
   - 关卡障碍智能体 → 关卡与风险清单
   - 核心决策智能体 → 初始决策方案
   - 买单价值智能体 → 价值与成本评估
   - 博弈观察智能体 → 外部博弈格局

2. **第二阶段（二次否定）**：认知对手盘博弈
   - 各智能体按对手盘矩阵相互质询
   - 信息补全、修正片面性
   - 博弈观察智能体中立统筹

3. **第三阶段（辩证融合）**：智能涌现
   - 整合各智能体合理内核
   - 输出《全维度辩证决策方案》
   - 持久化到 database/swarm_decisions.json

## 知识引用

- `.claude/skills/swarm_methodology.md` - 方法论
- `.claude/skills/agent_opponent_matrix.md` - 对手盘矩阵
- `.claude/agents/01_user_perspective.md` ~ `05_game_observer.md` - 智能体定义
- `configs/swarm_workflow_config.json` - 工作流配置

## 输出

- 结构化 JSON：《全维度辩证决策方案》
- 持久化：database/swarm_decisions.json
- 可审计：evidence_chain 包含每项结论的辩证依据
