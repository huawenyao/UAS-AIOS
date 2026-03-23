# AI招聘世界模型

## 世界模型

AI 招聘系统将“岗位、候选人、任务、事件、通知、评价”统一为可计算对象，驱动端到端自动化招聘流程。

核心目标：从简历初筛到面试评价形成可验证、可追踪、可学习的场景闭环。

## 实体模型

- **Job**：岗位画像（能力矩阵、业务情境、约束与指标）
- **Candidate**：候选人结构化信息与评分
- **Task**：任务级执行单元（screening / ai_interview / human_interview）
- **Event**：业务与系统事件（用于驱动状态流转）
- **Notification**：基于事件触发的角色通知
- **Evaluation**：面试或综合评价输出

## 事件模型

关键事件链：

1. `screening_completed`
2. `candidate_shortlisted`
3. `ai_interview_scheduled`
4. `ai_interview_completed`
5. `human_interview_completed`
6. `evaluation_updated`

事件驱动策略：任务完成即发布事件，事件触发通知与评价记录，保证流程可审计。

## 招聘场景闭环

闭环阶段遵循：

1. **Sense**：识别岗位意图与候选人信号
2. **Model**：构建人岗匹配与风险模型
3. **Decide**：给出推荐/待定/淘汰决策
4. **Act**：推进筛选、面试、通知动作
5. **Verify**：通过规则与结果验证质量
6. **Learn**：沉淀策略与经验，反哺下一轮招聘

该闭环支持 AI 招聘的领域化自治运行：流程可执行、结果可解释、策略可持续优化。
