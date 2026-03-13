# AI Recruitment OS

一个完全按 `UAS-Platform = (I, K, R, A, S, G, E, Π)` 标准生成的 sub uas app，面向 AI 全流程招聘场景。

## 项目目标

构建一个从用工目标到入职回流的招聘闭环操作系统，并以：

- `ASUI` 作为默认技术底座
- `autonomous_agent runtime` 作为默认运行时
- 目标守恒 / 审计治理 / 演化回路 作为内建机制

来避免目标损失和效果偏差。

## 快速开始

1. 阅读 `CLAUDE.md`
2. 查看 `configs/platform_manifest.json`
3. 查看 `configs/workflow_config.json` 与 `configs/swarm_agents.json`
4. 参考 `docs/APP_BLUEPRINT.md`、`docs/RECRUITMENT_OS_BLUEPRINT.md`
5. 运行：

```bash
python3 scripts/run_subapp.py "AI全流程招聘智能OS"
python3 scripts/run_subapp.py "AI全流程招聘智能OS" --evaluate
```

## 平台标准资产

- `configs/platform_manifest.json`
- `configs/runtime_config.json`
- `configs/governance_policy.json`
- `configs/evolution_policy.json`
- `configs/system_registry.json`
- `configs/workflow_config.json`
- `configs/swarm_agents.json`

## 项目目录

```text
ai-recruitment-os/
├── CLAUDE.md
├── .claude/
├── configs/
├── docs/
├── scripts/
├── database/
└── reports/
```
