# LifeWake 文档知识架构治理设计

> 日期：2026-09-14 · 状态：设计基线
> 范围：projects/lifewake 全部文档 + 仓库根级失效引用修复
> 方案：A（逻辑分层，元数据驱动，不动物理目录）

## 1. 背景与问题（盘点事实）

1. **未提交基线**：`projects/lifewake/docs/lifewake/` 全部 17 份规约文档处于 git untracked 状态，基准无法追溯。
2. **根级断链**：根 `CLAUDE.md` 快速索引引用 `docs/lifewake/`、`docs/GOVERNANCE_REGISTRY.md`、`docs/ECOSYSTEM_IMPLEMENTATION_STATUS.md`、`docs/enterprise-sales-os/README.md`、`docs/UAS_AIOS_ENTERPRISE_*` 等路径，实际不存在或位于别处（`projects/lifewake/docs/lifewake/`、`projects/enterprise-sales-os/`、`docs/strategic/design/`）。
3. **项目内断链**：`projects/lifewake/README.md` 引用 `../../docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md`（不存在，实际在本项目 `docs/lifewake/`）。
4. **层级语义冲突**：`docs/lifewake/README.md` 现有 L1（产品BP）/L2（体验规约）/L3（可运行）三层，缺少用户要求的 L0 宪章根基（业务/产品/方案三宪章）；业务宪章无独立文档，商业内容散落在 `METRICS_GROWTH_AND_BUSINESS.md` 与主 BP 商业章节。
5. **版本声明缺失**：17 份规约中仅 4 份有「版本：」头（`LIFEWAKE_PRODUCT_BLUEPRINT` v1.0、`PRODUCT_ESSENCE_CARRIER_AND_TECH` v1.0·2026-09-14、`BETA_SHELL_AND_GIFT_SPEC` v0.2·2026-09-14、`USER_SCENARIO_AND_EXPERIENCE_SYSTEM` v1.0）；`CAPABILITY_CONTRACTS`、`WORKFLOW_STATE_MACHINE`、`GOVERNANCE_MATRIX`、`DOMAIN_MODEL` 等核心规约无版本无日期，无法机械识别最近基准。
6. **新旧并存无裁定**：根 `docs/strategic/LIFEWAKE_USER_AGI_EXPERIENCE_DOMAIN.md`（Architecture Baseline·2026-07-22）早于项目内规约包（2026-09-14），未声明 superseded 关系。
7. **规约-实现漂移**：`MVP_ACCEPTANCE_CASES.md` 声称 CASE-001～017，代码/测试仅实现 001～014，漂移未标注。
8. **职责重叠**：`docs/DEVELOPMENT_PLAN.md`（工程实现计划+完成度）与 `docs/IMPLEMENTATION_ROADMAP.md`(Phase 0-3 路线图) 内容重叠。
9. **无治理台账**：根 CLAUDE.md 引用的 GOVERNANCE_REGISTRY 不存在；无文档注册表。

## 2. 目标 / 非目标

**目标**
- G1：建立 L0→L4 五层知识架构，L0 三宪章（业务/产品/方案）齐备，全部文档归属唯一层级。
- G2：每份 L0-L3 文档有统一版本头（层级/状态/版本/基准日期/上下游），相似内容可按规则机械识别最近基准。
- G3：建立双注册表（人读 + 机器可读）作为唯一治理台账，含基准裁定记录。
- G4：修复范围内全部断链；旧文档标记 superseded + 重定向，不物理移动、不删除。
- G5：自动校验脚本落地并挂入 `harness/invariants/run-all.py` 与 lifewake pytest，治理结果可持续验证。
- G6：untracked 规约文档先原样提交固化基线，治理改动独立成 commit，全程可追溯。

**非目标**
- 不重构物理目录结构（方案 B 已否决）。
- 不治理 lifewake 之外的其他 projects（aios-workstudio、enterprise-sales-os、跨境）文档。
- 不重写旧文档正文，只加头部声明块与必要重定向说明。
- 不实现 CASE-015～017（只标注漂移）。

## 3. 五层知识架构与文档归属

```
L0 宪章层（公理层：不可被增长/商业化/技术覆盖；改动必须显式升版）
L1 产品母体层（商业与产品全貌）
L2 规约层（可验收行为定义）
L3 实现与验收层（代码映射、CASE、计划）
L4 运行产物层（只读事实：reports/、database/；不设版本头，注册表仅登记类别）
```

