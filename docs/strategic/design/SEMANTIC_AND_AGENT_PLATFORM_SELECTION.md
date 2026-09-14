# 企业级 AGI AIOS：语义层本体 × Agent 平台选型

> 地位：面向未来的技术选型决策。服从 [`AI_PRODUCT_CHARTER.md`](../../AI_PRODUCT_CHARTER.md)、[`ENTERPRISE_AGI_OPERATING_HUB.md`](./ENTERPRISE_AGI_OPERATING_HUB.md)、ADR-EDH-001。  
> 资料窗口：2026-09。市场会变，**分层原则不变**。  
> 版本：v1.0 · 2026-09-09  
> 落地架构：[`UAS AIOS架构规划（自研OR集成）.md`](./UAS%20AIOS架构规划（自研OR集成）.md)  
> 模块设计：[`UAS_AIOS_MODULE_DESIGN.md`](./UAS_AIOS_MODULE_DESIGN.md)

---

## 0. 选型一句话

不要选「一个语义层产品」或「一个 Agent 平台」来当 AIOS。  
2026 年的正确做法是：**自有经营本体当内核，采购口径层与时态知识层，自有 Hub 当控制面，采购耐久运行时与开放协议。**

Palantir Ontology / Fabric IQ / Agentforce 是**别人的操作系统**。Cube / Graphiti / Temporal / MCP 是**可替换零件**。Capability Hub + 责任图 + 五维世界模型才是**我们的本体**。

---

## 1. 先拆开四个经常被混为一谈的东西

市场上「语义层」「世界模型」「Agent 平台」被厂商故意说成同一件事。对 UAS 必须拆开，否则选错层。

| 名称 | 回答的问题 | 典型产品 | 能否当 AIOS 内核 |
|------|------------|----------|------------------|
| **口径语义层** Measurement | 这个数怎么算、谁能看 | Cube、dbt MetricFlow、AtScale、Snowflake Semantic Views、LookML | 否。只保证 `kpi.is` 口径一致 |
| **经营本体** Operating ontology | 谁对什么目标、对哪些客体、卡在哪段流程负责 | Palantir Ontology、Fabric IQ、**UAS 责任图** | **是。这是产品内核，必须自有** |
| **知识 / 时态图谱** Meaning + time | 事实何时为真、证据在哪、关系怎么跳 | Graphiti/Zep、Utopia、Stardog、Neo4j GraphRAG | 否。服务 Explore 与记忆，不签发经营任务 |
| **Agent 平台 / 控制面** | 谁能调什么工具、审批、审计、剖面 | LangGraph、Copilot Studio、AIP、**Capability Hub** | **控制面必须自有**；循环引擎可采购 |

Gartner 2025 之后的共识也是这句话的弱形式：Agent 需要统一语义上下文；但**没有一个现成平台同时覆盖口径、实体关系、时态、治理执行**。Valliance 2026 把市场分成两营：只读分析语义层 vs 可写操作本体。我们要的是后者的**能力**，不要后者的**产品壳**。

---

## 2. 评估维度（过不了就不进短名单）

对照经营中枢三条命题与宪章。

| ID | 维度 | 通过标准 |
|----|------|----------|
| S1 | 目标 ≡ 数据 | 节点能同时挂 Goal、Owner、KPI、流程挂钩 |
| S2 | 五维可投影 | 空间/时间/主体/客体/反馈缺一可拒绝签发 |
| S3 | 应当 vs 事实 | 冲突可显式，不静默覆盖 |
| S4 | 证据接地 | 未接地不得进建议 |
| S5 | 知识即配置 | 法则/口径可版本化、可 ChangeSet |
| S6 | 场景禁写 / Runtime 才写 | 读路径与写路径可分剖面 |
| S7 | 双轨不混权 | 个人记忆 ≠ 经营承诺 |
| S8 | Agent 不直连系统 | 工具必须经网关，模型不见密钥 |
| S9 | 开放可替换 | Apache/MIT 或开放协议；禁止把内核锁进一家 SaaS |
| S10 | 面向 18–36 个月 | 协议层（MCP/A2A/OSI）可演进，不赌单一模型厂 SDK |

---

## 3. 语义层：全景与评分

