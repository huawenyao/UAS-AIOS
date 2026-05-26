# UAS-AIOS × AIPOS × SelfPaw 统一业务·产品·技术架构体系

> **版本**：v1.0 · 2026-05-23  
> **定位**：将 AIPOS 方法论、SelfPaw/CoPaw 工程实现与 UAS-AIOS 理论内核对齐，形成 **Server · CLI · AI** 三位一体的可交付架构。  
> **上游参考**：`aipos/CLAUDE.md`、`aipos/copaw-src/docs/SelfPaw-架构权威说明.md`、`UAS-AIOS/CLAUDE.md`、`docs/strategic/UAS-AIOS_Delivery_Form_And_Product_Design.md`

---

## 0. 架构总览（一图读懂）

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         业务与产品层（Business / Product）                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ SelfPaw      │  │ ΠPaw         │  │ UAS Studio   │  │ AIPOS 方法论     │ │
│  │ User AGI     │  │ Business AGI │  │ 开发者平台   │  │ 六层一库两环     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘ │
└─────────┼─────────────────┼─────────────────┼───────────────────┼───────────┘
          │                 │                 │                   │
┌─────────▼─────────────────▼─────────────────▼───────────────────▼───────────┐
│                    产品对象层（AIPOS 五件套 × UAS 八元组）                    │
│  Domain(认知包) → Project(目标容器) → Working Task(执行单元) → Asset(交付物) │
│  Intent · Evidence · State · Gate(G1-G7) · ChangeSet · Agent Contract       │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────────────────┐
│              技术交付层：Server · CLI · AI（SelfPaw 参考实现）               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │ SERVER          │  │ CLI             │  │ AI                          │  │
│  │ FastAPI :8088   │  │ selfpaw / asui  │  │ ReActAgent + AEE + Skills   │  │
│  │ Console API     │  │ init/app/models │  │ World Model · Memory · MCP  │  │
│  │ Channels/Webhook│  │ skills/domains  │  │ Agent Executors · Hooks     │  │
│  └────────┬────────┘  └────────┬────────┘  └──────────────┬──────────────┘  │
└───────────┼────────────────────┼─────────────────────────────┼──────────────┘
            │                    │                             │
┌───────────▼────────────────────▼─────────────────────────────▼──────────────┐
│                         UAS Kernel（UAS-AIOS 内核层）                         │
│  I 意图 │ K 知识(ASUI) │ R 运行时 │ A Agent编织 │ S 系统网格 │ G 治理 │ E 演化 │ Π 协议 │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │ 世界模型引擎 │ ASUI 8阶段工作流 │ Agent编排 │ 治理审计 │ 演化引擎 │ 协议栈  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────────┘
```

**核心命题**：认知实践是生产力创造价值的根本路线；**AGI = World Model + AI Agent**；工程上通过 **知识即配置、构建即运行、增量演化** 落地。

---

## 1. 战略定位与长远目标

### 1.1 三层使命对齐

| 层次 | AIPOS | UAS-AIOS | SelfPaw（参考实现） |
|------|-------|----------|---------------------|
| **道** | AI 原生企业价值操作系统 | 认知实践论 + 世界模型 | 自觉的认知架构驱动 |
| **德** | 门禁 G1-G7 + 治理闭环 | G 层治理 + 价值约束 | 协作策略 + wrap_tool_execution |
| **势** | 六层差异化 + 竞品对标 | 双轨 AGI（User / Business） | vs OpenClaw 认知/检索/学习优先 |
| **术** | Domain→Project→Task 闭环 | ASUI 8 阶段 + 蜂群编排 | AEE Sense→Plan→Act→Verify→Learn |
| **器** | ALE / 低代码语义交付 | UAS Studio + subapp | Server/CLI/Console/Channels |

### 1.2 长远目标（18–36 个月）

| 轨道 | 目标状态 | 可量化标志 |
|------|----------|------------|
| **User AGI（SelfPaw）** | 个人认知 OS：多通道、多项目、自进化 | P1–P5 演进完成；DIKWP 价值闭环可观测 |
| **Business AGI（ΠPaw）** | 组织级 Business AGI 平台 | 多 Agent 协同工作台 + 合规治理中心上线 |
| **Developer（UAS Studio）** | 低代码/无代码 UAS 应用生产 | 可视化工作流 + 世界模型设计器 |
| **Kernel（UAS-AIOS）** | 行业标准 AI 操作系统 | 协议栈标准化；百万级 Agent 生态 |

### 1.3 SelfPaw 演进总纲（来自 aipos 工程规划）

```
通用 AI 助手
  → 多场景多项目专业规划执行
  → 主动服务
  → 自主能力学习沉淀
  → 自进化
  → DIKWP 价值闭环
