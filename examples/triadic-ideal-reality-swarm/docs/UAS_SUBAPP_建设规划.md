# triadic-ideal-reality-swarm 建设规划：顶级 UAS SubApp

> 目标：在 **UAS 业务框架** 与 **ASUI 技术框架** 下，将本示例建设为具备 **智能全链路闭环**（渠道洞察→智能选品→内容生成→自动投放→效果优化→数据复盘）与 **智能驱动数据全流通** 的顶级 UAS SubApp。  
> 版本：v1.0 | 2026-03-15

---

## 一、建设目标与定位

### 1.1 目标陈述

- **业务目标**：成为 UAS 平台内**电商/营销增长场景**的标杆 SubApp，实现从「议题涌现分析」升级为「可执行的智能全链路营销闭环」。
- **技术目标**：严格符合 `UAS-Platform = (I, K, R, A, S, G, E, Π)` 与 ASUI 技术底座，通过共享 UAS Runtime Service 发现、校验、运行与演化。
- **体验目标**：一条业务意图（如「本周提升 ROI」「发现蓝海品并生成素材」）驱动全链路自动执行，结果可审计、可复盘、可演化。

### 1.2 产品定位

| 维度 | 定位 |
|------|------|
| **场景** | 电商营销自动化（含跨境）：渠道洞察、选品、内容、投放、优化、复盘 |
| **方法论** | 三维理念现实涌现（宏观/中观/微观 × 理念/现实）作为**决策与评估层**，六链路作为**执行层**，二者通过统一数据与知识层衔接 |
| **用户** | 中小卖家、品牌方、代运营团队（与平台 Studio/Runtime 交互，或通过议题/目标驱动） |

### 1.3 与 UAS 平台的关系

- 本 SubApp **挂载于 UAS 平台**，使用平台提供的 Runtime、治理、演化与协议栈。
- 可部署于 `projects/`（推荐）或保持于 `examples/` 并通过 `--projects-root examples` 挂载；**资产结构**与平台标准一致。

---

## 二、UAS 业务框架在本 SubApp 的映射

以下按 `UAS-Platform = (I, K, R, A, S, G, E, Π)` 逐层落实。

### 2.1 I - Intent Layer（意图与目标层）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **意图输入** | 用户/系统提交的**业务议题**或**目标**：如「本周提升 ROI」「发现蓝海品并产出素材」「对 X 方案做三维涌现评估」 |
| **目标归一化** | 工作流第一步「议题归一化」将自然语言转为结构化意图：场景、对象、约束、预期结果、成功指标 |
| **目标守恒** | 目的激活智能体 + governance 中的 `require_goal_statement`，防止执行过程中目的漂移 |

**交付物**：  
- `configs/workflow_config.json` 中保留并强化 `intake`（议题归一化）与 `purpose_activation`（目的激活）步骤，且与六链路共享同一意图上下文。  
- 在知识层（CLAUDE.md / skills）中明确定义「可接受的意图类型」与「目标→阶段」映射。