### 3.1 口径层（Measurement）

| 产品 | 开源 | 成熟度 | 对 Agent | 判 |
|------|------|--------|----------|----|
| **Cube Core** | Apache-2.0 | GA，嵌入分析主流 | 原生 MCP；REST/GraphQL/SQL | **首选服务层** |
| **dbt MetricFlow / Semantic Layer** | 引擎开源；完整 API 偏 Cloud | GA；2026-01 **Open Semantic Interchange (OSI)** 以 MetricFlow 为声明规格，Snowflake/Salesforce/Cube/AtScale/Databricks 已签名 | YAML 口径，关系薄 | **口径定义互换格式** |
| AtScale | 商用 | 企业 MDX/Excel 深 | 有 Agent 接入 | 已有微软/Excel 重资产才考虑 |
| Snowflake Semantic Views / Databricks Metric Views / Fabric 语义模型 / LookML | 平台内 | GA 或深化中 | 锁在仓/BI 内 | **仓内可用，不作跨系统内核** |
| Honeydew 等仓专用层 | 商用 | 窄 | 窄 | 否 |

**选型**：口径 **用 Cube Core 对外服务**（含 MCP 给 Explore/场景只读）；定义优先写成 **可被 OSI/MetricFlow 互换的 YAML**，避免绑死 dbt Cloud。禁止用仓厂商 Semantic View 当唯一真相。

### 3.2 经营本体（Operating ontology）——内核

| 产品 | 本质 | 判 |
|------|------|----|
| **Palantir Foundry Ontology + AIP** | 对象 + 关系 + **Actions**；Agent 在本体上操作；可空转部署 | **能力对标，产品不买。** 买了就没有 UAS，只剩实施商 |
| **Microsoft Fabric IQ** | Power BI 语义模型升操作本体 + Operations Agent | Preview（Ignite 2025）；微软锁。学其「语义可触发动作」，不采用 |
| Salesforce Data Cloud / Agentforce 数据模型 | CRM 内本体 | 只当 S 层 SoR，不当 AIOS |
| SAP Datasphere | ERP 逻辑外溢 | 同左 |
| Timbr.ai 无头本体 | 本体能力不绑平台 | 可观察，不作为 P0 |
| **UAS 责任图 + 企业世界模型 schema** | Goal≡Org≡KPI≡Process；五维；Law Pack | **选定为经营本体内核** |

Palantir 证明了 2026 年「操作语义层」必须带 **Actions**，否则只是更好的 BI。我们的 Actions 不放进 Palantir，而放进 `cs.*` + Hub 门禁。

### 3.3 知识 / 时态图谱（Meaning + time）

| 产品 | 定位 | 成熟度 | 判 |
|------|------|--------|----|
| **Graphiti**（getzep，Apache-2.0） | 增量双时态 Context Graph；Pydantic 实体类型；Neo4j/FalkorDB/Neptune | ~29k stars，生产向；Zep 云为托管版 | **K 层运行时首选** |
| **Utopia**（DeepLethe） | 本体工作台 + 双时态 + 冲突审核 + Ontology2SQL | v0.1，schema 不回退 | **知识工程工作台 Spike**，不进内核 |
| Stardog / Graphwise / Ontotext GraphDB | RDF/OWL/SHACL 推理 | 企业重 | 法规/语义网硬需求再上 |
| TypeDB | 强类型多态知识库 | 利基 | P2 观察：公理很严时再评 |
| Neo4j / FalkorDB | 图存储 | 基础设施 | **Graphiti 的后端，不是本体** |
| LlamaIndex GraphRAG / Microsoft GraphRAG | 社区摘要批处理 | 批式，不适合高频变更 | Explore 可试用，不作记忆主干 |
| Cognee | 文档向知识引擎 | 中 | 文档重场景备选，次于 Graphiti |

### 3.4 Agent 工作记忆（与图谱不同）

| 产品 | 特长 | 判 |
|------|------|----|
| **Lethe / pylethe** | 遗忘轴、lexical 精确清除、Ed25519 回执 | **SelfPaw 记忆 + GDPR** |
| Mem0 | 召回强、遗忘弱 | 不首选 |
| Letta（MemGPT） | Agent 自己管记忆 | 与 Hub 控制面冲突，不作为平台 |
| Zep Cloud | Graphiti 托管 + 治理 | 若不想运 Neo4j 可买；默认先自持 Graphiti |
| 聊天历史当状态 | — | **宪章禁止** |

