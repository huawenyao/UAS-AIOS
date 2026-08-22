# World Model Studio（ASUI subapp）

> 产品形态：认知实践的世界模型操作系统  
> ΠPaw = Business AGI **编排身份**，不是数字人聊天壳。  
> 宪章：`docs/AI_PRODUCT_CHARTER.md`

## 系统概述

岗位主体（用人经理）在五维世界模型上走完价值闭环 7 步。首屏是当前决策所需的低维结构（谁进 onsite），不是 Agent 列表。

领域情景（做深一个）：**招聘短名单 · Staff Engineer**。候选人是主体维度。

## 工作流

```
输入 → 模拟 → 生成 → 交互 → 进化 → 输出 → 收益
```

每步读写 `configs/world_model.json` 派生出的运行态，落盘到 `database/`。

## 知识层

| 文件 | 用途 |
|------|------|
| `configs/world_model.json` | 五维世界模型 + 理念/现实 + 法则 |
| `configs/cycle_policy.json` | 7 步、环位、G 级 |
| `knowledge/hiring_shortlist_laws.md` | 法则 Pack（改之即生效） |
| `.claude/skills/world_model_studio.md` | Agent 行为 |

## 验证标准

- [x] 世界模型一级公民：五维可看
- [x] 理念 vs 现实对冲
- [x] 7 步落盘，而非改对话历史
- [x] 门禁 / 环位 / 证据盒可见
- [x] ChangeSet 由体验信号生成
