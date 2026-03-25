## 面向 HR 的 AI 招聘工作台 - 全流程业务用例

### 1. 总览

- **角色**：HR 招聘负责人（如「小李」）、用人部门 Leader、候选人  
- **AI 形态**：嵌入式「AI 招聘工作台」，由多 Agent 协同完成从岗位画像 → 简历管理 → 人才画像 → 人岗匹配 → 面试邀约 → AI 预面试/联合面试 → 录用决策与闭环演化的全流程。  
- **设计约束**：关键环节 AI 输出必须是**结构化、量化、可追溯**的判断，且决策逻辑符合「认知实践」的广度与深度（多维度 × 有证据的推理链 × 可被实践反馈修正）。

---

### 2. 场景一：岗位画像管理（从 JD 文本到岗位认知模型）

**触发**：用人 Leader 提出一句话需求（如「要一个懂 AIGC 的市场运营」）。  

**AI 辅助流程**：

1. **需求澄清对话**  
   - AI 将自然语言需求拆解为结构化问卷（业务目标、关键任务、能力要求、协作对象、业务阶段、关键 KPI 等）。  
   - 通过在线问卷或对话方式完成澄清，并沉淀为岗位配置数据。

2. **自动构建岗位画像模型**  
   - 生成多维岗位画像：  
     - 业务维度：产品线、业务阶段、关键 KPI；  
     - 能力维度：必备/加分能力标签、权重、熟练度要求；  
     - 经验维度：行业/项目/团队规模要求；  
     - 行为/风格维度：执行/策略/创新/协同偏好。  
   - 同时生成对内的「标准岗位画像结构（Job.parsed_profile）」与对外使用的 JD 文案。

3. **画像版本与稀缺度分析**  
   - 管理岗位画像版本（V1 口头描述、V2 AI 首版、V3 调整版）。  
   - 输出岗位复杂度评分、市场稀缺度评分、与历史岗位相似度等量化指标。

**关键结构化输出（映射到 Job 实体）**：

- `parsed_profile.capability_matrix`：能力项数组（名称、重要性权重、要求熟练度）。  
- `parsed_profile.context`：业务阶段、关键 KPI、团队结构。  
- `parsed_profile.metrics`：`job_complexity_score`、`market_scarcity_score`、`internal_similarity_score` 等。

---

### 3. 场景二：简历管理（多源简历 → 统一知识底座）

**触发**：岗位发布后，从多个渠道获取到大量候选人简历。  

**AI 辅助流程**：

1. **多源收集与解析**  
   - 从邮箱、ATS、招聘网站、内推表格等自动拉取简历。  
   - 将简历解析为统一结构字段：教育、工作/项目经历、技能标签、作品链接等。

2. **去重与关系识别**  
   - 基于姓名、联系方式、账号指纹识别重复候选人与历史投递记录。  
   - 关联过往面试记录、结果与人才池标签。

3. **标签与风险提示**  
   - 自动打上技能标签、经验类型标签、稳定性标签等。  
   - 标记潜在风险项（频繁跳槽、履历断层、描述与事实疑似不一致等）。

**关键结构化输出（映射到 Candidate.basic_info 等）**：

- `basic_info.education[]`、`basic_info.experiences[]`、`basic_info.projects[]`  
- `basic_info.skills[]`（技能 + 证据片段引用）  
- `scores.stability_score`、`scores.result_quantification_score`、`scores.years_in_relevant_roles`  
- `risk_flags[]`：如「频繁跳槽」「长期空档」等。

---

### 4. 场景三：人才画像（从“简历”到“人”的多维建模）

**触发**：HR 希望长期运营某类核心人才（如「增长型运营人才」）的人才池。  

**AI 辅助流程**：

1. **单人画像构建**  
   - 基于简历、作品、历史对话/面试等，生成「一页纸人才画像卡」。  
   - 维度包括：核心能力谱系、职业轨迹、行为特征推断、潜力与风险等。

2. **人才聚类与分层**  
   - 将候选人聚类为不同人才簇（如策略型、内容创意型、数据驱动型等）。  
   - 为每个簇给出典型画像与适配岗位类型、薪资建议。

3. **动态演化**  
   - 新的面试/试用反馈持续回写到人才画像，更新各维度评分与标签。  
   - 人才画像成为跨岗位复用的长期资产。

**关键结构化输出（映射到 Candidate.scores / evidence 等）**：

- 能力向量：`scores.abilities.{ability_name}`（0–100）  
- 潜力与学习能力：`scores.potential_score`、`scores.self_driven_score`、`scores.cross_domain_score`  
- 行为与价值观倾向：`scores.outcome_oriented_index`、`scores.collaboration_index`、`scores.risk_preference_index`  
- 每个分数对应 `evidence[]` 中的证据 ID 与 `evidence_details`（来源、片段、解释）。

---

### 5. 场景四：人才匹配（岗位画像 × 人才画像）

**触发**：岗位画像确定后，需要从海量候选人中筛出优先沟通名单。  

**AI 辅助流程**：

