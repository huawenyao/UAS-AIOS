# ACA-Protocol 项目结构探索与认知空间设计报告

> **报告日期**：2026-03-13  
> **范围**：目录结构扫描、UAS-AIOS 架构理解、知识资产盘点、认知空间定义、索引体系设计  
> **实施状态**：✅ 已按本报告建议完成目录重组、认知空间定义、索引体系构建（2026-03-13）

---

## 一、目录结构扫描

### 1.1 当前一级、二级目录及关键文件

```
/workspace
├── CLAUDE.md                    # 根知识核心（ASUI 系统操作手册）
├── README.md                    # 项目说明
├── UAS_AIOS_ARCHITECTURE.md     # UAS-AIOS 架构文档（根目录）
├── ASUI_STRATEGY.md             # ASUI 战略分析（根目录）
├── AI_APPLICATION_PARADIGM_REPORT.md  # AI 范式报告（根目录）
├── uas_aios_pitch.html          # 产品 pitch 页面
│
├── .claude/
│   ├── skills/                  # 功能模块知识
│   │   ├── swarm_methodology.md
│   │   └── agent_opponent_matrix.md
│   ├── agents/                  # 场景化 Agent 配置
│   │   ├── README.md
│   │   ├── 01_user_perspective.md ~ 05_game_observer.md
│   │   └── .gitkeep
│   └── commands/                # 交互命令定义
│       ├── swarm_decision.md
│       └── .gitkeep
│
├── configs/                     # 业务规则配置
│   ├── swarm_workflow_config.json
│   └── .gitkeep
│
├── scripts/                     # 执行工具脚本
│   ├── swarm_run.py
│   ├── swarm_persist.py
│   └── .gitkeep
│
├── database/                    # 数据持久化
│   └── .gitkeep
│
├── docs/                        # 架构与战略文档
│   ├── ASUI_ARCHITECTURE.md
│   ├── ASUI_TECHNICAL_APPENDIX.md
│   └── ASUI_STRATEGIC_ANALYSIS_2025.md
│
├── whitepaper/                  # 白皮书
│   ├── ASUI_WHITEPAPER_CN.md
│   └── ASUI_WHITEPAPER_SLIDES.html
│
├── schemas/                     # JSON Schema 定义
│   └── workflow_config.schema.json
│
├── asui-cli/                    # CLI 工具包
│   ├── pyproject.toml
│   ├── README.md
│   └── src/asui/
│       ├── main.py, templates.py, init.py
│       └── __main__.py
│
└── examples/                    # 示例项目
    ├── customer-service/
    │   ├── CLAUDE.md
    │   ├── README.md
    │   ├── configs/workflow_config.json
    │   ├── .claude/skills/{ticket_rules.md, knowledge_base.md}
    │   └── scripts/create_ticket.py
    └── ai-recruitment/
        ├── CLAUDE.md
        ├── README.md
        ├── configs/workflow_config.json
        ├── .claude/skills/{jd_parser.md, evaluation_criteria.md}
        └── scripts/generate_report.py
```

### 1.2 当前目录结构问题清单

| 问题类型 | 具体表现 | 影响 |
|----------|----------|------|
| **冗余** | 根目录散落 3 个顶层架构/战略文档（UAS_AIOS_ARCHITECTURE.md、ASUI_STRATEGY.md、AI_APPLICATION_PARADIGM_REPORT.md） | 与 docs/ 职责重叠，难以区分"根级"与"文档级" |
| **分散** | 架构文档分布在根目录、docs/、whitepaper/ 三处 | 新成员难以快速定位"权威文档" |
| **命名不统一** | `UAS_AIOS_ARCHITECTURE.md` vs `ASUI_ARCHITECTURE.md`（UAS vs ASUI 混用） | 概念边界模糊 |
| **层级混乱** | `uas_aios_pitch.html` 与 `whitepaper/ASUI_WHITEPAPER_SLIDES.html` 功能相似，位置不同 | 产品材料分散 |
| **空目录** | `database/`、`configs/.gitkeep`、`.claude/commands/.gitkeep` 等仅含占位 | 需明确用途或合并 |
| **examples 结构不一致** | customer-service 有 2 个 skills，ai-recruitment 有 2 个 skills，但命名风格不同 | 示例可复制性降低 |
| **schemas 孤立** | `schemas/workflow_config.schema.json` 与 `configs/` 无显式关联 | 校验关系不清晰 |

