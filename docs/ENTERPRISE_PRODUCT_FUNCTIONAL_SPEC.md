# 企业级 UAS 产品功能规格（EPS-02）

> **版本** 1.0 | **父标准**：[ENTERPRISE_PLATFORM_STANDARD.md](./ENTERPRISE_PLATFORM_STANDARD.md)

---

## 1. 文档说明

### 1.1 目的

定义企业级数字人生态的**可交付产品功能**，供产品设计、研发排期、验收测试与商业报价使用。

### 1.2 角色（Persona）

| ID | 角色 | 典型用户 | 主要触点 |
|----|------|----------|----------|
| P-ADM | 租户管理员 | IT/数字化负责人 | 租户控制台、CS Studio、连接器 |
| P-GOV | 合规治理 | 内审、法务、风控 | 法则包、G6、审计中心 |
| P-BIZ | 业务负责人 | 销售/客服/财务总监 | ΠPaw 岗位工作室、KPI |
| P-EMP | 一线员工 | 销售、客服、HR | SelfPaw 工作台 |
| P-OPS | 平台运维 | SRE、实施顾问 | 运行时运维、连接器 |
| P-EXT | 外部客户 | 官网访客、渠道 | 对外网关（无控制台） |

### 1.3 优先级

| 级别 | 含义 |
|------|------|
| P0 | R0/R1 必须，无则无法演示单闭环 |
| P1 | R1/R2 必须，双轨与岗位化 |
| P2 | R2/R3，多租户与商业化 |
| P3 | 增强体验、生态市场 |

---

## 2. 产品模块总览

