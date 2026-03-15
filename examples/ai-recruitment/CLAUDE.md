# AI 全自动招聘系统 (ASUI 验证项目)

## 系统概述

基于 ASUI 架构的 AI 招聘系统验证项目。岗位画像 + 简历匹配 + 面试评估，全流程知识驱动，初筛效率提升 5 倍。

## 核心命令

- `/start` - 启动招聘流程
- `/addJob [岗位描述]` - 添加岗位并解析 JD
- `/match [岗位ID] [简历]` - 简历匹配打分
- `/evaluate [候选人ID]` - 面试评估（多维度判定）

## 工作流

1. **岗位解析** - 从 JD 提取结构化要求（学历、经验、技能、薪资）
2. **简历匹配** - 多维度匹配打分（学历/经验/技能）
3. **初筛报告** - 生成可审计的推荐报告
4. **面试评估** - 能力维度判定（专业/沟通/逻辑/文化契合）

## 知识层

| 文件 | 用途 |
|------|------|
| configs/workflow_config.json | 招聘工作流定义 |
| configs/entity_schemas.json | 关键实体结构（Job/Candidate/Task/Event/Notification/Evaluation） |
| configs/event_policy.json | 事件类型与触发（完成状态→通知与评价） |
| configs/runtime_config.json | 与 UAS autonomous_agent runtime 对齐（task 级状态、审计） |
| .claude/skills/jd_parser.md | 岗位解析规则 |
| .claude/skills/evaluation_criteria.md | 评估标准 |
| docs/entity_event_model.md | 实体与事件闭环、与 agent runtime 叠合说明 |
| docs/产品价值感设计.md | 业务目标、场景痛点、解决度与价值感设计（让用户明显感知价值） |

## 验证标准

- [x] 知识驱动：修改 evaluation_criteria.md 即改变打分逻辑
- [x] 构建即运行：新增评估维度无需改代码
- [x] 结构化输出：匹配结果写入 database/candidates.json
- [x] 可审计：生成 HTML 报告含证据链

## 数据流与实体闭环

```
岗位(Job) → 解析(LLM) → 结构化要求
    ↓
简历 → 匹配(LLM) → 多维度打分 → Candidate(status=screened) + Event(screening_completed)
    ↓
报告生成(script) → reports/candidate_xxx.html
    ↓
Task(ai_interview) 完成 → Event(ai_interview_completed) → Evaluation + Notification
```

- **实体**：database/jobs.json, candidates.json, tasks.json, events.json, notifications.json, evaluations.json
- **事件驱动**：scripts/entity_runtime.py 负责 Task 完成 → 事件发布 → 通知与评价创建，与 runtime_config 的 task_level 状态、审计一致

## 运行产物

- `database/`：jobs.json, candidates.json, tasks.json, events.json, notifications.json, evaluations.json
- `database/audit/`：实体写操作审计（当 audit_enabled 时）
- `reports/`：candidate_*.html（带证据链与风险）、蜂群测试结果、价值评估报告
- 终端：运行 workflow_execution 后输出价值摘要（本批有效简历数、推荐/待定人数）
