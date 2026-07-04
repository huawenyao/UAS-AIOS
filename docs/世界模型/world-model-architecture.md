# 世界模型认知架构技术规格

> 本文档定义 UAS-AIOS 世界模型的可运行认知架构

---

## 一、架构概述

世界模型认知主体是 UAS-AIOS 体系的核心认知引擎，实现从**意图**到**执行**的完整闭环。

### 设计目标

1. **持续运行**：非脚本式调用，是常驻内存的认知主体
2. **意图驱动**：外部意图激活，事件触发状态转移
3. **法则内化**：本源法则存储于知识层，动态情景化
4. **实时反馈**：执行反馈实时捕获，漂移检测与演化
5. **意图守恒**：策略始终与原始意图对齐

---

## 二、数据模型

### 2.1 配置模型 (`world_model_v2.schema.json`)

```json
{
  "meta": { "name": "", "domain": "" },
  "laws": { "categories": [{ "id": "", "name": "", "laws": [...] }] },
  "reducer": { "strategy": "causal|symbolic|neural|hybrid", "dimensions": [...] },
  "mappers": { "mappers": [...] },
  "runtime": { "execution_model": "", "state_machine": {...} },
  "intent_guard": { "threshold": 0.8, "checks": [...] },
  "evolution": { "enabled": true, "triggers": {...} }
}
```

### 2.2 状态模型 (`world_model_state.schema.json`)

```json
{
  "instance_id": "",
  "current_state": { "state_id": "", "state_name": "", "timestamp": "" },
  "context": {
    "intent": { "raw_input": "", "normalized": "", "vector": [], "constraints": [] },
    "scenario": { "entities": [], "relations": [] },
    "feedback": []
  },
  "laws_state": { "activated_laws": [], "confidences": {} },
  "evolution_state": { "drift_detected": false, "adaptations": [] }
}
```

---

## 三、认知状态机

### 3.1 状态定义

| 状态 | 含义 | 入口事件 |
|------|------|----------|
| `DORMANT` | 休眠，等待激活 | 系统启动 |
| `PERCEIVING` | 感知输入 | intent_received |
| `UNDERSTANDING` | 意图归一化 | perception_complete |
| `MAPPING` | 激活本源法则 | understanding_complete |
| `REDUCING` | 高维→低维降维 | mapping_complete |
| `REASONING` | 策略生成 | reduction_complete |
| `VALIDATING` | 意图守恒校验 | reasoning_complete |
| `ACTING` | 输出执行策略 | validation_passed |
| `MONITORING` | 监控反馈 | action_complete / feedback_received |
| `REFLECTING` | 漂移分析 | drift_detected |
| `EVOLVING` | 策略调整 | drift_confirmed |
| `COMPLETE` | 完成 | feedback_processed |
| `BLOCKED` | 阻塞 | validation_failed / drift_uncorrectable |
| `ERROR` | 错误 | 异常 |

### 3.2 状态转移图

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    ▼                                      │
              ┌──────────┐                                 │
    ┌────────→│ DORMANT  │                                 │
    │         └────┬─────┘                                 │
    │              │ intent_received                       │
    │              ▼                                       │
    │         ┌──────────┐                                 │
    │         │PERCEIVE │                                 │
    │         └────┬─────┘                                 │
    │              │ perception_complete                   │
    │              ▼                                       │
    │         ┌────────────┐                               │
    │         │UNDERSTAND │                               │
    │         └────┬─────┘                                 │
    │              │ understanding_complete                │
    │              ▼                                       │
    │         ┌──────────┐                                 │
    │         │ MAPPING  │                                 │
    │         └────┬─────┘                                 │
    │              │ mapping_complete                      │
    │              ▼                                       │
    │         ┌──────────┐                                 │
    │         │ REDUCING │                                 │
    │         └────┬─────┘                                 │
    │              │ reduction_complete                    │
    │              ▼                                       │
    │         ┌──────────┐                                 │
    │         │ REASONING│                                 │
    │         └────┬─────┘                                 │
    │              │ reasoning_complete                    │
    │              ▼                                       │
    │         ┌────────────┐                               │
    │    ┌───→│ VALIDATING │                               │
    │    │    └─────┬──────┘                               │
    │    │          │                                       │
    │    │    ┌─────┴─────┐                                 │
    │    │    │           │                                 │
    │    │    ▼           ▼                                 │
    │    │ validation   validation_failed                 │
    │    │ passed        (→ EVOLVING or BLOCKED)           │
    │    │    │           │                                 │
    │    │    ▼           │                                 │
    │    │  ┌──────────┐ │                                 │
    │    │  │  ACTING  │ │                                 │
    │    │  └────┬─────┘ │                                 │
    │    │       │action_complete                         │
    │    │       ▼                                         │
    │    │  ┌────────────┐                                 │
    │    │  │ MONITORING │←──────────────┐                 │
    │    │  └─────┬──────┘              │                 │
    │    │        │ feedback_received    │                 │
    │    │        │              ┌───────┴──────┐         │
    │    │        │              │               │         │
    │    │        │         no drift      drift_detected  │
    │    │        │              │               │         │
    │    │        │              ▼               ▼         │
    │    │        │        ┌──────────┐  ┌────────────┐     │
    │    │        │        │ COMPLETE │  │REFLECTING │     │
    │    │        │        └──────────┘  └─────┬──────┘     │
    │    │        │                           │             │
    │    │        └───────────→ (循环) ←─────┘             │
    │    │                                                   │
    │    └───────────────────────────────────────────────────┘
    │                       feedback_processed
    │
    └──────────────────────────────────────────────────────────
