# 三维理念现实涌现蜂群 - UAS SubApp

> 本示例同时作为 **UAS 平台 SubApp** 建设，目标为具备**智能全链路闭环**（渠道洞察→智能选品→内容生成→自动投放→效果优化→数据复盘）的顶级 SubApp。建设规划见 [docs/UAS_SUBAPP_建设规划.md](docs/UAS_SUBAPP_建设规划.md)。

## 验证目标

验证“三维 × 理念现实 × 目的激活 × 实例化验证进化”蜂群在复杂议题建模中的适用性：

- 宏观 / 中观 / 微观并行建模
- 理念与现实成对对冲
- 基础目的在具体场景中的激活
- 抽象结构映射到现实实体与接口
- 通过验证矩阵和指标系统驱动进化
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
| 现实实例化 | 调整 workflow 中的实例化步骤 | 输出自动映射为新的实体图谱 |
| 交叉验证 | 调整输出契约与验证规则 | 输出自动包含新的验证矩阵与评估指标 |
| 结构化输出 | 执行 `scripts/render_emergence_report.py` | 生成 JSON 与 Markdown 报告 |

## UAS 平台标准资产（已就绪）

- `configs/platform_manifest.json` - 平台清单
- `configs/runtime_config.json` - 运行时配置
- `configs/governance_policy.json` - 治理策略
- `configs/evolution_policy.json` - 演化策略
- `configs/system_registry.json` - 系统网格注册

使用共享 Runtime 运行（需在仓库根目录执行，且以 `examples` 为 subapp 根目录）：

```bash
python3 scripts/run_uas_runtime_service.py list --projects-root examples
python3 scripts/run_uas_runtime_service.py validate --app-id triadic-ideal-reality-swarm --projects-root examples
python3 scripts/run_uas_runtime_service.py run --app-id triadic-ideal-reality-swarm --projects-root examples --topic "如何把行业解决方案转化为真实工作方式？"
```

## 项目结构

```
triadic-ideal-reality-swarm/
├── CLAUDE.md
├── configs/
│   ├── platform_manifest.json
│   ├── runtime_config.json
│   ├── governance_policy.json
│   ├── evolution_policy.json
│   ├── system_registry.json
│   ├── workflow_config.json
│   └── swarm_agents.json
├── .claude/skills/
├── database/
├── reports/
├── scripts/
└── docs/
```
