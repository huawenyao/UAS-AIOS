# Spec-4A · TA-3 可运营（Hub 先 · NocoBase 后置）

| 项 | 值 |
|----|-----|
| 状态 | 已确认（用户 2026-09-14「批准」；切入 A） |
| 日期 | 2026-09-14 |
| 服从 | [Spec-0](./2026-09-12-aios-workstudio-modules-design.md) |
| 前置 | Spec-1…3 全绿 |
| 交付 | `projects/aios-workstudio/` + `services/hub-api/` 夹具 |

**一句话：** `#/memory` `#/automation` `#/wm` 真连 `hub.ops.*`；ΠPaw 禁 Lethe 检索；自动化只产建议；**不做 NocoBase**（Spec-4b）。

**禁止：** 静默生效；真 Lethe；`connector.rotate`；改皮肤；git commit（除非用户要求）。

---

## 1. 出站

| 码 | 判据 |
|----|------|
| A8 / I-08 | `track=pipaw` 调 `hub.memory.self.search` → `MEMORY_TRACK_FORBIDDEN`（既有回归） |
| D-03 | `automation/run` 只产 findings 或 pending ChangeSet；`auto_apply=false` |
| D-05 | forget → receipt → `memory/receipt` 可检索 |
| D-01 | scaffold：三页有对应 ops path |
| D-06 | schema drift fail 时相关演化确认仍阻断（沿用 Spec-2） |

## 2. 端点

| 方法 | 路径 | 行为 |
|------|------|------|
| GET | `/hub/v1/ops/memory/receipt` | 列回执；`q` 过滤；无备忘明文 |
| POST | `/hub/v1/ops/memory/forget` | body `{actor_id,memory_id}` → FixtureMemory.forget → 存回执 + 审计 |
| GET | `/hub/v1/ops/automation/jobs` | 作业 + findings 夹具 |
| POST | `/hub/v1/ops/automation/run` | 刷新 findings；可选 `_put_pending(kind=automation.*)` |
| GET | `/hub/v1/ops/wm/list` | 寿命摘要 |
| POST | `/hub/v1/ops/wm/get` | 已有 |

frontline 仍 403。rotate / 真 NocoBase 不做。

## 3. Demo

`hub-ops.js` 补方法；`app.js` 去掉三页离线芯片；`bootHubOps` 拉 receipt/jobs/wm.list。

## 4. 验收

unittest + curl：receipt 闭环、pipaw search 403、automation pending、wm list 200；浏览器三页非空。
