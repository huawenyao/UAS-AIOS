---
name: value-loop-protocol
description: 价值闭环7步与UAS-ASUI workflow步骤的显式映射协议。用于：(1) 理解价值闭环理论 (2) 工作流映射 (3) 推动-反馈-反身螺旋 (4) 待建设项识别
---

# 价值闭环协议

## 技能定位

本协议定义**价值闭环 7 步**与 UAS-ASUI **workflow 步骤**的显式映射，标明已实现与待建设，确保闭环语义可追溯。

## 价值闭环 7 步（理论）

1. **输入**：真实世界复杂问题 + 行业专家知识
2. **模拟**：数字孪生环境中海量试错与推演
3. **生成**：多种可能方案或行动建议
4. **交互**：人类/系统评估与修正，高质量反馈
5. **进化**：修正数据回流，更新世界模型，预测更准、决策更优
6. **输出**：切中价值流的执行，优化后的 AI 代理介入现实工作流
7. **收益**：实际效益反哺系统，支持更大规模模拟与更复杂任务

## 与 Workflow 步骤的映射

| 价值闭环步骤 | 对应 workflow step(s) | 实现状态 | 说明 |
|--------------|----------------------|----------|------|
| 1. 输入 | intent_activation, knowledge_binding | ✅ 已实现 | topic + payload；configs/skills 注入 |
| 2. 模拟 | simulation（可选） | ⏳ 占位 | 无专用步骤；可扩展为 parallel 多 run 或沙箱 |
| 3. 生成 | agent_planning, runtime_topology, system_mapping | ✅ 已实现 | LLM 步骤产出方案 |
| 4. 交互 | human_review（可选） | ⏳ 占位 | 新增 step 类型；写入 database/feedback |
| 5. 进化 | evolution_plan, evaluate | ✅ 已实现 | evolution_engine + state_store.update_evolution |
| 6. 输出 | render_report | ✅ 已实现 | reports/*.md, database/**/*.json |
| 7. 收益 | （无对应） | ❌ 待建设 | 需收益指标配置与反哺接口 |

## 推动—反馈—反身与 Workflow 对应

| 演化相位 | 对应步骤 | 说明 |
|----------|----------|------|
| **推动 (Drive)** | intent_activation | 任务/目标/约束注入；资源与权限分配 |
| **反馈 (Feedback)** | 各 step 执行结果 + evaluation | 执行结果、环境反应、主体评价、客体状态 |
| **反身 (Reflexivity)** | evolution_plan | 对假设、策略、世界模型的审视与修正 |

在 evolution_policy 中可配置：
```json
{
  "evolution_phases": {
    "drive": "intent_activation",
    "feedback": ["*_step_output", "evaluation"],
    "reflexivity": "evolution_plan"
  }
}
```

## 待建设项

- **模拟**：workflow 支持 `type: "simulation"` 或 parallel 多参数推演
- **交互**：workflow 支持 `type: "human_review"`，写入 database/feedback
- **收益**：configs 中收益指标定义；evolution 可读取并驱动下一轮资源

## 参考

- `docs/THEORY_SYSTEM.md` §2.2
- `docs/THEORY_ARCHITECTURE_CONSISTENCY_AUDIT.md` §3.3
