# UAS-AIOS 企业级可视化蓝图

> 本文把 UAS-AIOS 当前的架构理念、产品定义、功能设计、工程架构与 Enterprise Sales OS MVP 规约统一用图形化方式表达。详细文字规约见 [企业级 Agent 生态体系](./UAS_AIOS_ENTERPRISE_AGENT_ECOSYSTEM_L1_L3.md)、[企业级产品蓝图](./UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md) 与 [Enterprise Sales OS MVP 开发规约包](./enterprise-sales-os/README.md)。

---

## 1. 从第一性方法论到产品落地

```mermaid
flowchart TB
    Tao["道: 企业存在与价值创造原则"] --> De["德: 组织价值约束与合规边界"]
    De --> Shi["势: 主体差异 / 权限 / 资源 / 风险"]
    Shi --> Shu["术: Agent 策略 / 流程 / 治理规则"]
    Shu --> Qi["器: UAS Enterprise 产品套件"]

    Qi --> UAS["UAS-Platform = I,K,R,A,S,G,E,Pi"]
    UAS --> WM["世界模型: 空间 / 时间 / 主体 / 客体 / 反馈"]
    UAS --> ASUI["ASUI: 知识即配置 / 构建即运行 / 增量演化"]
    UAS --> Dual["双轨 AGI: selfpaw + PiPaw"]

    Dual --> L1["L1 SelfPaw Enterprise"]
    Dual --> L2["L2 PiPaw Workbench"]
    Dual --> L3["L3 PiPaw Growth & Service"]

    L1 --> MVP["Enterprise Sales OS MVP"]
    L2 --> MVP
    L3 --> MVP
    WM --> MVP
    ASUI --> MVP
```

---

## 2. 企业级 L1-L3 数字人生态

```mermaid
flowchart LR
    Employee["员工 / 经理"] --> L1["L1 个人数字分身<br/>SelfPaw Enterprise"]
    Customer["客户 / 渠道 / 官网"] --> Gateway["Outward Gateway"]

    L1 -->|Intent + Evidence + Scope + Risk| L2["L2 职能数字人<br/>PiPaw Workbench"]
    Gateway -->|客户意图 / 线索 / 工单| L3["L3 经营数字人<br/>PiPaw Growth & Service"]

    L2 --> Capability["cs.* 语义能力服务"]
    L3 --> Capability

    Capability --> Mesh["System Mesh / S-Grid"]
    Mesh --> CRM["CRM"]
    Mesh --> BPM["BPM"]
    Mesh --> ERP["ERP"]
    Mesh --> Finance["Finance"]
    Mesh --> DWH["Data Warehouse"]

    Capability --> Audit["Audit Chain"]
    Capability --> KPI["KPI Store"]
    Audit --> Evolution["ChangeSet / Evolution"]
    KPI --> Evolution
    Evolution --> Packs["Domain / Workflow / Law / Agent / Connector Pack"]
    Packs --> L1
    Packs --> L2
    Packs --> L3
```

---

## 3. 产品套件关系图

```mermaid
flowchart TB
    subgraph Experience["体验与岗位入口"]
        SP["SelfPaw Enterprise<br/>个人意图 / 证据 / 升级"]
        PW["PiPaw Workbench<br/>职能任务 / 审批 / 调度"]
        PGS["PiPaw Growth & Service<br/>获客 / 转化 / 服务 / 续约"]
    end

    subgraph Platform["平台能力"]
        DGP["Data & Governance Plane<br/>租户 / 权限 / 审计 / 策略"]
        CH["Capability Hub<br/>cs.* / 连接器 / 字段映射"]
        PS["Pack Studio<br/>Domain / Workflow / Law / Agent Pack"]
    end

    SP --> PW
    SP --> PGS
    PW --> CH
    PGS --> CH
    CH --> DGP
    DGP --> PS
    PS --> SP
    PS --> PW
    PS --> PGS
```

---