```

---

## 四、核心模块

### 4.1 意图守恒校验器 (IntentGuard)

```python
class IntentGuard:
    threshold: float = 0.8
    checks = [
        {'name': 'semantic_alignment', 'weight': 0.4},
        {'name': 'constraint_satisfaction', 'weight': 0.3},
        {'name': 'law_consistency', 'weight': 0.3}
    ]
```

**校验流程**：
1. 语义对齐：策略动作数量与意图匹配度
2. 约束满足：意图约束是否在策略中体现
3. 法则一致：激活法则的置信度

### 4.2 降维引擎 (Reducer)

**核心机制**：将高维现实映射为低维表示

```python
def reduce(intent, scenario):
    return {
        'subject': extract_dimension(intent, 'subject'),
        'object': extract_dimension(intent, 'object'),
        'causal_chain': extract_causal_chain(scenario),
        'invariants': extract_invariants(scenario),
        'abstraction': calculate_abstraction(intent)
    }
```

### 4.3 演化回路 (Evolution)

**触发条件**：
- 意图守恒校验失败
- 执行反馈漂移检测
- 置信度低于阈值

**演化动作**：
- 调整法则权重
- 更新映射函数
- 重置策略

---

## 五、使用接口

### 5.1 创建Agent

```python
from world_model_cognitive_agent import WorldModelCognitiveAgent

agent = WorldModelCognitiveAgent(config)
```

### 5.2 意图输入

```python
intent_id = agent.receive_intent("优化系统性能，确保响应时间<100ms")
```

### 5.3 执行循环

```python
# 方式1：一次性运行
result = agent.run_until_complete()

# 方式2：单步调试
while not agent.is_complete:
    agent.step()
```

### 5.4 反馈输入

```python
agent.receive_feedback({
    'expected': 'response_time < 100ms',
    'actual': 'response_time = 150ms',
    'channel': 'execution'
})
```

### 5.5 状态查询

```python
status = agent.get_status()
# { 'id': '', 'state': 'complete', 'events': 12, ... }
```

---

## 六、工程化约束

### 6.1 运行要求

- **内存常驻**：Agent实例持续运行，非每次调用创建
- **事件驱动**：状态转移由事件触发，非轮询
- **上下文保持**：状态机内保持完整上下文

### 6.2 扩展性

- **法则可插拔**：新增法则只需添加到配置
- **映射可定制**：自定义情景化映射器
- **通道可扩展**：新增反馈通道实现接口

---

## 七、文件清单

| 文件 | 描述 |
|------|------|
| `schemas/world_model_v2.schema.json` | 数据模型Schema |
| `schemas/world_model_state.schema.json` | 状态模型Schema |
| `scripts/world_model_cognitive_agent.py` | 认知Agent实现 |
| `scripts/world_model_event_driven.py` | 事件驱动版本 |
| `docs/world-model-architecture.md` | 本文档 |

---

*Version: 1.0*
*Generated: 2026-03-17*
