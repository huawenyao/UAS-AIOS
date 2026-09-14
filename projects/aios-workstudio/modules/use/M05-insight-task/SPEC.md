# M5 Insight→Task 编译器

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m5`

| 项 | 值 |
|----|----|
| **ID** | `m5` |
| **平面** | 使用平面（嵌在作战台） |
| **决策** | 自研 · 与 Hub 同进程 |
| **本仓库角色** | 本产品组合（UI 在此，内核在 Hub） |
| **代码落点** | `services/hub-api/uas_hub/insight_task.py` |
| **运行时** | CapabilityHub 同进程 · UI 嵌在作战台 |
| **切片** | `harness/slices/M5.md` |
| **需求** | `harness/requirements/REQ-UAS-M05.req.md` |

## 定位

把责任节点上的缺口编译成经营任务。任务必须带 source_node_id。未接地不得签发。不在签发时启动 Temporal。

## 非职责

外环寿命、连接器、口径公式

## 设计方案

insight.drill 收集 evidence_refs。task.issue 校验五件套、口径、接地、剖面。驳回原因进演化信号。

## 技术选型

Hub Python · insight/operating_task schema

## 接口

```
hub.scene.insight.drill · hub.scene.task.issue / return / transfer
```

## 否决

- 无源节点的任务
- 未接地派活
- 签发即启工作流

## 验收

- I-02 缺维不能签发
- I-04 未接地不能 issue

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m5 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
