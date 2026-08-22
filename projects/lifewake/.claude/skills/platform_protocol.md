# UAS Sub App 执行协议

## 标准阶段

每个 sub uas app 必须至少包含以下阶段：

1. `intent_activation`：明确业务目标、约束、成功标准
2. `knowledge_binding`：把目标绑定到知识资产和业务规则
3. `agent_planning`：生成 agent 分工与协作计划
4. `system_mapping`：映射系统接口、数据、工具和流程
5. `governance_check`：执行风险、权限、偏差与治理校验
6. `evolution_plan`：形成下一轮迭代策略

## 禁忌

- 不允许缺少目标守恒策略
- 不允许缺少审计治理配置
- 不允许缺少演化回路
- 不允许把业务子应用做成纯文档、不可运行的空壳
