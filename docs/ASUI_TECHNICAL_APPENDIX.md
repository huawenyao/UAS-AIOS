# ASUI技术附录：形式化定义与架构规范

## 一、形式化定义

### 1.1 系统三元组

```
ASUI_System = (K, A, E)

其中：
K = Knowledge Base = {CLAUDE.md, workflow_config, skills/*}
A = AI Orchestrator = {知识解释, 动态规划, 执行协调}
E = Execution Engine = {scripts, database, external_apis}
```

### 1.2 演化函数

```
evolve(System, ΔK) → System'

约束：
- ΔK 为知识增量（新增/修改/删除知识文档）
- System'.K = System.K ∪ ΔK
- System'.E 不变（无需代码变更）
- System'.A 自动适配新K（AI解释能力）
```

### 1.3 执行语义

```
execute(user_intent, System) →
  1. plan = A.interpret(K, user_intent)
  2. for step in plan:
       context = A.build_context(step, System)
       if step.requires_llm:
         result = A.call_llm(step.prompt, context, step.schema)
       else:
         result = E.run(step.script, context)
       E.persist(result)
  3. return E.aggregate(plan)
```

---

## 二、知识层Schema草案

### 2.1 CLAUDE.md 结构规范

```yaml
# 建议的CLAUDE.md元结构（可机器解析）
---
asui_version: "1.0"
project_type: scoring|workflow|chatbot
knowledge_refs:
  - workflow_config: "configs/workflow_config_v8.9.json"
  - skills_dir: ".claude/skills"
  - agents_dir: ".claude/agents"
---

# [项目名称]
# [系统概述]
# [核心命令列表]
# [数据流说明]
```

### 2.2 workflow_config Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ASUI Workflow Config",
  "type": "object",
  "required": ["version", "steps"],
  "properties": {
    "version": { "type": "string", "pattern": "^v[0-9]+\\.[0-9]+$" },
    "steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type"],
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "type": { "enum": ["script", "llm", "conditional"] },
          "script": { "type": "string" },
          "prompt_template": { "type": "string" },
          "output_schema": { "type": "object" },
          "dependencies": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

---

## 三、多Agent演进架构图

### 3.1 当前架构（单Agent顺序）

```
User: /start
        │
        ▼
┌───────────────────┐
│  Claude Code      │
│  (单上下文)        │
│  - 加载CLAUDE.md   │
│  - 解析workflow   │
│  - 顺序执行11步   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Execution Layer  │
│  - Python scripts │
│  - SQLite         │
│  - LLM API        │
└───────────────────┘
```

### 3.2 目标架构（编排器-工作者）

```
User: /start batch
        │
        ▼
┌─────────────────────────────┐
│  Lead Agent (Orchestrator)   │
│  - 解析workflow_config      │
│  - 识别可并行步骤(8,9)      │
│  - 分发任务到Worker池       │
└─────────────┬───────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│Worker1│ │Worker2│ │WorkerN│
│学生1  │ │学生2  │ │学生N  │
│独立   │ │独立   │ │独立   │
│上下文 │ │上下文 │ │上下文 │
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
    └─────────┼─────────┘
              ▼
┌─────────────────────────────┐
│  Aggregator                  │
│  - 合并维度得分              │
│  - 计算最终分                │
│  - 生成批量报告              │
└─────────────────────────────┘
```

---

## 四、与前沿框架的集成点

### 4.1 LangGraph集成

```python
# ASUI知识驱动LangGraph节点生成
def asui_to_langgraph(workflow_config: dict) -> StateGraph:
    graph = StateGraph(State)
    for step in workflow_config["steps"]:
        if step["type"] == "llm":
            graph.add_node(step["id"], create_llm_node(step))
        else:
            graph.add_node(step["id"], create_script_node(step))
    # 根据dependencies添加边
    return graph.compile()
```

### 4.2 Claude Subagents集成

```
Lead Agent职责：
- 加载workflow_config
- 将Step 8-9（维度判定）拆分为N个学生子任务
- 调用create_subagent(student_id) for each
- 收集结果并执行Step 10-13

Worker Subagent职责：
- 接收(student_id, question_context, dimension_defs)
- 独立执行LLM调用
- 返回结构化维度得分
```

---

## 五、量化评估指标体系

| 指标 | 定义 | 目标值 |
|------|------|--------|
| 知识/代码修改比 | 知识文件变更次数 / 代码变更次数 | > 3:1 |
| 功能上线周期 | 从需求到可用（分钟） | < 60 |
| 系统工具覆盖率 | AI可调用的工具数 / 总工具数 | 100% |
| 决策可追溯率 | 有证据链的决策数 / 总决策数 | 100% |
| 用户重复解释率 | 需重复说明需求的对话占比 | < 5% |
| 批量任务吞吐 | 学生数/分钟（评分场景） | > 5 |

---

*附录版本：v1.0 | 配合战略分析文档使用*
