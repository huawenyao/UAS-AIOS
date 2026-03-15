# 领域构建评估技能

> 实现世界模型对专业Agent的自主调度和按需创建/接入，用于构建和评估UAS subapp。

## 一、技能定位

- **技能名称**：domain_builder
- **功能**：基于世界模型理解业务领域，自主发现/创建/调度专业Agent，构建和评估subapp
- **依赖**：道德势术器（§二）、世界模型（§四）、UAS Platform标准

## 二、核心流程

```
业务议题 → 领域分析 → Agent发现/创建 → 调度编排 → 构建评估 → subapp产出
```

### 2.1 领域分析（Domain Analysis）

**输入**：业务议题/需求描述

**过程**：
1. **道层面**：识别业务领域的本源法则（能量守恒→资源平衡、供需关系→价值流）
2. **德层面**：明确主体价值取向（谁受益、什么是正确的事）
3. **势层面**：分析主体间差异对比结构
   - 识别关键主体（决策者、执行者、受益者、阻碍者）
   - 构建差异矩阵：意图差异、能力差异、资源差异
   - 确定"势"的位置：推动者/阻碍者/连接者

**输出**：
```json
{
  "domainessence": "业务本质描述",
  "coreagents": ["需要的专业Agent类型列表"],
  "powerstructure": {
    "promoters": ["推动主体"],
    "blockers": ["阻碍主体"],
    "connectors": ["连接主体"]
  },
  "conflicttension": "核心矛盾张力描述"
}
```

### 2.2 Agent发现/创建（Agent Discovery/Creation）

**输入**：领域分析结果

**过程**：
1. **注册表查询**：在Agent Registry中搜索匹配的专业Agent
2. **能力匹配**：对比业务需求与Agent能力矩阵
3. **按需创建**：如无匹配，实例化新Agent类型
4. **接入适配**：对外部Agent进行接口适配

**Agent类型模板**：
| 类型 | 职责 | 核心能力 |
|------|------|----------|
| **Analyzer** | 领域分析 | 本质提取、矛盾识别 |
| **Planner** | 方案规划 | 策略生成、路径优化 |
| **Executor** | 执行调度 | 任务分解、Agent编排 |
| **Evaluator** | 评估审计 | 指标计算、偏差检测 |
| **Evolver** | 演化优化 | 反馈整合、知识更新 |

**输出**：
```json
{
  "agentpool": [
    {"type": "Analyzer", "source": "registry", "id": "domain-expert-v1"},
    {"type": "Planner", "source": "created", "id": "strategy-planner-v1"},
    {"type": "Executor", "source": "registry", "id": "orchestrator-v1"}
  ],
  "creationlog": ["从模板创建了strategy-planner-v1"]
}
```

### 2.3 调度编排（Orchestration）

**输入**：Agent池 + 业务目标

**过程**：
1. **势分析**：基于当前"势"的状态确定调度策略
2. **推动阶段**：分发任务到各Agent
3. **反馈收集**：收集执行结果、环境反应
4. **反身修正**：审视假设、策略、世界模型

**调度策略**：
- **串行**：Analyzer → Planner → Executor → Evaluator
- **并行**：多Executor同时执行不同策略路径
- **迭代**：Executor → Evaluator → Planner → Executor（循环）

**输出**：
```json
{
  "executiontrace": [
    {"phase": "analyze", "agent": "domain-expert-v1", "output": "..."},
    {"phase": "plan", "agent": "strategy-planner-v1", "output": "..."}
  ],
  "worldmodelupdate": {"主体关系": "更新", "反馈通道": "新增"}
}
```

### 2.4 构建评估（Build & Evaluate）

**输入**：调度结果 + 业务目标

**构建过程**：
1. 生成subapp结构（参考UAS_SUBAPP_TEMPLATE）
2. 填充configs（platform_manifest.json, workflow_config.json等）
3. 注入领域知识（.claude/skills/）
4. 配置治理策略（governance_policy.json）

**评估维度**：
| 维度 | 指标 | 阈值 |
|------|------|------|
| **完整性** | I,K,R,A,S,G,E,Π 覆盖度 | ≥80% |
| **一致性** | 与道德势术器映射 | 无断裂 |
| **可运行性** | 最小闭环通过 | 是 |
| **演化性** | 演化回路存在 | 是 |
| **治理性** | 审计/回滚/权限 | 完整 |

**输出**：
```json
{
  "subappstructure": {
    "path": "projects/<domain>-app/",
    "files": ["CLAUDE.md", "configs/*.json", ...]
  },
  "evaluationreport": {
    "completeness": 0.95,
    "consistency": "A级",
    "runnable": true,
    "evolvable": true,
    "governable": true,
    "overall": "通过"
  },
  "nextsteps": ["补充system_registry.json", "完善evolution_policy.json"]
}
```

## 三、与世界模型的集成

### 3.1 世界模型作为"法则编译器"

领域分析阶段调用世界模型的"降维与重构"能力：
```
业务问题（高维）→ 抽象映射 → 本源法则层 → 求解 → 情景化策略
```

### 3.2 推动—反馈—反身螺旋

每次调度都遵循：
```
推动（任务分发）→ 反馈（结果收集）→ 反身（WM修正）→ 下一轮推动
```

### 3.3 主客体发现

世界模型在执行过程中自主发现：
- 关键主体：决策者、执行者、评审者
- 关键客体：方案、资源、流程
- 反馈通道：可观测的状态变化

## 四、使用方式

### 4.1 命令格式

```
/build_domain <业务议题描述>
  [--analyze]    # 仅做领域分析
  --create       # 创建subapp结构
  --evaluate     # 评估现有subapp
  --app-id <id>  # 指定评估的subapp
```

### 4.2 示例

```
/build_domain "构建一个AI招聘系统"
  → 输出：领域分析 + Agent池 + 构建计划

/build_domain "招聘系统" --create
  → 输出：完整的projects/ai-recruitment/子应用

/build_domain --app-id "ai-recruitment" --evaluate
  → 输出：评估报告 + 改进建议
```

## 五、文件输出规范

构建的subapp必须满足UAS Platform标准：

```
projects/<domain>/
├── CLAUDE.md                          # 业务子应用说明
├── .claude/
│   ├── skills/
│   │   ├── domain_protocol.md         # 领域专有协议
│   │   └── output_contract.md         # 输出契约
│   └── agents/
│       └── registry.json              # Agent注册
├── configs/
│   ├── platform_manifest.json         # 平台清单
│   ├── workflow_config.json           # 工作流配置
│   ├── swarm_agents.json              # Agent配置
│   ├── runtime_config.json            # 运行时配置
│   ├── governance_policy.json         # 治理策略
│   ├── evolution_policy.json          # 演化策略
│   └── system_registry.json           # 系统接入
├── scripts/                           # 业务脚本
├── database/                          # 数据持久化
└── docs/
    └── IMPLEMENTATION_ROADMAP.md      # 实现路线图
```

## 六、关键约束

1. **目标守恒**：所有构建必须忠于原始业务意图
2. **审计留痕**：Agent行为必须有日志记录
3. **可回滚**：所有变更必须可追溯和回退
4. **演化入口**：必须包含E层（演化回路）实现
5. **知识沉淀**：领域知识必须沉淀到.skills/目录

---

*本技能实现世界模型对专业Agent的自主调度，是UAS-AIOS"自主发现"能力的关键支撑。*