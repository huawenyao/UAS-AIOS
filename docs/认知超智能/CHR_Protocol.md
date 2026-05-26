# 因果假设可靠性协议（CHR Protocol）

> CHR = **Causal Hypothesis Reliability**  
> 目标：将“因果想象力”约束为可测试、可拒绝、可审计、可回放的工程协议。  
> 定位：CHR 只管理“假设如何进入、被检验、被提交/淘汰”；不替代世界模型本体与业务策略。

---

## 1. 协议思想原理

### 1.1 核心立场

1. 世界模型不是因果真理源，而是**因果假设生成器**。  
2. 任何因果主张只有在通过验证链后，才可晋升为组织级事实。  
3. 可靠性来自**验证-淘汰循环**，不是来自某个模型参数。

### 1.2 工程等价式

`可靠因果近似 = 假设生成 × 假设检验 × 持续证伪`

其中：
- 假设生成：LLM / 规则 / 专家注入都可。
- 假设检验：逻辑一致性 + 历史回测 + 小规模现实试探。
- 持续证伪：线上观测一旦触发反例条件，自动降级或撤销。

### 1.3 四个不可妥协原则

- **P1 可检验性优先**：不可检验假设不得进入提交流水线。  
- **P2 预测与事实分离**：预测结论默认是 `hypothesis`，不是 `committed_fact`。  
- **P3 证据链必需**：高风险因果主张必须带外部证据锚。  
- **P4 可回滚**：所有提交必须可审计、可撤销、可重放。

---

## 2. 协议对象模型

### 2.1 CausalHypothesis（最小字段）

```json
{
  "hypothesis_id": "ch_20260324_001",
  "claim": {
    "cause": "active_instances",
    "effect": "cpu_util",
    "direction": "decrease",
    "magnitude": 0.15,
    "time_to_effect_s": 120
  },
  "scope": {
    "domain": "infra_ops",
    "env": "prod",
    "time_window": "2026Q1"
  },
  "confidence": 0.73,
  "evidence": [
    {
      "type": "log_ref",
      "source_id": "deploy-log-123",
      "span": "..."
    }
  ],
  "falsifier": {
    "condition": "cpu_util_increase_gt_0.1_within_300s",
    "window_s": 300
  },
  "proposer": {
    "unit_id": "ua_scheduler_01",
    "model": "reason.llm",
    "version": "v1.4.2"
  },
  "base_world_version": "wm_v_1082"
}
```

### 2.2 验证结果对象

```json
{
  "hypothesis_id": "ch_20260324_001",
  "stage_results": {
    "gate0_testability": "PASS",
    "stage1_logical": "PASS",
    "stage2_historical": "CAUTION",
    "stage3_experiment": "PASS"
  },
  "adjusted_confidence": 0.68,
  "decision": "PROVISIONAL_COMMIT",
  "reason_codes": ["HISTORICAL_SUPPORT_WEAK", "EXPERIMENT_PASS"],
  "review_required": false
}
```

---

## 3. CHR 状态机（唯一流程）

状态集合：
- `DRAFT`
- `REJECT_TESTABILITY`
- `REJECT_LOGICAL`
- `REJECT_HISTORICAL`
- `EXPERIMENT_PENDING`
- `PROVISIONAL_COMMIT`
- `COMMITTED_FACT`
- `REVOKED`

状态迁移：

1. `DRAFT` --Gate0 可检验性失败--> `REJECT_TESTABILITY`
2. `DRAFT` --Stage1 逻辑失败--> `REJECT_LOGICAL`
3. `DRAFT` --Stage1 通过--> Stage2
4. Stage2 历史支持不足：
   - 若风险低：`PROVISIONAL_COMMIT`
   - 若风险中高：`EXPERIMENT_PENDING`
   - 若强矛盾：`REJECT_HISTORICAL`
5. `EXPERIMENT_PENDING` --试探通过--> `PROVISIONAL_COMMIT`
6. `PROVISIONAL_COMMIT` --连续观测通过阈值--> `COMMITTED_FACT`
7. `PROVISIONAL_COMMIT/COMMITTED_FACT` --触发 falsifier--> `REVOKED`

---

## 4. 三重验证（含前置 Gate0）

### Gate0：可检验性门（必须先过）

检查项：
- 是否有可观测 `effect`？
- 是否有可执行干预动作（或自然实验替代）？
- 是否定义 `falsifier`？
- 是否可在 SLA 内完成验证？

任一失败 -> `REJECT_TESTABILITY`

### Stage1：逻辑一致性检验

输入：假设 + 领域公理/规则  
输出：`PASS | REJECT_LOGICAL | CAUTION`

最小规则集：
- 类型/量纲一致
- 因果方向不与硬规则冲突
- 边界条件合法（范围、阈值、时间窗）

### Stage2：历史反事实回测

