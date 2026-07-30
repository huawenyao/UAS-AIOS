# ΠPaw 场景套件 Demo · 商业叙事与产品化闭环

> **版本**：v3.0 · 2026-07-05  
> **定位**：可售卖岗位 Agent 场景包（非平台愿景 Demo）  
> **载体**：`ΠPaw_Enterprise_Demo.html`  
> **配置**：`configs/commercial_scenario_catalog.json`

---

## 1. 产品定位（客户能听懂的一句话）

> **在你现有 CRM / OA / IM 之上**，用「岗位 Playbook + 可审计 cs.*」交付**可量化 ROI** 的场景套件；90 天 PoC 可验收，不替换地主系统。

| 不卖 | 要卖 |
|------|------|
| 企业经营 OS / 世界模型 | **客服 SLA 套件**、**B2B LTC 套件** |
| 战略罗盘首单 | 一线 Task Panel + Playbook |
| 架构先行 | Day-1 集成清单 + 验收报告 |

平台能力（UAS Kernel、四适配层、经营闭环）折叠在 **IT 交付** 视图，作为第二阶段扩面。

---

## 2. 商业闭环（Demo 主路径）

```
选场景 → 证价值 → 连系统 → 跑试点 → 验收扩面
  │        │        │        │         │
 SKU卡   ROI测算  集成勾选  Playbook  JSON验收报告
```

| 步骤 | 页面 | 动作 |
|------|------|------|
| **选场景** | 场景中心 | 选择「客服 SLA」或「B2B LTC」套件 |
| **证价值** | 场景中心 | ROI 测算器调参，获取年化收益/增量营收 |
| **连系统** | 场景中心 | 勾选 Day-1 必填集成（飞书/CRM/BPM/OA） |
| **跑试点** | 一线工作台 | 「一键跑试点」→ 逐步执行 Playbook cs.* |
| **验收扩面** | 场景中心 | 「生成验收报告」→ 扩面路径建议 |

---

## 3. 场景套件 SKU

### kit-cs-sla · 客服 SLA 岗位 Agent

| 项 | 内容 |
|----|------|
| **买家** | 客服负责人 / 运营 VP |
| **痛点** | 多渠道客诉、SLA 人工盯、审计缺失 |
| **价值** | 首响 ≤1h · SLA ≥95% · 审计 100% |
| **集成** | 飞书 IM → Outward Gateway · ITSM · CRM 画像 |
| **Playbook** | `playbook.cs_complaint_v1` |
| **Demo** | `demoCsEscalation()` |

### kit-b2b-ltc · B2B 报价审批 LTC

| 项 | 内容 |
|----|------|
| **买家** | 销售运营 / BU 负责人 |
| **痛点** | 报价周期长、审批卡 OA、Margin 与执行脱节 |
| **价值** | 报价 ≤5 天 · 赢单率 +8pp · 事前 Gate |
| **集成** | CRM 线索 · BPM 报价 · OA 折扣审批 |
| **Playbook** | `playbook.sales_ltc_quote_v1` |
| **Demo** | `demoLtcPlaybook()` |

---

## 4. 信息架构（商业叙事优先）

| 导航 | 面向 | 内容 |
|------|------|------|
| **场景中心** | 采购/业务负责人 | SKU · ROI · 集成 · 验收 |
| **一线工作台** | 客服/BD/运营 | Task Panel · Playbook · cs.* 审计 |
| **管理看板** | 部门负责人 | 待办 · 异常 · 战役进度 |
| **经营闭环** | 第二阶段 | PAC Margin · 双闭环 · 战略扩展 |
| **IT 交付** | 架构师/实施 | cs.* 目录 · Outward Gateway · UAS |

---

## 5. Harness 技术底座（IT 视图）

Demo 内嵌运行时仍对齐 `configs/` + `schemas/`：

| 模型 | 配置 | API |
|------|------|-----|
| WorkingTask | `working_task.schema.json` | `EnterpriseRuntime.workingTasks` |
| Playbook | `pipaw_*_agent_playbook.json` | `advancePlaybookStep()` |
| cs.* | `capability_registry.json` | `invokeCapability()` |
| Fixtures | `fixtures/` | `demoFromRuntimeFixtures()` |

---

## 6. 本地运行

```bash
python3 scripts/export_demo_harness_fixtures.py
node docs/strategic/demo/_check_js.mjs
cd docs/strategic/demo && python3 -m http.server 8080
# 打开 ΠPaw_Enterprise_Demo.html → 默认进入「场景中心」
```

---

## 7. 扩面路径

| 阶段 | 售卖物 | Demo 入口 |
|------|--------|-----------|
| **Phase-0** | 单场景套件 PoC | 场景中心 |
| **Phase-1** | 多场景 + 经营闭环 | 经营闭环 |
| **Phase-2** | 平台 + 四适配配置 | IT 交付 · 组织适配 |

---

*Demo 数据为模拟态；商业闭环叙事对齐中国 B2B SaaS 采购决策：场景楔子 → ROI → 集成 → 试点验收。*
