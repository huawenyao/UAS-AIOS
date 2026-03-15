# /createSubApp 命令

## 功能

触发 Agent 自主生产 UAS sub app。基于 command + agent skill 模式，Agent 加载生产协议与输出契约，完成从意图归一化到资产生成、校验注册的全流程。

## 语法

```
/createSubApp <业务描述> [选项]
```

## 选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--template` | 模板类型：uas-subapp, selfpaw-swarm, triadic-ideal-reality-swarm | 由 Agent 根据意图推断 |
| `--target` | 目标根目录：projects 或 examples | projects |
| `--name` | 子应用 ID（slug，如 ai-recruitment-os） | 由业务描述生成 |
| `--force` | 覆盖已存在的目录/文件 | false |
| `--dry-run` | 仅输出方案 JSON，不生成文件 | false |

## 示例

```
/createSubApp 跨境电商选品助手，支持多平台数据聚合与智能推荐
/createSubApp 招聘流程自动化 --template uas-subapp --target examples
/createSubApp 三维理念现实分析 --template triadic-ideal-reality-swarm
/createSubApp 多角色博弈决策 --template selfpaw-swarm --dry-run
```

## 执行流程

1. **加载技能**：读取 `.claude/skills/subapp_producer_protocol.md`、`subapp_output_contract.md`、`subapp_template_selector.md`
2. **意图归一化**：将业务描述转为结构化意图（目标、约束、对象、成功标准）
3. **模板选择**：根据意图或 `--template` 选择模板
4. **方案设计**：生成符合 output_contract 的完整方案 JSON
5. **资产生成**：调用 `python3 scripts/create_sub_uas_app.py <name> --target <target> --template <template>`
6. **定制写入**：根据方案覆盖/补充 configs、skills、docs
7. **校验**：执行 `python3 scripts/run_uas_runtime_service.py validate --app-id <name>`
8. **反馈**：输出生产报告与下一步建议

## 禁忌

- 禁止生成无 governance 配置的 sub app
- 禁止生成无 evolution 回路的 sub app
- 禁止在未指定 `--force` 时覆盖已有项目
