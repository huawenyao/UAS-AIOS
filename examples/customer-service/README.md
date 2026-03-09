# 智能客服 - ASUI 领域验证

## 验证目标

验证 ASUI 架构在**智能客服**领域的适用性：
- 知识库驱动对话
- 工单系统集成
- 修改知识即改变系统行为

## 快速开始

1. 在 Cursor/Claude Code 中打开本项目
2. 对 AI 说：`/start 用户问：什么时候发货？`
3. AI 将加载 CLAUDE.md、workflow_config、knowledge_base，执行工作流并返回回复

## 验证清单

| 验证项 | 方法 | 预期 |
|--------|------|------|
| 知识驱动 | 修改 knowledge_base.md 添加新 FAQ | 下次咨询可匹配新回复 |
| 构建即运行 | 无需重启/部署 | 知识修改立即生效 |
| 工单创建 | 输入无法匹配的咨询 | 创建工单写入 database/tickets.json |
| 可审计 | 查看 database/ | 会话与工单可追溯 |

## 项目结构

```
customer-service/
├── CLAUDE.md
├── configs/workflow_config.json
├── .claude/skills/
│   ├── knowledge_base.md
│   └── ticket_rules.md
├── scripts/create_ticket.py
└── database/          # 运行时生成
```
