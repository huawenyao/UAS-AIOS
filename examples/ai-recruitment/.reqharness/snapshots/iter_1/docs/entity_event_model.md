# AI 招聘 UAS App：关键实体、事件与业务流程闭环

## 1. 问题与目标

当前 AI 招聘/面试 UAS App 若缺少以下能力，将难以形成**完整场景闭环**并与 **UAS-ASUI 原生 agent runtime** 叠合：

- **关键实体的结构化管理**：Job、Candidate、Task 等有统一 schema 与存储，而非松散 JSON。
- **事件控制**：如 AI 面试完成状态、业务通知与评价，由「事件」驱动而非散落逻辑。
- **业务流程完整闭环**：岗位 → 初筛 → 面试任务 → 完成 → 事件 → 通知与评价，一环扣一环。
- **技术架构叠合 UAS-ASUI**：与 `autonomous_agent` runtime 的 **task 级状态隔离**、**审计**、**知识驱动** 一致。

本文档描述上述设计与实现要点。

---

## 2. 关键实体结构化管理

| 实体 | 用途 | 存储 | 与 Runtime 关系 |
|------|------|------|------------------|
| **Job** | 岗位，含解析后画像与状态 | `database/jobs.json` | 业务上下文，供 Agent 注入 |
| **Candidate** | 候选人，含初筛得分、决策、状态 | `database/candidates.json` | 与 Task 关联，状态随事件推进 |
| **Task** | 可执行单元（初筛/AI面试/人工面试/评价审核） | `database/tasks.json` | **与 runtime_config.state_isolation: task_level 一一对应**，每个 Task 一次执行、可审计 |
| **Event** | 业务与运行时事件 | `database/events.json` | 驱动状态流转、触发通知与评价，并写入审计 |
| **Notification** | 业务通知（HR/招聘经理/候选人） | `database/notifications.json` | 由 Event 触发 |
| **Evaluation** | 评价（初筛/AI面试/人工面试/综合） | `database/evaluations.json` | 由「面试完成」类事件触发创建 |

**Schema 定义**：`configs/entity_schemas.json`  
**事件与触发策略**：`configs/event_policy.json`（事件类型、关联实体状态、下游动作 create_evaluation / notify_*）。

---

## 3. 事件控制与业务闭环

### 3.1 事件类型（与 event_policy 一致）

- `screening_completed`：简历初筛完成 → Candidate.status = screened  
- `candidate_shortlisted`：进入面试名单 → Candidate.status = shortlisted  
- `ai_interview_scheduled`：AI 面试排期 → Task 创建  
- `ai_interview_completed`：**AI 面试完成** → Task.status = completed，Candidate.status = interview_completed，**触发 create_evaluation + notify_recruiter**  
- `human_interview_completed`：人工面试完成 → 同上  
- `evaluation_updated`：评价更新 → notify_hiring_manager  

### 3.2 闭环流程示意

```
Job (open)
    ↓
Candidate (screened) ← screening_completed
    ↓
Task (type=ai_interview, status=pending → completed)
    ↓
Event: ai_interview_completed
    ↓
Evaluation 创建 + Notification（HR/招聘经理）
```

**完成状态**：由 Task.status = completed 与 Event 共同表达；业务通知与评价由事件策略自动创建，保证闭环。

---

## 4. 与 UAS-ASUI autonomous_agent runtime 叠合

| Runtime 能力 | 在本 App 中的对应 |
|--------------|-------------------|
| **state_isolation: task_level** | 每个 **Task** 为一次独立执行单元，状态（pending/running/completed）隔离在 task 级别 |
| **audit_enabled** | 实体写操作与事件写入 `database/audit/`，可追溯 |
| **context_injection** | Job/Candidate 作为上下文注入到 Agent 或 workflow 的 prompt/payload |
| **knowledge_driven** | 评估维度、事件策略等由 configs 与 knowledge 层驱动，不改代码即可调行为 |
| **human_checkpoints** | 可在 Task 或 Event 层挂接 WRITE_RISK / SYSTEM_OP 审批点（扩展实现） |

**配置文件**：  
- `configs/runtime_config.json`（若存在）：与 `projects/ai-recruitment-os` 的 runtime 配置一致，体现 task_level、audit_enabled。  
- 实体与事件由 `configs/entity_schemas.json`、`configs/event_policy.json` 定义，由 `scripts/entity_runtime.py` 执行。

---

## 5. 使用方式

- **初筛完成后**：可为每位候选人创建 `Task(type=screening)` 并 `complete_task`，或直接 `emit_event("screening_completed", job_id, candidate_id)`，以写入 Event 与可选 Notification。  
- **AI 面试完成后**：创建 `Task(type=ai_interview)`，结束时调用 `complete_task(task_id, result)`，runtime 将发布 `ai_interview_completed`、创建 Evaluation 与 Notification。  
- **CLI**：  
  `python scripts/entity_runtime.py create_task --type ai_interview --job-id job-1 --candidate-id cand_xxx`  
  `python scripts/entity_runtime.py complete_task --task-id task_xxx --result '{"dimensions":{...},"summary":"..."}'`  
  `python scripts/entity_runtime.py emit_event --event-type screening_completed --job-id job-1 --candidate-id cand_xxx`

---

## 6. 小结

- **关键实体**：Job、Candidate、Task、Event、Notification、Evaluation 已结构化管理，schema 与存储统一。  
- **事件控制**：AI 面试完成等状态通过 Task 完成 + Event 表达，业务通知与评价由事件策略触发，形成闭环。  
- **业务流程**：从岗位到初筛、面试任务、完成状态、事件、通知与评价的完整场景闭环已打通。  
- **技术架构**：与 UAS-ASUI 原生 agent runtime 的 task 级状态、审计、知识驱动叠合，便于扩展人工审批与更多事件类型。
