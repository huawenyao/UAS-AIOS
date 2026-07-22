# LifeWake 脚本

| 脚本 | 作用 |
|------|------|
| `evaluate_lifewake_mvp.py` | 跑 CASE-001～008 验收 |
| `lifewake_policy.py` | 同意 / 惊喜 / 心跳 / 仪式策略 |
| `run_lifewake_pipeline.py` | workflow script 步入口（stdin JSON） |
| `render_lifewake_report.py` | 写入 `reports/` 与 `database/runs/` |
| `run_subapp.py` | 模板自带 UAS runtime 入口 |
| `evaluate_evolution.py` | 演化评估占位 |
| `render_uas_plan.py` | 通用方案渲染 |

验收：

```bash
python3 scripts/evaluate_lifewake_mvp.py
```
