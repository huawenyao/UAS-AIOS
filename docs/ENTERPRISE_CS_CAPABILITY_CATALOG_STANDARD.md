# 语义能力目录标准（EPS-05）

> **版本** 1.0 | **父标准**：[ENTERPRISE_PLATFORM_STANDARD.md](./ENTERPRISE_PLATFORM_STANDARD.md)

---

## 1. 能力卡片（Capability Card）

每个 `cs.<domain>.<verb>` 在目录中**必须**有一份能力卡片，作为产品、业务、研发、合规的共同语言。

### 1.1 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 全局唯一，如 `cs.quote.create` |
| `capability_version` | semver | 契约版本，破坏性变更升 major |
| `domain` | string | 业务域 |
| `verb` | string | 动作动词 |
| `business_definition` | string | ≤200 字，业务可读 |
| `execution_mode` | enum | deterministic \| assisted \| generative |
| `input_schema` | JSON Schema ref | 载荷结构 |
| `output_schema` | JSON Schema ref | 响应 data 结构 |
| `required_scopes` | string[] | 如 `quote:write` |
| `audit_level` | enum | full \| metadata_only |
| `implements_backend` | string[] | 内部 backend_id 列表 |
| `status` | enum | draft \| published \| deprecated |

### 1.2 条件必填

| 字段 | 何时必填 |
|------|----------|
| `policy_bundles` | execution_mode ≠ generative |
| `escalation_on_failure` | 涉及资金、合规、SLA |
| `kpi_attribution` | 经营闭环指标归因 |
| `sla` | 对外承诺类能力 |

### 1.3 能力卡片模板（YAML 人类编辑）

```yaml
id: cs.quote.create
capability_version: "2026.05.1"
domain: quote
verb: create
business_definition: 在信用与定价法则约束下创建报价草案，提交审批前不具法律效力
execution_mode: assisted
required_scopes:
  - quote:write
policy_bundles:
  - pricing_v4
  - credit_policy_v3
audit_level: full
implements_backend:
  - backend_crm
  - backend_erp
status: published
owner:
  product: 销售云
  engineering: platform-cs
change_log:
  - version: "2026.05.1"
    note: 初版，支持行项目折扣上限
```

机器可读汇总于 `enterprise_cs_capability_registry.json`。

---

## 2. 生命周期

```
draft → review → published → deprecated → retired
```

| 状态 | Agent 可见 | 说明 |
|------|------------|------|
| draft | 否（仅沙箱） | CS Studio 编辑中 |
| published | 是 | 生产可调用 |
| deprecated | 是（告警） | 建议迁移版本 |
| retired | 否 | 仅审计查询 |

**评审会（Capability Review）参与方**：P-BIZ（业务定义）、P-ADM（scope）、P-GOV（deterministic/红线）、P-OPS（连接器）。

---

## 3. 版本策略

| 变更类型 | 版本 bump | 示例 |
|----------|-----------|------|
| 新增可选字段 | patch | 加 optional note |
| 新增必填字段 | minor | 需客户端适配 |
| 删除/改名必填字段 | major | 旧版并行保留至 deprecated |

调用方在请求中指定 `capability_version`；未指定则使用租户「默认发布版」。

---

## 4. Domain 包与能力集

**Domain 包** = 一组能力卡片 + Ontology + 默认法则包引用。

| 包 ID | 包含 domain 示例 | 典型能力数 |
|-------|------------------|------------|
| `domain.b2b_sales` | lead, customer, quote, approval | 12–20 |
| `domain.recruitment` | job, candidate, interview | 10–15 |
| `domain.finance_shared` | invoice, payment | 6–10 |

安装 Domain 包 = 合并 registry + 安装 Ontology 到 K 层。

---

## 5. 岗位白名单绑定

岗位 Agent 通过 `allowed_capabilities` 或 `allowed_capabilities_prefix` 引用目录子集。

**规则**：

1. 白名单必须是 published 能力的子集  
2. `generative` 能力不得单独授予写库权限（须配对 deterministic 提交类）  
3. 跨域能力（如销售调 `cs.invoice.issue`）须 P-GOV 特批条目

---

## 6. 质量门禁（发布 checklist）

- [ ] business_definition 通过业务方签字（邮件/工单 ID 记入 owner）  
- [ ] input/output schema 契约测试绿  
- [ ] execution_mode 与 EPS-04 一致  
- [ ] 至少一个 backend 通过 FR-GRID-003 健康检查  
- [ ] 审计抽样：沙箱 invoke 产生 audit_id  
- [ ] 安全：无 schema 字段接受任意 HTML/脚本注入  

---

## 7. 目录服务 API（CS Studio 后端）

| 操作 | API |
|------|-----|
| 列表 | `GET /v1/tenants/{tid}/capabilities?domain=quote&status=published` |
| 详情 | `GET /v1/tenants/{tid}/capabilities/{id}/versions/{ver}` |
| 发布 | `POST /v1/tenants/{tid}/capabilities/{id}/publish` |
| 沙箱 | `POST /v1/tenants/{tid}/capabilities/{id}/sandbox-invoke` |

---

*注册表示例：`configs/enterprise_cs_capability_registry.example.json`*