## 4. 功能地图

```mermaid
flowchart TB
    Product["UAS Enterprise"]

    Product --> SP["SelfPaw Enterprise"]
    SP --> SP1["组织身份绑定"]
    SP --> SP2["Intent Hub"]
    SP --> SP3["Evidence Capture"]
    SP --> SP4["授权内执行"]
    SP --> SP5["个人蜂群决策"]
    SP --> SP6["向上升级"]

    Product --> PW["PiPaw Workbench"]
    PW --> PW1["Task Inbox"]
    PW --> PW2["Evidence Board"]
    PW --> PW3["Agent Dispatch"]
    PW --> PW4["Approval Gate"]
    PW --> PW5["Decision Memo"]
    PW --> PW6["KPI Attribution"]

    Product --> PGS["PiPaw Growth & Service"]
    PGS --> PGS1["Outward Gateway"]
    PGS --> PGS2["Lead Qualification"]
    PGS --> PGS3["Solution & Quote"]
    PGS --> PGS4["Service & SLA"]
    PGS --> PGS5["Renewal & Upsell"]
    PGS --> PGS6["Customer Audit Trail"]

    Product --> DGP["Data & Governance Plane"]
    DGP --> DGP1["Tenant & Identity"]
    DGP --> DGP2["Scope & Policy"]
    DGP --> DGP3["Audit Chain"]
    DGP --> DGP4["Master Data"]
    DGP --> DGP5["Event Stream"]
    DGP --> DGP6["ChangeSet Center"]

    Product --> CH["Capability Hub"]
    CH --> CH1["Capability Catalog"]
    CH --> CH2["Connector Runtime"]
    CH --> CH3["Field Mapping"]
    CH --> CH4["Policy Adapter"]
    CH --> CH5["Result Normalizer"]

    Product --> PS["Pack Studio"]
    PS --> PS1["Domain Pack"]
    PS --> PS2["Workflow Pack"]
    PS --> PS3["Law Pack"]
    PS --> PS4["Agent Pack"]
    PS --> PS5["Connector Pack"]
    PS --> PS6["Evaluation Pack"]
```

---

## 5. 技术工程分层

```mermaid
flowchart TB
    XL["Experience Layer<br/>SelfPaw UI / PiPaw Workbench / Growth Service / Admin"]
    AAL["Agent Application Layer<br/>Intent Hub / Task Board / Evidence Board / Agent Dispatch"]
    Core["UAS Core Runtime<br/>Context Injector / Orchestrator / State Store / Queue / AEE"]
    GE["Governance & Evolution Plane<br/>Policy Engine / Audit Chain / Approval Gate / ChangeSet"]
    CSL["Capability Service Layer<br/>cs.* API / Connector Runtime / Field Mapping / Result Normalizer"]
    SDP["Sovereign Data Plane<br/>Tenant / Identity / Master Data / Event Stream / KPI Store"]
    ES["Enterprise Systems<br/>CRM / BPM / ERP / Finance / DWH / Document System"]

    XL --> AAL --> Core --> GE --> CSL --> SDP --> ES
    ES -->|system events| SDP
    SDP -->|feedback| GE
    GE -->|policies / changesets| Core
```

---

## 6. 逻辑服务依赖

```mermaid
flowchart LR
    Intent["intent-service"] --> Evidence["evidence-service"]
    Evidence --> Orchestrator["agent-orchestrator"]
    Orchestrator --> Task["task-service"]
    Task --> Policy["policy-service"]
    Policy --> Approval["approval-service"]
    Policy --> Capability["capability-service"]
    Capability --> Connector["connector-service"]
    Connector --> Systems["enterprise systems"]
    Capability --> Audit["audit-service"]
    Audit --> Event["event-service"]
    Event --> KPI["kpi-service"]
    KPI --> ChangeSet["changeset-service"]
    ChangeSet --> Pack["pack-registry"]
    Pack --> Orchestrator
    Pack --> Policy
```