---

## 二、建议的优化后目录结构

```
/workspace
├── CLAUDE.md                    # 唯一根知识入口（保留）
├── README.md
│
├── docs/                        # 统一文档中心
│   ├── architecture/            # 架构文档（新建子目录）
│   │   ├── UAS_AIOS_ARCHITECTURE.md
│   │   ├── ASUI_ARCHITECTURE.md
│   │   └── ASUI_TECHNICAL_APPENDIX.md
│   ├── strategy/                # 战略与范式（新建子目录）
│   │   ├── ASUI_STRATEGY.md
│   │   ├── ASUI_STRATEGIC_ANALYSIS_2025.md
│   │   └── AI_APPLICATION_PARADIGM_REPORT.md
│   └── whitepaper/              # 白皮书（迁移或软链）
│       ├── ASUI_WHITEPAPER_CN.md
│       └── ASUI_WHITEPAPER_SLIDES.html
│
├── assets/                      # 产品与对外材料（新建）
│   ├── uas_aios_pitch.html
│   └── whitepaper_slides.html   # 统一命名
│
├── .claude/
│   ├── skills/
│   ├── agents/
│   └── commands/
│
├── configs/
│   ├── swarm_workflow_config.json
│   └── _schema/                 # 可选：将 schema 与 config 同层
│       └── workflow_config.schema.json
│
├── schemas/                     # 或保留为全局 schema 库
│   └── workflow_config.schema.json
│
├── scripts/
├── database/
├── asui-cli/
└── examples/
```

**优化原则**：
- 文档按类型（architecture / strategy / whitepaper）分层
- 根目录仅保留 CLAUDE.md、README.md 等入口级文件
- 产品材料集中到 `assets/` 或 `docs/` 下明确子目录

---

## 三、UAS-AIOS 架构理解

### 3.1 核心概念提取

#### U/US/S 层

| 层级 | 全称 | 核心职责 | 关键组件 |
|------|------|----------|----------|
| **U 层** | User Intelligence Layer | 用户身份、记忆、偏好、意图理解 | Soul Protocol、Cecil 记忆、意图引擎 |
| **A 层** | Agent Collaborative Network | 任务分解、专家路由、多 Agent 协调 | Orchestrator、Specialists、A2A 协议 |
| **S 层** | System Integration Layer | 专业系统接入、业务语义、执行引擎 | MCP、ASUI 知识库、工具注册中心 |

#### Agent 层

- **主编排 Agent（Orchestrator）**：任务分解 → 专家路由 → 并行协调 → 结果合成
- **专业 Agent 类型**：代码、数据、文档、业务流程、研究、通信
- **A2A 协议**：Agent 间发现、委派、协同的标准化通信
- **执行环境**：Agent 沙箱（类比 Cursor VM），状态隔离、可审计、可回滚

#### 知识体系（UAS-AIOS 第八章）

**维度 1：归属**
- 用户知识（U 层）→ 个人偏好、历史、专业能力
- Agent 知识（A 层）→ 任务执行方法、协调策略
- 系统知识（S 层）→ 业务规则、工具能力、数据 Schema

**维度 2：持久性**
- 会话记忆（小时级）
- 项目记忆（周级）
- 长期记忆（永久）
- 演化知识（持续更新）

**维度 3：结构化程度**
- 非结构化（CLAUDE.md 风格）
- 半结构化（workflow_config JSON）
- 结构化（SQLite/向量 DB）
- 形式化（Schema、类型系统）

#### AI 协议栈（Π）

| 协议 | 职责 |
|------|------|
| UIP | 用户意图协议，Soul + Cecil |
| A2A | Agent 间通信，任务委派 |
| MCP | 工具调用，系统集成 |
| ASUI | 知识驱动执行、结构化沉淀、增量演化 |

### 3.2 ASUI 与 UAS-AIOS 的关系

- **ASUI**：知识驱动、AI-System-UI 融合、增量演化的架构范式，偏 S 层实现
- **UAS-AIOS**：在 ASUI 基础上扩展 U 层（用户 Soul）、A 层（多 Agent 协作）、完整协议栈
- **映射**：ASUI 的 K/A/E 三元组 ≈ UAS-AIOS 的 S 层知识库 + A 层编排 + S 层执行引擎

---

## 四、现有知识资产盘点

### 4.1 按目录统计

