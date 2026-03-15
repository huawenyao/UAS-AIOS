# 基于 Command + Agent Skill 自主生产 UAS Sub App 的 Agent 架构设计

> 本文档给出可自主生产 UAS sub app 的 Agent 架构组件的全面分析设计，遵循项目理论原理（ASUI、UAS-AIOS、认知实践论）与产品架构方法。

---

## 一、需求与目标

### 1.1 核心需求

实现**基于 command + agent skill 生产 sub app** 的自主 Agent 架构，使系统能够：

1. **命令驱动**：用户通过 `/createSubApp` 等命令触发 sub app 生产
2. **技能驱动**：Agent 加载 `.claude/skills/` 下的 sub app 生产技能，理解生产协议与输出契约
3. **自主生产**：Agent 自主完成从意图归一化 → 方案设计 → 资产生成 → 注册入网的全流程
4. **标准合规**：产出物严格满足 UAS Platform 标准与 ASUI Autonomous Agent 标准

### 1.2 设计目标

| 目标 | 说明 |
|------|------|
| **知识即配置** | 生产协议、输出契约、模板选择逻辑均以显式知识形式存在 |
| **构建即运行** | 生成的 sub app 立即可被 UAS Runtime Service 发现与运行 |
| **增量演化** | 新增 skill 或 command 即扩展生产能力，无需改代码 |
| **可审计** | 每次生产有完整审计轨迹与决策依据 |

---

## 二、理论依据与架构对齐

### 2.1 与 ASUI 范式的对应

| ASUI 原则 | 本设计的实现 |
|-----------|--------------|
| 知识即配置 | `subapp_producer_protocol.md`、`subapp_output_contract.md` 作为显式知识驱动生产 |
| 构建即运行 | 生成后自动注册到 `.service_registry/`，`run_uas_runtime_service.py list` 立即可见 |
| 增量演化 | 新增 skill（如 `value_assessment.md`）可被生产流程引用；新增模板可扩展生产形态 |

### 2.2 与 UAS-AIOS 八元组的对应

| 构件 | 本设计的实现 |
|------|--------------|
| **I** 意图层 | `/createSubApp [业务描述]` 归一化为结构化意图（目标、约束、对象、成功标准） |
| **K** 知识底座 | `subapp_producer_protocol.md`、`subapp_output_contract.md`、模板知识、UAS 标准知识 |
| **R** 运行时 | 生产 Agent 运行在元项目的 autonomous_agent 上下文，调用 scripts、database |
| **A** Agent 编织 | 生产编排 Agent + 意图归一化 Agent + 方案设计 Agent + 资产生成 Agent（可多 Agent 协作） |
| **S** 系统网格 | `create_sub_uas_app.py`、`asui init`、`UASRuntimeService`、文件系统、registry |
| **G** 治理平面 | 生产前校验意图合法性；生产后校验产出物是否符合 UAS 标准 |
| **E** 演化回路 | 生产结果写入 database，支持后续评估与迭代建议 |
| **Π** 协议栈 | Command 协议、Skill 协议、Output Contract 协议 |

### 2.3 与认知实践论的对应

- **实践**：用户发起 `/createSubApp`，Agent 执行生产
- **表征**：意图模型、方案结构、配置 JSON、目录树
- **反馈**：validate 结果、registry 注册状态、runtime health check
- **反思**：evaluation 报告、evolution 建议
- **传承**：新 sub app 作为知识资产沉淀，可被后续生产复用

---

## 三、整体架构设计

### 3.1 架构总览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Command Layer（命令层）                               │
│  /createSubApp [业务描述] [--template xxx] [--target projects|examples]     │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Agent Skill Layer（技能层）                                │
│  .claude/skills/subapp_producer_protocol.md   ← 生产协议                     │
│  .claude/skills/subapp_output_contract.md     ← 输出契约                     │
│  .claude/skills/subapp_template_selector.md   ← 模板选择逻辑（可选）          │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Agent Orchestration Layer（编排层）                         │
│  SubAppProducerAgent：意图归一化 → 方案设计 → 资产生成 → 校验注册              │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Execution Layer（执行层）                                  │
│  create_sub_uas_app.py / asui init / 文件写入 / registry 更新                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 数据流

