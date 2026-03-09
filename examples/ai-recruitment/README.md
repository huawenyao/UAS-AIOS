# AI 全自动招聘 - ASUI 领域验证

## 验证目标

验证 ASUI 架构在**AI 招聘**领域的适用性：
- 岗位画像解析
- 简历多维度匹配
- 可审计报告生成

## 快速开始

1. 在 Cursor/Claude Code 中打开本项目
2. 对 AI 说：`/addJob 招聘 Python 后端工程师，本科以上，3年经验，熟悉 Django`
3. 对 AI 说：`/match 岗位1 [粘贴简历内容]`
4. AI 将执行工作流，生成 database/candidates.json 和 reports/candidate_xxx.html

## 验证清单

| 验证项 | 方法 | 预期 |
|--------|------|------|
| 知识驱动 | 修改 evaluation_criteria.md 调整权重 | 下次匹配使用新标准 |
| 构建即运行 | 在 workflow 添加新维度 | 无需改 Python 代码 |
| 结构化输出 | 执行 /match | 写入 candidates.json |
| 可审计 | 查看 reports/*.html | 含得分与证据链 |

## 项目结构

```
ai-recruitment/
├── CLAUDE.md
├── configs/workflow_config.json
├── .claude/skills/
│   ├── jd_parser.md
│   └── evaluation_criteria.md
├── scripts/generate_report.py
├── database/          # 运行时生成
└── reports/           # 运行时生成
```
