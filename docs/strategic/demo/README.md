# ΠPaw Business AGI Demo 设计说明

> **版本**：v2.2 · 2026-07-05  
> **依据**：`docs/strategic/detailed-design/` 业务体系与管理逻辑  
> **演示载体**：`ΠPaw_Enterprise_Demo.html`（单页交互 Demo，浏览器直接打开）

---

## 1. 结论：产品承载形态

Business AGI 不是「聊天框 + RPA」，而是**企业经营逻辑的数字化载体**。产品需同时承载：

| 维度 | 承载形态 | Demo 映射 |
|------|----------|-----------|
| **战略—执行贯通** | 四适配引擎（战略 / 组织 / 管理 / 业务）自上而下拆解，自下而上汇总 | 组织模型 + 战略罗盘 + 状态条实体链路 |
| **角色化入口** | 战略罗盘（决策层）· 管理驾驶舱（管理层）· 执行助手（一线） | 顶栏三工作台 + 智慧闭环角色胶囊 |
| **场景化落地** | N 个行业场景套件（四要素预匹配：场景·功能·数据·工具） | 策略库战役 + 价值流模板 + `scn-*` 场景 |
| **Agent 执行层** | L1 个人分身 · L2 职能数字人 · L3 经营数字人，经 `cs.*` 语义能力调用 | 组织树 Agent 编制 + Capability Hub |
| **工程底座** | UAS Kernel（I,K,R,A,S,G,E,Π）+ 六层工程栈 L1~L6 | 「系统架构」页 + 平台管线 Capture→Evolve |
| **价值闭环** | 双闭环：业务场景闭环 + 管理策略迭代闭环 | 智慧闭环主控台 + PDCA 双轨 |
| **内外价值流** | 对内（组织协同·效率·合规）+ 对外（获客·履约·服务·经营向外） | 内外价值流模块 + LTC/客服场景 |

```
┌─────────────────────────────────────────────────────────────────┐
│  角色化应用层                                                    │
│  战略罗盘 ──→ 管理驾驶舱 ──→ 执行助手                            │
├─────────────────────────────────────────────────────────────────┤
│  场景套件层    2B销售LTC · 制造OTD · 项目交付 · 客服SLA · …       │
├─────────────────────────────────────────────────────────────────┤
│  能力平台层    知识资产 · 通用AGI能力 · Agent工作台 · 价值闭环 · 治理 │
├─────────────────────────────────────────────────────────────────┤
│  四适配引擎    战略对齐 → 组织适配 → 管理模式 → 业务模式          │
├─────────────────────────────────────────────────────────────────┤
│  UAS Kernel   I·K·R·A·S·G·E·Π + 世界模型五维 + cs.* 能力平面      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Agent 能力与工程化承接

### 2.1 Agent 分层（数字人三层）

| 层级 | 角色 | 数据 scope | 典型 Agent | Demo 示例 |
|------|------|------------|------------|-----------|
| **L3** | 经营数字人（对外） | 客户域·商机·合同 | Sales Advisor、客户回流顾问 | 华东区 L3 Agent |
| **L2** | 职能数字人（对内跨部门） | 部门域·流程 | 经营分析官、招聘专员、生产调度 | 集团 L2 Agent |
| **L1** | 个人数字分身（对内个人） | 个人授权 + 岗位授权 | 销售个人分身 | 128 人绑定 |

**原则**：模型负责理解与生成；平台经 **语义能力 `cs.*`** 负责确定性执行；Agent 不直连业务系统。

### 2.2 六大智能引擎（L5）

感知 → 归因 → 策略 → 编排 → 预警 → 进化 — 对应 detailed-design 中「价值闭环系统」与「合规治理」的运行态实现。

### 2.3 五大经营实体（L4）

`Objective → Strategy → Action → Result → Attribution` — 确保决策智慧可记录、可归因、可沉淀为 SOP。

### 2.4 双闭环

**业务场景闭环**（定目标→追过程→拿结果→复盘）：

```
目标设定 → 路径规划 → 资源配置 → 执行落地 → 过程监控 → 异常处理 → 结果核算 → 复盘优化
```

**管理策略闭环**（策略制定→落地→评估→优化）：

```
策略制定 → 落地执行 → 效果评估 → 问题诊断 → 策略优化 → 下一轮迭代
```

Demo 中 PAC Margin 场景演示业务闭环；销售提成策略示例在 README 与「管理策略」模块中说明。

### 2.5 内外价值流

| 流向 | 定义 | 关键指标 | Demo 场景 |
|------|------|----------|-----------|
| **对内** | 组织协同、管理降本、合规审计、知识沉淀 | 管理成本↓、人效↑、审计覆盖率 | OKR 对齐、PDCA、审批合规 |
| **对外** | 获客、转化、履约、服务、回款 | 营收、Margin、NPS、SLA | LTC 报价闭环、客户挽回 |

---

## 3. Demo 信息架构（页面地图）

| 页面 | 产品名 | 面向角色 | 核心演示点 |
|------|--------|----------|------------|
| **智慧闭环** | 主控台 | 全角色（角色胶囊切换） | 四适配层条、双闭环、五大实体、六大引擎联动 |
| **战略罗盘** | 原「经营驾驶舱」 | CEO/BG | 四大金刚、战略拆解、全局风险 |
| **管理驾驶舱** | 原「策略工作台」 | BU/部门负责人 | 目标承接、过程管控、异常闭环 |
| **执行助手** | 原「个人工作台」 | 一线 BD/运营 | Task Panel、LTC/客诉 Playbook、cs.* 审计 |
| **组织模型** | 组织适配层配置 | 管理者/实施顾问 | OMTU、Agent 编制、RACI、五维映射 |
| **策略库** | 战役 + SOP 载体 | 策略主责 | 项目战役、里程碑、价值流执行态 |
| **系统架构** | 工程视图 | IT/架构师 | UAS 八元组、cs.*、Outward Gateway、六层栈 |
| **价值流模板** | 场景套件配置 | 实施顾问 | Pack/流程/规则、验收 KPI |

---

## 4. 推荐演示路径

### 路径 A · PAC Margin 经营闭环（B2B + LTC Playbook）

1. **智慧闭环** →「演示 PAC 闭环」  
2. 推进至「行动」步 → 自动创建 `playbook.sales_ltc_quote_v1` WorkingTask  
3. **执行助手** → 逐步「执行当前步骤」：`cs.lead.qualify_lead` → `cs.process.start` → `cs.approval.submit`  
4. 数据流模式 `b2b_sales`：Action → WT → Playbook → cs.* → Audit → Result  

### 路径 B · SelfPaw → ΠPaw 客诉升级（REQ-EDH-PP-001）

1. 点「客诉升级链路」— 数据流：Intent → Evidence → escalate → WT → Playbook → cs.*  
2. 角色「客服 Agent」→ Task Panel 逐步「执行当前步骤」  
3. 步骤与 `pipaw_cs_agent_playbook.json` 一致  

### 路径 C · Outward Gateway 对外会话（PP-002）

1. **系统架构** → Outward Gateway 面板 →「演示飞书 IM 入站」  
2. 数据流：Channel → Gateway → Intent → Agent Route → WT → Playbook → cs.*  
3. 对齐 `outward_gateway_routes.sample.json` · 飞书/企微 → `agent.cs_specialist`  

### 路径 D · 组织与战役

1. **组织适配** → 华东区 → 由缺口立项  
2. **策略库** → 华东 Q2 攻坚 KPI 联动  

---

## 5. Harness 运行时模型（Demo 内嵌）

| 模型 | 配置来源 | Demo API |
|------|----------|----------|
| IntentObject | `intent_samples/complaint_escalation.sample.json` | `escalateIntentToPipaw()` |
| Outward Intent | `outward_gateway` + routes | `routeOutwardMessage()` |
| WorkingTask | `working_task.schema.json` | `EnterpriseRuntime.workingTasks` |
| Agent Roster | `pipaw_business_agent_roster.json` | `HARNESS_AGENTS` + roster gate |
| CS Playbook | `pipaw_cs_agent_playbook.json` | `advancePlaybookStep()` |
| Sales Playbook | `pipaw_sales_agent_playbook.json` | `dispatchSalesPlaybookTask()` |
| Process Template | `process_templates/sales_quote_approval.json` | `cs.process.start` 步骤 |
| cs.* | `capability_registry.json` | `invokeCapability()` |

**数据流模式**（`EnterpriseRuntime.dataFlowMode`）：

| 模式 | 触发 | 节点链 |
|------|------|--------|
| `cs_escalation` | SelfPaw 客诉升级 | Intent → Evidence → escalate → WT → … |
| `outward` | Outward Gateway | Channel → Gateway → Intent → Route → WT → … |
| `b2b_sales` | PAC Action 分派 / LTC 演示 | Action → WT → Playbook → cs.* → … |

---

## 6. 本地运行

```bash
# 导出真实运行时 fixtures（intent_hub + task_panel）
python3 scripts/export_demo_harness_fixtures.py

