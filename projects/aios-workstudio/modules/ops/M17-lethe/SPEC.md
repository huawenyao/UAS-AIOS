# M17 个人记忆 · Lethe

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m17`

| 项 | 值 |
|----|----|
| **ID** | `m17` |
| **平面** | K-L3 |
| **决策** | 集成 · 独立数据库 |
| **本仓库角色** | 平台零件 · 不在本产品实现 |
| **代码落点** | `services/hub-api/uas_hub/adapters/memory.py` |
| **运行时** | 独立库 uas_lethe |
| **切片** | `harness/slices/M17.md` |
| **需求** | `harness/requirements/REQ-UAS-M17.req.md` |

## 定位

仅 hub.memory.self.* 且 track=selfpaw。WorkStudio 经营轨不得读。

## 非职责

KPI、任务、客户主数据

## 设计方案

无 FK 到责任图。

## 技术选型

Lethe · Postgres uas_lethe

## 接口

```
hub.memory.self.*
```

## 否决

- Mem0 当默认
- 与 ag_node 同库

## 验收

- I-08 pipaw 403

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m17 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
