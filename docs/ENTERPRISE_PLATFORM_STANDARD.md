# 企业级 UAS 平台标准（Enterprise Platform Standard）

> **版本** 1.0 | 2026-05  
> **状态** 标准文档（Normative for 企业级产品设计与工程实现）  
> **适用范围** ACA-protocol / UAS-AIOS 企业版（数字人生态 L1–L3、cs.* 语义能力、双轨 AGI）

---

## 一、文档体系

| 编号 | 文档 | 类型 | 读者 |
|------|------|------|------|
| EPS-00 | 本文 | 总纲与索引 | 全员 |
| EPS-01 | [ENTERPRISE_DIGITAL_HUMAN_L1_L3_ECOSYSTEM.md](./ENTERPRISE_DIGITAL_HUMAN_L1_L3_ECOSYSTEM.md) | 战略与架构 | 决策层、架构师 |
| EPS-02 | [ENTERPRISE_PRODUCT_FUNCTIONAL_SPEC.md](./ENTERPRISE_PRODUCT_FUNCTIONAL_SPEC.md) | **产品功能规格** | 产品、业务、交付 |
| EPS-03 | [ENTERPRISE_TECHNICAL_MODULE_SPEC.md](./ENTERPRISE_TECHNICAL_MODULE_SPEC.md) | **技术模块规格** | 研发、架构、集成 |
| EPS-04 | [ENTERPRISE_CS_CAPABILITY_PROTOCOL.md](./ENTERPRISE_CS_CAPABILITY_PROTOCOL.md) | cs.* 协议 | 研发、集成商 |
| EPS-05 | [ENTERPRISE_CS_CAPABILITY_CATALOG_STANDARD.md](./ENTERPRISE_CS_CAPABILITY_CATALOG_STANDARD.md) | 能力目录标准 | 产品、业务分析 |
| EPS-06 | [ENTERPRISE_INTENT_EVIDENCE_STANDARD.md](./ENTERPRISE_INTENT_EVIDENCE_STANDARD.md) | Intent/Evidence | 研发、合规 |
| EPS-07 | [ENTERPRISE_STAKEHOLDER_PLAYBOOK.md](./ENTERPRISE_STAKEHOLDER_PLAYBOOK.md) | 分层推动话术 | 售前、PMO |

**基础平台标准（非企业专属）**： [UAS_PLATFORM_STANDARD.md](./UAS_PLATFORM_STANDARD.md) · [ASUI_AUTONOMOUS_AGENT_STANDARD.md](./ASUI_AUTONOMOUS_AGENT_STANDARD.md)

---

## 二、标准层级模型

```
理论层    THEORY_SYSTEM / AGI_WORLD_MODEL_UAS / 道德势术器
    ↓
平台层    UAS (I,K,R,A,S,G,E,Π) + ASUI
    ↓
企业层    数据平面 + cs.* + DH-L1/L2/L3 + SelfPaw/ΠPaw   ← EPS-01～07
    ↓
交付层    Domain 包 / 岗位包 / 连接器包 / subapp (projects/*)
```

**企业层增加的不可省略约束**：

1. 租户主权与审计链（数据平面）  
2. Agent 仅调用 `cs.*`（语义能力层）  
3. 双轨升级协议（Intent + Evidence）  
4. 确定性终裁（G6 + execution_mode）

---

## 三、产品模块与技术模块对照（摘要）

| 产品模块（EPS-02） | 技术模块（EPS-03） | UAS 层 |
|-------------------|-------------------|--------|
| 租户与身份控制台 | TenantContextService | G |
| 数据平面管理 | DataPlaneAdmin + EventBus + AuditChain | S/G |
| CS Studio（能力目录） | CsRegistry + CsRouter | S |
| 连接器中心 S-Grid | SGridAdapterManager | S |
| 法则包管理 | PolicyBundleService | G/K |
| Intent Hub | IntentService | I |
| SelfPaw 工作台 | SelfPawRuntime（U 轨扩展） | I,R,A |
| ΠPaw 工作台 / 岗位工作室 | PiPawOrchestrator | A |
| 对外网关 | OutwardGateway | S/G |
| 审计与合规中心 | AuditQuery + G6Escalation | G |
| 演化与 KPI 中心 | EvolutionCenter + KpiAttribution | E |
| 运行时运维 | UASRuntimeService（已有） | R |

完整功能条目见 EPS-02；接口与部署单元见 EPS-03。

---

## 四、需求编号规则

| 前缀 | 含义 | 示例 |
|------|------|------|
| `FR-` | 产品功能需求（Functional Requirement） | FR-CS-012 |
| `NFR-` | 非功能需求 | NFR-AUD-001 |
| `TM-` | 技术模块（Technical Module） | TM-CS-Router |
| `API-` | 对外/对内 API 契约 | API-CS-Invoke |
| `CFG-` | 配置与包结构 | CFG-Domain-Pack |

---

## 五、实现阶段（R0–R3）

| 阶段 | 目标 | 产品可演示 | 技术交付 |
|------|------|------------|----------|
| **R0** | 单租户单闭环 | CS Studio 只读 + 1 条 cs 链路演 | CsRouter MVP、审计 JSONL |
| **R1** | DH-L3 单场景 | 对外留资→报价 + 审批 | Intent/Evidence + 岗位白名单 |
| **R2** | 双轨升级 | SelfPaw 升级 ΠPaw Task | IntentService + U 轨 scope |
| **R3** | 多租户商业 | 席位、法则包热更新、连接器市场 | 租户隔离 + 能力版本治理 |

当前仓库基线：**R0 部分**（subapp Runtime、ToolGateway、CapabilityRegistry 子集）。

---

## 六、配置与 Schema 资产

| 路径 | 用途 |
|------|------|
| `configs/enterprise_cs_capability_registry.example.json` | cs 能力注册表 |
| `configs/enterprise_digital_human_tiers.example.json` | DH 层级与岗位 |
| `configs/enterprise_data_plane_manifest.example.json` | 数据平面 |
| `configs/schemas/enterprise_intent.schema.json` | Intent 单 JSON Schema |
| `configs/schemas/enterprise_evidence_bundle.schema.json` | Evidence 包 |
| `configs/schemas/enterprise_cs_invoke.schema.json` | cs 调用信封 |

---

## 七、符合性检查清单（发布前）

- [ ] 所有 Agent 工具项均为 `cs.*`，无厂商 API 名  
- [ ] 资金/审批/合规能力标记 `execution_mode: deterministic`  
- [ ] 每次 cs 调用产生 `audit_id` 并可按 `request_id` 查询  
- [ ] DH 岗位配置含 `allowed_capabilities` 白名单  
- [ ] 升级路径含 Intent + Evidence 最小字段集（EPS-06）  
- [ ] subapp 满足 [ASUI_AUTONOMOUS_AGENT_STANDARD.md](./ASUI_AUTONOMOUS_AGENT_STANDARD.md)

---

*修订记录：1.0 初版，与 ENTERPRISE_DIGITAL_HUMAN L1-L3 生态对齐。*