```

五期工程路线：**P1 数据闭环 → P2 场景认知 → P3 迭代执行 → P4 多视角验证 → P5 自进化闭环**。

---

## 2. 竞品对比与差异化策略

### 2.1 竞品矩阵

| 维度 | OpenClaw | Cursor/Claude Code | Clawith | Palantir AIP | **UAS × SelfPaw** |
|------|----------|-------------------|---------|--------------|-------------------|
| **定位** | 个人 Agent 基座 + Gateway | IDE 内编码 Agent | 多 Agent 团队平台 | 企业本体 + 决策 | **认知 OS + 业务 AGI 双轨** |
| **架构** | 五层 + 独立 Gateway (Node) | 编辑器插件 + Cloud Agent | RBAC + Agent Mesh | 本体工程 + Kinetic | **ASUI + 世界模型 + AEE** |
| **知识** | Bootstrap 文件全量注入 | 项目上下文 + Rules | 组织知识库 | 强本体 Ontology | **Domain=认知包；K层知识即配置** |
| **记忆** | SQLite+vec 混合检索 | Session 级 | 共享 Feed | 企业数据湖 | **ReMe 检索优先 + 按需注入** |
| **治理** | 单操作者信任模型 | 用户级 | L1/L2/L3 分级执行 | 强合规 | **G1-G7 门禁 + ChangeSet + 审计** |
| **执行** | pi-agent + Shell | delegate_to_agent | 审批流 | Actions/Functions | **AEE + ReqHarness + UAS Runtime** |
| **演化** | 插件生态 | 弱 | 运营面板 | Writeback/Scenario | **E层演化引擎 + evolveApply** |
| **B端** | 弱 | 弱 | 中 | 强 | **ΠPaw 行业模板 + subapp** |

### 2.2 差异化定位（不成为「Python 版 OpenClaw」）

1. **认知优先**：四层显式认知 + Sense→Plan→Act→Verify→Learn 工程化、可观测  
2. **检索优先**：记忆按需检索，token 效率高于 bootstrap 全量注入  
3. **学习优先**：AEE + 失败分析 + 模式提取 → 能力沉淀飞轮  
4. **理论优先**：世界模型五维 + 道德势术器 + 价值闭环 7 步，非纯工具链堆叠  
5. **双轨交付**：SelfPaw（个人）与 ΠPaw（组织）共享 UAS Kernel，避免重复建设  

### 2.3 吸收与规避

| 向竞品学习 | 刻意规避 |
|------------|----------|
| OpenClaw：Lane 队列、webhook、agent-to-agent 输入 | 独立 Gateway 进程复杂度 |
| Cursor：Agent Executor 外置委托 | 黑盒执行、无 ChangeSet 追溯 |
| Clawith：L3 执行硬闸、租户 RBAC | 与 AIPOS 门禁重复建设 |
| Palantir：本体分层、Scenario 仿真 | 重平台轻 Agent 的交付形态 |

---

## 3. 业务架构：价值闭环与产品矩阵

### 3.1 三循环 × 价值闭环 7 步

**AIPOS 三循环**（业务第一性）：

```
价值认知循环 ──→ 价值创造循环 ──→ 价值捕获循环
     ↑___________________________________|
