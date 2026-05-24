# 企业级数字人生态 L1–L3：从第一性原理到产品化与商业闭环

> **版本** 1.0 | 2026-05  
> **定位**：在 UAS-AIOS 理论体系（道德势术器、世界模型五维、UAS 八元组、双轨 AGI、ASUI）之上，将「企业级 Agent 生态」从工具叙事推进为**契合组织内在逻辑**的数字人生态——并给出可配置、可审计、可商业化的闭环。  
> **命名约定**：本文 **DH-L1 / DH-L2 / DH-L3** 指**企业数字人层级**（Digital Human Tier），与认知文献中的 Cognitive Agent L1–L3、世界模型逻辑层 L1–L3 **不同义**，避免混读。

**关联文档**：[ENTERPRISE_PLATFORM_STANDARD.md](./ENTERPRISE_PLATFORM_STANDARD.md)（**产品/技术标准总索引 EPS-00**） · [THEORY_SYSTEM.md](./THEORY_SYSTEM.md) · [AGI_WORLD_MODEL_UAS.md](./AGI_WORLD_MODEL_UAS.md) · [UAS_PLATFORM_STANDARD.md](./UAS_PLATFORM_STANDARD.md) · [ASUI_ARCHITECTURE.md](./ASUI_ARCHITECTURE.md) · [ENTERPRISE_CS_CAPABILITY_PROTOCOL.md](./ENTERPRISE_CS_CAPABILITY_PROTOCOL.md) · [UAS_STRATEGIC_ROADMAP_OPENSOURCE_VS_COMMERCIAL.md](./UAS_STRATEGIC_ROADMAP_OPENSOURCE_VS_COMMERCIAL.md)

---

## 目录