---

## 7. 运行时主路径

```mermaid
sequenceDiagram
    participant User as 用户/客户/系统事件
    participant Intent as Intent Hub
    participant Evidence as Evidence Board
    participant Policy as Policy Engine
    participant Agent as PiPaw Agent
    participant Cap as Capability Hub
    participant Sys as System Mesh
    participant Audit as Audit Chain
    participant KPI as KPI Store
    participant Change as ChangeSet Center

    User->>Intent: 提交意图或业务事件
    Intent->>Evidence: 标准化 intent + 证据要求
    Evidence->>Policy: 提交 actor + scope + evidence
    Policy-->>Intent: allow / approval_required / deny
    Intent->>Agent: 分派任务
    Agent->>Cap: 调用 cs.*
    Cap->>Policy: 调用前策略检查
    Cap->>Sys: connector / script / MCP
    Sys-->>Cap: 标准化结果
    Cap->>Audit: 追加 capability_call
    Cap-->>Agent: result / error / rollback_ref
    Agent->>KPI: 记录业务结果
    KPI->>Change: 触发演化评估
    Change-->>Agent: ChangeSet draft
```

---

## 8. `cs.*` 能力调用图

```mermaid
flowchart LR
    Agent["PiPaw Agent"] --> Envelope["Capability Envelope<br/>capability / actor / scope / inputs / audit"]
    Envelope --> Validate["Schema Validation"]
    Validate --> Policy["Policy Adapter"]
    Policy --> Idem["Idempotency Check"]
    Idem --> Mapping["Field Mapping"]
    Mapping --> Connector["Connector Runtime"]
    Connector --> Mock["Mock CRM/BPM/Finance"]
    Mock --> Normalize["Result Normalizer"]
    Normalize --> Audit["Audit Append"]
    Audit --> Result["Standard Response<br/>status / result / error / rollback"]

    Validate -->|VALIDATION_ERROR| Result
    Policy -->|POLICY_DENIED| Result
    Idem -->|IDEMPOTENCY_CONFLICT| Result
    Connector -->|CONNECTOR_UNAVAILABLE| Result
```

---

## 9. 核心数据模型

```mermaid
erDiagram
    TENANT ||--o{ ACTOR : owns
    TENANT ||--o{ INTENT : contains
    ACTOR ||--o{ INTENT : creates
    INTENT ||--o{ EVIDENCE : references
    INTENT ||--o{ TASK : creates
    INTENT ||--o{ CAPABILITY_CALL : triggers
    INTENT ||--o{ AUDIT_EVENT : traces
    INTENT ||--o{ KPI_EVENT : measures
    INTENT ||--o| CHANGESET : proposes
    LEAD ||--o| ACCOUNT : maps_to
    LEAD ||--o{ QUOTE : requests
    QUOTE ||--o| APPROVAL : requires
    TASK ||--o{ AUDIT_EVENT : records
    CAPABILITY_CALL ||--o{ AUDIT_EVENT : records

    TENANT {
      string tenant_id
      string deployment_mode
      string data_region
    }
    ACTOR {
      string actor_id
      string actor_type
      string roles
    }
    INTENT {
      string intent_id
      string source
      string intent_type
      string risk_level
      string status
    }
    LEAD {
      string lead_id
      string qualification_status
      number qualification_score
    }
    QUOTE {
      string quote_id
      number net_amount
      number discount_rate
      string quote_status
    }
    APPROVAL {
      string approval_id
      string risk_level
      string status
    }
    CHANGESET {
      string changeset_id
      string target_pack
      string approval_status
    }
```

---

## 10. Enterprise Sales OS MVP 闭环

