# 蜂群智能体 · AI 招聘使用体验测试场景

> 基于 `configs/swarm_agents.json` 中定义的用户角色，对 `examples/ai-recruitment` 进行场景化体验测试与验收。

## 1. HR 招聘专员 (hr_recruiter)

| 场景 | 操作步骤 | 验收标准 | 依赖 |
|------|----------|----------|------|
| 发布新岗位并解析 JD | 执行 `/addJob [岗位描述]` 或等价操作 | 岗位写入 database/jobs.json，含解析后结构化字段 | 知识层 jd_parser.md、workflow parse_jd |
| 批量导入/粘贴简历并执行匹配 | 执行 `/match [岗位ID] [简历]` 或批量脚本 | 匹配结果写入 database/candidates.json，并生成报告 | workflow match_resume → score → report |
| 查看候选人排名与推荐报告 | 打开 reports/*.html 或 candidates.json | 报告可读，含得分与推荐结论；可排序查看 | scripts/generate_report.py |

**成功标准**：能无代码发布岗位、能批量处理简历、报告可读且含证据。

---

## 2. 招聘经理/用人部门负责人 (hiring_manager)

| 场景 | 操作步骤 | 验收标准 | 依赖 |
|------|----------|----------|------|
| 查看推荐名单与排名 | 查看 reports 或 database/candidates.json 排序结果 | 有明确排名与总分 | 匹配结果按 total_score 排序 |
| 查看单份候选人报告（得分、证据、风险） | 打开单份 candidate_*.html 或 JSON 中对应记录 | 报告含各维度得分、证据链、风险标识 | score 步骤的 evidence、risk_flags |
| 决定面试名单或要求补充信息 | 根据 decision（strong_recommend/recommend/borderline/not_recommend）做决策 | 决策档位清晰，可与证据对应 | evaluation_criteria.md |

**成功标准**：报告含决策依据、风险与证据清晰、可区分强推/推荐/待定。

---

## 3. 候选人（间接用户）(candidate)

| 场景 | 操作步骤 | 验收标准 | 依赖 |
|------|----------|----------|------|
| 简历被解析与评分的合理性 | 由招聘方使用系统对样本简历评分 | 评分维度与权重可解释、与 JD 一致 | evaluation_criteria.md、workflow |
| 可解释的筛选标准 | 查看评估标准文档与报告中的 evidence | 维度与档位公开，证据可追溯 | evaluation_criteria.md、evidence 输出 |
| 招聘方能否给出基于证据的反馈 | 报告是否含 evidence 列表 | 每条结论有对应证据引用 | score 步骤 output_schema |

**成功标准**：评分维度可解释、证据链可追溯、无隐藏偏见风险。

---

## 4. HR 运营/配置管理员 (hr_operations)

| 场景 | 操作步骤 | 验收标准 | 依赖 |
|------|----------|----------|------|
| 调整岗位评估维度与权重 | 修改 .claude/skills/evaluation_criteria.md 或岗位配置 | 下次匹配使用新权重/维度，无需改代码 | 知识驱动、workflow_config |
| 查看/导出结构化数据与审计记录 | 查看 database/candidates.json、reports/*.json | 数据可导出、含时间戳与完整得分 | database、reports |
| 确保输出符合合规与复盘需求 | 检查报告是否含可追溯说明 | 报告注明「可审计追溯」、结构化存储 | generate_report.py、output_schema |

**成功标准**：知识驱动可配置、数据可导出与审计、报告可追溯。

---

## 5. 面试官 (interviewer)

| 场景 | 操作步骤 | 验收标准 | 依赖 |
|------|----------|----------|------|
| 查看候选人匹配报告与证据 | 打开 candidate_*.html 或 candidates 中对应记录 | 能获取候选人画像与各维度得分、证据 | 报告与 database |
| 使用面试评估能力维度 | 执行 `/evaluate [候选人ID]`（若已实现） | 有专业/沟通/逻辑/文化契合等维度 | 面试评估扩展 |
| 将初筛结论与面试表现结合 | 参考 decision 与 evidence 设计面试问题 | 初筛结论与证据可支撑面试准备 | 报告内容完整性 |

**成功标准**：能获取候选人画像与证据、面试评估维度可用（若已实现）、与初筛结论一致。

---

## 执行方式

- **自动化部分**：运行 `scripts/swarm_ux_test_runner.py`，使用测试简历与现有岗位执行一次匹配流程，并基于能力矩阵与运行结果生成各角色体验结果。
- **人工/AI 辅助部分**：在 Cursor 中对 AI 说 `/addJob ...`、`/match ...` 等，观察是否符合上述场景与验收标准，并将结果纳入评估报告。
