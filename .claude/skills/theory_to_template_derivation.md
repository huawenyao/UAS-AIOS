---
name: theory-to-template-derivation
description: 从业务目标经世界模型分析到模板选择的可追溯推导链。用于：(1) 理论驱动的模板选择 (2) 世界模型分析 (3) 方法论信号解读 (4) 推导规则
---

# 理论→模板推演协议

## 技能定位

本协议定义从**业务目标**经**世界模型分析**与**方法论匹配**到**模板选择**的可追溯推导链。Agent 执行 sub app 生产时必须遵循此协议，确保模板选择由理论原理驱动而非仅关键词匹配。

## 推导链

```
业务目标（自然语言）
    │
    ▼
世界模型分析（五维：空间/时间/主体/客体/感知-行动-反馈）
    │
    ▼
方法论倾向判定（多主体博弈 | 理念-现实张力 | 线性流程）
    │
    ▼
模板选择（uas-subapp | selfpaw-swarm | triadic-ideal-reality-swarm）
```

## 一、世界模型分析输出

对业务目标进行世界模型五维分析，产出结构化对象：

```json
{
  "subjects": [
    { "id": "s1", "role": "决策者", "stake": "成败关键", "capability": "..." }
  ],
  "objects": [
    { "id": "o1", "type": "业务实体", "mutable": true, "description": "..." }
  ],
  "feedback_channels": [
    { "source": "销量数据", "delay": "日级", "reliability": "高" }
  ],
  "spatial_constraints": ["跨平台", "多地域"],
  "temporal_constraints": ["实时", "批次"],
  "methodology_signals": {
    "multi_agent_game": 0.8,
    "ideal_reality_tension": 0.3,
    "linear_flow": 0.5
  }
}
```

**methodology_signals** 说明：
- `multi_agent_game`：多主体博弈强度（0-1），主体间立场冲突、对手盘、博弈明显时高
- `ideal_reality_tension`：理念-现实张力强度（0-1），需宏观/中观/微观、理念落地推演时高
- `linear_flow`：线性流程强度（0-1），顺序执行、无复杂博弈时高

## 二、方法论→模板映射表

| 方法论倾向 | 判定条件 | 推荐模板 |
|------------|----------|----------|
| 多主体博弈 | multi_agent_game > 0.6，或 subjects ≥ 3 且存在明显立场冲突 | selfpaw-swarm |
| 理念-现实张力 | ideal_reality_tension > 0.6，或需「目的激活」「实例化」「涌现」 | triadic-ideal-reality-swarm |
| 线性流程 | linear_flow > 0.6，且 multi_agent_game < 0.4、ideal_reality_tension < 0.4 | uas-subapp |
| 混合 | 无法明确判定 | 取最高分对应模板；同分时优先 selfpaw > triadic > uas-subapp |

## 三、理论原理与模板能力对应

| 理论原理 | selfpaw-swarm | triadic-ideal-reality-swarm | uas-subapp |
|----------|---------------|-----------------------------|------------|
| 世界模型·主体 | 五智能体（用户/关卡/决策/买单/观察） | 九智能体（宏/中/微 × 理念/现实 + 目的/实例化/验证） | 七智能体（意图/知识/运行时/Agent/系统/治理/演化） |
| 推动—反馈—反身 | 第一次否定→第二次否定→辩证融合 | 目的激活→对冲→实例化→验证进化 | intent→governance→evolution |
| 主客体博弈 | ✓ 显式对手盘、质询 | ✓ 理念 vs 现实对冲 | 隐式（治理校验） |
| 价值闭环 | 生成→质询→融合→输出 | 生成→实例化→验证→涌现 | 生成→治理→演化→输出 |

## 四、推导规则

1. **显式指定优先**：用户提供 `--template` 时，跳过推导，直接使用。
2. **世界模型先行**：未指定时，必须先执行世界模型分析，再根据 methodology_signals 选模板。
3. **可追溯**：生产报告中必须包含 world_model_analysis 输出与 methodology_signals，便于审计。

## 五、参考

- `docs/AGI_WORLD_MODEL_UAS.md`
- `docs/THEORY_SYSTEM.md`
- `.claude/skills/subapp_template_selector.md`
