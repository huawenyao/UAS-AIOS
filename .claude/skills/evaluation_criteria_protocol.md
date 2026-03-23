---
name: evaluation-criteria-protocol
description: 定义uas-subapp的四维评价标准与执行逻辑。用于：(1) 评估subapp质量 (2) 驱动自主进化 (3) 业务/产品/技术/运行效果打分 (4) 制定改进建议
---

# UAS Sub App 四维评价协议

## 技能定位

本协议定义 uas-subapp 的评价标准与执行逻辑，用于业务、产品、技术、运行效果四维打分，驱动自主进化。

## 四维定义

| 维度 | 英文 | 评价要点 |
|------|------|----------|
| **业务** | business | 目标明确度、价值闭环、主客体覆盖、成功标准可量化 |
| **产品** | product | Agent编织完整、交付物清晰、评估指标定义、工作流闭环 |
| **技术** | technology | ASUI技术底座、autonomous_agent运行时、治理完整、知识资产完整 |
| **运行效果** | operational | 执行完成、审计可追溯、输出落盘、演化就绪 |

## 配置

`configs/evaluation_criteria.json` 定义各维度权重、evolution_threshold（默认70）、各维度评分项。

## 执行

- `scripts/evaluate_evolution.py`：接收 stdin 的 run state，输出 `{ status, total_score, dimension_scores, risks, suggestions }`
- Runtime 在 `--evaluate` 时调用，结果写入 cognitive_state.evolution
- 总分低于 evolution_threshold 时 status=needs_evolution，suggestions 驱动 /evolveApply

## 自主进化驱动

1. run --evaluate → 四维打分 → 低分维度产生 suggestions
2. state_store.update_evolution 写入 total_score、dimension_scores、suggestions
3. /evolveApply 将 suggestions 回写 configs/skills
4. 下一轮 run 使用更新后的配置，形成进化闭环
