# AI 全自动招聘 - ASUI 领域验证

## 验证目标

验证 ASUI 架构在**AI 招聘**领域的适用性：
- 岗位画像解析
- 简历多维度匹配
- 可审计报告生成
- 关键实体与事件闭环（Job/Candidate/Task/Event/Notification/Evaluation）

## 快速开始

**方式一：命令行（推荐，单一入口）**

```bash
# 指定简历目录，批量匹配并生成带证据链的 HTML 报告
python workflow_execution.py --resume-dir test_fixtures

# 或使用环境变量（Windows）
set RESUME_DIR=path/to/resumes
python workflow_execution.py
```

运行结束会输出 **价值摘要**（如：本批 X 份有效简历，推荐/待定共 Y 人，可解释推荐名单已生成），并发布 `screening_completed` 事件至 `database/events.json`。

**方式二：Cursor / AI 对话**

1. 在 Cursor/Claude Code 中打开本项目
2. 对 AI 说：`/addJob 招聘 Python 后端工程师，本科以上，3年经验，熟悉 Django`
3. 对 AI 说：`/match 岗位1 [粘贴简历内容]`
4. AI 将执行工作流，生成 database/candidates.json 和 reports/candidate_xxx.html

报告内容包含：**匹配得分、推荐结论、风险标识（中文）、证据链**，便于招聘经理与面试官直接理解推荐理由。

**方式三：真实场景验证（与 evolution_policy 对齐）**

使用 `database/jobs.json` 中的真实岗位与 `test_fixtures` 中的简历，跑通多岗位×多简历筛选并产出验证报告：

```bash
python scripts/validate_real_scenarios.py
```

输出：`database/candidates.json`、`reports/validation_report_*.md`（含 process_completion_score、decision_explainability_score 等）、每候选人 HTML 报告。

## 验证清单

| 验证项 | 方法 | 预期 |
|--------|------|------|
| 真实场景闭环 | `python scripts/validate_real_scenarios.py` | 多岗位×多简历筛选，验证报告通过 |
| 知识驱动 | 修改 evaluation_criteria.md 调整权重 | 下次匹配使用新标准 |
| 构建即运行 | 在 workflow 添加新维度 | 无需改 Python 代码 |
| 结构化输出 | 执行 /match 或 workflow_execution | 写入 candidates.json、events.json |
| 可审计 | 查看 reports/*.html、database/audit/ | 含得分与证据链、审计记录 |
| 实体与事件 | 运行后查看 database/tasks.json、events.json | 初筛完成触发 screening_completed |

## 项目结构

```
ai-recruitment/
├── CLAUDE.md
├── README.md
├── workflow_execution.py          # 主入口（支持 --resume-dir）
├── configs/
│   ├── workflow_config.json      # 招聘工作流定义
│   ├── entity_schemas.json       # 关键实体结构（Job/Candidate/Task/Event/Notification/Evaluation）
│   ├── event_policy.json         # 事件类型与触发策略
│   ├── runtime_config.json       # 与 UAS autonomous_agent runtime 对齐
│   └── swarm_agents.json         # 蜂群用户角色（体验测试用）
├── .claude/skills/
│   ├── jd_parser.md
│   └── evaluation_criteria.md
├── scripts/
│   ├── generate_report.py        # 报告生成（含证据链与风险）
│   ├── report_renderer.py        # HTML 渲染共用
│   ├── validate_real_scenarios.py # 真实场景验证（多岗位×多简历，evolution_policy 指标）
│   ├── entity_runtime.py         # 实体与事件运行时（Task/Event/Notification/Evaluation）
│   └── swarm_ux_test_runner.py   # 蜂群体验测试
├── docs/
│   ├── entity_event_model.md     # 实体与事件闭环、与 agent runtime 叠合
│   ├── 产品价值感设计.md          # 业务目标、痛点、价值感设计
│   └── swarm_ux_test_scenarios.md
├── test_fixtures/                 # 测试用简历
├── database/                     # 运行时生成（jobs, candidates, tasks, events, notifications, evaluations, audit）
└── reports/                      # 运行时生成（HTML 报告、蜂群测试结果、价值评估）
```

## 与招聘智能 OS 对齐

本示例在效率（初筛提效、可解释决策）、公平（可追溯、可配置）、体验（报告可读、价值摘要）上与 **projects/ai-recruitment-os** 的成功标准与指标一致；实体与事件设计见 `docs/entity_event_model.md`，价值感设计见 `docs/产品价值感设计.md`。