```
用户输入: /createSubApp 跨境电商选品助手
    │
    ├─→ 1. 意图归一化（Intent Normalization）
    │      输出: { topic, goal, constraints, success_metrics, target_audience }
    │
    ├─→ 2. 模板选择（Template Selection）
    │      输入: intent + 可选 --template
    │      输出: uas-subapp | selfpaw-swarm | triadic-ideal-reality-swarm | ...
    │
    ├─→ 3. 方案设计（Blueprint Design）
    │      输入: intent + template + UAS 标准知识
    │      输出: 符合 output_contract 的完整方案 JSON
    │
    ├─→ 4. 资产生成（Asset Generation）
    │      输入: 方案 + 模板
    │      输出: 目录树、configs、skills、scripts、docs
    │
    ├─→ 5. 校验与注册（Validate & Register）
    │      输入: 生成路径
    │      输出: validate 结果、registry 更新、health check
    │
    └─→ 6. 反馈（Feedback）
            输出: 生产报告、下一步建议
```

---

## 四、核心组件设计

### 4.1 Command 定义

**位置**：`.claude/commands/createSubApp.md`

**语法**：
```
/createSubApp <业务描述> [选项]
```

**选项**：
| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--template` | 模板类型 | 由 Agent 根据意图推断 |
| `--target` | 目标根目录 | projects |
| `--name` | 子应用 ID（slug） | 由业务描述生成 |
| `--force` | 覆盖已存在 | false |
| `--dry-run` | 仅输出方案，不生成文件 | false |

**示例**：
```
/createSubApp 跨境电商选品助手，支持多平台数据聚合与智能推荐
/createSubApp 招聘流程自动化 --template uas-subapp --target examples
/createSubApp 三维理念现实分析 --template triadic-ideal-reality-swarm
```

### 4.2 Agent Skill：生产协议

**位置**：`.claude/skills/subapp_producer_protocol.md`

**核心内容**：
- 生产阶段定义（与 UAS 标准工作流阶段对齐）
- 每阶段的输入/输出、依赖关系
- 禁忌与约束（如：禁止生成无 governance 的 sub app）
- 与 `platform_manifest.json`、`workflow_config.json` 的对应关系

### 4.3 Agent Skill：输出契约

**位置**：`.claude/skills/subapp_output_contract.md`

**核心内容**：
- 方案 JSON 的 schema（与 `render_uas_plan.py` 的 payload 对齐）
- 必填字段：topic, intent_model, knowledge_assets, agent_fabric, governance_controls, evolution_loop
- 可选字段：runtime_topology, system_mesh, delivery_plan
- 与 UAS_SUBAPP_TEMPLATE 中各 config 的映射关系

### 4.4 Agent Skill：模板选择逻辑（可选）

**位置**：`.claude/skills/subapp_template_selector.md`

**核心内容**：
- 模板类型与适用场景的映射
- 选择规则：如「多角色博弈」→ selfpaw-swarm；「理念-现实张力」→ triadic
- 默认：uas-subapp（通用 UAS 标准 sub app）

### 4.5 SubAppProducerAgent 工作流

**工作流配置**：可置于元项目 `configs/subapp_producer_workflow.json` 或内嵌于 skill

| 阶段 ID | 名称 | 类型 | 说明 |
|---------|------|------|------|
| intent_normalization | 意图归一化 | llm | 将业务描述转为结构化意图 |
| template_selection | 模板选择 | llm/rule | 根据意图选择模板 |
| blueprint_design | 方案设计 | llm | 生成符合 output_contract 的完整方案 |
| asset_generation | 资产生成 | script | 调用 create_sub_uas_app + 定制化写入 |
| validate | 校验 | script | 调用 validate_app |
| register | 注册 | script | 更新 service_registry |
| report | 生产报告 | script | 写入 database/productions/ |

### 4.6 执行层扩展

**新增脚本**：`scripts/produce_sub_uas_app.py`

- 输入：stdin JSON `{ topic, intent, template, blueprint?, dry_run }`
- 逻辑：
  1. 若 blueprint 为空，则需先由 Agent 生成（或由上层 workflow 传入）
  2. 调用 `run_init(project_path, template=template)` 生成基础骨架
  3. 根据 blueprint 覆盖/补充 configs、skills、docs
  4. 若 `!dry_run`，执行 validate 与 registry 更新
- 输出：`{ status, app_id, app_root, report_path, validation }`

**Registry 更新**：生产完成后，调用 `UASRuntimeService` 的发现逻辑，将新 sub app 加入 registry（若 projects_root 包含新路径）。

---

## 五、目录与文件结构

### 5.1 元项目新增/修改

```
.
├── .claude/
│   ├── commands/
│   │   ├── createSubApp.md          # 新增：命令定义
│   │   └── README.md
│   └── skills/
│       ├── subapp_producer_protocol.md   # 新增：生产协议
│       ├── subapp_output_contract.md     # 新增：输出契约
│       ├── subapp_template_selector.md   # 新增（可选）：模板选择
│       └── value_assessment.md           # 已有：可被生产流程引用
├── configs/
│   └── subapp_producer_workflow.json      # 新增（可选）：生产工作流
├── scripts/
│   ├── create_sub_uas_app.py              # 已有
│   └── produce_sub_uas_app.py             # 新增：生产编排脚本
└── database/
    └── productions/                       # 新增：生产记录
        └── README.md