| 目录 | 文件数 | 类型 | 说明 |
|------|--------|------|------|
| `.claude/skills` | 2 | 方法论、矩阵 | swarm_methodology.md, agent_opponent_matrix.md |
| `.claude/agents` | 6 | Agent 定义 | README + 01~05 五智能体 + .gitkeep |
| `.claude/commands` | 1 | 命令定义 | swarm_decision.md |
| `configs` | 1 | 工作流配置 | swarm_workflow_config.json |
| `docs` | 3 | 架构/战略 | ASUI_ARCHITECTURE, TECHNICAL_APPENDIX, STRATEGIC_ANALYSIS |
| `whitepaper` | 2 | 白皮书 | ASUI_WHITEPAPER_CN.md, SLIDES.html |
| 根目录 | 4 | 入口+架构 | CLAUDE.md, README, UAS_AIOS, ASUI_STRATEGY, AI_APPLICATION_PARADIGM |
| `examples/*/.claude/skills` | 4 | 示例技能 | ticket_rules, knowledge_base, jd_parser, evaluation_criteria |
| `examples/*/configs` | 2 | 示例配置 | workflow_config.json × 2 |
| `schemas` | 1 | Schema | workflow_config.schema.json |

### 4.2 按类型分类

| 类型 | 文件列表 | 用途 |
|------|----------|------|
| **系统入口** | CLAUDE.md（根 + examples） | AI 加载的项目操作手册 |
| **方法论/技能** | swarm_methodology.md, agent_opponent_matrix.md, ticket_rules.md, knowledge_base.md, jd_parser.md, evaluation_criteria.md | 领域规则、决策框架 |
| **Agent 定义** | 01_user_perspective.md ~ 05_game_observer.md | 蜂群智能体立场与输出结构 |
| **命令定义** | swarm_decision.md | /swarmDecision 的用法与知识引用 |
| **工作流配置** | swarm_workflow_config.json, workflow_config.json × 2 | 步骤、依赖、prompt 模板 |
| **架构文档** | UAS_AIOS_ARCHITECTURE.md, ASUI_ARCHITECTURE.md, ASUI_TECHNICAL_APPENDIX.md | 架构形式化与规范 |
| **战略/范式** | ASUI_STRATEGY.md, ASUI_STRATEGIC_ANALYSIS_2025.md, AI_APPLICATION_PARADIGM_REPORT.md | 战略分析与范式研究 |
| **白皮书** | ASUI_WHITEPAPER_CN.md, ASUI_WHITEPAPER_SLIDES.html | 对外规范与宣讲 |
| **Schema** | workflow_config.schema.json | 配置校验 |

---

## 五、认知空间维度定义草案

基于 UAS-AIOS 架构与现有知识资产，推断「认知空间」应包含的维度：

### 5.1 用户认知（User Cognition）

| 维度 | 内容 | 数据来源 |
|------|------|----------|
| 身份与偏好 | 角色、专业领域、输出偏好、沟通风格 | Soul Protocol、CLAUDE.md 用户描述 |
| 当前上下文 | 主目标、活跃项目、团队、组织 | Cecil 工作记忆、current_context |
| 历史模式 | 决策偏好、常用工具、反馈模式 | 语义记忆、结构化记忆 |

### 5.2 系统认知（System Cognition）

| 维度 | 内容 | 数据来源 |
|------|------|----------|
| 业务规则 | 流程、约束、操作规范 | workflow_config、skills、SYSTEM.md |
| 工具能力 | MCP 工具、输入输出 Schema | 工具注册中心、MCP Server 定义 |
| 数据模型 | 实体、关系、Schema | schemas/、数据库 DDL |

### 5.3 Agent 认知（Agent Cognition）

| 维度 | 内容 | 数据来源 |
|------|------|----------|
| 能力声明 | 领域、工具、并发、输入输出 | Agent Card、A2A |
| 协调策略 | 对手盘、博弈规则、融合优先级 | agent_opponent_matrix、swarm_methodology |
| 执行状态 | 任务队列、依赖、结果 | 运行时状态、审计记录 |

### 5.4 协议认知（Protocol Cognition）

| 维度 | 内容 | 数据来源 |
|------|------|----------|
| 协议栈 | UIP、A2A、MCP、ASUI 的职责与边界 | UAS_AIOS_ARCHITECTURE 第七章 |
| 数据流 | 意图 → 任务 → 工具调用 → 结果 | 协议流转示例 |
| 演化规则 | 知识更新、版本迁移、回滚策略 | evolve(System, ΔK) 定义 |

