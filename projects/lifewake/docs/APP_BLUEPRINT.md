# 生命回响 Sub App 蓝图

## 产品定义

**生命回响（LifeWake）** 是一面映照生命独奏的镜子，也是用户与 AI 共书史诗的旅程。MVP 聚焦：

1. **惊喜盲盒** — 潜意识回音壁：授权低敏感信号 → 静默编织 → 时机推送 → 灵感解析
2. **心跳音乐** — 生理共鸣艺术品：单人生物韵律 / 双人共鸣交响曲

技术底座：ASUI · 运行架构：autonomous_agent runtime · 规约：`docs/lifewake/`

完整产品 BP：`../../../docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md`。本文只描述
`projects/lifewake` 的可运行映射与验收入口。

## 关键闭环

```text
理念/意图 → 同意授权 → SignalBundle/设备 → 慢灵感时机 → 创作 →
RitualEnvelope → rubric 情感冲击 → 交付反馈 → ChangeSet 草案 → 收益快照
```

## UAS 映射


| 层   | 落点                                                              |
| --- | --------------------------------------------------------------- |
| I   | 惊喜探索、心跳共鸣、关系共创                                                  |
| K   | 哲学宪章、同意策略、风格与仪式模板                                               |
| R   | mock 穿戴 + mock 多模态生成                                            |
| A   | Privacy / Signal / Surprise / Pulse / Bond / Ritual / Evolution |
| S   | `lw.*` capability mesh                                          |
| G   | 用途/scope/撤回、未成年人、双向需求确认、情感 rubric 门禁                           |
| E   | wow/meh → ChangeSet（不自动写回）                                      |
| Π   | 能力契约与仪式输出协议                                                     |


## 非目标（v0.1）

- 真实设备 SDK / 真实多模态 API
- 正式移动端 UI
- 记忆时光机 / 关系纽带可视化 / 数字孪生代回（仅 reserved 接口）
- 广告画像、用户评分、原始生物流导出

## 验收

```bash
pytest -q
python scripts/evaluate_lifewake_mvp.py
python scripts/run_value_loop_prototype.py --run-id walkthrough_value_loop
python scripts/run_emotion_kpi_snapshot.py
```

CASE-001～014 覆盖正常与治理红线。原型命令必须产生运行、反馈、认知状态、
静态 HTML 仪式预览和收益快照，且 ChangeSet 只生成草案、不自动应用。