```

**UAS 价值闭环 7 步**（工程映射）：

| 步骤 | 业务含义 | 产品触点 | 技术载体 |
|------|----------|----------|----------|
| 1 输入 | 真实问题 + 领域知识 | Chat / 通道 / CLI | Channel + IntentObject |
| 2 模拟 | 数字孪生试错 | UAS Studio 仿真 | 世界模型推演模块 |
| 3 生成 | 多方案产出 | Task Panel / 报告 | Agent 编排 + Skills |
| 4 交互 | 人机协同评估 | Console / 审批 | Gate G4/G6 + 人工确认 |
| 5 进化 | 更新世界模型 | evolveApply | E层演化 + ChangeSet |
| 6 输出 | 介入工作流 | Asset / subapp 产出 | R层运行时 + S层集成 |
| 7 收益 | 效益反哺 | DIKWP 仪表盘 | 反馈 API + 指标采集 |

### 3.2 四层交付体系（UAS-AIOS 产品矩阵）

```
面向用户层     SelfPaw（User AGI）          ΠPaw（Business AGI）
面向开发者层   UAS Studio
基础设施层     UAS Kernel（ASUI + 世界模型 + 协议栈）
方法论层       AIPOS（六层一库两环 + 五件套）
```

### 3.3 统一产品对象模型（Domain → Project → Task → Asset）

| 对象 | 产品回答 | UAS 映射 | AIPOS 五件套 |
|------|----------|----------|--------------|
| **Domain** | 怎么理解、怎么做 | K 知识 + 世界模型 S 视图 | Ontology + Capability Bundle |
| **Project** | 为什么做、完成标准 | I 意图 + 情景上下文 | Intent Container + Evidence |
| **Working Task** | 这一次做什么 | R 运行时执行单元 | Agent Contract 输入 |
| **Task Panel** | 做到哪、卡在哪 | 可观测 + G 治理 | State + Gate 状态 |
| **Asset** | 交付物与证据 | 输出 + 审计 | Artifact + TraceLink |
| **ChangeSet** | 可审计变更 | E 演化回写 | 智能体变更契约 |

主链路：

```
Domain 定义认知边界 → Project 定义目标边界 → Working Task 触发 Agent Loop
→ Task Panel 呈现执行态 → Asset 沉淀交付 → ChangeSet 驱动演化
```

---

## 4. 技术架构：Server · CLI · AI 三位一体

### 4.1 三层职责划分

| 层 | 职责 | 主要组件 | 默认端口/入口 |
|----|------|----------|---------------|
| **SERVER** | 对外服务、通道接入、API、鉴权、持久化 | FastAPI、Routers、Channels、ArtifactStore | `:8088`（`selfpaw app`） |
| **CLI** | 初始化、运维、批处理、CI、Kernel 调度 | `selfpaw` CLI、`asui` CLI、`run_uas_runtime_service.py` | 命令行 |
| **AI** | 推理、规划、工具、记忆、学习 | SelfPawAgent、AEE、Skills、Memory、MCP | Agent Loop 内部 |

### 4.2 SERVER 层架构

```
Channels（钉钉/飞书/QQ/Discord/Console/SharedWeb/Webhook）
        │
        ▼
FastAPI Routers（/agent, /projects, /domains, /feedback, /mcp, …）
        │
        ▼
AgentRunner（RuntimeContext · 协作策略 · 执行平面 · Project/Domain 绑定）
        │
        ▼
SelfPawAgent（ReAct 流式 · Toolkit · Hooks · 工具门禁）
        │
        ▼
