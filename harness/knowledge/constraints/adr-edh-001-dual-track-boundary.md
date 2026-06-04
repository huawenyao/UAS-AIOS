# ADR-EDH-001：SelfPaw 与 ΠPaw 双轨边界

## Status

Accepted · 2026-05-23

## Context

企业级数字人生态需同时服务 **员工（对内）** 与 **经营（对外）**。SelfPaw 与 ΠPaw 共享 UAS Kernel，但产品边界易混淆导致重复建设或权限失控。

## Decision

1. **SelfPaw 企业版** = 组织内员工数字分身；数据 scope = 个人授权 ∪ 岗位授权。  
2. **ΠPaw** = 组织经营数字岗位体系；数据 scope = 角色分级组织数据。  
3. **升级路径**：经营类 Intent 必须由 SelfPaw **带 Evidence** 提交 ΠPaw Working Task，禁止静默越权。  
4. **共享**：Kernel、cs.*、审计、ChangeSet；**不共享**：对外通道默认仅 ΠPaw。  
5. **C 端个人版** Phase-0 不交付，仅保留架构复用。

## Consequences

- 需定义 `intent_escalation` 跨产品契约  
- Console 需区分员工视图与指挥席视图  
- 合规审计按产品轨道分表存储  

## 数据 Scope 实现（PL-001/002 对齐）

| 轨道 | `product_track` | 默认 scope | RBAC 角色示例 |
|------|-----------------|------------|---------------|
| SelfPaw | `selfpaw` | self, dept, dept_tree | role.employee, role.sales_rep |
| ΠPaw | `pipaw` | tenant（策略细分） | role.cs_agent, role.cs_lead |

- 配置：`configs/tenant_catalog.sample.json` + `configs/enterprise_rbac_template.json`  
- 规格：`harness/knowledge/technical/enterprise-rbac-abac-spec.md`  
- 跨租户拒绝：`scripts/validate_enterprise_policy.py` 用例 1–4  
