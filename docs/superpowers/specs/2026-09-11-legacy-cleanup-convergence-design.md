# 遗留清理与新版本收敛 · 设计方案

| 项 | 值 |
|----|-----|
| 日期 | 2026-09-11 |
| 状态 | 已确认，待实现 |
| 范围 | 全仓（清理 + 冲突消解 + 工程收敛） |
| 非目标 | 不实现新功能、不落地 M13–M24 真实零件、不做 git 提交 |

---

## 0. 目标与非目标

**目标**：
1. 删除失效的历史版本文件（旧栈代码、早期战略稿、重复产物）。
2. 消解新旧栈冲突（路径漂移、索引断链、`demo/` 半途重构、文档互指）。
3. 新版本工程收敛：**门禁 24 → 17 项，剩余 17/17 全绿**。

**非目标**：不实现新功能；不落地 M13–M24 真实零件；不执行任何 git 提交/分支操作。

---

## 1. 背景

仓库处于**战略换轨交割期**：HEAD 为旧栈（`asui-cli` ASUI 引擎）体系，工作区中几乎完整的**新栈**（`services/hub-api` Hub family、`harness/requirements/REQ-UAS-M01~M24`、`docs/strategic/design/*`、`schemas/protocol/`、`configs/protocol/`、`deploy/`）**全部未提交**。由此产生三类问题：

1. **失效历史文件**：旧栈代码、早期战略稿、重复产物仍在仓库中。
2. **冲突**：文档路径漂移、索引断链、`demo/` 半途重构、新旧栈文档互相指向。
3. **门禁失效**：`harness/invariants/run-all.py` 22/24（exit 1），违反其自订"禁止手工验收"的治理规则。

### 1.1 关键事实（实测）

- 门禁基线：`run-all.py` → 22/24 passed，exit 1。失败项：`uas_aios_phase_a`（缺 `demo/hub-pack-open.fixture.json`）、`ecosystem_prototype`（缺 `projects/selfpaw-enterprise`）。
- `asui-cli` **是门禁硬依赖**：`run-all.py` 5 处校验要求其文件存在并以 `cwd=asui-cli` 跑 pytest；11 个 `scripts/*.py` 以 `sys.path.insert(0, ".../asui-cli/src")` 注入。
- `demo/` 被 **24 份 `harness/slices/M*.md`** + `test_phase_a` + `entity-map.json` + 架构文档共同引用，是 M1 权威落点；工作区已将其删除，新版单文件工作台悬于项目根且引用**不存在的** `./nexus-ui.css`。
- CLAUDE.md 索引 8 处断链，其中 **4 处实为文件移动**（`docs/X` → `docs/strategic/design/X`），1 处为重复副本（`AIOS BP V1.0` 已在 `docs/商业经营/`）。

---

## 2. 决策记录

| ID | 决策 | 理由 | 代价 |
|----|------|------|------|
| **DEC-1** | `asui-cli` **全量删除**（方案 A） | 用户明确要求彻底清理 | 门禁 24 → 17 项，6 个领域失去自动化验证（含 1 项本已失败的 `ecosystem_prototype`） |
| **DEC-2** | 根目录 4 份旧战略稿删除 | 消除根目录堆文档；1 份为重复副本 | 需同步修改约 8 处引用 |
| **DEC-3** | examples 历史产物删除 | iter 快照为重复产物；memory 无引用 | 无（不触碰门禁依赖） |
| **DEC-4** | `demo/` **保留重构，全面改指向** | 尊重用户近期重构意图 | 需改 24+ 处引用 |
| **DEC-5** | CLAUDE.md 索引重建 | 消除系统性误导 | 无 |
| **DEC-6** | 本次**不执行任何 git 提交/分支操作** | 遵循项目操作规范 | 变更仅落工作区 |

---

## 3. 删除清单

### D1 · asui-cli 全量（DEC-1）

删除：`asui-cli/` 整个目录（5042 LOC）。

**级联修改 `harness/invariants/run-all.py`** —— 移除以下 **7 个** check 函数及其在 `checks` 列表中的注册：

| # | 函数 | 依赖 | 当前状态 |
|---|------|------|---------|
| 1 | `check_system_connectors` | `asui/connectors/router.py` + `cwd=asui-cli` pytest | PASS → 破 |
| 2 | `check_intent_escalation` | `asui/intent_hub.py` + `cwd=asui-cli` pytest | PASS → 破 |
| 3 | `check_org_identity_binding` | `cwd=asui-cli` pytest | PASS → 破 |
| 4 | `check_dual_track_loop` | `cwd=asui-cli` pytest + `run_edh_dual_track_loop.py` | PASS → 破 |
| 5 | `check_enterprise_sales_runtime` | `run_uas_runtime_service.py`（注入 asui 路径） | PASS → 破 |
| 6 | `check_uas_runtime_list` | `run_uas_runtime_service.py`（list 模式亦强制 `load_service()`） | PASS → 破 |
| 7 | `check_ecosystem_prototype` | `run_uas_runtime_service.py` + `run_edh_dual_track_loop.py` + `run_finance_prototype.py` + `run_outward_gateway_mock.py` | 已 FAIL（缺 selfpaw-enterprise） |

