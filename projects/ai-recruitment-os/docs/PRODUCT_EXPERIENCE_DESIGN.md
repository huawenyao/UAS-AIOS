# AI Recruitment OS 产品原型与体验设计

## 核心价值

AI Recruitment OS 的用户可感知价值聚焦在三句话：

1. 更快找到对的人。
2. 更少招错人。
3. 用证据招对人。

产品不以“全自动招聘”为目标，而是让 HR、Hiring Manager、面试官和候选人都获得更清楚、更可信、更省心的招聘体验。

## 用户旅程

### 1. Hiring Mission

Hiring Manager 输入用人诉求后，系统不直接生成 JD，而是追问业务目标、成功周期、关键任务、团队约束和失败反例。输出物是岗位成功画像，而不是普通职位描述。

用户感知：我知道这次到底要招什么人。

### 2. Role Success Model

系统把岗位拆成关键任务、必备能力、加分能力、风险信号、面试证据和试用期成功标准。HR 与 Hiring Manager 共同确认后，后续筛选、面试和复盘都围绕它执行。

用户感知：我们不再用模糊 JD 筛人。

### 3. Evidence Shortlist

候选人导入后，系统生成证据卡和短名单。每个推荐都展示匹配证据、风险、缺失信息和下一轮要验证的问题。系统不自动淘汰候选人，所有高影响决策必须人工确认。

用户感知：我不用翻完所有简历，也知道谁最值得看，以及为什么。

### 4. Interview Workspace

面试官看到本轮要验证的能力、推荐问题、追问建议和评分标准。面试过程中，系统把回答归入证据维度，并提醒评分偏差或证据缺口。

用户感知：面试更专业，评分更有依据。

### 5. Calibration Room

系统汇总多位面试官的评分、证据和冲突点，生成候选人对比矩阵和决策简报。最终录用、拒绝、加面、Offer 都由人确认。

用户感知：我们基于证据做决定，而不是靠感觉争论。

### 6. Candidate Portal

候选人看到流程阶段、面试准备方向、时间安排和反馈说明。被拒绝时，候选人获得经过人工确认的体面反馈，而不是黑箱式静默。

用户感知：这个招聘过程清楚、及时、公平。

### 7. Learning Loop

招聘结束后，系统生成复盘：渠道质量、短名单质量、面试有效性、Offer 接受原因、Candidate NPS、Evidence coverage rate、试用期表现和留存信号。后验反馈用于更新岗位成功模型。

用户感知：这次招聘经验会让下一次更准。

## P0 功能

| 功能 | 主要用户 | 用户价值 |
|---|---|---|
| 用人需求澄清 | Hiring Manager | 把模糊需求转为清楚目标 |
| 岗位成功画像 | HR / Hiring Manager | 统一筛选和面试标准 |
| 候选人证据卡 | HR | 快速理解候选人为什么匹配 |
| 证据短名单 | HR | 减少初筛时间 |
| 结构化面试卡 | 面试官 | 提升面试质量和一致性 |
| 校准决策室 | Hiring Manager | 基于证据做录用决策 |
| 候选人门户 | 候选人 | 提升透明度和尊重感 |
| 招聘复盘 | TA Lead | 让招聘持续变准 |

## 明确不做

1. 不做无人确认的自动淘汰。
2. 不做完全替代面试官的 AI 面试。
3. 不做 HRIS 或 ATS 的全量替代。
4. 不做黑箱分数排序。
5. 不在 V1 支持所有行业，先聚焦技术、销售或运营岗位中的一个标杆场景。

## Agent 体系

Agent 体系使用 UAS-AIOS 的 Business AGI 思路：多个岗位 Agent 围绕同一个招聘世界模型协作，所有 Agent 只能调用 `cs.*` 能力服务。

核心 Agent：

1. 招聘意图守恒 Agent：保持业务目标和岗位成功画像一致。
2. 候选人证据 Agent：把简历和资料转成可追溯证据。
3. 短名单推荐 Agent：生成可复核短名单。
4. 结构化面试 Agent：生成问题、追问、评分卡并捕获证据。
5. 校准决策 Agent：识别评分冲突并生成决策简报。
6. 候选人体验 Agent：提供进度、准备提示和反馈文案。
7. 公平合规 Agent：检查偏差、权限和高风险自动化行为。
8. 招聘后验演化 Agent：把入职后信号回流到世界模型。

机器可读配置见 `projects/ai-recruitment-os/configs/agent_system_design.json`。

## 关键体验原则

1. 先解释，再建议。
2. 人做决策，AI 做增强。
3. 每个推荐都有证据，每个风险都可追溯。
4. 候选人体验是核心产品价值，不是附属通知。
5. 招聘质量优先于自动化程度。

## 成功指标

北极星指标：

```text
Quality-adjusted hiring success rate
```

输入指标：

- Time to qualified shortlist
- Hiring manager shortlist acceptance
- Evidence coverage rate
- Candidate NPS
- Interviewer score conflict rate
- Offer acceptance rate
- 90-day success rate

P0 验收建议：

- HR 初筛时间下降 60%。
- Hiring Manager 对短名单满意度大于 80%。
- Evidence coverage rate 大于 85%。
- Candidate NPS 大于 50。
- 面试官评分冲突率下降 30%。
