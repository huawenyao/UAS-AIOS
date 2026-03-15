# /evolveApply 命令

## 功能

将 evolution 产出的 suggestions 及用户反馈回写到知识资产（configs、skills），实现业务层无限进化。需在 governance 允许下执行。

## 语法

```
/evolveApply [topic] [选项]
```

## 选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--app-id` | 目标 sub app ID | 当前项目 |
| `--dry-run` | 仅输出待应用项，不实际写入 | false |
| `--auto` | 自动应用低风险项，高风险项仍需确认 | false |

## 执行流程

1. **加载**：cognitive_state/{topic_slug}.json 的 evolution.suggestions
2. **合并**：database/feedback/{topic_slug}.json（若存在）作为用户修正
3. **分类**：按 evolution_writeback_protocol 解析类型与目标路径
4. **确认**：高风险项（config、skill）需用户确认
5. **回写**：备份 → 写入 → 审计
6. **清理**：已应用项从 suggestions 中移除

## 前置条件

- 必须先执行过带 `--evaluate` 的 run，或 evolution_plan 步骤已产出 suggestions
- 建议先运行 `/evolveApply [topic] --dry-run` 查看待应用项

## 参考

- `.claude/skills/evolution_writeback_protocol.md`
