# World Model Studio

认知实践世界模型的最小可运行原型。ΠPaw 只作为 Business AGI 编排身份保留；**产品不是数字人**。

产品定义（反思、废止清单、宪章 §7 检核）：[`docs/WORLD_MODEL_PRODUCT.md`](../../docs/WORLD_MODEL_PRODUCT.md)

## 如何本地运行

在仓库根目录：

```bash
# 1. 跑通一次 7 步闭环（读写世界模型并落盘）
python scripts/run_cognitive_cycle.py

# 2. 查看落盘
#    examples/world-model-studio/database/world_model.json
#    examples/world-model-studio/database/audits/latest.json
#    examples/world-model-studio/database/changesets/latest.json

# 3. 打开 UI（推荐本地静态服务，避免 file:// 限制）
cd examples/world-model-studio
python -m http.server 8765
# 浏览器打开 http://localhost:8765/ui/
```

用人经理驳回未接地字段（stdin）：

```bash
echo {"action":"confirm_with_uncertainty","evolve_signal":"reject_ungrounded_culture_fit"} | python scripts/run_cognitive_cycle.py --stdin
```

对照学历硬门槛方案（应被法则拦住，短名单不冻结）：

```bash
echo {"action":"choose_degree_hard"} | python examples/world-model-studio/scripts/run_cognitive_cycle.py --stdin
```

## 对照宪章 §7

见 `docs/WORLD_MODEL_PRODUCT.md` §检核。本原型声明：

| 条款 | 本情景 |
|------|--------|
| 道-1 | 7 步全走；北极星 quality-adjusted hiring success |
| 道-2 | 五维在 UI 与 JSON 同时可见；候选人在 subject |
| 道-3 | 首屏只暴露「谁进 onsite」 |
| 道-4 | 法则在 `knowledge/hiring_shortlist_laws.md` |
| 道-5 | `product_track=pipaw`；不读 SelfPaw 个人记忆 |
| 道-6 | 理念/现实对冲；culture_fit 默认值被剥离 |
| 红线-4 | 冻结短名单 In the loop · G3 |
| 德-组织-3 | `cs_preview.executed=false` |