### 3.5 语义层最终栈

```text
L0  经营本体（自有）     责任图 + 五维 WM + Law Pack + ChangeSet
L1  口径服务（采购）     Cube Core ← YAML/OSI 口径
L2  时态知识（采购）     Graphiti（运行时）[+ Utopia 工作台可选]
L3  工作记忆（采购）     Lethe（SelfPaw，分库）
L4  主数据 SoR（连接）   CRM/ERP/数仓 经 cs.* ；不问「再造一个 MDM」
```

**L0 永不外包。** L1–L3 均可替换，契约是：只读进 scene/explore；写生产只走 Hub + `cs.*`。

### 3.6 为什么 L2 不用 Dify / FastGPT / Coze 的「知识库 + Agent」

这是高频误判：把「时态知识」听成「知识库」，再把 Dify 一类开源套件当成一步到位。

L2 要回答的问题是：**这条事实何时为真、被哪条证据推翻、和客户/审批怎么跳**。不是「把文档切块后 RAG 问答」，更不是「再买一个带 Agent 的知识库应用工厂」。

| 维度 | Graphiti（[+ Utopia 工作台]） | Dify / FastGPT / Coze 知识库+Agent |
|------|------------------------------|-------------------------------------|
| 数据模型 | 实体/关系/事实带 **valid_from–valid_to**；旧事实作废不删除 | 文档切片 + 向量/关键词；至多有文档更新时间 |
| 变更 | 增量 episode，不必整库重算 | 重切片、重嵌入；高频经营事件（拜访、阶段变更）不适合当主干 |
| 冲突 | 双时态显式；应当 vs 事实不静默覆盖 | RAG/摘要倾向「最新一段话赢」，冲突不可审计 |
| 接地 | fact → episode → 源系统 ID，可写入 Task `evidence_refs` | 命中 chunk，很难绑定责任图 `object_ref` / `source_node_id` |
| 类型 | Pydantic 白名单（Customer/Visit…）对齐客体 | 无经营本体；实体名由模型即兴 |
| 查询 | 现在为真 / 某日为真 / 关系遍历 | 语义相似；不能可靠问「8 月 1 日决策链是谁」 |
| 控制面 | 只读进 Hub；写生产仍走 `cs.*` | 自带工作流、工具、会话、权限，**第二套 OS** |
| 剖面 | 可挂 `explore` 只读 | 难以表达 scene 禁写 / runtime 才写 |
| 双轨 | 与 Lethe、责任图分库 | 个人上传文档与经营知识默认混在一个 Dataset |
| Agent 循环 | 不提供循环，避免第三套 | 自带 Agent，违反 ADR-SEL-002 |

因此：

1. **Dify 知识库 ≈ 文档 RAG**，和 GraphRAG 批处理同类，Explore 可作**辅检索**（`cs.doc.search`），**不能当 L2 主干**。  
2. **Dify Agent/工作流 ≈ 聊天应用工厂**，选型文已排除作 OS；若「只用它的知识库、不用 Agent」，实际仍要运一整套应用运行时，且检索语义对不上责任图。  
3. **Utopia 不是 Dify 替代品**：它是本体编辑 + 冲突审核工作台（可选 Spike）。Dify 的 Dataset UI 是文档管理，不是双时态冲突台。  
4. 若只要「员工问文档」，那是办公套件问题，不是经营中枢的 K-L2。

允许的用法（窄）：租户开关下，Explore 把 Dify/独立向量库当作 **文档源连接器**，经 Hub 只读；命中结果必须再接地到 Graphiti 或 `cs.*` 才能进 Insight。禁止 Dify 签发任务、写 CRM、当 live 状态。

---

## 4. Agent 平台：全景与评分

同样拆层。2026 年「Agent 框架」战争已经让位给 **耐久执行 + 开放协议 + 控制面**。

### 4.1 不要当操作系统买的东西