```

### 5.2 生成的 Sub App 结构（遵循 UAS 标准）

与现有 `UAS_SUBAPP_TEMPLATE` 一致，确保：
- `CLAUDE.md`、`configs/*.json`、`.claude/skills/`、`scripts/`、`database/`、`reports/`
- `platform_manifest.json` 中 `technical_base: ASUI`、`runtime: autonomous_agent`

---

## 六、实现路径与优先级

### Phase 1：最小可行闭环（MVP）

1. **新增 Command**：`.claude/commands/createSubApp.md`，定义语法与示例
2. **新增 Skill**：`subapp_producer_protocol.md`、`subapp_output_contract.md`（精简版）
3. **Agent 行为**：当用户输入 `/createSubApp xxx` 时，AI 加载上述 skill，按协议执行：
   - 意图归一化（LLM）
   - 模板选择（默认 uas-subapp）
   - 方案设计（LLM，输出符合 output_contract 的 JSON）
   - 调用 `create_sub_uas_app.py` 生成骨架
   - 根据方案覆盖关键 config（如 workflow_config、swarm_agents 的定制化部分）
   - 执行 validate，输出报告
4. **无需新脚本**：复用 `create_sub_uas_app.py`，Agent 通过编辑生成的文件完成定制

### Phase 2：脚本化与自动化

1. **新增**：`scripts/produce_sub_uas_app.py`，接收 blueprint JSON，完成骨架生成 + 定制写入
2. **工作流配置**：`configs/subapp_producer_workflow.json`，可被 RuntimeManager 或独立 runner 执行
3. **Registry 集成**：生产完成后自动刷新 registry（或提供 `refresh` 命令）

### Phase 3：多模板与演化

1. **模板选择 Skill**：`subapp_template_selector.md`，支持 selfpaw、triadic 等
2. **生产记录**：`database/productions/` 记录每次生产的意图、方案、校验结果
3. **演化建议**：基于生产记录，生成「相似场景可复用」「需补充 skill」等建议

---

## 七、与现有组件的集成

| 现有组件 | 集成方式 |
|----------|----------|
| `create_sub_uas_app.py` | 作为资产生成阶段的核心调用，传入 `--template`、`--target` |
| `asui init` / `run_init` | 同上，通过 `create_sub_uas_app.py` 间接调用 |
| `UAS_SUBAPP_TEMPLATE` | 作为默认模板，Agent 可在此基础上覆盖 |
| `RuntimeManager` | 可选：生产工作流可作为「元工作流」在元项目运行，步骤中调用 produce 脚本 |
| `UASRuntimeService` | 生产后通过 `list` 或 `registry` 发现新 sub app；需确保 projects_root 包含新路径 |
| `workflow_config.schema.json` | 方案中的 workflow 需符合 schema |
| `platform_manifest.schema.json` | 生成的 platform_manifest.json 需通过 schema 校验 |

---

## 八、风险与约束

| 风险 | 缓解措施 |
|------|----------|
| Agent 生成的 config 不符合 schema | 在 output_contract 中明确 schema 引用；validate 阶段强制 schema 校验 |
| 生产覆盖已有项目 | 默认不 force；提供 `--force` 显式确认 |
| 模板与意图不匹配 | 通过 template_selector skill 约束选择逻辑；支持用户 `--template` 覆盖 |
| Registry 未及时更新 | 生产脚本结束后显式调用 registry 刷新；或文档说明需手动 `list` 触发发现 |

---

## 九、总结

本设计实现了**基于 command + agent skill 自主生产 UAS sub app** 的 Agent 架构，核心要点：

1. **Command**：`/createSubApp` 作为统一入口，触发生产流程
2. **Skill**：`subapp_producer_protocol`、`subapp_output_contract`、`subapp_template_selector` 作为显式知识，驱动 Agent 行为
3. **编排**：SubAppProducerAgent 按阶段执行意图归一化 → 方案设计 → 资产生成 → 校验注册
4. **执行**：复用 `create_sub_uas_app.py`，扩展 `produce_sub_uas_app.py` 支持 blueprint 驱动
5. **标准**：产出物严格满足 UAS Platform 标准与 ASUI Autonomous Agent 标准

该架构符合 ASUI「知识即配置、构建即运行、增量演化」原则，与 UAS-AIOS 八元组对齐，支持通过新增 skill 与 command 实现增量扩展。
