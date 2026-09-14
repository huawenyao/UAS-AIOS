# 进度 SSE

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `sse`

| 项 | 值 |
|----|----|
| **ID** | `sse` |
| **平面** | 使用平面 |
| **决策** | 自有 /hub/v1/exec/{task_id}/events |
| **本仓库角色** | 本产品组合（UI 在此，内核在 Hub） |
| **代码落点** | `services/hub-api/uas_hub/http_app.py` |
| **运行时** | GET /hub/v1/exec/{task_id}/events · 前台 EventSource |
| **切片** | `harness/slices/M1.md` |
| **需求** | `harness/requirements/REQ-UAS-M01.req.md` |

## 定位

Runtime 进度扇出。指挥舱只投影事件。审计才是真相源。

## 非职责

AG-UI 协议绑定、聊天流当状态

## 设计方案

Hub 持有事件缓冲。一线只见「待你确认」，不展示 workflow_id。

## 技术选型

FastAPI SSE · P1 Redis 扇出

## 接口

```
GET /hub/v1/exec/{task_id}/events
```

## 否决

- 把 AG-UI 当进度标准
- 把报告当回放源

## 验收

- 指挥舱与作战台同一 task_id

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 sse 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
