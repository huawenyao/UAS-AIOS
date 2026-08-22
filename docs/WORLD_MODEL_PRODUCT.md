# 认知实践的世界模型产品化

> 产品名：**World Model Studio**  
> 编排身份：ΠPaw（Business AGI）保留名称，**不再作为数字人产品**  
> 原型：`examples/world-model-studio/`  
> 服从：[`AI_PRODUCT_CHARTER.md`](./AI_PRODUCT_CHARTER.md)  
> 日期：2026-08-18

---

## 一句话

岗位主体在五维世界模型上走完「输入→模拟→生成→交互→进化→输出→收益」；产品是**法则编译器**，不是聊天壳。

---

## 方案对比（动手前）

| 方案 | 形态 | 为何放弃 / 采用 |
|------|------|----------------|
| A. 更好的数字员工 | 人设 + 对话 + 岗位 SOP | 重复旧失败：人格先于世界模型 |
| B. 经营驾驶舱 | KPI + Agent 编制墙 | 堆面板，违反道-3 降维 |
| **C. World Model Studio（采用）** | 五维模型一级公民 + 7 步状态机 | 宪章道-1…6 可在 UI 上被违反或被遵守 |

张力表（势）：主摩擦 = **认知摩擦 U**（用户看不见模型）与 **治理/效率**（短名单是组织承诺）。环位默认 **In the loop · G3**。牺牲：不提供「全自动淘汰」。监控：未接地分数是否流入建议。

---

## 旧 ΠPaw 为何落后（仓库事实）

1. **岗位人格化先于世界模型**：`configs/pipaw_business_agent_roster.json` 以「客服数字岗位 Agent」为人设入口；世界模型不在运行时被读写。  
2. **聊天/任务台冒充工作台**：`ΠPaw_Enterprise_Demo.html` 是 Tailwind 角色工作台；`pipaw_task_panel.py` 把待办当产品。宪章 6.3 写了「工作台不是聊天」，实现仍是任务壳。  
3. **Agent 堆叠而非降维**：详设文档把战略罗盘/驾驶舱/执行助手/低代码铺开，首屏是编制而非当前决策的低维结构。  
4. **模型执行代替平台执行**：`PipawCsAgentRuntime.run_current_step` 直接 `router.invoke`，闭环停在客服步骤，不更新五维模型，也不走 7 步。  
5. **双轨口惠**：`product_track=pipaw` 存在，但产品叙事是「经营数字人」；个人轨/经营轨在 Demo 里同一套人设工作台。

结论：**产品不是数字人，而是认知实践的世界模型操作系统。**

---

## 废止（已移除的历史实现）

| 路径 | 曾是什么 |
|------|----------|
| `asui-cli/src/asui/pipaw_cs_agent.py` | 客服数字人 runtime stub |
| `asui-cli/src/asui/pipaw_task_panel.py` | 假工作台 Task Panel |
| `asui-cli/tests/test_pipaw_cs_agent.py` | 上述验收 |
| `scripts/validate_pipaw_cs_agent.py` · `scripts/pipaw_task_panel.py` | 入口脚本 |
| `configs/pipaw_business_agent_roster.json` · `configs/pipaw_cs_agent_playbook.json` | 人设编制 / SOP |
| `schemas/business_agent_roster.schema.json` · `schemas/task_panel_view.schema.json` | 编制与面板契约 |
| `docs/strategic/demo/ΠPaw_Enterprise_Demo.html` | 过时经营 Demo |
| `docs/strategic/design/ΠPaw_High_Fidelity_Prototype_Design.md` | 高保真人设原型 |
| `docs/strategic/detailed-design/ΠPaw_Business_AGI_Platform_*.md` · `ΠPaw_Full_Stack_Product_Landing_Definition.md` | 与宪章冲突的平台蓝图 |
| `harness/knowledge/technical/pipaw-cs-agent-benchmark.md` | 客服 Agent 标杆规格 |

**未删**：双轨理论、Intent Hub、`product_track` 枚举、SelfPaw、asui-cli 内核、招聘 OS / 客服模板、宪章正文（6.3 已改写）。

---

## 新产品结构

```
examples/world-model-studio/
  configs/world_model.json     五维 + 对冲 + 法则
  configs/cycle_policy.json    7 步环位
  knowledge/hiring_shortlist_laws.md
  scripts/run_cognitive_cycle.py
  ui/                          可本地打开的法则编译器
  database/                    运行落后盘
```

情景做深：**招聘短名单**（沿用招聘域候选人事实）。销售报价不在本原型展开。

---

## 宪章 §7 检核（本原型）

- [x] 落在 7 步全链；收益指标 = 可解释短名单 / 零自动淘汰 / 未接地分不进建议  
- [x] 五维齐全；候选人在 subject  
- [x] 降低认知摩擦：首屏只问谁进 onsite  
- [x] 法则可配置、可回滚（ChangeSet）  
- [x] 理想/现实同时呈现  
- [x] 岗位职责先于人设（本原型无人设 Agent）  
- [x] 只预览 `cs.*`，不执行生产写  
- [x] 默认环位 In · G3；升级条件写在 LAW-GATE-001  
- [x] 证据盒、不确定点、门禁、回滚 48h  
- [x] 高影响人确认  
- [x] 经营轨 `product_track=pipaw`，不读个人记忆  
- [x] 未接地 culture_fit 不可流出  
- [x] 驳回信号生成 ChangeSet  
