# 演化回写协议

## 技能定位

本协议定义如何将 evolution 产出的 suggestions 回写到知识资产（configs、skills），实现业务层无限进化。需在 governance 允许下执行，支持人工确认。

## 可回写的 Suggestion 类型

| 类型 | 目标路径 | 需人工确认 | 说明 |
|------|----------|------------|------|
| `config_workflow` | configs/workflow_config.json | 是 | 工作流步骤调整 |
| `config_swarm` | configs/swarm_agents.json | 是 | Agent 角色/使命调整 |
| `config_evolution` | configs/evolution_policy.json | 是 | 演化策略调整 |
| `skill_add` | .claude/skills/{name}.md | 是 | 新增技能文件 |
| `skill_update` | .claude/skills/{name}.md | 是 | 更新技能内容 |
| `prompt_refine` | workflow step prompt_template | 否（低风险） | 仅 prompt 微调 |

## 回写流程

1. **收集**：从 cognitive_state.evolution.suggestions 或 database/feedback 读取
2. **分类**：按类型解析，提取 target_path、content、diff
3. **审批**：高风险类型需用户确认或 governance 规则通过
4. **执行**：写入目标路径，保留备份（database/evolution_backups/）
5. **审计**：记录到 database/audit/evolution_writeback.jsonl

## /evolveApply 命令语义

执行 `/evolveApply [topic]` 时：

1. 加载 cognitive_state/{topic_slug}.json 的 evolution.suggestions
2. 加载 database/feedback/{topic_slug}.json（若存在）作为用户修正
3. 合并为待应用列表
4. 按类型逐项应用（需确认的项先提示）
5. 写回后清空 evolution.suggestions 中已应用项

## 备份与回滚

- 每次回写前：复制目标文件到 database/evolution_backups/{timestamp}_{filename}
- 支持 `/evolveRollback [topic]` 从最近备份恢复

## 禁忌

- 禁止未经 governance 或用户确认修改 configs
- 禁止覆盖 evolution_policy 中的 require_validation_before_evolution
- 禁止删除已有 skill 文件（仅允许新增或更新）