| 层级 | 文档 | 处置 |
|------|------|------|
| L0 | `docs/lifewake/BUSINESS_CHARTER.md` | **新建**：从 METRICS_GROWTH_AND_BUSINESS（反增长原则、商业闭环约束）与主 BP 商业章节提炼：商业目的、价值主张、守恒红线、反增长约束。≤120 行，只写公理不写细节 |
| L0 | `docs/lifewake/PRODUCT_CHARTER.md` | 现有，补版本头 v1.0 |
| L0 | `docs/lifewake/PRODUCT_ESSENCE_CARRIER_AND_TECH.md` | 现有 v1.0·2026-09-14（方案宪章），补规范头 |
| L1 | `docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md` | 现有 v1.0，补规范头 |
| L1 | `docs/lifewake/METRICS_GROWTH_AND_BUSINESS.md` | 现有；商业宪章提炼后留指标树/实验/GTM 细节，头部注明「公理见 BUSINESS_CHARTER」 |
| L1 | `docs/lifewake/BETA_SHELL_AND_GIFT_SPEC.md` | 现有 v0.2·2026-09-14，补规范头 |
| L1 | `docs/lifewake/USER_SCENARIO_AND_EXPERIENCE_SYSTEM.md` | 现有 v1.0，补规范头 |
| L2 | `PRODUCT_EXPERIENCE_DESIGN` / `FUNCTIONAL_DESIGN` / `DOMAIN_MODEL` / `CAPABILITY_CONTRACTS` / `GOVERNANCE_MATRIX` / `WORKFLOW_STATE_MACHINE` / `WORLD_MODEL_CONFIG` / `FEEDBACK_CHANGESET` | 现有，补规范头；初始版本统一赋 v1.0·2026-09-14（治理基线首版，注册表注明「版本号为治理赋予」） |
| L2 | `DERIVATION_AND_VALIDATION_MATRIX.md` | 横切追溯矩阵，同上 |
| L3 | `MVP_ACCEPTANCE_CASES.md` | 补规范头 + 显著标注「CASE-015～017 已规约未实现」 |
| L3 | `docs/APP_BLUEPRINT.md` | 补规范头 |
| L3 | `docs/DEVELOPMENT_PLAN.md` | 吸收 IMPLEMENTATION_ROADMAP 的 Phase 1-3 章节后补规范头 |
| L3 | `docs/IMPLEMENTATION_ROADMAP.md` | **superseded** → 重定向到 DEVELOPMENT_PLAN |
| L3 | `prototype/README.md` | 补规范头 |
| L3 | `docs/lifewake/README.md` | 改写为 L0→L4 总索引（保留阅读顺序指引），补规范头 |
| — | 根 `docs/strategic/LIFEWAKE_USER_AGI_EXPERIENCE_DOMAIN.md` | 加「部分 superseded」头：UAS↔SelfPaw 定位（historical 有效）；产品/体验/规约细节以 projects/lifewake/docs/lifewake/ 2026-09-14 基线为准 |
| L4 | `reports/` · `database/` | 仅注册表登记产物类别与生成命令 |

**根 CLAUDE.md 断链修复表**（快速索引节）：

| 失效引用 | 修复 |
|----------|------|
| `./docs/lifewake/PRODUCT_ESSENCE_CARRIER_AND_TECH.md`、`docs/lifewake/` | → `projects/lifewake/docs/lifewake/…` |
| `docs/GOVERNANCE_REGISTRY.md`（分类治理与未闭环追踪） | → `projects/lifewake/docs/DOC_REGISTRY.md`（本次新建台账；备注其余项目治理待后续期） |
| `docs/ECOSYSTEM_IMPLEMENTATION_STATUS.md` + `scripts/run_ecosystem_prototype.py` | 删除该行（文件与脚本均不存在） |
| `docs/enterprise-sales-os/README.md` | → `projects/enterprise-sales-os/README.md` |
| `docs/UAS_AIOS_ENTERPRISE_AGENT_ECOSYSTEM_L1_L3.md` 等 ENTERPRISE/GAPS 系列 | → `docs/strategic/design/…`（逐条核对实际位置） |

`projects/lifewake/README.md`：`../../docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md` → `docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md`。

## 4. 文档头规范（基线识别机制）

每份 L0-L3 注册文档，H1 标题下第一个 blockquote 为治理头（机器可解析）：

```markdown
> 层级: L2-规约 | 状态: baseline | 版本: v1.0 | 基准日期: 2026-09-14
> 上游: [PRODUCT_CHARTER](./PRODUCT_CHARTER.md)
> 下游: [MVP_ACCEPTANCE_CASES](./MVP_ACCEPTANCE_CASES.md) · `lifewake/orchestrator.py`
```

- **字段**：`层级`（L0-宪章/L1-产品/L2-规约/L3-实现/横切）、`状态`、`版本`（vX.Y）、`基准日期`（YYYY-MM-DD）必填；`上游`/`下游` 至少其一（L0 可只有下游）。
- **状态枚举**：`baseline`（现行基准）｜`draft`（草案，不作依据）｜`superseded`（必须附 `基准指向: <path>`）｜`historical`（保留历史价值）。
- **最近基准识别规则**（同主题多文档时，校验脚本与人工共用）：① `baseline` 优先 → ② 版本号高者优先 → ③ 基准日期新者优先 → ④ 均缺失时以 git 最后修改时间兜底并报「无治理头」警告。
- **既有「版本：」行处理**：保留原声明内容，治理头与之合并（治理头为唯一机器解析入口）；原有 `> 上游：/下游：` 自由文本行保留不动。
- **日期补齐规则**：文档内已有日期沿用；无日期的以本次治理日 2026-09-14 为基准日期，版本赋 v1.0（或沿用文内版本），注册表备注「治理赋予」。