```mermaid
flowchart TB
    Input["官网线索 / 销售录入 / SelfPaw 升级"]
    Intent["Intent Hub<br/>生成标准意图单"]
    Evidence["Evidence Board<br/>证据校验"]
    Qualify["cs.lead.qualify<br/>线索资格判断"]
    Quote["cs.quote.draft<br/>报价草案"]
    Policy["Policy Engine<br/>G0-G4 / 金额 / 折扣 / 信用"]
    Approval["cs.approval.start<br/>审批任务"]
    Review["Sales / Finance / Compliance Review"]
    Report["审计报告 + KPI 摘要"]
    Change["ChangeSet 草案"]

    Input --> Intent --> Evidence --> Qualify --> Quote --> Policy
    Policy -->|G2| Report
    Policy -->|G3/G4| Approval --> Review --> Report
    Policy -->|blocked| Report
    Report --> Change
```

---

## 11. 治理决策树

```mermaid
flowchart TB
    Start["报价草案"] --> Scope["actor/action/data scope?"]
    Scope -->|否| Deny["POLICY_DENIED"]
    Scope -->|是| Evidence["证据满足?"]
    Evidence -->|否| NeedEvidence["EVIDENCE_REQUIRED<br/>collect_evidence task"]
    Evidence -->|是| Credit["credit_level blocked?"]
    Credit -->|是| Block["BUSINESS_RULE_BLOCKED"]
    Credit -->|否| Amount["金额 / 折扣判断"]
    Amount -->|net < 100000 and discount <= 10%| G2["G2<br/>内部草案"]
    Amount -->|net < 500000 or discount <= 25%| G3["G3<br/>sales_manager"]
    Amount -->|net >= 500000 or discount > 25%| G4["G4<br/>sales_manager + finance"]
    Amount -->|discount > 40%| Hard["默认拒绝 / 战略客户人工豁免"]
```

---

## 12. 工作流状态机

```mermaid
stateDiagram-v2
    [*] --> intent_created
    intent_created --> evidence_checking
    evidence_checking --> lead_qualifying
    evidence_checking --> evidence_required
    lead_qualifying --> quote_drafting
    lead_qualifying --> evidence_required
    lead_qualifying --> failed_retryable
    quote_drafting --> policy_checking
    quote_drafting --> business_blocked
    quote_drafting --> failed_retryable
    policy_checking --> approved
    policy_checking --> approval_pending
    policy_checking --> evidence_required
    policy_checking --> business_blocked
    approval_pending --> approved
    approval_pending --> rejected
    approval_pending --> evidence_required
    rejected --> quote_drafting
    approved --> report_rendered
    business_blocked --> report_rendered
    failed_retryable --> lead_qualifying
    failed_retryable --> needs_human
    evidence_required --> needs_human
    needs_human --> evidence_checking
    report_rendered --> changeset_drafted
    changeset_drafted --> closed
    closed --> [*]
```

---

## 13. 世界模型五维配置图

```mermaid
flowchart TB
    WM["Enterprise Sales World Model"]

    WM --> Space["空间<br/>租户 / 部门 / 渠道 / 系统边界 / 数据 scope"]
    WM --> Time["时间<br/>SLA / 报价有效期 / 审批时限 / 销售周期"]
    WM --> Subject["主体<br/>sales_rep / manager / finance / compliance / customer / agent"]
    WM --> Object["客体<br/>Lead / Account / Quote / Approval / Evidence / Task"]
    WM --> Feedback["反馈<br/>capability_result / approval_result / manual_feedback / KPI"]

    Subject --> Drive["推动<br/>预算明确 / 需求明确 / 决策人明确"]
    Object --> Blocker["阻碍<br/>证据不足 / 折扣超阈值 / 信用 blocked"]
    Feedback --> Connector["连接<br/>cs.approval.start / audit / KPI / ChangeSet"]
```

---

## 14. 反馈与 ChangeSet 演化闭环

