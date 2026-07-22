# LifeWake（生命回响）

情感共创型 UAS 子应用。完整产品 BP 见
[`LIFEWAKE_PRODUCT_BLUEPRINT.md`](../../docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md)，
项目实现摘要见 [`docs/APP_BLUEPRINT.md`](docs/APP_BLUEPRINT.md)。

## 快速验证

```bash
cd projects/lifewake
python3 scripts/evaluate_lifewake_mvp.py
pytest -q
python3 scripts/run_value_loop_prototype.py --run-id walkthrough_value_loop
python3 scripts/run_emotion_kpi_snapshot.py
```

```bash
python3 ../../scripts/run_uas_runtime_service.py list --projects-root projects
```

## MVP 能力

| 能力 | 说明 |
|------|------|
| `lw.surprise.compose` | 惊喜盲盒 |
| `lw.pulse.compose` | 单人心跳音乐 |
| `lw.pulse.duet` | 双人共鸣交响曲 |
| `lw.consent.check` | 同意门禁 |
| `lw.ritual.render` | 自我确认仪式 + wow 校验 |

## 可验证价值闭环

`run_value_loop_prototype.py` 一次完成输入、模拟、生成、反馈、
ChangeSet 草案、RitualEnvelope 输出与收益快照，并分别持久化到
`database/runs/`、`database/feedback/`、`database/cognitive_state/` 和
`reports/`。HTML 仪式报告可直接用浏览器打开。

验收覆盖 CASE-001～014：正常惊喜、同意缺失/撤回、solo/duet、非双向、
connector 恢复、低情感冲击、慢灵感延后、共享撤回、反馈演化链、
未成年人、设备断连和违规用途。