### 2.2 K - Knowledge Substrate（知识底座，ASUI）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **技术底座** | 明确声明 `technical_base: ASUI`，禁止纯 Prompt/纯脚本/无知识沉淀的实现 |
| **知识资产** | CLAUDE.md（系统操作手册）、.claude/skills/（各模块协议与契约）、configs/*.json（工作流、智能体、治理、演化、系统注册） |
| **知识驱动执行** | 所有阶段由 workflow_config + swarm_agents + skills 驱动；修改知识即生效，无需重写代码 |

**交付物**：  
- `configs/platform_manifest.json` 中 `platform.technical_base: "ASUI"`。  
- 知识层扩展：  
  - `.claude/skills/triadic_protocol.md`（保留，三维涌现协议）  
  - `.claude/skills/emergence_output_contract.md`（保留，涌现输出契约）  
  - 新增 `.claude/skills/channel_insight_protocol.md`（渠道洞察）  
  - 新增 `.claude/skills/product_selection_protocol.md`（智能选品）  
  - 新增 `.claude/skills/content_generation_protocol.md`（内容生成）  
  - 新增 `.claude/skills/campaign_placement_protocol.md`（自动投放）  
  - 新增 `.claude/skills/effect_optimization_protocol.md`（效果优化）  
  - 新增 `.claude/skills/data_retrospective_protocol.md`（数据复盘）  
  - 新增 `.claude/skills/data_flow_contract.md`（六链路数据流契约：各环节输入/输出 Schema 与存储约定）  

### 2.3 R - Autonomous Agent Runtime（自主智能体运行时）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **运行时** | 使用平台共享 `autonomous_agent` 运行时，通过 `scripts/run_uas_runtime_service.py` 的 `run` / `enqueue` / `process` 执行 |
| **上下文注入** | runtime_config 中 `context_injection: true`，执行时注入 CLAUDE.md、当前议题、上一步产出与数据库状态 |
| **状态隔离** | `state_isolation: task_level`，按任务/议题隔离认知状态与数据 |
| **审计与回滚** | `audit_enabled` / `rollback_enabled` 开启，关键写操作落库并可追溯 |

**交付物**：  
- `configs/runtime_config.json`（对齐 ai-recruitment-os，含 context_injection、state_isolation、audit、rollback、human_checkpoints）。  
- 可被 `run_uas_runtime_service.py --app-id triadic-ideal-reality-swarm`（或最终 app-id）正确发现与执行。

### 2.4 A - Agent Fabric（Agent 编织层）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **三维涌现蜂群** | 保留现有：目的锚点、宏观/中观/微观理念与现实、实例化、验证进化；用于**战略议题分析、方案评估、目标拆解** |
| **六链路执行智能体** | 新增与六步闭环一一对应的角色（可复用或细分）：渠道洞察 Agent、选品 Agent、内容生成 Agent、投放 Agent、效果优化 Agent、数据复盘 Agent |
| **协作关系** | 三维蜂群产出「目的 + 宏观/中观/微观约束」→ 作为六链路执行的策略与边界输入；六链路产出结构化数据 → 作为复盘与演化输入，并回写知识层 |

**交付物**：  
- `configs/swarm_agents.json` 扩展：在现有 9 个涌现智能体基础上，增加 6 个执行智能体（或 6 组能力），并定义其 `challenge_targets` 与上下游数据契约。  
- `configs/workflow_config.json` 扩展：在现有「涌现流程」之外或之内，增加六链路阶段（可拆为子工作流或同文件内新 steps），并保证与 `data_flow_contract` 一致。

### 2.5 S - System Mesh（专业系统网格层）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **系统注册** | 在 system_registry 中声明本 SubApp 依赖的外部系统与数据源 |
| **对接方式** | 通过 MCP / API 适配器对接（具体实现可分阶段：先 mock/本地数据，再真实 API） |
| **数据语义** | 各系统在数据流契约中映射为统一字段（如「渠道」「品类」「素材」「计划」「效果指标」） |

**交付物**：  
- `configs/system_registry.json`：注册例如 `channel_data_source`（电商/社交/行业数据）、`ad_platform`（直通车/巨量/Amazon SP 等）、`content_platform`、`internal_erp` 等，并标注 type 与 mode（native/external）。  
- 各六链路 skill 中声明本环节「读哪些系统、写哪些存储」，与 data_flow_contract 一致。

### 2.6 G - Governance Plane（治理平面）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **审计** | 所有写库、调外部 API、投放/关停等动作留痕，满足可追溯 |
| **权限与风险** | 高敏感操作（如自动关停计划、大额预算调整）可配置为需人工确认（human_checkpoints） |
| **可解释性** | 选品理由、投放策略、优化建议等输出结构化，满足 require_explainability |

**交付物**：  
- `configs/governance_policy.json`：定义 audit_required、permission_model、require_explainability、require_traceability、high_risk_requires_human_approval 等。  
- 与 runtime_config 中的 human_checkpoints 一致。

### 2.7 E - Evolution Loop（演化回路）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **复盘驱动** | 数据复盘模块产出「问题诊断、优化建议、指标偏差」→ 写入 database 与 reports，并触发 evolution_policy |
| **知识更新** | 演化策略允许在满足条件时更新 skills/workflow/阈值（如选品准确率阈值、ROI 目标），形成闭环 |
| **漂移规则** | 定义目的漂移、效果不达标、数据异常等条件下的回退或重试动作 |

**交付物**：  
- `configs/evolution_policy.json`：定义 goal_guard、iteration、evaluation_thresholds（如选品准确率、ROI、复盘完成率）、drift_rules（如 purpose_drift、effect_below_threshold → 回到目的激活或优化步骤）。  
- 数据复盘步骤的输出与 evolution 的输入格式对齐。

### 2.8 Π - Protocol Stack（协议栈）

| 要素 | 在本 SubApp 的落地 |
|------|---------------------|
| **UIP** | 用户/系统意图通过议题或目标表述，归一化后进入工作流 |
| **A2A** | 智能体间通过标准化数据结构与契约传递（见 data_flow_contract） |
| **MCP** | 对外部数据源与广告/内容平台的调用通过 MCP 或统一 Tool Gateway 抽象 |
| **ASUI** | 知识文档（CLAUDE.md + skills）+ configs 驱动执行，符合 ASUI 规范 |

**交付物**：  
- 在 CLAUDE.md 与 skills 中明确各协议的使用边界；与 asui-cli / UAS Runtime 的现有协议实现兼容。

---

## 三、ASUI 技术框架在本 SubApp 的落地

### 3.1 知识即配置

- **CLAUDE.md**：作为本 SubApp 的「系统操作手册」，必须包含：  
  - 项目概述与定位（三维涌现 + 六链路闭环）  
  - 目录结构、知识层文件说明、configs 说明  
  - 核心命令（如 `/emerge`、`/run_chain`、`/retrospect`）与工作流简述  
  - 与 UAS Runtime 的对接方式（如 `run_uas_runtime_service run --app-id ...`）  
- **configs/**：所有业务规则与流程以 JSON 配置表达，禁止硬编码业务逻辑在脚本中；脚本仅做「读取 config + 执行步骤 + 写库/写报告」。  
- **.claude/skills/**：各模块的输入输出、规则、敏感词/平台规则等以 Markdown 知识文件维护，AI 与引擎按需加载。

### 3.2 构建即运行

- 修改 workflow_config、swarm_agents、skills 或 governance/evolution 后，**无需重新部署**；下次执行即按新配置运行。  
- 版本与变更可通过 git 或知识库版本管理追溯。

### 3.3 可审计、可回滚、可演化

- **可审计**：每个步骤的输入输出与写库操作写入 `database/`（如 `database/emergence/`、`database/insight/`、`database/campaigns/` 等），并可在治理平面中查询。  
- **可回滚**：关键状态（如认知状态、任务状态）支持按版本或时间点回滚（由 Runtime 与 governance 支持）。  
- **可演化**：evolution_policy 与数据复盘输出驱动知识与阈值更新，形成闭环。

### 3.4 目录与资产清单（对标 UAS 平台标准）

```
triadic-ideal-reality-swarm/   # 或 projects/<app-id>/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── skills/
│   │   ├── triadic_protocol.md
│   │   ├── emergence_output_contract.md
│   │   ├── channel_insight_protocol.md
│   │   ├── product_selection_protocol.md
│   │   ├── content_generation_protocol.md
│   │   ├── campaign_placement_protocol.md
│   │   ├── effect_optimization_protocol.md
│   │   ├── data_retrospective_protocol.md
│   │   └── data_flow_contract.md
│   ├── agents/
│   └── commands/
├── configs/
│   ├── platform_manifest.json   # 必须，UAS 平台清单
│   ├── runtime_config.json      # 必须
│   ├── workflow_config.json     # 必须，含涌现 + 六链路
│   ├── swarm_agents.json        # 必须，含涌现 + 执行智能体
│   ├── governance_policy.json   # 必须
│   ├── evolution_policy.json    # 必须
│   └── system_registry.json     # 必须
├── database/
│   ├── emergence/
│   ├── insight/                 # 渠道洞察产出
│   ├── products/                # 选品与供应商
│   ├── content/                 # 内容与素材
│   ├── campaigns/               # 投放计划与效果
│   └── cognitive_state/         # 认知状态（Runtime 使用）
├── reports/
├── scripts/
│   ├── render_emergence_report.py
│   └── ...                      # 六链路各环节脚本（按需）
└── docs/
    ├── UAS_SUBAPP_建设规划.md   # 本文
    └── 电商闭环能力审查报告.md
```

---

## 四、智能全链路闭环与数据全流通设计

### 4.1 六链路在 workflow 中的形态

建议采用**两段式工作流**（可合并为单 workflow_config，用 phases 区分）：

1. **涌现段**（现有）：议题归一化 → 目的激活 → 三维拆解 → 理念现实对冲 → 现实实例化 → 交叉验证 → 涌现综合 → 写报告。  
   - 产出：目的锚点、宏观/中观/微观约束、实例化实体图谱、验证矩阵、**可执行的策略与边界**（如 ROI 目标、允许的渠道、风险偏好）。

2. **执行段**（新增）：  
   - **渠道洞察**：按 data_flow_contract 从 S 层拉取或模拟渠道数据 → 产出《热点品类洞察报告》、竞品动态等 → 写入 database/insight/。  
   - **智能选品**：读取 insight + 目的与约束 → 选品算法/规则 → 产出蓝海品列表、《选品可行性报告》、供应商匹配 → 写入 database/products/。  
   - **内容生成**：读取选品结果 + 品牌/平台规则（skills）→ 生成标题、详情、素材、脚本 → 写入 database/content/。  
   - **自动投放**：读取内容与策略 + system_registry 中的 ad_platform → 创建/调整计划（或 mock）→ 写入 database/campaigns/。  
   - **效果优化**：读取投放与效果数据 → 规则/策略（加预算、关停、换素材）→ 写回 campaigns 或 API。  
   - **数据复盘**：汇总 insight/products/content/campaigns 与效果指标 → 日报/周报/月报 + 演化建议 → 写入 reports/ 与 evolution 输入。

各环节的**输入输出**严格遵循 `.claude/skills/data_flow_contract.md`，实现**智能驱动数据全流通**：上游产出即下游输入，且关键节点持久化，可追溯、可回放。

### 4.2 数据流契约要点（data_flow_contract）

- **渠道洞察**：输入 = 议题/目的、渠道列表、时间范围；输出 = 热点品类、增长类目、竞品动作、报告路径。  
- **智能选品**：输入 = 洞察报告、目的约束、利润/竞争阈值；输出 = 推荐品列表、可行性报告、供应商参考、写入 products 的 ID。  
- **内容生成**：输入 = 选品结果、平台规则、风格配置；输出 = 标题/详情/素材/脚本文件或 ID，写入 content。  
- **自动投放**：输入 = 内容 ID、预算、定向、出价策略；输出 = 计划 ID、状态、写入 campaigns。  
- **效果优化**：输入 = 计划 ID、效果指标、目标 ROI；输出 = 调价/关停/换素材动作及结果，写回 campaigns。  
- **数据复盘**：输入 = 全链路 ID 与指标；输出 = 日报/周报/月报、异常预警、演化建议，写入 reports 与 evolution。

### 4.3 与三维涌现的衔接

- 涌现段的「目的激活 + 实例化」产出：**业务目标、可接受的渠道、ROI 目标、风险等级、创意风格** 等，作为执行段的**全局上下文**注入。  
- 执行段在关键节点（如选品、投放关停）可再次调用「验证进化」智能体做一致性检查，防止偏离目的。  
- 数据复盘的结论可反哺「目的漂移」检测与 evolution_policy，形成**涌现 ↔ 执行 ↔ 演化**三角闭环。

---

## 五、建设阶段与里程碑

### Phase 0：UAS 标准合规（当前 SubApp 升级为「可被发现、可校验、可运行」）

| 序号 | 任务 | 交付物 |
|------|------|--------|
| 0.1 | 增加平台清单与运行时配置 | configs/platform_manifest.json、configs/runtime_config.json |
| 0.2 | 增加治理与演化配置 | configs/governance_policy.json、configs/evolution_policy.json |
| 0.3 | 增加系统注册（先占位/ mock） | configs/system_registry.json |
| 0.4 | 通过 UAS Runtime 的 validate / health | `run_uas_runtime_service validate --app-id <id>` 通过 |

**验收**：本目录作为 SubApp 被 `list` 列出，`validate` 与 `health` 通过，`run --topic "某议题"` 能跑通现有涌现流程并写库。

### Phase 1：知识层与数据流契约（ASUI 六链路知识骨架）

| 序号 | 任务 | 交付物 |
|------|------|--------|
| 1.1 | 编写六链路协议 skills | channel_insight / product_selection / content_generation / campaign_placement / effect_optimization / data_retrospective protocol + data_flow_contract |
| 1.2 | 扩展 workflow_config 中「执行段」占位步骤 | 六步以 llm 或 script 占位，输入输出符合 data_flow_contract，可先 mock 数据 |
| 1.3 | 扩展 swarm_agents 中六链路执行智能体 | swarm_agents.json 中新增 6 个（或 6 组）Agent，与步骤绑定 |
| 1.4 | 更新 CLAUDE.md | 包含六链路命令、数据流说明、与 UAS 对接说明 |

**验收**：执行「涌现 + 六链路占位」完整跑通，各步有明确输入输出并写 database 对应目录。

### Phase 2：S 层对接与真实数据流（按需分渠道/平台）

| 序号 | 任务 | 交付物 |
|------|------|--------|
| 2.1 | 渠道洞察：对接或模拟数据源 | 从 system_registry 中配置的数据源拉取（或读取本地 JSON），产出《热点品类洞察报告》写入 database/insight/ |
| 2.2 | 智能选品：规则/算法实现 | 基于 insight 与 evolution 阈值，产出选品列表与可行性报告，写入 database/products/ |
| 2.3 | 内容生成：调用 LLM + 平台规则 | 基于选品与 skills 中的规则生成文案/素材路径，写入 database/content/ |
| 2.4 | 自动投放 / 效果优化：API 或 mock | 与 system_registry 中 ad_platform 对接（或 mock），计划创建与调优结果写入 database/campaigns/ |
| 2.5 | 数据复盘：汇总与报告 | 聚合各库数据，生成日报/周报/月报与演化建议，写入 reports/ 与 evolution 输入 |

**验收**：端到端一条议题驱动「洞察→选品→内容→投放→优化→复盘」，数据在各 database 与 reports 中可查，可审计。

### Phase 3：治理、演化与「顶级」体验

| 序号 | 任务 | 交付物 |
|------|------|--------|
| 3.1 | 治理强化 | 所有写库与调 API 留痕；高敏感操作经 human_checkpoints；可解释输出结构化 |
| 3.2 | 演化闭环 | 复盘输出自动触发 evolution_policy 的 drift_rules 与阈值更新建议，并支持知识文件更新 |
| 3.3 | 文档与示例 | README、CLAUDE、docs 中补充使用示例、数据流图、与平台 Studio/Runtime 的配合说明 |
| 3.4 | 性能与鲁棒性 | 大批量/多渠道下的稳定性与错误处理；必要时拆子工作流或异步任务 |

**验收**：满足 UAS 平台对 SubApp 的「审计、回滚、演化」要求；文档与示例足以支撑「顶级 UAS SubApp」的对外展示与交付。

---

## 六、风险与依赖

| 风险 | 缓解 |
|------|------|
| 真实渠道/广告 API 合规与成本 | 先 mock + 本地数据；真实对接时严格遵循各平台 ToS 与数据法规，并在 governance 中显性化 |
| 六链路与三维涌现的复杂度叠加 | 明确「涌现定策略、执行做动作」的分工，用 data_flow_contract 约束接口，避免步骤膨胀 |
| Runtime 与 asui-cli 版本演进 | 与主仓 UAS 平台保持同步，在 CI 或文档中注明兼容的 runtime 版本 |

**依赖**：  
- 仓库内 `asui-cli`、`scripts/run_uas_runtime_service.py`、`schemas/uas_platform_manifest.schema.json` 等保持可用。  
- 若部署于 `projects/`，需保证 `projects_root` 指向包含本 SubApp 的根目录。

---

## 七、总结

本规划将 **triadic-ideal-reality-swarm** 从「三维理念现实涌现」方法论示例，升级为符合 **UAS 业务框架**（I,K,R,A,S,G,E,Π）与 **ASUI 技术框架**（知识即配置、构建即运行、可审计可演化）的 **顶级 UAS SubApp**，具备：

1. **完整的平台标准资产**：platform_manifest、runtime_config、governance、evolution、system_registry、workflow、swarm_agents 与知识层。  
2. **智能全链路闭环**：渠道洞察→智能选品→内容生成→自动投放→效果优化→数据复盘，与三维涌现层衔接。  
3. **智能驱动数据全流通**：通过 data_flow_contract 与 database/reports 的规范设计，实现各环节数据可追溯、可复用、可驱动演化。

按 Phase 0 → 1 → 2 → 3 分阶段实施，可先达成「平台合规 + 知识骨架 + 占位闭环」，再逐步接入真实数据与 API，最终达到治理与演化闭环的「顶级」标准。