```
┌─────────────────────────────────────────────────────────────────┐
│                    企业控制台 Enterprise Console                 │
├────────────┬────────────┬────────────┬────────────┬────────────┤
│ 租户与身份  │ CS Studio  │ S-Grid     │ 法则包     │ 审计合规   │
│ FR-TEN-*   │ FR-CS-*    │ FR-GRID-*  │ FR-POL-*   │ FR-AUD-*   │
├────────────┴────────────┴────────────┴────────────┴────────────┤
│  SelfPaw 工作台 (DH-L1)          │  ΠPaw 工作台 (DH-L2/L3)      │
│  FR-SP-*                         │  FR-PP-*                     │
├──────────────────────────────────┴──────────────────────────────┤
│  对外网关 FR-GW-*  │  演化/KPI FR-EVO-*  │  运行时运维 FR-RT-*     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 模块功能规格

### 3.1 租户与身份控制台（Tenant & Identity）

**目标**：建立企业主权边界，为所有 cs 调用注入 `tenant_id` + `actor`。

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-TEN-001 | 租户开通 | P0 | 创建租户、区域、数据驻留策略 | 生成 tenant_id，写入数据平面 manifest |
| FR-TEN-002 | SSO 绑定 | P1 | OIDC/SAML 对接企业 IdP | 登录后映射 user_id |
| FR-TEN-003 | 组织树同步 | P1 | 部门/岗位从 HR 或手工维护 | 岗位 ID 可用于 scope |
| FR-TEN-004 | 角色与 scope | P0 | RBAC/ABAC：定义 `lead:write` 等 scope | cs 调用前校验失败可解释 |
| FR-TEN-005 | 席位管理 | P2 | DH-L1/L2/L3 席位分配与到期 | 超额调用返回 `SEAT_LIMIT` |
| FR-TEN-006 | 服务账号 | P1 | Agent/网关用 machine actor | 与个人 actor 审计区分 |

**用户故事（P-ADM）**：作为 IT 管理员，我能为销售部开通 50 个 DH-L1 席位，并限制他们只能调用 `cs.lead.*` 与 `cs.customer.search`。

---

### 3.2 数据平面管理（Data Plane Admin）

**目标**：主数据、事件流、审计链的可视与策略配置（非业务 OLTP 替代）。

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-DP-001 | 主数据域配置 | P1 | 声明 customer/product/org 等 SoR | 与 `cs.mdm.resolve` 联动 |
| FR-DP-002 | 事件主题订阅 | P1 | intent.* / cs.* 主题可见 | 支持按 tenant 过滤 |
| FR-DP-003 | 审计保留策略 | P0 | 保留天数、脱敏级别 | 与 audit_level 一致 |
| FR-DP-004 | 主权策略 | P0 | 禁止 Agent 直连外部 API 开关 | 配置为 false 时集成测试失败 |
| FR-DP-005 | 数据导出 | P2 | 合规场景批量导出 audit | 含 request_id 链路 |

---

### 3.3 CS Studio（语义能力目录）

**目标**：产品化定义、发布、版本化 `cs.*` 能力（见 EPS-05）。

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-CS-001 | 能力目录浏览 | P0 | 按 domain 分组展示能力卡片 | 含 execution_mode、scope |
| FR-CS-002 | 能力卡片 CRUD | P0 | 创建/编辑能力定义与 schema | 导出 registry JSON |
| FR-CS-003 | 版本发布 | P0 | capability_version 发布与冻结 | 旧版调用可指定版本 |
| FR-CS-004 | 模拟调用 | P0 | 沙箱 invoke（不真实写后端） | 返回契约校验结果 |
| FR-CS-005 | 绑定法则包 | P1 | 能力关联 policy_bundle_id | 拒绝时返回 POLICY_DENIED |
| FR-CS-006 | 绑定连接器 | P0 | 选择 implements_backend | 健康检查状态可见 |
| FR-CS-007 | 岗位白名单预览 | P1 | 按岗位 Agent 查看可用 cs | 与 FR-PP-003 一致 |
| FR-CS-008 | 变更影响分析 | P2 | 版本升级影响哪些岗位包 | 列出依赖方 |

**用户故事（P-BIZ + P-ADM）**：作为销售总监，我能看到「销售顾问岗位」能用的 8 个业务能力，且不能看到财务开票能力。

---

### 3.4 S-Grid 连接器中心

**目标**：CRM/BPM/ERP 适配器管理，**不对 Agent 暴露**。

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-GRID-001 | 连接器注册 | P0 | 注册 backend_id、类型、凭证槽 | 凭证加密存储 |
| FR-GRID-002 | 字段映射 | P0 | 厂商字段 ↔ cs payload schema | 映射测试通过 |
| FR-GRID-003 | 健康检查 | P0 | 定时探测连接器 | 不健康时 cs 返回 DEGRADED |
| FR-GRID-004 | 幂等与重试 | P0 | idempotency_key 透传 | 重复请求不重复副作用 |
| FR-GRID-005 | 死信与升级 | P1 | 失败 N 次创建 ΠPaw Task | Task 含 request_id |
| FR-GRID-006 | 多后端路由 | P2 | 同一 cs 多 backend 主备 | 可配置 failover |

---

### 3.5 法则包管理（Policy Bundle）

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-POL-001 | 法则包版本 | P1 | 定价/信用/审批矩阵版本化 | policy_bundle_id 可引用 |
| FR-POL-002 | 热更新 | P2 | 不重启 Agent 生效新规则 | 审计记录 bundle 切换 |
| FR-POL-003 | 仿真回放 | P2 | 历史请求用新规则重放 | 仅沙箱，不写生产 |
| FR-POL-004 | 红线规则 | P1 | G6 红线条目维护 | 触发强制升级人工 |

---

### 3.6 Intent Hub（SelfPaw 企业版入口）

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-SP-001 | 自然语言意图识别 | P0 | 分类：办事/查询/升级 | 输出 intent_type |
| FR-SP-002 | 经营类一键升级 | P1 | 报价/合同/退款类升级 ΠPaw | 生成 Intent 单 + Evidence |
| FR-SP-003 | 个人 scope 执行 | P0 | 授权内 cs 调用 | 越权拒绝 |
| FR-SP-004 | 个人蜂群备忘录 | P1 | 五视角决策备忘录 | 可 PDF/JSON 导出 |
| FR-SP-005 | 代拟不代决 | P0 | generative 仅草稿，写库走 cs | 审计区分 suggest/execute |
| FR-SP-006 | 周报与汇总 | P2 | 周期性 rollup 到 ΠPaw | 含 SLA 异常条目 |
| FR-SP-007 | L2 分身代理 | P2 | 委托 DH-L2 代执行部分 cs | delegation_from 写入 actor |

---

### 3.7 ΠPaw 工作台与岗位工作室（DH-L2/L3）

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-PP-001 | 数字岗位编制 | P1 | 创建岗位 Agent：包+白名单+KPI | 对应 commercial 席位 |
| FR-PP-002 | 任务队列 | P0 | 接收升级 Intent、SLA Task | 可分配、可关闭 |
| FR-PP-003 | 岗位 cs 白名单 | P0 | 运行时强制校验 | 违反写审计 |
| FR-PP-004 | 跨部门编排 | P1 | DH-L2 调度多 cs 顺序/并行 | 编排图可审计 |
| FR-PP-005 | 经营向外看板 | P2 | 获转服续漏斗 | 对接 analytics cs |
| FR-PP-006 | 人工接管 | P0 | G6 人工决策写回 | 保留 full_reasoning_chain |
| FR-PP-007 | 对话+执行分离 UI | P1 | 左侧推理、右侧已执行 cs 时间线 | 与 audit_id 联动 |

---

### 3.8 对外网关（Outward Gateway）

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-GW-001 | 渠道接入 | P1 | 官网/微信/邮件入站 | 映射 tenant + 会话 |
| FR-GW-002 | 脱敏与限流 | P0 | 外部不可见内部主数据全文 | rate limit 可配置 |
| FR-GW-003 | 路由 DH-L3 Agent | P1 | 按渠道绑定销售/客服 Agent | 审计标 channel_id |
| FR-GW-004 | 人机转接 | P1 | 升级真人客服保留上下文 | Evidence 传递 |

---

### 3.9 审计与合规中心

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-AUD-001 | 全链路查询 | P0 | 按 audit_id / request_id / user | 含 cs 入参出参摘要 |
| FR-AUD-002 | 推理链存档 | P1 | LLM 输出作附件，非法律依据 | 与 deterministic 结果分离 |
| FR-AUD-003 | 合规报表 | P2 | 按月导出违规/升级统计 | 满足内审抽样 |
| FR-AUD-004 | 数据驻留证明 | P2 | 区域与存储位置报告 | 对接 FR-TEN-001 |

---

### 3.10 演化与 KPI 中心

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-EVO-001 | KPI 看板 | P1 | 岗位 Agent KPI 实时/离线 | 数据来自 cs.analytics |
| FR-EVO-002 | ChangeSet 提案 | P1 | 法则/话术/资格模型调整建议 | 需 P-GOV 审批 |
| FR-EVO-003 | 演化应用 | P1 | 批准后热更新 bundle | 对应 /evolveApply |
| FR-EVO-004 | A/B 话术 | P3 | 对外话术实验 | 归因到 channel |

---

### 3.11 运行时运维（Runtime Ops）

**基线**：复用 `scripts/run_uas_runtime_service.py`（见 EPS-03 TM-Runtime）。

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-RT-001 | Subapp 注册发现 | P0 | list/registry/health | 已有 |
| FR-RT-002 | 议题运行与队列 | P0 | run/enqueue/process | 已有 |
| FR-RT-003 | 认知状态查看 | P0 | state by topic | 已有 |
| FR-RT-004 | 企业租户注入 | P1 | run 时强制 tenant context | 无 tenant 拒绝 |
| FR-RT-005 | cs 调用轨迹 | P1 | run 结果含 cs_trace[] | 新增字段 |

---

### 3.12 包市场（Domain / 岗位 / 连接器）

| ID | 功能 | 优先级 | 描述 | 验收标准 |
|----|------|--------|------|----------|
| FR-MKT-001 | Domain 包安装 | P2 | Ontology + 默认 cs 集 | 一键导入 registry |
| FR-MKT-002 | 岗位包安装 | P2 | Agent 定义 + 白名单 | 绑定席位类型 |
| FR-MKT-003 | 连接器包安装 | P2 | 映射模板 + 凭证向导 | 通过 FR-GRID-002 测试 |

---

## 4. 非功能需求（NFR）

| ID | 类别 | 要求 |
|----|------|------|
| NFR-SEC-001 | 安全 | 凭证不落 Agent prompt；连接器密钥 HSM/密管 |
| NFR-SEC-002 | 安全 | 租户间数据默认 deny-all |
| NFR-AUD-001 | 审计 | P0 能力 audit_level=full，保留 ≥365 天（可配置） |
| NFR-AVL-001 | 可用 | CsRouter 核心路径 SLA 99.5%（商业托管） |
| NFR-PERF-001 | 性能 | cs 调用 P95 < 3s（不含 LLM）；LLM 异步化 |
| NFR-COMP-001 | 合规 | 支持 metadata_only 审计级别字段 |
| NFR-I18N-001 | 国际化 | 控制台与错误码中英双语 P2 |

---

## 5. 界面信息架构（IA）摘要

| 导航 | 模块 | 默认 Persona |
|------|------|--------------|
| 首页 | 经营漏斗 + 待办 Task | P-BIZ |
| 组织 | FR-TEN-* | P-ADM |
| 能力 | CS Studio | P-ADM, P-BIZ |
| 连接 | S-Grid | P-ADM, P-OPS |
| 合规 | 法则包 + 审计 | P-GOV |
| 我的助手 | SelfPaw | P-EMP |
| 数字岗位 | ΠPaw Studio | P-BIZ |
| 运维 | Runtime Ops | P-OPS |

---

## 6. 与商业 SKU 映射

| SKU | 包含 FR 范围 |
|-----|-------------|
| 租户基础版 | TEN-*, DP-001/003/004, AUD-001 |
| SelfPaw 席位 | SP-001～005 |
| ΠPaw 岗位席位 | PP-001～004, 007 |
| 连接器包 | GRID-* |
| 行业 Domain 包 | MKT-001 + 预置 CS 目录 |
| 合规增值包 | POL-*, AUD-*, G6 |

---

## 7. R0 最小可演示包（MVP Bundle）

**场景**：B2B 留资 → 资格判断 → 创建报价草案 → 提交审批  

| 模块 | 包含 FR |
|------|---------|
| CS Studio | CS-001, 002, 004, 006 |
| S-Grid | GRID-001, 002, 003 |
| ΠPaw | PP-002, 003, 007 |
| 审计 | AUD-001 |
| Runtime | RT-001～003, 005（规划） |

---

*下一文档：[ENTERPRISE_TECHNICAL_MODULE_SPEC.md](./ENTERPRISE_TECHNICAL_MODULE_SPEC.md)*
