# 基于 UAS-AIOS 的 Projects 自动进化与认知实践闭环实现指南

> 如何实现 projects 的自动进化、完成认知实践闭环，并朝向世界顶级 AI 产品演进。

---

## 一、目标与定位

- **Projects 自动进化**：在 UAS-AIOS 架构下，各 sub uas app（如 `projects/ai-recruitment-os`）按**演化策略**自动执行「意图→治理→进化规划→评估→漂移处理→认知状态更新」，无需人工逐轮触发。
- **认知实践闭环**：将理论中的**认知实践论**（实践→表征→反思→再实践）与**价值闭环 7 步**（输入→模拟→生成→交互→进化→输出→收益）工程化落地，形成「执行→反馈→反身→再执行」的可持续循环。
- **世界顶级 AI 产品**：通过闭环持续降低**三元摩擦**（认知 U、执行 A、知识 S），在**目的守恒**与**治理可审计**前提下，让产品在真实场景中不断逼近帕累托最优，实现范式级竞争力。

---

## 二、架构映射：UAS-AIOS 中的「进化」与「认知」

### 2.1 已有构件（可直接复用）

| 构件 | 位置 | 作用 |
|------|------|------|
| **E 演化回路** | `evolution_policy.json` + `evaluate_evolution.py` / `evaluate_iteration.py` | 目标守恒、漂移规则、评估阈值、迭代环 default_loop |
| **业务回路执行器** | `projects/ai-recruitment-os/scripts/business_loop_runner.py` | 按 default_loop 执行 intent_activation → governance_check → evolution_plan，写观测与评估 |
| **认知状态** | `CognitiveStateStore`、`database/cognitive_state/{topic}.json` | 持久化 intent、evaluation、evolution、timeline，供反身与下一轮推动 |
| **观测** | `database/observability/loop_runs/{run_id}/` | run_summary、evaluation、steps、drift_events，全流程可审计 |
| **治理** | `governance_policy.json` + `evaluate_evolution.py` | 平台标准校验（ASUI、autonomous_agent、治理控制、演化回路） |

### 2.2 认知实践闭环在 UAS 中的对应

| 认知实践论阶段 | 价值闭环 7 步 | UAS-AIOS 实现 |
|----------------|---------------|----------------|
| **实践** | 输入、模拟、生成 | I 意图激活 + K 知识绑定 + A 规划 + S 执行（workflow 前段） |
| **表征** | 生成、输出 | step_outputs、plans、reports 写入 database/reports |
| **反馈** | 交互、进化 | G 治理校验 + E 演化评估（evaluate_evolution / evaluate_iteration） |
| **反身** | 进化 | evolution_plan、drift_rules、CognitiveStateStore.update_evolution、purpose_anchor 扩展 |
| **再实践** | 收益反哺、下一轮输入 | 下一轮 business_loop_runner 或 /evolve 时读取 cognitive_state + plans |

闭环是否「完成」的判据：**每一轮运行都有「推动→反馈→反身」的显式记录，且反身结果写回知识/计划/认知状态，下一轮推动能读到**。

---

## 三、Projects 自动进化的实现要点

### 3.1 单项目闭环（以 ai-recruitment-os 为例）

当前已具备：

1. **触发**：手动执行 `python scripts/business_loop_runner.py`。
2. **回路**：`intent_activation` → `governance_check` → `evolution_plan`。
3. **评估**：`run_evaluate_iteration(plan, evolution_policy)` → status / risks / missing_purpose_keywords。
4. **漂移处理**：`apply_drift_rule` → 写入 `drift_events.json`，得到 actions（如 return_to_purpose_activation）。
5. **观测**：`run_summary.json`、`evaluation.json`、steps、drift_events 写入 `loop_runs/{run_id}/`。

**缺失的「自动」与「认知闭环」**：

- **自动**：无定时/事件驱动的调度，未在方案或代码变更时自动跑一轮。
- **认知回写**：`business_loop_runner` 未在评估/漂移后**写回** `database/plans/` 或 `database/cognitive_state/`，evolution 报告（如 evolution_20260315.md）多为人工或单次脚本生成。

### 3.2 实现自动进化的三块工作

#### （1）评估与漂移后写回认知状态与计划

- 在 `business_loop_runner.py` 的 `run_evaluate_iteration` 与 `apply_drift_rule` 之后：
  - 若存在 `CognitiveStateStore` 或等价接口：调用 `update_evaluation(evaluation)`、`update_evolution({ "drift_actions": actions, "risks": evaluation["risks"], "suggestions": evaluation["suggestions"] })`，并 `snapshot()`。
  - 若需**自动修正计划**（如 purpose_anchor 补全）：在 `needs_evolution` 且 action 为 `return_to_purpose_activation` 时，根据 `evolution_policy.goal_guard.required_purpose_keywords` 与当前 `plan.purpose_anchor` 生成补全建议或直接补全，写回 `database/plans/ai-full-cycle-recruitment-os.json`（可先写备份再覆盖）。
- 这样「反身」结果持久化，下一轮「推动」可读。

#### （2）自动触发方式（选一种或组合）

- **定时**：cron / Task Scheduler 定期执行 `python scripts/business_loop_runner.py`（如每日/每周）。
- **事件驱动**：在 git pre-push、或 CI 中「方案/配置变更」时运行 `business_loop_runner`，失败则阻断或仅报错。
- **平台级调度**：在 UAS 平台层增加「Evolution Scheduler」服务，按 `evolution_policy.iteration.schedule`（需在 evolution_policy 中扩展）对已注册的 sub uas app 轮询执行业务回路。

