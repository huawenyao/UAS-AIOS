# Enterprise Sales OS MVP 开发规约包

> 本目录把 [UAS-AIOS 企业级产品蓝图](../UAS_AIOS_ENTERPRISE_PRODUCT_BLUEPRINT.md) 中的 B2B 线索到报价审批 MVP 收敛为可开发规约。目标是让 `projects/enterprise-sales-os/` 能以单个 UAS subapp 原型进入开发，而不是提前拆成微服务平台。

---

## 1. v0.2 开发边界

| 项 | 决策 |
|----|------|
| 工程形态 | 单个 `projects/enterprise-sales-os/` subapp |
| 运行方式 | 复用现有 `scripts/run_uas_runtime_service.py` 与 autonomous_agent runtime |
| 系统集成 | 使用 mock connector / script gateway，不接真实 CRM/ERP |
| SelfPaw | 暂以结构化 `actor + scope + evidence` payload 模拟 SelfPaw 升级，不建设平台级 U 层 |
| ΠPaw | 实现 Sales Advisor、Compliance Reviewer、Finance Reviewer 三类岗位 Agent |
| 演化 | 生成 ChangeSet 草案，不自动写回生产配置 |
| UI | 暂不建设正式 UI，以 JSON 输入、reports 输出、audit/state 文件验证闭环 |

---

## 2. MVP 闭环

```text
lead_created / sales_manual_input
  → Intent Hub: 标准化意图单
  → Evidence Board: 证据校验与补证据判断
  → ΠPaw Sales Advisor: 线索资格判断
  → cs.lead.qualify
  → cs.quote.draft
  → Policy Engine: G0-G4 + 金额/折扣/客户等级
  → cs.approval.start
  → ΠPaw Compliance / Finance Reviewer
  → quote_approval_task + audit_report + kpi_summary
  → feedback + ChangeSet draft
```

---

## 3. 规约文件

| 文件 | 解决的问题 |
|------|------------|
| [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) | 明确 Lead、Account、Quote、Approval、Evidence、Task、AuditEvent、KPIEvent、ChangeSet 字段、生命周期与事件 |
| [CAPABILITY_CONTRACTS.md](./CAPABILITY_CONTRACTS.md) | 定义 P0 `cs.*` 能力服务的输入、输出、错误、权限、幂等和回滚 |
| [GOVERNANCE_MATRIX.md](./GOVERNANCE_MATRIX.md) | 把 G0-G4、金额、折扣、客户等级、审批人规则变成可执行策略 |
| [WORKFLOW_STATE_MACHINE.md](./WORKFLOW_STATE_MACHINE.md) | 定义任务、审批、补证据、失败、回滚和人工接管状态机 |
| [WORLD_MODEL_CONFIG.md](./WORLD_MODEL_CONFIG.md) | 为世界模型五维、主客体、反馈通道和推动/阻碍/连接提供配置占位 |
| [FEEDBACK_CHANGESET.md](./FEEDBACK_CHANGESET.md) | 定义人工反馈、KPI 归因、ChangeSet 草案和受控回写流程 |
| [MVP_ACCEPTANCE_CASES.md](./MVP_ACCEPTANCE_CASES.md) | 提供端到端验收用例，覆盖成功、拒绝、证据不足、能力失败和治理拦截 |

---

## 4. 开发完成定义

v0.2 配置原型完成时必须满足：

1. `enterprise-sales-os` 能被 UAS Runtime Service 发现和 validate。
2. 至少 5 条验收用例可通过脚本或 runtime 执行。
3. 每次运行都生成 intent、evidence、capability_call、approval、audit、report。
4. 高风险报价必须进入审批，不允许自动对外承诺。
5. 失败用例必须产出明确错误码、审计记录和下一步建议。
6. 至少一条反馈能生成 ChangeSet 草案。
