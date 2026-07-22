# 生命回响 Sub App 蓝图

## 产品定义

**生命回响（LifeWake）** 是一面映照生命独奏的镜子，也是用户与 AI 共书史诗的旅程。MVP 聚焦：

1. **惊喜盲盒** — 潜意识回音壁：授权低敏感信号 → 静默编织 → 时机推送 → 灵感解析
2. **心跳音乐** — 生理共鸣艺术品：单人生物韵律 / 双人共鸣交响曲

技术底座：ASUI · 运行架构：autonomous_agent runtime · 规约：`docs/lifewake/`

## 关键闭环

```text
同意授权 → 信号/设备就绪 → lw.surprise | lw.pulse → 仪式渲染 → 情感冲击校验 → 审计 / ChangeSet
```

## UAS 映射

| 层 | 落点 |
|----|------|
| I | 惊喜探索、心跳共鸣、关系共创 |
| K | 哲学宪章、同意策略、风格与仪式模板 |
| R | mock 穿戴 + mock 多模态生成 |
| A | Privacy / Signal / Surprise / Pulse / Bond / Ritual / Evolution |
| S | `lw.*` capability mesh |
| G | 用途限制、撤回、双向门禁、wow 门禁 |
| E | wow/meh → ChangeSet（不自动写回） |
| Π | 能力契约与仪式输出协议 |

## 非目标（v0.1）

- 真实设备 SDK / 真实多模态 API
- 正式移动端 UI
- 记忆时光机 / 关系纽带可视化 / 数字孪生代回（仅 reserved 接口）
- 广告画像、用户评分、原始生物流导出

## 验收

`python scripts/evaluate_lifewake_mvp.py` → CASE-001～008 全部通过。