AEE + Memory + Artifact + AgentExecutorRegistry
```

**与 UAS Kernel 对齐**：

| Server 模块 | UAS 八元组 |
|-------------|------------|
| Routers + Auth | G 治理 + Π 协议 |
| AgentRunner | R 运行时 + I 意图激活 |
| Domain/Project API | K 知识 + S 系统网格 |
| AEE / ExecutionLog | G 审计 + E 演化输入 |
| Feedback API | E 演化 + 价值闭环 |

### 4.3 CLI 层架构

双 CLI 分工：

| CLI | 仓库 | 用户 | 核心命令 |
|-----|------|------|----------|
| **selfpaw** | aipos/copaw-src | 终端用户 / 运维 | `init`, `app`, `models`, `skills`, `domains`, `projects` |
| **asui** | UAS-AIOS/asui-cli | 开发者 / 架构师 | `init`, subapp 脚手架 |
| **uas-runtime** | UAS-AIOS/scripts | 平台运维 | `list`, `run`, `enqueue`, `process`, `health`, `validate` |

CLI 与 Server 关系：

```
CLI（构建态）                    Server（运行态）
selfpaw init ──────────────→  config.json / providers / working dir
selfpaw skills install ─────→  active_skills / SKILL.md 热加载
asui init -t uas-subapp ───→  projects/<app>/configs/*.json
run_uas_runtime_service ───→  批处理 / 队列 / subapp 编排（无 HTTP）
```

**ASUI 原则在 CLI 的体现**：修改 `configs/`、`CLAUDE.md`、`.claude/skills/` → 下次执行即生效，无需重编译。

### 4.4 AI 层架构

```
┌─────────────────────────────────────────────────────────────┐
│ 认知执行核（SelfPawAgent / ReAct）                            │
│  PromptBuilder: AGENTS → SOUL → PROFILE → RuntimeContext块   │
├─────────────────────────────────────────────────────────────┤
│ AEE（Agent Execution Engine）                                │
│  Intent · ExecutionPlan · Gate · Feedback · ChangeSet · Trace│
├─────────────────────────────────────────────────────────────┤
│ 能力扩展                                                      │
│  Skills │ Builtin Tools │ MCP │ Agent Executors │ ReqHarness │
├─────────────────────────────────────────────────────────────┤
│ 记忆与世界模型                                                │
│  MemoryManager │ Domain WorldModel │ Project CognitiveView  │
└─────────────────────────────────────────────────────────────┘
```

**认知闭环（maiPaw 标准）**：

```
Sense → Persona Bind → Route → Plan → Act → Verify → Learn
  │                                              │
  └──────────── 世界模型 / Memory 更新 ◄─────────┘
```

**与 UAS 八阶段工作流映射**：

| ASUI 8 阶段 | AEE / Agent 阶段 |
|-------------|------------------|
| intent_activation | Sense + IntentObject |
| understanding | Route + Domain/Project 绑定 |
| planning | create_execution_plan |
| execution | Act（工具调用） |
| monitoring | ExecutionLog / Task Panel |
| render_report | Asset 产出 |
| evaluation | Verify + Gate G4/G7 |
| （演化） | Learn + ChangeSet → E层 |

### 4.5 Console 前端（Server 的 UI 延伸）

```
console/src/
├── api/client.ts      → FastAPI Backend
├── pages/chat/        → Agent 交互（AI 层入口）
├── pages/domains/     → Domain 认知包管理（K层）
├── pages/skills/      → Skills 能力管理
└── pages/models/      → Provider 配置
```

Console 不是第四根支柱，而是 **Server 的可视化壳**；ΠPaw 企业演示（`docs/strategic/demo/`）代表 Business AGI 的控制台愿景。

---

## 5. AIPOS 六层 × UAS Kernel 七层 对照

| AIPOS 六层 | 含义 | UAS Kernel 层 | SelfPaw 实现 |
|------------|------|---------------|--------------|
| L1 战略与价值层 | 意图、价值主张 | I 意图 | Project.goal / IntentObject |
| L2 业务与流程层 | 业务流程语义 | S 系统网格 | Domain Ontology + Working Task |
| L3 智能体架构层 | Agent 编排 | A Agent 编织 | ReAct + delegate + 蜂群模板 |
| L4 AI 平台层 | 模型、工具、RAG | R 运行时 + 资源管理 | providers + MCP + Skills |
| L5 数据与本体层 | 知识资产 | K 知识 + 世界模型 | Domain YAML + ASUI configs |
| L6 技术架构层 | 部署、安全、观测 | 基础设施 + G 治理 | FastAPI + Auth + ExecutionTrace |

**一库**：架构知识底座 → `CLAUDE.md` + `.claude/skills/` + `harness/knowledge/`  
**两环**：价值闭环 + 治理闭环 → 7 步闭环 + G1-G7 门禁

---

## 6. 门禁与治理统一口径

### 6.1 AIPOS 门禁 G1-G7

| 门禁 | 含义 | SelfPaw 落点 | UAS G 层 |
|------|------|--------------|----------|
| G1 | 追踪链 | ExecutionTrace + task_id | 审计溯源 |
| G3 | 可实现性 | Planning Gate | 规划约束 |
| G4 | 可测性 | Verify 步骤 + 验收标准 | 评估引擎 |
| G6 | 红线 | gate_constraints + 协作白名单 | 合规拦截 |
| G7 | 评测基线 | Feedback + DIKWP 指标 | 演化输入 |

### 6.2 双环治理模型

```
执行前：Prompt 注入 Gate 自检（规划态）
执行中：wrap_tool_execution + L3 硬闸（Clawith 可对齐）
执行后：ChangeSet 审计 + evolveApply 回写（演化态）
```

---

## 7. 仓库与模块映射

| 能力 | AIPOS 仓库 | UAS-AIOS 仓库 | 关系 |
|------|------------|---------------|------|
| 方法论与标准 | `aipos/docs/` | `docs/`、`CLAUDE.md` | UAS 提供理论内核；AIPOS 提供交付规范 |
| 参考实现 | `aipos/copaw-src/` | — | SelfPaw = User AGI 参考实现 |
| Kernel 运行时 | — | `asui-cli/src/asui/engine/` | UASRuntimeService |
| subapp 模板 | harness/requirements | `projects/`、`examples/` | 业务 AGI 验证 |
| 战略原型 | — | `docs/strategic/demo/` | ΠPaw UI 愿景 |
| 需求.harness | `aipos/harness/` | `examples/*/.reqharness/` | 共享 ReqHarness 范式 |

**集成原则**：SelfPaw 的 Domain/Project/AEE **实例化** UAS 的 K/I/R；UAS Runtime Service **编排** subapp；AIPOS 五件套 **约束** 两者交付形态。

---

## 8. 分阶段落地路线图

### Phase 0（当前 → 3 个月）：三位一体 MVP

| 目标 | Server | CLI | AI | UAS |
|------|--------|-----|-----|-----|
| 统一对象模型 | Project/Task API 稳定 | `selfpaw` + `asui init` | Domain→Task 闭环 | subapp health 通过 |
| 可观测 | Task Panel 任务态 | `run_uas_runtime_service list` | ExecutionTrace | 审计目录落地 |
| 治理 | 协作白名单 | evolveApply 脚本 | Gate Prompt | G层 policy json |
| 文档 | 本文档 + 权威架构 | CLAUDE 互链 | AEE 文档对齐 | Kernel 设计同步 |

### Phase 1（3–9 个月）：认知深化（SelfPaw P1–P3）

- 用户反馈 API + DIKWP 数据采集  
- ScenarioModel + 迭代 Plan→Act→Verify→Revise  
- UAS Kernel HTTP API 网关（subapp 远程调度）  
- UAS Studio CLI 可视化包装（`asui studio` 占位）

### Phase 2（9–18 个月）：双轨产品化

- ΠPaw 企业版：多 Agent 工作台 + 组织知识库  
- 蜂群 / 三维理念现实模板接入 Business AGI  
- ALE 专题：语义资产包发布  
- 协议栈：MCP + A2A + UIP 标准化

### Phase 3（18–36 个月）：生态与标准

- Agent / Skill Marketplace  
- 分布式 UAS Kernel 调度  
- 行业合规认证（金融/政务/医疗）  
- AIPOS 能力标准 L3+ 对外认证

---

## 9. 关键接口契约（跨层集成）

### 9.1 AgentRequest（Server → AI）

```yaml
required: [channel, session_id, query]
optional: [active_project_id, active_domain_ids, meta, caller_agent_id]
runtime_context:  # Runner 写入，模型不可覆盖
  execution_plane: project_task | global_workspace | mixed
  collaboration: { surface, trust_tier, resolved_tool_allowlist }
  task_id: string
