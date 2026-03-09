# 智能客服系统 (ASUI 验证项目)

## 系统概述

基于 ASUI 架构的智能客服系统验证项目。知识库驱动对话 + 工单系统集成，实现 80% 常见问题自动回复。

## 核心命令

- `/start` - 启动客服会话，处理用户咨询
- `/ticket [工单ID]` - 查询或创建工单
- `/addKnowledge` - 添加 FAQ 知识

## 工作流

1. **意图识别** - 分析用户咨询类型（产品咨询/退款/投诉/技术问题）
2. **知识检索** - 从 knowledge_base.md 匹配最佳回复
3. **生成回复** - 基于检索结果生成自然语言回复
4. **工单创建** - 无法解决时按 ticket_rules.md 创建工单并分配

## 知识层

| 文件 | 用途 |
|------|------|
| configs/workflow_config.json | 客服工作流定义 |
| .claude/skills/knowledge_base.md | 产品/FAQ 知识 |
| .claude/skills/ticket_rules.md | 工单分类与升级规则 |

## 验证标准

- [x] 知识驱动：修改 knowledge_base.md 即改变回复内容
- [x] 构建即运行：添加新 FAQ 无需重启
- [x] 结构化输出：工单创建写入 database/tickets.json
- [x] 可审计：每次会话记录在 database/sessions.json

## 数据流

```
用户输入 → 意图识别(LLM) → 知识检索 → 回复生成(LLM)
                ↓
         无法解决 → 工单创建(script) → tickets.json
```
