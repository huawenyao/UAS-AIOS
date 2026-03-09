# ACA-protocol / ASUI

APP AGENT contract，build by tech protocol

## ASUI 架构

ASUI（AI-System-UI Integration）是一种以显式知识为驱动、实现 AI 能力与系统执行深度融合的智能系统架构模式。

## 项目结构

```
├── whitepaper/          # ASUI 架构白皮书
├── schemas/             # workflow_config JSON Schema
├── asui-cli/            # asui init 脚手架
├── examples/            # 领域验证项目
│   ├── customer-service/   # 智能客服
│   └── ai-recruitment/    # AI 全自动招聘
└── docs/                # 战略分析文档
```

## 快速开始

### 1. 安装 asui 脚手架

```bash
cd asui-cli && pip install -e .
```

### 2. 初始化项目

```bash
# 默认模板
asui init my-project

# 智能客服模板
asui init customer-service-demo -t customer-service

# AI 招聘模板
asui init recruitment-demo -t recruitment
```

### 3. 运行领域验证

在 Cursor/Claude Code 中打开 `examples/customer-service` 或 `examples/ai-recruitment`，按照各自 README 执行验证。

## 文档

- [ASUI 架构白皮书](whitepaper/ASUI_WHITEPAPER_CN.md)
- [战略分析 2025](docs/ASUI_STRATEGIC_ANALYSIS_2025.md)
- [技术附录](docs/ASUI_TECHNICAL_APPENDIX.md)
