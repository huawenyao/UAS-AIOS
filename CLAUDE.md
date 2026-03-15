# UAS-AIOS 项目系统操作手册

> 本文件是 UAS-AIOS 架构的**知识层核心**，AI 将自动加载此文档理解项目上下文并生成执行计划。

---

## 一、项目概述

| 属性 | 值 |
|------|-----|
| **项目名称** | ACA-protocol / UAS-AIOS |
| **架构范式** | ASUI（AI-System-UI Integration） |
| **核心命题** | 认知实践是生产力创造价值的根本路线 |
| **核心原则** | 知识即配置、构建即运行、增量演化 |

---

## 二、核心理论体系（图谱）

```
╔═══════════════════════════════════════════════════════════════════╗
║                    道德势术器：AGI认知进化路径                      ║
╠═══════════════════════════════════════════════════════════════════╣
║   道 (Tao) ──→ 德 (De) ──→ 势 (Shi) ──→ 术 (Shu) ──→ 器 (Qi)      ║
║     │            │            │            │            │          ║
║   存在论      价值论      博弈论      方法论      工程论          ║
║     │            │            │            │            │          ║
║ 本源法则    价值约束    差异对比    策略制定    工具实现        ║
╚═══════════════════════════════════════════════════════════════════╝
                          │
                          ▼
              认知实践论 → 价值闭环（7步）
                          │
              世界模型（五维：空间/时间/主体/客体/反馈）
                          │
              AGI = World Model + AI Agent
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
   User AGI (selfpaw)               Business AGI (Πpaw)
   蜂群智能体（五智能体）              多专业Agent编排
        │                                   │
        └─────────────────┬─────────────────┘
                          ▼
              UAS-AIOS (I,K,R,A,S,G,E,Π)
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     ASUI            三元张力           演化螺旋
   知识即配置       U/A/S摩擦         推动—反馈—反身
```

---

## 三、核心方法论

### 3.1 道德势术器（元方法论）

| 层次 | 内涵 | AGI映射 | 工程实现 |
|------|------|---------|----------|
| **道** | 系统总体性原则 | WM元理论层 | 知识库/配置 |
| **德** | 主体价值取向 | 价值函数/约束 | 治理规则/G层 |
| **势** | 主体间差异对比 | WM结构性张力 | 任务分析/主客体建模 |
| **术** | 方法策略层 | Agent策略 | A层Agent编排 |
| **器** | 工具产品层 | 执行器 | R层运行时/S层系统 |

### 3.2 世界模型（认知内核）

- **本质**：法则编译器（不是预测器）
- **机制**：降维与重构
  ```
  现实（高维混沌）→ 抽象映射 → 世界模型（低维有序）→ 求解 → 映射回现实
  ```
- **三重身份**：镜像（反映世界）→ 透镜（看本质）→ 熔炉（重塑现实）
- **五维**：空间、时间、主体、客体、感知—行动—反馈
- **层次**：宏观层（本源法则）→ 微观层（情景化）→ 执行层

### 3.3 演化机制

- **推动—反馈—反身螺旋**：
  ```
  推动 → 反馈 → 反身 → 推动（收敛到最佳选择）
  ```
- **价值闭环（7步）**：
  输入 → 模拟 → 生成 → 交互 → 进化 → 输出 → 收益

---

## 四、工程架构

### 4.1 UAS-AIOS 形式化

```
UAS-Platform = (I, K, R, A, S, G, E, Π)

I   - 意图（Intent）
K  - 知识底座（默认ASUI）
R  - 自主运行时（Runtime）
A  - Agent编织（Agent Fabric）
S  - 系统网格（System Grid）
G  - 治理（Governance）
E  - 演化回路（Evolution）
Π  - 协议栈（Protocol Stack）
```

### 4.2 ASUI 技术底座

- **定义**：AI-System-UI Integration
- **三元组**：AI能力层 × System执行层 × UI交互层
- **原则**：知识即配置、构建即运行、增量演化

### 4.3 双轨AGI

| 轨道 | 定义 | 工程实现 |
|------|------|----------|
| **User AGI** | 面向个人的通用智能体 | selfpaw（蜂群形态）|
| **Business AGI** | 面向组织的专业智能体 | Πpaw（多Agent编排）|

---

## 五、目录结构

