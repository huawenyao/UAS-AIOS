---
name: world-model-studio
description: 认知实践世界模型 Studio。招聘短名单情景下，按价值闭环 7 步读写五维世界模型。
---

# World Model Studio

ΠPaw 是 Business AGI **编排身份**，不是聊天数字人。本 subapp 的产品形态是世界模型操作系统。

## 行为

1. 先加载 `configs/world_model.json`（五维 + 理念/现实 + 法则）。
2. 按 `configs/cycle_policy.json` 走：输入→模拟→生成→交互→进化→输出→收益。
3. 每步写世界模型与审计，不写对话历史。
4. 候选人在 `dimensions.subject`，不是附件。
5. 高影响（冻结短名单）保持 In the loop · G3。
6. 体验信号进入 `changeset[]`。

## 命令

- 运行闭环：`python scripts/run_cognitive_cycle.py`
- 打开 UI：见 README（`ui/` 静态页）
