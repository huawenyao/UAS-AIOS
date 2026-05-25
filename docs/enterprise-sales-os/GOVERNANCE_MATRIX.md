# Enterprise Sales OS 治理矩阵

> 本文把 G0-G4 风险等级、报价金额、折扣、客户等级、信用状态和审批角色落为可执行策略。v0.2 开发时应先用静态 JSON 配置实现，后续再迁移到策略服务。

---

## 1. 风险等级

| 等级 | 含义 | 示例动作 | 默认控制 |
|------|------|----------|----------|
| **G0** | 只读或审计追加 | 查询线索、追加审计 | scope 校验 + audit |
| **G1** | 草稿生成 | 邮件草稿、报价草案说明 | 人工发送，禁止外部承诺 |
| **G2** | 授权内低风险执行 | 线索资格判断、创建内部任务 | 自动执行 + 可回滚 |
| **G3** | 经营承诺前置动作 | 超阈值折扣、较大金额报价 | 销售经理审批 |
| **G4** | 财务/合规影响动作 | 高折扣、高金额、信用例外、法务风险 | 财务/合规联合审批 |

MVP 不实现 G5/G6 自动化；任何疑似 G5/G6 均返回 `HUMAN_REVIEW_REQUIRED` 或 `BUSINESS_RULE_BLOCKED`。

---

## 2. 角色与权限

| 角色 | 数据 scope | 动作 scope |
|------|------------|------------|
| `sales_rep` | `crm.leads.assigned`、`crm.accounts.assigned` | `cs.lead.qualify`、`cs.quote.draft` |
| `sales_manager` | `crm.leads.team`、`crm.accounts.team`、`quotes.team` | sales_rep 全部 + `cs.approval.decide.sales` |
| `finance_reviewer` | `quotes.pending_finance`、`accounts.credit` | `cs.approval.decide.finance` |
| `compliance_reviewer` | `quotes.pending_compliance`、`contracts.policy` | `cs.approval.decide.compliance` |
| `ppaw_sales_advisor` | 继承 `on_behalf_of` 的销售数据 scope | `cs.lead.qualify`、`cs.quote.draft`、`cs.audit.append` |
| `ppaw_compliance_reviewer` | `quotes.pending_compliance` | `cs.audit.append`、生成合规意见 |
| `ppaw_finance_reviewer` | `quotes.pending_finance`、`accounts.credit` | `cs.audit.append`、生成财务意见 |

---

## 3. 报价治理规则

### 3.1 金额与折扣

| 条件 | 风险 | 审批要求 |
|------|------|----------|
| `net_amount < 100000` 且 `discount_rate <= 0.10` | G2 | 无审批，仅内部草案 |
| `net_amount < 100000` 且 `0.10 < discount_rate <= 0.15` | G3 | `sales_manager` |
| `100000 <= net_amount < 500000` 或 `0.15 < discount_rate <= 0.25` | G3 | `sales_manager` |
| `net_amount >= 500000` 或 `discount_rate > 0.25` | G4 | `sales_manager` + `finance_reviewer` |
| `discount_rate > 0.40` | G4 | 默认拒绝，除非 `strategic` 客户且人工豁免 |

### 3.2 客户等级

| 客户等级 | 默认控制 |
|----------|----------|
| `smb` | 走标准金额/折扣规则 |
| `mid_market` | 走标准金额/折扣规则 |
| `enterprise` | 金额阈值不变，必须补充需求证据 |
| `strategic` | 允许申请超阈值豁免，但必须 G4 |

### 3.3 信用状态

| 信用 | 控制 |
|------|------|
| `A` | 标准规则 |
| `B` | 账期超过 `net_30` 进入 G3 |
| `C` | 任意报价进入 G4 finance |
| `blocked` | `BUSINESS_RULE_BLOCKED`，不得生成可审批报价 |

---

## 4. 证据要求

| 动作 | 必需证据 |
|------|----------|
| `cs.lead.qualify` | 至少 1 条客户需求证据 |
| `cs.quote.draft` | 需求证据 + 产品/服务项 |
| G3 折扣审批 | 折扣理由 + 竞争/预算/战略价值任一证据 |
| G4 金额审批 | 需求证据 + 折扣理由 + 付款条件 + 客户等级 |
| 信用例外 | 财务说明 + 人工备注 |

证据不足时必须返回 `EVIDENCE_REQUIRED`，创建 `collect_evidence` 任务，不得继续推进审批。

---

## 5. 策略判定顺序

```text
1. actor scope check
2. capability scope check
3. input schema validation
4. evidence requirement check
5. customer credit check
6. amount / discount risk classification
7. approval role resolution
8. audit append
```

任何一步失败，都必须写入审计事件。

---

## 6. 可执行配置草案

```json
{
  "risk_levels": ["G0", "G1", "G2", "G3", "G4"],
  "quote_policy": {
    "auto_draft": {
      "max_net_amount": 100000,
      "max_discount_rate": 0.10,
      "risk_level": "G2"
    },
    "sales_manager_approval": {
      "max_net_amount": 500000,
      "max_discount_rate": 0.25,
      "risk_level": "G3",
      "required_roles": ["sales_manager"]
    },
    "finance_approval": {
      "min_net_amount": 500000,
      "min_discount_rate": 0.25,
      "risk_level": "G4",
      "required_roles": ["sales_manager", "finance_reviewer"]
    },
    "hard_block": {
      "max_discount_rate": 0.40,
      "credit_blocked": true
    }
  }
}
```

---

## 7. 治理验收

| 用例 | 期望 |
|------|------|
| 普通报价，8% 折扣，金额 8 万 | G2，无审批 |
| 18% 折扣，金额 8 万 | G3，销售经理审批 |
| 12% 折扣，金额 60 万 | G4，销售经理 + 财务审批 |
| 信用 blocked 客户 | 拦截，不生成报价 |
| 缺需求证据 | 补证据任务 |
| Agent 尝试发送客户报价 | 拦截，返回 `HUMAN_REVIEW_REQUIRED` |