```
.
├── CLAUDE.md                    # 本文件 - 系统操作手册
├── .claude/
│   ├── skills/                  # 功能模块知识
│   ├── agents/                  # 场景化Agent配置
│   └── commands/                # 交互命令定义
├── configs/                     # 业务规则配置
├── scripts/                     # 执行工具脚本
├── database/                    # 数据持久化
├── examples/                    # 示例应用
│   ├── selfpaw-cognitive-swarm/    # 蜂群智能体（User AGI）
│   ├── triadic-ideal-reality-swarm/ # 三维理念现实
│   └── ai-recruitment/              # 招聘OS业务应用
├── docs/
│   ├── THEORY_SYSTEM.md             # 理论体系总纲 ← 核心必读
│   ├── AGI_WORLD_MODEL_UAS.md       # 世界模型与双轨AGI
│   ├── ASUI_ARCHITECTURE.md         # ASUI架构
│   ├── TEMPLATE_PROJECT_RELATIONSHIP.md  # 模板与项目关系（从运行逻辑推导）
│   ├── UAS_ASUI_PROTOCOL_GAPS_AND_ROADMAP.md  # 协议化与智能化推演不足及改进路线图
│   ├── 世界模型/
│   │   └── 世界模型.md               # 法则编译器深度解析
│   └── theory_system_visualization.html  # 理论可视化（浏览器打开）
└── heartbeat_logs/              # 心跳日志
```

---

## 六、关键工作流

### 6.1 认知实践闭环

```
1. 输入 → 真实问题 + 领域知识
2. 模拟 → 数字孪生环境试错
3. 生成 → 多种可能方案
4. 交互 → 人机协同评估
5. 进化 → 更新世界模型
6. 输出 → 介入现实工作流
7. 收益 → 效益反哺系统
```

### 6.2 交互命令

| 命令 | 功能 |
|------|------|
| /start | 启动主工作流 |
| /addQuest | 添加新题目/任务 |
| /addData | 添加新数据 |
| /createSubApp | 自主生产 UAS sub app（基于 command + agent skill） |
| /evolveApply | 将 evolution 建议回写到 configs/skills，实现业务层进化 |

### 6.3 智能体任务执行（ASUI标准）

```
intent_activation → understanding → planning →
execution → monitoring → render_report → evaluation
```

---

## 七、修改即生效

- 修改本文件或 configs 中的配置 → 无需重启，下次执行即生效
- 添加 .claude/skills/ 下的知识文件 → AI 自动纳入上下文

---

## 八、快速索引

| 需求 | 查阅位置 |
|------|----------|
| 理解项目核心理论 | §二、§三本文档 |
| 了解工程架构 | §四、本文档 |
| 世界模型深度理解 | docs/THEORY_SYSTEM.md §4.1.1 |
| 道德势术器详解 | docs/THEORY_SYSTEM.md §二 |
| ASUI技术细节 | docs/ASUI_ARCHITECTURE.md |
| 蜂群智能体实现 | examples/selfpaw-cognitive-swarm/ |
| 三维理念现实 | examples/triadic-ideal-reality-swarm/ |
| 领域构建评估技能 | .claude/skills/domain_builder.md |
| Agent注册表 | .claude/agents/domain_agent_registry.json |

---

## 九、领域构建评估（Domain Builder）

> 技能文件：`.claude/skills/domain_builder.md`

### 9.1 功能定位

实现世界模型对专业Agent的**自主调度**和**按需创建/接入**，用于构建和评估UAS subapp。

### 9.2 核心流程

```
业务议题 → 领域分析 → Agent发现/创建 → 调度编排 → 构建评估 → subapp产出
```

### 9.3 Agent类型

| 类型 | 职责 | 来源 |
|------|------|------|
| **Analyzer** | 领域分析、本质提取 | builtin |
| **Planner** | 策略规划、路径优化 | template |
| **Executor** | 调度编排、任务分解 | builtin |
| **Evaluator** | 评估审计、偏差检测 | builtin |
| **Evolver** | 演化优化、知识更新 | template |

### 9.4 使用方式

```
/build_domain <业务议题> [--analyze] [--create] [--evaluate] [--app-id <id>]
```

### 9.5 评估维度

| 维度 | 指标 |
|------|------|
| 完整性 | I,K,R,A,S,G,E,Π 覆盖度 ≥80% |
| 一致性 | 与道德势术器映射无断裂 |
| 可运行性 | 最小闭环通过 |
| 演化性 | 演化回路存在 |
| 治理性 | 审计/回滚/权限完整 |

---

*本文件随项目理论体系更新，核心内容需保持稳定。*