1. **多维匹配评分**  
   - 基于 Job.parsed_profile 与 Candidate.scores，计算：  
     - 能力匹配分、业务情境匹配分、文化/团队 fit 分、成长空间指数等。  
   - 输出可视化雷达图与结构化字段。

2. **可调策略与排序**  
   - HR 可以调整权重（如更看重即战力或潜力），AI 重新计算综合匹配分。  

3. **可解释推荐**  
   - 给出推荐等级（强烈推荐/推荐/边界/不推荐）。  
   - 附上匹配/不匹配的关键理由与证据链。

**关键结构化输出（映射到 Candidate.scores / decision 等）**：

- `scores.matching.ability_match_score`  
- `scores.matching.context_match_score`  
- `scores.matching.culture_fit_score`  
- `scores.matching.growth_potential_score`  
- `scores.matching.overall_match_score`  
- `decision`：`strong_recommend | recommend | borderline | not_recommend`  
- `evidence[]`：关键理由与证据引用。

---

### 6. 场景五：面试邀约与意向度量化

**触发**：根据匹配结果对 TopN 候选人发起沟通与面试邀约。  

**AI 辅助流程**：

1. **邀约策略生成**  
   - 针对不同候选人的画像，生成个性化的邀约渠道与话术。  

2. **批量发送与跟踪**  
   - 批量发送多渠道邀约，同时跟踪打开、回复、点击行为。  

3. **候选人意向度评估**  
   - 根据互动行为与内容，量化候选人意向度与沟通质量。

**关键结构化输出（可映射到 Candidate.scores / Notification 扩展字段）**：

- `scores.intent.intent_score`（0–100）  
- `scores.intent.communication_clarity_score`（0–100）  
- `scores.intent.motivation_fit_score`（0–100）  
- `risk_flags[]` 中增加「薪资期望明显超出区间」等提示。

---

### 7. 场景六：AI 预面试与联合面试（多维量化评估）

**触发**：候选人同意沟通，但 HR/面试官时间有限。  

**AI 辅助流程**：

1. **AI 预面试**  
   - 围绕关键项目、问题解决过程、复盘能力、动机与期望等发起结构化问答。  
   - 对每个项目生成「目标-行动-结果-复盘」四元组，并评分。

2. **生成预面试报告**  
   - 输出项目掌控程度、结果导向度、问题解决复杂度、逻辑思维、合作意识等量化维度。  
   - 为人工面试生成「必须追问问题」清单。

3. **人机联合面试**  
   - 在视频/现场面试中，AI 做记录与提醒：追问不一致点、补齐未覆盖维度。  
   - 会后生成结构化面试纪要与评估维度得分。

**关键结构化输出（映射到 Evaluation.dimensions、summary 等）**：

- `dimensions.professional_skill_score`  
- `dimensions.problem_solving_score`  
- `dimensions.communication_score`  
- `dimensions.thinking_logic_score`  
- `dimensions.culture_fit_score`  
- `dimensions.potential_score`  
- `summary`：结构化自然语言总结与推荐意见。

---

### 8. 场景七：录用决策与闭环演化

**触发**：在多名终面候选人之间做录用选择，并沉淀为长期人才资产。  

**AI 辅助流程**：

1. **多候选人对比视图**  
   - 汇总各候选人在各维度（能力、潜力、文化、风险、薪资期望等）的评分。  
   - 暴露不同面试官间的评分分歧与评价冲突点。

2. **决策建议与 Offer 策略**  
   - 生成录用建议（录用/待定/不录用），并给出主客观依据。  
   - 基于市场与人才画像，给出薪酬与激励结构建议。  

3. **实践反馈与模型更新**  
   - 入职后跟踪试用期 KPI、主管满意度、协作评价等真实表现。  
   - 对比当时的匹配评分与实际结果，自动生成模型回顾，提示哪些维度/权重需要调整。

**关键结构化输出（可扩展到 Evaluation / Candidate / 新增 Feedback 实体）**：

- 试用期表现：`post_hire.probation_kpi_completion`、`post_hire.manager_satisfaction_score`、`post_hire.team_collaboration_score`  
- 结果标签：`post_hire.outcome`（如「成功转正」「试用期内离职」等），用于反哺模型。  

---

### 9. 认知实践视角下的设计约束小结

- **广度**：  
  - 对岗位：通过 `Job.parsed_profile` 中的能力矩阵、业务情境、约束等多维建模。  
  - 对人才：通过 `Candidate.scores` 下的能力、潜力、行为、意向、匹配等多维度建模。  
  - 对流程：通过 `Task`、`Event`、`Notification`、`Evaluation` 串联起从输入到输出的完整工作流。

- **深度**：  
  - 所有分数/标签必须绑定到 `evidence` 与 `Evaluation.dimensions` 的证据与推理说明，可审计可追问。  
  - 模型需要接入真实结果反馈（入职后表现），周期性更新权重与特征抽取逻辑。

- **工程落地建议**：  
  - 在 `configs/entity_schemas.json` 中为 Job、Candidate、Evaluation 等增加上述结构化字段（或嵌套对象），并在评估逻辑中统一写入。  
  - 配合 `docs/entity_event_model.md`，保证数据模型与事件驱动闭环一致，为后续演化（E）留足空间。

