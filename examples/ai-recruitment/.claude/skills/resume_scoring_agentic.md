# 简历评分（CLAUDE CODE AGENTIC Skill）

> 目标：让 Claude Code / Cloud Agent 在 AI 招聘场景中，针对指定岗位画像，**稳定、可审计、可演化** 地为候选人简历打分，并输出结构化结果，供后续脚本生成报告。

---

## 一、输入与前置条件

### 1.1 上下文前提

- 已存在**岗位画像**（Job Profile），可来自：
  - `workflow_config.parse_jd` 的输出，或
  - 预先存在的结构化配置（如 `jobs.json` 中某个 `job_id`）
- 当前会话中可获得：
  - `job_profile`：岗位画像 JSON
  - `resume_text`：候选人完整简历原文（UTF-8 文本）

### 1.2 你在这个 Skill 中的角色

- 不是“聊天机器人”，而是 **评分引擎**：
  - 必须遵守本 Skill 中定义的**字段、范围、权重和输出 JSON Schema**
  - 必须为每个关键得分给出 **证据链（evidence）**
  - 输出用于后续脚本 / 系统消费，而不是给人类看的「漂亮文案」

---

## 二、评分维度与权重（与 `evaluation_criteria.md` 对齐）

### 2.1 基础维度（0–10 分）

#### 2.1.1 学历匹配度 `education_score`

- 依据：
  - 岗位画像中的最低学历要求（如：本科/硕士/博士）
  - 候选人最高学历、专业相关性、院校层次（如有明显信息）
- 打分建议（可调整但要解释）：
  - 明显低于要求：0–3
  - 刚好满足：6–8
  - 明显超过（重点专业/院校 + 强相关）：8–10

#### 2.1.2 经验匹配度 `experience_score`

- 依据：
  - 岗位要求的总经验年限 / 关键领域经验
  - 简历中真实体现的相关经验（按项目和岗位描述判断）
- 打分建议：
  - 经验证明显不足：0–3
  - 接近要求（差 1 年左右）：4–6
  - 精准匹配或略超出：7–9
  - 远超要求且高度相关：9–10

#### 2.1.3 技能匹配度 `skill_score`

- 依据：
  - 岗位 `must_have.skills` / `nice_to_have.skills` 中的关键词
  - 候选人在项目经历中对这些技能的使用深度与频率
- 打分建议：
  - 必备技能缺失：0–3
  - 必备技能基本覆盖，部分有实践：6–8
  - 必备 + 加分技能均有且有深度项目实践：8–10

#### 2.1.4 工程实践 `engineering_score`（如无信息可置 0–5）

- 依据：
  - 是否提到：测试（单测/集成）、CI/CD、Code Review、文档、规范化流程
  - 是否参与过性能优化、故障处理、稳定性建设

#### 2.1.5 领域经验 `domain_score`

- 依据：
  - 岗位画像中的目标业务领域（如：电商、金融、SaaS）
  - 候选人过往项目的行业上下文

#### 2.1.6 成长潜力 `potential_score`

- 依据：
  - 学习轨迹（自学项目、跨领域迁移、快速晋升等）
  - 承担责任（是否担任 owner / 负责关键模块）
  - 面对复杂问题的解决记录

### 2.2 风险与证据信号

- `risk_flags`：字符串数组，记录潜在风险或需要面试重点确认的点，例如：
  - `"frequent_job_hops"`（频繁跳槽）
  - `"cv_gaps"`（简历空档期较长）
  - `"vague_responsibilities"`（职责描述模糊）
- `evidence`：字符串数组，引用简历中的关键原句/片段，说明评分依据。

### 2.3 综合评分 `total_score`

- 采用加权方式计算总分（0–10）：

  - 默认权重（可按岗位画像覆盖）：
    - `education`: 0.10
    - `experience`: 0.25
    - `skill`: 0.35
    - `engineering`: 0.10
    - `domain`: 0.10
    - `potential`: 0.10

- 计算公式（伪代码）：

```text
total_score =
  education_score  * weights.education  +
  experience_score * weights.experience +
  skill_score      * weights.skill      +
  engineering_score* weights.engineering+
  domain_score     * weights.domain     +
  potential_score  * weights.potential
```

> 注意：如果岗位画像中提供了自定义权重，必须优先使用岗位画像中的权重。

---

## 三、输出 Schema（必须严格遵守）

最终输出必须是一个 **单一 JSON 对象**，不要包含额外说明文字，也不要在 JSON 外输出任何字符（包括注释、自然语言解释等）。字段如下：

