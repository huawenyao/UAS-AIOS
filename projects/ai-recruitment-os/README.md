# AI Recruitment OS

基于蜂群智能体与三维理念现实智能体群的独立招聘智能 OS 项目。

## 项目目标

构建一个从用工目标到入职回流的 AI 全流程招聘操作系统，并用目标守恒、偏差校验、交叉验证、迭代进化机制避免方案失真。

## 快速开始

1. 阅读 `CLAUDE.md`
2. 查看 `configs/workflow_config.json` 与 `configs/swarm_agents.json`
3. 参考 `docs/RECRUITMENT_OS_BLUEPRINT.md`
4. 用 `scripts/render_recruitment_plan.py` 生成结构化方案
5. 用 `scripts/evaluate_iteration.py` 检查目标偏差并产出进化建议

## 目录结构

```text
ai-recruitment-os/
├── CLAUDE.md
├── .claude/
│   ├── agents/
│   ├── commands/
│   └── skills/
├── configs/
├── docs/
├── scripts/
├── database/
└── reports/
```
