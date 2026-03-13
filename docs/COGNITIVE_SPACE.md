# UAS-AIOS 认知空间定义

> 基于 UAS-AIOS 架构的显式认知维度与知识归属体系

## 一、认知空间概述

**认知空间**是 UAS-AIOS 对系统内所有可被 AI 理解、引用、演化的知识资产的显式组织框架。它将隐含在文档与配置中的知识结构形式化，支持：

- **知识定位**：快速找到某类知识所在
- **影响分析**：修改某知识时，识别受影响实体
- **归属清晰**：明确知识属于用户、Agent 还是系统层
- **索引构建**：为知识索引体系提供维度定义

## 二、五维认知空间

### 2.1 用户认知（User Cognition）

| 维度 | 内容 | 数据来源 | 持久性 |
|------|------|----------|--------|
| 身份与偏好 | 角色、专业领域、输出偏好、沟通风格 | Soul Protocol、用户描述 | 长期 |
| 当前上下文 | 主目标、活跃项目、团队、组织 | Cecil 工作记忆、current_context | 会话 |
| 历史模式 | 决策偏好、常用工具、反馈模式 | 语义记忆、结构化记忆 | 项目/长期 |

**归属**：U 层（User Intelligence Layer）

### 2.2 系统认知（System Cognition）

| 维度 | 内容 | 数据来源 | 持久性 |
|------|------|----------|--------|
| 业务规则 | 流程、约束、操作规范 | workflow_config、skills、CLAUDE.md | 项目/演化 |
| 工具能力 | MCP 工具、输入输出 Schema | 工具注册中心、MCP Server | 长期 |
| 数据模型 | 实体、关系、Schema | schemas/、数据库 DDL | 长期 |

**归属**：S 层（System Integration Layer）

### 2.3 Agent 认知（Agent Cognition）

| 维度 | 内容 | 数据来源 | 持久性 |
|------|------|----------|--------|
| 能力声明 | 领域、工具、并发、输入输出 | Agent Card、.claude/agents/ | 项目/长期 |
| 协调策略 | 对手盘、博弈规则、融合优先级 | agent_opponent_matrix、swarm_methodology | 项目 |
| 执行状态 | 任务队列、依赖、结果 | 运行时状态、审计记录 | 会话 |

**归属**：A 层（Agent Collaborative Network）

### 2.4 协议认知（Protocol Cognition）

| 维度 | 内容 | 数据来源 | 持久性 |
|------|------|----------|--------|
| 协议栈 | UIP、A2A、MCP、ASUI 的职责与边界 | UAS_AIOS_ARCHITECTURE | 长期 |
| 数据流 | 意图 → 任务 → 工具调用 → 结果 | 协议流转示例 | 长期 |
| 演化规则 | 知识更新、版本迁移、回滚策略 | evolve(System, ΔK) 定义 | 长期 |

**归属**：跨 U/A/S 的协议层

### 2.5 知识归属与持久性

| 维度 | 取值 | 说明 |
|------|------|------|
| **归属** | U / A / S | 用户知识 / Agent 知识 / 系统知识 |
| **持久性** | 会话 / 项目 / 长期 / 演化 | 生命周期 |
| **结构化程度** | 非结构化 / 半结构化 / 结构化 / 形式化 | 可解析性 |

## 三、认知空间与索引

认知空间维度为索引体系提供实体分类与关系定义的基础：

- **实体**：Document、Skill、Agent、Command、Workflow、Step、Schema、Concept
- **关系**：references、depends_on、implements、opponent_of、validates、defines、extends
- **索引存储**：`database/knowledge_index.json`

详见 [索引体系设计](PROJECT_STRUCTURE_AND_COGNITIVE_SPACE_REPORT.md#六索引体系设计草案) 与 `scripts/build_knowledge_index.py`。

## 四、认知空间与 ASUI 的映射

| ASUI 概念 | 认知空间映射 |
|-----------|--------------|
| K（知识库） | 系统认知 + Agent 认知 + 部分用户认知 |
| A（AI 编排） | Agent 认知 + 协议认知 |
| E（执行引擎） | 系统认知（工具能力、数据模型） |
| CLAUDE.md | 系统入口，引用系统认知与 Agent 认知 |

---

*认知空间定义 v1.0 | 随 UAS-AIOS 架构演进*