#### （3）多项目统一进化（跨 projects）

- 在仓库根或平台层维护 **project registry**（如 `projects/registry.json` 或 `.service_registry`），列出所有 sub uas app 及各自 `scripts/business_loop_runner.py` 路径。
- 统一调度脚本：遍历 registry，对每个 project 执行其 `business_loop_runner`，汇总各项目的 `evaluation_status`、`drift_actions`，写总览报告（如 `reports/evolution_portfolio_{date}.md`）。
- 这样「projects 自动进化」从单项目扩展到**全仓/全平台**。

---

## 四、认知实践闭环的完整链路（可落地检查清单）

1. **推动**  
   - 输入：议题/目标、当前 plan、cognitive_state。  
   - 执行：intent_activation（及可选 knowledge_binding、agent_planning 等）。  
   - 输出：更新 intent / purpose_anchor，写入 cognitive_state 或 plans。

2. **执行**  
   - 执行：runtime_topology、system_mapping、业务步骤（如招聘 OS 的筛选/面试/评价）。  
   - 输出：step_outputs、报告、数据库记录。

3. **反馈**  
   - 执行：governance_check、evaluate_iteration（及 evaluate_evolution）。  
   - 输出：evaluation（status、risks、suggestions、missing_purpose_keywords）、governance 结果。

4. **反身**  
   - 执行：evolution_plan、apply_drift_rule；根据 actions 更新 plan 或知识（如 purpose_anchor、success_metrics）。  
   - 输出：evolution 写入 cognitive_state；必要时写回 plans、reports（如 evolution_YYYYMMDD.md）。

5. **再实践**  
   - 下一轮：读取更新后的 cognitive_state 与 plans，重新从「推动」开始；或由人/调度器触发下一轮。

**闭环完成标志**：上述 5 步在单次或连续两次运行中全部发生，且 4 的写回在 5 中可被读取。

---

## 五、从闭环到「世界顶级 AI 产品」的衔接

- **价值闭环 7 步**（输入→模拟→生成→交互→进化→输出→收益）中，当前实现较强的是：输入、生成、进化、输出；**模拟**（数字孪生/沙箱）、**交互**（人机协同评估）、**收益**（效益反哺系统）在一致性审计中仍为部分或缺失。
- **产品级建议**：
  - **模拟**：在关键业务（如招聘）中引入「沙箱运行」或「影子评估」，用历史/合成数据跑闭环，不直接动生产，再对比评估结果与真实结果。
  - **交互**：在 evolution_plan 或评估后增加「人机协同」节点：关键漂移动作需人工确认或修正，再写回认知状态/计划；将人的反馈纳入 timeline。
  - **收益**：在 success_metrics 中增加业务结果指标（如录用质量、周期、候选人体验），从数据库或报表中自动采集，与 evaluation_thresholds 对照，驱动 evolution_policy 的阈值或 goal_guard 的迭代。
- **三元摩擦**：  
  - 认知摩擦 (U)：通过 CLAUDE.md、skills、intent_activation 与 purpose_anchor 的持续校准降低。  
  - 执行摩擦 (A)：通过 ASUI 知识驱动编排、autonomous_agent 与业务回路自动化降低。  
  - 知识摩擦 (S)：通过显式知识库、evolution 反身更新 success_metrics 与领域 skills 降低。  
  自动进化 + 认知闭环的本质，就是**持续用反馈与反身缩小这三类摩擦**，使产品在约束 C(t) 下逼近帕累托最优，形成**范式级**竞争力。

---

## 六、建议的下一步（优先级）

| 优先级 | 动作 | 说明 |
|--------|------|------|
| P0 | 在 business_loop_runner 中增加「评估/漂移后写回 cognitive_state 与（可选）plans」 | 先闭合单项目认知反身回路 |
| P1 | 在 evolution_policy 或 business_loop_config 中增加「自动应用」策略：当 action=return_to_purpose_activation 时自动补全 purpose_anchor 并写回 plan | 减少人工，进化可自动修正目的漂移 |
| P2 | 引入定时或事件驱动调度，定期/按变更执行 business_loop_runner | 实现「projects 自动进化」的触发自动化 |
| P3 | 建立 project registry + 统一进化脚本，生成全仓 evolution 总览报告 | 多项目统一观测与进化 |
| P4 | 在关键业务中接入「模拟」「交互」「收益」环节，并纳入评估与 evolution_policy | 与价值闭环 7 步和世界顶级产品目标对齐 |

---

## 七、相关文档索引

| 主题 | 文档 |
|------|------|
| 理论体系与价值闭环 | [docs/THEORY_SYSTEM.md](./THEORY_SYSTEM.md) |
| ASUI 架构与演化 | [docs/ASUI_ARCHITECTURE.md](./ASUI_ARCHITECTURE.md) |
| 业务回路与观测 | [projects/ai-recruitment-os/docs/业务回路与观测.md](../projects/ai-recruitment-os/docs/业务回路与观测.md) |
| 理念与实现一致性 | [docs/THEORY_ARCHITECTURE_CONSISTENCY_AUDIT.md](./THEORY_ARCHITECTURE_CONSISTENCY_AUDIT.md) |
| 招聘 OS 进化报告示例 | [projects/ai-recruitment-os/reports/evolution_20260315.md](../projects/ai-recruitment-os/reports/evolution_20260315.md) |

---

*本文档随 UAS-AIOS 演化机制与认知闭环的落地而更新。*