| 产品 | 为什么排除作为 AIOS |
|------|-------------------|
| Palantir AIP | 别人的操作本体 + Agent；实施重、锁平台 |
| Microsoft Copilot Studio / Agent 365 | 低摩擦，但数据与身份 gravitate 到微软租户 |
| Salesforce Agentforce | CRM 内最强；无 on-prem；按 action 计价；跨系统弱 |
| ServiceNow / SAP Joule / UiPath | 流程或 RPA 领地；可当 S 层系统，不当内核 |
| Dify / Coze / FastGPT / n8n 当 OS | 聊天/编排应用工厂，不是经营中枢 |
| CrewAI | 角色/人格优先，违反「岗位先于人格」 |
| AutoGen 当主干 | 会话中心，状态容易掉进对话 |
| 模型厂 Agents SDK 当内核 | OpenAI / Claude / Google ADK / AWS Strands 跟模型走；作适配器可以，作 OS 不行 |

### 4.2 循环与耐久（可采购）

| 产品 | 角色 | 判 |
|------|------|----|
| **Temporal** | 外环：长任务、审批暂停、失败精确续跑、SLA | **P0 耐久运行时** |
| **LangGraph 1.0** | 内环：有状态图、checkpoint、HITL interrupt | **P0 Agent 图**（Python 主栈） |
| PydanticAI | 类型安全工具 I/O；可挂 Temporal/DBOS | **工具契约层**，与 Hub JSON Schema 对齐 |
| Codex / Pi 级 harness | T1 已写「采购循环内核」 | **可选内环实现**；不要绑死品牌；与 LangGraph 二选一落地，不要三套循环 |
| Mastra / Vercel AI SDK | TS 内环 | 若前台纯 TS 再评；Hub 保持 Python/协议中立 |
| Agno | 轻量高性能 | 观察，不作主干 |
| Microsoft Agent Framework / Semantic Kernel | .NET/企业微软栈 | 客户全微软再适配 |
| Camunda / 专业 BPM | 确定性流程 SoR | **经 cs.* 调用，不替代 Temporal 外环** |

T1 Capability Hub 原文：「不自研第三套循环内核」。2026 补充：**外环 Temporal + 内环 LangGraph（或既有 Codex 循环）= 一套内核的两个尺度**，不是两套产品。

### 4.3 协议（面向未来必须押这里）

| 协议 | 方向 | 2026 状态 | 选型 |
|------|------|-----------|------|
| **MCP** | Agent → 工具（垂直） | Linux Foundation Agentic AI；企业网关模式 | **今天就部署**；所有 `cs.*` 对模型只暴露 MCP 语义名 |
| **A2A** | Agent → Agent（水平） | v1 左右；ACP 已并入 | **L2/L3 跨岗位再启用**；岗位 Agent Card |
| AG-UI | Agent → 前端事件流 | 与 CopilotKit/Bedrock 集成中 | **观察**；WorkStudio 先自有事件 |
| A2UI | 生成式 UI | 早期 | 观察 |
| ACP | 曾与 A2A 竞争 | **已弃用** | 忽略 |
| OSI（Open Semantic Interchange） | 口径定义互换 | 2026-01，MetricFlow 规格 | **口径层跟这个走** |

企业正确拼法（业界已收敛）：**A2A 在 Agent 之间，MCP 在 Agent 之内；身份、审批、审计是两者外面的共享控制面。** 这正好是 Hub 的位置。

### 4.4 Agent 平台最终栈

```text
控制面（自有）     Capability Hub
                 剖面 scene|explore|builder|runtime
                 双轨 · G0–G6 · 审批 · 审计 · Skill 发现≠执行

协议（开放）       MCP Gateway（工具）
                 A2A（跨岗位委托，P1+）

外环（采购）       Temporal：任务寿命、HITL、重试、Saga

内环（采购其一）   LangGraph 1.0  或  既有 Codex/Pi 循环
                 禁止再写第三套

工具契约           Pydantic / JSON Schema = cs.* 输入输出
                 模型不见 REST/SQL/密钥

记忆               Lethe（个人，可遗忘）
                 Graphiti（岗位上下文图，只读进建议前要接地）
```

---

## 5. 对标决策矩阵（浓缩）

