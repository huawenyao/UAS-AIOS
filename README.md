# ACA-protocol

APP AGENT contract，build by tech protocol

## 架构范式：ASUI

本项目采用 **ASUI**（AI-System-UI Integration）架构范式：

- **知识驱动**：CLAUDE.md + configs 定义业务规则，修改即生效
- **构建即运行**：无需编译/部署，知识更新后立即可用
- **增量演化**：通过添加知识文件持续扩展系统能力

## 项目结构

```
├── CLAUDE.md          # 系统操作手册（AI 自动加载）
├── .claude/
│   ├── skills/        # 功能模块知识
│   ├── agents/        # 场景化 Agent 配置
│   └── commands/      # 交互命令定义
├── configs/           # 业务规则配置
├── scripts/           # 执行工具脚本
├── database/          # 数据持久化
└── docs/
    └── ASUI_ARCHITECTURE.md  # 架构理论文档
```

## 文档

- [ASUI 架构理论分析](./docs/ASUI_ARCHITECTURE.md) - 从第一性原理出发的体系化分析
