# asui-cli

ASUI 架构脚手架 - 快速初始化知识驱动型 AI 系统项目。

## 安装

```bash
pip install -e .
# 或从源码安装
cd asui-cli && pip install .
```

## 使用

### 初始化默认项目

```bash
asui init my-project
```

### 使用模板初始化

```bash
# 智能客服模板
asui init customer-service-demo -t customer-service

# AI 全自动招聘模板
asui init recruitment-demo -t recruitment

# selfpaw 原生认知蜂群模板
asui init selfpaw-swarm-demo -t selfpaw-swarm
```

### 在当前目录初始化

```bash
asui init .
```

### 覆盖已存在文件

```bash
asui init my-project -f
```

## 模板说明

| 模板 | 说明 |
|------|------|
| **default** | 通用 ASUI 项目结构 |
| **customer-service** | 智能客服：知识库驱动 + 工单集成 |
| **recruitment** | AI 招聘：岗位解析 + 简历匹配 + 评估报告 |
| **selfpaw-swarm** | 认知蜂群：五智能体对手盘 + 否定之否定辩证决策 |

## 生成的项目结构

```
project/
├── CLAUDE.md              # 系统操作手册
├── .claude/
│   ├── skills/            # 功能模块知识
│   ├── agents/            # 领域 Agent
│   └── commands/          # 交互命令
├── configs/
│   └── workflow_config.json
├── scripts/               # 执行脚本
└── database/              # 数据持久化
```

## 许可证

MIT