| 候选 | 作语义内核 | 作 Agent OS | 作零件 |
|------|------------|-------------|--------|
| 责任图 + 五维 WM | **选定** | — | — |
| Capability Hub | — | **选定** | — |
| Palantir Ontology/AIP | 否（锁） | 否 | 对标学习 Actions |
| Fabric IQ / Copilot Studio | 否 | 否 | 客户微软栈可适配连接器 |
| Agentforce | 否 | 否 | CRM SoR + cs.sales.* |
| Cube Core | 否 | 否 | **口径 MCP** |
| MetricFlow / OSI | 否 | 否 | **口径互换** |
| Graphiti | 否 | 否 | **时态知识运行时** |
| Utopia | 否 | 否 | 知识工作台 Spike |
| Lethe | 否 | 否 | SelfPaw 遗忘记忆 |
| LangGraph | 否 | 否 | **内环** |
| Temporal | 否 | 否 | **外环** |
| MCP + A2A | 否 | 否 | **协议本体** |
| CrewAI / Dify / 聊天壳 | 否 | 否 | 不用 |

---

## 6. 18 个月落地节奏

| 阶段 | 语义 | Agent |
|------|------|-------|
| **现在–6 周** | 责任图 schema 作为 L0 唯一写入；Cube 或等价 YAML 先手工对齐 LTC 口径 | Hub 四剖面保持；MCP Gateway 包现有只读查询；禁止新循环框架分叉 |
| **Q1** | Graphiti 接 Explore：客户时间线 / what-changed；证据进 Task | Temporal 接 Runtime 长任务与审批暂停；内环选定 LangGraph **或** 固化 Codex 循环（二选一写进 ADR） |
| **Q2** | Cube Core 对外 MCP；OSI 口径文件进 git | A2A Agent Card 仅岗位级（CM / 法务 / 指挥席）；Lethe 分库 |
| **Q3–Q4** | Utopia 仅当知识审核台评估；不接写 | 执行门禁仍在 Hub；外部「ontology action」若出现（Utopia/Fabric）只做 **cs.* 前的额外检查** |
| **明确不做** | 不迁 Palantir；不以仓 Semantic View 为内核；不以 Graphiti 替代责任图 | 不以 Copilot Studio/Agentforce 为 OS；不引入 CrewAI；不把聊天历史当状态 |

---

## 7. ADR 草案（选型冻结）

**ADR-SEL-001 语义分层**  
经营本体自有（责任图 + 五维 + Law Pack）。口径采购 Cube Core + OSI 可互换定义。时态知识采购 Graphiti。文档本体工作台可选 Utopia，默认不进生产写路径。

**ADR-SEL-002 Agent 双环**  
控制面自有 Hub。外环 Temporal。内环**默认 LangGraph 1.0**（经 InnerLoop SPI）。既有 Codex/Pi 仅作同一 SPI 的备选实现，禁止并行第三套。工具对模型只经 MCP Gateway。跨岗位委托用 A2A，不用自研总线。  
落地权威：[`UAS AIOS架构规划（自研OR集成）.md`](./UAS%20AIOS架构规划（自研OR集成）.md)。

**ADR-SEL-003 禁替代清单**  
禁止用 Palantir/Fabric IQ/Agentforce/Copilot Studio 替换 L0 或 Hub。禁止用口径层或知识图谱签发生产写。禁止第三套 Agent 循环。

---

## 8. 面向未来的判断（为什么这套能活过 18–36 个月）

1. **操作本体会继续被巨头产品化**（Palantir、微软、Salesforce）。自有 L0 是唯一不被收编的护城河。  
2. **口径会协议化**（OSI）。押互换格式，不押某一家 Cloud Semantic Layer。  
3. **Agent 框架会继续换皮**；耐久执行（Temporal）和协议（MCP/A2A）会留下。内环可换，外环与网关不换。  
4. **遗忘与双时态**会成为合规刚需。Lethe + Graphiti 补的是 Hub 没有、BI 也不做的轴。  
5. **聊天壳与人格编排**会被办公套件吞掉。UAS 继续做「看见并办成」，不跟面积战。

争议时：德压过术；G 层否决权高于「某开源项目 star 更多」。