## 5. 双注册表

**`projects/lifewake/docs/DOC_REGISTRY.md`**（人读总账）：
- 按 L0→L4 分节列出全部注册文档：路径｜层级｜状态｜版本｜基准日期｜职责一句话｜备注
- 「基准裁定」小节：逐条记录相似内容裁定及理由（体验域文档 2026-07-22→部分 superseded；IMPLEMENTATION_ROADMAP→superseded by DEVELOPMENT_PLAN；MVP_ACCEPTANCE_CASES 015-017 漂移标注；等）
- 「L4 产物」小节：产物类别 + 生成命令
- 「治理规则」小节：文档头规范、状态枚举、基线识别规则、校验命令

**`projects/lifewake/configs/doc_registry.json`**（机器可读，校验脚本唯一事实源）：

```json
{
  "registry_version": "1.0",
  "updated": "2026-09-14",
  "documents": [
    {
      "path": "docs/lifewake/PRODUCT_CHARTER.md",
      "layer": "L0", "role": "产品宪章", "status": "baseline",
      "version": "v1.0", "date": "2026-09-14",
      "upstream": [], "downstream": ["docs/lifewake/LIFEWAKE_PRODUCT_BLUEPRINT.md"],
      "superseded_by": null, "notes": ""
    }
  ],
  "artifacts": [
    {"path": "reports/", "generated_by": "scripts/run_value_loop_prototype.py 等"}
  ]
}
```

路径均相对 `projects/lifewake/`；根级文档（体验域、根 CLAUDE.md）以 `../../` 前缀登记为 `external` 条目（只校验存在性与治理头，不要求在本注册表分层内）。

## 6. 自动校验：`scripts/check_doc_governance.py`

纯标准库，CLI：`python scripts/check_doc_governance.py [--json]`，退出码 0/1。五项不变量：

| # | 不变量 |
|---|--------|
| INV-DOC-1 | 注册表 ↔ 文件系统双向一致（注册文档都存在；`docs/`、`docs/lifewake/`、`prototype/README.md` 下实有 .md 都已注册） |
| INV-DOC-2 | 每份 L0-L3 文档有合法治理头（四字段齐全、状态在枚举内、版本/日期格式正确） |
| INV-DOC-3 | 治理头与正文内相对链接无断链（含上游/下游指向的文件存在） |
| INV-DOC-4 | 每份 `baseline` 文档沿 `upstream` 链可达至少一份 L0 文档（无孤儿基准） |
| INV-DOC-5 | `superseded` 必有 `superseded_by`/基准指向，且指向文档状态为 `baseline` |

挂载：① `harness/invariants/run-all.py` 新增 `check_lifewake_doc_governance`（子进程调用，仓库级）② `projects/lifewake/tests/test_doc_governance.py`（import 脚本模块逐不变量断言，项目级）。

## 7. git 提交策略

| Commit | 内容 | 说明 |
|--------|------|------|
| 1 基线固化 | untracked `docs/lifewake/` 17 份文档**原样**提交 | 治理前原始状态永久可追溯 |
| 2 治理实施 | BUSINESS_CHARTER 新建、全部治理头、双注册表、README 索引改写、superseded 标记、ROADMAP 并入 DEVELOPMENT_PLAN、项目 README/CLAUDE.md 断链修复、体验域文档头 | 知识架构落地 |
| 3 校验体系 | check_doc_governance.py、test_doc_governance.py、harness 挂载、根 CLAUDE.md 断链修复 | 防再腐化；根级修改独立成 commit |

只 stage 本次治理涉及文件；工作区中其他项目的未提交改动（enterprise-sales-os、aios-workstudio）不得混入。

## 8. 验收标准

1. `python scripts/check_doc_governance.py` 退出码 0，五项不变量全过。
2. `pytest -q` 全绿（48 个既有测试 + 新增 doc governance 测试）。
3. `python ../../harness/invariants/run-all.py` 通过（含新增检查）。
4. 根 CLAUDE.md 快速索引所有路径可解析；lifewake README/CLAUDE.md 引用全部有效。
5. 任一相似主题（如 LifeWake 产品蓝图 vs 体验域文档）按第 4 节规则能在 1 分钟内机械判定最近基准。
6. git 历史呈现 3 个语义清晰的治理 commit，Commit 1 中文档与治理前逐字节一致。

## 9. 风险与缓解

| 风险 | 缓解 |
|------|------|
| 治理头改写误伤正文 | 只在 H1 后插入/合并 blockquote；Commit 1 先固化原状，diff 可逐行核对 |
| 版本号「治理赋予」被误读为历史版本 | 注册表与治理头备注显式声明；有真实版本声明的沿用原值 |
| 根 CLAUDE.md 修改与其他分支冲突 | 独立 Commit 3，改动最小化（只动快速索引行） |
| 校验脚本对根级 external 文档误报 | external 条目只查存在性与治理头，豁免分层/上游链校验 |
