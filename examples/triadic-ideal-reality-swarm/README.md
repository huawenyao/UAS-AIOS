# 三维理念现实涌现蜂群 - ASUI 验证项目

## 验证目标

验证“三维 × 理念现实 × 目的激活”蜂群在复杂议题建模中的适用性：

- 宏观 / 中观 / 微观并行建模
- 理念与现实成对对冲
- 基础目的在具体场景中的激活
- 输出可审计的《三维理念现实涌现方案》

## 快速开始

1. 在 Cursor/Claude Code 中打开本项目
2. 对 AI 说：`/emerge 议题：如何把行业解决方案转化为真实工作方式？`
3. AI 将加载 `CLAUDE.md`、`configs/workflow_config.json`、`configs/swarm_agents.json` 与 `.claude/skills/`
4. 执行完成后，涌现结果会被写入 `database/emergence/` 与 `reports/`

## 验证清单

| 验证项 | 方法 | 预期 |
|--------|------|------|
| 三维建模 | 调整 workflow 中的宏观/中观/微观步骤 | 下次涌现自动采用新维度结构 |
| 理念现实对冲 | 修改 `swarm_agents.json` 的对手盘 | 输出自动反映新的对冲关系 |
| 目的激活 | 调整 `triadic_protocol.md` 的激活规则 | 生成结果随知识变化而变化 |
| 结构化输出 | 执行 `scripts/render_emergence_report.py` | 生成 JSON 与 Markdown 报告 |
