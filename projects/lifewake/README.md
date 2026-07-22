# LifeWake（生命回响）

情感共创型 UAS 子应用。产品规约见仓库 [`docs/lifewake/`](../../docs/lifewake/)。

## 快速验证

```bash
cd projects/lifewake
python3 scripts/evaluate_lifewake_mvp.py
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
