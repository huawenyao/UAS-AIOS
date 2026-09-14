# M11 Audit

> 权威来源：`docs/strategic/design/uas-aios-cluster.html` · `m11`

| 项 | 值 |
|----|----|
| **ID** | `m11` |
| **平面** | 治理面 |
| **决策** | 自研追加写审计链 |
| **本仓库角色** | 本产品只经 hub.* 消费 |
| **代码落点** | `services/hub-api/uas_hub/hub.py` |
| **运行时** | Hub 审计链 |
| **切片** | `harness/slices/M11.md` |
| **需求** | `harness/requirements/REQ-UAS-M11.req.md` |

## 定位

按 correlation / node / cs 检索。不是 KPI 墙。

## 非职责

口径服务、指挥舱报表

## 设计方案

调用链入审计。ops 事件类型与 cs.invoked 区分。

## 技术选型

Postgres 分区表 · hash chain（P1）

## 接口

```
hub.ops.audit.search/export · hub.audit.query
```

## 否决

- 把 Cube 当审计

## 验收

- 可按 task_id / node_id 找回

## 脚手架纪律

- WorkStudio 一线只走北向 `hub.*`，禁止零件 SDK。
- 不得在 `projects/aios-workstudio` 内复制一份 m11 内核。
- 变更契约先改 `modules/catalog.json` 再重新生成本文件：`python modules/gen_specs.py`