```

### 9.2 UAS Subapp Run（CLI → Kernel）

```bash
python scripts/run_uas_runtime_service.py run \
  --app-id ai-recruitment-os \
  --topic "业务议题" \
  [--evaluate]
```

### 9.3 ChangeSet（AI → E 层演化）

```yaml
changeset_id: string
source: aee | evolve | manual
artifacts: [{ path, action, evidence_ref }]
gates_passed: [G1, G4, G7]
rollback_ref: optional
```

---

## 10. 决策原则（架构铁律）

1. **单 Agent 内核**：不因多 Agent 需求复制第二套 ReAct；外出用 Executor / 蜂群模板。  
2. **系统态与模型态分离**：RuntimeContext 仅 Runner 写入。  
3. **知识即配置**：业务规则进 K 层，不进硬编码。  
4. **加法优先**：新能力以 Skill / Hook / Router / subapp 添加。  
5. **Feature Flag 守护**：SelfPaw P1–P5 默认关闭，独立可回滚。  
6. **证据驱动演化**：无 Trace + Feedback 不触发 evolveApply。  
7. **双轨共享内核**：SelfPaw 与 ΠPaw 不 fork Kernel，只 fork 产品层。

---

## 11. 阅读索引

| 主题 | AIPOS | UAS-AIOS |
|------|-------|----------|
| 当前实现权威 | `copaw-src/docs/SelfPaw-架构权威说明.md` | `asui-cli/src/asui/engine/service.py` |
| 竞品对比 | `docs/04-架构与实现/OpenClaw*.md` | `docs/UAS_STRATEGIC_ROADMAP*.md` |
| 演进路线 | `copaw-src/docs/selfpaw-evolution-plan.md` | `docs/strategic/UAS-AIOS_Delivery_Form*.md` |
| 产品 Spec | `docs/03-产品与业务/AIPOS_Domains_Projects*.md` | `docs/strategic/detailed-design/ΠPaw*.md` |
| 世界模型 | `docs/04-架构与实现/AIPOS_World-Model*.md` | `docs/世界模型/世界模型.md` |
| 治理映射 | `docs/04-架构与实现/Clawith治理与AIPOS*.md` | `configs/governance_policy.json`（subapp） |

---

*本文档为 UAS-AIOS 战略层架构锚点；SelfPaw 工程变更须回溯 §4–§6 对齐检查；AIPOS 规范更新须同步 §5 对照表。*
