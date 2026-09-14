# M18 外环 · Temporal

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m18`

| 项 | 值 |
|----|----|
| **ID** | `m18` |
| **平面** | 运行面 |
| **决策** | 集成 · 须保留 HITL/续跑 |
| **本仓库角色** | 平台零件 · 不在本产品实现 |
| **代码落点** | `services/temporal-worker` |
| **运行时** | hub.exec.open → RuntimeCycleWorkflow |
| **切片** | `harness/slices/M18.md` |
| **需求** | `harness/requirements/REQ-UAS-M18.req.md` |

## 定位

任务寿命、审批暂停、精确续跑。业务用户只见「待你确认」。

## 非职责

解释 Law Pack、持 SoR 密钥

## 设计方案

Temporal UI 仅 SRE 逃生，禁止链到 WorkStudio。

## 技术选型

Temporal 1.25 · Python SDK

## 接口

```
hub.exec.open · hub.instance.cycle_step
```

## 否决

- Celery 当寿命
- 一线菜单出现 workflow_id

## 验收

- I-06 Worker 仍走门禁

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m18 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