输入：历史样本、相似情境索引  
输出指标：
- `direction_agreement`
- `magnitude_error`
- `sample_size`

判定建议：
- `direction_agreement >= 0.7`：支持
- `0.3 ~ 0.7`：不确定
- `< 0.3`：反驳

### Stage3：小规模现实试探

机制：分级行动（10% -> 30% -> 60%）+ 任何一步触发中止条件即停止。  
必须配置：
- 风险预算
- 安全边界
- 观察窗口
- 自动回滚动作

---

## 5. 决策与提交语义

### 5.1 三种提交级别

| 级别 | 含义 | 使用场景 |
|------|------|----------|
| `REJECTED` | 不进入共享 WM | 逻辑冲突/证据不足 |
| `PROVISIONAL_COMMIT` | 限域、限时有效 | 新机制、样本不足 |
| `COMMITTED_FACT` | 组织级事实 | 通过完整验证且稳定 |

### 5.2 提交规则

- `COMMITTED_FACT` 必须满足：
  - Stage1 = PASS
  - Stage2 = SUPPORT 或 Stage3 = PASS
  - 外部证据阈值满足（按域策略）
- 任意高风险域（资金、安全、合规）必须经过 Stage3 或人工双签。

---

## 6. 冲突消解与优先级

当多条假设竞争同一事实槽位 `(subject, predicate, window)`：

1. 先比较 `base_world_version`（OCC，过期直接拒绝）
2. 再比较证据等级（高到低）：
   - `human_signed`
   - `tool_callback_hash`
   - `external_api_idempotent`
   - `llm_with_span`
   - `llm_without_span`
3. 同等级冲突 -> `ESCALATE_REVIEW`
4. 禁止“最后写入覆盖”

---

## 7. 失效模式与降级策略

| 失效模式 | 表现 | 降级策略 |
|----------|------|----------|
| 假因果（混杂） | 历史相关高但实验失败 | 降置信 + 回到 Stage0 重定义变量 |
| 缺因果（漏边） | 长期预测偏差高 | 提升探索预算，触发候选边挖掘 |
| 错因果（方向反） | falsifier 高频触发 | 自动 `REVOKED` + 冻结该模板 |
| 验证资源不足 | Stage3 长期排队 | 风险分层，低风险先 provisional |

---

## 8. 可自动化指标（项目级 SLO）

1. `chr_testability_pass_rate`  
2. `chr_stage1_reject_rate`  
3. `chr_reject_then_amend_success_rate`  
4. `chr_provisional_to_committed_conversion_rate`  
5. `chr_falsifier_trigger_rate`  
6. `chr_mean_time_to_revocation`（发现错误因果到撤销的平均时间）

> 建议至少 5 个纳入 CI/周报；与业务 KPI 分开但关联分析。

---

## 9. 可证伪条款（项目级）

满足任一条，判定当前因果路线失败并触发路线调整：

1. 连续 3 个迭代 `chr_falsifier_trigger_rate` 高于阈值且无下降趋势。  
2. `chr_provisional_to_committed_conversion_rate` 长期接近 0（表示体系只会提案不会积累事实）。  
3. 在关键域中，CHR 后的干预效果不优于朴素基线。  
4. 出现可复现的“绕过 CHR 直接写 committed”路径。

---

## 10. 与现有仓库的落地对接

- 对接 `UACA_UniAgent_TOGAF_Architecture.md`：
  - L3 消息新增 `PROPOSAL` 子类型 `causal_hypothesis`
  - L5 提交引入 `PROVISIONAL_COMMIT` 状态
- 对接 `cognitive_practice_world_model`：
  - 在 `training/tuning.py` 增加 `falsifier` 检查钩子
  - 在 runtime 增加 `revoke_hypothesis()` 事件写回

---

## 11. 最小实施清单（两周版本）

1. 定义 `CausalHypothesis` JSON Schema v0.1。  
2. 实现 Gate0 + Stage1（规则版）。  
3. 增加 `PROVISIONAL_COMMIT` 与 `REVOKED` 两个状态。  
4. 落地 5 个 CHR 指标并接入周报。  
5. 选 1 条高价值因果链做端到端演示（提案→验证→提交→证伪/固化）。

---

## 12. 机器可读契约与样例

### 12.1 JSON Schema

- `docs/认知超智能/schemas/chr_hypothesis.schema.json`
- `docs/认知超智能/schemas/chr_validation_result.schema.json`
- `docs/认知超智能/schemas/chr_state_machine.schema.json`

### 12.2 最小样例

- 通过样例：`docs/认知超智能/examples/chr/hypothesis_pass.json`
- 拒绝样例：`docs/认知超智能/examples/chr/validation_reject.json`
- 撤销样例：`docs/认知超智能/examples/chr/validation_revoked.json`

---

*版本：CHR Protocol v0.2（含机器可读契约）*  