```mermaid
flowchart LR
    Run["一次业务运行"] --> Feedback["人工反馈 / 审批意见 / 能力失败 / KPI 偏差"]
    Feedback --> Attribution["归因<br/>Domain / Workflow / Law / Agent / Connector / Evaluation"]
    Attribution --> Draft["ChangeSet Draft"]
    Draft --> Review["Human Review"]
    Review -->|reject| Archive["保留原因 + audit"]
    Review -->|approve| NonProd["Apply to non-prod config"]
    NonProd --> Acceptance["运行验收用例"]
    Acceptance -->|pass| Promote["人工发布"]
    Acceptance -->|fail| Draft
```

---

## 15. Pack 到运行时的映射

```mermaid
flowchart TB
    Domain["Domain Pack<br/>ontology / terms / lifecycle"] --> Context["Context Injector"]
    Workflow["Workflow Pack<br/>workflow_config"] --> Runtime["Runtime Manager"]
    Law["Law Pack<br/>governance_policy"] --> Policy["Policy Engine"]
    Agent["Agent Pack<br/>swarm_agents / skills"] --> Orchestrator["Agent Orchestrator"]
    Connector["Connector Pack<br/>system_registry / field_mapping"] --> Capability["Capability Hub"]
    Evaluation["Evaluation Pack<br/>evaluate_sales_loop"] --> Evolution["Evolution Engine"]

    Context --> Orchestrator
    Runtime --> Orchestrator
    Policy --> Capability
    Orchestrator --> Capability
    Capability --> Evolution
```

---

## 16. MVP 验收矩阵

```mermaid
flowchart TB
    Cases["MVP Acceptance Cases"]
    Cases --> C1["CASE-001<br/>标准线索自动生成报价草案"]
    Cases --> C2["CASE-002<br/>折扣超阈值进入销售经理审批"]
    Cases --> C3["CASE-003<br/>大金额报价进入财务审批"]
    Cases --> C4["CASE-004<br/>证据不足进入补证据"]
    Cases --> C5["CASE-005<br/>信用 blocked 拦截"]
    Cases --> C6["CASE-006<br/>connector 可重试失败"]
    Cases --> C7["CASE-007<br/>审批拒绝生成降折扣建议"]
    Cases --> C8["CASE-008<br/>人工反馈生成 ChangeSet 草案"]

    C1 --> Output["统一输出<br/>intent / audit / report / world_model_view / state"]
    C2 --> Output
    C3 --> Output
    C4 --> Output
    C5 --> Output
    C6 --> Output
    C7 --> Output
    C8 --> Output
```

---

## 17. 仓库落地路径

```mermaid
flowchart TB
    Specs["docs/enterprise-sales-os<br/>开发规约包"] --> Project["projects/enterprise-sales-os"]
    Project --> Configs["configs<br/>platform / workflow / agents / governance / evolution / world_model / capability"]
    Project --> Scripts["scripts<br/>cs_lead_qualify / cs_quote_draft / cs_approval_start / evaluate"]
    Project --> DB["database<br/>audit / events / feedback / changesets / state"]
    Project --> Reports["reports<br/>audit_report / kpi_summary / evolution"]

    Configs --> Runtime["scripts/run_uas_runtime_service.py"]
    Scripts --> Runtime
    DB --> Runtime
    Runtime --> Validate["list / validate / run / state"]
    Validate --> Acceptance["MVP_ACCEPTANCE_CASES"]
```

---

## 18. 版本路线图

```mermaid
flowchart LR
    V01["v0.1<br/>文档蓝图"] --> V02["v0.2<br/>配置原型"]
    V02 --> V03["v0.3<br/>闭环 MVP"]
    V03 --> V04["v0.4<br/>治理增强"]
    V04 --> V05["v0.5<br/>Pack 化"]
    V05 --> V10["v1.0<br/>企业试点"]

    V02 --> D02["runtime discover + mock scripts"]
    V03 --> D03["lead -> quote -> approval -> audit"]
    V04 --> D04["G0-G4 + field scope + policy tests"]
    V05 --> D05["pack registry + reusable templates"]
    V10 --> D10["real CRM/BPM/Finance connector"]
```
