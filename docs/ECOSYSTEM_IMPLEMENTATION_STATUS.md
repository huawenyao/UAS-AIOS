# 数字人生态实现状态（原型版）

> **last_review**: 2026-07-22 · 与 [GOVERNANCE_REGISTRY.md](./GOVERNANCE_REGISTRY.md) 同步
> **SelfPaw 主实现**：[`aipos/copaw-src`](../aipos/copaw-src)（本机 `C:\Users\ranwu\XiaomiCloud\aipos\copaw-src`）— 见 [SELFPaw_REFERENCE_IMPLEMENTATION.md](./SELFPaw_REFERENCE_IMPLEMENTATION.md)

## 四层口径

| 层级 | 全生态 | Business AGI | User AGI（含 copaw-src） |
|------|--------|--------------|--------------------------|
| D1 定义 | ~90% | ~90% | ~90% |
| D2 契约 | ~68% | ~70% | ~65%（UAS 企业契约 + copaw 产品） |
| D3 可运行闭环 | ~58% | ~62% | ~70%（copaw 可独立运行；UAS 侧 L1 企业桥接 ~45%） |
| D4 生产就绪 | ~15% | ~18% | ~25%（copaw 产品级；企业租户一体化待 Wave 6） |

**口径**：User AGI **不等于**仅 `UAS-AIOS/projects/selfpaw-enterprise`；个人认知 OS 以 **copaw-src** 为准。

## User AGI Experience Domain（独立口径）

LifeWake 是 SelfPaw 下的 **生命体验域（Experience Domain）原型**，不是第三 AGI 轨，也不是企业数字人 L1/L2/L3 中的新增层级。其成熟度单独记录，**不计入上表 Business AGI 或企业 L1-L3 完成率**。

| 体验域 | D1 定义 | D2 契约 | D3 可运行闭环 | D4 生产就绪 |
|--------|---------|---------|---------------|-------------|
| LifeWake | baseline | prototype（`lw.*` + 通用 G/E/Π schemas） | prototype（MVP CASE 验收） | planned（SelfPaw Core、持久化撤回/删除、长期影响评估待闭环） |

架构边界见 `docs/strategic/LIFEWAKE_USER_AGI_EXPERIENCE_DOMAIN.md`。

## 全场景原型（`configs/ecosystem_scenario_catalog.json`）

| 场景 ID | 层级 | 验收 |
|---------|------|------|
| L1-personal-session | L1 | `run_uas_runtime_service run --app-id selfpaw-enterprise` |
| L1-escalate-to-pipaw | L1→L3 | `scripts/run_edh_dual_track_loop.py` |
| selfpaw-experience-lifewake | Experience Domain（不计入 L1-L3） | 隔离运行 `projects/lifewake/scripts/evaluate_lifewake_mvp.py` |
| L2-recruitment-os | L2 | `examples/ai-recruitment/.../run_entity_closed_loop.py` |
| L3-sales-b2b | L3 | `evaluate_sales_mvp.py` 8/8 |
| L3-cs-ticket | L3 | `test_pipaw_cs_agent.py` |
| L3-finance-approval | L3 | `run_finance_prototype.py` |
| L3-outward-notify | L3 | `run_outward_gateway_mock.py` |
| platform-value-loop | 平台 | `run_value_loop_full.py` |

一键：`python scripts/run_ecosystem_prototype.py`

## 产品原型页

浏览器打开：`docs/strategic/demo/EDH_Ecosystem_Prototype.html`
