# UAS 招聘 Sub App 方案：测试招聘流程

## 意图模型
- 围绕“测试招聘流程”生成的业务意图与成功标准

## 知识资产
- .claude/skills/output_contract.md
- .claude/skills/platform_protocol.md
- .claude/skills/recruitment_os_protocol.md
- .claude/skills/recruitment_output_contract.md
- CLAUDE.md
- configs/business_loop_config.json
- configs/evolution_policy.json
- configs/governance_policy.json
- configs/platform_manifest.json
- configs/runtime_config.json
- configs/swarm_agents.json
- configs/system_registry.json
- configs/workflow_config.json

## 运行时拓扑
- runtime=autonomous_agent_runtime
- context_injection=True
- state_isolation=task_level

## Agent编织
- 意图守恒智能体
- 知识架构智能体
- Agent编织智能体
- 运行时智能体
- 系统网格智能体
- 治理审计智能体
- 进化规划智能体
- 用人部门智能体
- HR运营智能体
- 候选人体验智能体
- 公平合规智能体
- 宏观理念智能体
- 宏观现实智能体
- 中观理念智能体
- 中观现实智能体
- 微观理念智能体
- 微观现实智能体

## 系统网格
- ats:recruitment_tracking
- resume_source:candidate_source
- calendar:interview_scheduling
- hris:onboarding_feedback
- knowledge_base:asui_knowledge

## 治理控制
- audit
- approval
- rollback

## 评估指标
- candidate_experience_score>=0.75
- decision_explainability_score>=0.8
- interviewer_alignment_score>=0.7
- process_completion_score>=0.85

## 演化回路
- intent_activation
- governance_check
- evolution_plan

## 交付计划
- Phase 1：方案与骨架
- Phase 2：MVP
- Phase 3：闭环增强
- Phase 4：演化开发