1. [第一性原理：组织为何需要数字人生态](#一第一性原理组织为何需要数字人生态)
2. [总体架构：数据平面 → 能力 → Agent → 经营](#二总体架构数据平面--能力--agent--经营)
3. [平台 + 模型分层与职责边界](#三平台--模型分层与职责边界)
4. [双轨 AGI 的企业化：SelfPaw 企业版 × ΠPaw](#四双轨-agi-的企业化selfpaw-企业版--πpaw)
5. [DH-L1 / L2 / L3：三层数字人与岗位编制](#五dh-l1--l2--l3三层数字人与岗位编制)
6. [UAS 八元组的企业映射](#六uas-八元组的企业映射)
7. [协同协议：Intent、Evidence、升级与对外网关](#七协同协议intentevidence升级与对外网关)
8. [灵活动态适配：产品化封装单元](#八灵活动态适配产品化封装单元)
9. [端到端经营闭环示例（B2B 线索→回款）](#九端到端经营闭环示例b2b-线索回款)
10. [商业落地与双轨战略](#十商业落地与双轨战略)
11. [实现状态、差距与工程路线图](#十一实现状态差距与工程路线图)
12. [配置资产与快速启动](#十二配置资产与快速启动)

---

## 一、第一性原理：组织为何需要数字人生态

### 1.1 组织的三重内在逻辑（比「上 AI」更本质）

| 逻辑 | 组织现实 | 数字人生态必须回答的问题 | UAS 理论锚点 |
|------|----------|--------------------------|--------------|
| **主权逻辑** | 数据、决策、审计归属企业，不可默认外包给模型厂商 | 谁在什么边界内能读、写、调用、留痕？ | **德**（价值约束）→ **G** 治理平面 |
| **分工逻辑** | 岗位、流程、权限是数百年演化的协作接口 | Agent 如何「像岗位」而非「像聊天」？ | **势**（主客体差异）→ 世界模型**主体**维 |
| **价值逻辑** | 经营 = 对内履约 + 对外获转服续 | 数字人如何接入 P&L 与 SLA，而非 demo？ | **价值闭环 7 步** → **E** 演化回路 |

**结论**：企业要的不是「更多 Agent」，而是**在主权边界内、按岗位分工协作、对经营结果负责**的数字人体系。工具型 Copilot 解决「个人效率」；数字人生态解决「组织生产力与经营闭环」。

### 1.2 道德势术器 → 企业工程映射

```
道 ── 企业存在论：租户主权、合规边界、不可逾越的红线（法则包）
德 ── 价值取向：ROI、客户体验、员工赋能、风险可接受度（G 层策略）
势 ── 内外张力：对内履约 vs 对外获转服续；个人 scope vs 组织 scope（DH 分层）
术 ── 方法：Agent 规划 + 确定性引擎执行；蜂群决策备忘录（A 层编排）
器 ── 产品：cs.* 能力服务、BPM/表单/权限、S-Grid 连接器（S 层 + 平台）
```

### 1.3 AGI 分解在企业场景的约束

沿用 [AGI_WORLD_MODEL_UAS.md](./AGI_WORLD_MODEL_UAS.md)：

```
AGI = World Model ⊕ AI Agent
```

在企业场景中增加**硬约束**（Janus / UACA 工程化共识在 UAS 中的落地）：

| 环节 | LLM（模型层） | 平台（UAS 确定性层） |
|------|---------------|----------------------|
| 理解意图、生成草案、共情话术 | ✅ 主力 | 结构化提取 + schema 校验 |
| 资格判断、审批、开票、权限变更 | 候选方案 | ✅ **符号/规则/工作流终裁** |
| 对外承诺、资金、合同 | 不参与终裁 | ✅ G6 合规 + 人工升级点 |

**原则**：**模型负责理解与生成；平台负责执行与合规。** Agent 做规划与证据组织；`cs.*` 与 BPM 做可重试、可审计的执行。

---

## 二、总体架构：数据平面 → 能力 → Agent → 经营

### 2.1 自上而下依赖链（企业主权优先）

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 经营向外：获 · 转 · 服 · 续          （DH-L3 + ΠPaw 经营 Agent）          │
├─────────────────────────────────────────────────────────────────────────┤
│ 类人 Agent：决策 · 流程推进 · 跨岗调度  （DH-L2/L3 + A 层 Fabric）          │
├─────────────────────────────────────────────────────────────────────────┤
│ 数字基础能力：流程 · 表单 · 权限 · 主数据   （平台 PaaS，非 Agent 直连）        │
├─────────────────────────────────────────────────────────────────────────┤
│ 业务能力服务化 cs.*：customer / approval / invoice / quote …           │
├─────────────────────────────────────────────────────────────────────────┤
│ 企业主权数据平面：租户 · 主数据 · 事件流 · 审计链                          │
└─────────────────────────────────────────────────────────────────────────┘
                              ↑
                    S-Grid 仅在此层之下翻译接入
                    （CRM / BPM / ERP / 财务）
```

**关键纪律**：**Agent 不直连 CRM/BPM/ERP**；只调用 **`cs.<domain>.<verb>`** 语义能力。平台完成：权限校验、字段映射、幂等重试、审计写入、失败升级。

### 2.2 与 UAS-Platform 八元组的对齐

`UAS-Platform = (I, K, R, A, S, G, E, Π)` — 见 [UAS_PLATFORM_STANDARD.md](./UAS_PLATFORM_STANDARD.md)。

企业级扩展不是第九个字母，而是**在每层注入租户、岗位、cs 契约**（详见 §六）。

---

## 三、平台 + 模型分层与职责边界

### 3.1 三层技术栈

| 层 | 组成 | 职责 | 不负责 |
|----|------|------|--------|
| **模型层** | 通用 LLM、领域模型、嵌入/OCR/语音 | 语义理解、生成、归纳、共情 | 终裁、直连生产库、绕过审计 |
| **平台层（UAS）** | Agent 平台（WM·AEE·编排·G·E）、数字基础能力、S-Grid | 执行、合规、编排、演化、cs 注册 | 替代 ERP 成为 SoR |
| **数据平面** | 租户隔离、主数据、事件流、审计链 | 主权、可追溯、Replay | 业务规则（规则在 K + 法则包） |

### 3.2 Agent 平台内部（ASUI 企业化）

```
K（知识）: 行业 Domain 包 + 岗位 Agent 包 + 法则包
R（运行时）: autonomous_agent + Intent Hub + 任务队列（共享 Runtime Service）
A（编织）: SelfPaw 蜂群 / ΠPaw 多岗位编排 / DH-L2 跨部门调度
S（网格）: S-Grid 连接器 → 仅实现 cs.* 后端，不对 Agent 暴露原始 API
G（治理）: 租户策略、工具白名单、红线、人工升级、回滚
E（演化）: KPI 归因 → ChangeSet → 法则包/话术/流程参数热更新
Π（协议）: Intent/Evidence 契约、cs OpenAPI、A2A 子集（跨 Agent）
```

### 3.3 数字基础能力（平台 PaaS，Agent 的消费方）

| 能力 | Agent 用法 | 确定性 |
|------|------------|--------|
| 流程 BPM | `cs.workflow.start` / `signal` | 引擎状态机 |
| 表单 | `cs.form.submit` | schema 校验 |
| 权限 | 每次 cs 调用前 R+G 注入 scope | ABAC/RBAC |
| 主数据 | `cs.mdm.resolve` | 租户主数据 SoR |

---

## 四、双轨 AGI 的企业化：SelfPaw 企业版 × ΠPaw

### 4.1 为何是「双轨」而非「两个产品」

| 维度 | SelfPaw 企业版（User AGI / UAS-U） | ΠPaw（Business AGI / UAS-S） |
|------|-----------------------------------|------------------------------|
| **组织角色** | 员工数字分身（第二大脑 + 办事代理） | 经营与职能数字岗位体系 |
| **场景** | 对内：写、查、办、汇 | 对外：获转服续 + 对内履约与调度 |
| **数据 scope** | 个人授权 ∪ 岗位授权 | 组织全局（按角色分级） |
| **Agent 形态** | 个人 ReAct + 五视角蜂群 | 多岗位 Agent + 跨部门编排 |
| **向上关系** | 提交 **Intent 单 + Evidence** | 接收升级、分配 Task、调度 cs.* |

二者是**同一世界模型上的两个主体层级**：员工是「微观主体」，组织是「宏观主体」；升级不是「换个聊天窗口」，而是**主权与责任的转移**（G 层记录）。

### 4.2 SelfPaw 企业版：六大能力模块

| # | 模块 | 能力要点 | 主要 UAS 层 |
|---|------|----------|-------------|
| 1 | **组织身份绑定** | SSO、租户、岗位、数据 scope | G + 数据平面 |
| 2 | **Intent Hub** | 意图识别；经营类一键升级 ΠPaw | I |
| 3 | **岗位 Domain 包** | 销售/研发/HR 等 Ontology + 可用 cs 白名单 | K |
| 4 | **授权内执行** | 填表、发起流程、代拟邮件；L2 分身代理 | R + S |
| 5 | **个人蜂群决策** | 五视角 → 可审计《决策备忘录》 | A |
| 6 | **向上汇总** | 周报摘要；SLA 异常 → 自动创建 ΠPaw Task | I → ΠPaw |

### 4.3 ΠPaw：经营向外 + 数字岗位编制

**经营向外 = 触达 × 履约 × 决策 × 调度**

| 岗位 Agent（示例） | 方向 | 类人能力 | 典型 cs.* |
|-------------------|------|----------|-----------|
| 线索培育 / 销售顾问 | 对外 | 顾问式销售、资格判断 | `cs.lead.*`, `cs.quote.*` |
| 客服 / 履约 | 外/内 | 共情、SLA、流程推进 | `cs.case.*`, `cs.workflow.*` |
| 投标 / 合规 | 外/内 | 专业写作、红线拦截 | `cs.compliance.*`, G6 |
| 财务 / 调度 / 经营分析 | 内 | 精确计算、资源博弈、KPI | `cs.invoice.*`, `cs.analytics.*` |

**数字岗位编制**：每个岗位 Agent = `Prompt/技能包 + cs 工具白名单 + KPI 指标 + 升级策略`（可版本化、可审计），对应商业侧的「席位」计费单元。

---

## 五、DH-L1 / L2 / L3：三层数字人与岗位编制

### 5.1 层级定义（企业生态，非认知成熟度）

```
                    ┌──────────────────────────────────────┐
   DH-L3 经营数字人  │ 销售顾问 · 客服 · 投标 · 渠道伙伴      │ → ΠPaw（对外）
   （对外）         │ 获 · 转 · 服 · 续                       │
                    ├──────────────────────────────────────┤
   DH-L2 职能数字人  │ 招聘 · 财务 · 合规 · 跨部门调度        │ → ΠPaw 工作台
   （对内跨部门）    │ 组织级流程与资源博弈                    │
                    ├──────────────────────────────────────┤
   DH-L1 个人数字分身│ 第二大脑 · 任务代理 · 向上汇总          │ → SelfPaw 企业版
   （对内个人）      │ 员工主权 + 岗位 scope                  │
                    └──────────────────────────────────────┘
```

### 5.2 升级与代理规则（组织逻辑的核心）

| 触发 | 从 | 到 | 携带物 |
|------|----|----|--------|
| 经营类意图（报价、合同、投诉升级） | DH-L1 | DH-L3 或指定 L2 | Intent 单 + Evidence + 个人蜂群备忘录 |
| 跨部门资源争用 | DH-L1 | DH-L2 调度 Agent | SLA、阻塞点、已尝试 cs 调用 |
| 合规红线 | 任意 | G6 人工 + 审计 | 完整推理链，模型输出仅作附件 |
| 对外客户入口 | 客户 | Outward Gateway → DH-L3 | 会话 ID 映射租户，禁止直连内部主数据 |

### 5.3 与现有仓库示例的对应

| 层级 | 参考实现（当前仓库） | 平台级状态 |
|------|---------------------|------------|
| DH-L1 | `examples/selfpaw-cognitive-swarm`（蜂群决策验证） | U 层运行时：**规划**，见 [THEORY_ARCHITECTURE_CONSISTENCY_AUDIT.md](./THEORY_ARCHITECTURE_CONSISTENCY_AUDIT.md) |
| DH-L2/L3 | `projects/ai-recruitment-os`、`examples/ai-recruitment` | Business 轨 subapp：**部分实现** |
| cs.* | 见 [ENTERPRISE_CS_CAPABILITY_PROTOCOL.md](./ENTERPRISE_CS_CAPABILITY_PROTOCOL.md) | **协议 + 示例配置**，运行时待统一注册 |

---

## 六、UAS 八元组的企业映射

| 元组 | 企业含义 | 关键资产 |
|------|----------|----------|
| **I** | 经营/职能/个人意图；Intent Hub；升级事件 | `intent_schema`, Intent 单存储 |
| **K** | Domain 包、岗位包、法则包、话术 | `CLAUDE.md`, `.claude/skills/`, `configs/world_model.json` |
| **R** | 租户运行时、scope 注入、队列 | `runtime_config.json`, `run_uas_runtime_service.py` |
| **A** | SelfPaw 蜂群、ΠPaw 岗位 Agent、编排图 | `swarm_agents.json`, `workflow_config.json` |
| **S** | S-Grid：cs 实现体，不对 Agent 暴露 | `system_registry.json`, `enterprise_cs_capability_registry` |
| **G** | 权限、红线、审批矩阵、审计 | `governance_policy.json`, `database/audit/` |
| **E** | KPI 归因、ChangeSet、热更新 | `evolution_policy.json`, `/evolveApply` |
| **Π** | cs 契约、Intent/Evidence、A2A 子集 | `ENTERPRISE_CS_CAPABILITY_PROTOCOL.md` |

---

## 七、协同协议：Intent、Evidence、升级与对外网关

### 7.1 Intent 单（最小结构）

```json
{
  "intent_id": "uuid",
  "tier_source": "DH-L1",
  "actor": { "tenant_id": "t1", "user_id": "u1", "roles": ["sales_rep"] },
  "intent_type": "escalate_quote",
  "goal": "为客户 ACME 生成可审批报价",
  "constraints": ["credit_policy_v3", "region_CN"],
  "escalation_target": "DH-L3:sales_advisor",
  "created_at": "ISO8601"
}
```

### 7.2 Evidence 包（可审计）

- 引用的主数据 ID（非全文敏感数据）
- 已执行的 `cs.*` 调用摘要（request_id、结果码）
- 个人蜂群《决策备忘录》或 ΠPaw 岗位推理链
- 置信度与待核实项（世界模型 **认识论包裹**）

### 7.3 协同链路（形式化）

```
员工 SelfPaw ──Intent+Evidence──► ΠPaw 职能/经营 Agent ──cs.*──► 平台执行 ──► S-Grid ──► 企业系统
     ▲                                    │
     └──────── 状态/待办回写 ──────────────┘

对外客户 ──► Outward Gateway（脱敏、限流、租户路由）──► ΠPaw L3 Agent ──► 同上
```

---

## 八、灵活动态适配：产品化封装单元

| 封装单元 | 切换/适配方式 | 商业交付物 |
|----------|---------------|------------|
| **行业 Domain 包** | Ontology + 合规 + 话术 | 垂直套件（制造/零售/B2B SaaS） |
| **流程模板包** | 参数化 BPM + Agent 绑定 + SLA | 可上架流程市场 |
| **能力连接器包** | CRM/BPM/财务 endpoint + 字段映射 | 实施服务 + 年费 |
| **法则包** | 定价/信用/审批矩阵热更新 | 治理订阅 |
| **岗位 Agent 包** | Prompt + cs 白名单 + KPI | **按席位计费** |

**切换行业** = 切换 Domain + 法则 + 连接器，**不**重写 Agent 代码；符合 ASUI「知识即配置」。

---

## 九、端到端经营闭环示例（B2B 线索→回款）

| 阶段 | 业务动作 | 主导层级 | cs.* / 平台 |
|------|----------|----------|-------------|
| 1 | 官网留资 | DH-L3 / Gateway | `cs.lead.capture` |
| 2 | 资格判断 | DH-L3 销售顾问 | `cs.lead.qualify`（规则终裁） |
| 3 | 需求诊断 | DH-L3 + 可选 DH-L1 协助 | `cs.opportunity.update` |
| 4 | 报价 | DH-L3 | `cs.quote.create` |
| 5 | 合规审查 | G6 + DH-L2 合规 | `cs.compliance.review` |
| 6 | 审批 | BPM | `cs.approval.submit` / `signal` |
| 7 | 履约 | DH-L3 客服/交付 | `cs.order.fulfill` |
| 8 | 开票回款 | DH-L2 财务 | `cs.invoice.issue`, `cs.payment.match` |
| 9 | KPI 归因 | E 层 | `cs.analytics.attribute` → ChangeSet |
| 10 | 演化 | E + K | 法则包/话术/资格模型热更新 |

**价值闭环 7 步映射**：输入(留资) → 模拟(资格/报价草稿) → 生成(方案) → 交互(审批) → 进化(ChangeSet) → 输出(履约/票) → 收益(KPI 归因)。

---

## 十、商业落地与双轨战略

### 10.1 产品矩阵（开源 × 商业）

对齐 [UAS_STRATEGIC_ROADMAP_OPENSOURCE_VS_COMMERCIAL.md](./UAS_STRATEGIC_ROADMAP_OPENSOURCE_VS_COMMERCIAL.md)：

| 层级 | 开源（协议 + 参考实现） | 商业（企业变现） |
|------|-------------------------|------------------|
| 协议 | ASUI、cs.* schema、Intent/Evidence | 合规认证、行业法则库 |
| 平台 | `asui-cli`、Runtime Service、示例 subapp | 多租户托管、S-Grid 企业连接器、审计 SaaS |
| 生态 | Domain/岗位包社区 | 垂直套件、实施、席位订阅 |

### 10.2 计费单元（与组织逻辑一致）

1. **租户基础费**：数据平面 + G 审计存储  
2. **DH-L1 席位**：SelfPaw 企业版（按员工）  
3. **DH-L2/L3 岗位席位**：ΠPaw 岗位 Agent（按数字岗位）  
4. **cs 调用量 / 连接器**：S-Grid 集成规模  
5. **行业套件**：Domain + 流程模板 + 法则包打包  

### 10.3 交付里程碑（技术能力导向）

| 阶段 | 目标 | 依赖能力 |
|------|------|----------|
| P0 | 单 subapp 跑通 cs 契约 + 审计 | `system_registry` + ToolGateway → cs 适配器 |
| P1 | DH-L1 原型：Intent Hub + 升级 ΠPaw Task | U 层运行时、租户 scope |
| P2 | DH-L3 单场景闭环（留资→报价） | 法则包 + G6 |
| P3 | 多租户数据平面 + 席位治理 | 商业托管 |
| P4 | 行业套件复制 | Domain/岗位包市场 |

---

## 十一、实现状态、差距与工程路线图

| 能力 | 状态 | 说明 |
|------|------|------|
| Business 轨 subapp（ΠPaw 形态） | ✅ 部分 | `projects/*`, Runtime Service |
| SelfPaw 蜂群（DH-L1 方法论） | ✅ 示例 | `examples/selfpaw-cognitive-swarm` |
| 平台级 U 层 / SelfPaw 企业版 | ❌ 规划 | 无租户 Intent Hub、无个人 scope 注入 |
| cs.* 统一注册与 Agent 白名单 | 🟡 协议 | 本文 + 示例 JSON；`CapabilityRegistry` 待扩展 |
| 数据平面（租户/事件/审计链） | 🟡 子集 | subapp 内 `database/audit/`；无跨 subapp 租户服务 |
| Studio / System Hub 产品化 | ❌ 规划 | 见 UAS_PLATFORM_STANDARD |
| 价值闭环「模拟/收益」步 | 🟡 | 见 UAS_ASUI_PROTOCOL_GAPS_AND_ROADMAP |

**P0 工程动作（建议顺序）**：

1. 采纳 `configs/enterprise_cs_capability_registry.example.json` 作为 `system_registry` 的企业扩展。  
2. 在 `CapabilityRegistry.build()` 中暴露 `cs_capabilities` 供 Agent 白名单校验。  
3. 新增 `configs/world_model.json` 占位（主体/客体/反馈），与 Intent/Evidence 对齐。  
4. 立项 U 层 Runtime：租户 + `actor` 注入 `ContextInjector`。  

---

## 十二、配置资产与快速启动

| 文件 | 用途 |
|------|------|
| [docs/ENTERPRISE_PLATFORM_STANDARD.md](./ENTERPRISE_PLATFORM_STANDARD.md) | 企业标准总纲（EPS-00～07） |
| [docs/ENTERPRISE_PRODUCT_FUNCTIONAL_SPEC.md](./ENTERPRISE_PRODUCT_FUNCTIONAL_SPEC.md) | 产品功能规格（FR-*） |
| [docs/ENTERPRISE_TECHNICAL_MODULE_SPEC.md](./ENTERPRISE_TECHNICAL_MODULE_SPEC.md) | 技术模块规格（TM-*） |
| [configs/enterprise_cs_capability_registry.example.json](../configs/enterprise_cs_capability_registry.example.json) | cs.* 能力与 S-Grid 映射示例 |
| [configs/enterprise_digital_human_tiers.example.json](../configs/enterprise_digital_human_tiers.example.json) | DH-L1/L2/L3 岗位与升级策略 |
| [configs/enterprise_data_plane_manifest.example.json](../configs/enterprise_data_plane_manifest.example.json) | 租户/主数据/审计链占位 |
| [configs/schemas/](../configs/schemas/) | Intent / Evidence / cs.invoke JSON Schema |
| [.claude/skills/enterprise_digital_human_ecosystem.md](../.claude/skills/enterprise_digital_human_ecosystem.md) | Agent 构建/评估技能入口 |

**验证现有 Business 轨**：

```bash
pip install -e "./asui-cli[dev]"
python3 scripts/run_uas_runtime_service.py list
python3 scripts/run_uas_runtime_service.py run --app-id ai-recruitment-os --topic "端到端招聘闭环验证" --evaluate
```

---

*本文随 UAS-AIOS 企业级演进更新；DH 层级命名与认知/WM 层级 explicitly 区分。*
