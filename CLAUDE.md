# ASUI 项目系统操作手册

> 本文件是 ASUI 架构的**知识层核心**，AI 将自动加载此文档理解项目上下文并生成执行计划。

## 项目概述

- **项目名称**：ACA-protocol
- **架构范式**：ASUI（AI-System-UI Integration）
- **核心原则**：知识即配置、构建即运行、增量演化

## 目录结构

```
.
├── CLAUDE.md              # 本文件 - 系统操作手册
├── .claude/
│   ├── skills/            # 功能模块知识
│   ├── agents/            # 场景化 Agent 配置
│   └── commands/          # 交互命令定义
├── configs/               # 业务规则配置
├── scripts/               # 执行工具脚本
├── database/              # 数据持久化
└── docs/
    ├── ASUI_ARCHITECTURE.md  # 架构理论文档
    ├── THEORY_SYSTEM.md     # 理论体系总纲（方法论综合与关系图谱）
    ├── TEMPLATE_PROJECT_RELATIONSHIP.md  # 模板与项目关系（从运行逻辑推导）
    └── theory_system_visualization.html  # 理论体系可视化（浏览器打开）
```

## 核心工作流

1. **知识定义**：在 CLAUDE.md、configs、skills 中定义业务规则
2. **AI 解释**：AI 加载知识文档，理解上下文
3. **执行协调**：AI 调用 scripts、database 等系统工具
4. **结果反馈**：结构化输出写入数据库，生成报告

## 交互命令

| 命令 | 功能 |
|------|------|
| /start | 启动主工作流 |
| /addQuest | 添加新题目/任务 |
| /addData | 添加新数据 |
| /createSubApp | 自主生产 UAS sub app（基于 command + agent skill） |

## 修改即生效

- 修改本文件或 configs 中的配置 → 无需重启，下次执行即生效
- 添加 .claude/skills/ 下的知识文件 → AI 自动纳入上下文