```json
{
  "candidate_id": "string",
  "job_id": "string",
  "scores": {
    "education_score": 0,
    "experience_score": 0,
    "skill_score": 0,
    "engineering_score": 0,
    "domain_score": 0,
    "potential_score": 0,
    "total_score": 0
  },
  "decision": "strong_recommend | recommend | borderline | not_recommend",
  "risk_flags": ["string"],
  "evidence": [
    "简要说明学历评分依据 + 简历原文片段",
    "简要说明经验评分依据 + 简历原文片段",
    "简要说明技能评分依据 + 简历原文片段",
    "如有风险或潜力评估，也要给出对应证据"
  ]
}
```

### 3.1 决策建议规则

- `total_score >= 8.5` → `"strong_recommend"`
- `7.0 <= total_score < 8.5` → `"recommend"`
- `5.0 <= total_score < 7.0` → `"borderline"`
- `total_score < 5.0` → `"not_recommend"`

如果存在严重 `risk_flags`，可以在高分情况下仍然给出 `"borderline"` 或 `"recommend"`，并在 `evidence` 中明确说明原因。

---

## 四、Agentic 执行策略（给 Claude Code 的操作指导）

当你作为 Claude Code / Cloud Agent 使用本 Skill 对简历评分时，请遵循以下步骤：

1. **读取岗位画像（Job Profile）**  
   - 如果工作流已经提供了 `job_profile` JSON，直接使用。  
   - 否则，从配置或数据库中读取对应 `job_id` 的岗位画像（例如 `database/jobs.json`）。  
   - 确保识别出：最低学历、经验年限、必备 / 加分技能、权重配置。

2. **解析简历为人才画像（Talent Profile）**（可复用 `match_resume` 步骤的输出）  
   - 通读 `resume_text`，提取：
     - 学历信息：最高学历、专业、院校
     - 工作经历：公司、时间、岗位、职责、成果
     - 项目经历：技术栈、规模、困难点与解决方案
     - 业务领域：所处行业和场景
     - 工程实践：测试、CI/CD、Code Review、性能优化等
   - 不需要把 Talent Profile 完整输出，但要在评分时引用这些信息。

3. **按维度独立打分（缺失信息处理）**  
   - 对 `education_score` / `experience_score` / `skill_score` / `engineering_score` / `domain_score` / `potential_score` 逐一评估。  
   - 每个维度都要在心里对应至少 1 条简历证据，并在最后写进 `evidence`。  
   - 如果某个维度在简历中几乎没有信息（例如完全看不到工程实践），默认给 3–5 分，并在 evidence 中明确说明「信息不足，仅基于有限信号给出保守估计」。  
   - 确保每项得分在 0–10 范围内，避免使用超过范围或非数字。

4. **计算综合分与决策**  
   - 根据岗位画像中的权重（或默认权重）计算 `total_score`。  
   - 根据得分和 `risk_flags` 选择合理的 `decision`。

5. **返回结构化 JSON（严格模式）**  
   - 最终回答只能是符合「输出 Schema」的 JSON。  
   - 不要在 JSON 外输出任何解释性文字；不要多余字段；不要输出 `null`，用 0 或空列表代替。  
   - 如无法给出合理评分，应尽量给出保守分数而不是报错，但要在 `risk_flags` 和 `evidence` 中充分说明不确定性。

---

## 五、使用示例（思考过程示例，仅供你内部推理）

> 注意：下面是你在内部推理时可以参考的示意，不要把这些文字原样输出给用户或下游脚本。

- 岗位：Python 后端工程师，要求本科以上，3 年以上 Python/Django 后端经验，有电商或 SaaS 经验优先。  
- 简历：某候选人 4 年后端经验，其中 3 年 Python/Django，主导过电商订单系统重构，提到使用 Redis、消息队列、Docker，有简单 CI/CD 经验。

内部评估大致为：

- education_score ≈ 8（本科，专业相关）  
- experience_score ≈ 8–9（经验年限与要求匹配略超）  
- skill_score ≈ 9–10（主栈与加分栈都较强）  
- engineering_score ≈ 7–8（有测试和 CI/CD，但描述不算特别深入）  
- domain_score ≈ 8（有电商经验）  
- potential_score ≈ 7–8（有承担重构项目的 owner 角色）  

然后按权重算出 total_score，并结合是否存在跳槽频繁/空档等 `risk_flags` 做最终决策。