# 语法检查（可选）
node docs/strategic/demo/_check_js.mjs

# 启动静态服务（fixtures 加载需 HTTP，不可用 file://）
cd docs/strategic/demo && python3 -m http.server 8080
# 浏览器打开 http://localhost:8080/ΠPaw_Enterprise_Demo.html
# 执行助手 →「加载真实运行时」导入 fixtures/escalate_response.json
```

### Fixtures 目录

| 文件 | 来源 |
|------|------|
| `fixtures/escalate_response.json` | `scripts/escalate_intent.py` 等价输出 |
| `fixtures/task_panel_current.json` | `PipawTaskPanel.build_view()` |
| `fixtures/playbook_cs.json` / `playbook_sales.json` | configs |
| `fixtures/manifest.json` | 导出时间与校验命令 |

---

## 7. 与 detailed-design / 架构基线索引

| 主题 | 文档 |
|------|------|
| **标准化架构 + TOGAF 交付** | `../design/BusinessAGI_Standardized_Architecture_AND_TOGAF_Delivery.md` |
| Harness Agent 应用规范 | `../../harness/knowledge/technical/pipaw-cs-agent-benchmark.md` |
| 平台功能模块 | `../detailed-design/ΠPaw_Business_AGI_Platform_Detailed_Design.md` |
| 四适配层 + 双闭环 | `../detailed-design/ΠPaw_Business_AGI_Platform_Enhanced_Design.md` |
| 三层角色化应用 + 场景套件 | `../detailed-design/ΠPaw_Full_Stack_Product_Landing_Definition.md` |
| UAS 内核 | `../detailed-design/UAS_Kernel_Detailed_Design.md` |
| 数字人生态 | `../Enterprise_Digital_Human_Ecosystem_Product_Definition.md` |

---

*Demo 为产品叙事与交互原型，数据为模拟态；工程实现以 UAS Kernel + Studio 为准。*
