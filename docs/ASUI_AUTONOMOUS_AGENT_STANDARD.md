# ASUI Autonomous Agent 技术架构标准

## 核心原则

ASUI 在 UAS 中不是可选范式，而是默认技术架构标准。

所有 UAS 业务应用都必须满足：

1. 显式知识驱动
2. 构建-运行一体化
3. autonomous_agent 运行
4. 结构化可审计
5. 可回滚
6. 可演化

## 标准分层

### Knowledge Layer

必须存在：

- `CLAUDE.md`
- `workflow_config.json`
- `swarm_agents.json`
- `governance_policy.json`
- `evolution_policy.json`
- `.claude/skills/`

### Runtime Layer

必须定义：

- `runtime_config.json`
- context injection
- task isolation
- permission model
- escalation path

### Execution Layer

必须提供：

- system registry
- render script
- evaluation script
- database / reports outputs

## 标准工作流阶段

1. `intent_activation`
2. `knowledge_binding`
3. `agent_planning`
4. `runtime_topology`
5. `system_mapping`
6. `governance_check`
7. `evolution_plan`
8. `render_report`

## 工具标准

### 渲染脚本

必须把方案写入：

- `reports/*.md`
- `database/**/*.json`

### 评估脚本

必须至少检查：

- 目标守恒
- 技术底座是否为 ASUI
- runtime 是否为 autonomous_agent
- 是否存在 governance controls
- 是否存在 evolution loop

## 推荐生成路径

推荐所有业务项目通过：

- `asui init <target> -t uas-subapp`

或：

- `python3 scripts/create_sub_uas_app.py <name>`

生成标准化 sub uas app。
