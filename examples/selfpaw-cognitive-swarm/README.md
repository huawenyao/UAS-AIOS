# selfpaw 原生认知蜂群 - ASUI 验证项目

## 验证目标

验证 ASUI 在“多智能体认知对冲 + 辩证融合决策”场景下的适用性：

- 五大智能体独立建模
- 否定之否定的两轮升维
- 可审计的《全维度辩证决策方案》输出

## 快速开始

1. 在 Cursor/Claude Code 中打开本项目
2. 对 AI 说：`/dialectic 议题：是否推出面向中小商家的订阅版产品？`
3. AI 将加载 `CLAUDE.md`、`configs/workflow_config.json`、`configs/swarm_agents.json` 与 `.claude/skills/`
4. 执行完成后，蜂群结论会被写入 `database/decisions/` 与 `reports/`

## 验证清单

| 验证项 | 方法 | 预期 |
|--------|------|------|
| 知识驱动 | 调整 `configs/swarm_agents.json` 的立场或对手盘 | 下次辩证自动采用新关系 |
| 构建即运行 | 修改 `workflow_config.json` 的阶段或输出契约 | 无需改脚本即可改变蜂群流程 |
| 结构化输出 | 执行 `scripts/render_decision.py` | 生成 JSON 与 Markdown 决策报告 |
| 可审计 | 查看 `database/decisions/*.json` 与 `reports/*.md` | 保留博弈与融合结果 |

## 项目结构

```
selfpaw-cognitive-swarm/
├── CLAUDE.md
├── configs/
│   ├── workflow_config.json
│   └── swarm_agents.json
├── .claude/skills/
│   ├── swarm_protocol.md
│   └── decision_output_contract.md
├── scripts/render_decision.py
├── database/          # 运行时生成决策 JSON
└── reports/           # 运行时生成 Markdown 报告
```
