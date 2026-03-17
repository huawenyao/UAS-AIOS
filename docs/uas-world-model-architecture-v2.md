# UAS World Model 架构设计

> 定位：UAS 元Agent 的认知引擎组件

---

## 一、架构定位

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         UAS 元Agent                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐ │
│   │                    World Model (认知引擎)                         │ │
│   │                                                                  │ │
│   │   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │ │
│   │   │  目标理解     │  │  动态规划     │  │  系统建模     │       │ │
│   │   │ Intent Under. │  │  Planning    │  │ Modeling     │       │ │
│   │   └───────────────┘  └───────────────┘  └───────────────┘       │ │
│   │                                                                  │ │
│   │   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │ │
│   │   │  知识表示     │  │  隐空间推理   │  │  漂移检测     │       │ │
│   │   │ Knowledge    │  │ Latent Plan  │  │  Evolution   │       │ │
│   │   └───────────────┘  └───────────────┘  └───────────────┘       │ │
│   │                                                                  │ │
│   └─────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                   │
│   ┌─────────────────────────────────────────────────────────────────┐ │
│   │                    SubAgent 生成引擎                              │ │
│   │                    (Agent Fabric)                                │ │
│   └─────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    SubAgent (Agentic Agent)                            │
│   - 意图执行                                                          │
│   - 行动闭环                                                          │
│   - 反馈演化                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 二、调用接口

### 2.1 统一调用入口

```python
from uas_world_model import UASWorldModelService

wm_service = UASWorldModelService()

# 调用方式
wm_service.process_intent(raw_intent, context)
wm_service.create_plan(goal, context, actions)
wm_service.model_system(description, context)
wm_service.check_drift(expected, actual, context)
```

### 2.2 能力枚举

```python
class WMCapability(Enum):
    INTENT_UNDERSTANDING = "intent_understanding"
    GOAL_DECOMPOSITION = "goal_decomposition"
    DYNAMIC_PLANNING = "dynamic_planning"
    SYSTEM_MODELING = "system_modeling"
    CONTEXT_REASONING = "context_reasoning"
    DRIFT_DETECTION = "drift_detection"
```

---

## 三、UAS 工作流中的 World Model

### 3.1 Intent Activation 阶段

```
用户输入 → [World Model: 目标理解] → 归一化意图 → SubAgent 目标
```

**调用**：
```python
intent_result = wm_service.process_intent(
    "优化招聘流程，确保3天内完成初筛",
    context={"domain": "recruitment"}
)
```

**返回**：
```json
{
  "intent_id": "xxx",
  "normalized": "优化招聘流程确保3天内完成初筛",
  "constraints": ["3天内", "完成初筛"],
  "goals": ["优化招聘流程"],
  "confidence": 0.85
}
```

### 3.2 Agent Planning 阶段

```
意图 → [World Model: 目标分解 + 动态规划] → 执行策略
```

**调用**：
```python
plan_result = wm_service.create_plan(
    goal="优化招聘流程",
    context={
        "current_state": "人工筛选简历",
        "state_attributes": {"time": "5天", "cost": "高"},
        "goal_attributes": {"time": "3天", "cost": "降低30%"}
    },
    actions=[
        {"name": "自动筛选", "cost": 1.0},
        {"name": "AI面试", "cost": 0.8},
        {"name": "流程并行化", "cost": 1.5}
    ]
)
```

**返回**：
```json
{
  "selected_action": "自动筛选",
  "trajectories": 3,
  "confidence": 0.78
}
```

### 3.3 AgentFabric 阶段

```
业务场景 → [World Model: 系统建模] → Agent 能力配置
```

**调用**：
```python
model_result = wm_service.model_system(
    "招聘系统：候选人投递 → HR筛选 → 面试安排 → offer发放",
    context={"scale": "1000人/年"}
)
```

### 3.4 Evolution 阶段

```
执行结果 → [World Model: 漂移检测] → 知识更新
```

**调用**：
```python
drift_result = wm_service.check_drift(
    expected="3天完成初筛",
    actual="4天完成初筛",
    context={"entities": ["筛选流程"]}
)
```

---

## 四、模块清单

| 文件 | 功能 | 对外接口 |
|------|------|----------|
| `intent_understanding.py` | 目标理解 | `understand_intent()` |
| `knowledge_base.py` | 知识表示 | `retrieve()`, `query_graph()` |
| `planning_engine.py` | 规划推理 | `plan()` |
| `world_model_builder.py` | 模型构建 | `build()` |
| `latent_planning.py` | 隐空间规划 | `imagine()`, `optimize_policy()` |
| `knowledge_evolution.py` | 知识演化 | `evolve()` |
| `uas_world_model.py` | 统一封装 | `process_intent()`, `create_plan()`, etc. |

---

## 五、使用示例

```python
# 1. 创建服务
from uas_world_model import UASWorldModelService

wm = UASWorldModelService()

# 2. Intent Activation
intent = wm.process_intent("构建招聘OS，自动筛选简历")

# 3. Planning
plan = wm.create_plan(
    goal=intent['data']['goals'][0],
    context={'current_state': 'manual', 'goal_attributes': {'automation': 0.8}}
)

# 4. AgentFabric (SubAgent generation)
# ... 使用 plan 结果生成 SubAgent

# 5. Evolution
drift = wm.check_drift(expected=0.8, actual=0.6)
```

---

## 六、与现有 UAS 组件关系

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           UAS Platform                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   I (Intent) ──────────→ [World Model] ──────────→ AgentFabric        │
│                         目标理解                  SubAgent生成         │
│                                                                         │
│   K (Knowledge) ←─────── [World Model]                                │
│                        知识表示 + 推理                                   │
│                                                                         │
│   R (Runtime) ──────────→ [World Model] ──────────→ Evolution         │
│                        规划执行                  漂移检测               │
│                                                                         │
│   S (System Grid) ─────→ [World Model]                                │
│                        系统建模                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

*Version: 2.0 - 重构版*