> **审查更正**：初稿误记为 5 项。实测 `run_uas_runtime_service.py:36` 无条件调 `load_service()`（内含 `from asui.engine import UASRuntimeService`），故 `list` 模式同样依赖 asui；`run_ecosystem_prototype.py` 另引用 4 个待删脚本。

**级联清理**：`configs/ecosystem_scenario_catalog.json` 中指向已删脚本的 runner 条目同步移除或标注。

**级联删除 11 个脚本**：

```
scripts/validate_connectors.py
scripts/validate_intent_escalation.py
scripts/validate_org_identity.py
scripts/validate_domain_binding.py
scripts/run_edh_dual_track_loop.py
scripts/run_uas_runtime_service.py
scripts/create_sub_uas_app.py
scripts/escalate_intent.py
scripts/invoke_capability.py
scripts/run_finance_prototype.py
scripts/run_outward_gateway_mock.py
```

> 实现时须逐一确认无其他 invariant 间接调用；若发现，同步清理。

### D2 · 根目录旧战略稿（DEC-2）

```
AIOS — 企业智能经营操作系统产品 BP V1.0.md   # 与 docs/商业经营/ 重复
UAS_AIOS_ARCHITECTURE.md                     # 被 5 处引用
ASUI_STRATEGY.md                             # 被 3 处引用
AI_APPLICATION_PARADIGM_REPORT.md            # 被 3 处引用
```

同步修改引用（`docs/THEORY_SYSTEM.md`、`docs/AI_PRODUCT_CHARTER.md`、`docs/AGI_WORLD_MODEL_UAS.md`、`docs/UAS_STRATEGIC_ROADMAP_OPENSOURCE_VS_COMMERCIAL.md`、`docs/商业经营/COMPANY_OPERATING_STRATEGY.md`、`docs/商业经营/whitepaper/UAS_AIOS_WHITEPAPER_CN.md`）：改为指向 `docs/strategic/design/` 下的新文档，或删除该引用句。

### D3 · examples 历史产物（DEC-3）

```
examples/ai-recruitment/.reqharness/snapshots/iter_1 .. iter_6   # 3.1M
examples/memory/                                                  # 24K
```

> 已验证 `check_recruitment_entity_loop` 仅调用 `examples/ai-recruitment/scripts/run_entity_closed_loop.py`，不读 snapshots。

### D4 · 废弃文档残留引用

清理以下文件名的全部引用（文件本身已删或从未存在）：

```
GOVERNANCE_REGISTRY.md
ECOSYSTEM_IMPLEMENTATION_STATUS.md
TEMPLATE_PROJECT_RELATIONSHIP.md
CROSS_BORDER_AD_AGENT_SWARM_PLAN.md
CROSS_BORDER_TRIADIC_PRODUCT_BLUEPRINT.md
AI_RECRUITMENT_TRIADIC_SWARM_PLAN.md
docs/enterprise-sales-os/README.md        # 索引指向但不存在
```

---

## 4. 冲突消解

### C1 · demo/ 改指向（DEC-4）

**新权威路径**：`projects/aios-workstudio/WorkStudio/`

动作：
1. 迁移 `projects/aios-workstudio/客户经理LTC工作台.html` → `projects/aios-workstudio/WorkStudio/index.html`
2. 新建 `projects/aios-workstudio/WorkStudio/nexus-ui.css`（内容取自 HEAD 的 `projects/aios-workstudio/demo/workstudio.css`）
3. 删除根目录游离副本
4. 改指向以下引用（`demo/` → `WorkStudio/`）：

```
harness/slices/M1.md .. M24.md                    # 24 份，各 1 处
harness/requirements/REQ-UAS-M01.req.md:54
harness/entity-map.json:261
harness/knowledge/technical/uas-aios-module-delivery.md:173,174
docs/strategic/design/UAS_AIOS_ARCHITECTURE_SPEC.md:529
docs/strategic/design/UAS_AIOS_MODULE_DESIGN.md:48,78
scripts/slice_module.py
scripts/export_hub_pack_open.py                   # OUT_JSON / OUT_JS
services/hub-api/tests/test_phase_a.py:190
```

5. 运行 `python scripts/export_hub_pack_open.py` 生成 `WorkStudio/hub-pack-open.fixture.json` + `.js`

### C2 · CLAUDE.md 索引重建（DEC-5）

