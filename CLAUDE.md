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
│   ├── skills/            # 功能模块知识（含 swarm_methodology、agent_opponent_matrix）
│   ├── agents/            # 场景化 Agent 配置（含蜂群五智能体 01-05）
│   └── commands/          # 交互命令定义（含 swarm_decision）
├── configs/               # 业务规则配置（含 swarm_workflow_config.json）
├── scripts/               # 执行工具脚本（含 build_knowledge_index、swarm_*、query_index）
├── database/              # 数据持久化（swarm_decisions.json、knowledge_index.json）
├── docs/                  # 统一文档中心
│   ├── architecture/      # UAS_AIOS、ASUI 架构
│   ├── strategy/          # 战略与范式分析
│   ├── whitepaper/        # 白皮书
│   └── COGNITIVE_SPACE.md # 认知空间定义
└── assets/                # 产品材料（uas_aios_pitch.html）
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
| /swarmDecision [议题] | 启动 SelfPaw 蜂群认知智能体，基于否定之否定辩证升维的全维度决策洞察 |

### SelfPaw 蜂群智能体体系

基于否定之否定辩证升维方法论，用蜂群智能体替代个人单一决策：

- **五智能体**：用户视角、关卡障碍、核心决策、买单价值、博弈观察
- **三阶段**：初次否定（多维拆解）→ 二次否定（对手盘博弈）→ 辩证融合（智能涌现）
- **知识层**：`.claude/skills/swarm_methodology.md`、`.claude/agents/01-05_*.md`
- **工作流**：`configs/swarm_workflow_config.json`

## 认知空间与索引

- **认知空间**：用户认知、系统认知、Agent 认知、协议认知（见 `docs/COGNITIVE_SPACE.md`）
- **知识索引**：`python scripts/build_knowledge_index.py` 构建实体-关系索引
- **索引查询**：`python scripts/query_index.py --entity agent` 按类型筛选；`--refs` / `--deps` 查询引用

## 修改即生效

- 修改本文件或 configs 中的配置 → 无需重启，下次执行即生效
- 添加 .claude/skills/ 下的知识文件 → AI 自动纳入上下文
- 知识变更后运行 `build_knowledge_index.py` → 更新索引
