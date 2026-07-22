# LifeWake 脚本

| 脚本 | 作用 |
|------|------|
| `evaluate_lifewake_mvp.py` | 跑 CASE-001～014 行为验收 |
| `lifewake_policy.py` | 同意 / SignalBundle / 时机 / 情感 / Bond 策略 |
| `run_value_loop_prototype.py` | 运行并持久化完整最小价值闭环 |
| `run_emotion_kpi_snapshot.py` | 从运行事实聚合情感与治理 KPI |
| `run_lifewake_pipeline.py` | workflow script 步入口（stdin JSON） |
| `render_lifewake_report.py` | 写入 `reports/` 与 `database/runs/` |
| `run_subapp.py` | 模板自带 UAS runtime 入口 |
| `evaluate_evolution.py` | 演化评估占位 |
| `render_uas_plan.py` | 通用方案渲染 |

验收：

```bash
python3 scripts/evaluate_lifewake_mvp.py
pytest -q
python3 scripts/run_value_loop_prototype.py
python3 scripts/run_emotion_kpi_snapshot.py
```
