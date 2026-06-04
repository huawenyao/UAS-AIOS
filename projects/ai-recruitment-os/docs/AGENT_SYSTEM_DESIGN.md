# AI Recruitment OS Agent 体系设计

## 设计原则

AI Recruitment OS 的 Agent 体系遵循 UAS-AIOS 八元组：

```text
I: 招聘意图与岗位成功目标
K: 岗位、候选人、面试、合规知识
R: autonomous_agent runtime
A: 招聘 Agent Fabric
S: ATS / HRIS / 日历 / 邮件 / 题库 / BI 系统网格
G: 权限、审计、公平、人工确认
E: 入职后反馈与招聘模型演化
Π: cs.* 能力服务协议
```

核心约束：

1. Agent 只能调用 `cs.*` 能力服务。
2. 高影响决策必须人工确认。
3. 推荐、拒绝、录用、Offer 都必须有证据链。
4. 后验反馈只能生成模型更新提案，不能自动覆盖生产规则。

## Agent Fabric

| Agent | 服务对象 | 核心产出 |
|---|---|---|
| 招聘意图守恒 Agent | Hiring Manager | 岗位成功画像 |
| 候选人证据 Agent | HR | 候选人证据卡 |
| 短名单推荐 Agent | HR | 可复核短名单 |
| 结构化面试 Agent | 面试官 | 面试卡、证据纪要、评分建议 |
| 校准决策 Agent | Hiring Manager | 候选人对比、决策简报 |
| 候选人体验 Agent | 候选人 | 流程通知、准备提示、反馈文案 |
| 公平合规 Agent | Compliance Owner | 偏差审查、高风险拦截 |
| 招聘后验演化 Agent | TA Lead | 模型更新提案、复盘报告 |

## 能力服务边界

能力服务定义见 `configs/agent_system_design.json`。关键服务包括：

- `cs.role.create_success_model`
- `cs.candidate.build_evidence_card`
- `cs.candidate.rank_shortlist`
- `cs.interview.generate_scorecard`
- `cs.interview.capture_evidence`
- `cs.decision.compare_candidates`
- `cs.audit.run_fairness_review`
- `cs.feedback.update_recruitment_world_model`

## 运行链路

```text
Hiring Mission
  -> Role Success Model
  -> Evidence Shortlist
  -> Interview Workspace
  -> Calibration Room
  -> Candidate Portal
  -> Learning Loop
```

每个阶段都写入审计链：

```text
actor -> input -> agent -> capability -> output -> reviewer -> decision -> timestamp
```

## 治理门禁

| 门禁 | 触发条件 | 系统行为 |
|---|---|---|
| G1 目标守恒 | 岗位目标缺失或频繁变更 | 阻止进入短名单 |
| G2 证据不足 | 推荐或拒绝缺少证据 | 要求补充信息 |
| G3 偏差风险 | 筛选或评分存在群体偏差 | 触发公平审查 |
| G4 高影响决策 | 拒绝、录用、Offer | 要求人类确认 |
| G5 数据越权 | Agent 请求超出权限数据 | 拦截并写审计 |
| G6 反馈污染 | 后验数据不足以更新模型 | 只生成观察报告 |
| G7 规则演化 | 修改岗位或评分规则 | 需要 TA Lead 审批 |

## 原型入口

静态产品原型位于：

```text
projects/ai-recruitment-os/prototype/index.html
```