- 4 份移动文档修正路径：`docs/{X}` → `docs/strategic/design/{X}`
  - `UAS_AIOS_ENTERPRISE_AGENT_ECOSYSTEM_L1_L3.md`
  - `UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md`
  - `UAS_AIOS_ENTERPRISE_VISUAL_BLUEPRINT.md`
  - `UAS_ASUI_PROTOCOL_GAPS_AND_ROADMAP.md`
- 移除已删条目：`docs/GOVERNANCE_REGISTRY.md`、`docs/ECOSYSTEM_IMPLEMENTATION_STATUS.md`、`docs/enterprise-sales-os/README.md`（或改为实际路径）
- 补入新架构文档：`docs/strategic/design/` 下 7 份 + `docs/superpowers/specs/`
- 逐条验证路径存在性

### C3 · asui-cli 引用改指（DEC-1 衍生）

20 份文档中指向 `asui-cli/...` 的引用 → 改为 `services/hub-api/...` 或删除。含：

```
.claude/skills/subapp_producer_protocol.md
docs/AI_PRODUCT_CHARTER.md
docs/SELFPaw_REFERENCE_IMPLEMENTATION.md
docs/strategic/UAS_AIPOS_SelfPaw_Integrated_Product_Tech_Architecture.md
docs/UAS_STRATEGIC_ROADMAP_OPENSOURCE_VS_COMMERCIAL.md
docs/WORLD_MODEL_PRODUCT.md
docs/商业经营/COMPANY_OPERATING_STRATEGY.md
docs/商业经营/whitepaper/UAS_AIOS_WHITEPAPER_CN.md
examples/triadic-ideal-reality-swarm/docs/UAS_SUBAPP_建设规划.md
harness/entity-map.json
harness/state.json
harness/knowledge/technical/cs-process-semantic-api.md
harness/knowledge/technical/edh-platform-baseline.md
harness/knowledge/technical/intent-escalation-api.md
harness/knowledge/technical/system-connector-spec.md
harness/requirements/REQ-EDH-PL-007.req.md
harness/requirements/REQ-EDH-SP-003.req.md
harness/requirements/REQ-UAS-M14.req.md
projects/enterprise-sales-os/scripts/run_subapp.py
projects/lifewake/scripts/run_subapp.py
projects/README.md
README.md
```

> 涉及 `REQ-EDH-*` 的需求文档需判断：其对应能力若随 asui-cli 退役，则标注废弃；否则改指新实现。

---

## 5. 验收标准

| # | 标准 | 验证命令/方式 |
|---|------|--------------|
| **A1** | 门禁 17/17 全绿 | `python harness/invariants/run-all.py` → 17/17，exit 0 |
| **A2** | CLAUDE.md 索引零断链 | 逐条提取路径并验证存在性 |
| **A3** | 全仓无 asui-cli 悬空引用 | `grep -rn "asui-cli" --include="*" .` → 空 |
| **A4** | demo 链路可用 | `python scripts/export_hub_pack_open.py` 成功；`test_phase_a` 通过 |
| **A5** | 根目录归位 | 根目录仅余 `CLAUDE.md`、`README.md`（及 `.gitignore` 等配置） |
| **A6** | 无悬空引用 | D2/D4 涉及的文件名在全仓 grep 为空 |
| **A7** | index.html 无破损引用 | `WorkStudio/index.html` 引用的 `nexus-ui.css` 存在 |

---

## 6. 风险与回退

| 风险 | 影响 | 缓解 |
|------|------|------|
| 删除不可逆 | 已提交内容需 `git revert` | 变更仅落工作区，不提交；建议先行 `git stash`/提交做检查点 |
| 门禁覆盖下降 | 5 个领域失去自动验证 | 已明示；后续如需恢复，须按方案 C 移植内核（另立计划） |
| 引用遗漏 | 新断链 | A2/A3/A6 三项 grep 验收兜底 |
| `nexus-ui.css` 派生不符 | UI 样式偏差 | 取自 HEAD `workstudio.css`，非新造 |

---

## 7. 实现顺序（供 writing-plans 展开）

1. **先建检查点认知**：确认工作区状态，避免误删未提交成果
2. **C1 demo 改指向** + 生成 fixture —— 先让 `uas_aios_phase_a` 复绿（2 项失败之一）
3. **D3 examples 清理**（低风险、无级联）
4. **D1 asui-cli 删除 + invariant/scripts 级联**
5. **D2/D4 文档与引用清理**
6. **C3 asui-cli 引用改指**
7. **C2 CLAUDE.md 索引重建**
8. **A1–A7 全量验收**

> 验收口径：删除 7 项后余 **17** 项。其中 `uas_aios_phase_a` 由 C1 修复为绿；`ecosystem_prototype` 随 D1 一并移除（其依赖的 4 个脚本已删，且本已失败）。故最终目标为 **17/17 全绿，exit 0**。
>
> 若希望保留 `ecosystem_prototype` 与 `uas_runtime_list` 的覆盖，须改用方案 C（把 `UASRuntimeService` 等移植出 asui-cli），属另立计划。