### 5.5 知识归属与持久性

| 维度 | 内容 |
|------|------|
| 归属 | 用户知识 / Agent 知识 / 系统知识 |
| 持久性 | 会话 / 项目 / 长期 / 演化 |
| 结构化程度 | 非结构化 / 半结构化 / 结构化 / 形式化 |

---

## 六、索引体系设计草案

### 6.1 实体类型

| 实体类型 | 标识 | 属性示例 | 来源 |
|----------|------|----------|------|
| **Document** | 文件路径 | path, type, title, last_modified | 所有 .md、.json |
| **Skill** | 技能 ID | name, domain, rules_summary | .claude/skills/*.md |
| **Agent** | agent_id | name, stance, opponents, output_schema | .claude/agents/*.md |
| **Command** | 命令名 | name, description, knowledge_refs | .claude/commands/*.md |
| **Workflow** | workflow_id | version, steps, dependencies | configs/*.json |
| **Step** | step_id | workflow_id, type, prompt_ref, schema_ref | workflow_config.steps |
| **Schema** | schema_id | path, required_fields | schemas/*.json |
| **Concept** | 概念名 | layer(U/A/S), protocol, definition | 架构文档中的术语 |

### 6.2 关系类型

| 关系 | 主体 | 客体 | 说明 |
|------|------|------|------|
| **references** | Command, Step, Workflow | Document, Skill, Agent | 知识引用 |
| **depends_on** | Step | Step | 工作流依赖 |
| **implements** | Agent | Skill | Agent 实现某技能 |
| **opponent_of** | Agent | Agent | 对手盘关系 |
| **validates** | Schema | Workflow, Config | 校验目标 |
| **defines** | Document | Concept | 文档定义概念 |
| **extends** | Document | Document | 继承/扩展（如 example CLAUDE → 根 CLAUDE） |

### 6.3 现有引用关系（从代码与文档提取）

```
swarm_decision.md
  → swarm_methodology.md
  → agent_opponent_matrix.md
  → 01_user_perspective.md ~ 05_game_observer.md
  → swarm_workflow_config.json

swarm_workflow_config.json
  → swarm_methodology.md (global_config.methodology)
  → agent_opponent_matrix.md (global_config.opponent_matrix)
  → .claude/agents (global_config.agents_dir)
  → 各 step 的 prompt 中引用 agents/*.md

CLAUDE.md
  → .claude/skills/
  → .claude/agents/
  → configs/
  → docs/ASUI_ARCHITECTURE.md

UAS_AIOS_ARCHITECTURE.md
  → ASUI（概念）
  → MCP、A2A、Soul、Cecil（协议）
  → Cursor Cloud Agent（类比）
```

### 6.4 存储形式建议

| 形式 | 用途 | 格式 |
|------|------|------|
| **图结构** | 实体与关系查询、影响分析 | 邻接表 / Neo4j / 内存图 |
| **倒排索引** | 全文检索、概念定位 | 基于 path + content 的索引 |
| **扁平 JSON** | 快速加载、CLI 输出 | `index.json` 含 entities + relations |
| **增量更新** | 文件变更时更新索引 | 监听 .claude、configs、docs 变更 |

**推荐最小实现**：
- 单文件 `database/knowledge_index.json`：entities 数组 + relations 数组
- 构建脚本：扫描 .claude、configs、docs、whitepaper，解析 frontmatter 与显式引用，输出索引
- 可选：用 `jq` 或简单脚本做「谁引用了 X」「X 依赖哪些」查询

---

## 七、总结

| 维度 | 现状 | 建议 |
|------|------|------|
| **目录结构** | 根目录文档冗余，docs/whitepaper 分散 | 统一到 docs/ 下 architecture、strategy、whitepaper 子目录 |
| **认知空间** | 隐含在 UAS-AIOS 与 ASUI 文档中 | 显式定义五维度：用户、系统、Agent、协议、知识归属 |
| **索引体系** | 无显式索引，引用靠人工阅读 | 建立实体-关系索引，支持引用链与影响分析 |
| **知识资产** | 27 个 .md、4 个 .json，类型清晰 | 保持分类，补充索引元数据与交叉引用规范 |

---

*报告完成。可根据实际实施情况迭代更新。*
